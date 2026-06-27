import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../models/bible_book.dart';

class BibleDataService {
  static const String _dataBoxName = 'bible_data';
  static const String _booksKey = 'books';
  static const String _versionKey = 'version';

  String currentVersion = '개역개정';

  /// Loads Bible data from assets JSON and seeds Hive if empty.
  Future<List<BibleBook>> loadAndSeedBibleData() async {
    final box = await Hive.openBox(_dataBoxName);

    // Check if already seeded
    final existing = box.get(_booksKey) as List?;
    if (existing != null && existing.isNotEmpty) {
      currentVersion = box.get(_versionKey) as String? ?? '개역개정';
      // Return from Hive (cast properly)
      return existing.cast<BibleBook>();
    }

    // Load from assets
    final jsonString = await rootBundle.loadString('assets/data/kor_bible_full.json');
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;

    currentVersion = jsonMap['version'] as String? ?? '개역개정';
    final booksJson = jsonMap['books'] as List<dynamic>;
    final books = booksJson
        .map((bookJson) => BibleBook.fromJson(bookJson as Map<String, dynamic>))
        .toList();

    // Seed to Hive
    await box.put(_booksKey, books);
    await box.put(_versionKey, currentVersion);

    return books;
  }

  /// Get books from Hive (assumes already loaded)
  Future<List<BibleBook>> getBooks() async {
    final box = await Hive.openBox(_dataBoxName);
    currentVersion = box.get(_versionKey) as String? ?? '개역개정';
    final books = box.get(_booksKey) as List?;
    return books?.cast<BibleBook>() ?? [];
  }

  /// For testing with sample data
  Future<List<BibleBook>> loadSampleData() async {
    final jsonString = await rootBundle.loadString('assets/data/kor_bible_sample.json');
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
    final booksJson = jsonMap['books'] as List<dynamic>;
    return booksJson
        .map((bookJson) => BibleBook.fromJson(bookJson as Map<String, dynamic>))
        .toList();
  }
}
