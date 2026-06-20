#!/usr/bin/env python3
"""
Korean Bible (Public Domain) OSIS Downloader & Parser
- Downloads kor-korean.osis.xml from seven1m/open-bibles
- Converts to clean JSON structure for Flutter/Hive
- Outputs: kor_bible_full.json + bible_stats.txt
Run this on your local machine with internet access.
"""

import requests
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os

GITHUB_RAW_URL = "https://raw.githubusercontent.com/seven1m/open-bibles/master/kor-korean.osis.xml"
OUTPUT_JSON = "kor_bible_full.json"
OUTPUT_STATS = "bible_stats.txt"

def download_osis():
    print("Downloading kor-korean.osis.xml from GitHub...")
    response = requests.get(GITHUB_RAW_URL, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    
    with open("kor-korean.osis.xml", "wb") as f, tqdm(
        total=total_size, unit='B', unit_scale=True, desc="Downloading OSIS"
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    print("Download complete: kor-korean.osis.xml")

def parse_osis_to_json(xml_path):
    print("Parsing OSIS XML to structured JSON (this may take 30-60 seconds)...")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # OSIS namespace
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    
    books = []
    verse_count = 0
    
    # Find book divs
    for book_div in root.findall('.//osis:div[@type="book"]', ns):
        book_name = book_div.get('osisID', book_div.get('n', 'Unknown Book'))
        chapters = []
        
        # Find chapters within book
        chapter_elements = book_div.findall('.//osis:chapter', ns)
        if not chapter_elements:
            chapter_elements = book_div.findall('.//osis:div[@type="chapter"]', ns)
        
        for idx, chapter_div in enumerate(chapter_elements, 1):
            chapter_num = chapter_div.get('osisID', '').split('.')[-1]
            if not chapter_num or not chapter_num.isdigit():
                chapter_num = str(idx)
            
            verses = []
            for verse_elem in chapter_div.findall('.//osis:verse', ns):
                verse_num_str = verse_elem.get('osisID', '').split('.')[-1]
                verse_num = int(verse_num_str) if verse_num_str.isdigit() else len(verses) + 1
                text = ''.join(verse_elem.itertext()).strip()
                if text:
                    verses.append({
                        "verse": verse_num,
                        "text": text
                    })
                    verse_count += 1
            
            if verses:
                chapters.append({
                    "chapter": int(chapter_num),
                    "verses": verses
                })
        
        if chapters:
            books.append({
                "book": book_name,
                "chapters": chapters
            })
    
    data = {
        "version": "개역개정 (Public Domain)",
        "source": "https://github.com/seven1m/open-bibles (kor-korean.osis.xml)",
        "license": "Public Domain",
        "total_books": len(books),
        "books": books
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    with open(OUTPUT_STATS, "w", encoding="utf-8") as f:
        total_chapters = sum(len(b['chapters']) for b in books)
        f.write(f"Version: 개역개정 (Public Domain)\n")
        f.write(f"Total Books: {len(books)}\n")
        f.write(f"Total Chapters: {total_chapters}\n")
        f.write(f"Total Verses: {verse_count}\n")
        f.write(f"Source: seven1m/open-bibles - Public Domain\n")
    
    print(f"\nParsing complete!")
    print(f"  Books: {len(books)}")
    print(f"  Chapters: {total_chapters}")
    print(f"  Verses: {verse_count}")
    print(f"  Output files: {OUTPUT_JSON}, {OUTPUT_STATS}")

if __name__ == "__main__":
    if not os.path.exists("kor-korean.osis.xml"):
        download_osis()
    else:
        print("Using existing kor-korean.osis.xml")
    
    parse_osis_to_json("kor-korean.osis.xml")
    print("\n✅ All done! Next steps:")
    print("1. Copy kor_bible_full.json to your Flutter project: assets/data/")
    print("2. Update pubspec.yaml assets section")
    print("3. Upload outputs to Google Drive 05_Data folder")
    print("4. Proceed to Dart Hive model and loader implementation")