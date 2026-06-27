// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'bible_chapter.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class BibleChapterAdapter extends TypeAdapter<BibleChapter> {
  @override
  final int typeId = 1;

  @override
  BibleChapter read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return BibleChapter(
      chapter: fields[0] as int,
      verses: (fields[1] as List).cast<BibleVerse>(),
    );
  }

  @override
  void write(BinaryWriter writer, BibleChapter obj) {
    writer
      ..writeByte(2)
      ..writeByte(0)
      ..write(obj.chapter)
      ..writeByte(1)
      ..write(obj.verses);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is BibleChapterAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
