#!/usr/bin/env python3
"""
Download Public Domain English Bibles (KJV OSIS, ASV Zefania) and convert
to the same JSON shape as assets/data/kor_bible_full.json for multi-version UI.

Outputs (compact JSON):
  assets/data/eng_kjv_full.json
  assets/data/eng_asv_full.json
"""
from __future__ import annotations

import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
CACHE = ROOT / "scripts" / "_bible_cache"
CACHE.mkdir(parents=True, exist_ok=True)

# Canonical book order matching kor-korean / app mapping keys
OSIS_BOOKS = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Josh", "Judg", "Ruth",
    "1Sam", "2Sam", "1Kgs", "2Kgs", "1Chr", "2Chr", "Ezra", "Neh", "Esth",
    "Job", "Ps", "Prov", "Eccl", "Song", "Isa", "Jer", "Lam", "Ezek", "Dan",
    "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph",
    "Hag", "Zech", "Mal",
    "Matt", "Mark", "Luke", "John", "Acts", "Rom", "1Cor", "2Cor", "Gal",
    "Eph", "Phil", "Col", "1Thess", "2Thess", "1Tim", "2Tim", "Titus", "Phlm",
    "Heb", "Jas", "1Pet", "2Pet", "1John", "2John", "3John", "Jude", "Rev",
]

# Zefania book number (1-66) -> OSIS id
ZEF_NUM_TO_OSIS = {i + 1: b for i, b in enumerate(OSIS_BOOKS)}

KJV_URL = "https://raw.githubusercontent.com/seven1m/open-bibles/master/eng-kjv.osis.xml"
ASV_URL = "https://raw.githubusercontent.com/seven1m/open-bibles/master/eng-asv.zefania.xml"


def download(url: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 100_000:
        print(f"Using cache: {dest.name} ({dest.stat().st_size // 1024} KB)")
        return dest
    print(f"Downloading {url} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"  saved {dest} ({dest.stat().st_size // 1024} KB)")
    return dest


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def parse_osis(path: Path) -> dict[str, list]:
    """Return book_id -> list of chapters {chapter, verses:[{verse,text}]}

    Supports container-style OSIS (verses with text children) and
    milestone-style OSIS (sID/eID verse markers with interleaved text).
    """
    print(f"Parsing OSIS {path.name} ...")
    tree = ET.parse(path)
    root = tree.getroot()
    books: dict[str, list] = {}

    def walk_book(book_el, book_id: str) -> list:
        """Milestone-aware walk: collect text between verse sID and eID."""
        # chapter_num -> {verse_num: text}
        by_ch: dict[int, dict[int, str]] = {}
        current_ch: int | None = None
        current_v: int | None = None
        buf: list[str] = []

        def flush():
            nonlocal buf, current_ch, current_v
            if current_ch is not None and current_v is not None and buf:
                text = re.sub(r"\s+", " ", "".join(buf)).strip()
                if text:
                    by_ch.setdefault(current_ch, {})[current_v] = text
            buf = []

        def handle(el):
            nonlocal current_ch, current_v, buf
            tag = local_name(el.tag)
            if tag == "chapter":
                # milestone chapter start/end
                n = el.get("n")
                if el.get("sID") or el.get("osisRef") or (n and el.get("eID") is None and "eID" not in el.attrib):
                    if n and str(n).isdigit():
                        flush()
                        current_ch = int(n)
                        current_v = None
                elif el.get("eID"):
                    flush()
                    current_v = None
                # container chapter with osisID Gen.1
                oid = el.get("osisID") or ""
                if oid and "." in oid:
                    parts = oid.split(".")
                    if len(parts) >= 2 and parts[1].isdigit():
                        flush()
                        current_ch = int(parts[1])
                        current_v = None
            elif tag == "verse":
                if el.get("sID") or (el.get("osisID") and el.get("eID") is None and "eID" not in el.attrib):
                    flush()
                    n = el.get("n")
                    oid = el.get("osisID") or ""
                    if n and str(n).isdigit():
                        current_v = int(n)
                    elif oid:
                        last = oid.split(".")[-1]
                        if last.isdigit():
                            current_v = int(last)
                    # container-style: text inside verse element
                    inner = "".join(el.itertext()).strip()
                    if inner and current_ch is not None and current_v is not None:
                        # If verse has child text already, may also be milestone empty
                        if not el.get("sID") or inner:
                            # For pure container verses without sID
                            if not el.get("sID"):
                                by_ch.setdefault(current_ch, {})[current_v] = re.sub(
                                    r"\s+", " ", inner
                                ).strip()
                                current_v = None
                elif el.get("eID"):
                    flush()
                    current_v = None
            # text nodes are via tail/text of elements while in verse
            if el.text and current_v is not None:
                buf.append(el.text)
            for child in list(el):
                handle(child)
                if child.tail and current_v is not None:
                    buf.append(child.tail)

        # Only walk children of book (not nested books)
        for child in list(book_el):
            handle(child)
        flush()

        chapters = []
        for ch_num in sorted(by_ch.keys()):
            verses = [
                {"verse": vn, "text": by_ch[ch_num][vn]}
                for vn in sorted(by_ch[ch_num].keys())
            ]
            if verses:
                chapters.append({"chapter": ch_num, "verses": verses})
        return chapters

    for el in root.iter():
        if local_name(el.tag) != "div":
            continue
        if el.get("type") != "book":
            continue
        book_id = el.get("osisID") or el.get("n") or "Unknown"
        book_id = book_id.split(".")[0]
        chapters = walk_book(el, book_id)
        if chapters:
            books[book_id] = chapters
    print(f"  OSIS books parsed: {len(books)}")
    return books


def parse_zefania(path: Path) -> dict[str, list]:
    print(f"Parsing Zefania {path.name} ...")
    tree = ET.parse(path)
    root = tree.getroot()
    books: dict[str, list] = {}

    for book_el in root.iter():
        if local_name(book_el.tag) not in ("BIBLEBOOK", "biblebook"):
            continue
        bnum = book_el.get("bnumber") or book_el.get("bNumber")
        if not bnum or not str(bnum).isdigit():
            continue
        book_id = ZEF_NUM_TO_OSIS.get(int(bnum))
        if not book_id:
            continue
        chapters = []
        for ch_el in book_el:
            if local_name(ch_el.tag) not in ("CHAPTER", "chapter"):
                continue
            cnum = ch_el.get("cnumber") or ch_el.get("cNumber")
            if not cnum or not str(cnum).isdigit():
                continue
            verses = []
            for v_el in ch_el:
                if local_name(v_el.tag) not in ("VERS", "vers", "VERSE", "verse"):
                    continue
                vnum = v_el.get("vnumber") or v_el.get("vNumber")
                if not vnum or not str(vnum).isdigit():
                    continue
                text = "".join(v_el.itertext()).strip()
                text = re.sub(r"\s+", " ", text)
                if text:
                    verses.append({"verse": int(vnum), "text": text})
            if verses:
                verses.sort(key=lambda x: x["verse"])
                chapters.append({"chapter": int(cnum), "verses": verses})
        chapters.sort(key=lambda c: c["chapter"])
        if chapters:
            books[book_id] = chapters
    print(f"  Zefania books parsed: {len(books)}")
    return books


def to_app_json(books_map: dict[str, list], version: str, source: str, license_: str) -> dict:
    books = []
    for bid in OSIS_BOOKS:
        chs = books_map.get(bid)
        if not chs:
            print(f"  WARNING missing book {bid}")
            continue
        books.append({"book": bid, "chapters": chs})
    return {
        "version": version,
        "abbreviation": version.split()[0] if version else "",
        "source": source,
        "license": license_,
        "total_books": len(books),
        "books": books,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"Wrote {path} ({path.stat().st_size // 1024} KB), books={data['total_books']}")


def main() -> None:
    kjv_xml = download(KJV_URL, CACHE / "eng-kjv.osis.xml")
    asv_xml = download(ASV_URL, CACHE / "eng-asv.zefania.xml")

    kjv_map = parse_osis(kjv_xml)
    asv_map = parse_zefania(asv_xml)

    # Fix common OSIS id aliases
    aliases = {
        "Psalm": "Ps",
        "Psalms": "Ps",
        "SongOfSongs": "Song",
        "Song of Solomon": "Song",
        "Sir": "Song",
        "Philippians": "Phil",
        "Philemon": "Phlm",
    }
    for src, dst in aliases.items():
        if src in kjv_map and dst not in kjv_map:
            kjv_map[dst] = kjv_map.pop(src)

    write_json(
        DATA / "eng_kjv_full.json",
        to_app_json(
            kjv_map,
            "KJV (King James Version)",
            "seven1m/open-bibles eng-kjv.osis.xml",
            "Public Domain",
        ),
    )
    write_json(
        DATA / "eng_asv_full.json",
        to_app_json(
            asv_map,
            "ASV (American Standard Version 1901)",
            "seven1m/open-bibles eng-asv.zefania.xml",
            "Public Domain",
        ),
    )

    # sanity: Gen 1:1
    for label, m in (("KJV", kjv_map), ("ASV", asv_map)):
        g = m.get("Gen", [{}])[0].get("verses", [{}])[0].get("text", "")[:80]
        print(f"{label} Gen1:1: {g}")


if __name__ == "__main__":
    main()
