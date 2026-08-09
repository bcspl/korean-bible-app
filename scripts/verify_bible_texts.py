#!/usr/bin/env python3
"""
Verify app Bible JSONs (KRV / KJV / ASV) against:
- Protestant canon structure (66 books, standard chapter counts)
- Re-parsed PD sources (KJV OSIS, ASV Zefania from seven1m/open-bibles)
- Unbound Korean complete dump structure alignment with KJV
- Golden-verse spot checks for well-known PD wording
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
CACHE = ROOT / "scripts" / "_bible_cache"

CANON_CHAPTERS = {
    "Gen": 50, "Exod": 40, "Lev": 27, "Num": 36, "Deut": 34, "Josh": 24,
    "Judg": 21, "Ruth": 4, "1Sam": 31, "2Sam": 24, "1Kgs": 22, "2Kgs": 25,
    "1Chr": 29, "2Chr": 36, "Ezra": 10, "Neh": 13, "Esth": 10, "Job": 42,
    "Ps": 150, "Prov": 31, "Eccl": 12, "Song": 8, "Isa": 66, "Jer": 52,
    "Lam": 5, "Ezek": 48, "Dan": 12, "Hos": 14, "Joel": 3, "Amos": 9,
    "Obad": 1, "Jonah": 4, "Mic": 7, "Nah": 3, "Hab": 3, "Zeph": 3,
    "Hag": 2, "Zech": 14, "Mal": 4, "Matt": 28, "Mark": 16, "Luke": 24,
    "John": 21, "Acts": 28, "Rom": 16, "1Cor": 16, "2Cor": 13, "Gal": 6,
    "Eph": 6, "Phil": 4, "Col": 4, "1Thess": 5, "2Thess": 3, "1Tim": 6,
    "2Tim": 4, "Titus": 3, "Phlm": 1, "Heb": 13, "Jas": 5, "1Pet": 5,
    "2Pet": 3, "1John": 5, "2John": 1, "3John": 1, "Jude": 1, "Rev": 22,
}

# Classic KJV verse totals for key books (1769 tradition)
KJV_BOOK_VERSES = {
    "Gen": 1533, "2Chr": 822, "Job": 1070, "Ps": 2461, "1Pet": 105,
    "Matt": 1071, "Luke": 1151, "John": 879, "Rev": 404, "Rom": 433,
}


def normalize(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def load_index(path: Path) -> tuple[dict, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    m: dict = {}
    for b in data["books"]:
        m[b["book"]] = {
            c["chapter"]: {v["verse"]: v["text"] for v in c["verses"]}
            for c in b["chapters"]
        }
    return data, m


def total_verses(m: dict) -> int:
    return sum(len(vs) for chs in m.values() for vs in chs.values())


def main() -> int:
    failures: list[str] = []
    print("=" * 60)
    print("BIBLE TEXT VERIFICATION REPORT")
    print("=" * 60)

    paths = {
        "KRV": DATA / "kor_bible_full.json",
        "KJV": DATA / "eng_kjv_full.json",
        "ASV": DATA / "eng_asv_full.json",
    }
    versions = {k: load_index(p) for k, p in paths.items()}

    # A. Structure
    print("\n[A] STRUCTURE vs Protestant canon")
    for name, (meta, m) in versions.items():
        ch_bad = [
            (b, len(m.get(b, {})), n)
            for b, n in CANON_CHAPTERS.items()
            if len(m.get(b, {})) != n
        ]
        empty = sum(
            1
            for chs in m.values()
            for vs in chs.values()
            for t in vs.values()
            if not str(t).strip()
        )
        tv = total_verses(m)
        print(
            f"  {name}: books={len(m)} verses={tv} empty={empty} "
            f"chapter_mismatches={len(ch_bad)}"
        )
        if ch_bad:
            print("    BAD:", ch_bad[:12])
            failures.append(f"{name} chapter mismatches: {ch_bad}")
        if empty:
            failures.append(f"{name} has {empty} empty verses")
        if len(m) != 66:
            failures.append(f"{name} book count {len(m)} != 66")

    # B. KJV/ASV classic book verse totals
    print("\n[B] KJV/ASV book verse totals (classic 1769 map)")
    for name in ("KJV", "ASV"):
        m = versions[name][1]
        for b, expect in KJV_BOOK_VERSES.items():
            got = sum(len(m[b][c]) for c in m[b])
            ok = got == expect
            print(f"  {name} {b}: {got} (expect {expect}) {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append(f"{name} {b} verses {got}!={expect}")

    # C. Cross-version alignment KJV==ASV structure; KRV==KJV structure
    print("\n[C] Cross-version verse-map alignment")
    _, krv = versions["KRV"]
    _, kjv = versions["KJV"]
    _, asv = versions["ASV"]
    diff_ka = 0
    diff_kr = 0
    samples_ka = []
    samples_kr = []
    for b, nch in CANON_CHAPTERS.items():
        for c in range(1, nch + 1):
            kv = set(kjv.get(b, {}).get(c, {}))
            av = set(asv.get(b, {}).get(c, {}))
            rv = set(krv.get(b, {}).get(c, {}))
            if kv != av:
                diff_ka += 1
                if len(samples_ka) < 8:
                    samples_ka.append((b, c, sorted(kv - av)[:5], sorted(av - kv)[:5]))
            if kv != rv:
                diff_kr += 1
                if len(samples_kr) < 8:
                    samples_kr.append((b, c, sorted(kv - rv)[:5], sorted(rv - kv)[:5]))
    print(f"  KJV vs ASV verse-set chapter diffs: {diff_ka}")
    print(f"  KJV vs KRV verse-set chapter diffs: {diff_kr}")
    if samples_ka:
        print("  KJV/ASV samples:", samples_ka)
    if samples_kr:
        print("  KJV/KRV samples:", samples_kr)
    if diff_ka:
        failures.append(f"KJV/ASV structure diffs: {diff_ka}")
    # KRV vs KJV may differ slightly due to versification (e.g. 2 Cor 13:14,
    # 3 John 14/15, Ps 72:20). Report but only fail if large.
    if diff_kr > 20:
        failures.append(f"KJV/KRV structure diffs too high: {diff_kr}")
    elif diff_kr:
        print(
            f"  NOTE: {diff_kr} KRV/KJV versification differences "
            f"(expected for Korean vs English numbering)"
        )

    # D. Golden verses
    print("\n[D] Golden verse spot-checks (authoritative PD wording)")
    golden = [
        ("KJV", "Gen", 1, 1, "In the beginning God created the heaven and the earth."),
        (
            "KJV",
            "John",
            3,
            16,
            "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
        ),
        ("KJV", "Ps", 23, 1, "The LORD is my shepherd; I shall not want."),
        (
            "KJV",
            "Rom",
            8,
            28,
            "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
        ),
        ("ASV", "Gen", 1, 1, "In the beginning God created the heavens and the earth."),
        (
            "ASV",
            "John",
            3,
            16,
            "For God so loved the world, that he gave his only begotten Son, that whosoever believeth on him should not perish, but have eternal life.",
        ),
        ("KRV", "Gen", 1, 1, "태초에 하나님이 천지를 창조하시니라"),
        ("KRV", "John", 3, 16, "하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니"),
        ("KRV", "Gen", 1, 3, "가라사대"),  # KRV style marker (substring)
        ("KRV", "Ps", 23, 1, "여호와는 나의 목자시니"),
    ]
    g_ok = 0
    for ver, b, c, v, expect in golden:
        got = versions[ver][1].get(b, {}).get(c, {}).get(v, "")
        gn, en = normalize(got), normalize(expect)
        ok = gn == en or en in gn or gn.rstrip(".!") == en.rstrip(".!")
        status = "OK" if ok else "FAIL"
        print(f"  {status} {ver} {b} {c}:{v}")
        if not ok:
            print(f"    expect: {expect[:90]}")
            print(f"    got:    {got[:90]}")
            failures.append(f"Golden fail {ver} {b}:{c}:{v}")
        else:
            g_ok += 1
    print(f"  Golden pass: {g_ok}/{len(golden)}")

    # E. Re-parse sources
    print("\n[E] App JSON vs re-parsed open-bibles sources")
    dl_path = ROOT / "scripts" / "download_pd_bibles.py"
    if (CACHE / "eng-kjv.osis.xml").exists() and dl_path.exists():
        spec = importlib.util.spec_from_file_location("dl", dl_path)
        assert spec and spec.loader
        dl = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dl)

        def to_map(pm: dict) -> dict:
            out: dict = {}
            for bid, chs in pm.items():
                out[bid] = {}
                for ch in chs:
                    out[bid][ch["chapter"]] = {
                        v["verse"]: v["text"] for v in ch["verses"]
                    }
            return out

        kjv_src = to_map(dl.parse_osis(CACHE / "eng-kjv.osis.xml"))
        asv_src = to_map(dl.parse_zefania(CACHE / "eng-asv.zefania.xml"))

        def compare(a: dict, b: dict, books) -> tuple[int, int, list]:
            text_diff = 0
            missing = 0
            samples = []
            for book in books:
                if book not in a or book not in b:
                    missing += 1
                    continue
                for c in set(a[book]) | set(b[book]):
                    av = a[book].get(c, {})
                    bv = b[book].get(c, {})
                    for v in set(av) | set(bv):
                        if v not in av or v not in bv:
                            missing += 1
                            continue
                        if normalize(av[v]) != normalize(bv[v]):
                            text_diff += 1
                            if len(samples) < 5:
                                samples.append(
                                    (book, c, v, av[v][:50], bv[v][:50])
                                )
            return text_diff, missing, samples

        books = list(CANON_CHAPTERS)
        td, ms, sm = compare(kjv, kjv_src, books)
        print(f"  KJV app vs OSIS re-parse: text_diff={td} missing={ms}")
        if sm:
            print("    samples:", sm)
        if td or ms:
            failures.append(f"KJV reparse mismatch td={td} ms={ms}")

        td, ms, sm = compare(asv, asv_src, books)
        print(f"  ASV app vs Zefania re-parse: text_diff={td} missing={ms}")
        if sm:
            print("    samples:", sm)
        if td or ms:
            failures.append(f"ASV reparse mismatch td={td} ms={ms}")
    else:
        print("  (skip re-parse — cache/scripts missing)")

    # F. KRV style markers
    print("\n[F] KRV linguistic markers (개역한글 vs 개역개정 style)")
    gaya = sum(
        1
        for chs in krv.values()
        for vs in chs.values()
        for t in vs.values()
        if "가라사대" in t
    )
    ireu = sum(
        1
        for chs in krv.values()
        for vs in chs.values()
        for t in vs.values()
        if "이르시되" in t
    )
    print(f"  가라사대 occurrences: {gaya}")
    print(f"  이르시되 occurrences: {ireu}")
    if gaya < 50:
        failures.append(f"KRV too few 가라사대 markers ({gaya}) — may not be KRV")

    # G. Fingerprints
    print("\n[G] Content fingerprints (SHA-256 prefix)")
    for name, m in (("KRV", krv), ("KJV", kjv), ("ASV", asv)):
        h = hashlib.sha256()
        for b in sorted(m.keys()):
            for c in sorted(m[b].keys()):
                for v in sorted(m[b][c].keys()):
                    h.update(f"{b}.{c}.{v}|{m[b][c][v]}".encode("utf-8"))
        print(f"  {name}: {h.hexdigest()[:24]}…")

    print("\n" + "=" * 60)
    if failures:
        print(f"RESULT: FAIL — {len(failures)} issue(s)")
        for f in failures:
            print(" -", f)
        return 1
    print("RESULT: PASS — structure, sources, golden verses, alignment OK")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
