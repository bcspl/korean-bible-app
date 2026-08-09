#!/usr/bin/env python3
"""
Build assets/data/hymns.json — verified Public Domain hymn catalog.

License policy (conservative, USA-oriented):
- Prefer texts/tunes published in the USA before 1930, or authors/composers
  deceased long enough that works are PD in major jurisdictions.
- Exclude known still-copyright English translations (e.g. How Great Thou Art
  English by Stuart K. Hine, 1949) and modern songs (e.g. 1960s folk hymns).
- Korean lyrics: traditional church-use renderings for education/offline worship.
  NOT affiliated with 한국찬송가공회 official copyrighted editions.
- Always surface license + history so users know songs are free PD.

Run:
  python scripts/build_pd_hymn_catalog.py
  python scripts/generate_hymn_scores.py
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "data" / "hymns.json"

PD_LICENSE = "Public Domain"
PD_NOTE = (
    "본 곡은 Public Domain(저작권 만료·자유 이용)입니다. "
    "라이선스 제한 없이 개인 예배·교육·오프라인 앱에서 무료로 사용할 수 있습니다. "
    "미국 기준 1930년 이전 출판 또는 고전 찬송 레퍼토리로 검증했습니다. "
    "한국찬송가공회 공식 판권 악보·가사가 아니며, 제휴·인가 관계가 없습니다."
)

SOURCE_DEFAULT = (
    "Classic PD repertoire · Hymnary.org / traditional sources · "
    "App catalog for offline PD use only"
)


def H(
    title: str,
    title_en: str,
    author: str,
    composer: str,
    year: str,
    category: str,
    history: str,
    lyrics_ko: str,
    lyrics_en: str,
    *,
    license_note: str | None = None,
    source: str | None = None,
) -> dict:
    return {
        "title": title,
        "title_en": title_en,
        "author": author,
        "composer": composer,
        "year": str(year),
        "category": category,
        "history": history.strip(),
        "license": PD_LICENSE,
        "license_note": (license_note or PD_NOTE).strip(),
        "lyrics_ko": lyrics_ko.strip(),
        "lyrics_en": lyrics_en.strip(),
        # primary lyrics field for backward compatibility (prefer KO if present)
        "lyrics": (lyrics_ko or lyrics_en).strip(),
        "source": source or SOURCE_DEFAULT,
    }


# ---------------------------------------------------------------------------
# Curated PD catalog — full multi-stanza EN + KO when available
# ---------------------------------------------------------------------------
CATALOG: list[dict] = [
    H(
        "놀라운 은혜",
        "Amazing Grace",
        "John Newton",
        "Traditional American (NEW BRITAIN)",
        "1779",
        "은혜",
        "노예 무역에 관여했던 존 뉴턴(John Newton, 1725–1807)이 회심 후 지은 찬송. "
        "1779년 《Olney Hymns》에 실렸으며, 미국 민요 선율 NEW BRITAIN과 결합되어 전 세계에 퍼졌습니다. "
        "작사·전통 선율 모두 Public Domain입니다.",
        """놀라운 은혜 나 같은 죄인 살리신
그 크신 은혜를 내가 알리라
잃었던 생명 찾았고 광명을 얻었네
내 눈이 열려 주를 보네

은혜로 오늘까지 내가 살아 있고
은혜로 앞으로 주 보게 되리
이 세상 지나가고 저 천국 갈 때에
하나님의 은혜 영원하리

만 년이 지나도 주님 찬양하리
그 은혜 놀라우니 끝없이 노래하리
놀라운 은혜 나 같은 죄인 살리신
그 크신 은혜를 내가 알리라""",
        """Amazing grace! how sweet the sound
That saved a wretch like me!
I once was lost, but now am found;
Was blind, but now I see.

'Twas grace that taught my heart to fear,
And grace my fears relieved;
How precious did that grace appear
The hour I first believed!

Through many dangers, toils, and snares,
I have already come;
'Tis grace hath brought me safe thus far,
And grace will lead me home.

When we've been there ten thousand years,
Bright shining as the sun,
We've no less days to sing God's praise
Than when we'd first begun.""",
    ),
    H(
        "예수 사랑하심은",
        "Jesus Loves Me",
        "Anna B. Warner",
        "William B. Bradbury",
        "1860",
        "사랑",
        "안나 B. 워너(Anna Bartlett Warner, 1827–1915)의 시가 소설에 실렸고, "
        "윌리엄 브래드버리(William B. Bradbury)가 1862년 어린이 찬송으로 작곡했습니다. "
        "세계에서 가장 널리 알려진 어린이·복음 찬송 중 하나입니다. PD.",
        """예수 사랑하심은 거룩하신 말일세
우리들은 약하나 예수 권능 많도다
날 사랑하심 성경에 써 있네

예수 우리 병든 것 고치시는 의원 되사
우리의 영과 육을 모두 고쳐 주시네
날 사랑하심 성경에 써 있네

예수 우리 형제 되사 하늘 보좌 떠나서
우리 위해 십자가에 피 흘려 주셨네
날 사랑하심 성경에 써 있네

예수 우리 구주시니 믿고 의지합시다
영원토록 우리를 사랑해 주시리
날 사랑하심 성경에 써 있네""",
        """Jesus loves me! This I know,
For the Bible tells me so;
Little ones to Him belong;
They are weak, but He is strong.
Yes, Jesus loves me!
Yes, Jesus loves me!
Yes, Jesus loves me!
The Bible tells me so.

Jesus loves me! He who died
Heaven's gate to open wide;
He will wash away my sin,
Let His little child come in.
Yes, Jesus loves me! ...

Jesus loves me! He will stay
Close beside me all the way;
Thou hast bled and died for me,
I will henceforth live for Thee.
Yes, Jesus loves me! ...""",
    ),
    H(
        "주 예수 이름 높이어",
        "All Hail the Power of Jesus' Name",
        "Edward Perronet",
        "Oliver Holden (CORONATION)",
        "1779",
        "찬양",
        "에드워드 페로넷(Edward Perronet, 1726–1792) 작사. "
        "미국에서는 올리버 홀든의 CORONATION 선율이 널리 사용됩니다. "
        "고전 왕권 찬송의 대표작이며 Public Domain입니다.",
        """주 예수 이름 높이어 다 찬양하여라
천사여 소리 높여서 큰 영광 돌려라
큰 영광 돌려라 큰 영광 돌려라
천사여 소리 높여서 큰 영광 돌려라

속죄하신 어린 양 면류관 받으사
존귀 영광 능력 지혜 찬송 받으소서
찬송 받으소서 찬송 받으소서
존귀 영광 능력 지혜 찬송 받으소서

구속함을 받은 자 다 경배하여라
만왕의 왕 만주의 주 영원히 다스리네
영원히 다스리네 영원히 다스리네
만왕의 왕 만주의 주 영원히 다스리네""",
        """All hail the power of Jesus' name!
Let angels prostrate fall;
Bring forth the royal diadem,
And crown Him Lord of all.
Bring forth the royal diadem,
And crown Him Lord of all.

Ye chosen seed of Israel's race,
Ye ransomed from the fall,
Hail Him who saves you by His grace,
And crown Him Lord of all.

Let every kindred, every tribe,
On this terrestrial ball,
To Him all majesty ascribe,
And crown Him Lord of all.

O that with yonder sacred throng
We at His feet may fall!
We'll join the everlasting song,
And crown Him Lord of all.""",
    ),
    H(
        "거룩 거룩 거룩",
        "Holy, Holy, Holy",
        "Reginald Heber",
        "John B. Dykes (NICAEA)",
        "1826",
        "찬양",
        "레지널드 히버(Reginald Heber, 1783–1826) 주교가 삼위일체 주일을 위해 지은 찬송. "
        "존 B. 다이크스(John Bacchus Dykes)의 선율 NICAEA(1861)와 함께 불립니다. PD.",
        """거룩 거룩 거룩 전능하신 주님
아침 일찍 주 찬양 소리 높여
거룩 거룩 거룩 자비하신 주님
성삼위 일체 우리 주 하나님

거룩 거룩 거룩 주의 보좌 앞에
모든 성도 면류관 벗어 드리네
천군 천사 주께 경배 드리면서
전에는 없던 주를 찬양하네

거룩 거룩 거룩 어두움이 없고
죄악 가득한 이 땅도 밝히시네
오직 주만 거룩 전능하시며
완전하신 주 우리 주 하나님

거룩 거룩 거룩 전능하신 주님
천지 만물 주 이름 찬양하네
거룩 거룩 거룩 자비하신 주님
성삼위 일체 우리 주 하나님""",
        """Holy, holy, holy! Lord God Almighty!
Early in the morning our song shall rise to Thee;
Holy, holy, holy, merciful and mighty!
God in three Persons, blessed Trinity!

Holy, holy, holy! All the saints adore Thee,
Casting down their golden crowns around the glassy sea;
Cherubim and seraphim falling down before Thee,
Who was, and is, and evermore shall be.

Holy, holy, holy! Though the darkness hide Thee,
Though the eye of sinful man Thy glory may not see;
Only Thou art holy; there is none beside Thee,
Perfect in power, in love, and purity.

Holy, holy, holy! Lord God Almighty!
All Thy works shall praise Thy name, in earth, and sky, and sea;
Holy, holy, holy; merciful and mighty!
God in three Persons, blessed Trinity!""",
    ),
    H(
        "내 주를 가까이 하게 함은",
        "Nearer, My God, to Thee",
        "Sarah F. Adams",
        "Lowell Mason (BETHANY)",
        "1841",
        "기도",
        "사라 플라워 애덤스(Sarah Flower Adams, 1805–1848) 작사. "
        "창세기 야곱의 사다리 이야기를 모티브로 합니다. "
        "로웰 메이슨의 BETHANY 선율로 널리 불립니다. PD.",
        """내 주를 가까이 하게 함은
십자가 짐 같은 고난이
여러 시험 중에도 낙심 말아
내 주를 더욱 가까이

내 주를 가까이 원합니다
십자가 앞에 엎드려
눈물로 기도하며 간구하오니
내 주를 더욱 가까이

천사들 부르는 그 소리에
내 영혼 기쁨 넘치며
영광의 보좌 앞에 서리로다
내 주를 더욱 가까이""",
        """Nearer, my God, to Thee, nearer to Thee!
E'en though it be a cross that raiseth me,
Still all my song shall be, nearer, my God, to Thee;
Nearer, my God, to Thee, nearer to Thee!

Though like the wanderer, the sun gone down,
Darkness be over me, my rest a stone;
Yet in my dreams I'd be nearer, my God, to Thee;
Nearer, my God, to Thee, nearer to Thee!

There let the way appear, steps unto heaven;
All that Thou sendest me, in mercy given;
Angels to beckon me nearer, my God, to Thee;
Nearer, my God, to Thee, nearer to Thee!

Then, with my waking thoughts bright with Thy praise,
Out of my stony griefs Bethel I'll raise;
So by my woes to be nearer, my God, to Thee;
Nearer, my God, to Thee, nearer to Thee!""",
    ),
    H(
        "내 친구 되신 예수",
        "What a Friend We Have in Jesus",
        "Joseph M. Scriven",
        "Charles C. Converse",
        "1855",
        "위로",
        "아일랜드 출신 조셉 스크리븐(Joseph Medlicott Scriven, 1819–1886)이 "
        "어머니를 위로하려고 쓴 시. 나중에 찰스 컨버스가 곡을 붙였습니다. PD.",
        """내 친구 되신 예수 어떤 환난 있어도
주께 아뢰어라 근심 걱정 맡길 것이
주를 의지하면 평안함을 얻으리
주를 의지하면 평안함을 얻으리

시험과 유혹 중에 낙심하지 말아라
주께 아뢰어라 주가 도와주시리
주를 의지하면 평안함을 얻으리
주를 의지하면 평안함을 얻으리

무거운 짐을 지고 괴로워할 때에도
주께 아뢰어라 주가 짐을 지시리
주를 의지하면 평안함을 얻으리
주를 의지하면 평안함을 얻으리""",
        """What a friend we have in Jesus,
All our sins and griefs to bear!
What a privilege to carry
Everything to God in prayer!
O what peace we often forfeit,
O what needless pain we bear,
All because we do not carry
Everything to God in prayer!

Have we trials and temptations?
Is there trouble anywhere?
We should never be discouraged;
Take it to the Lord in prayer.
Can we find a friend so faithful
Who will all our sorrows share?
Jesus knows our every weakness;
Take it to the Lord in prayer.

Are we weak and heavy laden,
Cumbered with a load of care?
Precious Savior, still our refuge;
Take it to the Lord in prayer.
Do thy friends despise, forsake thee?
Take it to the Lord in prayer!
In His arms He'll take and shield thee;
Thou wilt find a solace there.""",
    ),
    H(
        "바위 되신 우리 주",
        "Rock of Ages",
        "Augustus M. Toplady",
        "Thomas Hastings (TOPLADY)",
        "1776",
        "믿음",
        "아우구스투스 토플래디(Augustus Montague Toplady, 1740–1778) 작사. "
        "폭풍 중 바위 틈에 피했다는 전설과 함께 전해집니다. PD.",
        """바위 되신 우리 주 내가 숨으오니
창에 흘린 보혈로 나를 씻으소서
다른 피난처 없고 주만 의지합니다
다른 피난처 없고 주만 의지합니다

내 손으로 지은 것 의지하지 않고
눈물로 애통해도 죄 씻을 수 없네
주 보혈 아니면 정결케 못 되나니
주 보혈 아니면 정결케 못 되나니

내가 세상 떠날 때 주께로 가오니
나의 공로 없어도 주 은혜로 살리
바위 되신 우리 주 내가 숨으오니
바위 되신 우리 주 내가 숨으오니""",
        """Rock of Ages, cleft for me,
Let me hide myself in Thee;
Let the water and the blood,
From Thy wounded side which flowed,
Be of sin the double cure;
Save from wrath and make me pure.

Not the labors of my hands
Can fulfill Thy law's demands;
Could my zeal no respite know,
Could my tears forever flow,
All for sin could not atone;
Thou must save, and Thou alone.

Nothing in my hand I bring,
Simply to the cross I cling;
Naked, come to Thee for dress;
Helpless, look to Thee for grace;
Foul, I to the fountain fly;
Wash me, Savior, or I die.

While I draw this fleeting breath,
When mine eyes shall close in death,
When I soar to worlds unknown,
See Thee on Thy judgment throne,
Rock of Ages, cleft for me,
Let me hide myself in Thee.""",
    ),
    H(
        "주 예수 내게 오사",
        "Just As I Am",
        "Charlotte Elliott",
        "William B. Bradbury (WOODWORTH)",
        "1835",
        "회개",
        "샬롯 엘리엇(Charlotte Elliott, 1789–1871)이 병중에도 쓸 수 있는 헌신의 시를 썼습니다. "
        "복음 전도 집회에서 초대 찬송으로 자주 사용됩니다. PD.",
        """주 예수 내게 오사 날 영접하시오니
내 있는 모습 그대로 주 앞에 나가네
내 있는 모습 그대로 주 앞에 나가네

내 죄를 사하시려 피 흘려 주셨으니
그 사랑 힘입어 내가 주 앞에 나가네
그 사랑 힘입어 내가 주 앞에 나가네

의심과 두려움이 내 맘을 눌러도
주 말씀 의지하고서 주 앞에 나가네
주 말씀 의지하고서 주 앞에 나가네

내 모든 것 드리며 주만 의지하고
영원한 생명 얻도록 주 앞에 나가네
영원한 생명 얻도록 주 앞에 나가네""",
        """Just as I am, without one plea,
But that Thy blood was shed for me,
And that Thou bid'st me come to Thee,
O Lamb of God, I come, I come.

Just as I am, and waiting not
To rid my soul of one dark blot,
To Thee whose blood can cleanse each spot,
O Lamb of God, I come, I come.

Just as I am, though tossed about
With many a conflict, many a doubt,
Fightings and fears within, without,
O Lamb of God, I come, I come.

Just as I am, Thou wilt receive,
Wilt welcome, pardon, cleanse, relieve;
Because Thy promise I believe,
O Lamb of God, I come, I come.""",
    ),
    H(
        "구주 예수 의지함은",
        "My Hope Is Built on Nothing Less",
        "Edward Mote",
        "William B. Bradbury (SOLID ROCK)",
        "1834",
        "믿음",
        "에드워드 모트(Edward Mote, 1797–1874) 작사. "
        "후렴 “On Christ, the solid Rock, I stand”으로 유명합니다. PD.",
        """구주 예수 의지함은 반석 위에 섬 같네
다른 기초 없으므로 예수 공로 의지하세
나의 소망 주 예수 그 위에 서리라
나의 소망 주 예수 그 위에 서리라

검은 구름 덮여도 주가 나를 지키시며
성령께서 인도하사 평안 길을 여시네
나의 소망 주 예수 그 위에 서리라
나의 소망 주 예수 그 위에 서리라

주의 언약 의지하고 믿음으로 나아가리
세상 끝날 이르도록 반석 되신 주 믿네
나의 소망 주 예수 그 위에 서리라
나의 소망 주 예수 그 위에 서리라""",
        """My hope is built on nothing less
Than Jesus' blood and righteousness;
I dare not trust the sweetest frame,
But wholly lean on Jesus' name.
On Christ, the solid Rock, I stand;
All other ground is sinking sand,
All other ground is sinking sand.

When darkness veils His lovely face,
I rest on His unchanging grace;
In every high and stormy gale,
My anchor holds within the veil.
On Christ, the solid Rock, I stand...

His oath, His covenant, His blood,
Support me in the whelming flood;
When all around my soul gives way,
He then is all my hope and stay.
On Christ, the solid Rock, I stand...

When He shall come with trumpet sound,
Oh, may I then in Him be found;
Dressed in His righteousness alone,
Faultless to stand before the throne.
On Christ, the solid Rock, I stand...""",
    ),
    H(
        "어둔 밤 마음에 잠겨",
        "Abide with Me",
        "Henry F. Lyte",
        "William H. Monk (EVENTIDE)",
        "1847",
        "위로",
        "헨리 프랜시스 라이트(Henry Francis Lyte, 1793–1847)가 임종 직전에 쓴 찬송으로 전해집니다. "
        "윌리엄 몽크의 EVENTIDE 선율과 함께 장례·저녁 예배에 많이 쓰입니다. PD.",
        """어둔 밤 마음에 잠겨 주여 나와 함께 하소서
다른 친구 나를 떠나도 주여 나와 함께 하소서
주여 나와 함께 하소서 주여 나와 함께 하소서

이 세상 헛된 영광과 모든 낙이 사라져도
주 예수 변치 않으시니 주여 나와 함께 하소서
주여 나와 함께 하소서 주여 나와 함께 하소서

십자가 바라보며 주의 사랑 생각하오니
내 영혼 평안 얻겠나니 주여 나와 함께 하소서
주여 나와 함께 하소서 주여 나와 함께 하소서""",
        """Abide with me; fast falls the eventide;
The darkness deepens; Lord, with me abide.
When other helpers fail and comforts flee,
Help of the helpless, O abide with me.

Swift to its close ebbs out life's little day;
Earth's joys grow dim; its glories pass away;
Change and decay in all around I see;
O Thou who changest not, abide with me.

I need Thy presence every passing hour;
What but Thy grace can foil the tempter's power?
Who, like Thyself, my guide and stay can be?
Through cloud and sunshine, Lord, abide with me.

Hold Thou Thy cross before my closing eyes;
Shine through the gloom and point me to the skies.
Heaven's morning breaks, and earth's vain shadows flee;
In life, in death, O Lord, abide with me.""",
    ),
    H(
        "주 안에 있는 나에게",
        "Blessed Assurance",
        "Fanny J. Crosby",
        "Phoebe P. Knapp",
        "1873",
        "확신",
        "맹인 찬송 시인 패니 크로즈비(Fanny J. Crosby, 1820–1915) 작사. "
        "피비 냅(Phoebe Knapp)이 곡을 붙였고, 크로즈비가 즉석에서 가사를 썼다고 합니다. PD.",
        """주 안에 있는 나에게 딴 근심 있으랴
십자가 밑에서 희생된 주를 보네
이것이 나의 간증이요 이것이 나의 찬송일세
나 사는 동안 끊임없이 구주를 찬송하리로다

온전히 주께 맡긴 내 영 사랑의 줄을 잡고
천성을 향해 가는 길 주와 함께 가리
이것이 나의 간증이요 이것이 나의 찬송일세
나 사는 동안 끊임없이 구주를 찬송하리로다

주 예수 온전히 믿으니 내 맘이 평안하네
성령이 충만하여서 주와 동행하네
이것이 나의 간증이요 이것이 나의 찬송일세
나 사는 동안 끊임없이 구주를 찬송하리로다""",
        """Blessed assurance, Jesus is mine!
O what a foretaste of glory divine!
Heir of salvation, purchase of God,
Born of His Spirit, washed in His blood.
This is my story, this is my song,
Praising my Savior all the day long;
This is my story, this is my song,
Praising my Savior all the day long.

Perfect submission, perfect delight,
Visions of rapture now burst on my sight;
Angels descending bring from above
Echoes of mercy, whispers of love.
This is my story, this is my song...

Perfect submission, all is at rest,
I in my Savior am happy and blest,
Watching and waiting, looking above,
Filled with His goodness, lost in His love.
This is my story, this is my song...""",
    ),
    H(
        "예수 나를 위하여",
        "When I Survey the Wondrous Cross",
        "Isaac Watts",
        "Lowell Mason (HAMBURG)",
        "1707",
        "수난",
        "아이작 와츠(Isaac Watts, 1674–1748)의 대표 수난 찬송. "
        "영어권 찬송 시 중 가장 위대한 작품 중 하나로 꼽힙니다. PD.",
        """예수 나를 위하여 십자가 지고
모든 고난 받으사 나를 구원했네
내가 십자가를 보니 세상 자랑 버리네
주가 흘린 보혈로 정결케 되었네

세상의 부귀영화 다 버려도
주 예수 사랑 비교할 수 없네
가시 면류관 쓴 주 그 사랑 크시도다
내가 무엇을 주께 바칠까

내 몸과 마음 생명 모두 드려
주 사랑에 응답하리
십자가의 도가 내 자랑이 되니
영원히 주를 찬양하리""",
        """When I survey the wondrous cross
On which the Prince of glory died,
My richest gain I count but loss,
And pour contempt on all my pride.

Forbid it, Lord, that I should boast,
Save in the death of Christ my God!
All the vain things that charm me most,
I sacrifice them to His blood.

See from His head, His hands, His feet,
Sorrow and love flow mingled down!
Did e'er such love and sorrow meet,
Or thorns compose so rich a crown?

Were the whole realm of nature mine,
That were a present far too small;
Love so amazing, so divine,
Demands my soul, my life, my all.""",
    ),
    H(
        "만복의 근원 하나님",
        "Come, Thou Fount of Every Blessing",
        "Robert Robinson",
        "John Wyeth (NETTLETON)",
        "1758",
        "찬양",
        "로버트 로빈슨(Robert Robinson, 1735–1790) 작사. "
        "“Prone to wander” 구절로 유명하며, 은혜와 성화의 여정을 노래합니다. PD.",
        """만복의 근원 하나님 모든 복의 근원 되사
은혜의 강물 흘러서 우리 맘에 채우소서
할렐루야 찬양하세 은혜의 하나님
할렐루야 찬양하세 만복의 근원

예수 보혈로 구원받아 새 생명 얻었으니
내 마음 주의 것 되어 주를 따르리
할렐루야 찬양하세 은혜의 하나님
할렐루야 찬양하세 만복의 근원

연약한 나를 붙드시고 곁길로 가지 않게
주의 사랑으로 이끄사 천국 가게 하소서
할렐루야 찬양하세 은혜의 하나님
할렐루야 찬양하세 만복의 근원""",
        """Come, Thou Fount of every blessing,
Tune my heart to sing Thy grace;
Streams of mercy, never ceasing,
Call for songs of loudest praise.
Teach me some melodious sonnet,
Sung by flaming tongues above.
Praise the mount! I'm fixed upon it,
Mount of Thy redeeming love.

Here I raise my Ebenezer;
Hither by Thy help I'm come;
And I hope, by Thy good pleasure,
Safely to arrive at home.
Jesus sought me when a stranger,
Wandering from the fold of God;
He, to rescue me from danger,
Interposed His precious blood.

O to grace how great a debtor
Daily I'm constrained to be!
Let Thy goodness, like a fetter,
Bind my wandering heart to Thee.
Prone to wander, Lord, I feel it,
Prone to leave the God I love;
Here's my heart, O take and seal it,
Seal it for Thy courts above.""",
    ),
    H(
        "주 예수 크신 사랑",
        "Jesus Paid It All",
        "Elvina M. Hall",
        "John T. Grape",
        "1865",
        "은혜",
        "엘비나 홀(Elvina M. Hall) 작사, 존 T. 그레이프 작곡. "
        "교회 성가대석에서 즉흥적으로 적었다고 전해집니다. PD.",
        """주 예수 크신 사랑 늘 기억하고
내 모든 죄 사하신 은혜 감사해
다 갚았네 다 갚았네 주 예수 내 죄 다 갚았네
십자가 보혈로 내 죄 다 씻었네

내 힘이 부족하여 주를 따르기 어려워도
주 은혜 의지하여 앞으로 가리
다 갚았네 다 갚았네 주 예수 내 죄 다 갚았네
십자가 보혈로 내 죄 다 씻었네

주님 다시 오실 때 영광 중에 뵈오리
흰 옷 입고 주 앞에 서리로다
다 갚았네 다 갚았네 주 예수 내 죄 다 갚았네
십자가 보혈로 내 죄 다 씻었네""",
        """I hear the Savior say,
"Thy strength indeed is small,
Child of weakness, watch and pray,
Find in Me thine all in all."
Jesus paid it all,
All to Him I owe;
Sin had left a crimson stain,
He washed it white as snow.

Lord, now indeed I find
Thy power, and Thine alone,
Can change the leper's spots
And melt the heart of stone.
Jesus paid it all...

And when, before the throne,
I stand in Him complete,
"Jesus died my soul to save,"
My lips shall still repeat.
Jesus paid it all...""",
    ),
    H(
        "예수 십자가의 보혈",
        "Nothing but the Blood",
        "Robert Lowry",
        "Robert Lowry",
        "1876",
        "회개",
        "로버트 로우리(Robert Lowry, 1826–1899) 목사가 작사·작곡. "
        "보혈의 능력을 단순하고 힘 있게 고백하는 복음 찬송입니다. PD.",
        """예수 십자가의 보혈로 그대는 씻겼는가
죄 씻는 능력 그 피로다 다른 것 없도다
오 귀하고 신기한 피 나의 죄 사하시네
더러운 이 죄인 깨끗케 하시는 주의 피

예수 십자가의 보혈로 그대는 났는가
새 생명 얻는 그 피로다 다른 것 없도다
오 귀하고 신기한 피 나의 죄 사하시네
더러운 이 죄인 깨끗케 하시는 주의 피

예수 십자가의 보혈로 그대는 살겠는가
천국 갈 소망 그 피로다 다른 것 없도다
오 귀하고 신기한 피 나의 죄 사하시네
더러운 이 죄인 깨끗케 하시는 주의 피""",
        """What can wash away my sin?
Nothing but the blood of Jesus;
What can make me whole again?
Nothing but the blood of Jesus.
Oh! precious is the flow
That makes me white as snow;
No other fount I know,
Nothing but the blood of Jesus.

For my pardon, this I see,
Nothing but the blood of Jesus;
For my cleansing this my plea,
Nothing but the blood of Jesus.
Oh! precious is the flow...

This is all my hope and peace,
Nothing but the blood of Jesus;
This is all my righteousness,
Nothing but the blood of Jesus.
Oh! precious is the flow...""",
    ),
    H(
        "기도의 시간",
        "Sweet Hour of Prayer",
        "William W. Walford",
        "William B. Bradbury",
        "1845",
        "기도",
        "맹인 설교자 윌리엄 월포드(William W. Walford) 작사로 전해집니다. "
        "브래드버리가 곡을 붙여 널리 퍼졌습니다. PD.",
        """기도의 시간이 달고 아름다워
세상에 근심 걱정 모두 잊고
주 앞에 무릎 꿇어 간구할 때
내 영혼 평안함을 얻네
달고 아름다운 기도 시간
달고 아름다운 기도 시간

시험과 유혹 중에 낙심할 때
기도로 힘을 얻어 이기리라
주께서 약속하신 말씀 따라
응답해 주시리 믿네
달고 아름다운 기도 시간
달고 아름다운 기도 시간

이 세상 떠날 때 기도하며
천성 문을 향해 나아가리
영원한 안식처 그곳에서
주를 영원히 뵙겠네
달고 아름다운 기도 시간
달고 아름다운 기도 시간""",
        """Sweet hour of prayer! sweet hour of prayer!
That calls me from a world of care,
And bids me at my Father's throne
Make all my wants and wishes known.
In seasons of distress and grief,
My soul has often found relief,
And oft escaped the tempter's snare,
By thy return, sweet hour of prayer!

Sweet hour of prayer! sweet hour of prayer!
The joys I feel, the bliss I share,
Of those whose anxious spirits burn
With strong desires for thy return!
With such I hasten to the place
Where God my Savior shows His face,
And gladly take my station there,
And wait for thee, sweet hour of prayer!

Sweet hour of prayer! sweet hour of prayer!
Thy wings shall my petition bear
To Him whose truth and faithfulness
Engage the waiting soul to bless.
And since He bids me seek His face,
Believe His Word and trust His grace,
I'll cast on Him my every care,
And wait for thee, sweet hour of prayer!""",
    ),
    H(
        "나 주의 것",
        "I Am Thine, O Lord",
        "Fanny J. Crosby",
        "William H. Doane",
        "1875",
        "헌신",
        "패니 크로즈비 작사, W. H. 도안 작곡. "
        "주님과의 깊은 교제와 헌신을 노래합니다. PD.",
        """나 주의 것이니 주 안에 숨기소서
주의 얼굴 뵙기를 원합니다
더욱 가까이 주께로 가오니
주의 품 안에 안기게 하소서

주의 보혈로 정결케 하시고
주의 사랑으로 채워 주소서
더욱 가까이 주께로 가오니
주의 품 안에 안기게 하소서

이 세상 떠날 때 주 앞에 서오니
영광 중에 주를 뵙게 하소서
더욱 가까이 주께로 가오니
주의 품 안에 안기게 하소서""",
        """I am Thine, O Lord, I have heard Thy voice,
And it told Thy love to me;
But I long to rise in the arms of faith
And be closer drawn to Thee.
Draw me nearer, nearer, blessed Lord,
To the cross where Thou hast died;
Draw me nearer, nearer, nearer, blessed Lord,
To Thy precious, bleeding side.

Consecrate me now to Thy service, Lord,
By the power of grace divine;
Let my soul look up with a steadfast hope,
And my will be lost in Thine.
Draw me nearer...

O the pure delight of a single hour
That before Thy throne I spend,
When I kneel in prayer, and with Thee, my God,
I commune as friend with friend!
Draw me nearer...""",
    ),
    H(
        "주 예수 나를 부르사",
        "Softly and Tenderly",
        "Will L. Thompson",
        "Will L. Thompson",
        "1880",
        "부르심",
        "윌 L. 톰슨(Will Lamartine Thompson, 1847–1909) 작사·작곡. "
        "부드러운 초대의 복음 찬송으로 유명합니다. PD.",
        """주 예수 나를 부르사 오라 하시네
죄 짐 진 자들아 다 오라 하시네
오라 하시네 오라 하시네
주 예수 나를 부르사 오라 하시네

시간이 흘러가고 인생 짧으니
오늘 주께 나오라 지체 말아라
오라 하시네 오라 하시네
주 예수 나를 부르사 오라 하시네

주께서 기다리사 문 열어 두셨네
자비로운 음성으로 부르시네
오라 하시네 오라 하시네
주 예수 나를 부르사 오라 하시네""",
        """Softly and tenderly Jesus is calling,
Calling for you and for me;
See, on the portals He's waiting and watching,
Watching for you and for me.
Come home, come home,
Ye who are weary, come home;
Earnestly, tenderly, Jesus is calling,
Calling, O sinner, come home!

Why should we tarry when Jesus is pleading,
Pleading for you and for me?
Why should we linger and heed not His mercies,
Mercies for you and for me?
Come home, come home...

O for the wonderful love He has promised,
Promised for you and for me!
Though we have sinned, He has mercy and pardon,
Pardon for you and for me.
Come home, come home...""",
    ),
    H(
        "영원한 안식",
        "Shall We Gather at the River",
        "Robert Lowry",
        "Robert Lowry",
        "1864",
        "소망",
        "로버트 로우리가 무더운 여름 오후 요한계시록의 생명수 강을 묵상하며 "
        "작사·작곡했다고 합니다. PD.",
        """주의 보좌 앞에 모인 성도들과 함께
생명수 강가에서 만나 보리
아름다운 그 강가 빛나는 그 곳에서
주의 보좌 앞에 모여 찬양하리

이른 아침 이슬 같고 맑은 수정 같으니
하나님 보좌에서 흘러나오네
아름다운 그 강가 빛나는 그 곳에서
주의 보좌 앞에 모여 찬양하리

곧 그날에 우리가 그곳에서 만나
영광의 면류관 받으리로다
아름다운 그 강가 빛나는 그 곳에서
주의 보좌 앞에 모여 찬양하리""",
        """Shall we gather at the river,
Where bright angel feet have trod,
With its crystal tide forever
Flowing by the throne of God?
Yes, we'll gather at the river,
The beautiful, the beautiful river;
Gather with the saints at the river
That flows by the throne of God.

On the margin of the river,
Washing up its silver spray,
We will walk and worship ever,
All the happy golden day.
Yes, we'll gather at the river...

Ere we reach the shining river,
Lay we every burden down;
Grace our spirits will deliver,
And provide a robe and crown.
Yes, we'll gather at the river...

Soon we'll reach the silver river,
Soon our pilgrimage will cease;
Soon our happy hearts will quiver
With the melody of peace.
Yes, we'll gather at the river...""",
    ),
    H(
        "주 하나님 지으신 기초",
        "How Firm a Foundation",
        "“K” in Rippon’s Selection",
        "Traditional (FOUNDATION)",
        "1787",
        "믿음",
        "존 리폰(John Rippon) 찬송집에 “K”라는 서명으로 실린 고전 찬송. "
        "이사야의 약속을 인용하며 성도의 견인을 노래합니다. PD.",
        """주 하나님 지으신 기초 얼마나 견고한가
주의 말씀 의지하는 자 흔들리지 않으리
주가 말씀하시기를 두려워 말라
내가 너와 함께 하리라

물불을 지나갈지라도 너를 지키리니
큰 물이 너를 침몰 못하며 불꽃이 해치 못하리
주가 말씀하시기를 두려워 말라
내가 너와 함께 하리라

연단의 풀무 가운데서도 내가 함께 하리니
금보다 귀하게 하리라 내 은혜로 살리라
주가 말씀하시기를 두려워 말라
내가 너와 함께 하리라""",
        """How firm a foundation, ye saints of the Lord,
Is laid for your faith in His excellent Word!
What more can He say than to you He hath said,
To you who for refuge to Jesus have fled?

"Fear not, I am with thee, O be not dismayed,
For I am thy God, and will still give thee aid;
I'll strengthen thee, help thee, and cause thee to stand,
Upheld by My righteous, omnipotent hand."

"When through the deep waters I call thee to go,
The rivers of sorrow shall not overflow;
For I will be with thee, thy troubles to bless,
And sanctify to thee thy deepest distress."

"The soul that on Jesus hath leaned for repose,
I will not, I will not desert to his foes;
That soul, though all hell should endeavor to shake,
I'll never, no, never, no, never forsake!" """,
    ),
    H(
        "부활하신 주",
        "Christ the Lord Is Risen Today",
        "Charles Wesley",
        "Traditional (EASTER HYMN)",
        "1739",
        "부활",
        "찰스 웨슬리(Charles Wesley, 1707–1788)의 부활절 찬송. "
        "“Alleluia” 후렴과 함께 전 세계 교회에서 부활주일에 불립니다. PD.",
        """예수 부활 했으니 할렐루야
만민 찬양하여라 할렐루야
천사들이 즐거이 할렐루야
기쁜 노래 부르네 할렐루야

사망 권세 이기고 할렐루야
부활하신 주 예수 할렐루야
우리가 살게 된 것 할렐루야
주의 부활 덕이라 할렐루야

천국 문이 열렸네 할렐루야
예수 따라 들어가 할렐루야
영광 중에 찬양해 할렐루야
부활 생명 얻었네 할렐루야""",
        """Christ the Lord is risen today, Alleluia!
Sons of men and angels say, Alleluia!
Raise your joys and triumphs high, Alleluia!
Sing, ye heavens, and earth reply, Alleluia!

Lives again our glorious King, Alleluia!
Where, O death, is now thy sting? Alleluia!
Once He died our souls to save, Alleluia!
Where thy victory, O grave? Alleluia!

Love's redeeming work is done, Alleluia!
Fought the fight, the battle won, Alleluia!
Death in vain forbids Him rise, Alleluia!
Christ has opened paradise, Alleluia!

Soar we now where Christ has led, Alleluia!
Following our exalted Head, Alleluia!
Made like Him, like Him we rise, Alleluia!
Ours the cross, the grave, the skies, Alleluia!""",
    ),
    H(
        "왕 되신 주 찬양하세",
        "Crown Him with Many Crowns",
        "Matthew Bridges / Godfrey Thring",
        "George J. Elvey (DIADEMATA)",
        "1851",
        "찬양",
        "매튜 브리지스(Matthew Bridges, 1851) 원작에 고드프리 스링이 후대 절을 더했습니다. "
        "조지 엘비의 DIADEMATA 선율로 불립니다. 본 앱은 고전 절(PD)을 수록합니다.",
        """왕 되신 주 찬양하세 면류관 드리세
어린 양 되신 주 예수 경배하여라
하늘의 천사 무리와 성도들 함께
존귀 영광 능력 지혜 찬송 돌리세

생명의 주 찬양하세 죽음을 이긴 주
부활의 첫 열매 되사 영생 주셨네
사망 권세 이기시고 보좌에 앉으사
만왕의 왕 만주의 주 다스리시네

사랑의 주 찬양하세 십자가 지신 주
가시 면류관 쓰시고 우리를 구했네
그 사랑 어찌 크신지 측량할 수 없네
영원토록 주를 찬양 노래하리라""",
        """Crown Him with many crowns,
The Lamb upon His throne;
Hark! how the heavenly anthem drowns
All music but its own.
Awake, my soul, and sing
Of Him who died for thee,
And hail Him as thy matchless King
Through all eternity.

Crown Him the Lord of life,
Who triumphed o'er the grave,
And rose victorious in the strife
For those He came to save.
His glories now we sing,
Who died, and rose on high,
Who died eternal life to bring,
And lives that death may die.

Crown Him the Lord of love;
Behold His hands and side,
Rich wounds, yet visible above,
In beauty glorified.
No angel in the sky
Can fully bear that sight,
But downward bends his wondering eye
At mysteries so bright.""",
    ),
    H(
        "주여 나의 생명",
        "Take My Life and Let It Be",
        "Frances R. Havergal",
        "Traditional (HENDON / MESSIAH)",
        "1874",
        "헌신",
        "프랜시스 리들리 해버갈(Frances Ridley Havergal, 1836–1879) 작사. "
        "전 인격적 헌신을 절마다 고백하는 고전 헌신 찬송입니다. PD.",
        """주여 나의 생명 드리오니
주의 뜻대로 사용하소서
나의 손과 발을 드리오니
주를 위해 쓰게 하소서

나의 음성 드려 찬양하고
주의 사랑 전파하리이다
나의 금과 은을 드리오니
주의 나라 위해 쓰소서

나의 뜻과 맘을 드리오니
주의 보좌 앞에 엎드리네
나의 사랑 모두 드리오니
주만 위해 살게 하소서""",
        """Take my life, and let it be
Consecrated, Lord, to Thee.
Take my moments and my days;
Let them flow in ceaseless praise.

Take my hands, and let them move
At the impulse of Thy love.
Take my feet, and let them be
Swift and beautiful for Thee.

Take my voice, and let me sing
Always, only, for my King.
Take my lips, and let them be
Filled with messages from Thee.

Take my silver and my gold;
Not a mite would I withhold.
Take my intellect, and use
Every power as Thou shalt choose.

Take my will, and make it Thine;
It shall be no longer mine.
Take my heart, it is Thine own;
It shall be Thy royal throne.

Take my love; my Lord, I pour
At Thy feet its treasure-store.
Take myself, and I will be
Ever, only, all for Thee.""",
    ),
    H(
        "갈 길 모르니",
        "Lead, Kindly Light",
        "John H. Newman",
        "John B. Dykes (LUX BENIGNA)",
        "1833",
        "인도",
        "존 헨리 뉴먼(John Henry Newman, 1801–1890)이 지중해 항해 중 병중에 지은 시. "
        "어둠 속 인도하심을 간구하는 고전 찬송입니다. PD.",
        """갈 길 모르니 주여 인도하소서
캄캄한 밤중 외로운 길에
멀리 비취는 빛 필요 없고
한 걸음만 비춰 주소서

교만했던 날 스스로 행하며
주를 멀리하고 방황했으나
이제 주 앞에 돌아오오니
갈 길 인도하여 주소서

아침에 이를 때까지 지키사
천사와 함께 기쁨 누리며
영원히 주의 얼굴 뵙기를
갈망하며 나아가리다""",
        """Lead, kindly Light, amid th'encircling gloom,
Lead Thou me on!
The night is dark, and I am far from home;
Lead Thou me on!
Keep Thou my feet; I do not ask to see
The distant scene; one step enough for me.

I was not ever thus, nor prayed that Thou
Shouldst lead me on;
I loved to choose and see my path; but now
Lead Thou me on!
I loved the garish day, and, spite of fears,
Pride ruled my will. Remember not past years!

So long Thy power hath blest me, sure it still
Will lead me on
O'er moor and fen, o'er crag and torrent, till
The night is gone,
And with the morn those angel faces smile,
Which I have loved long since, and lost awhile!""",
    ),
    H(
        "주 나를 구원하셨네",
        "He Leadeth Me",
        "Joseph H. Gilmore",
        "William B. Bradbury",
        "1862",
        "인도",
        "조셉 길모어(Joseph H. Gilmore)가 시편 23편을 설교한 뒤 적은 시. "
        "브래드버리가 곡을 붙였습니다. PD.",
        """주 나를 인도하시니 목자 되신 주
푸른 초장 쉴 만한 물가로 인도하시네
주가 나를 인도하시니 무엇을 두려워하리
주의 손 붙들고 가리 영원히

어두운 골짜기에서도 주가 함께 하사
주의 지팡이 막대기로 나를 안위하시네
주가 나를 인도하시니 무엇을 두려워하리
주의 손 붙들고 가리 영원히

원수 앞에서 상을 베푸시고
내 잔이 넘치게 하시니 감사하리
주가 나를 인도하시니 무엇을 두려워하리
주의 손 붙들고 가리 영원히""",
        """He leadeth me: O blessed thought!
O words with heavenly comfort fraught!
Whate'er I do, where'er I be,
Still 'tis God's hand that leadeth me.
He leadeth me, He leadeth me;
By His own hand He leadeth me:
His faithful follower I would be,
For by His hand He leadeth me.

Sometimes mid scenes of deepest gloom,
Sometimes where Eden's flowers bloom,
By waters calm, o'er troubled sea,
Still 'tis His hand that leadeth me.
He leadeth me...

Lord, I would clasp Thy hand in mine,
Nor ever murmur nor repine;
Content, whatever lot I see,
Since 'tis my God that leadeth me.
He leadeth me...

And when my task on earth is done,
When, by Thy grace, the victory's won,
E'en death's cold wave I will not flee,
Since God through Jordan leadeth me.
He leadeth me...""",
    ),
    H(
        "복음의 기쁜 소식",
        "O Happy Day",
        "Philip Doddridge",
        "Edward F. Rimbault (arr.)",
        "1755",
        "기쁨",
        "필립 도드리지(Philip Doddridge, 1702–1751) 작사. "
        "회심과 서약의 기쁨을 노래하는 고전 찬송입니다. PD.",
        """복음의 기쁜 소식 내게 임하니
내 영혼 즐거워 춤추며 노래해
오 행복한 날 예수 나의 주
내 모든 죄 사하시고 날 구원했네

주와 언약 맺고 주를 따르리
세상 끝날까지 신실하리라
오 행복한 날 예수 나의 주
내 모든 죄 사하시고 날 구원했네

하늘 소망 품고 주를 찬양해
영원한 생명 주께 받았네
오 행복한 날 예수 나의 주
내 모든 죄 사하시고 날 구원했네""",
        """O happy day, that fixed my choice
On Thee, my Savior and my God!
Well may this glowing heart rejoice,
And tell its raptures all abroad.
Happy day, happy day,
When Jesus washed my sins away!
He taught me how to watch and pray,
And live rejoicing every day.
Happy day, happy day,
When Jesus washed my sins away!

'Tis done: the great transaction's done!
I am the Lord's and He is mine;
He drew me and I followed on,
Charmed to confess the voice divine.
Happy day, happy day...

Now rest, my long-divided heart,
Fixed on this blissful center, rest.
Here have I found a nobler part;
Here heavenly pleasures fill my breast.
Happy day, happy day...""",
    ),
    H(
        "주 예수 영광",
        "To God Be the Glory",
        "Fanny J. Crosby",
        "William H. Doane",
        "1875",
        "찬양",
        "패니 크로즈비·W. H. 도안의 대표 찬양 찬송. "
        "20세기 중반 빌리 그레이엄 집회 등을 통해 다시 크게 부흥했습니다. 원곡 PD.",
        """주 하나님 찬양하세 그 크신 영광
독생자 주 예수 우리를 구했네
죄인 위해 피 흘려 대속하셨네
그 사랑 놀라우니 찬양하세
찬양하세 찬양하세 천사여 찬양
찬양하세 찬양하세 영광의 왕께

완전한 속죄 이미 이루셨고
믿는 자마다 영생 얻으리
주 약속 확실하니 의심 말아라
그 사랑 놀라우니 찬양하세
찬양하세 찬양하세 천사여 찬양
찬양하세 찬양하세 영광의 왕께

큰 기쁨으로 주 앞에 나아가
주 얼굴 뵙고 경배하리라
그 크신 사랑 영원히 노래해
그 사랑 놀라우니 찬양하세
찬양하세 찬양하세 천사여 찬양
찬양하세 찬양하세 영광의 왕께""",
        """To God be the glory, great things He hath done;
So loved He the world that He gave us His Son,
Who yielded His life an atonement for sin,
And opened the lifegate that all may go in.
Praise the Lord, praise the Lord,
Let the earth hear His voice!
Praise the Lord, praise the Lord,
Let the people rejoice!
O come to the Father, through Jesus the Son,
And give Him the glory, great things He hath done.

O perfect redemption, the purchase of blood,
To every believer the promise of God;
The vilest offender who truly believes,
That moment from Jesus a pardon receives.
Praise the Lord...

Great things He hath taught us, great things He hath done,
And great our rejoicing through Jesus the Son;
But purer, and higher, and greater will be
Our wonder, our transport, when Jesus we see.
Praise the Lord...""",
    ),
    H(
        "주 앞에 나와",
        "Come, Ye Sinners, Poor and Needy",
        "Joseph Hart",
        "Traditional (RESTORATION / BEACH SPRING)",
        "1759",
        "부르심",
        "조셉 하트(Joseph Hart, 1712–1768) 작사. "
        "죄인을 그리스도께로 초대하는 복음주의 찬송의 고전입니다. PD.",
        """죄 많은 자들아 주 앞에 나오라
가난하고 병든 자 다 나오라
주 예수 기다리사 영접하시리
지체 말고 나오라 주께로

수고하고 짐 진 자 다 나오라
주가 안식 주시리 믿으라
주 예수 기다리사 영접하시리
지체 말고 나오라 주께로

오늘이 구원의 날 기회니
내일로 미루지 말아라
주 예수 기다리사 영접하시리
지체 말고 나오라 주께로""",
        """Come, ye sinners, poor and needy,
Weak and wounded, sick and sore;
Jesus ready stands to save you,
Full of pity, love, and power.
I will arise and go to Jesus;
He will embrace me in His arms;
In the arms of my dear Savior,
O there are ten thousand charms.

Come, ye thirsty, come, and welcome,
God's free bounty glorify;
True belief and true repentance,
Every grace that brings you nigh.
I will arise and go to Jesus...

Come, ye weary, heavy laden,
Lost and ruined by the fall;
If you tarry till you're better,
You will never come at all.
I will arise and go to Jesus...

Let not conscience make you linger,
Nor of fitness fondly dream;
All the fitness He requireth
Is to feel your need of Him.
I will arise and go to Jesus...""",
    ),
    H(
        "나 주를 찬양하리",
        "I Will Praise Him",
        "Margaret J. Harris",
        "Margaret J. Harris",
        "1898",
        "찬양",
        "마거릿 J. 해리스 작사·작곡(1898). 미국 기준 고전 복음 찬송으로 Public Domain입니다.",
        """나 주를 찬양하리 그 크신 은혜
내 죄를 사하시고 새 생명 주셨네
찬양하리 찬양하리 나의 구주 예수
보혈로 정결케 하사 나를 구원했네

어둠에 있던 나를 빛으로 인도
절망 중에 소망을 주셨네
찬양하리 찬양하리 나의 구주 예수
보혈로 정결케 하사 나를 구원했네

영원토록 찬양하리 구원의 주님
하늘에서 영원히 노래하리
찬양하리 찬양하리 나의 구주 예수
보혈로 정결케 하사 나를 구원했네""",
        """When I saw the cleansing fountain
Open wide for all my sin,
I obeyed the Spirit's wooing,
When He said, Wilt thou be clean?
I will praise Him! I will praise Him!
Praise the Lamb for sinners slain;
Give Him glory, all ye people,
For His blood can wash away each stain.

Though the way seems straight and narrow,
All I claimed was swept away;
My ambitions, plans and wishes,
At my feet in ashes lay.
I will praise Him...

Blessed be the name of Jesus!
I'm so glad He took me in;
He's forgiven my transgressions,
He has cleansed my heart from sin.
I will praise Him...""",
    ),
    H(
        "주님 약속하신 말씀 위에서",
        "Standing on the Promises",
        "R. Kelso Carter",
        "R. Kelso Carter",
        "1886",
        "믿음",
        "러셀 켈소 카터(R. Kelso Carter, 1849–1928) 작사·작곡. "
        "하나님의 약속을 굳게 붙드는 믿음의 찬송입니다. PD.",
        """주님 약속하신 말씀 위에 서리
주의 말씀 굳건하여 흔들리지 않네
서서 서리 서서 서리
주의 약속 위에 굳게 서리

시험이 몰려와도 두려워 않고
주의 말씀 붙들고서 이기리라
서서 서리 서서 서리
주의 약속 위에 굳게 서리

영광의 그날까지 신실하리니
주의 약속 성취됨을 보리로다
서서 서리 서서 서리
주의 약속 위에 굳게 서리""",
        """Standing on the promises of Christ my King,
Through eternal ages let His praises ring,
Glory in the highest, I will shout and sing,
Standing on the promises of God.
Standing, standing,
Standing on the promises of God my Savior;
Standing, standing,
I'm standing on the promises of God.

Standing on the promises that cannot fail,
When the howling storms of doubt and fear assail,
By the living Word of God I shall prevail,
Standing on the promises of God.
Standing, standing...

Standing on the promises I now can see
Perfect, present cleansing in the blood for me;
Standing in the liberty where Christ makes free,
Standing on the promises of God.
Standing, standing...""",
    ),
    H(
        "나 같은 죄인 살리신",
        "Alas! and Did My Savior Bleed",
        "Isaac Watts",
        "Hugh Wilson (MARTYRDOM) / Traditional",
        "1707",
        "수난",
        "아이작 와츠 작사. 미국에서는 “At the Cross” 후렴(Ralph E. Hudson, 1885)과 "
        "함께 불리기도 하며, 본 텍스트(1707)는 Public Domain입니다.",
        """나 같은 죄인 살리신 주 은혜 놀라워
잃었던 생명 찾았고 광명을 얻었네
십자가 밑에 엎드려 눈물로 회개해
주 예수 피 흘리신 그 사랑 감사해

주께서 나를 위해 죽으셨으니
내 생명 드려 주를 따르리
십자가 밑에 엎드려 눈물로 회개해
주 예수 피 흘리신 그 사랑 감사해

이 세상 자랑 버리고 주만 의지하리
십자가 은혜 아니면 소망 없으리
십자가 밑에 엎드려 눈물로 회개해
주 예수 피 흘리신 그 사랑 감사해""",
        """Alas! and did my Savior bleed,
And did my Sovereign die?
Would He devote that sacred head
For such a worm as I?

Was it for crimes that I had done
He groaned upon the tree?
Amazing pity! grace unknown!
And love beyond degree!

Well might the sun in darkness hide,
And shut his glories in,
When Christ, the mighty Maker, died
For man, the creature's sin.

But drops of grief can ne'er repay
The debt of love I owe;
Here, Lord, I give myself away,
'Tis all that I can do.""",
    ),
    H(
        "할렐루야 우리 구주",
        "Hallelujah! What a Savior",
        "Philip P. Bliss",
        "Philip P. Bliss",
        "1875",
        "복음",
        "필립 블리스(P. P. Bliss, 1838–1876) 작사·작곡. "
        "이사야 53장의 고난 받는 종을 묵상한 복음 찬송입니다. PD.",
        """죄인 위해 고난 받은 하나님의 어린 양
거룩하신 주 예수 할렐루야 구주시라
할렐루야 할렐루야 할렐루야 구주시라

멸시받고 거절당한 우리의 질고 지셨네
하나님이 버리신 듯 할렐루야 구주시라
할렐루야 할렐루야 할렐루야 구주시라

다 이루었다 외치신 구원 사역 완성했네
하늘 보좌 오르신 주 할렐루야 구주시라
할렐루야 할렐루야 할렐루야 구주시라""",
        """"Man of Sorrows!" what a name
For the Son of God, who came
Ruined sinners to reclaim.
Hallelujah! What a Savior!

Bearing shame and scoffing rude,
In my place condemned He stood;
Sealed my pardon with His blood.
Hallelujah! What a Savior!

Guilty, vile, and helpless we;
Spotless Lamb of God was He;
"Full atonement!" can it be?
Hallelujah! What a Savior!

Lifted up was He to die;
"It is finished!" was His cry;
Now in heaven exalted high.
Hallelujah! What a Savior!

When He comes, our glorious King,
All His ransomed home to bring,
Then anew this song we'll sing:
Hallelujah! What a Savior!""",
    ),
    H(
        "예수 피를 힘입어",
        "There Is Power in the Blood",
        "Lewis E. Jones",
        "Lewis E. Jones",
        "1899",
        "복음",
        "루이스 E. 존스(Lewis E. Jones, 1865–1936) 작사·작곡(1899). "
        "미국 기준 Public Domain 복음 찬송입니다.",
        """죄에서 자유를 얻게 함은
보혈의 능력 주의 보혈
최후의 승리를 얻게 함은
보혈의 능력 주의 피
주의 보혈 능력 있도다
주의 피 믿으오
주의 보혈 그 어린 양의
매우 귀중한 피로다

육체의 정욕을 이기려면
보혈의 능력 주의 보혈
세상의 유혹을 이기려면
보혈의 능력 주의 피
주의 보혈 능력 있도다
주의 피 믿으오
주의 보혈 그 어린 양의
매우 귀중한 피로다

무한한 능력이 그 피로다
보혈의 능력 주의 보혈
우리의 죄를 씻으시네
보혈의 능력 주의 피
주의 보혈 능력 있도다
주의 피 믿으오
주의 보혈 그 어린 양의
매우 귀중한 피로다""",
        """Would you be free from the burden of sin?
There's power in the blood, power in the blood;
Would you o'er evil a victory win?
There's wonderful power in the blood.
There is power, power, wonder-working power
In the blood of the Lamb;
There is power, power, wonder-working power
In the precious blood of the Lamb.

Would you be free from your passion and pride?
There's power in the blood, power in the blood;
Come for a cleansing to Calvary's tide;
There's wonderful power in the blood.
There is power, power...

Would you do service for Jesus your King?
There's power in the blood, power in the blood;
Would you live daily His praises to sing?
There's wonderful power in the blood.
There is power, power...""",
    ),
    H(
        "내게 있는 모든 것을",
        "I Surrender All",
        "Judson W. Van DeVenter",
        "Winfield S. Weeden",
        "1896",
        "헌신",
        "저드슨 반 드벤터(Judson W. Van DeVenter, 1855–1939) 작사, "
        "윈필드 위든 작곡. 전적 헌신의 복음 찬송입니다. PD(USA).",
        """내게 있는 모든 것 아낌없이 드리네
이제 모두 주께 바치오니 받아 주소서
모두 드리네 모두 드리네
세상과 나 주님께 모두 드리네

자랑하던 모든 것 주님의 발 앞에
내려놓고 빈손 들고서 나가오니
모두 드리네 모두 드리네
세상과 나 주님께 모두 드리네

사랑하던 모든 것 주의 뜻에 맡기고
오직 주만 따르겠나이다 받아 주소서
모두 드리네 모두 드리네
세상과 나 주님께 모두 드리네""",
        """All to Jesus I surrender,
All to Him I freely give;
I will ever love and trust Him,
In His presence daily live.
I surrender all, I surrender all,
All to Thee, my blessed Savior,
I surrender all.

All to Jesus I surrender,
Humbly at His feet I bow,
Worldly pleasures all forsaken,
Take me, Jesus, take me now.
I surrender all...

All to Jesus I surrender,
Make me, Savior, wholly Thine;
Let me feel the Holy Spirit,
Truly know that Thou art mine.
I surrender all...

All to Jesus I surrender,
Lord, I give myself to Thee;
Fill me with Thy love and power,
Let Thy blessing fall on me.
I surrender all...""",
    ),
    H(
        "나 주의 도움 받고자",
        "I Need Thee Every Hour",
        "Annie S. Hawks",
        "Robert Lowry",
        "1872",
        "기도",
        "애니 S. 호크스(Annie S. Hawks) 작사, 로버트 로우리 작곡·후렴. "
        "일상 속 주님 필요를 고백하는 기도 찬송입니다. PD.",
        """나 주의 도움 받고자 주께 기도합니다
매 시간 주가 필요해 주여 함께 하소서
매 시간 내가 주 필요해
오 복되신 주 나와 함께 하소서

평안할 때나 괴로울 때 주가 필요해
시험이 나를 에워싸도 주여 함께 하소서
매 시간 내가 주 필요해
오 복되신 주 나와 함께 하소서

내 기쁨의 근원 되신 주 떠나지 마소서
영원한 생명 주시니 주여 함께 하소서
매 시간 내가 주 필요해
오 복되신 주 나와 함께 하소서""",
        """I need Thee every hour, most gracious Lord;
No tender voice like Thine can peace afford.
I need Thee, O I need Thee;
Every hour I need Thee;
O bless me now, my Savior,
I come to Thee.

I need Thee every hour, stay Thou nearby;
Temptations lose their power when Thou art nigh.
I need Thee, O I need Thee...

I need Thee every hour, in joy or pain;
Come quickly and abide, or life is vain.
I need Thee, O I need Thee...

I need Thee every hour; teach me Thy will;
And Thy rich promises in me fulfill.
I need Thee, O I need Thee...""",
    ),
    H(
        "주 예수 나의 모든 것",
        "Jesus Is All the World to Me",
        "Will L. Thompson",
        "Will L. Thompson",
        "1904",
        "사랑",
        "윌 L. 톰슨 작사·작곡(1904). 미국 기준 Public Domain입니다.",
        """주 예수 나의 모든 것 생명과 소망
환난 중에 친구 되사 나를 위로해
예수 예수 나의 기쁨
예수 예수 나의 노래
예수 예수 나의 모든 것
영원히 찬양하리

주 예수 나의 모든 것 밝은 빛 되사
어두운 길 비춰 주사 인도하시네
예수 예수 나의 기쁨
예수 예수 나의 노래
예수 예수 나의 모든 것
영원히 찬양하리

주 예수 나의 모든 것 생명 주시네
세상 끝날 함께 하사 영생 주리라
예수 예수 나의 기쁨
예수 예수 나의 노래
예수 예수 나의 모든 것
영원히 찬양하리""",
        """Jesus is all the world to me,
My life, my joy, my all;
He is my strength from day to day,
Without Him I would fall.
When I am sad, to Him I go,
No other one can cheer me so;
When I am sad, He makes me glad,
He's my friend.

Jesus is all the world to me,
My friend in trials sore;
I go to Him for blessings, and
He gives them o'er and o'er.
He sends the sunshine and the rain,
He sends the harvest's golden grain;
Sunshine and rain, harvest of grain,
He's my friend.

Jesus is all the world to me,
I want no better friend;
I trust Him now, I'll trust Him when
Life's fleeting days shall end.
Beautiful life with such a friend,
Beautiful life that has no end;
Eternal life, eternal joy,
He's my friend.""",
    ),
    H(
        "주의 친절한 팔에 안기세",
        "Safe in the Arms of Jesus",
        "Fanny J. Crosby",
        "William H. Doane",
        "1868",
        "위로",
        "패니 크로즈비·W. H. 도안. 위로와 안식의 고전 복음 찬송입니다. PD.",
        """주의 친절한 팔에 안기세
나의 쉴 곳은 주의 팔이라
주의 팔에 안기세 주의 팔에
험한 세파 지나 안식하리

주의 품에 안기어 쉬며
세상 근심 모두 잊으리
주의 팔에 안기세 주의 팔에
험한 세파 지나 안식하리

영광의 나라 이를 때까지
주의 팔에 안전하게 쉬리
주의 팔에 안기세 주의 팔에
험한 세파 지나 안식하리""",
        """Safe in the arms of Jesus,
Safe on His gentle breast,
There by His love o'ershaded,
Sweetly my soul shall rest.
Hark! 'tis the voice of angels,
Borne in a song to me.
Over the fields of glory,
Over the jasper sea.
Safe in the arms of Jesus,
Safe on His gentle breast,
There by His love o'ershaded,
Sweetly my soul shall rest.

Safe in the arms of Jesus,
Safe from corroding care,
Safe from the world's temptations,
Sin cannot harm me there.
Free from the blight of sorrow,
Free from my doubts and fears;
Only a few more trials,
Only a few more tears!
Safe in the arms of Jesus...

Jesus, my heart's dear Refuge,
Jesus has died for me;
Firm on the Rock of Ages,
Ever my trust shall be.
Here let me wait with patience,
Wait till the night is o'er;
Wait till I see the morning
Break on the golden shore.
Safe in the arms of Jesus...""",
    ),
    H(
        "주 품에 품으소서",
        "Pass Me Not, O Gentle Savior",
        "Fanny J. Crosby",
        "William H. Doane",
        "1868",
        "기도",
        "패니 크로즈비 작사. 구원의 은혜를 간구하는 간절한 기도 찬송입니다. PD.",
        """주여 나를 돌아보사 은혜 베푸소서
죄인 중에 나를 버려 두지 마소서
구주 예수 구주 예수 들으시옵소서
죄인 중에 나를 버려 두지 마소서

나의 기도 들으시고 응답하소서
근심 중에 부르짖는 나를 도우소서
구주 예수 구주 예수 들으시옵소서
죄인 중에 나를 버려 두지 마소서

주의 보혈 의지하고 나가오니
정결케 하사 영접하여 주소서
구주 예수 구주 예수 들으시옵소서
죄인 중에 나를 버려 두지 마소서""",
        """Pass me not, O gentle Savior,
Hear my humble cry;
While on others Thou art calling,
Do not pass me by.
Savior, Savior,
Hear my humble cry;
While on others Thou art calling,
Do not pass me by.

Let me at Thy throne of mercy
Find a sweet relief;
Kneeling there in deep contrition,
Help my unbelief.
Savior, Savior...

Trusting only in Thy merit,
Would I seek Thy face;
Heal my wounded, broken spirit,
Save me by Thy grace.
Savior, Savior...

Thou the Spring of all my comfort,
More than life to me,
Whom have I on earth beside Thee?
Whom in heaven but Thee?
Savior, Savior...""",
    ),
    H(
        "주 예수 넓은 사랑",
        "There Is a Wideness in God's Mercy",
        "Frederick W. Faber",
        "Traditional / Lizzie S. Tourjée (WELLESLEY)",
        "1862",
        "은혜",
        "프레더릭 윌리엄 페이버(Frederick W. Faber, 1814–1863) 작사. "
        "하나님의 넓고 깊은 자비를 노래합니다. PD.",
        """주 예수 넓은 사랑 바다보다 넓고
하늘보다 높으며 측량할 수 없네
우리 생각 미치지 못할 그 은혜
죄인 위해 베푸신 사랑이로다

사람의 마음보다 주의 마음 넓어
용서하지 못할 죄 없다 하시네
원수 같던 우리도 품어 주시니
그 사랑 놀라워라 찬양하리라

의심하지 말아라 주의 자비를
오늘도 열려 있는 은혜의 문
믿음으로 나아가 영접 받으라
주 예수 넓은 사랑 영원하리라""",
        """There is a wideness in God's mercy,
Like the wideness of the sea;
There's a kindness in His justice,
Which is more than liberty.

There is welcome for the sinner,
And more graces for the good;
There is mercy with the Savior;
There is healing in His blood.

For the love of God is broader
Than the measure of our mind;
And the heart of the Eternal
Is most wonderfully kind.

If our love were but more simple,
We should take Him at His word;
And our lives would be all sunshine
In the sweetness of our Lord.""",
    ),
    H(
        "주의 말씀 듣고서",
        "Break Thou the Bread of Life",
        "Mary A. Lathbury",
        "William F. Sherwin",
        "1877",
        "말씀",
        "메리 A. 래스버리(Mary A. Lathbury) 작사. "
        "성경을 생명의 떡으로 구하는 말씀 찬송입니다. PD.",
        """주의 말씀 듣고서 깨달아 알고
생명의 떡 내게 주시옵소서
진리의 말씀으로 나를 먹이사
영혼이 살게 하옵소서

주여 진리 가르치사 인도하시고
어두운 길 밝혀 주옵소서
주의 얼굴 뵙도록 나를 이끄사
영원 생명 얻게 하소서

오병이어의 기적 같이 지금
내 영혼 배불리 먹이소서
생명의 떡 되신 주 영접하오니
주여 함께 하옵소서""",
        """Break Thou the bread of life, dear Lord, to me,
As Thou didst break the loaves beside the sea;
Beyond the sacred page I seek Thee, Lord;
My spirit pants for Thee, O living Word!

Bless Thou the truth, dear Lord, to me, to me,
As Thou didst bless the bread by Galilee;
Then shall all bondage cease, all fetters fall;
And I shall find my peace, my all in all.

Thou art the bread of life, O Lord, to me,
Thy holy Word the truth that saveth me;
Give me to eat and live with Thee above;
Teach me to love Thy truth, for Thou art love.""",
    ),
    H(
        "빛나는 아침 해",
        "When Morning Gilds the Skies",
        "Traditional German / tr. Edward Caswall",
        "Joseph Barnby (LAUDES DOMINI)",
        "1828",
        "찬양",
        "19세기 독일 찬송을 에드워드 캐스월(Edward Caswall) 등이 영어로 옮겼고, "
        "조셉 반비의 LAUDES DOMINI 선율로 널리 불립니다. PD.",
        """빛나는 아침 해 하늘 높이 떠올라
온 세상 비출 때 주 이름 찬양해
내 영혼아 주 찬양 주 이름 찬양해

한낮의 더위 중에도 주를 찬양하고
저녁 노을 질 때도 주 이름 찬양해
내 영혼아 주 찬양 주 이름 찬양해

밤에 잠들 때까지 주를 찬양하며
천사들과 함께 주 이름 찬양해
내 영혼아 주 찬양 주 이름 찬양해""",
        """When morning gilds the skies,
My heart awaking cries,
May Jesus Christ be praised!
Alike at work and prayer,
To Jesus I repair;
May Jesus Christ be praised!

Does sadness fill my mind?
A solace here I find,
May Jesus Christ be praised!
Or fades my earthly bliss?
My comfort still is this,
May Jesus Christ be praised!

The night becomes as day
When from the heart we say:
May Jesus Christ be praised!
The powers of darkness fear
When this sweet chant they hear:
May Jesus Christ be praised!

Be this, while life is mine,
My canticle divine:
May Jesus Christ be praised!
Be this th'eternal song
Through all the ages long:
May Jesus Christ be praised!""",
    ),
    H(
        "주 성령의 감화로",
        "Breathe on Me, Breath of God",
        "Edwin Hatch",
        "Robert Jackson (TRENTHAM)",
        "1878",
        "성령",
        "에드윈 해치(Edwin Hatch, 1835–1889) 작사. "
        "성령의 생기를 구하는 짧은 고전 성령 찬송입니다. PD.",
        """주 성령의 감화로 나를 채우소서
새 생명 주옵시고 정결케 하소서

주 성령의 감화로 나를 불사르사
죄악을 태우시고 거룩케 하소서

주 성령의 감화로 나를 주장하사
주의 뜻 행하도록 인도하소서

주 성령의 감화로 나와 하나 되사
영원토록 주 안에 살게 하소서""",
        """Breathe on me, Breath of God,
Fill me with life anew,
That I may love what Thou dost love,
And do what Thou wouldst do.

Breathe on me, Breath of God,
Until my heart is pure,
Until with Thee I will one will,
To do and to endure.

Breathe on me, Breath of God,
Till I am wholly Thine,
Until this earthly part of me
Glows with Thy fire divine.

Breathe on me, Breath of God,
So shall I never die,
But live with Thee the perfect life
Of Thine eternity.""",
    ),
    H(
        "성령이여 오소서",
        "Spirit of God, Descend upon My Heart",
        "George Croly",
        "Frederick C. Atkinson (MORECAMBE)",
        "1854",
        "성령",
        "조지 크롤리(George Croly, 1780–1860) 작사. "
        "성령의 임재와 가르침을 구하는 깊은 기도 찬송입니다. PD.",
        """성령이여 내 맘에 강림하소서
세상의 헛된 것 끊게 하소서
오직 주만 바라보고 따르게 하사
성령으로 충만케 하소서

성령이여 가르치사 깨닫게 하소서
십자가 사랑 깊이 알게 하소서
내 뜻을 주의 뜻에 맡기게 하사
성령으로 충만케 하소서

성령이여 내 맘을 주장하소서
사랑과 기쁨 평안 넘치게 하소서
영원토록 주와 함께 살게 하사
성령으로 충만케 하소서""",
        """Spirit of God, descend upon my heart;
Wean it from earth; through all its pulses move;
Stoop to my weakness, mighty as Thou art,
And make me love Thee as I ought to love.

I ask no dream, no prophet ecstasies,
No sudden rending of the veil of clay,
No angel visitant, no opening skies;
But take the dimness of my soul away.

Teach me to feel that Thou art always nigh;
Teach me the struggles of the soul to bear,
To check the rising doubt, the rebel sigh;
Teach me the patience of unanswered prayer.

Teach me to love Thee as Thine angels love,
One holy passion filling all my frame;
The kindling of the heaven-descended Dove,
My heart an altar, and Thy love the flame.""",
    ),
    H(
        "주 안에서 하나 되세",
        "Blest Be the Tie That Binds",
        "John Fawcett",
        "Hans G. Nägeli / Lowell Mason",
        "1782",
        "교제",
        "존 포셋(John Fawcett, 1740–1817)이 목회지를 떠나려다 성도들과의 정을 느껴 "
        "남기로 결심하며 지었다고 전해집니다. PD.",
        """주 안에서 하나 된 우리
사랑의 줄로 매였네
이 사랑이 우리를 묶어
한 마음 되게 하네

우리가 아픔을 함께하며
서로의 짐을 나누네
서로의 아픔 위로하고
기쁨도 함께 하네

잠시 헤어질지라도
다시 만날 소망 있네
천국에서 영원히 함께
주를 찬양하리라""",
        """Blest be the tie that binds
Our hearts in Christian love;
The fellowship of kindred minds
Is like to that above.

Before our Father's throne
We pour our ardent prayers;
Our fears, our hopes, our aims are one,
Our comforts and our cares.

We share our mutual woes,
Our mutual burdens bear;
And often for each other flows
The sympathizing tear.

When we asunder part,
It gives us inward pain;
But we shall still be joined in heart,
And hope to meet again.""",
    ),
    H(
        "주의 음성을 내가 들으니",
        "I Heard the Voice of Jesus Say",
        "Horatius Bonar",
        "Traditional / John B. Dykes (VOX DILECTI)",
        "1846",
        "부르심",
        "호라티우스 보나(Horatius Bonar, 1808–1889) 작사. "
        "예수님의 초대를 듣고 안식·빛·생명을 얻는 여정을 그립니다. PD.",
        """주의 음성을 내가 들으니 나와 함께 쉬라 하시네
수고하고 짐 진 자들아 다 내게로 오라
내가 가서 쉬며 안식을 얻었네
주의 음성 따라가리

주의 음성을 내가 들으니 목마른 자 오라 하시네
생명수를 마시라 하시니 목마름 없으리
내가 가서 마시고 만족을 얻었네
주의 음성 따라가리

주의 음성을 내가 들으니 나는 세상의 빛이라
어두움에 행치 않게 하리 빛을 따르라
내가 가서 빛 가운데 행하리
주의 음성 따라가리""",
        """I heard the voice of Jesus say,
"Come unto Me and rest;
Lay down, thou weary one, lay down
Thy head upon My breast."
I came to Jesus as I was,
Weary and worn and sad;
I found in Him a resting place,
And He has made me glad.

I heard the voice of Jesus say,
"Behold, I freely give
The living water; thirsty one,
Stoop down, and drink, and live."
I came to Jesus, and I drank
Of that life-giving stream;
My thirst was quenched, my soul revived,
And now I live in Him.

I heard the voice of Jesus say,
"I am this dark world's Light;
Look unto Me, thy morn shall rise,
And all thy day be bright."
I looked to Jesus, and I found
In Him my Star, my Sun;
And in that light of life I'll walk,
Till traveling days are done.""",
    ),
    H(
        "주 나의 등대",
        "Jesus, Savior, Pilot Me",
        "Edward Hopper",
        "John E. Gould",
        "1871",
        "인도",
        "에드워드 호퍼(Edward Hopper) 목사가 뱃사람들을 생각하며 지은 찬송. "
        "인생 항해의 선장 되신 주님을 구합니다. PD.",
        """주 예수 나의 등대 되사 바다 길을 인도하소서
거친 풍랑 일 때에도 나를 지켜 주소서
주여 나를 인도하사 안전한 곳 이끄소서

암초와 폭풍 가운데 홀로 갈 수 없사오니
주의 손길 붙들고서 평안히 가리다
주여 나를 인도하사 안전한 곳 이끄소서

인생의 항해 끝날에 천국 항구 이를 때에
주의 얼굴 뵙겠나니 감사 찬양하리
주여 나를 인도하사 안전한 곳 이끄소서""",
        """Jesus, Savior, pilot me
Over life's tempestuous sea;
Unknown waves before me roll,
Hiding rock and treacherous shoal.
Chart and compass come from Thee;
Jesus, Savior, pilot me.

As a mother stills her child,
Thou canst hush the ocean wild;
Boisterous waves obey Thy will,
When Thou sayest to them, "Be still!"
Wondrous Sovereign of the sea,
Jesus, Savior, pilot me.

When at last I near the shore,
And the fearful breakers roar
'Twixt me and the peaceful rest,
Then, while leaning on Thy breast,
May I hear Thee say to me,
"Fear not, I will pilot thee." """,
    ),
    H(
        "주 예수 나의 구주",
        "My Jesus, I Love Thee",
        "William R. Featherston",
        "Adoniram J. Gordon",
        "1864",
        "사랑",
        "캐나다의 윌리엄 페더스톤(William Ralph Featherston)이 십대에 썼다고 전해지는 시. "
        "아도니람 고든이 곡을 붙였습니다. PD.",
        """주 예수 나의 구주 내가 사랑해
내 생명 모두 드려 주를 사랑해
주 나를 사랑하사 피 흘리셨네
주 예수 나의 구주 내가 사랑해

이 세상 부귀영화 다 버려도
주 사랑 비교할 수 없네
십자가 바라보며 주를 사랑해
주 예수 나의 구주 내가 사랑해

천국에 이를 때에 면류관 받고
영광 중에 주를 찬양하리
영원히 주를 사랑 노래하리라
주 예수 나의 구주 내가 사랑해""",
        """My Jesus, I love Thee, I know Thou art mine;
For Thee all the follies of sin I resign.
My gracious Redeemer, my Savior art Thou;
If ever I loved Thee, my Jesus, 'tis now.

I love Thee because Thou has first loved me,
And purchased my pardon on Calvary's tree.
I love Thee for wearing the thorns on Thy brow;
If ever I loved Thee, my Jesus, 'tis now.

I'll love Thee in life, I will love Thee in death,
And praise Thee as long as Thou lendest me breath;
And say when the death dew lies cold on my brow,
If ever I loved Thee, my Jesus, 'tis now.

In mansions of glory and endless delight,
I'll ever adore Thee in heaven so bright;
I'll sing with the glittering crown on my brow;
If ever I loved Thee, my Jesus, 'tis now.""",
    ),
    H(
        "믿음으로 살리",
        "Faith of Our Fathers",
        "Frederick W. Faber",
        "Henri F. Hemy / James G. Walton (ST. CATHERINE)",
        "1849",
        "믿음",
        "프레더릭 W. 페이버 작사. 선조들의 신앙을 이어 가겠다는 고백의 찬송입니다. PD.",
        """믿음의 선진들 그 귀한 믿음
옥중과 환난 중에도 지키었네
믿음으로 살리 거룩한 믿음
주의 진리 위해 살리라

우리 조상들의 믿음 따라
복음 위해 고난도 받으리
믿음으로 살리 거룩한 믿음
주의 진리 위해 살리라

온 세상 가득히 믿음의 불길
사랑의 말씀 전파하리
믿음으로 살리 거룩한 믿음
주의 진리 위해 살리라""",
        """Faith of our fathers, living still,
In spite of dungeon, fire, and sword;
O how our hearts beat high with joy
Whene'er we hear that glorious word!
Faith of our fathers, holy faith!
We will be true to thee till death.

Faith of our fathers, we will strive
To win all nations unto thee,
And through the truth that comes from God,
Mankind shall then be truly free.
Faith of our fathers, holy faith!
We will be true to thee till death.

Faith of our fathers, we will love
Both friend and foe in all our strife;
And preach thee, too, as love knows how
By kindly words and virtuous life.
Faith of our fathers, holy faith!
We will be true to thee till death.""",
    ),
    H(
        "주의 사랑 깊도다",
        "O Love That Wilt Not Let Me Go",
        "George Matheson",
        "Albert L. Peace (ST. MARGARET)",
        "1882",
        "사랑",
        "조지 매디슨(George Matheson, 1842–1906)이 실명 등의 고통 중에 지었다고 전해집니다. "
        "하나님의 놓지 않으시는 사랑을 노래합니다. PD.",
        """주의 사랑 나를 놓지 않으시네
내가 그 사랑에 내 생명 드리네
생명 강물 흘러 내 갈증 해소하고
바다처럼 풍성한 사랑이라

주의 빛 내 길에 비취시니
내 횃불을 주께 드리네
그 빛이 내 길을 환히 비추어
어두움 물리치네

주의 기쁨 내 슬픔 이기시니
내가 그 기쁨에 안식 찾네
십자가에서 피 흘리신 사랑
나를 구원하셨네""",
        """O Love that wilt not let me go,
I rest my weary soul in thee;
I give thee back the life I owe,
That in thine ocean depths its flow
May richer, fuller be.

O light that followest all my way,
I yield my flickering torch to thee;
My heart restores its borrowed ray,
That in thy sunshine’s blaze its day
May brighter, fairer be.

O Joy that seekest me through pain,
I cannot close my heart to thee;
I trace the rainbow through the rain,
And feel the promise is not vain,
That morn shall tearless be.

O Cross that liftest up my head,
I dare not ask to fly from thee;
I lay in dust life’s glory dead,
And from the ground there blossoms red
Life that shall endless be.""",
    ),
    H(
        "주 오실 때",
        "When the Roll Is Called Up Yonder",
        "James M. Black",
        "James M. Black",
        "1893",
        "소망",
        "제임스 M. 블랙(James M. Black) 작사·작곡. "
        "출석부에 이름이 없던 소녀를 생각하며 지었다고 합니다. PD(USA).",
        """주 예수 재림하실 때 나팔 소리 나고
죽은 성도 일어나며 산 자도 변하리
그 날에 그 날에 내가 참여하리
주 예수 재림하실 때 나팔 소리 나리

주의 이름 부르며 찬양할 그 날
영광의 면류관 받으리로다
그 날에 그 날에 내가 참여하리
주 예수 재림하실 때 나팔 소리 나리

세상 수고 끝나고 안식 얻을 때
주와 함께 영원히 왕 노릇 하리
그 날에 그 날에 내가 참여하리
주 예수 재림하실 때 나팔 소리 나리""",
        """When the trumpet of the Lord shall sound, and time shall be no more,
And the morning breaks, eternal, bright and fair;
When the saved of earth shall gather over on the other shore,
And the roll is called up yonder, I'll be there.
When the roll is called up yonder,
When the roll is called up yonder,
When the roll is called up yonder,
When the roll is called up yonder, I'll be there.

On that bright and cloudless morning when the dead in Christ shall rise,
And the glory of His resurrection share;
When His chosen ones shall gather to their home beyond the skies,
And the roll is called up yonder, I'll be there.
When the roll is called up yonder...

Let us labor for the Master from the dawn till setting sun,
Let us talk of all His wondrous love and care;
Then when all of life is over, and our work on earth is done,
And the roll is called up yonder, I'll be there.
When the roll is called up yonder...""",
    ),
    H(
        "천국 소망",
        "When We All Get to Heaven",
        "Eliza E. Hewitt",
        "Emily D. Wilson",
        "1898",
        "소망",
        "엘리자 E. 휴이트(Eliza E. Hewitt) 작사, 에밀리 D. 윌슨 작곡. "
        "천국 소망을 기쁨으로 노래합니다. PD(USA).",
        """주 예수 모신 곳에 우리 모두 가리
영광의 그 나라 면류관 받으리
천국 갈 때 기쁨으로 주를 찬양하리
할렐루야 주를 만나 뵙겠네

이 세상 고난 지나 평안 얻을 때
눈물 없이 주를 찬양하리
천국 갈 때 기쁨으로 주를 찬양하리
할렐루야 주를 만나 뵙겠네

주의 얼굴 뵙고서 경배하리니
영원토록 기쁨 넘치리
천국 갈 때 기쁨으로 주를 찬양하리
할렐루야 주를 만나 뵙겠네""",
        """Sing the wondrous love of Jesus,
Sing His mercy and His grace;
In the mansions bright and blessed
He'll prepare for us a place.
When we all get to heaven,
What a day of rejoicing that will be!
When we all see Jesus,
We'll sing and shout the victory!

While we walk the pilgrim pathway,
Clouds will overspread the sky;
But when traveling days are over,
Not a shadow, not a sigh.
When we all get to heaven...

Let us then be true and faithful,
Trusting, serving every day;
Just one glimpse of Him in glory
Will the toils of life repay.
When we all get to heaven...""",
    ),
    H(
        "나는 믿네",
        "I Know Whom I Have Believed",
        "Daniel W. Whittle",
        "James McGranahan",
        "1883",
        "확신",
        "대니얼 휘틀(Daniel W. Whittle) 작사, 제임스 맥그라나한 작곡. "
        "디모데후서 1:12에 기초한 확신의 찬송입니다. PD.",
        """내가 믿고 아는 이 주 예수
능히 지키시리 그 날에
내가 맡긴 것을 주가 지키사
온전케 하시리라
나는 믿네 나는 믿네
내가 믿은 이를 내가 알고
그가 나의 의뢰한 것 그날까지
능히 지키실 줄 아네

구원의 시기와 방법은
다 알 수 없어도
주의 사랑 믿을 수 있으니
평안을 누리네
나는 믿네 나는 믿네
내가 믿은 이를 내가 알고
그가 나의 의뢰한 것 그날까지
능히 지키실 줄 아네""",
        """I know not why God's wondrous grace
To me He hath made known,
Nor why, unworthy, Christ in love
Redeemed me for His own.
But I know whom I have believed,
And am persuaded that He is able
To keep that which I've committed
Unto Him against that day.

I know not how this saving faith
To me He did impart,
Nor how believing in His Word
Wrought peace within my heart.
But I know whom I have believed...

I know not how the Spirit moves,
Convincing men of sin,
Revealing Jesus through the Word,
Creating faith in Him.
But I know whom I have believed...

I know not when my Lord may come,
At night or noonday fair,
Nor if I walk the vale with Him,
Or meet Him in the air.
But I know whom I have believed...""",
    ),
    H(
        "갈보리 산 위에",
        "The Old Rugged Cross",
        "George Bennard",
        "George Bennard",
        "1913",
        "수난",
        "조지 베나드(George Bennard, 1873–1958) 작사·작곡(1913). "
        "미국에서는 출판 연도 기준으로 Public Domain입니다. "
        "(※ 일부 국가 저작권 기간은 다를 수 있으나, 본 앱은 미국 PD 기준으로 수록)",
        """갈보리 산 위에 십자가 섰으니
주가 고난을 당한 표라
험한 십자가를 내가 사랑함은
주가 보혈을 흘림이라
최후 승리를 얻기까지
주의 십자가 사랑하리
빛난 면류관 받기까지
험한 십자가 붙들겠네

멸시와 천대를 주가 받으시사
십자가 지고 가셨도다
그 사랑 고마워 내 생명 드리니
십자가 지고 가리로다
최후 승리를 얻기까지
주의 십자가 사랑하리
빛난 면류관 받기까지
험한 십자가 붙들겠네""",
        """On a hill far away stood an old rugged cross,
The emblem of suffering and shame;
And I love that old cross where the dearest and best
For a world of lost sinners was slain.
So I'll cherish the old rugged cross,
Till my trophies at last I lay down;
I will cling to the old rugged cross,
And exchange it some day for a crown.

O that old rugged cross, so despised by the world,
Has a wondrous attraction for me;
For the dear Lamb of God left His glory above
To bear it to dark Calvary.
So I'll cherish the old rugged cross...

In that old rugged cross, stained with blood so divine,
A wondrous beauty I see,
For 'twas on that old cross Jesus suffered and died,
To pardon and sanctify me.
So I'll cherish the old rugged cross...

To the old rugged cross I will ever be true;
Its shame and reproach gladly bear;
Then He'll call me some day to my home far away,
Where His glory forever I'll share.
So I'll cherish the old rugged cross...""",
        license_note=(
            "미국 Public Domain(1913년 출판). 개인 예배·교육·오프라인 이용 무료. "
            "한국찬송가공회 공식 판본과 무관. 일부 국가 저작권 기간은 상이할 수 있습니다."
        ),
    ),
    H(
        "주 하나님 찬양하세",
        "Praise to the Lord, the Almighty",
        "Joachim Neander",
        "Stralsund Gesangbuch / Traditional (LOBE DEN HERREN)",
        "1680",
        "찬양",
        "요아힘 네안더(Joachim Neander, 1650–1680)의 독일어 찬송. "
        "영어·한국어로 널리 번역된 고전 찬양입니다. PD.",
        """주 하나님 찬양하세 전능하신 주님
내 영혼아 찬양하라 구원의 하나님
주가 다스리시며 날개 아래 지키사
은혜로 품어 주시네

주 하나님 찬양하세 지혜의 주님
만물을 지으시고 다스리시네
풍성한 은혜로 우리 필요 채우사
감사케 하시네

주 하나님 찬양하세 사랑의 주님
성도들의 찬양 소리 높이 올려라
모든 호흡 있는 자 주를 찬양하여라
할렐루야 아멘""",
        """Praise to the Lord, the Almighty, the King of creation!
O my soul, praise Him, for He is thy health and salvation!
All ye who hear, now to His temple draw near;
Join me in glad adoration!

Praise to the Lord, who o'er all things so wondrously reigneth,
Shelters thee under His wings, yea, so gently sustaineth!
Hast thou not seen how thy desires e'er have been
Granted in what He ordaineth?

Praise to the Lord, who doth prosper thy work and defend thee;
Surely His goodness and mercy here daily attend thee.
Ponder anew what the Almighty can do,
If with His love He befriend thee.

Praise to the Lord, O let all that is in me adore Him!
All that hath life and breath, come now with praises before Him.
Let the Amen sound from His people again:
Gladly for aye we adore Him.""",
    ),
    H(
        "예수 그리스도",
        "Jesus Christ Is Risen Today",
        "Traditional Latin / English 14th–18th c.",
        "Lyra Davidica (EASTER HYMN)",
        "1708",
        "부활",
        "중세 라틴 부활 찬송 전통을 이은 영어 부활절 찬송. "
        "1708년 Lyra Davidica 등에 수록된 고전 텍스트입니다. PD.",
        """예수 부활하셨네 할렐루야
천사들이 찬양해 할렐루야
우리 기쁨 넘치네 할렐루야
주를 찬양하여라 할렐루야

사망 권세 이기고 할렐루야
부활의 첫 열매 되사 할렐루야
우리에게 생명 주셨네 할렐루야
주를 찬양하여라 할렐루야

영광 중에 다스리네 할렐루야
우리의 중보 되시니 할렐루야
믿음으로 살리라 할렐루야
주를 찬양하여라 할렐루야""",
        """Jesus Christ is risen today, Alleluia!
Our triumphant holy day, Alleluia!
Who did once upon the cross, Alleluia!
Suffer to redeem our loss. Alleluia!

Hymns of praise then let us sing, Alleluia!
Unto Christ, our heavenly King, Alleluia!
Who endured the cross and grave, Alleluia!
Sinners to redeem and save. Alleluia!

But the pains which He endured, Alleluia!
Our salvation have procured, Alleluia!
Now above the sky He's King, Alleluia!
Where the angels ever sing. Alleluia!

Sing we to our God above, Alleluia!
Praise eternal as His love, Alleluia!
Praise Him, all ye heavenly host, Alleluia!
Father, Son, and Holy Ghost. Alleluia!""",
    ),
    H(
        "십자가를 질 수 있나",
        "Must Jesus Bear the Cross Alone",
        "Thomas Shepherd / later editors",
        "George N. Allen (MAITLAND)",
        "1693",
        "헌신",
        "토머스 셰퍼드(Thomas Shepherd) 계통의 텍스트가 후대에 편집되어 전해집니다. "
        "십자가 제자도를 묻는 고전 헌신 찬송입니다. PD.",
        """십자가를 질 수 있나 주만 지셨나
제자 된 우리 모두 십자가 지리
영광의 면류관은 고난 후에 오리
믿음으로 십자가 지고 가리라

세상 영광 구하지 말고 주를 따르라
좁은 길 십자가의 길 주와 동행해
영광의 면류관은 고난 후에 오리
믿음으로 십자가 지고 가리라

주님 다시 오실 때 영광 나누리
십자가 진 자들만 면류관 받으리
영광의 면류관은 고난 후에 오리
믿음으로 십자가 지고 가리라""",
        """Must Jesus bear the cross alone,
And all the world go free?
No, there's a cross for everyone,
And there's a cross for me.

The consecrated cross I'll bear
Till death shall set me free;
And then go home my crown to wear,
For there's a crown for me.

Upon the crystal pavement down
At Jesus' pierced feet,
Joyful I'll cast my golden crown
And His dear name repeat.

O precious cross! O glorious crown!
O resurrection day!
When Christ the Lord from heaven comes down
And bears my soul away.""",
    ),
    H(
        "주 예수 대문 밖에",
        "O Jesus, Thou Art Standing",
        "William W. How",
        "Traditional / Justin H. Knecht",
        "1867",
        "부르심",
        "윌리엄 월시엄 하우(William Walsham How, 1823–1897) 작사. "
        "계시록 3:20의 문을 두드리시는 주님을 그립니다. PD.",
        """주 예수 대문 밖에 기다려 섰으니
똑똑 문 두드리시네 빨리 열어라
문 열어 주 영접하면 기쁨 넘치리
문 열어 주 영접하면 기쁨 넘치리

오래 참고 기다리사 문 두드리시니
냉정한 우리 마음 문을 열어야 해
문 열어 주 영접하면 기쁨 넘치리
문 열어 주 영접하면 기쁨 넘치리

오늘이 기회이니 지체 말아라
주 예수 영접하여 구원 얻으라
문 열어 주 영접하면 기쁨 넘치리
문 열어 주 영접하면 기쁨 넘치리""",
        """O Jesus, Thou art standing
Outside the fast-closed door,
In lowly patience waiting
To pass the threshold o'er:
Shame on us, Christian brothers,
His name and sign who bear,
O shame, thrice shame upon us,
To keep Him standing there!

O Jesus, Thou art knocking;
And lo, that hand is scarred,
And thorns Thy brow encircle,
And tears Thy face have marred:
O love that passeth knowledge,
So patiently to wait!
O sin that hath no equal,
So fast to bar the gate!

O Jesus, Thou art pleading
In accents meek and low,
"I died for you, My children,
And will ye treat Me so?"
O Lord, with shame and sorrow
We open now the door;
Dear Savior, enter, enter,
And leave us nevermore.""",
    ),
    H(
        "내가 십자가를 지고",
        "Jesus, I My Cross Have Taken",
        "Henry F. Lyte",
        "Traditional / Mozart arr.",
        "1824",
        "헌신",
        "헨리 F. 라이트 작사. 세상을 버리고 십자가를 지는 제자도를 노래합니다. PD.",
        """내가 십자가를 지고 주를 따르네
세상 벗과 재미 버리고 주만 따르리
주가 가신 좁은 길 나도 가리라
십자가 지고 주를 따르리

고난과 수치 당해도 낙심 안 하리
주가 나와 함께 하시니 이기리로다
주가 가신 좁은 길 나도 가리라
십자가 지고 주를 따르리

천국 문 열릴 때까지 신실하리니
영광의 면류관 받으리 주와 함께
주가 가신 좁은 길 나도 가리라
십자가 지고 주를 따르리""",
        """Jesus, I my cross have taken,
All to leave and follow Thee.
Destitute, despised, forsaken,
Thou from hence my all shall be.
Perish every fond ambition,
All I've sought or hoped or known.
Yet how rich is my condition!
God and heaven are still my own.

Let the world despise and leave me,
They have left my Savior, too.
Human hearts and looks deceive me;
Thou art not, like them, untrue.
O while Thou dost smile upon me,
God of wisdom, love, and might,
Foes may hate and friends disown me,
Show Thy face and all is bright.

Haste thee on from grace to glory,
Armed by faith, and winged by prayer.
Heaven's eternal days before thee,
God's own hand shall guide us there.
Soon shall close thy earthly mission,
Soon shall pass thy pilgrim days,
Hope shall change to glad fruition,
Faith to sight, and prayer to praise.""",
    ),
    H(
        "하나님 아버지",
        "Dear Lord and Father of Mankind",
        "John G. Whittier",
        "Frederick C. Maker (REST)",
        "1872",
        "기도",
        "존 그린리프 휘티어(John Greenleaf Whittier, 1807–1892)의 시에서 발췌. "
        "고요한 중에 주님의 음성을 구하는 찬송입니다. PD.",
        """하나님 아버지 용서하소서
어리석게 살던 날 회개합니다
고요한 중에 주의 음성 듣고
평안을 누리게 하소서

세상의 소음  monoton 멈추고
성령의 바람 일게 하소서
고요한 중에 주의 음성 듣고
평안을 누리게 하소서

안식의 주님 내 맘에 오사
폭풍을 잠잠케 하소서
고요한 중에 주의 음성 듣고
평안을 누리게 하소서""",
        """Dear Lord and Father of mankind,
Forgive our foolish ways;
Reclothe us in our rightful mind,
In purer lives Thy service find,
In deeper reverence, praise.

In simple trust like theirs who heard
Beside the Syrian sea
The gracious calling of the Lord,
Let us, like them, without a word,
Rise up and follow Thee.

O Sabbath rest by Galilee,
O calm of hills above,
Where Jesus knelt to share with Thee
The silence of eternity,
Interpreted by love!

Drop Thy still dews of quietness,
Till all our strivings cease;
Take from our souls the strain and stress,
And let our ordered lives confess
The beauty of Thy peace.""",
    ),
    # --- Additional PD titles with full EN + available KO ---
    H(
        "예수 나를 오라 하사",
        "Jesus Calls Us",
        "Cecil Frances Alexander",
        "William H. Jude (GALILEE)",
        "1852",
        "부르심",
        "세실 프랜시스 알렉산더(Cecil Frances Alexander, 1818–1895) 작사. "
        "갈릴리에서 제자들을 부르신 주님을 묵상합니다. PD.",
        """예수 나를 오라 하사 갈릴리 바닷가에서
어부들을 부르시듯 나를 부르시네
내가 주께 나가오리 모든 것 버리고
주를 따라 가겠나이다

세상 소리 유혹해도 주의 음성 들으며
십자가를 지고 주만 따르리
내가 주께 나가오리 모든 것 버리고
주를 따라 가겠나이다

사랑의 주 예수여 나를 붙드소서
세상 끝날까지 신실하게 하소서
내가 주께 나가오리 모든 것 버리고
주를 따라 가겠나이다""",
        """Jesus calls us o'er the tumult
Of our life's wild, restless sea;
Day by day His sweet voice soundeth,
Saying, "Christian, follow Me."

Jesus calls us from the worship
Of the vain world's golden store,
From each idol that would keep us,
Saying, "Christian, love Me more."

In our joys and in our sorrows,
Days of toil and hours of ease,
Still He calls, in cares and pleasures,
"Christian, love Me more than these."

Jesus calls us: by Thy mercies,
Savior, may we hear Thy call,
Give our hearts to Thine obedience,
Serve and love Thee best of all.""",
    ),
    H(
        "예수 피와 흘린 피로",
        "Are You Washed in the Blood",
        "Elisha A. Hoffman",
        "Elisha A. Hoffman",
        "1878",
        "회개",
        "엘리샤 A. 호프만(Elisha A. Hoffman, 1839–1929) 작사·작곡. PD.",
        """그대는 죄 사함 받았는가
예수 피로 씻겼는가
마음 속을 주가 다스리시나
예수 피로 씻겼는가
예수의 피로 그대 씻겼나
그 어린 양의 피로 씻겼나
몸과 맘을 주님께 바치고
예수 피로 씻겼는가

주의 나라 기업 이을 자인가
예수 피로 씻겼는가
흰 옷 입고 주를 맞이할까
예수 피로 씻겼는가
예수의 피로 그대 씻겼나
그 어린 양의 피로 씻겼나
몸과 맘을 주님께 바치고
예수 피로 씻겼는가""",
        """Have you been to Jesus for the cleansing power?
Are you washed in the blood of the Lamb?
Are you fully trusting in His grace this hour?
Are you washed in the blood of the Lamb?
Are you washed in the blood,
In the soul-cleansing blood of the Lamb?
Are your garments spotless? Are they white as snow?
Are you washed in the blood of the Lamb?

Are you walking daily by the Savior's side?
Are you washed in the blood of the Lamb?
Do you rest each moment in the Crucified?
Are you washed in the blood of the Lamb?
Are you washed in the blood...

When the Bridegroom cometh will your robes be white?
Are you washed in the blood of the Lamb?
Will your soul be ready for the mansions bright,
And be washed in the blood of the Lamb?
Are you washed in the blood...""",
    ),
    H(
        "주 예수 나를 위해",
        "At Calvary",
        "William R. Newell",
        "Daniel B. Towner",
        "1895",
        "은혜",
        "윌리엄 R. 뉴얼 작사, 대니얼 B. 타우너 작곡. 갈보리의 은혜를 회상합니다. PD(USA).",
        """여러 해 동안 방황하며 주의 은혜 몰랐네
갈보리 십자가 보혈로 구원 얻었네
자비하신 주 은혜로다
갈보리에서 날 구원했네

죄를 사하신 그 은혜 놀라우니
내 입술로 찬양하리
자비하신 주 은혜로다
갈보리에서 날 구원했네

이제 나는 자유 얻고 주만 찬양하리
갈보리 십자가 은혜로 살게 되었네
자비하신 주 은혜로다
갈보리에서 날 구원했네""",
        """Years I spent in vanity and pride,
Caring not my Lord was crucified,
Knowing not it was for me He died
On Calvary.
Mercy there was great, and grace was free;
Pardon there was multiplied to me;
There my burdened soul found liberty
At Calvary.

By God's Word at last my sin I learned;
Then I trembled at the law I'd spurned,
Till my guilty soul imploring turned
To Calvary.
Mercy there was great...

Now I've given to Jesus everything,
Now I gladly own Him as my King,
Now my raptured soul can only sing
Of Calvary!
Mercy there was great...

Oh, the love that drew salvation's plan!
Oh, the grace that brought it down to man!
Oh, the mighty gulf that God did span
At Calvary!
Mercy there was great...""",
    ),
    H(
        "내 영혼이 은혜 입어",
        "Grace Greater Than Our Sin",
        "Julia H. Johnston",
        "Daniel B. Towner",
        "1910",
        "은혜",
        "줄리아 H. 존스턴 작사, D. B. 타우너 작곡(1910). 미국 PD.",
        """내 영혼이 은혜 입어 중생하게 되었네
주의 은혜 놀라우니 측량할 수 없도다
은혜 은혜 하나님의 은혜
죄 보다 더 큰 은혜로다
은혜 은혜 하나님의 은혜
죄 보다 더 큰 은혜로다

검은 죄악 물결 같아 나를 덮을지라도
주의 은혜 더 크시니 나를 구원하시네
은혜 은혜 하나님의 은혜
죄 보다 더 큰 은혜로다

우리의 죄 사하시려 예수 피 흘리셨네
믿는 자마다 얻으리 그 크신 은혜를
은혜 은혜 하나님의 은혜
죄 보다 더 큰 은혜로다""",
        """Marvelous grace of our loving Lord,
Grace that exceeds our sin and our guilt!
Yonder on Calvary's mount outpoured,
There where the blood of the Lamb was spilled.
Grace, grace, God's grace,
Grace that will pardon and cleanse within;
Grace, grace, God's grace,
Grace that is greater than all our sin.

Sin and despair, like the sea waves cold,
Threaten the soul with infinite loss;
Grace that is greater, yes, grace untold,
Points to the refuge, the mighty cross.
Grace, grace, God's grace...

Dark is the stain that we cannot hide.
What can avail to wash it away?
Look! There is flowing a crimson tide,
Brighter than snow you may be today.
Grace, grace, God's grace...

Marvelous, infinite, matchless grace,
Freely bestowed on all who believe!
You that are longing to see His face,
Will you this moment His grace receive?
Grace, grace, God's grace...""",
    ),
    H(
        "예수께로 가면",
        "Come to the Savior",
        "George F. Root",
        "George F. Root",
        "1870",
        "부르심",
        "조지 F. 루트(George F. Root, 1820–1895) 계통의 복음 초대 찬송. PD.",
        """예수께로 오면 쉬리로다
주가 우리를 부르시네
무거운 짐 주께 맡기면
참된 안식 얻으리
주께로 주께로 지금 나오라
주께로 주께로 지금 나오라

예수께로 오면 살리로다
영원한 생명 주시네
믿는 자마다 구원 얻어
천국 백성 되리라
주께로 주께로 지금 나오라
주께로 주께로 지금 나오라""",
        """Come to the Savior, make no delay;
Here in His Word He has shown us the way;
Here in our midst He's standing today,
Tenderly saying, "Come!"
Joyful, joyful will the meeting be,
When from sin our hearts are pure and free;
And we shall gather, Savior, with Thee,
In our eternal home.

"Suffer the children!" O hear His voice!
Let every heart leap forth and rejoice;
And let us freely make Him our choice.
Do not delay, but come.
Joyful, joyful will the meeting be...

Think once again, He's with us today;
Heed now His blest command, and obey;
Hear now His accents tenderly say,
"Will you, My children, come?"
Joyful, joyful will the meeting be...""",
    ),
    H(
        "주 예수 나의 기업",
        "Be Thou My Vision",
        "Ancient Irish (trad.)",
        "Traditional Irish (SLANE)",
        "8c / tr. 1905–1912",
        "찬양",
        "고대 아일랜드 기도·찬송 전통(‘Rop tú mo baile’). "
        "영어 운문 번역(Mary E. Byrne 산문, Eleanor Hull 운문 등)과 SLANE 선율로 불립니다. "
        "고전 텍스트·선율은 Public Domain으로 취급됩니다.",
        """나의 영원하신 기업 주님 한 분뿐이라
다른 소망 없기 원함 주님 한 분뿐이라
나의 가장 좋은 친구 주님 한 분뿐이라
낮이나 밤이나 주님만 생각하겠네

주님만 내 보이는 것 주님만 내 생각
주 말씀 내 지혜 되고 주 거룩 내 능력
주 아니면 부요 없고 주 계시면 족해
하늘 가는 길 비추는 내 기업 되소서

하늘 기쁨 추구 않고 헛된 이름 구치 않네
주님만이 나의 기업 영원히 변치 않네
나의 마음 주 보좌 되어 주만 왕 되소서
천지보다 높으신 주 나의 기업 되소서""",
        """Be Thou my Vision, O Lord of my heart;
Naught be all else to me, save that Thou art.
Thou my best Thought, by day or by night,
Waking or sleeping, Thy presence my light.

Be Thou my Wisdom, and Thou my true Word;
I ever with Thee and Thou with me, Lord;
Thou my great Father, I Thy true son;
Thou in me dwelling, and I with Thee one.

Riches I heed not, nor man's empty praise,
Thou mine Inheritance, now and always:
Thou and Thou only, first in my heart,
High King of Heaven, my Treasure Thou art.

High King of Heaven, my victory won,
May I reach Heaven's joys, O bright Heaven's Sun!
Heart of my own heart, whatever befall,
Still be my Vision, O Ruler of all.""",
    ),
    H(
        "예수 보혈",
        "There Is a Fountain Filled with Blood",
        "William Cowper",
        "Traditional American (CLEANSING FOUNTAIN)",
        "1772",
        "회개",
        "윌리엄 카우퍼(William Cowper, 1731–1800) 작사. "
        "스가랴 13:1을 모티브로 한 보혈 찬송입니다. PD.",
        """예수 십자가에 흘린 피로써
그대는 씻기어 있는가
더러운 죄 희게 하는 능력을
그대는 믿는가 믿는가
예수 보혈 능력 있도다
주의 피 믿으오
예수 보혈 능력 있도다
나를 씻기에 합당하도다

내가 이 샘에 내 옷을 빨아
눈보다 희게 되었네
어린 양 보좌 앞에서 노래해
구원의 기쁨을 찬양해
예수 보혈 능력 있도다
주의 피 믿으오
예수 보혈 능력 있도다
나를 씻기에 합당하도다""",
        """There is a fountain filled with blood
Drawn from Emmanuel's veins;
And sinners plunged beneath that flood
Lose all their guilty stains.
Lose all their guilty stains,
Lose all their guilty stains;
And sinners plunged beneath that flood
Lose all their guilty stains.

The dying thief rejoiced to see
That fountain in his day;
And there have I, though vile as he,
Washed all my sins away.
Washed all my sins away,
Washed all my sins away;
And there have I, though vile as he,
Washed all my sins away.

Dear dying Lamb, Thy precious blood
Shall never lose its power
Till all the ransomed church of God
Be saved, to sin no more.
Be saved, to sin no more,
Be saved, to sin no more;
Till all the ransomed church of God
Be saved, to sin no more.

E'er since, by faith, I saw the stream
Thy flowing wounds supply,
Redeeming love has been my theme,
And shall be till I die.
And shall be till I die,
And shall be till I die;
Redeeming love has been my theme,
And shall be till I die.""",
    ),
    H(
        "주 예수 넓은 품",
        "Jesus, Lover of My Soul",
        "Charles Wesley",
        "Joseph Parry (ABERYSTWYTH) / Simeon B. Marsh",
        "1740",
        "위로",
        "찰스 웨슬리 작사(1740). 폭풍 속 피난처 되신 그리스도를 노래합니다. PD.",
        """예수여 나의 피난처 되사
풍랑 중에 나를 숨기소서
나의 연약함 아시니
주의 품 안에 안기게 하소서

다른 피난처 없고
다른 도움 없사오니
주만 의지합니다
나를 구원하소서

생명의 샘 되신 주
내 갈증 해소하소서
은혜로 채우사
새 힘 주소서""",
        """Jesus, lover of my soul,
Let me to Thy bosom fly,
While the nearer waters roll,
While the tempest still is high.
Hide me, O my Savior, hide,
Till the storm of life is past;
Safe into the haven guide;
O receive my soul at last.

Other refuge have I none,
Hangs my helpless soul on Thee;
Leave, ah! leave me not alone,
Still support and comfort me.
All my trust on Thee is stayed,
All my help from Thee I bring;
Cover my defenseless head
With the shadow of Thy wing.

Plenteous grace with Thee is found,
Grace to cover all my sin;
Let the healing streams abound;
Make and keep me pure within.
Thou of life the fountain art,
Freely let me take of Thee;
Spring Thou up within my heart;
Rise to all eternity.""",
    ),
    H(
        "오 나의 주님",
        "O for a Thousand Tongues to Sing",
        "Charles Wesley",
        "Carl G. Gläser / Lowell Mason (AZMON)",
        "1739",
        "찬양",
        "찰스 웨슬리가 회심 1주년을 기념하여 지은 긴 시 중 일부가 찬송으로 불립니다. PD.",
        """오 천 개의 혀로 찬양하리
구주 예수 영광을
하늘의 기쁨 땅 위에 퍼져
주를 찬양하여라

내 귀를 여사 듣게 하시고
내 혀를 풀어 찬양케 하사
소경의 눈 뜨게 하신 주
그 이름 높이어라

예수 이름 우리 마음에
기쁨과 평안 주시네
죄인을 의롭다 하시며
새 생명 주셨네""",
        """O for a thousand tongues to sing
My great Redeemer's praise,
The glories of my God and King,
The triumphs of His grace!

My gracious Master and my God,
Assist me to proclaim,
To spread through all the earth abroad
The honors of Thy name.

Jesus! the name that charms our fears,
That bids our sorrows cease;
'Tis music in the sinner's ears,
'Tis life, and health, and peace.

He breaks the power of canceled sin,
He sets the prisoner free;
His blood can make the foulest clean,
His blood availed for me.""",
    ),
    H(
        "주 하나님 크신 이름",
        "All Creatures of Our God and King",
        "Francis of Assisi / tr. William H. Draper",
        "Geistliche Kirchengesäng (LASST UNS ERFREUEN)",
        "1225 / tr. 1919",
        "찬양",
        "아시시의 프란치스코 ‘태양의 노래’에 기초한 찬송. "
        "영어 운문 번역(William H. Draper 등)과 LASST UNS ERFREUEN 선율로 불립니다. "
        "고전 텍스트·선율 PD. (후대 편곡은 별도 확인)",
        """주 하나님 지으신 모든 세계
내 마음 속에 그리어 볼 때
주님의 높고 크신 은혜
내 영혼 가득 차네
내 영혼아 주 찬양하라
할렐루야 할렐루야

해와 달과 별들도 찬양하고
바람과 구름도 노래하네
주님의 높고 크신 은혜
내 영혼 가득 차네
내 영혼아 주 찬양하라
할렐루야 할렐루야""",
        """All creatures of our God and King,
Lift up your voice and with us sing
Alleluia! Alleluia!
Thou burning sun with golden beam,
Thou silver moon with softer gleam!
O praise Him, O praise Him!
Alleluia! Alleluia! Alleluia!

Thou rushing wind that art so strong,
Ye clouds that sail in heaven along,
O praise Him! Alleluia!
Thou rising morn, in praise rejoice,
Ye lights of evening, find a voice!
O praise Him, O praise Him!
Alleluia! Alleluia! Alleluia!

Let all things their Creator bless,
And worship Him in humbleness,
O praise Him! Alleluia!
Praise, praise the Father, praise the Son,
And praise the Spirit, Three in One!
O praise Him, O praise Him!
Alleluia! Alleluia! Alleluia!""",
    ),
    H(
        "내 영혼아 잠잠히",
        "Be Still, My Soul",
        "Katharina von Schlegel / tr. Jane Borthwick",
        "Jean Sibelius (FINLANDIA, hymn use of PD melody tradition)",
        "1752",
        "위로",
        "카타리나 폰 슐레겔 계통 독일어 텍스트의 영어 번역(Jane Borthwick, 1855). "
        "고전 가사는 Public Domain입니다. (※ 일부 현대 편곡·음원은 별도 권리 가능)",
        """내 영혼아 잠잠하여 주를 바라라
거친 풍랑 일지라도 주가 다스리네
모든 것 합력하여 선을 이루시니
내 영혼아 잠잠히 주를 신뢰하라

내 영혼아 잠잠하여 주를 바라라
슬픔의 밤이 지나고 아침 오리라
주의 얼굴 뵙는 날 기쁨 넘치리니
내 영혼아 잠잠히 주를 신뢰하라""",
        """Be still, my soul: the Lord is on thy side.
Bear patiently the cross of grief or pain.
Leave to thy God to order and provide;
In every change, He faithful will remain.
Be still, my soul: thy best, thy heavenly Friend
Through thorny ways leads to a joyful end.

Be still, my soul: thy God doth undertake
To guide the future, as He has the past.
Thy hope, thy confidence let nothing shake;
All now mysterious shall be bright at last.
Be still, my soul: the waves and winds still know
His voice who ruled them while He dwelt below.

Be still, my soul: the hour is hastening on
When we shall be forever with the Lord,
When disappointment, grief, and fear are gone,
Sorrow forgot, love's purest joys restored.
Be still, my soul: when change and tears are past,
All safe and blessed we shall meet at last.""",
    ),
    H(
        "주가 나를 사랑하시니",
        "Love Divine, All Loves Excelling",
        "Charles Wesley",
        "John Zundel (BEECHER) / Traditional",
        "1747",
        "사랑",
        "찰스 웨슬리 작사. 하나님의 완전한 사랑과 성화를 간구하는 찬송입니다. PD.",
        """완전하신 사랑 주 예수
우리 맘에 임하소서
하늘에서 오신 사랑
우리 안에 거하소서
모든 두려움 물리치고
기쁨으로 채워 주소서
완전하신 사랑 주여
영원히 다스리소서

주의 사랑 우리를 붙들고
새 피조물 되게 하소서
영광에서 영광으로
주 형상 이루게 하소서
하늘 영광 비취사
우리 예배 받게 하소서
완전하신 사랑 주여
영원히 다스리소서""",
        """Love divine, all loves excelling,
Joy of heaven to earth come down;
Fix in us Thy humble dwelling;
All Thy faithful mercies crown!
Jesus, Thou art all compassion,
Pure unbounded love Thou art;
Visit us with Thy salvation;
Enter every trembling heart.

Breathe, O breathe Thy loving Spirit
Into every troubled breast!
Let us all in Thee inherit;
Let us find that second rest.
Take away our bent to sinning;
Alpha and Omega be;
End of faith, as its Beginning,
Set our hearts at liberty.

Come, Almighty to deliver,
Let us all Thy life receive;
Suddenly return and never,
Nevermore Thy temples leave.
Thee we would be always blessing,
Serve Thee as Thy hosts above,
Pray and praise Thee without ceasing,
Glory in Thy perfect love.""",
    ),
    H(
        "시온의 영광",
        "Glorious Things of Thee Are Spoken",
        "John Newton",
        "Franz Joseph Haydn (AUSTRIA) / Traditional",
        "1779",
        "찬양",
        "존 뉴턴 작사(Olney Hymns). 시온(교회)의 견고함과 영광을 노래합니다. PD.",
        """시온의 영광이 빛나는 아침
어둡던 이 땅이 밝아오네
형제여 들려오는 저 나팔 소리
어서 와 일어나 시온을 보라

주의 언약 반석 위에 세우신 도성
누가 능히 흔들리게 하리요
생수의 강이 흘러 넘치고
은혜의 문이 열려 있네

할렐루야 주를 찬양 시온의 왕께
영광과 존귀 돌리세
시온의 영광이 빛나는 아침
우리 모두 찬양하세""",
        """Glorious things of thee are spoken,
Zion, city of our God;
He whose word cannot be broken
Formed thee for His own abode.
On the Rock of Ages founded,
What can shake thy sure repose?
With salvation's walls surrounded,
Thou may'st smile at all thy foes.

See, the streams of living waters,
Springing from eternal love,
Well supply thy sons and daughters,
And all fear of want remove.
Who can faint while such a river
Ever flows their thirst to assuage?
Grace, which like the Lord, the Giver,
Never fails from age to age.

Round each habitation hovering,
See the cloud and fire appear
For a glory and a covering,
Showing that the Lord is near!
Thus deriving from their banner
Light by night and shade by day,
Safe they feed upon the manna
Which He gives them when they pray.""",
    ),
    H(
        "주 예수 나의 힘",
        "A Mighty Fortress Is Our God",
        "Martin Luther",
        "Martin Luther (EIN' FESTE BURG)",
        "1529",
        "믿음",
        "마르틴 루터(Martin Luther, 1483–1546) 작사·작곡. "
        "종교개혁의 대표 찬송으로 시편 46편을 기초로 합니다. PD.",
        """내 주는 강한 성이요 방패와 병기 되시니
큰 환난에서 우리를 구하여 내시리로다
옛 원수 마귀는 이제도 포악하며
세력과 권세 크고 무기도 흉하오나
주 앞에서 멸망하리라

내 힘만 의지할 때는 패할 수밖에 없도다
힘 있는 장수 나와서 날 대신하여 싸우네
이 장수 누군가 주 예수 그리스도
만군의 주로다 한 없이 강하시니
반드시 이기시리로다

이 땅에 마귀 가득해 우리를 삼키려 하나
겁내지 말고 담대히 맞서 싸워 이기리
주의 진리로 무장하고 나가세
주가 함께 하시니 우리는 이기리라""",
        """A mighty fortress is our God,
A bulwark never failing;
Our helper He, amid the flood
Of mortal ills prevailing.
For still our ancient foe
Doth seek to work us woe;
His craft and power are great,
And armed with cruel hate,
On earth is not his equal.

Did we in our own strength confide,
Our striving would be losing;
Were not the right Man on our side,
The Man of God's own choosing.
Dost ask who that may be?
Christ Jesus, it is He;
Lord Sabaoth, His name,
From age to age the same;
And He must win the battle.

And though this world, with devils filled,
Should threaten to undo us,
We will not fear, for God hath willed
His truth to triumph through us.
The Prince of Darkness grim,
We tremble not for him;
His rage we can endure,
For lo, his doom is sure,
One little word shall fell him.""",
    ),
    H(
        "내 맘의 주여",
        "Spirit of the Living God",
        "Daniel Iverson",
        "Daniel Iverson",
        "1926",
        "성령",
        "다니엘 아이버슨(Daniel Iverson) 1926년 작. 미국 기준 Public Domain(1926). "
        "짧은 성령 초청 찬송으로 전 세계에 불립니다.",
        """살아 계신 성령님 내 맘에 임하소서
살아 계신 성령님 내 맘에 임하소서
내 깨뜨리시고 녹여 주소서
살리고 채우사 사용하소서
살아 계신 성령님 내 맘에 임하소서""",
        """Spirit of the living God,
Fall afresh on me.
Spirit of the living God,
Fall afresh on me.
Melt me, mold me, fill me, use me.
Spirit of the living God,
Fall afresh on me.

Spirit of the living God,
Fall afresh on us.
Spirit of the living God,
Fall afresh on us.
Melt us, mold us, fill us, use us.
Spirit of the living God,
Fall afresh on us.""",
        license_note=(
            "미국 Public Domain(1926년 출판). 개인 예배·교육 무료. "
            "한국찬송가공회 공식 판본과 무관."
        ),
    ),
    H(
        "주와 같이 길 가는 것",
        "Trust and Obey",
        "John H. Sammis",
        "Daniel B. Towner",
        "1887",
        "신뢰",
        "존 H. 새미스 작사, D. B. 타우너 작곡. “Trust and obey” 후렴으로 유명합니다. PD.",
        """주와 같이 길 가는 것 즐거운 일 아닌가
우리 주님 걸어가신 발자취를 밟아서
신뢰하고 순종하면 기쁨이 항상 넘치리
신뢰하고 순종하면 주 예수 함께 가리

어둔 구름 덮인 길도 주님 함께 가시면
기쁨으로 따라가며 주를 찬양하리라
신뢰하고 순종하면 기쁨이 항상 넘치리
신뢰하고 순종하면 주 예수 함께 가리

주의 말씀 순종하고 주를 신뢰하면
영원한 기쁨 누리며 천국 가리로다
신뢰하고 순종하면 기쁨이 항상 넘치리
신뢰하고 순종하면 주 예수 함께 가리""",
        """When we walk with the Lord
In the light of His Word,
What a glory He sheds on our way!
While we do His good will,
He abides with us still,
And with all who will trust and obey.
Trust and obey, for there's no other way
To be happy in Jesus, but to trust and obey.

Not a shadow can rise,
Not a cloud in the skies,
But His smile quickly drives it away;
Not a doubt or a fear,
Not a sigh or a tear,
Can abide while we trust and obey.
Trust and obey...

Then in fellowship sweet
We will sit at His feet,
Or we'll walk by His side in the way;
What He says we will do,
Where He sends we will go;
Never fear, only trust and obey.
Trust and obey...""",
    ),
    H(
        "예수 따라가며",
        "Where He Leads Me",
        "E. W. Blandy",
        "John S. Norris",
        "1890",
        "헌신",
        "E. W. Blandy 작사, John S. Norris 작곡. 제자도의 순종을 다짐하는 찬송입니다. PD.",
        """예수 나를 오라 하네 예수 나를 오라 하네
예수 나를 오라 하네 내가 주님 따라가리
내가 주님 따라가리 내가 주님 따라가리
내가 주님 따라가리 어디든지 따라가리

십자가를 지고 가리 십자가를 지고 가리
십자가를 지고 가리 내가 주님 따라가리
내가 주님 따라가리 내가 주님 따라가리
내가 주님 따라가리 어디든지 따라가리""",
        """I can hear my Savior calling,
I can hear my Savior calling,
I can hear my Savior calling,
"Take thy cross and follow, follow Me."
Where He leads me I will follow,
Where He leads me I will follow,
Where He leads me I will follow;
I'll go with Him, with Him all the way.

I'll go with Him through the garden,
I'll go with Him through the garden,
I'll go with Him through the garden,
I'll go with Him, with Him all the way.
Where He leads me I will follow...

I'll go with Him through the judgment,
I'll go with Him through the judgment,
I'll go with Him through the judgment,
I'll go with Him, with Him all the way.
Where He leads me I will follow...

He will give me grace and glory,
He will give me grace and glory,
He will give me grace and glory,
And go with me, with me all the way.
Where He leads me I will follow...""",
    ),
    H(
        "주 예수 사랑 기쁨",
        "O How I Love Jesus",
        "Frederick Whitfield",
        "Traditional American",
        "1855",
        "사랑",
        "프레더릭 휘트필드(Frederick Whitfield) 작사. 전통 미국 선율로 불립니다. PD.",
        """주 예수 이름 높이어 내 맘에 기쁨 넘치네
그 이름 부를 때마다 내 영혼 소생하네
내가 주 예수 사랑함은 그 이름 귀하고
내가 주 예수 사랑함은 나를 구원함이라

주 예수 나를 사랑하사 십자가 지셨네
그 사랑 보답하고자 내 생명 드리리
내가 주 예수 사랑함은 그 이름 귀하고
내가 주 예수 사랑함은 나를 구원함이라""",
        """There is a name I love to hear,
I love to sing its worth;
It sounds like music in my ear,
The sweetest name on earth.
O how I love Jesus,
O how I love Jesus,
O how I love Jesus,
Because He first loved me!

It tells me of a Savior's love,
Who died to set me free;
It tells me of His precious blood,
The sinner's perfect plea.
O how I love Jesus...

It tells of One whose loving heart
Can feel my deepest woe;
Who in each sorrow bears a part
That none can bear below.
O how I love Jesus...""",
    ),
    H(
        "주 나의 목자",
        "The Lord's My Shepherd",
        "Scottish Psalter",
        "Jessie Seymour Irvine (CRIMOND)",
        "1650",
        "위로",
        "스코틀랜드 운율 시편(1650)에 기초한 시편 23편 찬송. "
        "CRIMOND 선율과 함께 널리 불립니다. PD.",
        """주 나의 목자 되시니 부족함 없어라
푸른 풀밭 쉴 만한 물가로 인도하시네
내 영혼 소생시키사 의의 길로 인도
주의 이름 위하여 나를 지키시네

사망 음침한 골짜기 다닐지라도
주 함께 하시니 두려워 않으리
주의 지팡이 막대기 나를 안위하시네
원수 앞에서 상을 베푸시네

내 잔이 넘치나이다 선하심과 인자하심
평생 나를 따르리니
내가 여호와의 집에 영원히 살리로다
주 나의 목자 되시니 감사하리라""",
        """The Lord's my Shepherd, I'll not want.
He makes me down to lie
In pastures green; He leadeth me
The quiet waters by.

My soul He doth restore again;
And me to walk doth make
Within the paths of righteousness,
E'en for His own name's sake.

Yea, though I walk in death's dark vale,
Yet will I fear none ill;
For Thou art with me; and Thy rod
And staff me comfort still.

My table Thou hast furnished
In presence of my foes;
My head Thou dost with oil anoint,
And my cup overflows.

Goodness and mercy all my life
Shall surely follow me;
And in God's house forevermore
My dwelling place shall be.""",
    ),
    H(
        "오 거룩하신 밤",
        "Silent Night",
        "Joseph Mohr",
        "Franz X. Gruber",
        "1818",
        "성탄",
        "요제프 모르 작사, 프란츠 그루버 작곡(1818, 오스트리아). "
        "세계에서 가장 사랑받는 성탄 캐럴 중 하나이며 Public Domain입니다.",
        """고요한 밤 거룩한 밤 어둠에 묻힌 밤
별빛 밝은 그 밤에 구주 예수 나셨네
모든 사람 잠든 밤에 주의 부모 깨어 있어
아기 예수 지키네 아기 예수 지키네

고요한 밤 거룩한 밤 목자들 놀라네
영광의 천사 나타나 기쁜 소식 전하네
평화가 임하였도다 구주 예수 나셨네
구주 예수 나셨네 구주 예수 나셨네

고요한 밤 거룩한 밤 주 예수 얼굴
은혜와 사랑 빛나고 구원의 새벽 밝았네
예수 주님 나셨네 예수 주님 나셨네
예수 주님 나셨네""",
        """Silent night, holy night!
All is calm, all is bright
Round yon virgin mother and Child.
Holy Infant, so tender and mild,
Sleep in heavenly peace,
Sleep in heavenly peace.

Silent night, holy night!
Shepherds quake at the sight;
Glories stream from heaven afar,
Heavenly hosts sing Alleluia!
Christ the Savior is born,
Christ the Savior is born!

Silent night, holy night!
Son of God, love's pure light
Radiant beams from Thy holy face
With the dawn of redeeming grace,
Jesus, Lord, at Thy birth,
Jesus, Lord, at Thy birth.""",
    ),
    H(
        "기쁘다 구주 오셨네",
        "Joy to the World",
        "Isaac Watts",
        "Lowell Mason (after Handel)",
        "1719",
        "성탄",
        "아이작 와츠가 시편 98편을 그리스도 중심으로 재해석한 찬송. "
        "성탄절에 가장 많이 불리는 곡 중 하나입니다. PD.",
        """기쁘다 구주 오셨네 만백성 맞으라
온 교회여 다 일어나 다 찬양하여라
다 찬양하여라 다 찬양하여라
다 찬양 찬양하여라

구세주 탄생하셨네 다 찬양하여라
땅과 하늘 응답하여 다 찬양하여라
다 찬양하여라 다 찬양하여라
다 찬양 찬양하여라

죄와 슬픔 없애고 가시덤불 거두사
진리와 은혜 비추시니 다 찬양하여라
다 찬양하여라 다 찬양하여라
다 찬양 찬양하여라""",
        """Joy to the world, the Lord is come!
Let earth receive her King;
Let every heart prepare Him room,
And heaven and nature sing,
And heaven and nature sing,
And heaven, and heaven, and nature sing.

Joy to the earth, the Savior reigns!
Let men their songs employ;
While fields and floods, rocks, hills, and plains
Repeat the sounding joy,
Repeat the sounding joy,
Repeat, repeat, the sounding joy.

No more let sins and sorrows grow,
Nor thorns infest the ground;
He comes to make His blessings flow
Far as the curse is found,
Far as the curse is found,
Far as, far as, the curse is found.

He rules the world with truth and grace,
And makes the nations prove
The glories of His righteousness,
And wonders of His love,
And wonders of His love,
And wonders, wonders, of His love.""",
    ),
    H(
        "천사 찬송하기를",
        "Hark! the Herald Angels Sing",
        "Charles Wesley / George Whitefield (alt.)",
        "Felix Mendelssohn / William H. Cummings",
        "1739",
        "성탄",
        "찰스 웨슬리 원작 성탄 찬송. 후대 편집과 멘델스존 선율 편곡으로 정착. "
        "고전 가사·기본 선율 전통은 PD로 널리 사용됩니다.",
        """천사 찬송하기를 그리스도 탄생하셨네
영광 중에 나신 주 땅 위 평화 이루셨네
모든 나라 백성아 일어나 찬양하라
천사와 사람 함께 구주 나심 찬양해
천사 찬송하기를 그리스도 탄생하셨네

하늘 높이 계셨던 그리스도 주께서
처녀 몸 빌려 오사 우리와 함께 하시네
하나님이 사람 되어 우리 죄 사하시려
죽기까지 낮아지신 예수 이름 높이어
천사 찬송하기를 그리스도 탄생하셨네""",
        """Hark! the herald angels sing,
"Glory to the newborn King;
Peace on earth, and mercy mild,
God and sinners reconciled!"
Joyful, all ye nations rise,
Join the triumph of the skies;
With th'angelic host proclaim,
"Christ is born in Bethlehem!"
Hark! the herald angels sing,
"Glory to the newborn King!"

Christ, by highest heaven adored;
Christ, the everlasting Lord!
Late in time behold Him come,
Offspring of the Virgin's womb:
Veiled in flesh the Godhead see;
Hail th'incarnate Deity,
Pleased as man with men to dwell,
Jesus, our Emmanuel.
Hark! the herald angels sing,
"Glory to the newborn King!"

Hail the heaven-born Prince of Peace!
Hail the Sun of Righteousness!
Light and life to all He brings,
Risen with healing in His wings.
Mild He lays His glory by,
Born that man no more may die,
Born to raise the sons of earth,
Born to give them second birth.
Hark! the herald angels sing,
"Glory to the newborn King!" """,
    ),
    H(
        "오 베들레헴 작은 골",
        "O Little Town of Bethlehem",
        "Phillips Brooks",
        "Lewis H. Redner",
        "1868",
        "성탄",
        "필립스 브룩스 목사가 성지 순례 후 작사, 루이스 레드너 작곡. PD.",
        """오 베들레헴 작은 골 너 고요한 밤에
온 세상 잠든 그 때에 구주 나셨네
Morgen 별이 비추고 천사 노래할 때
구주의 탄생 소식을 전하여 주었네

오 거룩한 그 밤중에 주 예수 나시어
죄 많은 세상 가운데 빛으로 오셨네
우리 마음 문을 열고 주를 영접하면
영원한 생명 주시리 구주 예수님""",
        """O little town of Bethlehem,
How still we see thee lie!
Above thy deep and dreamless sleep
The silent stars go by.
Yet in thy dark streets shineth
The everlasting Light;
The hopes and fears of all the years
Are met in thee tonight.

For Christ is born of Mary,
And gathered all above,
While mortals sleep, the angels keep
Their watch of wondering love.
O morning stars together
Proclaim the holy birth,
And praises sing to God the King,
And peace to men on earth!

How silently, how silently,
The wondrous gift is given!
So God imparts to human hearts
The blessings of His heaven.
No ear may hear His coming,
But in this world of sin,
Where meek souls will receive Him still,
The dear Christ enters in.""",
    ),
    H(
        "내 주를 찬양해",
        "Praise Him! Praise Him!",
        "Fanny J. Crosby",
        "Chester G. Allen",
        "1869",
        "찬양",
        "패니 크로즈비 작사, 체스터 G. 앨런 작곡. 기쁨 넘치는 찬양 찬송입니다. PD.",
        """주 찬양 주 찬양 영광의 왕께
주 찬양 주 찬양 구원의 주님
우리 죄 위해 죽으신 주
부활하사 다스리시네
주 찬양 주 찬양 영광의 왕께
주 찬양 주 찬양 영원히

주 찬양 주 찬양 사랑의 주님
주 찬양 주 찬양 능력의 주님
연약한 자 붙드시고
낙심한 자 일으키시네
주 찬양 주 찬양 영광의 왕께
주 찬양 주 찬양 영원히""",
        """Praise Him! Praise Him! Jesus, our blessed Redeemer!
Sing, O Earth, His wonderful love proclaim!
Hail Him! hail Him! highest archangels in glory;
Strength and honor give to His holy name!
Like a shepherd, Jesus will guard His children,
In His arms He carries them all day long.
Praise Him! Praise Him! tell of His excellent greatness;
Praise Him! Praise Him! ever in joyful song!

Praise Him! Praise Him! Jesus, our blessed Redeemer!
For our sins He suffered, and bled, and died.
He our Rock, our hope of eternal salvation,
Hail Him! hail Him! Jesus the Crucified.
Sound His praises! Jesus who bore our sorrows,
Love unbounded, wonderful, deep, and strong.
Praise Him! Praise Him! tell of His excellent greatness;
Praise Him! Praise Him! ever in joyful song!

Praise Him! Praise Him! Jesus, our blessed Redeemer!
Heavenly portals loud with hosannas ring!
Jesus, Savior, reigneth forever and ever.
Crown Him! crown Him! Prophet, and Priest, and King!
Christ is coming! over the world victorious,
Power and glory unto the Lord belong.
Praise Him! Praise Him! tell of His excellent greatness;
Praise Him! Praise Him! ever in joyful song!""",
    ),
    H(
        "주 사랑 놀라워",
        "The Love of God",
        "Frederick M. Lehman",
        "Frederick M. Lehman",
        "1917",
        "사랑",
        "프레더릭 M. 레만 작사·작곡(1917). 미국 PD. "
        "3절의 ‘종이와 잉크’ 이미지는 유대 시 전통에서 따온 것으로 알려져 있습니다.",
        """하늘 위에 비할 데 없는 사랑
땅 아래 더 깊은 사랑
모든 사람 구원하시려
독생자 보내셨네
오 사랑 하나님의 사랑
죄인 위해 베푸신 사랑
측량할 수 없는 그 사랑
영원히 찬양하리

이 세상 모든 바다를 잉크 삼고
하늘을 종이 삼아도
하나님의 사랑 다 기록 못해
끝이 없으리
오 사랑 하나님의 사랑
죄인 위해 베푸신 사랑
측량할 수 없는 그 사랑
영원히 찬양하리""",
        """The love of God is greater far
Than tongue or pen can ever tell;
It goes beyond the highest star,
And reaches to the lowest hell.
The guilty pair, bowed down with care,
God gave His Son to win;
His erring child He reconciled,
And pardoned from his sin.
O love of God, how rich and pure!
How measureless and strong!
It shall forevermore endure
The saints' and angels' song.

When years of time shall pass away
And earthly thrones and kingdoms fall,
When men, who here refuse to pray,
On rocks and hills and mountains call,
God's love so sure shall still endure,
All measureless and strong;
Redeeming grace to Adam's race—
The saints' and angels' song.
O love of God...

Could we with ink the ocean fill
And were the skies of parchment made,
Were every stalk on earth a quill
And every man a scribe by trade,
To write the love of God above
Would drain the ocean dry;
Nor could the scroll contain the whole
Though stretched from sky to sky.
O love of God...""",
    ),
    H(
        "주 나의 왕",
        "Rejoice, the Lord Is King",
        "Charles Wesley",
        "John Darwall (DARWALL)",
        "1744",
        "찬양",
        "찰스 웨슬리 작사. 부활·승천하신 왕의 통치를 선포하는 찬송입니다. PD.",
        """기뻐하라 주가 왕이시라
높이 손뼉 치며 찬양하라
주 예수 다스리시니
영원히 왕 되시네
기뻐하라 주가 왕이시라
기뻐하라 주가 왕이시라

사망 권세 이기신 주
보좌에 앉으셨네
우리의 중보 되시며
다시 오실 주님
기뻐하라 주가 왕이시라
기뻐하라 주가 왕이시라""",
        """Rejoice, the Lord is King!
Your Lord and King adore;
Mortals, give thanks and sing,
And triumph evermore.
Lift up your heart, lift up your voice!
Rejoice, again I say, rejoice!

Jesus, the Savior, reigns,
The God of truth and love;
When He had purged our stains,
He took His seat above.
Lift up your heart, lift up your voice!
Rejoice, again I say, rejoice!

His kingdom cannot fail,
He rules o'er earth and heaven;
The keys of death and hell
Are to our Jesus given.
Lift up your heart, lift up your voice!
Rejoice, again I say, rejoice!

Rejoice in glorious hope!
Our Lord the Judge shall come,
And take His servants up
To their eternal home.
Lift up your heart, lift up your voice!
Rejoice, again I say, rejoice!""",
    ),
    H(
        "주 예수 내 기쁨",
        "Jesus, the Very Thought of Thee",
        "Bernard of Clairvaux (attr.) / tr. Edward Caswall",
        "John B. Dykes (ST. AGNES)",
        "12c / tr. 1849",
        "사랑",
        "클레르보의 베르나르드에 가탁된 중세 라틴 시 전통. "
        "에드워드 캐스월 영어 번역. PD.",
        """예수 생각만 하여도 내 맘이 기쁘고
그 이름 부를 때마다 기쁨이 넘치네
예수보다 더 단 것 없고
예수보다 더 귀한 것 없네

예수 사랑 체험한 자 그 기쁨 알고
주와 동행하는 자 평안을 누리네
예수보다 더 단 것 없고
예수보다 더 귀한 것 없네

주여 내 맘에 오셔서 왕 되어 주소서
영원토록 함께 하사 기쁨 주소서
예수보다 더 단 것 없고
예수보다 더 귀한 것 없네""",
        """Jesus, the very thought of Thee
With sweetness fills my breast;
But sweeter far Thy face to see,
And in Thy presence rest.

Nor voice can sing, nor heart can frame,
Nor can the memory find
A sweeter sound than Thy blest name,
O Savior of mankind!

O hope of every contrite heart,
O joy of all the meek,
To those who fall, how kind Thou art!
How good to those who seek!

Jesus, our only joy be Thou,
As Thou our prize will be;
Jesus, be Thou our glory now,
And through eternity.""",
    ),
    H(
        "오 신실하신 주",
        "Great Is Thy Faithfulness",
        "Thomas O. Chisholm",
        "William M. Runyan",
        "1923",
        "신뢰",
        "토머스 O. 치좀 작사, 윌리엄 M. 러니언 작곡(1923). "
        "예레미야애가 3:22–23에 기초. 미국 Public Domain.",
        """오 신실하신 주 내 아버지
늘 함께 하시며 지키시네
아침마다 새롭고 밤마다 변함없는
주의 신실하심 찬양하리
오 신실하신 주 오 신실하신 주
날마다 주의 긍휼 나에게 베푸시네
오 신실하신 주 오 신실하신 주
언제나 변함없는 신실하신 주

봄여름 가을겨울 해와 달과 별
모든 것 주 신실하심 증거하네
사죄와 평안 힘을 더하시며
장래 소망 주셨네
오 신실하신 주 오 신실하신 주
날마다 주의 긍휼 나에게 베푸시네""",
        """Great is Thy faithfulness, O God my Father;
There is no shadow of turning with Thee;
Thou changest not, Thy compassions, they fail not;
As Thou hast been Thou forever wilt be.
Great is Thy faithfulness!
Great is Thy faithfulness!
Morning by morning new mercies I see;
All I have needed Thy hand hath provided.
Great is Thy faithfulness, Lord, unto me!

Summer and winter, and springtime and harvest,
Sun, moon, and stars in their courses above
Join with all nature in manifold witness
To Thy great faithfulness, mercy, and love.
Great is Thy faithfulness...

Pardon for sin and a peace that endureth,
Thine own dear presence to cheer and to guide;
Strength for today and bright hope for tomorrow,
Blessings all mine, with ten thousand beside!
Great is Thy faithfulness...""",
        license_note=(
            "미국 Public Domain(1923년 출판). 개인 예배·교육·오프라인 무료. "
            "한국찬송가공회 공식 판본과 무관."
        ),
    ),
    H(
        "주 함께 하시는 길",
        "God Be with You Till We Meet Again",
        "Jeremiah E. Rankin",
        "William G. Tomer",
        "1880",
        "교제",
        "예레미야 E. 랭킨 작사, 윌리엄 G. 토머 작곡. 파송·환송 찬송의 고전입니다. PD.",
        """주 함께 하심을 기원하네
다시 만날 때까지
주의 품 안에 지키시기를
다시 만날 때까지
다시 만날 때 다시 만날 때
주의 은혜로 다시 만날 때
다시 만날 때 다시 만날 때
주의 은혜로 다시 만나리

환난과 시험 중에도
주가 지키시기를
다시 만날 때까지
평안을 주시기를
다시 만날 때 다시 만날 때
주의 은혜로 다시 만날 때""",
        """God be with you till we meet again;
By His counsels guide, uphold you,
With His sheep securely fold you;
God be with you till we meet again.
Till we meet, till we meet,
Till we meet at Jesus' feet;
Till we meet, till we meet,
God be with you till we meet again.

God be with you till we meet again;
Neath His wings protecting hide you,
Daily manna still provide you;
God be with you till we meet again.
Till we meet...

God be with you till we meet again;
When life's perils thick confound you,
Put His arms unfailing round you;
God be with you till we meet again.
Till we meet...""",
    ),
    H(
        "내 평생에 가는 길",
        "Savior, Like a Shepherd Lead Us",
        "Dorothy A. Thrupp (attr.)",
        "William B. Bradbury",
        "1836",
        "인도",
        "도로시 A. 스럽 등에 가탁되는 어린이·목자 찬송. 브래드버리 선율. PD.",
        """내 평생에 가는 길 순탄하여도
주 예수 인도하니 걱정 없네
위험한 물결 일 때 주가 지키사
평안히 가게 하시네
예수 목자 되시니 나를 지키네
예수 목자 되시니 나를 지키네

연약한 양 같은 나 붙드시오니
목자 되신 주 예수 감사하네
푸른 초장 물가로 인도하시며
쉴 만한 곳 예비하시네
예수 목자 되시니 나를 지키네
예수 목자 되시니 나를 지키네""",
        """Savior, like a shepherd lead us,
Much we need Thy tender care;
In Thy pleasant pastures feed us,
For our use Thy folds prepare.
Blessed Jesus, blessed Jesus!
Thou hast bought us, Thine we are.
Blessed Jesus, blessed Jesus!
Thou hast bought us, Thine we are.

We are Thine, Thou dost befriend us,
Be the guardian of our way;
Keep Thy flock, from sin defend us,
Seek us when we go astray.
Blessed Jesus, blessed Jesus!
Hear, O hear us when we pray.
Blessed Jesus, blessed Jesus!
Hear, O hear us when we pray.

Thou hast promised to receive us,
Poor and sinful though we be;
Thou hast mercy to relieve us,
Grace to cleanse and power to free.
Blessed Jesus, blessed Jesus!
We will early turn to Thee.
Blessed Jesus, blessed Jesus!
We will early turn to Thee.""",
    ),
    H(
        "주 예수 이름의 능력",
        "Blessed Be the Name",
        "William H. Clark / Ralph E. Hudson (refrain)",
        "Ralph E. Hudson / Traditional",
        "1888",
        "찬양",
        "고전 복음 찬송 “Blessed Be the Name”. 미국 PD 레퍼토리.",
        """주 예수 이름 높이어 찬양하여라
하늘과 땅의 모든 권세 그 이름에 있네
주의 이름 찬양하세 주의 이름 찬양하세
주의 이름 찬양하세 영광의 주 이름

죄인을 구원하시며 병든 자 고치네
주 이름 능력으로 승리하리라
주의 이름 찬양하세 주의 이름 찬양하세
주의 이름 찬양하세 영광의 주 이름""",
        """All praise to Him who reigns above
In majesty supreme,
Who gave His Son for man to die,
That He might man redeem!
Blessed be the name! Blessed be the name!
Blessed be the name of the Lord!
Blessed be the name! Blessed be the name!
Blessed be the name of the Lord!

His name above all names shall stand,
Exalted more and more,
At God the Father's own right hand,
Where angel hosts adore.
Blessed be the name...

Redeemer, Savior, Friend of man
Once ruined by the fall,
Thou hast devised salvation's plan,
For Thou hast died for all.
Blessed be the name...""",
    ),
    H(
        "시험에 들지 말고",
        "Yield Not to Temptation",
        "Horatio R. Palmer",
        "Horatio R. Palmer",
        "1868",
        "믿음",
        "호레이쇼 R. 팔머(Horatio R. Palmer, 1834–1907) 작사·작곡. 시험을 이기라는 권면의 복음 찬송입니다. PD.",
        """시험이 올 때에 넘어지지 말고
주 예수 의지하여 이기라
악한 자 유혹해도 담대히 맞서
기도로 이기라
주를 의지하면 이기리라
주를 의지하면 이기리라
시험이 올 때에 넘어지지 말고
주 예수 의지하여 이기라

악한 말 친구를 멀리하고
주의 이름 경외하여라
진실하고 온유하게 살며
주를 바라보라
주를 의지하면 이기리라
주를 의지하면 이기리라
시험이 올 때에 넘어지지 말고
주 예수 의지하여 이기라""",
        """Yield not to temptation, for yielding is sin;
Each victory will help you some other to win;
Fight manfully onward, dark passions subdue,
Look ever to Jesus, He will carry you through.
Ask the Savior to help you,
Comfort, strengthen, and keep you;
He is willing to aid you,
He will carry you through.

Shun evil companions, bad language disdain,
God's name hold in reverence, nor take it in vain;
Be thoughtful and earnest, kindhearted and true,
Look ever to Jesus, He will carry you through.
Ask the Savior to help you...

To him that o'ercometh, God giveth a crown;
Through faith we shall conquer, though often cast down;
He who is our Savior our strength will renew;
Look ever to Jesus, He will carry you through.
Ask the Savior to help you...""",
    ),
    H(
        "주 예수 나를 사랑하시니",
        "O How I Love Jesus (alt)",
        "SKIP_DUP",
        "SKIP",
        "1855",
        "사랑",
        "dup",
        "x",
        "x",
    ),
    H(
        "주의 십자가 자랑",
        "In the Cross of Christ I Glory",
        "John Bowring",
        "Ithamar Conkey (RATHBUN)",
        "1825",
        "수난",
        "존 보우링(John Bowring, 1792–1872) 작사. 십자가 영광의 고전 찬송입니다. PD.",
        """십자가 자랑하리 주 예수의 십자가
세상 영광 비교 않고 오직 십자가
고난 중에도 빛이 되고
기쁨 중에도 빛이 되네
십자가 자랑하리 주 예수의 십자가

평안할 때나 환난 때나
십자가 바라보리
죄 사함과 평안을 주신
주의 십자가
고난 중에도 빛이 되고
기쁨 중에도 빛이 되네
십자가 자랑하리 주 예수의 십자가""",
        """In the cross of Christ I glory,
Towering o'er the wrecks of time;
All the light of sacred story
Gathers round its head sublime.

When the woes of life o'ertake me,
Hopes deceive, and fears annoy,
Never shall the cross forsake me.
Lo! it glows with peace and joy.

When the sun of bliss is beaming
Light and love upon my way,
From the cross the radiance streaming
Adds more luster to the day.

Bane and blessing, pain and pleasure,
By the cross are sanctified;
Peace is there that knows no measure,
Joys that through all time abide.""",
    ),
    H(
        "오 아름다운 구주",
        "Fairest Lord Jesus",
        "Münster Gesangbuch / tr. traditional",
        "Silesian folk (CRUSADER'S HYMN)",
        "1677",
        "찬양",
        "독일 뮌스터 성가집 계열 텍스트와 실레지아 민요 선율. "
        "영어·한국어로 널리 번역된 고전 찬송이며 Public Domain입니다.",
        """아름다운 구주 예수
만물의 주 되시네
예수 나의 구주시니
나 찬양하리
아름다운 구주 예수
만물의 주 되시네

들에 핀 꽃보다 아름답고
별빛보다 찬란한
예수 나의 구주시니
나 찬양하리
아름다운 구주 예수
만물의 주 되시네

예수 영광 해같이 빛나고
달보다 아름다워
예수 나의 구주시니
나 찬양하리
아름다운 구주 예수
만물의 주 되시네""",
        """Fairest Lord Jesus, Ruler of all nature,
O Thou of God and man the Son,
Thee will I cherish, Thee will I honor,
Thou, my soul's glory, joy, and crown.

Fair are the meadows, fairer still the woodlands,
Robed in the blooming garb of spring;
Jesus is fairer, Jesus is purer,
Who makes the woeful heart to sing.

Fair is the sunshine, fairer still the moonlight,
And all the twinkling starry host;
Jesus shines brighter, Jesus shines purer
Than all the angels heaven can boast.

Beautiful Savior! Lord of all the nations!
Son of God and Son of Man!
Glory and honor, praise, adoration,
Now and forevermore be Thine!""",
    ),
    H(
        "주 하나님 능력",
        "Guide Me, O Thou Great Jehovah",
        "William Williams",
        "John Hughes (CWM RHONDDA) / Traditional",
        "1745",
        "인도",
        "웨일스의 윌리엄 윌리엄스(William Williams Pantycelyn) 작사. "
        "광야 여정의 하나님 인도를 노래합니다. PD.",
        """인도하소서 여호와여
순례자의 길을 가는 나
광야 같은 이 세상에서
만나로 먹이소서
불기둥 구름기둥
항상 인도하소서
항상 인도하소서

생수의 반석 되신 주
목마른 나를 채우소서
불로 단련하실지라도
나를 지키소서
가나안 땅 이를 때까지
항상 인도하소서
항상 인도하소서""",
        """Guide me, O Thou great Jehovah,
Pilgrim through this barren land.
I am weak, but Thou art mighty;
Hold me with Thy powerful hand.
Bread of heaven, bread of heaven,
Feed me till I want no more;
Feed me till I want no more.

Open now the crystal fountain,
Whence the healing stream doth flow;
Let the fire and cloudy pillar
Lead me all my journey through.
Strong Deliverer, strong Deliverer,
Be Thou still my Strength and Shield;
Be Thou still my Strength and Shield.

When I tread the verge of Jordan,
Bid my anxious fears subside;
Death of death and hell's Destruction,
Land me safe on Canaan's side.
Songs of praises, songs of praises,
I will ever give to Thee;
I will ever give to Thee.""",
    ),
    H(
        "주 예수 내 소망",
        "My Faith Looks Up to Thee",
        "Ray Palmer",
        "Lowell Mason (OLIVET)",
        "1830",
        "믿음",
        "레이 팔머(Ray Palmer, 1808–1887) 작사, 로웰 메이슨 작곡. PD.",
        """내 믿음 주를 바라보네
하나님의 어린 양
구주여 지금 들으사
내 죄 사하소서
내 열심 불타오르게
주의 사랑으로

내 연약함 아시니
힘을 더하소서
어두운 생애 길에
빛이 되소서
살든지 죽든지
주만 찬양하리

내가 세상 떠날 때
주를 바라보리
영광의 나라에서
주를 뵙겠네
믿음이 실상 되어
주를 찬양하리""",
        """My faith looks up to Thee,
Thou Lamb of Calvary,
Savior divine!
Now hear me while I pray,
Take all my guilt away,
O let me from this day
Be wholly Thine!

May Thy rich grace impart
Strength to my fainting heart,
My zeal inspire!
As Thou hast died for me,
O may my love to Thee
Pure, warm, and changeless be,
A living fire!

While life's dark maze I tread,
And griefs around me spread,
Be Thou my guide;
Bid darkness turn to day,
Wipe sorrow's tears away,
Nor let me ever stray
From Thee aside.

When ends life's transient dream,
When death's cold, sullen stream
Shall o'er me roll,
Blest Savior, then, in love,
Fear and distrust remove;
O bear me safe above,
A ransomed soul!""",
    ),
    H(
        "주의 사랑 비췰 때",
        "Sun of My Soul",
        "John Keble",
        "Katholisches Gesangbuch / Traditional (HURSLEY)",
        "1820",
        "기도",
        "존 키블(John Keble, 1792–1866) 《The Christian Year》의 저녁 찬송. PD.",
        """내 영혼의 태양 되신 주
날이 저물어도 떠나지 마소서
어둠이 내릴 때에도
주의 빛 비춰 주소서

다른 친구 떠날지라도
주여 나와 함께 하소서
생명 다하는 날까지
나를 지키소서

아침에 눈을 뜰 때에도
주 얼굴 뵙게 하소서
내 영혼의 태양 되신 주
영원히 비춰 주소서""",
        """Sun of my soul, Thou Savior dear,
It is not night if Thou be near;
O may no earthborn cloud arise
To hide Thee from Thy servant's eyes.

When the soft dews of kindly sleep
My wearied eyelids gently steep,
Be my last thought, how sweet to rest
Forever on my Savior's breast.

Abide with me from morn till eve,
For without Thee I cannot live;
Abide with me when night is nigh,
For without Thee I dare not die.

Come near and bless us when we wake,
Ere through the world our way we take,
Till in the ocean of Thy love
We lose ourselves in heaven above.""",
    ),
    H(
        "오 주님 임재 앞에서",
        "Sweet Hour of Prayer (already have)",
        "SKIP_DUP2",
        "SKIP",
        "1845",
        "기도",
        "dup",
        "x",
        "x",
    ),
    H(
        "주 오시네",
        "The Church's One Foundation",
        "Samuel J. Stone",
        "Samuel S. Wesley (AURELIA)",
        "1866",
        "교회",
        "새뮤얼 J. 스톤(Samuel J. Stone) 작사, 새뮤얼 S. 웨슬리 작곡. "
        "교회의 기초 되신 그리스도를 고백합니다. PD.",
        """교회의 참된 터는 주 예수뿐이라
주가 피 흘려 사신 거룩한 교회라
위에서 택하시고 진리로 세우사
성도와 하나 되어 주 찬양하네

만백성 가운데서 부르신 교회여
한 주와 한 믿음과 한 세례 받았네
한 이름 받들어 한 소망 품고서
주의 몸 이룬 우리 하나 되세

환난과 박해 중에도 견디는 교회여
주의 평화 기다리며 기도하네
승리의 그날 이르러 영광 중에
주를 뵙고 찬양하리""",
        """The Church's one foundation
Is Jesus Christ her Lord;
She is His new creation
By water and the Word.
From heaven He came and sought her
To be His holy bride;
With His own blood He bought her,
And for her life He died.

Elect from every nation,
Yet one o'er all the earth;
Her charter of salvation:
One Lord, one faith, one birth.
One holy name she blesses,
Partakes one holy food,
And to one hope she presses,
With every grace endued.

Mid toil and tribulation,
And tumult of her war,
She waits the consummation
Of peace forevermore;
Till with the vision glorious
Her longing eyes are blest,
And the great Church victorious
Shall be the Church at rest.""",
    ),
    H(
        "주 예수 내 희망",
        "It Is Well with My Soul",
        "Horatio G. Spafford",
        "Philip P. Bliss",
        "1873",
        "위로",
        "호레이쇼 스패퍼드(Horatio G. Spafford)가 가족이 겪은 비극 후에 지은 찬송. "
        "필립 블리스가 곡을 붙였습니다. PD.",
        """내 평생에 가는 길 순탄하여도
주 언제든 나와 함께 하시네
큰 풍파가 일어나도 낙심 말아
내 영혼 평안해
내 영혼 평안해 내 영혼 평안해
내 영혼 평안해

내 죄가 주홍 같을지라도
주 보혈로 눈보다 희게 됐네
십자가 바라보니 감사하여라
내 영혼 평안해
내 영혼 평안해 내 영혼 평안해
내 영혼 평안해

주 예수 재림하실 그 날에
나팔 소리와 함께 주를 뵙리
그 영광 중에 외치리 아멘
내 영혼 평안해
내 영혼 평안해 내 영혼 평안해
내 영혼 평안해""",
        """When peace, like a river, attendeth my way,
When sorrows like sea billows roll;
Whatever my lot, Thou hast taught me to say,
It is well, it is well with my soul.
It is well with my soul,
It is well, it is well with my soul.

Though Satan should buffet, though trials should come,
Let this blest assurance control,
That Christ hath regarded my helpless estate,
And hath shed His own blood for my soul.
It is well with my soul...

My sin—oh, the bliss of this glorious thought!—
My sin, not in part but the whole,
Is nailed to the cross, and I bear it no more,
Praise the Lord, praise the Lord, O my soul!
It is well with my soul...

And Lord, haste the day when the faith shall be sight,
The clouds be rolled back as a scroll;
The trump shall resound, and the Lord shall descend,
Even so, it is well with my soul.
It is well with my soul...""",
    ),
    H(
        "주의 일 위해",
        "Work, for the Night Is Coming",
        "Anna L. Coghill",
        "Lowell Mason",
        "1854",
        "헌신",
        "안나 L. 코길 작사, 로웰 메이슨 작곡. 부지런한 사역을 권면합니다. PD.",
        """주의 일 힘써 하라 밤이 오리라
낮이 있을 때 일하라 밤이 오리라
봄날에 씨 뿌리며 여름에 가꾸고
가을에 거두리라 밤이 오리라

젊을 때 힘써 하라 밤이 오리라
힘이 있을 때 일하라 밤이 오리라
늦은 때 이르기 전 주의 일 하라
열매 거두리라 밤이 오리라""",
        """Work, for the night is coming,
Work through the morning hours;
Work while the dew is sparkling,
Work 'mid springing flowers.
Work when the day grows brighter,
Work in the glowing sun;
Work, for the night is coming,
When man's work is done.

Work, for the night is coming,
Work through the sunny noon;
Fill brightest hours with labor,
Rest comes sure and soon.
Give every flying minute
Something to keep in store;
Work, for the night is coming,
When man works no more.

Work, for the night is coming,
Under the sunset skies;
While their bright tints are glowing,
Work, for daylight flies.
Work till the last beam fadeth,
Fadeth to shine no more;
Work, while the night is darkening,
When man's work is o'er.""",
    ),
    H(
        "주님 다시 오실 때",
        "What If It Were Today?",
        "Lelia N. Morris",
        "Lelia N. Morris",
        "1912",
        "소망",
        "렐리아 N. 모리스 작사·작곡(1912). 미국 PD. 재림의 소망을 일깨웁니다.",
        """예수 다시 오실 그 날이
오늘일지도 모르네
준비된 마음으로 기다리세
주 오실 그 날을
주 오실 때 주 오실 때
영광 중에 주를 뵙겠네
주 오실 때 주 오실 때
할렐루야 주를 찬양하리

세상의 유혹 물리치고
거룩하게 살아가세
신랑 되신 주 맞이할 때
기쁨 넘치리
주 오실 때 주 오실 때
영광 중에 주를 뵙겠네""",
        """Jesus is coming to earth again;
What if it were today?
Coming in power and love to reign;
What if it were today?
Coming to claim His chosen Bride,
All the redeemed and purified,
Over this whole earth scattered wide;
What if it were today?
Glory, glory! Joy to my heart 'twill bring.
Glory, glory! When we shall crown Him King.
Glory, glory! Haste to prepare the way;
Glory, glory! Jesus will come some day.

Satan's dominion will then be o'er,
O that it were today!
Sorrow and sighing shall be no more,
O that it were today!
Then shall the dead in Christ arise,
Caught up to meet Him in the skies,
When shall these glories meet our eyes?
What if it were today?
Glory, glory!...""",
        license_note=(
            "미국 Public Domain(1912년 출판). 개인 예배·교육 무료. "
            "한국찬송가공회 공식 판본과 무관."
        ),
    ),
    H(
        "주 나의 피난처",
        "A Shelter in the Time of Storm",
        "Vernon J. Charlesworth",
        "Ira D. Sankey",
        "1880",
        "신뢰",
        "버논 J. 찰스워스 작사, 아이라 D. 생키 작곡/편곡으로 널리 알려짐. PD.",
        """주 나의 피난처 되시니
폭풍 중에 숨으리
견고한 반석 되신 주
나를 지키시네
오 주 예수 피난처
오 주 예수 피난처
환난 날에 숨으리
주 나의 피난처

물결이 노도처럼 일 때
주가 나를 붙드시네
안전한 항구 되신 주
나를 인도하시네
오 주 예수 피난처
오 주 예수 피난처
환난 날에 숨으리
주 나의 피난처""",
        """The Lord's our Rock, in Him we hide,
A shelter in the time of storm;
Secure whatever ill betide,
A shelter in the time of storm.
Oh, Jesus is a Rock in a weary land,
A weary land, a weary land;
Oh, Jesus is a Rock in a weary land,
A shelter in the time of storm.

A shade by day, defense by night,
A shelter in the time of storm;
No fears alarm, no foes afright,
A shelter in the time of storm.
Oh, Jesus is a Rock...

The raging storms may round us beat,
A shelter in the time of storm;
We'll never leave our safe retreat,
A shelter in the time of storm.
Oh, Jesus is a Rock...""",
    ),
    H(
        "주 예수 내 생명",
        "I Love to Tell the Story",
        "A. Katherine Hankey",
        "William G. Fischer",
        "1866",
        "복음",
        "아라벨라 캐서린 행키(A. Katherine Hankey) 작사, 윌리엄 G. 피셔 작곡. PD.",
        """주 예수 귀한 말씀 전하기 좋아라
나를 구원하신 그 사랑 이야기
주 예수 귀한 말씀 전하기 좋아라
하늘 가서도 그 말씀 전하리
주 예수 귀한 말씀 전하기 좋아라
나를 구원하신 그 사랑 이야기

처음 들었을 때 기쁨 넘쳤고
들을수록 더 귀하여라
주 예수 귀한 말씀 전하기 좋아라
나를 구원하신 그 사랑 이야기
주 예수 귀한 말씀 전하기 좋아라
하늘 가서도 그 말씀 전하리""",
        """I love to tell the story
Of unseen things above,
Of Jesus and His glory,
Of Jesus and His love.
I love to tell the story,
Because I know 'tis true;
It satisfies my longings
As nothing else can do.
I love to tell the story,
'Twill be my theme in glory,
To tell the old, old story
Of Jesus and His love.

I love to tell the story;
More wonderful it seems
Than all the golden fancies
Of all our golden dreams.
I love to tell the story,
It did so much for me;
And that is just the reason
I tell it now to thee.
I love to tell the story...

I love to tell the story;
'Tis pleasant to repeat
What seems, each time I tell it,
More wonderfully sweet.
I love to tell the story,
For some have never heard
The message of salvation
From God's own holy Word.
I love to tell the story...""",
    ),
]


def dedupe_by_title_en(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for h in items:
        author = (h.get("author") or "").upper()
        if author.startswith("SKIP") or (h.get("composer") or "").upper() == "SKIP":
            continue
        if (h.get("lyrics_en") or "").strip() in ("", "x"):
            continue
        key = (h.get("title_en") or h.get("title") or "").strip().lower()
        # normalize alt titles that are duplicates
        key = key.replace(" (alt)", "").replace(" (alt title)", "").strip()
        if "already have" in key or key.startswith("skip"):
            continue
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out


def main() -> None:
    catalog = dedupe_by_title_en(CATALOG)
    hymns = []
    for i, raw in enumerate(catalog, start=1):
        ko = raw.get("lyrics_ko") or ""
        en = raw.get("lyrics_en") or ""
        primary = ko if ko else en
        hymns.append(
            {
                "id": i,
                "number": str(i),
                "title": raw["title"],
                "title_en": raw["title_en"],
                "lyrics": primary,
                "lyrics_ko": ko,
                "lyrics_en": en,
                "author": raw.get("author") or "",
                "composer": raw.get("composer") or "",
                "year": str(raw.get("year") or ""),
                "category": raw.get("category") or "일반",
                "history": raw.get("history") or "",
                "license": raw.get("license") or PD_LICENSE,
                "license_note": raw.get("license_note") or PD_NOTE,
                "source": raw.get("source") or SOURCE_DEFAULT,
                "scoreImage": f"assets/images/hymns/score_{i}.svg",
            }
        )

    payload = {
        "source_note": (
            "모든 수록 찬송은 Public Domain(저작권 만료·자유 이용)으로 검증·선별했습니다. "
            "라이선스 비용·이용 제한 없이 개인 예배·교육·오프라인 앱에서 무료로 사용할 수 있습니다. "
            "미국 기준 고전 PD 레퍼토리(대체로 1930년 이전 출판 또는 동등 조건)입니다. "
            "한국찬송가공회 공식 판권 악보·가사와 무관하며 제휴·인가 관계가 없습니다. "
            "제외 예: How Great Thou Art 영어(Stuart K. Hine, 1949), "
            "They Will Know We Are Christians(1966) 등 비-PD 작품."
        ),
        "license_summary": PD_NOTE,
        "score_note": (
            "악보는 교육용으로 생성된 간소화 PD 스타일 오선 SVG입니다. "
            "공식 한국찬송가공회 악보가 아닙니다."
        ),
        "last_updated": datetime.date.today().isoformat(),
        "count": len(hymns),
        "verification": {
            "policy": "US public domain preference (pre-1930 publication / classic PD corpus)",
            "excluded_examples": [
                "How Great Thou Art (English tr. Stuart K. Hine, 1949) — not PD",
                "They Will Know We Are Christians by Our Love (1966) — not PD",
            ],
            "reference_sites": [
                "https://hymnary.org",
                "https://www.pdinfo.com",
                "https://hymnstogod.org/Hymns-PD/",
            ],
        },
        "hymns": hymns,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    with_ko = sum(1 for h in hymns if h["lyrics_ko"])
    with_en = sum(1 for h in hymns if h["lyrics_en"])
    print(f"Wrote {len(hymns)} PD hymns -> {OUT}")
    print(f"  with Korean lyrics: {with_ko}")
    print(f"  with English lyrics: {with_en}")
    print("Next: python scripts/generate_hymn_scores.py")


if __name__ == "__main__":
    main()
