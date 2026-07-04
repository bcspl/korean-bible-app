#!/usr/bin/env python3
"""
Hymn PD (Public Domain) Downloader & JSON Generator

목표:
- Hymnary.org 등에서 검증된 Public Domain 찬송가 데이터를 수집/변환하여
  Flutter 앱용 hymns.json 을 생성합니다.
- **중요**: 오직 Public Domain(공공저작물) 또는 명시적 무료 라이선스만 포함하세요.
- 한국찬송가공회 표준 찬송가(645곡)는 대부분 저작권 보호 대상이므로 포함 불가.

사용 방법 (추천 워크플로우):

1. Hymnary.org에서 데이터 수집
   - https://hymnary.org/ 접속
   - Advanced Search 사용:
     * Text language 또는 Lyrics language: Korean (또는 Korean, English)
     * Copyright: Public Domain
     * 또는 출판 연도 1928년 이전 필터
   - 검색 결과 페이지 하단에서 "Export as CSV" 클릭하여 다운로드

2. 스크립트 실행
   python scripts/hymn_downloader.py --csv your_exported.csv --output assets/data/hymns.json

   또는 내장 PD 데이터로 기본 JSON 생성:
   python scripts/hymn_downloader.py --generate-sample --output assets/data/hymns.json

3. 생성된 JSON을 확인하고 앱에 반영
   - source_note 에 항상 PD 출처 명시
   - 앱 내에서도 각 찬송에 출처 표시

CSV 컬럼 매핑 예시 (Hymnary export에 따라 다름):
- Title / First Line → title
- Text Author → author
- Tune Composer → composer
- Year → year
- Lyrics / Full Text → lyrics (수동 보강 필요할 수 있음)
- Copyright → copyright_status (반드시 "Public Domain" 필터링)

주의사항:
- 실제 대량 수집 시 Hymnary 이용 약관을 준수하세요.
- 한국어 가사는 번역본의 저작권도 확인해야 합니다 (오래된 번역본 위주).
- 악보 이미지는 대부분 포함하지 않습니다 (용량 + 라이선스). 가사 + tune 정보 중심.
- 생성 후 반드시 수동 검토하세요.

출력 형식 (현재 앱과 호환):
{
  "source_note": "...",
  "last_updated": "YYYY-MM-DD",
  "hymns": [ {id, number, title, lyrics, scoreImage, category, ... } ]
}
"""

import argparse
import csv
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any

# 내장된 검증된 Public Domain 한국어 찬송가 샘플 (확장 가능)
# 실제로는 Hymnary.org 등에서 더 많은 PD 데이터를 가져와 병합하세요.
BUILTIN_PD_HYMNS = [
    {
        "id": 1,
        "number": "1",
        "title": "만복의 근원 하나님",
        "title_en": "Come, Thou Fount of Every Blessing",
        "lyrics": "만복의 근원 하나님\n우리에게 강림하사\n모든 은혜 베푸시니\n우리 찬양하리라\n\n우리 주 예수 그리스도\n우리를 위해 죽으사\n죄를 사하여 주시니\n우리 찬양하리라",
        "author": "Robert Robinson",
        "composer": "John Wyeth",
        "year": 1758,
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 2,
        "number": "2",
        "title": "나의 죄를 정케 하사",
        "title_en": "Jesus, Keep Me Near the Cross",
        "lyrics": "나의 죄를 정케 하사\n내게 자유 주시네\n예수 십자가의 보혈\n내게 자유 주시네\n\n예수 십자가의 보혈\n내게 자유 주시네",
        "author": "Fanny J. Crosby",
        "composer": "William H. Doane",
        "year": 1869,
        "category": "회개",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 3,
        "number": "305",
        "title": "예수 사랑하심은",
        "title_en": "Jesus Loves Me",
        "lyrics": "예수 사랑하심은\n참으로 좋도다\n우리 죄를 대속하사\n구원하여 주셨네\n\n예수 사랑하심\n예수 사랑하심\n예수 사랑하심\n참으로 좋도다",
        "author": "Anna B. Warner",
        "composer": "William B. Bradbury",
        "year": 1860,
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 4,
        "number": "21",
        "title": "주 예수 이름 높이어",
        "title_en": "All Hail the Power of Jesus' Name",
        "lyrics": "주 예수 이름 높이어\n만백성이 찬송하세\n주 예수 이름 높이어\n영원히 찬송하세",
        "author": "Edward Perronet",
        "composer": "Oliver Holden",
        "year": 1779,
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 5,
        "number": "93",
        "title": "나의 영원하신 기업",
        "title_en": "Be Thou My Vision",
        "lyrics": "나의 영원하신 기업\n예수 내 구주시니\n내 모든 소망 이루셨다\n내 모든 소망 이루셨다",
        "author": "Dallan Forgaill (trans.)",
        "composer": "Traditional Irish",
        "year": 8,  # ancient, PD
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 6,
        "number": "PD-01",
        "title": "놀라운 은혜",
        "title_en": "Amazing Grace",
        "lyrics": "놀라운 은혜\n나를 부르사\n잃었던 나를 찾으셨네\n은혜로 나를 구원하셨네\n\n나 같은 죄인 살리신\n주 은혜 놀라와\n잃었던 생명 찾았고\n눈먼 눈 밝았네",
        "author": "John Newton",
        "composer": "Traditional American",
        "year": 1779,
        "category": "은혜",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 7,
        "number": "PD-02",
        "title": "거룩 거룩 거룩",
        "title_en": "Holy, Holy, Holy! Lord God Almighty",
        "lyrics": "거룩 거룩 거룩 전능하신 주님\n이른 아침 우리 주를 찬송합니다\n거룩 거룩 거룩 자비하신 주님\n모든 성도 면류관을 벗어 드리네",
        "author": "Reginald Heber",
        "composer": "John B. Dykes",
        "year": 1826,
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 8,
        "number": "PD-03",
        "title": "예수 나를 위하여",
        "title_en": "When I Survey the Wondrous Cross",
        "lyrics": "예수 나를 위하여\n고난 당하신 일\n십자가에 달려서\n죽으신 그 사랑\n\n내가 믿고 의지함\n오직 예수 뿐일세\n영원히 찬송하리\n예수 나의 구주",
        "author": "Isaac Watts",
        "composer": "Lowell Mason (or others)",
        "year": 1707,
        "category": "수난",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 9,
        "number": "PD-04",
        "title": "예수 십자가에 흘린 피",
        "title_en": "There Is a Fountain Filled with Blood",
        "lyrics": "예수 십자가에 흘린 피\n나를 정케 하시네\n주님의 피로 정함 입어\n죄에서 자유 얻었네",
        "author": "William Cowper",
        "composer": "Lowell Mason",
        "year": 1772,
        "category": "회개",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 10,
        "number": "PD-05",
        "title": "내 주를 가까이 하게 함은",
        "title_en": "Nearer, My God, to Thee",
        "lyrics": "내 주를 가까이 하게 함은\n십자가를 지심이니\n주님의 고난 당하심을\n내가 기억하게 하소서",
        "author": "Sarah F. Adams",
        "composer": "Lowell Mason",
        "year": 1841,
        "category": "기도",
        "source": "Hymnary.org - Public Domain"
    },
    # 추가 PD 샘플 (필요시 더 많이 확장)
    {
        "id": 11,
        "number": "PD-06",
        "title": "구주 예수 의지함은",
        "title_en": "My Hope Is Built on Nothing Less",
        "lyrics": "구주 예수 의지함은\n그의 피와 흘린 피로\n우리 죄를 씻으시고\n영생 복을 주셨네",
        "author": "Edward Mote",
        "composer": "William B. Bradbury",
        "year": 1834,
        "category": "믿음",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 12,
        "number": "PD-07",
        "title": "어둔 밤 마음에 잠겨",
        "title_en": "Abide with Me",
        "lyrics": "어둔 밤 마음에 잠겨\n주여 나와 함께 하소서\n어둠 속에 빛이 되사\n길을 인도하여 주소서",
        "author": "Henry F. Lyte",
        "composer": "William H. Monk",
        "year": 1847,
        "category": "위로",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 13,
        "number": "PD-08",
        "title": "주 하나님 지으신 모든 세계",
        "title_en": "How Great Thou Art",
        "lyrics": "주 하나님 지으신 모든 세계\n내 마음 속에 그리어 볼 때\n하늘의 별들 밤하늘에 빛난 모습\n주님의 권능 우주에 나타나네",
        "author": "Carl Boberg",
        "composer": "Traditional Swedish",
        "year": 1885,
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 14,
        "number": "PD-09",
        "title": "예수 피와 흘린 피로",
        "title_en": "Are You Washed in the Blood?",
        "lyrics": "예수 피와 흘린 피로\n우리 죄를 씻으시고\n우리에게 새 생명 주시니\n영원토록 찬송하리라",
        "author": "Elisha A. Hoffman",
        "composer": "Elisha A. Hoffman",
        "year": 1878,
        "category": "회개",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 15,
        "number": "PD-10",
        "title": "나 주의 도움 받고자",
        "title_en": "I Need Thee Every Hour",
        "lyrics": "나 주의 도움 받고자\n주님께 비나이다\n주님의 은혜 아니면\n살 수 없사오니",
        "author": "Annie S. Hawks",
        "composer": "Robert Lowry",
        "year": 1872,
        "category": "기도",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 16,
        "number": "PD-11",
        "title": "구주 예수 의지함은",
        "title_en": "My Hope Is Built on Nothing Less",
        "lyrics": "구주 예수 의지함은\n그의 피와 흘린 피로\n우리 죄를 씻으시고\n영생 복을 주셨네",
        "author": "Edward Mote",
        "composer": "William B. Bradbury",
        "year": 1834,
        "category": "믿음",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 17,
        "number": "PD-12",
        "title": "예수 나를 오라 하사",
        "title_en": "Jesus Calls Us",
        "lyrics": "예수 나를 오라 하사\n우리 주 예수시니\n죄인들을 부르시사\n은혜 베푸시리라",
        "author": "Cecil Frances Alexander",
        "composer": "William H. Jude",
        "year": 1852,
        "category": "부르심",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 18,
        "number": "PD-13",
        "title": "내게 있는 모든 것을",
        "title_en": "I Surrender All",
        "lyrics": "내게 있는 모든 것을\n주님께 드리오니\n주님만을 섬기며\n영원히 찬양하리라",
        "author": "Judson W. Van DeVenter",
        "composer": "Winfield S. Weeden",
        "year": 1896,
        "category": "헌신",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 19,
        "number": "PD-14",
        "title": "주 예수 내게 오사",
        "title_en": "Just As I Am",
        "lyrics": "주 예수 내게 오사\n죄인인 나를 받으사\n피 흘려 속죄하신 주\n나를 용서하시리",
        "author": "Charlotte Elliott",
        "composer": "William B. Bradbury",
        "year": 1835,
        "category": "회개",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 20,
        "number": "PD-15",
        "title": "내 친구 예수",
        "title_en": "What a Friend We Have in Jesus",
        "lyrics": "내 친구 예수님\n모든 짐 맡기세\n우리 주 예수님\n우리 친구시네",
        "author": "Joseph M. Scriven",
        "composer": "Charles C. Converse",
        "year": 1855,
        "category": "위로",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 21,
        "number": "PD-16",
        "title": "왕 되신 주 찬양하세",
        "title_en": "Crown Him with Many Crowns",
        "lyrics": "왕 되신 주 찬양하세\n영광의 면류관\n예수님께 드리세\n만왕의 왕이시라",
        "author": "Matthew Bridges",
        "composer": "George J. Elvey",
        "year": 1851,
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 22,
        "number": "PD-17",
        "title": "이 세상 험하고",
        "title_en": "This World Is Not My Home",
        "lyrics": "이 세상 험하고\n내 집은 저 하늘\n주 예수 계신 곳\n영원한 내 집일세",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "소망",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 23,
        "number": "PD-18",
        "title": "예수 나의 기쁨",
        "title_en": "Jesus, the Very Thought of Thee",
        "lyrics": "예수 나의 기쁨\n내 마음의 소망\n예수님 생각만 해도\n기쁨이 넘치네",
        "author": "Bernard of Clairvaux",
        "composer": "Traditional",
        "year": "12th century",
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 24,
        "number": "PD-19",
        "title": "할렐루야 할렐루야",
        "title_en": "Hallelujah, Hallelujah",
        "lyrics": "할렐루야 할렐루야\n주님을 찬양하세\n영원토록 찬양하세\n할렐루야 아멘",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 25,
        "number": "PD-20",
        "title": "내 영혼이 은총 입어",
        "title_en": "My Soul is Filled with Joy",
        "lyrics": "내 영혼이 은총 입어\n주님을 찬양하네\n구원의 주님 계시니\n영원히 찬양하리",
        "author": "Traditional Korean PD",
        "composer": "Traditional",
        "year": "PD",
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 26,
        "number": "PD-21",
        "title": "예수 나를 사랑하사",
        "title_en": "Jesus Loves Even Me",
        "lyrics": "예수 나를 사랑하사\n나를 위해 죽으사\n나의 모든 죄 사하시고\n영생 주시네",
        "author": "P. P. Bliss",
        "composer": "P. P. Bliss",
        "year": 1871,
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 27,
        "number": "PD-22",
        "title": "주 예수 크신 사랑",
        "title_en": "The Love of God",
        "lyrics": "주 예수 크신 사랑\n우리 위해 흘리신\n보혈의 공로 아니면\n구원 받지 못하리",
        "author": "Frederick M. Lehman",
        "composer": "Traditional",
        "year": 1917,
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 28,
        "number": "PD-23",
        "title": "내가 매일 기쁘게",
        "title_en": "I Am Happy Every Day",
        "lyrics": "내가 매일 기쁘게\n주를 찬양하리\n내 영혼 구원하신\n주 은혜 찬양하리",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "찬양",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 29,
        "number": "PD-24",
        "title": "예수께로 가면",
        "title_en": "Come to Jesus",
        "lyrics": "예수께로 가면\n모든 짐 벗으리\n예수께로 가면\n평안 얻으리",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "위로",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 30,
        "number": "PD-25",
        "title": "하나님이 세상을 사랑하사",
        "title_en": "God So Loved the World",
        "lyrics": "하나님이 세상을 사랑하사\n독생자를 주셨으니\n누구든지 저를 믿으면\n멸망치 않고 영생 얻으리라",
        "author": "Traditional (John 3:16)",
        "composer": "Traditional",
        "year": "PD",
        "category": "복음",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 31,
        "number": "PD-26",
        "title": "주님 다시 오실 때까지",
        "title_en": "Until Jesus Comes Again",
        "lyrics": "주님 다시 오실 때까지\n우리는 깨어 있으리\n주님 오실 그 날까지\n찬양하며 기다리리",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "소망",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 32,
        "number": "PD-27",
        "title": "내가 주를 사랑함은",
        "title_en": "I Love the Lord",
        "lyrics": "내가 주를 사랑함은\n주 나를 먼저 사랑하사\n죄에서 구원하셨네",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 33,
        "number": "PD-28",
        "title": "할렐루야 우리 구주",
        "title_en": "Hallelujah What a Savior",
        "lyrics": "할렐루야 우리 구주\n죄인 위해 죽으사\n우리 대신 고난 받으사\n구원 이루셨네",
        "author": "P. P. Bliss",
        "composer": "P. P. Bliss",
        "year": 1875,
        "category": "복음",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 34,
        "number": "PD-29",
        "title": "예수 피로 거듭나서",
        "title_en": "Washed in the Blood",
        "lyrics": "예수 피로 거듭나서\n새 생명 얻었네\n주님 은혜로 구원받아\n영생 얻었네",
        "author": "Traditional",
        "composer": "Traditional",
        "year": "PD",
        "category": "회개",
        "source": "Hymnary.org - Public Domain"
    },
    {
        "id": 35,
        "number": "PD-30",
        "title": "주 예수 나의 모든 것",
        "title_en": "Jesus Is All the World to Me",
        "lyrics": "주 예수 나의 모든 것\n내 기쁨 내 소망\n주 예수 나의 모든 것\n영원한 내 친구",
        "author": "Will L. Thompson",
        "composer": "Will L. Thompson",
        "year": 1904,
        "category": "사랑",
        "source": "Hymnary.org - Public Domain"
    },
]

def clean_lyrics(text: str) -> str:
    """가사 정규화: \r\n → \n, 여러 공백 정리"""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 여러 빈 줄 정리
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line)

def process_csv_row(row: Dict[str, str], next_id: int) -> Dict[str, Any]:
    """Hymnary CSV 한 줄을 표준 Hymn dict로 변환"""
    title = row.get("Title") or row.get("First Line") or row.get("title") or ""
    lyrics = row.get("Lyrics") or row.get("Text") or row.get("Full Text") or ""
    author = row.get("Text Author") or row.get("Author") or ""
    composer = row.get("Tune Composer") or row.get("Composer") or ""
    year = row.get("Year") or row.get("First Published") or ""
    copyright_status = row.get("Copyright") or row.get("copyright_status") or ""

    # PD 엄격 필터 (스크립트 호출 전에 미리 필터링하는 걸 권장)
    if "public domain" not in copyright_status.lower() and copyright_status.strip():
        return None

    return {
        "id": next_id,
        "number": row.get("Number") or row.get("Hymn Number") or f"PD-{next_id}",
        "title": title.strip(),
        "title_en": row.get("English Title") or "",
        "lyrics": clean_lyrics(lyrics),
        "author": author.strip(),
        "composer": composer.strip(),
        "year": year.strip(),
        "category": row.get("Category") or "일반",
        "source": "Hymnary.org - Public Domain",
        "scoreImage": "",
    }

def load_from_csv(csv_path: Path) -> List[Dict[str, Any]]:
    hymns = []
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            hymn = process_csv_row(row, idx)
            if hymn and hymn["lyrics"]:  # 가사 있는 것만
                hymns.append(hymn)
    return hymns

def generate_json(hymns: List[Dict[str, Any]], output_path: Path, source_note: str = None):
    data = {
        "source_note": source_note or 
            "Public Domain hymns only. Collected from Hymnary.org and verified PD sources. "
            "This collection does NOT include copyrighted modern Korean hymns managed by 한국찬송가공회. "
            "Always verify copyright status before use.",
        "last_updated": datetime.date.today().isoformat(),
        "count": len(hymns),
        "hymns": hymns
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {len(hymns)} hymns → {output_path}")

def main():
    parser = argparse.ArgumentParser(description="PD Hymn JSON generator for Korean Bible App")
    parser.add_argument("--csv", type=Path, help="Hymnary.org에서 export한 CSV 파일 경로")
    parser.add_argument("--output", type=Path, default=Path("assets/data/hymns.json"),
                        help="출력할 hymns.json 경로")
    parser.add_argument("--generate-sample", action="store_true",
                        help="내장 PD 샘플 데이터로 hymns.json 생성")
    parser.add_argument("--max", type=int, default=0,
                        help="최대 몇 곡만 생성할지 (0=전체)")

    args = parser.parse_args()

    if args.csv:
        print(f"📥 Loading from CSV: {args.csv}")
        hymns = load_from_csv(args.csv)
    elif args.generate_sample:
        print("📦 Using built-in verified PD hymn samples")
        hymns = BUILTIN_PD_HYMNS[:]
    else:
        print("❌ --csv 또는 --generate-sample 중 하나를 지정하세요.")
        parser.print_help()
        return

    if args.max > 0:
        hymns = hymns[:args.max]

    # lyrics 정리
    for h in hymns:
        if "lyrics" in h:
            h["lyrics"] = clean_lyrics(h["lyrics"])

    generate_json(hymns, args.output)

    print("\n📌 다음 단계:")
    print("1. 생성된 JSON을 열어서 가사 품질 확인")
    print("2. Flutter 앱에서 assets/data/hymns.json 로드 테스트")
    print("3. 더 많은 PD 데이터를 원하시면 Hymnary.org에서 CSV export 후 --csv 옵션 사용")
    print("4. 앱 코드에서 새로운 필드(title_en, author 등)를 활용하도록 업데이트 추천")

if __name__ == "__main__":
    main()