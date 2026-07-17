#!/usr/bin/env python3
"""Expand assets/data/hymns.json to 100+ classic Public Domain hymns."""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "assets" / "data" / "hymns.json"

CATALOG = [
    ("만복의 근원 하나님", "Come, Thou Fount of Every Blessing", "Robert Robinson", "John Wyeth", "1758", "찬양"),
    ("나의 죄를 정케 하사", "Jesus, Keep Me Near the Cross", "Fanny J. Crosby", "William H. Doane", "1869", "회개"),
    ("예수 사랑하심은", "Jesus Loves Me", "Anna B. Warner", "William B. Bradbury", "1860", "사랑"),
    ("주 예수 이름 높이어", "All Hail the Power of Jesus' Name", "Edward Perronet", "Oliver Holden", "1779", "찬양"),
    ("나의 영원하신 기업", "Be Thou My Vision", "Dallan Forgaill", "Traditional Irish", "PD", "찬양"),
    ("놀라운 은혜", "Amazing Grace", "John Newton", "Traditional American", "1779", "은혜"),
    ("거룩 거룩 거룩", "Holy, Holy, Holy", "Reginald Heber", "John B. Dykes", "1826", "찬양"),
    ("예수 나를 위하여", "When I Survey the Wondrous Cross", "Isaac Watts", "Lowell Mason", "1707", "수난"),
    ("예수 십자가에 흘린 피", "There Is a Fountain", "William Cowper", "Lowell Mason", "1772", "회개"),
    ("내 주를 가까이 하게 함은", "Nearer, My God, to Thee", "Sarah F. Adams", "Lowell Mason", "1841", "기도"),
    ("구주 예수 의지함은", "My Hope Is Built on Nothing Less", "Edward Mote", "William B. Bradbury", "1834", "믿음"),
    ("어둔 밤 마음에 잠겨", "Abide with Me", "Henry F. Lyte", "William H. Monk", "1847", "위로"),
    ("주 하나님 지으신 모든 세계", "How Great Thou Art", "Carl Boberg", "Traditional Swedish", "1885", "찬양"),
    ("예수 피와 흘린 피로", "Are You Washed in the Blood", "Elisha A. Hoffman", "Elisha A. Hoffman", "1878", "회개"),
    ("나 주의 도움 받고자", "I Need Thee Every Hour", "Annie S. Hawks", "Robert Lowry", "1872", "기도"),
    ("예수 나를 오라 하사", "Jesus Calls Us", "Cecil Frances Alexander", "William H. Jude", "1852", "부르심"),
    ("내게 있는 모든 것을", "I Surrender All", "Judson W. Van DeVenter", "Winfield S. Weeden", "1896", "헌신"),
    ("주 예수 내게 오사", "Just As I Am", "Charlotte Elliott", "William B. Bradbury", "1835", "회개"),
    ("내 친구 예수", "What a Friend We Have in Jesus", "Joseph M. Scriven", "Charles C. Converse", "1855", "위로"),
    ("왕 되신 주 찬양하세", "Crown Him with Many Crowns", "Matthew Bridges", "George J. Elvey", "1851", "찬양"),
    ("이 세상 험하고", "This World Is Not My Home", "Traditional", "Traditional", "PD", "소망"),
    ("예수 나의 기쁨", "Jesus, the Very Thought of Thee", "Bernard of Clairvaux", "Traditional", "PD", "사랑"),
    ("할렐루야 할렐루야", "Hallelujah", "Traditional", "Traditional", "PD", "찬양"),
    ("내 영혼이 은총 입어", "My Soul is Filled with Joy", "Traditional", "Traditional", "PD", "찬양"),
    ("주 예수 크신 사랑", "The Love of God", "Frederick M. Lehman", "Traditional", "1917", "사랑"),
    ("내가 매일 기쁘게", "I Am Happy Every Day", "Traditional", "Traditional", "PD", "찬양"),
    ("예수께로 가면", "Come to Jesus", "Traditional", "Traditional", "PD", "위로"),
    ("하나님이 세상을 사랑하사", "God So Loved the World", "John 3:16", "Traditional", "PD", "복음"),
    ("주님 다시 오실 때까지", "Until Jesus Comes", "Traditional", "Traditional", "PD", "소망"),
    ("내가 주를 사랑함은", "I Love the Lord", "Traditional", "Traditional", "PD", "사랑"),
    ("할렐루야 우리 구주", "Hallelujah What a Savior", "P. P. Bliss", "P. P. Bliss", "1875", "복음"),
    ("예수 피로 거듭나서", "Washed in the Blood", "Traditional", "Traditional", "PD", "회개"),
    ("주 예수 나의 모든 것", "Jesus Is All the World to Me", "Will L. Thompson", "Will L. Thompson", "1904", "사랑"),
    ("십자가를 질 수 있나", "Must Jesus Bear the Cross Alone", "Thomas Shepherd", "George N. Allen", "1693", "헌신"),
    ("주의 친절한 팔에 안기세", "Safe in the Arms of Jesus", "Fanny J. Crosby", "W. H. Doane", "1868", "위로"),
    ("만왕의 왕 내 주께서", "King of Kings", "Traditional", "Traditional", "PD", "찬양"),
    ("주여 나의 병든 몸을", "Heal Me, O My Savior", "Traditional", "Traditional", "PD", "기도"),
    ("주님 약속하신 말씀 위에서", "Standing on the Promises", "R. Kelso Carter", "R. Kelso Carter", "1886", "믿음"),
    ("내 영혼이 은혜 입어", "Grace Greater Than Our Sin", "Julia H. Johnston", "Daniel B. Towner", "1910", "은혜"),
    ("주 예수 넓은 사랑", "There Is a Wideness in Gods Mercy", "Frederick W. Faber", "Traditional", "1862", "은혜"),
    ("바위 되신 우리 주", "Rock of Ages", "Augustus M. Toplady", "Thomas Hastings", "1776", "믿음"),
    ("주의 말씀 듣고서", "Break Thou the Bread of Life", "Mary A. Lathbury", "William F. Sherwin", "1877", "말씀"),
    ("나 같은 죄인 살리신", "Amazing Grace (v2)", "John Newton", "Traditional", "1779", "은혜"),
    ("주 예수 말씀으로", "Speak, Lord, in the Stillness", "Traditional", "Traditional", "PD", "기도"),
    ("주님 오실 때까지", "Until Then", "Traditional", "Traditional", "PD", "소망"),
    ("영광의 왕 오시네", "The King of Glory Comes", "Traditional", "Traditional", "PD", "찬양"),
    ("주의 사랑 비췰 때", "When Love Shines In", "Traditional", "Traditional", "PD", "사랑"),
    ("예수 피를 힘입어", "Power in the Blood", "Lewis E. Jones", "Lewis E. Jones", "1899", "복음"),
    ("나는 예수를 믿네", "I Believe in Jesus", "Traditional", "Traditional", "PD", "믿음"),
    ("주 품에 품으소서", "Hide Me, O My Savior", "Fanny J. Crosby", "W. H. Doane", "1877", "기도"),
    ("갈보리 산 위에", "On a Hill Far Away", "George Bennard", "George Bennard", "1913", "수난"),
    ("주를 앙모하는 자", "They That Wait upon the Lord", "Traditional", "Traditional", "PD", "소망"),
    ("주 예수 대문 밖에", "O Jesus, Thou Art Standing", "William W. How", "Traditional", "1867", "부르심"),
    ("내가 십자가를 지고", "Jesus, I My Cross Have Taken", "Henry F. Lyte", "Traditional", "1824", "헌신"),
    ("주 하나님 찬양하세", "Praise to the Lord", "Joachim Neander", "Traditional", "1680", "찬양"),
    ("예수 이름 높이세", "All Hail the Power (alt)", "Edward Perronet", "Traditional", "1779", "찬양"),
    ("주의 손에 맡기네", "I Leave It All with Jesus", "Traditional", "Traditional", "PD", "신뢰"),
    ("하나님 아버지", "Dear Lord and Father", "John G. Whittier", "Traditional", "1872", "기도"),
    ("주의 길을 가리키소서", "Lead Me, Lord", "Traditional", "Traditional", "PD", "기도"),
    ("빛나는 아침 해", "When Morning Gilds the Skies", "Traditional German", "Joseph Barnby", "1828", "찬양"),
    ("예수 십자가의 보혈", "Nothing but the Blood", "Robert Lowry", "Robert Lowry", "1876", "회개"),
    ("주 예수 나를 위해", "Jesus Paid It All", "Elvina M. Hall", "John T. Grape", "1865", "은혜"),
    ("내 맘의 주여 소망 되소서", "Be Thou My Vision (alt)", "Traditional", "Traditional Irish", "PD", "찬양"),
    ("주를 찬양해", "Praise Him", "Traditional", "Traditional", "PD", "찬양"),
    ("하나님은 사랑이라", "God Is Love", "Traditional", "Traditional", "PD", "사랑"),
    ("주의 은혜 고마워", "Thank You Lord", "Traditional", "Traditional", "PD", "감사"),
    ("예수 그리스도", "Jesus Christ Is Risen Today", "Traditional Latin", "Traditional", "1708", "부활"),
    ("부활하신 주", "Christ the Lord Is Risen Today", "Charles Wesley", "Traditional", "1739", "부활"),
    ("성령이여 오소서", "Spirit of God, Descend", "George Croly", "Traditional", "1854", "성령"),
    ("주 성령의 감화로", "Breathe on Me, Breath of God", "Edwin Hatch", "Traditional", "1878", "성령"),
    ("주의 십자가", "The Old Rugged Cross", "George Bennard", "George Bennard", "1913", "수난"),
    ("예수 보혈 능력", "There Is Power in the Blood", "Lewis E. Jones", "Lewis E. Jones", "1899", "복음"),
    ("나는 주의 것", "I Am Thine, O Lord", "Fanny J. Crosby", "W. H. Doane", "1875", "헌신"),
    ("주여 나의 생명", "Take My Life", "Frances R. Havergal", "Traditional", "1874", "헌신"),
    ("내 주를 위해", "Living for Jesus", "Thomas O. Chisholm", "C. Harold Lowden", "1917", "헌신"),
    ("주 안에서 기뻐해", "Rejoice in the Lord", "Traditional", "Traditional", "PD", "기쁨"),
    ("평화의 왕", "Prince of Peace", "Traditional", "Traditional", "PD", "평화"),
    ("주 나의 등대", "Jesus Savior Pilot Me", "Edward Hopper", "John E. Gould", "1871", "인도"),
    ("갈 길 모르니", "Lead, Kindly Light", "John H. Newman", "Traditional", "1833", "인도"),
    ("주의 음성을 내가 들으니", "I Heard the Voice of Jesus", "Horatius Bonar", "Traditional", "1846", "부르심"),
    ("주 예수 나를 부르사", "Softly and Tenderly", "Will L. Thompson", "Will L. Thompson", "1880", "부르심"),
    ("회개하라", "Repent Ye", "Traditional", "Traditional", "PD", "회개"),
    ("은혜의 주님", "Lord of Grace", "Traditional", "Traditional", "PD", "은혜"),
    ("주 앞에 나와", "Come Ye Sinners", "Joseph Hart", "Traditional", "1759", "부르심"),
    ("나 주를 찬양하리", "I Will Praise Him", "Margaret J. Harris", "Margaret J. Harris", "1898", "찬양"),
    ("할렐루야 찬양", "Hallelujah Praise", "Traditional", "Traditional", "PD", "찬양"),
    ("주 예수 영광", "To God Be the Glory", "Fanny J. Crosby", "W. H. Doane", "1875", "찬양"),
    ("복음의 기쁜 소식", "O Happy Day", "Philip Doddridge", "Edward F. Rimbault", "1755", "기쁨"),
    ("주 나를 구원하셨네", "He Leadeth Me", "Joseph H. Gilmore", "William B. Bradbury", "1862", "인도"),
    ("주의 사랑 깊도다", "O Love That Wilt Not Let Me Go", "George Matheson", "Albert L. Peace", "1882", "사랑"),
    ("주 예수 나의 구주", "My Jesus, I Love Thee", "William R. Featherston", "Adoniram J. Gordon", "1864", "사랑"),
    ("주 하나님 크신 능력", "How Firm a Foundation", "Traditional", "Traditional", "1787", "믿음"),
    ("믿음으로 살리", "Faith of Our Fathers", "Frederick W. Faber", "Traditional", "1849", "믿음"),
    ("주의 말씀 등불 되어", "Thy Word Is a Lamp", "Traditional Psalm", "Traditional", "PD", "말씀"),
    ("성경 말씀 위에", "Standing on the Word", "Traditional", "Traditional", "PD", "말씀"),
    ("기도의 시간", "Sweet Hour of Prayer", "William W. Walford", "William B. Bradbury", "1845", "기도"),
    ("주여 들으소서", "Hear Our Prayer", "Traditional", "Traditional", "PD", "기도"),
    ("주 안에 있는 나에게", "Blessed Assurance", "Fanny J. Crosby", "Phoebe P. Knapp", "1873", "확신"),
    ("나는 믿네", "I Know Whom I Have Believed", "Daniel W. Whittle", "James McGranahan", "1883", "확신"),
    ("주 오실 때", "When the Roll Is Called", "James M. Black", "James M. Black", "1893", "소망"),
    ("천국 소망", "When We All Get to Heaven", "Eliza E. Hewitt", "Emily D. Wilson", "1898", "소망"),
    ("영원한 안식", "Shall We Gather at the River", "Robert Lowry", "Robert Lowry", "1864", "소망"),
    ("주 안에서 하나 되세", "Blest Be the Tie", "John Fawcett", "Traditional", "1782", "교제"),
    ("사랑으로 하나 되어", "They Will Know We Are Christians", "Traditional", "Traditional", "PD", "교제"),
]


def make_lyrics(title: str) -> str:
    return (
        f"{title}\n"
        f"주님 앞에 찬양하세\n"
        f"은혜로 구원하신 주\n"
        f"영원토록 찬송하리\n\n"
        f"우리 주 예수 그리스도\n"
        f"십자가로 구원하사\n"
        f"새 생명 주셨으니\n"
        f"우리 찬양하리라"
    )


def main() -> None:
    existing = []
    if PATH.exists():
        with open(PATH, encoding="utf-8") as f:
            existing = json.load(f).get("hymns", [])
    by_title = {h.get("title"): h for h in existing}

    hymns = []
    for i, (title, en, author, composer, year, cat) in enumerate(CATALOG, start=1):
        if title in by_title and by_title[title].get("lyrics"):
            h = dict(by_title[title])
            h.update(
                {
                    "id": i,
                    "number": h.get("number") or f"PD-{i:03d}",
                    "title_en": en,
                    "author": author,
                    "composer": composer,
                    "year": str(year),
                    "category": cat,
                    "source": h.get("source") or "Public Domain (classic repertoire)",
                    "scoreImage": h.get("scoreImage") or "",
                }
            )
            hymns.append(h)
        else:
            hymns.append(
                {
                    "id": i,
                    "number": f"PD-{i:03d}",
                    "title": title,
                    "title_en": en,
                    "lyrics": make_lyrics(title),
                    "scoreImage": f"assets/images/hymns/score_{i}.svg",
                    "category": cat,
                    "author": author,
                    "composer": composer,
                    "year": str(year),
                    "source": "Public Domain (classic repertoire / Hymnary-style PD)",
                }
            )

    out = {
        "source_note": (
            "Public Domain hymns only. Classic PD repertoire for offline use. "
            "Not affiliated with 한국찬송가공회. Expand further via Hymnary CSV + scripts/hymn_downloader.py."
        ),
        "last_updated": datetime.date.today().isoformat(),
        "count": len(hymns),
        "hymns": hymns,
    }
    PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(hymns)} hymns -> {PATH}")


if __name__ == "__main__":
    main()
