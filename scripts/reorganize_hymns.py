#!/usr/bin/env python3
"""Inspect and reorganize hymns.json into correct sequential order.

Rules:
- Sort by meaningful number: pure digits first (numeric), then PD-xx (numeric), then rest.
- Reassign id = 1..N in that order.
- Reassign display number = "1".."N" (app list order = sequential catalog order).
- Keep original PD/hymnal number in notes via original_number field if different.
- Update scoreImage to assets/images/hymns/score_{id}.svg
- Preserve source_note / metadata.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HYMNS_JSON = ROOT / "assets" / "data" / "hymns.json"


def sort_key(number: str):
    s = str(number or "").strip()
    m = re.fullmatch(r"(\d+)", s)
    if m:
        return (0, int(m.group(1)), s)
    m = re.fullmatch(r"PD-0*(\d+)", s, re.I)
    if m:
        return (1, int(m.group(1)), s)
    m = re.fullmatch(r"PD-?(.*)", s, re.I)
    if m:
        return (2, 0, m.group(1))
    return (3, 0, s)


def main() -> int:
    dry = "--dry-run" in sys.argv or "-n" in sys.argv
    apply = "--apply" in sys.argv or (not dry and "--inspect" not in sys.argv)

    data = json.loads(HYMNS_JSON.read_text(encoding="utf-8"))
    hymns = list(data.get("hymns") or [])
    print(f"Loaded {len(hymns)} hymns from {HYMNS_JSON}")
    print(f"count field={data.get('count')} last_updated={data.get('last_updated')}")
    print()

    print("=== CURRENT ORDER (as stored) ===")
    for i, h in enumerate(hymns, 1):
        print(
            f"{i:3}. number={str(h.get('number')):10} id={h.get('id')!s:>4}  "
            f"{(h.get('title') or '')[:36]:36}  score={h.get('scoreImage', '')}"
        )

    nums = [str(h.get("number", "")) for h in hymns]
    ids = [h.get("id") for h in hymns]
    print()
    print(f"ids sequential 1..N? {ids == list(range(1, len(ids) + 1))}")
    print(f"id min/max/unique: {min(ids) if ids else None}/{max(ids) if ids else None}/{len(set(ids))}")
    dups = sorted({n for n in nums if nums.count(n) > 1})
    print(f"duplicate numbers: {dups or 'none'}")

    # Detect out-of-order relative to natural number sort
    sorted_by_num = sorted(hymns, key=lambda h: sort_key(str(h.get("number", ""))))
    out_of_order = [h for h, s in zip(hymns, sorted_by_num) if h is not s]
    print(f"out-of-order vs number-sort: {len(out_of_order)} positions differ" if out_of_order else "already number-sorted")

    print()
    print("=== TARGET ORDER (number-sort then renumber 1..N) ===")
    for i, h in enumerate(sorted_by_num, 1):
        print(
            f"{i:3}. was number={str(h.get('number')):10} id={h.get('id')!s:>4}  "
            f"{(h.get('title') or '')[:40]}"
        )

    if dry or "--inspect" in sys.argv:
        print("\n(dry-run / inspect only — no write)")
        return 0

    if not apply:
        print("Pass --apply to write, or --inspect/--dry-run to only report.")
        return 0

    # Backup
    backup = HYMNS_JSON.with_suffix(".json.bak")
    backup.write_text(HYMNS_JSON.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"\nBackup written: {backup}")

    reorganized = []
    for new_id, h in enumerate(sorted_by_num, 1):
        old_number = str(h.get("number", ""))
        new_h = dict(h)
        new_h["id"] = new_id
        new_h["number"] = str(new_id)
        new_h["scoreImage"] = f"assets/images/hymns/score_{new_id}.svg"
        # Preserve previous catalog number for reference
        if old_number and old_number != str(new_id):
            new_h["original_number"] = old_number
        elif "original_number" in new_h and new_h.get("original_number") == str(new_id):
            # clean redundant
            pass
        reorganized.append(new_h)

    data["hymns"] = reorganized
    data["count"] = len(reorganized)
    data["last_updated"] = date.today().isoformat()
    note = data.get("source_note") or ""
    if "reorganized" not in note.lower():
        data["source_note"] = (
            note.rstrip()
            + " Numbers reorganized to sequential app catalog order (1..N); original numbers kept in original_number when different."
        )

    HYMNS_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(reorganized)} hymns → sequential numbers 1..{len(reorganized)}")
    print("Next: run generate_hymn_scores.py to refresh SVG labels/paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
