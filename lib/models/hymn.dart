class Hymn {
  final int id;
  final String number;
  final String title;
  final String? titleEn;
  final String lyrics;
  final String? lyricsKo;
  final String? lyricsEn;
  final String scoreImage;
  final String category;
  final String? author;
  final String? composer;
  final String? year;
  final String? source; // e.g. "Hymnary.org - Public Domain"
  final String? history;
  final String? license;
  final String? licenseNote;

  Hymn({
    required this.id,
    required this.number,
    required this.title,
    this.titleEn,
    required this.lyrics,
    this.lyricsKo,
    this.lyricsEn,
    required this.scoreImage,
    required this.category,
    this.author,
    this.composer,
    this.year,
    this.source,
    this.history,
    this.license,
    this.licenseNote,
  });

  /// Korean lyrics if present, else primary [lyrics].
  String get displayLyricsKo {
    final ko = lyricsKo?.trim();
    if (ko != null && ko.isNotEmpty) return ko;
    return lyrics;
  }

  /// English lyrics if present.
  String get displayLyricsEn {
    final en = lyricsEn?.trim();
    if (en != null && en.isNotEmpty) return en;
    return '';
  }

  bool get hasEnglishLyrics => displayLyricsEn.isNotEmpty;
  bool get hasKoreanLyrics {
    final ko = lyricsKo?.trim();
    if (ko != null && ko.isNotEmpty) return true;
    // Primary field often holds Korean in older data
    return lyrics.trim().isNotEmpty;
  }

  bool get isPublicDomain {
    final lic = (license ?? source ?? '').toLowerCase();
    return lic.contains('public domain') ||
        lic.contains('pd') ||
        (license ?? '').contains('Public Domain');
  }

  factory Hymn.fromJson(Map<String, dynamic> json) {
    return Hymn(
      id: json['id'] as int,
      number: json['number']?.toString() ?? '',
      title: json['title'] as String? ?? '',
      titleEn: json['title_en'] as String?,
      lyrics: json['lyrics'] as String? ?? '',
      lyricsKo: json['lyrics_ko'] as String?,
      lyricsEn: json['lyrics_en'] as String?,
      scoreImage: json['scoreImage'] as String? ?? '',
      category: json['category'] as String? ?? '일반',
      author: json['author'] as String?,
      composer: json['composer'] as String?,
      year: json['year']?.toString(),
      source: json['source'] as String?,
      history: json['history'] as String?,
      license: json['license'] as String?,
      licenseNote: json['license_note'] as String?,
    );
  }
}
