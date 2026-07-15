#!/usr/bin/env python3
"""One-time offline build: merge public HSK 1-9 (HSK 3.0) word lists with
Han-Viet readings and Vietnamese meanings into data/hsk_vocab_full.json.

Not run at app startup — this is a dev-time script. Run it manually with:
    pip install -r scripts/requirements.txt
    python3 scripts/build_hsk_vocab.py

Sources (see plan/README for licenses):
  - krmanik/HSK-3.0            hanzi + pinyin + English gloss, official HSK 3.0 bands
  - ryanphung/chinese-hanviet-cognates   word-level Han-Viet reading + Vietnamese meaning
  - ph0ngp/CVDICT               CEDICT-format Chinese->Vietnamese dictionary (fallback meaning)
  - truyencuatui/VietPhrase      single-character Han-Viet reading table (fallback reading)
"""
import csv
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from pypinyin import Style, pinyin

ROOT = Path(__file__).resolve().parent.parent
CACHE = Path(__file__).resolve().parent / ".cache"
CACHE.mkdir(exist_ok=True)
OUT_DATA = ROOT / "data" / "hsk_vocab_full.json"
OUT_REPORT = ROOT / "data" / "hsk_vocab_report.json"

KRMANIK_BASE = "https://raw.githubusercontent.com/krmanik/HSK-3.0/main/New%20HSK%20(2021)/HSK%20List%20(Meaning)/HSK%20{}.tsv"
BANDS = ["1", "2", "3", "4", "5", "6", "7-9"]

COGNATES_URL = "https://raw.githubusercontent.com/ryanphung/chinese-hanviet-cognates/master/outputs/chinese-hanviet-cognates.tsv"
NONCOGNATES_URL = "https://raw.githubusercontent.com/ryanphung/chinese-hanviet-cognates/master/outputs/chinese-hanviet-non-cognates.tsv"
CVDICT_URL = "https://raw.githubusercontent.com/ph0ngp/CVDICT/main/CVDICT.u8"
VIETPHRASE_URL = "https://raw.githubusercontent.com/truyencuatui/VietPhrase/master/VietPhrase.txt"


def fetch_text(url: str, cache_name: str, encoding: str = "utf-8") -> str:
    path = CACHE / cache_name
    if not path.exists():
        print(f"Downloading {cache_name} ...", file=sys.stderr)
        urllib.request.urlretrieve(url, path)
    return path.read_bytes().decode(encoding)


# ---------- Parse krmanik HSK band lists ----------

def load_hsk_bands():
    """Returns {band: [(traditional, simplified, pinyin_raw, meaning_en), ...]}"""
    bands = {}
    for b in BANDS:
        text = fetch_text(KRMANIK_BASE.format(b), f"hsk_{b}.tsv")
        rows = []
        for line in text.splitlines():
            if not line.strip():
                continue
            cols = line.split("\t")
            if len(cols) < 3:
                continue
            trad, simp, py = cols[0], cols[1], cols[2]
            meaning_en = cols[3] if len(cols) > 3 else ""
            rows.append((trad.strip(), simp.strip(), py.strip(), meaning_en.strip()))
        bands[b] = rows
        print(f"HSK {b}: {len(rows)} words", file=sys.stderr)
    return bands


# ---------- Parse ryanphung word-level Han-Viet + meaning ----------

def load_ryanphung():
    """Returns dict simplified -> {hanviet, meaning, freq_rank} (first/most-frequent wins)."""
    out = {}

    def ingest(text):
        reader = csv.DictReader(text.splitlines(), delimiter="\t")
        for i, row in enumerate(reader):
            word = row.get("word", "").strip()
            if not word or word in out:
                continue
            out[word] = {
                "hanviet": row.get("hanviet", "").strip(),
                "meaning": row.get("meaning", "").strip(),
                "rank": i,
            }

    ingest(fetch_text(COGNATES_URL, "cognates.tsv"))
    ingest(fetch_text(NONCOGNATES_URL, "noncognates.tsv"))
    print(f"ryanphung word-level entries: {len(out)}", file=sys.stderr)
    return out


# ---------- Character-level Han-Viet fallback table ----------
#
# Primary source: derive per-character readings directly from ryanphung's
# word-level Han-Viet data itself — for every compound whose hanviet field
# splits into exactly as many syllables as the word has characters, align
# syllable[i] <-> char[i] and take a majority vote per character. This is
# far more reliable than a raw single-character lookup table, because a
# lone character's "first" translation is often a vernacular gloss rather
# than its actual Sino-Vietnamese reading (e.g. VietPhrase's entry for 薄
# is "mỏng" [=thin, a meaning] not "bạc" [=the actual Han-Viet reading]).
#
# Secondary/last-resort source: VietPhrase.txt single-character entries,
# for characters that never appear in an alignable ryanphung compound.

def build_char_table_from_ryanphung(ryanphung: dict):
    votes = {}
    for word, info in ryanphung.items():
        hv = info["hanviet"]
        if not hv:
            continue
        # ryanphung often lists several alternate whole-word readings for the
        # same word (tone-sandhi variants) separated by "/". Counting each
        # alternative as a full vote inflates ties for polyphonic characters
        # (every alternative of the same word "votes" for a different reading
        # of that character) — weight each word's contribution by 1/N so one
        # word can't outvote many other words that only offer one reading.
        alts = [a.strip() for a in hv.split("/") if a.strip()]
        valid_alts = [a.split(" ") for a in alts if len(a.split(" ")) == len(word) and all(a.split(" "))]
        if not valid_alts:
            continue
        weight = 1.0 / len(valid_alts)
        for syll in valid_alts:
            for ch, r in zip(word, syll):
                votes.setdefault(ch, Counter())[r.strip()] += weight
    table = {ch: c.most_common(1)[0][0] for ch, c in votes.items()}
    print(f"Char Han-Viet derived from ryanphung compounds: {len(table)} chars", file=sys.stderr)
    return table


def load_vietphrase_char_fallback():
    text = fetch_text(VIETPHRASE_URL, "vietphrase.txt", encoding="utf-16")
    out = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, val = line.split("=", 1)
        if len(key) != 1:
            continue
        reading = val.split("/")[0].strip().lower()
        if reading and key not in out:
            out[key] = reading
    print(f"VietPhrase single-char fallback entries: {len(out)}", file=sys.stderr)
    return out


def compose_hanviet(word: str, primary_table: dict, fallback_table: dict):
    parts = []
    missing = False
    used_fallback = False
    for ch in word:
        if ch in primary_table:
            parts.append(primary_table[ch])
        elif ch in fallback_table:
            parts.append(fallback_table[ch])
            used_fallback = True
        else:
            missing = True
    if not parts:
        return "", "missing"
    kind = "composed_partial" if missing else ("composed_fallback" if used_fallback else "composed")
    return " ".join(parts), kind


# ---------- Parse CVDICT (CEDICT-format Chinese->Vietnamese dictionary) ----------

CEDICT_LINE_RE = re.compile(r"^(\S+)\s+(\S+)\s+\[([^\]]*)\]\s+/(.*)/\s*$")
CLASSIFIER_RE = re.compile(r"CL:[^/]*")


def load_cvdict():
    """CEDICT format has one line per (word, pronunciation) pair — the same
    simplified word can appear multiple times (different readings/senses,
    including surname/proper-noun entries, which CEDICT convention marks by
    capitalizing the pinyin, e.g. "封 [Feng1] /surname Feng/"). Collect all
    lines per word, preferring lowercase-pinyin (common-word) senses over
    capitalized (proper-noun) ones, so a rare surname reading doesn't win
    just because it happened to sort first in the file.
    """
    text = fetch_text(CVDICT_URL, "cvdict.u8")
    common = {}
    proper = {}
    for line in text.splitlines():
        if not line or line.startswith("#") or line.startswith("%"):
            continue
        m = CEDICT_LINE_RE.match(line)
        if not m:
            continue
        _trad, simp, py, defs = m.groups()
        cleaned = CLASSIFIER_RE.sub("", defs)
        senses = [s.strip() for s in cleaned.split("/") if s.strip()]
        if not senses:
            continue
        bucket = proper if (py and py[0].isupper()) else common
        bucket.setdefault(simp, []).extend(senses)

    out = {}
    for simp in set(common) | set(proper):
        senses = common.get(simp) or proper.get(simp)
        # de-dup while preserving order
        seen = set()
        deduped = [s for s in senses if not (s in seen or seen.add(s))]
        out[simp] = deduped
    print(f"CVDICT entries: {len(out)}", file=sys.stderr)
    return out


# ---------- Pinyin (regenerated for consistent tone-mark + spacing) ----------

def to_pinyin(word: str) -> str:
    syllables = pinyin(word, style=Style.TONE, heteronym=False, errors="default")
    return " ".join(s[0] for s in syllables)


# ---------- Load existing hand-curated words to dedupe against ----------

def load_curated_simplified():
    sys.path.insert(0, str(ROOT))
    import seed_data  # noqa: E402

    return {w[0] for w in seed_data.get_words()}


def clean_vi_meaning(senses):
    text = ", ".join(senses[:4])  # cap at 4 senses, matches existing convention density
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    bands = load_hsk_bands()
    ryanphung = load_ryanphung()
    char_hanviet_primary = build_char_table_from_ryanphung(ryanphung)
    char_hanviet_fallback = load_vietphrase_char_fallback()
    cvdict = load_cvdict()
    curated = load_curated_simplified()

    # Flatten 1-6 directly; split "7-9" band into 3 tiers by frequency (ryanphung rank
    # when available, else original file order) — HSK 3.0 doesn't split 7-9 per-word
    # officially, this is an app-level convenience split.
    flat = []  # (level, trad, simp, pinyin_raw, meaning_en)
    for b in ["1", "2", "3", "4", "5", "6"]:
        for trad, simp, py, men in bands[b]:
            flat.append((int(b), trad, simp, py, men))

    band79 = bands["7-9"]
    ranked = sorted(
        range(len(band79)),
        key=lambda i: ryanphung.get(band79[i][1], {}).get("rank", 10**9 + i),
    )
    n = len(ranked)
    third = n // 3
    level_for_rank = {}
    for pos, idx in enumerate(ranked):
        if pos < third:
            level_for_rank[idx] = 7
        elif pos < 2 * third:
            level_for_rank[idx] = 8
        else:
            level_for_rank[idx] = 9
    for i, (trad, simp, py, men) in enumerate(band79):
        flat.append((level_for_rank[i], trad, simp, py, men))

    seen_simplified = set()
    words = []
    stats = {
        "hanviet_composed": 0, "hanviet_composed_fallback": 0,
        "hanviet_composed_partial": 0, "hanviet_missing": 0,
        "meaning_ryanphung": 0, "meaning_cvdict": 0, "meaning_english_fallback": 0,
        "skipped_curated_dup": 0, "skipped_dup_in_bulk": 0,
    }
    per_level_count = {}

    for level, trad, simp, py_raw, meaning_en in flat:
        if simp in curated:
            stats["skipped_curated_dup"] += 1
            continue
        if simp in seen_simplified:
            stats["skipped_dup_in_bulk"] += 1
            continue
        seen_simplified.add(simp)

        rp = ryanphung.get(simp)
        # Always compose the displayed reading from the per-character majority-vote
        # table rather than trusting ryanphung's word-level "hanviet" field verbatim:
        # that field often lists several alternate readings (tone-sandhi variants)
        # separated by "/" in file order, not frequency order, so blindly taking the
        # first alternative sometimes picks an uncommon reading (e.g. "địa上" first
        # alternative was "đích thướng" instead of the standard "địa thượng").
        hanviet, kind = compose_hanviet(simp, char_hanviet_primary, char_hanviet_fallback)
        stats[f"hanviet_{kind}"] += 1

        if rp and rp["meaning"]:
            meanings_vi = clean_vi_meaning(rp["meaning"].split("/"))
            stats["meaning_ryanphung"] += 1
        elif simp in cvdict:
            meanings_vi = clean_vi_meaning(cvdict[simp])
            stats["meaning_cvdict"] += 1
        else:
            meanings_vi = f"(EN) {meaning_en}" if meaning_en else ""
            stats["meaning_english_fallback"] += 1

        py = to_pinyin(simp) or py_raw

        words.append({
            "simplified": simp,
            "pinyin": py,
            "meanings": meanings_vi,
            "hsk_level": level,
            "sino_viet": hanviet,
        })
        per_level_count[level] = per_level_count.get(level, 0) + 1

    OUT_DATA.parent.mkdir(exist_ok=True)
    with open(OUT_DATA, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=1)

    report = {
        "total_words": len(words),
        "per_level_count": dict(sorted(per_level_count.items())),
        "stats": stats,
    }
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
