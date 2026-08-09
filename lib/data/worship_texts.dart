import '../models/bible_version.dart';

/// Curated worship texts (Public Domain).
///
/// Lord's Prayer: **prayer body only** — narrative frames from Matt 6
/// (e.g. "After this manner therefore pray ye", "그러므로 너희는 이렇게 기도하라")
/// are intentionally stripped. Wording follows each version's Matt 6:9–13.
class WorshipTexts {
  WorshipTexts._();

  // ---------------------------------------------------------------------------
  // 주기도문 (Lord's Prayer) — prayer only
  // ---------------------------------------------------------------------------

  /// 개역한글 — Matt 6:9–13 기도 본문 (서사 제외) + 전통 송영.
  static const String lordsPrayerKrv = '''하늘에 계신 우리 아버지여
이름이 거룩히 여김을 받으시오며
나라이 임하옵시며
뜻이 하늘에서 이룬 것 같이
땅에서도 이루어지이다

오늘날 우리에게 일용할 양식을 주옵시고
우리가 우리에게 죄 지은 자를 사하여 준 것 같이
우리 죄를 사하여 주옵시고
우리를 시험에 들게 하지 마옵시고
다만 악에서 구하옵소서

나라와 권세와 영광이 아버지께 영원히 있사옵나이다
아멘.''';

  /// KJV — Matt 6:9–13 prayer only (no "After this manner therefore pray ye").
  static const String lordsPrayerKjv = '''Our Father which art in heaven,
Hallowed be thy name.
Thy kingdom come.
Thy will be done in earth, as it is in heaven.
Give us this day our daily bread.
And forgive us our debts, as we forgive our debtors.
And lead us not into temptation, but deliver us from evil:
For thine is the kingdom, and the power, and the glory, for ever.
Amen.''';

  /// ASV 1901 — Matt 6:9–13 prayer only (no narrative frame).
  /// Note: ASV v.13 has no longer doxology in the Greek-critical tradition;
  /// text matches ASV scripture prayer clauses.
  static const String lordsPrayerAsv = '''Our Father who art in heaven,
Hallowed be thy name.
Thy kingdom come.
Thy will be done, as in heaven, so on earth.
Give us this day our daily bread.
And forgive us our debts, as we also have forgiven our debtors.
And bring us not into temptation, but deliver us from the evil one.
Amen.''';

  static String lordsPrayer(BibleVersionId id) {
    switch (id) {
      case BibleVersionId.krv:
        return lordsPrayerKrv;
      case BibleVersionId.kjv:
        return lordsPrayerKjv;
      case BibleVersionId.asv:
        return lordsPrayerAsv;
    }
  }

  static String lordsPrayerCaption(BibleVersionId id) {
    switch (id) {
      case BibleVersionId.krv:
        return '개역한글 · 마 6:9–13 기도 본문만 · Public Domain';
      case BibleVersionId.kjv:
        return 'KJV · Matthew 6:9–13 prayer only · Public Domain';
      case BibleVersionId.asv:
        return 'ASV (1901) · Matthew 6:9–13 prayer only · Public Domain';
    }
  }

  // ---------------------------------------------------------------------------
  // 사도신경 (Apostles' Creed)
  // ---------------------------------------------------------------------------

  /// 개역한글 전통 문안 (한국 교회 통용 개역한글 계열).
  static const String creedKrv = '''전능하사 천지를 만드신 하나님 아버지를 내가 믿사오며,
그 외아들 우리 주 예수 그리스도를 믿사오니,
이는 성령으로 잉태하사 동정녀 마리아에게 나시고,
본디오 빌라도에게 고난을 받으사 십자가에 못 박혀 죽으시고,
장사한 지 사흘 만에 죽은 자 가운데서 다시 살아나시며,
하늘에 오르사 전능하신 하나님 우편에 앉아 계시다가,
저리로서 산 자와 죽은 자를 심판하러 오시리라.
성령을 믿사오며, 거룩한 공회와 성도가 서로 교통하는 것과,
죄를 사하여 주시는 것과, 몸이 다시 사는 것과,
영원히 사는 것을 믿사옵나이다. 아멘.''';

  /// Traditional English Apostles' Creed (PD liturgy; KJV-era English).
  static const String creedKjv = '''I believe in God the Father Almighty,
Maker of heaven and earth:

And in Jesus Christ his only Son our Lord,
Who was conceived by the Holy Ghost,
Born of the Virgin Mary,
Suffered under Pontius Pilate,
Was crucified, dead, and buried;
He descended into hell;
The third day he rose again from the dead;
He ascended into heaven,
And sitteth on the right hand of God the Father Almighty;
From thence he shall come to judge the quick and the dead.

I believe in the Holy Ghost;
The holy Catholic Church;
The Communion of Saints;
The Forgiveness of sins;
The Resurrection of the body,
And the Life everlasting. Amen.''';

  /// ASV-era English liturgy: same creed; "Holy Spirit" preferred in some
  /// 20c printings — we keep classical PD form with ASV-adjacent wording
  /// where it differs only in minor orthography (who/which already in creed).
  static const String creedAsv = '''I believe in God the Father Almighty,
Maker of heaven and earth:

And in Jesus Christ his only Son our Lord,
Who was conceived by the Holy Spirit,
Born of the Virgin Mary,
Suffered under Pontius Pilate,
Was crucified, dead, and buried;
He descended into hell;
The third day he rose again from the dead;
He ascended into heaven,
And sitteth on the right hand of God the Father Almighty;
From thence he shall come to judge the quick and the dead.

I believe in the Holy Spirit;
The holy Catholic Church;
The Communion of Saints;
The Forgiveness of sins;
The Resurrection of the body,
And the Life everlasting. Amen.''';

  static String creed(BibleVersionId id) {
    switch (id) {
      case BibleVersionId.krv:
        return creedKrv;
      case BibleVersionId.kjv:
        return creedKjv;
      case BibleVersionId.asv:
        return creedAsv;
    }
  }

  static String creedCaption(BibleVersionId id) {
    switch (id) {
      case BibleVersionId.krv:
        return '개역한글 전통 사도신경 · Public Domain';
      case BibleVersionId.kjv:
        return 'English Apostles\' Creed (KJV-era) · Public Domain';
      case BibleVersionId.asv:
        return 'English Apostles\' Creed (ASV-era wording) · Public Domain';
    }
  }
}
