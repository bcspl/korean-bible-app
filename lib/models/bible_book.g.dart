// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'bible_book.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class BibleBookAdapter extends TypeAdapter<BibleBook> {
  @override
  final int typeId = 2;

  @override
  BibleBook read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return BibleBook(
      book: fields[0] as String,
      chapters: (fields[1] as List).cast<BibleChapter>(),
    );
  }

  @override
  void write(BinaryWriter writer, BibleBook obj) {
    writer
      ..writeByte(2)
      ..writeByte(0)
      ..write(obj.book)
      ..writeByte(1)
      ..write(obj.chapters);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is BibleBookAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
