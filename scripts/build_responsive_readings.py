#!/usr/bin/env python3
"""
Build scripture-based 교독문 catalog from KRV verse references only.

- Does NOT copy 한국찬송가공회 교독문 numbers/edits
- Does NOT use 개역개정 text
- Passages are references; app renders KRV / KJV / ASV at runtime
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "data" / "responsive_readings.json"


def R(
    title_ko: str,
    title_en: str,
    category: str,
    passages: list[dict],
    note: str = "",
) -> dict:
    return {
        "title_ko": title_ko,
        "title_en": title_en,
        "category": category,
        "note": note,
        "passages": passages,
    }


def ps(chapter: int, verses: list[int] | None = None) -> dict:
    p: dict = {"book": "Ps", "chapter": chapter}
    if verses:
        p["verses"] = verses
    return p


def ref(book: str, chapter: int, verses: list[int] | None = None) -> dict:
    p: dict = {"book": book, "chapter": chapter}
    if verses:
        p["verses"] = verses
    return p


# Categories are app-specific (not hymnal 교독문 numbers)
CATALOG: list[dict] = [
    # --- 시편 ---
    R("복 있는 사람", "Blessed is the man", "시편", [ps(1)]),
    R("주의 이름 어찌 아름다운지요", "How excellent is Thy name", "시편", [ps(8)]),
    R("하늘이 하나님의 영광을 선포", "The heavens declare", "시편", [ps(19)]),
    R("여호와는 나의 목자", "The Lord is my shepherd", "시편", [ps(23)]),
    R("영광의 왕", "The King of glory", "시편", [ps(24)]),
    R("여호와는 나의 빛", "The Lord is my light", "시편", [ps(27)]),
    R("허물의 사함을 받은 자", "Blessed is he whose transgression is forgiven", "시편", [ps(32)]),
    R("항상 주를 송축하리로다", "I will bless the Lord at all times", "시편", [ps(34)]),
    R("하나님은 우리의 피난처", "God is our refuge", "시편", [ps(46)]),
    R("정한 마음을 창조하소서", "Create in me a clean heart", "시편", [ps(51)]),
    R("하나님이 우리에게 복을 주시리로다", "God be merciful unto us", "시편", [ps(67)]),
    R("주의 장막이 사랑스러운지요", "How amiable are Thy tabernacles", "시편", [ps(84)]),
    R("주여 주는 우리의 거처", "Lord, Thou hast been our dwelling place", "시편", [ps(90)]),
    R("지존자의 은밀한 곳", "He that dwelleth in the secret place", "시편", [ps(91)]),
    R("오라 여호와께 노래하며", "O come, let us sing unto the Lord", "시편", [ps(95)]),
    R("새 노래로 여호와께", "O sing unto the Lord a new song", "시편", [ps(96)]),
    R("여호와께 찬양 새 노래", "O sing unto the Lord a new song (98)", "시편", [ps(98)]),
    R("온 땅이여 즐거이 부를지어다", "Make a joyful noise", "시편", [ps(100)]),
    R("내 영혼아 여호와를 송축", "Bless the Lord, O my soul", "시편", [ps(103)]),
    R("나의 도움이 어디서 올까", "I will lift up mine eyes", "시편", [ps(121)]),
    R("깊은 데서 주께 부르짖었나이다", "Out of the depths", "시편", [ps(130)]),
    R("형제가 연합하여 동거함", "Behold, how good and how pleasant", "시편", [ps(133)]),
    R("주께서 나를 감찰하시고", "O Lord, Thou hast searched me", "시편", [ps(139)]),
    R("왕이신 나의 하나님", "I will extol Thee, my God", "시편", [ps(145)]),
    R("호흡 있는 자마다 찬양", "Praise ye the Lord", "시편", [ps(150)]),
    # --- 성탄 ---
    R(
        "한 아기가 우리에게 났고",
        "For unto us a child is born",
        "성탄",
        [ref("Isa", 9, [2, 6, 7])],
        "이사야의 메시아 예언 (성탄)",
    ),
    R(
        "처녀가 잉태하여 아들을 낳을 것이요",
        "A virgin shall conceive",
        "성탄",
        [ref("Isa", 7, [14]), ref("Isa", 9, [6])],
    ),
    R(
        "평강의 왕",
        "The Prince of Peace",
        "성탄",
        [ref("Isa", 9, [6, 7]), ref("Isa", 11, [1, 2, 3, 4])],
    ),
    R(
        "목자들에게 나타난 천사",
        "Good tidings of great joy",
        "성탄",
        [ref("Luke", 2, [8, 9, 10, 11, 12, 13, 14])],
    ),
    R(
        "마리아의 찬가 (마그니피캇)",
        "My soul doth magnify the Lord",
        "성탄",
        [ref("Luke", 1, [46, 47, 48, 49, 50, 51, 52, 53, 54, 55])],
    ),
    R(
        "사가랴의 찬가",
        "Blessed be the Lord God of Israel",
        "성탄",
        [ref("Luke", 1, [68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79])],
    ),
    R(
        "시므온의 찬가 (눈크 디미티스)",
        "Lord, now lettest Thou Thy servant depart",
        "성탄",
        [ref("Luke", 2, [29, 30, 31, 32])],
    ),
    R(
        "말씀이 육신이 되어",
        "The Word was made flesh",
        "성탄",
        [ref("John", 1, [1, 2, 3, 4, 5, 14])],
    ),
    # --- 부활 ---
    R(
        "그가 살아나셨다",
        "He is risen",
        "부활",
        [ref("Luke", 24, [1, 2, 3, 4, 5, 6, 7])],
    ),
    R(
        "엠마오 길",
        "The road to Emmaus",
        "부활",
        [ref("Luke", 24, [13, 15, 16, 27, 30, 31, 32])],
    ),
    R(
        "부활의 첫 열매",
        "Christ the firstfruits",
        "부활",
        [ref("1Cor", 15, [3, 4, 20, 21, 22, 55, 56, 57])],
    ),
    R(
        "사망아 너의 승리가 어디 있느냐",
        "O death, where is thy sting?",
        "부활",
        [ref("1Cor", 15, [51, 52, 53, 54, 55, 56, 57])],
    ),
    R(
        "빈 무덤",
        "The empty tomb",
        "부활",
        [ref("Matt", 28, [1, 2, 5, 6, 7])],
    ),
    R(
        "내가 곧 부활이요 생명이니",
        "I am the resurrection and the life",
        "부활",
        [ref("John", 11, [25, 26]), ref("John", 14, [1, 2, 3, 6])],
    ),
    # --- 이사야 ---
    R(
        "여호와의 집에 대하여",
        "The mountain of the Lord's house",
        "이사야",
        [ref("Isa", 2, [2, 3, 4, 5])],
    ),
    R(
        "내가 여기 있나이다 나를 보내소서",
        "Here am I; send me",
        "이사야",
        [ref("Isa", 6, [1, 2, 3, 5, 6, 7, 8])],
    ),
    R(
        "광야에서 외치는 자의 소리",
        "The voice of him that crieth in the wilderness",
        "이사야",
        [ref("Isa", 40, [1, 3, 4, 5, 8, 11, 28, 29, 31])],
    ),
    R(
        "고난 받는 종",
        "The suffering servant",
        "이사야",
        [ref("Isa", 53, [3, 4, 5, 6, 7, 11, 12])],
    ),
    R(
        "오라 우리가 여호와께로 돌아가자",
        "Come, and let us return unto the Lord",
        "이사야",
        [ref("Isa", 55, [1, 6, 7, 8, 9, 10, 11])],
    ),
    R(
        "새 하늘과 새 땅",
        "New heavens and a new earth",
        "이사야",
        [ref("Isa", 65, [17, 18, 19, 24, 25])],
    ),
    # --- 누가복음 ---
    R(
        "주의 성령이 내게 임하셨으니",
        "The Spirit of the Lord is upon me",
        "누가복음",
        [ref("Luke", 4, [16, 17, 18, 19, 20, 21])],
    ),
    R(
        "심령이 가난한 자는 복이 있나니",
        "Blessed be ye poor",
        "누가복음",
        [ref("Luke", 6, [20, 21, 22, 23, 27, 28, 31, 35, 36])],
    ),
    R(
        "주 기도의 가르침 (누가)",
        "Lord, teach us to pray",
        "누가복음",
        [ref("Luke", 11, [1, 2, 3, 4, 9, 10, 13])],
    ),
    R(
        "잃은 양을 찾으시는 목자",
        "Joy over one sinner that repenteth",
        "누가복음",
        [ref("Luke", 15, [1, 2, 4, 5, 6, 7])],
    ),
    R(
        "탕자의 비유",
        "The prodigal son",
        "누가복음",
        [ref("Luke", 15, [11, 13, 17, 18, 20, 21, 22, 23, 24])],
    ),
    R(
        "십자가 위에서",
        "Father, forgive them",
        "누가복음",
        [ref("Luke", 23, [33, 34, 39, 42, 43, 46])],
    ),
]


def main() -> None:
    readings = []
    for i, raw in enumerate(CATALOG, start=1):
        readings.append(
            {
                "id": i,
                "number": str(i),
                "title_ko": raw["title_ko"],
                "title_en": raw["title_en"],
                "title": raw["title_ko"],  # backward-compatible list title
                "category": raw["category"],
                "note": raw.get("note") or "",
                "passages": raw["passages"],
                "source": "개역한글(KRV)·KJV·ASV 성경 구절 교독 (앱 자체 구성)",
            }
        )

    out = {
        "source_note": (
            "교독문은 앱에 수록된 Public Domain 성경(개역한글 KRV, KJV, ASV) 구절을 "
            "인도자/회중 교독 형식으로 구성한 것입니다. "
            "한국찬송가공회 새찬송가 교독문 번호·편집 문안을 복제하지 않았으며, "
            "개역개정(NKRV) 본문을 사용하지 않습니다. "
            "카테고리(시편·성탄·부활·이사야·누가복음)는 앱 자체 분류입니다."
        ),
        "license": "Public Domain scripture (KRV / KJV / ASV)",
        "last_updated": datetime.date.today().isoformat(),
        "count": len(readings),
        "categories": ["시편", "성탄", "부활", "이사야", "누가복음"],
        "readings": readings,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(readings)} readings -> {OUT}")
    from collections import Counter
    print("by category:", dict(Counter(r["category"] for r in readings)))


if __name__ == "__main__":
    main()
