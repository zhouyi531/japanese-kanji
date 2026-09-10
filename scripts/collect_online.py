#!/usr/bin/env python3
"""Incrementally enrich data/kanji.json from public Japanese dictionary APIs."""
from __future__ import annotations

import argparse
import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KANJI_API = "https://kanjiapi.dev/v1/kanji/"
JISHO_API = "https://jisho.org/api/v1/search/words?keyword="
KANJI_RE = re.compile(r"[一-龯々]")
NAME_MARKERS = ("Place", "Company", "Organization", "Station", "Surname", "Given name", "Full name")

def get_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "KanjiGardenCollector/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)

def atomic_write(path: Path, value: object) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    temp.replace(path)

def clean_kun(value: str) -> str:
    return value.replace("-", "").strip()

def to_hiragana(value: str) -> str:
    return "".join(chr(ord(char) - 0x60) if "ァ" <= char <= "ヶ" else char for char in value)

def reading_targets(entry: dict) -> list[tuple[str, str, str]]:
    """Return (kind, display reading, normalized matching key)."""
    targets = [("on", value, to_hiragana(value)) for value in entry.get("on", []) if value]
    for value in entry.get("kun", []):
        clean = clean_kun(value)
        stem = clean.split(".", 1)[0]
        if stem:
            targets.append(("kun", value, to_hiragana(stem)))
    return targets

def kun_query_word(char: str, reading: str) -> str | None:
    """食 + た.べる -> 食べる; readings without okurigana have no exact form."""
    if "." not in reading:
        return None
    return char + clean_kun(reading).split(".", 1)[1]

def candidate_covers(candidate: dict, target: tuple[str, str, str], char: str) -> bool:
    kind, display, key = target
    reading = to_hiragana(candidate["reading"])
    if kind == "kun":
        exact_word = kun_query_word(char, display)
        if exact_word and candidate["word"] == exact_word:
            return True
        # Avoid claiming that a single kana appearing somewhere proves coverage.
        return len(key) >= 2 and (reading == key or reading.startswith(key))
    return len(key) >= 2 and key in reading

def parse_jisho(result: object, char: str, max_word_length: int, query_word: str | None = None) -> list[dict]:
    candidates: list[dict] = []
    for rank, item in enumerate(result.get("data", []) if isinstance(result, dict) else []):
        senses = item.get("senses", [])
        first_sense = senses[0] if senses else {}
        parts = first_sense.get("parts_of_speech", [])
        if any(marker in part for marker in NAME_MARKERS for part in parts):
            continue
        meaning = ", ".join(first_sense.get("english_definitions", []))
        for japanese in item.get("japanese", []):
            word, reading = japanese.get("word", ""), japanese.get("reading", "")
            if not word or char not in word or not reading or not KANJI_RE.search(word):
                continue
            if len(word) > max_word_length:
                continue
            score = (100 if item.get("is_common") else 0) + max(0, 30 - rank)
            score += max(0, 12 - len(word) * 2)
            if query_word and word == query_word:
                score += 80
            candidates.append({"word": word, "reading": reading, "meaning": meaning,
                               "common": bool(item.get("is_common")), "score": score})
    return candidates

def get_candidates(char: str, entry: dict, max_word_length: int) -> list[dict]:
    candidates: list[dict] = []
    queries: list[tuple[str, str | None]] = [(f"{char} #common", None), (char, None)]
    for reading in entry.get("on", []):
        if reading:
            queries.append((f"{char} {to_hiragana(reading)}", None))
    for reading in entry.get("kun", []):
        word = kun_query_word(char, reading)
        if word:
            queries.append((word, word))
    seen_queries: set[str] = set()
    for query, exact in queries:
        if query in seen_queries:
            continue
        seen_queries.add(query)
        result = get_json(JISHO_API + urllib.parse.quote(query))
        candidates.extend(parse_jisho(result, char, max_word_length, exact))
    best: dict[tuple[str, str], dict] = {}
    for candidate in candidates:
        key = (candidate["word"], candidate["reading"])
        if key not in best or candidate["score"] > best[key]["score"]:
            best[key] = candidate
    return sorted(best.values(), key=lambda item: (-item["score"], len(item["word"]), item["word"]))

def select_coverage_words(char: str, entry: dict, candidates: list[dict], max_words: int) -> tuple[list[dict], set[str]]:
    targets = reading_targets(entry)
    covered: set[str] = set()
    for row in entry.get("c", []):
        if len(row) < 2:
            continue
        existing = {"word": row[0], "reading": row[1]}
        covered.update(display for target in targets if candidate_covers(existing, target, char)
                       for display in [target[1]])

    selected: list[dict] = []
    used = {row[0] for row in entry.get("c", []) if row}
    # First maximize reading coverage, preferring common and short candidates.
    for target in targets:
        display = target[1]
        if display in covered:
            continue
        match = next((item for item in candidates
                      if item["word"] not in used and candidate_covers(item, target, char)), None)
        if match:
            selected.append(match); used.add(match["word"]); covered.add(display)
            if len(selected) >= max_words:
                return selected, covered
    # Then fill the remaining budget with the best common candidates.
    for item in candidates:
        if item["word"] in used:
            continue
        selected.append(item); used.add(item["word"])
        if len(selected) >= max_words:
            break
    return selected, covered

def collect_one(char: str, entry: dict, max_words: int, max_word_length: int,
                coverage_first: bool) -> tuple[dict, int, int, int]:
    added = 0
    try:
        detail = get_json(KANJI_API + urllib.parse.quote(char))
        if isinstance(detail, dict):
            entry["on"] = list(dict.fromkeys(entry.get("on", []) + detail.get("on_readings", [])))
            entry["kun"] = list(dict.fromkeys(entry.get("kun", []) + [clean_kun(x) for x in detail.get("kun_readings", [])]))
            if not entry.get("m") and detail.get("meanings"):
                entry["m"] = ", ".join(detail["meanings"])
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"kanjiapi {char}: {exc}")

    try:
        candidates = get_candidates(char, entry, max_word_length)
        if coverage_first:
            selected, covered = select_coverage_words(char, entry, candidates, max_words)
        else:
            known = {row[0] for row in entry.get("c", []) if row}
            selected = [item for item in candidates if item["word"] not in known][:max_words]
            covered = set()
        for item in selected:
            entry.setdefault("c", []).append([item["word"], item["reading"], item["meaning"]])
            added += 1
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"jisho {char}: {exc}")
        covered = set()
    targets = reading_targets(entry)
    if not covered:
        _, covered = select_coverage_words(char, entry, [], 0)
    return entry, added, len(covered), len(targets)

def run(path: Path, batch: int, max_words: int, new_kanji: int,
        max_word_length: int, coverage_first: bool, checkpoint_every: int) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    added_chars: list[str] = []
    if new_kanji:
        try:
            online_chars = get_json(KANJI_API + "joyo")
            missing = [char for char in online_chars if char not in data]
            random.shuffle(missing)
            added_chars = missing[:new_kanji]
        except (urllib.error.URLError, TimeoutError, ValueError, TypeError) as exc:
            print(f"kanji list: {exc}")
    existing_chars = list(data)
    random.shuffle(existing_chars)
    chars = added_chars + existing_chars
    total = 0
    covered_total = target_total = 0
    pass_size = max(batch, len(added_chars))
    selected_chars = chars[:min(pass_size, len(chars))]
    for processed, char in enumerate(selected_chars, 1):
        if char not in data:
            data[char] = {"on": [], "kun": [], "m": "", "c": []}
            print(f"new kanji: {char}")
        data[char], added, covered, targets = collect_one(
            char, data[char], max_words, max_word_length, coverage_first)
        total += added
        covered_total += covered; target_total += targets
        print(f"{char}: +{added} words; reading coverage {covered}/{targets}")
        if processed % checkpoint_every == 0:
            atomic_write(path, data)
            print(f"checkpoint: {processed}/{len(selected_chars)} processed -> {path}")
        time.sleep(0.35)
    atomic_write(path, data)
    print(f"saved {len(data)} kanji; added {total} words -> {path}")
    if coverage_first:
        print(f"processed reading coverage: {covered_total}/{target_total} (heuristic)")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data/kanji.json")
    parser.add_argument("--batch", type=int, default=20, help="kanji processed per pass")
    parser.add_argument("--max-words", type=int, default=5, help="new compounds per kanji")
    parser.add_argument("--new-kanji", type=int, default=3, help="new joyo kanji added per pass")
    parser.add_argument("--max-word-length", type=int, default=6, help="reject longer words/names")
    parser.add_argument("--coverage-first", action=argparse.BooleanOptionalAction, default=True,
                        help="prioritize common words that cover distinct on/kun readings")
    parser.add_argument("--checkpoint-every", type=int, default=1,
                        help="atomically save after every N processed kanji (default: 1)")
    parser.add_argument("--interval", type=int, default=0, help="repeat every N seconds; 0 runs once")
    args = parser.parse_args()
    while True:
        run(args.data, max(1, args.batch), max(1, args.max_words), max(0, args.new_kanji),
            max(1, args.max_word_length), args.coverage_first, max(1, args.checkpoint_every))
        if args.interval <= 0: break
        time.sleep(max(60, args.interval))

if __name__ == "__main__":
    main()
