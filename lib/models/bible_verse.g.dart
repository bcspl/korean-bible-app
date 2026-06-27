// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'bible_verse.dart';

// **************************************************************************
// TypeAdapterGenerator
// **************************************************************************

class BibleVerseAdapter extends TypeAdapter<BibleVerse> {
  @override
  final int typeId = 0;

  @override
  BibleVerse read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return BibleVerse(
      verse: fields[0] as int,
      text: fields[1] as String,
    );
  }

  @override
  void write(BinaryWriter writer, BibleVerse obj) {
    writer
      ..writeByte(2)
      ..writeByte(0)
      ..write(obj.verse)
      ..writeByte(1)
      ..write(obj.text);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is BibleVerseAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
