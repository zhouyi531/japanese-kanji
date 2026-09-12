/**
 * 漢字の庭 — Kanji Garden
 * Interactive kanji explorer with artistic design
 */

(function () {
    'use strict';

    // State
    let kanjiData = {};
    let relatedCache = {};  // Precomputed relationships
    let homophoneIndex = new Map();  // reading -> Map(word -> { meaning, owner kanji })
    const MAX_HOMOPHONES = 10;
    let activeKanji = null;
    let searchTerm = '';
    let currentPage = 1;
    const PAGE_SIZE = 200;  // kanji per page
    const MASTERED_KEY = 'kanji-garden:mastered:v1';
    const mastered = loadMastered();  // per-browser progress, stored locally

    // DOM refs
    const grid = document.getElementById('kanji-grid');
    const detailPanel = document.getElementById('detail-panel');
    const overlay = document.getElementById('overlay');
    const closeBtn = document.getElementById('close-panel');
    const searchInput = document.getElementById('search-input');
    const countEl = document.getElementById('kanji-count');
    const wordCountEl = document.getElementById('word-count');
    const paginationEl = document.getElementById('pagination');
    const pageInfoEl = document.getElementById('page-info');

    // Detail panel elements
    const detailChar = document.getElementById('detail-char');
    const detailMeaning = document.getElementById('detail-meaning');
    const onTags = document.getElementById('on-tags');
    const kunTags = document.getElementById('kun-tags');
    const compoundsList = document.getElementById('compounds-list');
    const relatedGrid = document.getElementById('related-grid');
    const masterBtn = document.getElementById('master-toggle');

    // ===== MASTERED PROGRESS (localStorage) =====
    function loadMastered() {
        try {
            const value = JSON.parse(localStorage.getItem(MASTERED_KEY) || '[]');
            return new Set(Array.isArray(value) ? value : []);
        } catch (e) {
            console.warn('Could not read mastered kanji:', e);
            return new Set();
        }
    }

    function saveMastered() {
        try { localStorage.setItem(MASTERED_KEY, JSON.stringify([...mastered])); }
        catch (e) { console.warn('Could not save mastered kanji:', e); }
    }

    function toggleMastered(char) {
        if (mastered.has(char)) mastered.delete(char);
        else mastered.add(char);
        saveMastered();
        const card = grid.querySelector(`.kanji-card[data-char="${char}"]`);
        if (card) card.classList.toggle('mastered', mastered.has(char));
        updateMasterUi(char);
    }

    function updateMasterUi(char) {
        const isMastered = mastered.has(char);
        masterBtn.classList.toggle('is-mastered', isMastered);
        masterBtn.setAttribute('aria-pressed', String(isMastered));
        masterBtn.textContent = isMastered ? '✓ 習得済み（取り消す）' : '習得済みにする';
        masteredCountEl.textContent = mastered.size;
    }
    const masteredCountEl = document.getElementById('mastered-count');

    // ===== INITIALIZATION =====
    async function init() {
        try {
            // The collector rewrites this file in place. Always revalidate it so a
            // browser session cannot hide newly collected entries behind HTTP cache.
            const resp = await fetch('data/kanji.json', { cache: 'no-store' });
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            kanjiData = await resp.json();
        } catch (e) {
            console.error('Failed to load kanji data:', e);
            grid.innerHTML = `<div class="empty-state"><div class="empty-icon">⚠️</div><p>Failed to load kanji data</p></div>`;
            return;
        }

        countEl.textContent = Object.keys(kanjiData).length;
        wordCountEl.textContent = Object.values(kanjiData)
            .reduce((total, entry) => total + (entry.c || []).length, 0);
        masteredCountEl.textContent = mastered.size;
        precomputeRelations();
        buildHomophoneIndex();
        renderGrid();
        setupEvents();
        initBackground();
    }

    // ===== GRID RENDERING =====
    function getFilteredChars() {
        const chars = Object.keys(kanjiData);
        if (!searchTerm) return chars;
        return chars.filter(char => matchesSearch(char, kanjiData[char], searchTerm));
    }

    function renderGrid() {
        const filtered = getFilteredChars();
        const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
        if (currentPage > totalPages) currentPage = totalPages;

        const start = (currentPage - 1) * PAGE_SIZE;
        const pageChars = filtered.slice(start, start + PAGE_SIZE);

        // Update count
        countEl.textContent = filtered.length;
        pageInfoEl.textContent = searchTerm
            ? `${filtered.length} matches · Page ${currentPage}/${totalPages}`
            : `Page ${currentPage} of ${totalPages}`;

        // Clear and rebuild grid
        grid.innerHTML = '';
        const fragment = document.createDocumentFragment();

        pageChars.forEach((char, i) => {
            const entry = kanjiData[char];
            const card = document.createElement('div');
            card.className = 'kanji-card';
            card.dataset.char = char;
            if (mastered.has(char)) card.classList.add('mastered');
            card.style.animationDelay = `${Math.min(i * 0.001, 0.3)}s`;

            // Apply states
            if (activeKanji) {
                if (char === activeKanji) card.classList.add('active');
                else if (isRelated(activeKanji, char)) card.classList.add('related');
                else card.classList.add('dimmed');
            }

            // Build tooltip content
            const onReading = entry.on.slice(0, 2).join(' · ');
            const kunReading = entry.kun.slice(0, 2).join(' · ');
            const readingDisplay = [onReading, kunReading].filter(Boolean).join(' / ') || '—';

            card.innerHTML = `
                <span class="char">${char}</span>
                <div class="tooltip">
                    <div class="t-reading">${escapeHtml(readingDisplay)}</div>
                    <div class="t-meaning">${escapeHtml(entry.m)}</div>
                </div>
            `;

            card.addEventListener('click', () => activateKanji(char));
            fragment.appendChild(card);
        });

        grid.appendChild(fragment);
        renderPagination(totalPages);
    }

    function renderPagination(totalPages) {
        paginationEl.innerHTML = '';
        if (totalPages <= 1) return;

        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = `page-btn ${currentPage === 1 ? 'disabled' : ''}`;
        prevBtn.textContent = '← Prev';
        prevBtn.addEventListener('click', () => goToPage(currentPage - 1));
        paginationEl.appendChild(prevBtn);

        // Page numbers
        const maxVisible = 7;
        let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
        let endPage = Math.min(totalPages, startPage + maxVisible - 1);
        if (endPage - startPage < maxVisible - 1) startPage = Math.max(1, endPage - maxVisible + 1);

        if (startPage > 1) {
            addPageBtn(1);
            if (startPage > 2) addEllipsis();
        }

        for (let p = startPage; p <= endPage; p++) {
            addPageBtn(p);
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) addEllipsis();
            addPageBtn(totalPages);
        }

        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = `page-btn ${currentPage === totalPages ? 'disabled' : ''}`;
        nextBtn.textContent = 'Next →';
        nextBtn.addEventListener('click', () => goToPage(currentPage + 1));
        paginationEl.appendChild(nextBtn);
    }

    function addPageBtn(page) {
        const btn = document.createElement('button');
        btn.className = `page-btn ${page === currentPage ? 'active' : ''}`;
        btn.textContent = page;
        btn.addEventListener('click', () => goToPage(page));
        paginationEl.appendChild(btn);
    }

    function addEllipsis() {
        const span = document.createElement('span');
        span.className = 'page-btn disabled';
        span.textContent = '…';
        paginationEl.appendChild(span);
    }

    function goToPage(page) {
        const filtered = getFilteredChars();
        const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
        if (page < 1 || page > totalPages) return;
        currentPage = page;
        renderGrid();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // ===== ACTIVATION (PIN) =====
    function activateKanji(char) {
        const entry = kanjiData[char];
        if (!entry) return;

        activeKanji = char;

        // Update card states
        document.querySelectorAll('.kanji-card').forEach(card => {
            card.classList.remove('active', 'related', 'dimmed');
            if (card.dataset.char === char) {
                card.classList.add('active');
            } else if (isRelated(char, card.dataset.char)) {
                card.classList.add('related');
            } else {
                card.classList.add('dimmed');
            }
        });

        // Populate detail panel
        populateDetail(char, entry);

        // Open panel
        detailPanel.classList.add('open');
        overlay.classList.add('visible');
        detailPanel.scrollTop = 0;
    }

    function deactivateKanji() {
        activeKanji = null;
        document.querySelectorAll('.kanji-card').forEach(card => {
            card.classList.remove('active', 'related', 'dimmed');
        });
        detailPanel.classList.remove('open');
        overlay.classList.remove('visible');
    }

    // ===== DETAIL PANEL =====
    function populateDetail(char, entry) {
        // Hero
        detailChar.textContent = char;
        detailMeaning.textContent = entry.m;
        updateMasterUi(char);

        // On readings
        onTags.innerHTML = '';
        if (entry.on.length > 0) {
            entry.on.forEach(r => {
                const tag = document.createElement('span');
                tag.className = 'reading-tag on';
                tag.textContent = r;
                onTags.appendChild(tag);
            });
            document.getElementById('on-readings').style.display = '';
        } else {
            document.getElementById('on-readings').style.display = 'none';
        }

        // Kun readings
        kunTags.innerHTML = '';
        if (entry.kun.length > 0) {
            entry.kun.forEach(r => {
                const tag = document.createElement('span');
                tag.className = 'reading-tag kun';
                tag.textContent = r;
                kunTags.appendChild(tag);
            });
            document.getElementById('kun-readings').style.display = '';
        } else {
            document.getElementById('kun-readings').style.display = 'none';
        }

        // Compounds
        compoundsList.innerHTML = '';
        if (entry.c && entry.c.length > 0) {
            entry.c.forEach(([word, reading, meaning]) => {
                const item = document.createElement('div');
                item.className = 'compound-item';
                item.dataset.word = word;

                // Highlight the active kanji in the compound word
                const highlightedWord = word.split('').map(c =>
                    c === char ? `<span class="highlight-char">${c}</span>` : c
                ).join('');

                item.innerHTML = `
                    <span class="compound-word">${highlightedWord}</span>
                    <span class="compound-reading">${escapeHtml(reading)}</span>
                    <span class="compound-meaning">${escapeHtml(meaning)}</span>
                `;
                appendHomophones(item, word, reading);

                // Hover on compound to highlight its kanji in the grid
                const otherKanji = [...word].filter(c => c !== char && kanjiData[c]);
                item.addEventListener('mouseenter', () => {
                    document.querySelectorAll('.kanji-card').forEach(card => {
                        if (otherKanji.includes(card.dataset.char)) {
                            card.classList.add('related');
                        }
                    });
                });
                item.addEventListener('mouseleave', () => {
                    document.querySelectorAll('.kanji-card.related').forEach(card => {
                        if (card.dataset.char !== activeKanji) {
                            card.classList.remove('related');
                        }
                    });
                });

                compoundsList.appendChild(item);
            });
        }

        // Related kanji - find kanji that appear together in compounds
        relatedGrid.innerHTML = '';
        const relatedChars = findRelatedKanji(char);
        relatedChars.forEach(rc => {
            const card = document.createElement('div');
            card.className = 'related-card';
            card.textContent = rc;
            card.title = kanjiData[rc]?.m || '';
            card.addEventListener('click', () => {
                activateKanji(rc);
            });
            relatedGrid.appendChild(card);
        });
    }

    // ===== RELATIONSHIP LOGIC =====
    function precomputeRelations() {
        // Build a map: for each kanji, which other kanji share compounds
        Object.keys(kanjiData).forEach(char => {
            const related = new Set();
            const entry = kanjiData[char];

            // 1. Kanji in same compound words
            if (entry.c) {
                entry.c.forEach(([word]) => {
                    for (const c of word) {
                        if (c !== char && kanjiData[c]) {
                            related.add(c);
                        }
                    }
                });
            }

            // 2. Other kanji whose compounds reference this one
            Object.entries(kanjiData).forEach(([k, v]) => {
                if (k === char) return;
                if (v.c) {
                    for (const [word] of v.c) {
                        if (word.includes(char)) {
                            related.add(k);
                            break;
                        }
                    }
                }
            });

            relatedCache[char] = [...related].slice(0, 30);
        });
    }

    // Homophones: other compound words anywhere in the dataset with the same reading.
    function buildHomophoneIndex() {
        homophoneIndex = new Map();
        Object.entries(kanjiData).forEach(([owner, entry]) => {
            (entry.c || []).forEach(([word, reading, meaning]) => {
                if (!reading || [...word].length < 2) return;  // multi-character words only
                if (!homophoneIndex.has(reading)) homophoneIndex.set(reading, new Map());
                const words = homophoneIndex.get(reading);
                if (!words.has(word)) words.set(word, { meaning, owner });
            });
        });
    }

    function appendHomophones(item, word, reading) {
        const others = [...(homophoneIndex.get(reading) || [])]
            .filter(([w]) => w !== word)
            .slice(0, MAX_HOMOPHONES);
        if (others.length === 0) return;

        const row = document.createElement('div');
        row.className = 'compound-homophones';
        const label = document.createElement('span');
        label.className = 'homophone-label';
        label.textContent = '同音';
        row.appendChild(label);
        others.forEach(([w, { meaning, owner }]) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'homophone-word';
            btn.textContent = w;
            btn.title = `${meaning || ''}（${owner}）`;
            btn.addEventListener('click', () => showCompound(owner, w));
            row.appendChild(btn);
        });
        item.appendChild(row);
    }

    // Open the kanji that lists this compound, then point at the compound itself.
    function showCompound(owner, word) {
        activateKanji(owner);
        const target = [...compoundsList.querySelectorAll('.compound-item')]
            .find(item => item.dataset.word === word);
        if (!target) return;
        target.scrollIntoView({ block: 'center', behavior: 'smooth' });
        target.classList.add('flash');
        setTimeout(() => target.classList.remove('flash'), 1600);
    }

    function findRelatedKanji(char) {
        return relatedCache[char] || [];
    }

    function isRelated(sourceChar, targetChar) {
        if (sourceChar === targetChar) return false;
        return (relatedCache[sourceChar] || []).includes(targetChar);
    }

    // ===== SEARCH =====
    function handleSearch(term) {
        searchTerm = term.trim().toLowerCase();
        currentPage = 1;  // Reset to first page on search
        renderGrid();
    }

    function matchesSearch(char, entry, term) {
        // Match by character itself
        if (char.includes(term)) return true;

        // Match by meaning
        if (entry.m.toLowerCase().includes(term)) return true;

        // Match by on reading
        if (entry.on.some(r => r.toLowerCase().includes(term))) return true;

        // Match by kun reading
        if (entry.kun.some(r => r.toLowerCase().includes(term))) return true;

        // Match by compound words
        if (entry.c) {
            for (const [word, reading, meaning] of entry.c) {
                if (word.includes(term) || reading.toLowerCase().includes(term) || meaning.toLowerCase().includes(term)) {
                    return true;
                }
            }
        }

        return false;
    }

    // ===== EVENTS =====
    function setupEvents() {
        closeBtn.addEventListener('click', deactivateKanji);
        masterBtn.addEventListener('click', () => {
            if (activeKanji) toggleMastered(activeKanji);
        });
        overlay.addEventListener('click', deactivateKanji);
        document.addEventListener('kanji:show-detail', event => {
            const char = event.detail?.char;
            if (char && kanjiData[char]) activateKanji(char);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (activeKanji) {
                    deactivateKanji();
                } else if (searchTerm) {
                    searchInput.value = '';
                    handleSearch('');
                    searchInput.blur();
                }
            }
        });

        // Debounced search
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                handleSearch(e.target.value);
            }, 150);
        });

        // Keyboard shortcut: / to focus search
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // ===== BACKGROUND PARTICLES =====
    function initBackground() {
        const canvas = document.getElementById('bg-canvas');
        const ctx = canvas.getContext('2d');
        let particles = [];
        let w, h;

        function resize() {
            w = canvas.width = window.innerWidth;
            h = canvas.height = window.innerHeight;
        }

        function createParticles() {
            particles = [];
            const count = Math.floor((w * h) / 25000);
            for (let i = 0; i < count; i++) {
                particles.push({
                    x: Math.random() * w,
                    y: Math.random() * h,
                    vx: (Math.random() - 0.5) * 0.15,
                    vy: (Math.random() - 0.5) * 0.15,
                    size: Math.random() * 1.5 + 0.5,
                    alpha: Math.random() * 0.15 + 0.03,
                    hue: Math.random() > 0.7 ? 15 : (Math.random() > 0.5 ? 45 : 220),
                });
            }
        }

        function animate() {
            ctx.clearRect(0, 0, w, h);

            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;

                // Wrap around
                if (p.x < 0) p.x = w;
                if (p.x > w) p.x = 0;
                if (p.y < 0) p.y = h;
                if (p.y > h) p.y = 0;

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = `hsla(${p.hue}, 40%, 60%, ${p.alpha})`;
                ctx.fill();
            });

            requestAnimationFrame(animate);
        }

        window.addEventListener('resize', () => {
            resize();
            createParticles();
        });

        resize();
        createParticles();
        animate();
    }

    // ===== UTILITIES =====
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Start
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
