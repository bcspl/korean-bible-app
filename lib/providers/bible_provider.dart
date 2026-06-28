import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../models/bible_book.dart';
import '../models/bible_bookmark.dart';
import '../models/hymn.dart';
import '../services/bible_data_service.dart';

// Full Bible book names mapping (key from JSON -> Korean, English full)
const Map<String, Map<String, String>> _bibleBookNames = {
  'Gen': {'korean': '창세기', 'english': 'Genesis'},
  'Exod': {'korean': '출애굽기', 'english': 'Exodus'},
  'Lev': {'korean': '레위기', 'english': 'Leviticus'},
  'Num': {'korean': '민수기', 'english': 'Numbers'},
  'Deut': {'korean': '신명기', 'english': 'Deuteronomy'},
  'Josh': {'korean': '여호수아', 'english': 'Joshua'},
  'Judg': {'korean': '사사기', 'english': 'Judges'},
  'Ruth': {'korean': '룻기', 'english': 'Ruth'},
  '1Sam': {'korean': '사무엘상', 'english': '1 Samuel'},
  '2Sam': {'korean': '사무엘하', 'english': '2 Samuel'},
  '1Kgs': {'korean': '열왕기상', 'english': '1 Kings'},
  '2Kgs': {'korean': '열왕기하', 'english': '2 Kings'},
  '1Chr': {'korean': '역대상', 'english': '1 Chronicles'},
  '2Chr': {'korean': '역대하', 'english': '2 Chronicles'},
  'Ezra': {'korean': '에스라', 'english': 'Ezra'},
  'Neh': {'korean': '느헤미야', 'english': 'Nehemiah'},
  'Esth': {'korean': '에스더', 'english': 'Esther'},
  'Job': {'korean': '욥기', 'english': 'Job'},
  'Ps': {'korean': '시편', 'english': 'Psalms'},
  'Prov': {'korean': '잠언', 'english': 'Proverbs'},
  'Eccl': {'korean': '전도서', 'english': 'Ecclesiastes'},
  'Song': {'korean': '아가', 'english': 'Song of Songs'},
  'Isa': {'korean': '이사야', 'english': 'Isaiah'},
  'Jer': {'korean': '예레미야', 'english': 'Jeremiah'},
  'Lam': {'korean': '예레미야 애가', 'english': 'Lamentations'},
  'Ezek': {'korean': '에스겔', 'english': 'Ezekiel'},
  'Dan': {'korean': '다니엘', 'english': 'Daniel'},
  'Hos': {'korean': '호세아', 'english': 'Hosea'},
  'Joel': {'korean': '요엘', 'english': 'Joel'},
  'Amos': {'korean': '아모스', 'english': 'Amos'},
  'Obad': {'korean': '오바댜', 'english': 'Obadiah'},
  'Jonah': {'korean': '요나', 'english': 'Jonah'},
  'Mic': {'korean': '미가', 'english': 'Micah'},
  'Nah': {'korean': '나훔', 'english': 'Nahum'},
  'Hab': {'korean': '하박국', 'english': 'Habakkuk'},
  'Zeph': {'korean': '스바냐', 'english': 'Zephaniah'},
  'Hag': {'korean': '학개', 'english': 'Haggai'},
  'Zech': {'korean': '스가랴', 'english': 'Zechariah'},
  'Mal': {'korean': '말라기', 'english': 'Malachi'},
  'Matt': {'korean': '마태복음', 'english': 'Matthew'},
  'Mark': {'korean': '마가복음', 'english': 'Mark'},
  'Luke': {'korean': '누가복음', 'english': 'Luke'},
  'John': {'korean': '요한복음', 'english': 'John'},
  'Acts': {'korean': '사도행전', 'english': 'Acts'},
  'Rom': {'korean': '로마서', 'english': 'Romans'},
  '1Cor': {'korean': '고린도전서', 'english': '1 Corinthians'},
  '2Cor': {'korean': '고린도후서', 'english': '2 Corinthians'},
  'Gal': {'korean': '갈라디아서', 'english': 'Galatians'},
  'Eph': {'korean': '에베소서', 'english': 'Ephesians'},
  'Phil': {'korean': '빌립보서', 'english': 'Philippians'},
  'Col': {'korean': '골로새서', 'english': 'Colossians'},
  '1Thess': {'korean': '데살로니가전서', 'english': '1 Thessalonians'},
  '2Thess': {'korean': '데살로니가후서', 'english': '2 Thessalonians'},
  '1Tim': {'korean': '디모데전서', 'english': '1 Timothy'},
  '2Tim': {'korean': '디모데후서', 'english': '2 Timothy'},
  'Titus': {'korean': '디도서', 'english': 'Titus'},
  'Phlm': {'korean': '빌레몬서', 'english': 'Philemon'},
  'Heb': {'korean': '히브리서', 'english': 'Hebrews'},
  'Jas': {'korean': '야고보서', 'english': 'James'},
  '1Pet': {'korean': '베드로전서', 'english': '1 Peter'},
  '2Pet': {'korean': '베드로후서', 'english': '2 Peter'},
  '1John': {'korean': '요한1서', 'english': '1 John'},
  '2John': {'korean': '요한2서', 'english': '2 John'},
  '3John': {'korean': '요한3서', 'english': '3 John'},
  'Jude': {'korean': '유다서', 'english': 'Jude'},
  'Rev': {'korean': '요한계시록', 'english': 'Revelation'},
};

String getBookDisplayName(String key) {
  final names = _bibleBookNames[key] ?? {'korean': key, 'english': key};
  return '${names['korean']} (${names['english']})';
}

class BibleProvider with ChangeNotifier {
  List<BibleBook> _books = [];
  int _currentBookIndex = 0;
  int _currentChapterIndex = 0;

  bool _isLoading = false;
  bool _hasError = false;
  String _errorMessage = '';

  List<BibleBook> get books => _books;
  bool get isLoading => _isLoading;
  bool get hasError => _hasError;
  String get errorMessage => _errorMessage;

  BibleBook? get currentBook => _books.isNotEmpty ? _books[_currentBookIndex] : null;
  int get currentBookIndex => _currentBookIndex;
  int get currentChapterIndex => _currentChapterIndex;

  List<BibleBookmark> _bookmarks = [];
  List<BibleBookmark> get bookmarks => List.unmodifiable(_bookmarks);

  List<Hymn> _hymns = [];
  List<Hymn> get hymns => List.unmodifiable(_hymns);

  List<int> _favoriteHymnIds = [];
  List<Hymn> get favoriteHymns => _hymns.where((h) => _favoriteHymnIds.contains(h.id)).toList();

  String get version => BibleDataService().currentVersion;

  Future<void> loadBooks() async {
    if (_books.isNotEmpty) return;
    _isLoading = true;
    _hasError = false;
    notifyListeners();
    try {
      final service = BibleDataService();
      _books = await service.getBooks();
      if (_books.isEmpty) {
        _books = await service.loadAndSeedBibleData();
      }
      await loadBookmarks();
      await loadHymns();
    } catch (e) {
      _hasError = true;
      _errorMessage = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> loadBookmarks() async {
    final box = await Hive.openBox<BibleBookmark>('bookmarks');
    _bookmarks = box.values.toList()
      ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
  }

  Future<void> loadHymns() async {
    if (_hymns.isNotEmpty) return;
    try {
      final jsonString = await rootBundle.loadString('assets/data/hymns.json');
      final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
      final list = (jsonMap['hymns'] as List<dynamic>)
          .map((e) => Hymn.fromJson(e as Map<String, dynamic>))
          .toList();
      _hymns = list;
    } catch (e) {
      _hymns = [];
    }
    await loadHymnFavorites();
    notifyListeners();
  }

  Future<void> loadHymnFavorites() async {
    final box = await Hive.openBox<int>('hymn_favorites');
    _favoriteHymnIds = box.values.toList();
  }

  Future<void> toggleHymnFavorite(int hymnId) async {
    final box = await Hive.openBox<int>('hymn_favorites');
    if (_favoriteHymnIds.contains(hymnId)) {
      _favoriteHymnIds.remove(hymnId);
      await box.delete(hymnId);
    } else {
      _favoriteHymnIds.add(hymnId);
      await box.put(hymnId, hymnId);
    }
    notifyListeners();
  }

  Future<void> addBookmark(BibleBookmark bookmark) async {
    final box = await Hive.openBox<BibleBookmark>('bookmarks');
    // Remove duplicate for same position
    for (var key in box.keys) {
      final existing = box.get(key);
      if (existing != null &&
          existing.bookIndex == bookmark.bookIndex &&
          existing.chapterIndex == bookmark.chapterIndex &&
          existing.verseIndex == bookmark.verseIndex) {
        await box.delete(key);
        break;
      }
    }
    await box.add(bookmark);
    _bookmarks = box.values.toList()
      ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
    notifyListeners();
  }

  Future<void> removeBookmark(BibleBookmark bookmark) async {
    final box = await Hive.openBox<BibleBookmark>('bookmarks');
    for (var key in box.keys) {
      final existing = box.get(key);
      if (existing != null &&
          existing.bookIndex == bookmark.bookIndex &&
          existing.chapterIndex == bookmark.chapterIndex &&
          existing.verseIndex == bookmark.verseIndex) {
        await box.delete(key);
        break;
      }
    }
    _bookmarks = box.values.toList()
      ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
    notifyListeners();
  }

  bool isVerseBookmarked(int bookIndex, int chapterIndex, int verseIndex) {
    return _bookmarks.any((b) =>
        b.bookIndex == bookIndex &&
        b.chapterIndex == chapterIndex &&
        b.verseIndex == verseIndex);
  }

  bool isChapterBookmarked(int bookIndex, int chapterIndex) {
    return _bookmarks.any((b) =>
        b.bookIndex == bookIndex &&
        b.chapterIndex == chapterIndex &&
        b.verseIndex == null);
  }

  void setCurrentBook(int index) {
    if (index >= 0 && index < _books.length) {
      _currentBookIndex = index;
      _currentChapterIndex = 0;
      notifyListeners();
    }
  }

  void setCurrentChapter(int index) {
    final book = currentBook;
    if (book != null && index >= 0 && index < book.chapters.length) {
      _currentChapterIndex = index;
      notifyListeners();
    }
  }

  void goToNextChapter() {
    final book = currentBook;
    if (book == null) return;
    if (_currentChapterIndex < book.chapters.length - 1) {
      _currentChapterIndex++;
    } else if (_currentBookIndex < _books.length - 1) {
      _currentBookIndex++;
      _currentChapterIndex = 0;
    }
    notifyListeners();
  }

  void goToPreviousChapter() {
    final book = currentBook;
    if (book == null) return;
    if (_currentChapterIndex > 0) {
      _currentChapterIndex--;
    } else if (_currentBookIndex > 0) {
      _currentBookIndex--;
      _currentChapterIndex = _books[_currentBookIndex].chapters.length - 1;
    }
    notifyListeners();
  }

  String get currentBookDisplayName {
    if (currentBook == null) return '';
    return getBookDisplayName(currentBook!.book);
  }

  String getBookDisplayNameForIndex(int index) {
    if (index < 0 || index >= _books.length) return '';
    return getBookDisplayName(_books[index].book);
  }

  List<VerseMatch> searchVerses(String query) {
    if (query.trim().isEmpty) return [];
    final q = query.toLowerCase().trim();
    final results = <VerseMatch>[];
    for (int bi = 0; bi < _books.length; bi++) {
      final book = _books[bi];
      final disp = getBookDisplayNameForIndex(bi).toLowerCase();
      for (int ci = 0; ci < book.chapters.length; ci++) {
        final chapter = book.chapters[ci];
        for (int vi = 0; vi < chapter.verses.length; vi++) {
          final verse = chapter.verses[vi];
          if (verse.text.toLowerCase().contains(q) || disp.contains(q)) {
            results.add(VerseMatch(
              bi,
              ci,
              vi,
              getBookDisplayNameForIndex(bi),
              '${ci + 1}:${vi + 1} ${verse.text}',
            ));
            if (results.length >= 50) return results;
          }
        }
      }
    }
    return results;
  }
}

class VerseMatch {
  final int bookIndex;
  final int chapterIndex;
  final int verseIndex;
  final String bookDisplay;
  final String snippet;
  VerseMatch(this.bookIndex, this.chapterIndex, this.verseIndex, this.bookDisplay, this.snippet);
}
