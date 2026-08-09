import 'dart:convert';
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';

import '../models/bible_book.dart';
import '../models/bible_version.dart';

class BibleDataService {
  static const String _dataBoxName = 'bible_data';
  static const String _booksKey = 'books';
  static const String _versionKey = 'version';
  static const String _revisionKey = 'data_revision';

  /// Primary Korean PD text (개역한글 / KRV).
  static const String expectedVersion = '개역한글 (KRV)';

  /// Bump when kor_bible_full.json content is replaced with a verified dump.
  static const String expectedDataRevision = '2026-08-10-holybible-pd';

  static String currentVersion = expectedVersion;

  /// In-memory caches for all PD versions (book key -> BibleBook).
  static final Map<BibleVersionId, Map<String, BibleBook>> _versionMaps = {};
  static final Map<BibleVersionId, List<BibleBook>> _versionLists = {};
  static final Map<BibleVersionId, String> _versionLabels = {};

  /// Robust open that recovers from stale lock files.
  Future<Box> _openBoxSafely(String name) async {
    for (int attempt = 0; attempt < 3; attempt++) {
      try {
        return await Hive.openBox(name);
      } on PathAccessException catch (e) {
        final msg = e.toString().toLowerCase();
        if (msg.contains('lock') && attempt < 2) {
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
      } catch (_) {}
    }
  }

  bool _needsReseed(
    List? existing,
    String? storedVersion,
    String? storedRevision,
  ) {
    if (existing == null || existing.isEmpty) return true;
    if (storedVersion == null || storedVersion.trim().isEmpty) return true;
    if (storedRevision != expectedDataRevision) return true;
    final v = storedVersion;
    if (v.contains('개역개정') || v.toUpperCase().contains('NKRV')) return true;
    if (v.contains('개역한글') || v.toUpperCase().contains('KRV')) return false;
    return v != expectedVersion;
  }

  Future<List<BibleBook>> _loadVersionFromAsset(BibleVersionId id) async {
    if (_versionLists.containsKey(id)) {
      return _versionLists[id]!;
    }
    final jsonString = await rootBundle.loadString(id.assetPath);
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
    final label = jsonMap['version'] as String? ?? id.fullLabel;
    _versionLabels[id] = label;
    final booksJson = jsonMap['books'] as List<dynamic>? ?? [];
    final books = booksJson
        .map((b) => BibleBook.fromJson(b as Map<String, dynamic>))
        .toList();
    final map = <String, BibleBook>{};
    for (final b in books) {
      map[b.book] = b;
    }
    _versionMaps[id] = map;
    _versionLists[id] = books;
    return books;
  }

  /// Ensure KRV + KJV + ASV are loaded into memory.
  Future<void> loadAllVersions() async {
    await Future.wait([
      _loadVersionFromAsset(BibleVersionId.krv),
      _loadVersionFromAsset(BibleVersionId.kjv),
      _loadVersionFromAsset(BibleVersionId.asv),
    ]);
  }

  String labelFor(BibleVersionId id) =>
      _versionLabels[id] ?? id.fullLabel;

  List<BibleBook> booksFor(BibleVersionId id) =>
      List.unmodifiable(_versionLists[id] ?? const []);

  /// Verse text for a version by canonical book key, 1-based chapter & verse.
  String? verseText(
    BibleVersionId id,
    String bookKey,
    int chapter,
    int verse,
  ) {
    final book = _versionMaps[id]?[bookKey];
    if (book == null) return null;
    for (final ch in book.chapters) {
      if (ch.chapter == chapter) {
        for (final v in ch.verses) {
          if (v.verse == verse) return v.text;
        }
      }
    }
    return null;
  }

  /// All verse numbers present in any selected version for chapter.
  List<int> verseNumbers(
    String bookKey,
    int chapter, {
    List<BibleVersionId> versions = const [
      BibleVersionId.krv,
      BibleVersionId.kjv,
      BibleVersionId.asv,
    ],
  }) {
    final set = <int>{};
    for (final id in versions) {
      final book = _versionMaps[id]?[bookKey];
      if (book == null) continue;
      for (final ch in book.chapters) {
        if (ch.chapter == chapter) {
          for (final v in ch.verses) {
            set.add(v.verse);
          }
        }
      }
    }
    final list = set.toList()..sort();
    return list;
  }

  Future<List<BibleBook>> loadAndSeedBibleData() async {
    await loadAllVersions();
    final box = await _openBoxSafely(_dataBoxName);

    final existing = box.get(_booksKey) as List?;
    final storedVersion = box.get(_versionKey) as String?;
    final storedRevision = box.get(_revisionKey) as String?;

    if (!_needsReseed(existing, storedVersion, storedRevision)) {
      BibleDataService.currentVersion = storedVersion ?? expectedVersion;
      return existing!.cast<BibleBook>();
    }

    // Always prefer fresh asset for KRV after revision bumps
    await _loadVersionFromAsset(BibleVersionId.krv);
    final books = List<BibleBook>.from(booksFor(BibleVersionId.krv));
    BibleDataService.currentVersion = expectedVersion;
    await box.put(_booksKey, books);
    await box.put(_versionKey, currentVersion);
    await box.put(_revisionKey, expectedDataRevision);
    return books;
  }

  Future<List<BibleBook>> getBooks() async {
    await loadAllVersions();
    final box = await _openBoxSafely(_dataBoxName);
    BibleDataService.currentVersion =
        box.get(_versionKey) as String? ?? expectedVersion;
    final books = box.get(_booksKey) as List?;
    if (books != null && books.isNotEmpty) {
      return books.cast<BibleBook>();
    }
    return booksFor(BibleVersionId.krv);
  }

  Future<List<BibleBook>> loadSampleData() async {
    final jsonString =
        await rootBundle.loadString('assets/data/kor_bible_sample.json');
    final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
    final booksJson = jsonMap['books'] as List<dynamic>;
    return booksJson
        .map((bookJson) => BibleBook.fromJson(bookJson as Map<String, dynamic>))
        .toList();
  }
}
