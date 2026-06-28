// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'bible_bookmark.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class BibleBookmarkAdapter extends TypeAdapter<BibleBookmark> {
  @override
  final int typeId = 3;

  @override
  BibleBookmark read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return BibleBookmark(
      bookIndex: fields[0] as int,
      chapterIndex: fields[1] as int,
      verseIndex: fields[2] as int?,
      snippet: fields[3] as String,
      createdAt: fields[4] as DateTime,
    );
  }

  @override
  void write(BinaryWriter writer, BibleBookmark obj) {
    writer
      ..writeByte(5)
      ..writeByte(0)
      ..write(obj.bookIndex)
      ..writeByte(1)
      ..write(obj.chapterIndex)
      ..writeByte(2)
      ..write(obj.verseIndex)
      ..writeByte(3)
      ..write(obj.snippet)
      ..writeByte(4)
      ..write(obj.createdAt);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is BibleBookmarkAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
