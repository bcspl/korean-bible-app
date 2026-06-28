import 'package:hive/hive.dart';

part 'bible_bookmark.g.dart';

@HiveType(typeId: 3)
class BibleBookmark {
  @HiveField(0)
  final int bookIndex;

  @HiveField(1)
  final int chapterIndex;

  @HiveField(2)
  final int? verseIndex; // null이면 장 전체 북마크

  @HiveField(3)
  final String snippet; // 미리보기용 (절 텍스트 또는 장 제목)

  @HiveField(4)
  final DateTime createdAt;

  BibleBookmark({
    required this.bookIndex,
    required this.chapterIndex,
    this.verseIndex,
    required this.snippet,
    required this.createdAt,
  });

  bool get isVerseBookmark => verseIndex != null;

  factory BibleBookmark.fromJson(Map<String, dynamic> json) {
    return BibleBookmark(
      bookIndex: json['bookIndex'] as int,
      chapterIndex: json['chapterIndex'] as int,
      verseIndex: json['verseIndex'] as int?,
      snippet: json['snippet'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
        'bookIndex': bookIndex,
        'chapterIndex': chapterIndex,
        'verseIndex': verseIndex,
        'snippet': snippet,
        'createdAt': createdAt.toIso8601String(),
      };
}
