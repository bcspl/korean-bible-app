import 'package:hive/hive.dart';

import 'bible_chapter.dart';

part 'bible_book.g.dart';

@HiveType(typeId: 2)
class BibleBook {
  @HiveField(0)
  final String book;

  @HiveField(1)
  final List<BibleChapter> chapters;

  BibleBook({
    required this.book,
    required this.chapters,
  });

  factory BibleBook.fromJson(Map<String, dynamic> json) {
    return BibleBook(
      book: json['book'] as String,
      chapters: (json['chapters'] as List)
          .map((c) => BibleChapter.fromJson(c as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() => {
        'book': book,
        'chapters': chapters.map((c) => c.toJson()).toList(),
      };
}
