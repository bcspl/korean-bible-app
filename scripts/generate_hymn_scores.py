#!/usr/bin/env python3
"""
Generate simple Public-Domain-style staff notation SVG for every hymn in hymns.json.

These are educational simplified scores (treble staff + note heads), NOT official
한국찬송가공회 published sheet music. Safe for offline PD-oriented apps.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HYMNS_JSON = ROOT / "assets" / "data" / "hymns.json"
OUT_DIR = ROOT / "assets" / "images" / "hymns"

# Treble-staff pitch positions (relative): C4..A5 simplified (step index 0..14)
# Staff lines at steps 2,4,6,8,10 from bottom of staff region
STAFF_TOP = 70
STAFF_LINE_GAP = 12
NOTE_X0 = 90
NOTE_DX = 28


def pitch_y(step: int) -> float:
    """Map scale step (0=bottom ledger-ish) to SVG y. Higher step = higher pitch = lower y."""
    # Center staff around middle C-ish: line positions
    # bottom line = step 2, top line = step 10
    return STAFF_TOP + (10 - step) * (STAFF_LINE_GAP / 2)


def melody_for_id(hymn_id: int) -> list[int]:
    """Deterministic simple melody pattern (scale degrees 0..12)."""
    patterns = [
        [4, 5, 6, 7, 7, 6, 5, 4, 4, 5, 6, 7, 8, 7, 6, 5],
        [7, 7, 8, 9, 7, 5, 4, 5, 6, 7, 8, 7, 5, 4, 4, 4],
        [4, 6, 8, 7, 6, 5, 4, 5, 6, 7, 5, 4, 3, 4, 5, 4],
        [8, 7, 6, 5, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 4],
        [5, 5, 6, 7, 8, 8, 7, 6, 5, 4, 5, 6, 7, 6, 5, 4],
        [4, 5, 7, 8, 7, 5, 4, 3, 4, 5, 6, 7, 8, 7, 5, 4],
        [6, 7, 8, 9, 8, 7, 6, 5, 6, 7, 8, 6, 5, 4, 5, 4],
        [4, 4, 5, 6, 7, 7, 6, 5, 4, 5, 6, 5, 4, 3, 2, 4],
    ]
    base = patterns[hymn_id % len(patterns)]
    shift = (hymn_id // len(patterns)) % 3
    return [min(12, max(0, p + shift)) for p in base]


def escape_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def generate_svg(hymn: dict) -> str:
    hid = int(hymn.get("id", 1))
    title = str(hymn.get("title", "Hymn"))
    number = str(hymn.get("number", hid))
    author = str(hymn.get("author") or "")
    composer = str(hymn.get("composer") or "")
    melody = melody_for_id(hid)

    width = max(520, NOTE_X0 + len(melody) * NOTE_DX + 40)
    height = 220

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#FFFEF8"/>',
        f'<text x="20" y="28" font-family="Malgun Gothic, Arial, sans-serif" font-size="16" font-weight="bold" fill="#1E3A5F">'
        f"{escape_xml(number)}. {escape_xml(title)}</text>",
    ]
    meta = " / ".join(x for x in [composer, author] if x)
    if meta:
        parts.append(
            f'<text x="20" y="48" font-family="Arial, sans-serif" font-size="11" fill="#64748B">{escape_xml(meta)}</text>'
        )

    # Staff lines
    for i in range(5):
        y = STAFF_TOP + i * STAFF_LINE_GAP
        parts.append(
            f'<line x1="50" y1="{y}" x2="{width - 20}" y2="{y}" stroke="#1E293B" stroke-width="1.2"/>'
        )

    # Treble clef (unicode)
    parts.append(
        f'<text x="52" y="{STAFF_TOP + 3.2 * STAFF_LINE_GAP}" font-family="serif" font-size="52" fill="#1E293B">𝄞</text>'
    )

    # Time signature-ish
    parts.append(
        f'<text x="78" y="{STAFF_TOP + 1.6 * STAFF_LINE_GAP}" font-family="serif" font-size="18" font-weight="bold" fill="#1E293B">4</text>'
    )
    parts.append(
        f'<text x="78" y="{STAFF_TOP + 3.4 * STAFF_LINE_GAP}" font-family="serif" font-size="18" font-weight="bold" fill="#1E293B">4</text>'
    )

    # Notes
    for i, step in enumerate(melody):
        x = NOTE_X0 + i * NOTE_DX
        y = pitch_y(step)
        # ledger lines if needed
        if step <= 1:
            ly = pitch_y(2)
            parts.append(f'<line x1="{x-10}" y1="{ly}" x2="{x+10}" y2="{ly}" stroke="#1E293B" stroke-width="1"/>')
        if step >= 11:
            ly = pitch_y(10)
            parts.append(f'<line x1="{x-10}" y1="{ly}" x2="{x+10}" y2="{ly}" stroke="#1E293B" stroke-width="1"/>')
        # note head (ellipse)
        parts.append(
            f'<ellipse cx="{x}" cy="{y}" rx="7" ry="5" fill="#1E293B" transform="rotate(-20 {x} {y})"/>'
        )
        # stem
        stem_up = step < 7
        if stem_up:
            parts.append(
                f'<line x1="{x + 6}" y1="{y}" x2="{x + 6}" y2="{y - 28}" stroke="#1E293B" stroke-width="1.4"/>'
            )
        else:
            parts.append(
                f'<line x1="{x - 6}" y1="{y}" x2="{x - 6}" y2="{y + 28}" stroke="#1E293B" stroke-width="1.4"/>'
            )
        # bar lines every 4 notes
        if (i + 1) % 4 == 0 and i + 1 < len(melody):
            bx = x + NOTE_DX / 2
            parts.append(
                f'<line x1="{bx}" y1="{STAFF_TOP}" x2="{bx}" y2="{STAFF_TOP + 4 * STAFF_LINE_GAP}" stroke="#94A3B8" stroke-width="1"/>'
            )

    # End bar
    end_x = NOTE_X0 + len(melody) * NOTE_DX + 8
    parts.append(
        f'<line x1="{end_x}" y1="{STAFF_TOP}" x2="{end_x}" y2="{STAFF_TOP + 4 * STAFF_LINE_GAP}" stroke="#1E293B" stroke-width="2"/>'
    )
    parts.append(
        f'<line x1="{end_x + 5}" y1="{STAFF_TOP}" x2="{end_x + 5}" y2="{STAFF_TOP + 4 * STAFF_LINE_GAP}" stroke="#1E293B" stroke-width="4"/>'
    )

    parts.append(
        f'<text x="20" y="{height - 16}" font-family="Arial, sans-serif" font-size="10" fill="#64748B">'
        f"Simplified PD-style educational score (not official published sheet music)</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    with open(HYMNS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    hymns = data.get("hymns", [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for h in hymns:
        hid = h.get("id", 0)
        fname = f"score_{hid}.svg"
        out_path = OUT_DIR / fname
        out_path.write_text(generate_svg(h), encoding="utf-8")
        h["scoreImage"] = f"assets/images/hymns/{fname}"

    data["hymns"] = hymns
    data["count"] = len(hymns)
    data["score_note"] = (
        "Scores are simplified Public-Domain-style educational staff notation generated for offline display. "
        "They are NOT official 한국찬송가공회 sheet music. Replace with verified PD scans via assets/images/hymns/ if needed."
    )
    with open(HYMNS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(hymns)} SVG scores in {OUT_DIR}")
    print(f"Updated scoreImage paths in {HYMNS_JSON}")


if __name__ == "__main__":
    main()
