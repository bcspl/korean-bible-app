import 'package:hive/hive.dart';

part 'bible_verse.g.dart';

@HiveType(typeId: 0)
class BibleVerse {
  @HiveField(0)
  final int verse;

  @HiveField(1)
  final String text;

  BibleVerse({
    required this.verse,
    required this.text,
  });

  factory BibleVerse.fromJson(Map<String, dynamic> json) {
    return BibleVerse(
      verse: json['verse'] as int,
      text: json['text'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
        'verse': verse,
        'text': text,
      };
}
