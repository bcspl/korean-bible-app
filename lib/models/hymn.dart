class Hymn {
  final int id;
  final String number;
  final String title;
  final String? titleEn;
  final String lyrics;
  final String scoreImage;
  final String category;
  final String? author;
  final String? composer;
  final String? year;
  final String? source; // e.g. "Hymnary.org - Public Domain"

  Hymn({
    required this.id,
    required this.number,
    required this.title,
    this.titleEn,
    required this.lyrics,
    required this.scoreImage,
    required this.category,
    this.author,
    this.composer,
    this.year,
    this.source,
  });

  factory Hymn.fromJson(Map<String, dynamic> json) {
    return Hymn(
      id: json['id'] as int,
      number: json['number']?.toString() ?? '',
      title: json['title'] as String? ?? '',
      titleEn: json['title_en'] as String?,
      lyrics: json['lyrics'] as String? ?? '',
      scoreImage: json['scoreImage'] as String? ?? '',
      category: json['category'] as String? ?? '일반',
      author: json['author'] as String?,
      composer: json['composer'] as String?,
      year: json['year']?.toString(),
      source: json['source'] as String?,
    );
  }
}
