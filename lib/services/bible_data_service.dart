import 'dart:convert';
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';

import '../models/bible_book.dart';

class BibleDataService {
  static const String _dataBoxName = 'bible_data';
  static const String _booksKey = 'books';
  static const String _versionKey = 'version';

  static String currentVersion = '개역개정';

  /// Robust open that recovers from stale lock files (common on desktop when previous runs were killed).
  Future<Box> _openBoxSafely(String name) async {
    for (int attempt = 0; attempt < 3; attempt++) {
      try {
        return await Hive.openBox(name);
      } on PathAccessException catch (e) {
        final msg = e.toString().toLowerCase();
        if (msg.contains('lock') && attempt < 2) {
          // Try to release local box and delete stale lock files (Documents + support dir)
          try {
            if (Hive.isBoxOpen(name)) {
              await Hive.box(name).close();
            }
          } catch (_) {}

          await _deleteLockIfStale(name);

          await Future.delayed(const Duration(milliseconds: 150));
          continue;
        }
        rethrow;
      } catch (e) {
        final msg = e.toString().toLowerCase();
        if ((msg.contains('lock') || msg.contains('access')) && attempt < 2) {
          await _deleteLockIfStale(name);
          await Future.delayed(const Duration(milliseconds: 250));
          continue;
        }
        rethrow;
      }
    }
    // Last attempt
    return await Hive.openBox(name);
  }

  Future<void> _deleteLockIfStale(String boxName) async {
    for (final futureDir in [
      getApplicationDocumentsDirectory(),
      getApplicationSupportDirectory(),
    ]) {
      try {
        final dir = await futureDir;
        final lockFile = File('${dir.path}/$boxName.lock');
        if (await lockFile.exists()) {
          await lockFile.delete();
        }
      } catch (_) {
        // ignore - another process may still hold it or path issue
      }
    }
  }

  /// Loads Bible data from assets JSON and seeds Hive if empty.
  Future<List<BibleBook>> loadAndSeedBibleData() async {
    final box = await _openBoxSafely(_dataBoxName);

    // Check if already seeded
    final existing = box.get(_booksKey) as List?;
    if (existing != null && existing.isNotEmpty) {
      BibleDataService.currentVersion = box.get(_versionKey) as String? ?? '개역개정';
      // Return from Hive (cast properly)
      return existing.cast<BibleBook>();
    }

    // Load from assets
    final jsonString = await rootBundle.loadString('assets/data/kor_bible_full.json');
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;

    BibleDataService.currentVersion = jsonMap['version'] as String? ?? '개역개정';
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
    final box = await _openBoxSafely(_dataBoxName);
    BibleDataService.currentVersion = box.get(_versionKey) as String? ?? '개역개정';
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
