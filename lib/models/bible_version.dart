/// Public Domain Bible versions available offline in this app.
enum BibleVersionId {
  krv,
  kjv,
  asv,
}

extension BibleVersionIdX on BibleVersionId {
  String get code {
    switch (this) {
      case BibleVersionId.krv:
        return 'KRV';
      case BibleVersionId.kjv:
        return 'KJV';
      case BibleVersionId.asv:
        return 'ASV';
    }
  }

  String get shortLabel {
    switch (this) {
      case BibleVersionId.krv:
        return '개역한글';
      case BibleVersionId.kjv:
        return 'KJV';
      case BibleVersionId.asv:
        return 'ASV';
    }
  }

  String get fullLabel {
    switch (this) {
      case BibleVersionId.krv:
        return '개역한글 (KRV)';
      case BibleVersionId.kjv:
        return 'KJV (King James)';
      case BibleVersionId.asv:
        return 'ASV (1901)';
    }
  }

  /// Asset path for full Bible JSON.
  String get assetPath {
    switch (this) {
      case BibleVersionId.krv:
        return 'assets/data/kor_bible_full.json';
      case BibleVersionId.kjv:
        return 'assets/data/eng_kjv_full.json';
      case BibleVersionId.asv:
        return 'assets/data/eng_asv_full.json';
    }
  }

  bool get isKorean => this == BibleVersionId.krv;

  static BibleVersionId? fromCode(String? code) {
    if (code == null) return null;
    final c = code.toUpperCase();
    for (final v in BibleVersionId.values) {
      if (v.code == c) return v;
    }
    return null;
  }
}
