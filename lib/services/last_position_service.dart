import 'package:shared_preferences/shared_preferences.dart';

/// 앱 섹션 (하단 탭 인덱스와 동일).
enum AppSection { bible, worship, hymn }

extension AppSectionX on AppSection {
  int get tabIndex => index; // 0 성경 · 1 예배자료 · 2 찬송가
}

class BiblePosition {
  final int bookIndex;
  final int chapterIndex;
  final double scrollOffset;
  const BiblePosition(this.bookIndex, this.chapterIndex, [this.scrollOffset = 0]);

  String encode() =>
      '$bookIndex:$chapterIndex:${scrollOffset.toStringAsFixed(0)}';

  static BiblePosition? decode(String? s) {
    if (s == null) return null;
    final p = s.split(':');
    if (p.length < 2) return null;
    final b = int.tryParse(p[0]);
    final c = int.tryParse(p[1]);
    final o = p.length > 2 ? double.tryParse(p[2]) ?? 0 : 0.0;
    if (b == null || c == null || b < 0 || c < 0) return null;
    return BiblePosition(b, c, o < 0 ? 0 : o);
  }
}

/// 예배자료 위치: 'creed' | 'prayer' | 'reading' | 'reading:<번호>'
class WorshipPosition {
  final String screen; // creed, prayer, reading
  final int? readingNumber;
  const WorshipPosition(this.screen, [this.readingNumber]);

  String encode() =>
      readingNumber == null ? screen : '$screen:$readingNumber';

  static WorshipPosition? decode(String? s) {
    if (s == null || s.isEmpty) return null;
    final p = s.split(':');
    const valid = {'creed', 'prayer', 'reading'};
    if (!valid.contains(p[0])) return null;
    final n = p.length > 1 ? int.tryParse(p[1]) : null;
    return WorshipPosition(p[0], p[0] == 'reading' ? n : null);
  }
}

/// 섹션별 마지막 위치 저장 (SharedPreferences · 저장은 비동기 fire-and-forget).
class LastPositionService {
  static const kSection = 'last_section';
  static const kBible = 'last_bible_position';
  static const kWorship = 'last_worship_position';
  static const kHymn = 'last_hymn_id';

  static AppSection? section;
  static BiblePosition? bible;
  static WorshipPosition? worship;
  static int? hymnId;
  static bool _loaded = false;

  static Future<void> load() async {
    if (_loaded) return;
    try {
      final prefs = await SharedPreferences.getInstance();
      final s = prefs.getInt(kSection);
      section = (s != null && s >= 0 && s < AppSection.values.length)
          ? AppSection.values[s]
          : null;
      bible = BiblePosition.decode(prefs.getString(kBible));
      worship = WorshipPosition.decode(prefs.getString(kWorship));
      hymnId = prefs.getInt(kHymn);
    } catch (_) {}
    _loaded = true;
  }

  static bool hasPosition(AppSection s) {
    switch (s) {
      case AppSection.bible:
        return bible != null;
      case AppSection.worship:
        return worship != null;
      case AppSection.hymn:
        return hymnId != null;
    }
  }

  static Future<void> _queue = Future.value();

  /// 쓰기를 순서대로 실행 (호출자는 기다리지 않음).
  static void _write(Future<void> Function(SharedPreferences p) f) {
    _queue = _queue.then((_) async {
      try {
        await f(await SharedPreferences.getInstance());
      } catch (_) {}
    });
  }

  /// 대기 중인 저장 완료 (테스트용).
  static Future<void> flush() => _queue;

  static void saveSection(AppSection s) {
    section = s;
    _write((p) async {
      await p.setInt(kSection, s.index);
    });
  }

  static void saveBible(BiblePosition pos) {
    bible = pos;
    section = AppSection.bible;
    _write((p) async {
      await p.setString(kBible, pos.encode());
      await p.setInt(kSection, AppSection.bible.index);
    });
  }

  static void saveWorship(WorshipPosition pos) {
    worship = pos;
    section = AppSection.worship;
    _write((p) async {
      await p.setString(kWorship, pos.encode());
      await p.setInt(kSection, AppSection.worship.index);
    });
  }

  static void saveHymn(int id) {
    hymnId = id;
    section = AppSection.hymn;
    _write((p) async {
      await p.setInt(kHymn, id);
      await p.setInt(kSection, AppSection.hymn.index);
    });
  }

  /// 테스트용 초기화.
  static void resetForTest() {
    section = null;
    bible = null;
    worship = null;
    hymnId = null;
    _loaded = false;
  }
}
