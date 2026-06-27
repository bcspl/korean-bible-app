import 'package:hive/hive.dart';

import 'bible_verse.dart';

part 'bible_chapter.g.dart';

@HiveType(typeId: 1)
class BibleChapter {
  @HiveField(0)
  final int chapter;

  @HiveField(1)
  final List<BibleVerse> verses;

  BibleChapter({
    required this.chapter,
    required this.verses,
  });

  factory BibleChapter.fromJson(Map<String, dynamic> json) {
    return BibleChapter(
      chapter: json['chapter'] as int,
      verses: (json['verses'] as List)
          .map((v) => BibleVerse.fromJson(v as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() => {
        'chapter': chapter,
        'verses': verses.map((v) => v.toJson()).toList(),
      };
}
