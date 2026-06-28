class Hymn {
  final int id;
  final String number;
  final String title;
  final String lyrics;
  final String scoreImage;
  final String category;

  Hymn({
    required this.id,
    required this.number,
    required this.title,
    required this.lyrics,
    required this.scoreImage,
    required this.category,
  });

  factory Hymn.fromJson(Map<String, dynamic> json) {
    return Hymn(
      id: json['id'] as int,
      number: json['number'] as String,
      title: json['title'] as String,
      lyrics: json['lyrics'] as String,
      scoreImage: json['scoreImage'] as String,
      category: json['category'] as String,
    );
  }
}
