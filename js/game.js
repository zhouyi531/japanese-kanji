(function () {
    'use strict';

    const screen = document.getElementById('game-screen');
    const field = document.getElementById('game-field');
    const target = document.getElementById('game-target');
    const shot = document.getElementById('game-shot');
    const message = document.getElementById('game-message');
    const answers = document.getElementById('game-answers');
    const startButton = document.getElementById('game-start');
    const scoreEl = document.getElementById('game-score');
    const comboEl = document.getElementById('game-combo');
    const heartsEl = document.getElementById('game-hearts');
    const promptEl = document.getElementById('game-prompt');
    const mistakePanel = document.getElementById('mistake-panel');
    const mistakeList = document.getElementById('mistake-list');
    const mistakeEmpty = document.getElementById('mistake-empty');
    const mistakeReview = document.getElementById('mistake-review');
    const mistakeClear = document.getElementById('mistake-clear');
    const mistakeCount = document.getElementById('mistake-count');
    const STORAGE_KEY = 'kanji-garden-mistakes-v1';
    const API_PATH = 'api/mistakes';
    let syncTimer = 0;
    let data = {}, pool = [], running = false, timer = 0, frame = 0;
    let score = 0, combo = 0, lives = 3, mode = 'mixed', current = null, startAt = 0, accepting = false;
    let reviewingMistakes = false;
    const roundMs = 7200;

    async function ensureData() {
        if (Object.keys(data).length) return;
        const response = await fetch('data/kanji.json', { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        data = await response.json();
        buildPool();
    }

    function cleanReading(value) { return value.replace(/\./g, ''); }
    function buildPool() {
        pool = [];
        Object.entries(data).forEach(([char, entry]) => {
            const readings = [...(entry.on || []), ...(entry.kun || [])].map(cleanReading).filter(Boolean);
            if (readings.length) pool.push({ type: 'kanji', text: char, reading: readings[0], accepted: readings });
            (entry.c || []).forEach(([word, reading]) => {
                if (word && reading && /[一-龯々]/.test(word)) pool.push({ type: 'word', text: word, reading, accepted: [reading] });
            });
        });
    }

    function candidates() { return pool.filter(item => mode === 'mixed' || item.type === mode); }
    function mistakeId(item) { return `${item.type}:${item.text}:${item.reading}`; }

    // The notebook lives in localStorage for instant use and offline fallback,
    // and is mirrored to the server so it survives restarts and other browsers.
    function apiEnabled() { return /^https?:$/.test(window.location.protocol); }
    async function apiCall(method, body, suffix = '') {
        const response = await fetch(API_PATH + suffix, {
            method,
            cache: 'no-store',
            headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
            body: body === undefined ? undefined : JSON.stringify(body)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const text = await response.text();
        return text ? JSON.parse(text) : null;
    }
    function loadMistakes() {
        try {
            const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            return Array.isArray(value) ? value : [];
        } catch (_) { return []; }
    }
    function saveMistakes(items) {
        try { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); }
        catch (error) { console.warn('Could not save review notebook:', error); }
        renderMistakes();
        scheduleSync();
    }
    function scheduleSync() {
        if (!apiEnabled()) return;
        clearTimeout(syncTimer);
        syncTimer = window.setTimeout(pushMistakes, 200);
    }
    async function pushMistakes() {
        if (!apiEnabled()) return;
        try { await apiCall('PUT', { items: loadMistakes() }); }
        catch (error) { console.warn('Could not sync review notebook to server:', error); }
    }
    function mergeMistakes(remote, local) {
        const merged = remote.map(item => ({ ...item }));
        const index = new Map(merged.map((item, at) => [item.id, at]));
        local.forEach(item => {
            const at = index.get(item.id);
            if (at === undefined) {
                index.set(item.id, merged.length);
                merged.push({ ...item });
                return;
            }
            const kept = merged[at];
            kept.wrongCount = Math.max(kept.wrongCount || 1, item.wrongCount || 1);
            if (!kept.accepted || !kept.accepted.length) kept.accepted = item.accepted || [];
            if ((item.lastWrongAt || '') > (kept.lastWrongAt || '')) {
                kept.lastWrongAt = item.lastWrongAt;
                kept.reason = item.reason;
            }
        });
        return merged;
    }
    async function syncFromServer() {
        if (!apiEnabled()) return;
        let remote;
        try { remote = await apiCall('GET'); }
        catch (error) { console.warn('Could not load review notebook from server:', error); return; }
        if (!Array.isArray(remote)) return;
        if (!remote.length) {
            // First run with persistence enabled: keep whatever this browser has.
            if (loadMistakes().length) pushMistakes();
            return;
        }
        const local = loadMistakes();
        const merged = mergeMistakes(remote, local);
        try { localStorage.setItem(STORAGE_KEY, JSON.stringify(merged)); }
        catch (error) { console.warn('Could not cache review notebook:', error); }
        renderMistakes();
        if (JSON.stringify(merged) !== JSON.stringify(remote)) pushMistakes();
    }
    function recordMistake(reason) {
        if (!current) return;
        const items = loadMistakes();
        const id = mistakeId(current);
        const found = items.find(item => item.id === id);
        if (found) {
            found.wrongCount = (found.wrongCount || 1) + 1;
            found.lastWrongAt = new Date().toISOString();
            found.reason = reason;
        } else {
            items.unshift({
                id, type: current.type, text: current.text, reading: current.reading,
                accepted: current.accepted, wrongCount: 1,
                lastWrongAt: new Date().toISOString(), reason
            });
        }
        saveMistakes(items);
    }
    function renderMistakes() {
        const items = loadMistakes();
        mistakeCount.textContent = items.length;
        mistakeEmpty.hidden = items.length > 0;
        mistakeReview.disabled = items.length === 0;
        mistakeClear.disabled = items.length === 0;
        mistakeList.innerHTML = '';
        items.forEach(item => {
            const row = document.createElement('article');
            row.className = 'mistake-row';
            const content = document.createElement('div');
            const text = document.createElement('strong');
            text.className = 'mistake-word';
            [...item.text].forEach(char => {
                if (/[一-龯]/.test(char)) {
                    const link = document.createElement('button');
                    link.type = 'button'; link.className = 'mistake-kanji-link';
                    link.textContent = char; link.title = `${char}の情報を見る`;
                    link.addEventListener('click', () => {
                        closeMistakes();
                        document.dispatchEvent(new CustomEvent('kanji:show-detail', { detail: { char } }));
                    });
                    text.appendChild(link);
                } else {
                    text.appendChild(document.createTextNode(char));
                }
            });
            const reading = document.createElement('span');
            reading.className = 'mistake-reading'; reading.textContent = `【${item.reading}】`;
            const meta = document.createElement('small');
            meta.textContent = `${item.type === 'word' ? '単語' : '漢字'} · ${item.wrongCount || 1}回間違い`;
            content.append(text, reading, meta);
            const remove = document.createElement('button');
            remove.type = 'button'; remove.className = 'mistake-delete'; remove.textContent = '削除';
            remove.addEventListener('click', () => saveMistakes(loadMistakes().filter(x => x.id !== item.id)));
            row.append(content, remove); mistakeList.appendChild(row);
        });
    }
    function shuffle(items) {
        for (let i = items.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [items[i], items[j]] = [items[j], items[i]];
        }
        return items;
    }

    function nextRound() {
        if (!running) return;
        const saved = loadMistakes();
        const savedIds = new Set(saved.map(item => item.id));
        const choices = reviewingMistakes
            ? pool.filter(item => savedIds.has(mistakeId(item)))
            : candidates();
        if (!choices.length) { gameOver(); return; }
        current = choices[Math.floor(Math.random() * choices.length)];
        const distractors = shuffle([...new Set(pool.map(x => x.reading).filter(x => !current.accepted.includes(x)))].slice()).slice(0, 3);
        const labels = shuffle([current.reading, ...distractors]);
        target.textContent = current.text;
        target.className = `game-target ${current.type}`;
        target.style.left = `${12 + Math.random() * 76}%`;
        answers.innerHTML = '';
        message.className = 'game-message';
        labels.forEach((label, index) => {
            const button = document.createElement('button');
            button.type = 'button';
            button.textContent = label;
            button.dataset.reading = label;
            button.innerHTML = `<span>${index + 1}</span>${label}`;
            button.addEventListener('click', choose);
            answers.appendChild(button);
        });
        startAt = performance.now();
        accepting = true;
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(fall);
    }

    function fall(now) {
        if (!running || !current || !accepting) return;
        const progress = Math.min(1, (now - startAt) / roundMs);
        target.style.top = `${8 + progress * 68}%`;
        if (progress >= 1) { damage('時間切れ！'); return; }
        frame = requestAnimationFrame(fall);
    }

    function choose(event) {
        if (!running || !current) return;
        const picked = event.currentTarget.dataset.reading;
        if (current.accepted.includes(picked)) hit();
        else {
            event.currentTarget.classList.add('wrong');
            damage('読み方が違う！');
        }
    }

    function hit() {
        accepting = false;
        cancelAnimationFrame(frame);
        combo += 1;
        score += 100 + combo * 10;
        shot.style.setProperty('--shot-x', `${target.offsetLeft + target.offsetWidth / 2}px`);
        shot.style.setProperty('--shot-y', `${target.offsetTop + target.offsetHeight / 2}px`);
        shot.classList.remove('fire'); void shot.offsetWidth; shot.classList.add('fire');
        target.classList.add('destroyed');
        showMessage(`命中！ ${current.text}【${current.reading}】`, 'good');
        updateHud();
        timer = window.setTimeout(nextRound, 650);
    }

    function damage(text) {
        if (!accepting) return;
        accepting = false;
        cancelAnimationFrame(frame);
        recordMistake(text.includes('時間') ? 'timeout' : 'wrong');
        lives -= 1; combo = 0;
        field.classList.remove('damaged'); void field.offsetWidth; field.classList.add('damaged');
        target.classList.add('crashed');
        showMessage(`${text} 正解：${current.reading}`, 'bad');
        updateHud();
        if (lives <= 0) window.setTimeout(gameOver, 700);
        else timer = window.setTimeout(nextRound, 900);
    }

    function showMessage(text, type) { message.textContent = text; message.className = `game-message show ${type}`; }
    function updateHud() {
        scoreEl.textContent = score; comboEl.textContent = combo;
        heartsEl.textContent = `${'♥ '.repeat(lives)}${'♡ '.repeat(3 - lives)}`.trim();
    }
    function start() {
        clearTimeout(timer); score = 0; combo = 0; lives = 3; running = true;
        startButton.hidden = true; message.className = 'game-message'; updateHud(); nextRound();
    }
    function gameOver() {
        running = false; current = null; accepting = false; cancelAnimationFrame(frame);
        target.textContent = ''; answers.innerHTML = '';
        showMessage(`GAME OVER · 得点 ${score}`, 'bad');
        startButton.textContent = 'もう一度'; startButton.hidden = false;
    }
    function close() {
        running = false; current = null; accepting = false; clearTimeout(timer); cancelAnimationFrame(frame);
        screen.classList.remove('open'); screen.setAttribute('aria-hidden', 'true'); document.body.classList.remove('game-active');
    }

    function openMistakes() {
        renderMistakes(); syncFromServer(); mistakePanel.classList.add('open');
        mistakePanel.setAttribute('aria-hidden', 'false');
    }
    function closeMistakes() {
        mistakePanel.classList.remove('open'); mistakePanel.setAttribute('aria-hidden', 'true');
    }

    document.getElementById('game-open').addEventListener('click', async () => {
        try { await ensureData(); } catch (error) { console.error(error); return; }
        reviewingMistakes = false; promptEl.textContent = '正しい読み方を選んで迎撃せよ';
        document.querySelectorAll('.game-mode').forEach(x => x.classList.toggle('active', x.dataset.mode === mode));
        screen.classList.add('open'); screen.setAttribute('aria-hidden', 'false'); document.body.classList.add('game-active'); start();
    });
    document.getElementById('game-close').addEventListener('click', close);
    startButton.addEventListener('click', start);
    document.querySelectorAll('.game-mode').forEach(button => button.addEventListener('click', () => {
        reviewingMistakes = false; promptEl.textContent = '正しい読み方を選んで迎撃せよ';
        mode = button.dataset.mode;
        document.querySelectorAll('.game-mode').forEach(x => x.classList.toggle('active', x === button));
        if (running) { clearTimeout(timer); nextRound(); }
    }));
    document.getElementById('mistake-open').addEventListener('click', openMistakes);
    document.getElementById('mistake-close').addEventListener('click', closeMistakes);
    mistakePanel.addEventListener('click', event => { if (event.target === mistakePanel) closeMistakes(); });
    mistakeClear.addEventListener('click', () => {
        if (window.confirm('錯題をすべて削除しますか？')) saveMistakes([]);
    });
    mistakeReview.addEventListener('click', async () => {
        try { await ensureData(); } catch (error) { console.error(error); return; }
        if (!loadMistakes().length) return;
        reviewingMistakes = true; promptEl.textContent = '錯題だけを復習中';
        document.querySelectorAll('.game-mode').forEach(x => x.classList.remove('active'));
        closeMistakes(); screen.classList.add('open'); screen.setAttribute('aria-hidden', 'false');
        document.body.classList.add('game-active'); start();
    });
    document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && mistakePanel.classList.contains('open')) { closeMistakes(); return; }
        if (!screen.classList.contains('open')) return;
        if (event.key === 'Escape') close();
        const index = Number(event.key) - 1;
        if (index >= 0 && index < answers.children.length) answers.children[index].click();
    });
    renderMistakes();
    syncFromServer();
})();
