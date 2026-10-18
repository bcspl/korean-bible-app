import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';
import '../services/last_position_service.dart';
import 'book_list_screen.dart';
import 'bookmark_list_screen.dart';
import 'chapter_list_screen.dart';
import 'creed_screen.dart';
import 'hymn_detail_screen.dart';
import 'hymn_list_screen.dart';
import 'lords_prayer_screen.dart';
import 'responsive_reading_screen.dart';
import 'settings_screen.dart';
import 'verse_viewer_screen.dart';
import 'worship_materials_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  /// 이번 실행에서 이미 '이어보기'를 연 섹션 (섹션당 1회만 자동으로 엶).
  final Set<AppSection> _resumed = {};
  BibleProvider? _waitingProvider;
  AppSection? _pending;

  final List<Widget> _screens = const [
    BookListScreen(),
    WorshipMaterialsScreen(),
    HymnListScreen(),
    BookmarkListScreen(),
    SettingsScreen(),
  ];

  @override
  void initState() {
    super.initState();
    _restore();
  }

  @override
  void dispose() {
    _waitingProvider?.removeListener(_onProviderChanged);
    super.dispose();
  }

  Future<void> _restore() async {
    await LastPositionService.load();
    if (!mounted) return;
    final section = LastPositionService.section;
    if (section == null) return; // 처음 사용: 기본 홈
    setState(() => _currentIndex = section.tabIndex);
    _resume(section);
  }

  AppSection? _sectionForTab(int i) =>
      i < AppSection.values.length ? AppSection.values[i] : null;

  void _onTabTap(int i) {
    setState(() => _currentIndex = i);
    final s = _sectionForTab(i);
    if (s != null) {
      LastPositionService.saveSection(s);
      _resume(s);
    }
  }

  void _resume(AppSection s) {
    if (_resumed.contains(s) || !LastPositionService.hasPosition(s)) return;
    final provider = context.read<BibleProvider>();
    final needsData = s == AppSection.bible || s == AppSection.hymn;
    final ready = s == AppSection.bible
        ? provider.books.isNotEmpty
        : (s == AppSection.hymn ? provider.hymns.isNotEmpty : true);
    if (needsData && !ready) {
      if (provider.hasError) return;
      _pending = s;
      if (_waitingProvider == null) {
        _waitingProvider = provider;
        provider.addListener(_onProviderChanged);
      }
      return;
    }
    _resumed.add(s);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) _open(s, provider);
    });
    WidgetsBinding.instance.scheduleFrame();
  }

  void _onProviderChanged() {
    final p = _waitingProvider;
    final s = _pending;
    if (p == null || s == null) return;
    final ready = s == AppSection.bible ? p.books.isNotEmpty : p.hymns.isNotEmpty;
    if (!ready && !p.hasError) return;
    p.removeListener(_onProviderChanged);
    _waitingProvider = null;
    _pending = null;
    // 사용자가 그 사이 다른 탭으로 이동했다면 열지 않음
    if (!mounted || _sectionForTab(_currentIndex) != s || !ready) return;
    _resume(s);
  }

  void _open(AppSection s, BibleProvider provider) {
    final nav = Navigator.of(context);
    switch (s) {
      case AppSection.bible:
        final pos = LastPositionService.bible!;
        if (pos.bookIndex >= provider.books.length) return;
        final book = provider.books[pos.bookIndex];
        if (pos.chapterIndex >= book.chapters.length) return;
        provider.setCurrentBook(pos.bookIndex);
        provider.setCurrentChapter(pos.chapterIndex);
        // 뒤로가기: 본문 → 장 목록 → 성경 목록
        nav.push(MaterialPageRoute(
            builder: (_) => ChapterListScreen(bookIndex: pos.bookIndex)));
        nav.push(MaterialPageRoute(
            builder: (_) => VerseViewerScreen(
                  bookIndex: pos.bookIndex,
                  chapterIndex: pos.chapterIndex,
                  initialScrollOffset: pos.scrollOffset,
                )));
        break;
      case AppSection.worship:
        final pos = LastPositionService.worship!;
        Widget screen;
        if (pos.screen == 'creed') {
          screen = const CreedScreen();
        } else if (pos.screen == 'prayer') {
          screen = const LordsPrayerScreen();
        } else {
          screen = ResponsiveReadingScreen(
              initialReadingNumber: pos.readingNumber);
        }
        nav.push(MaterialPageRoute(builder: (_) => screen));
        break;
      case AppSection.hymn:
        final id = LastPositionService.hymnId;
        Hymn? hymn;
        for (final h in provider.hymns) {
          if (h.id == id) {
            hymn = h;
            break;
          }
        }
        if (hymn == null) return;
        final h = hymn;
        nav.push(MaterialPageRoute(builder: (_) => HymnDetailScreen(hymn: h)));
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: Semantics(
        label: '메인 하단 내비게이션',
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: _onTabTap,
          type: BottomNavigationBarType.fixed,
          selectedItemColor: Colors.indigo,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.menu_book),
              label: '성경',
              tooltip: '성경 탭',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.account_balance),
              label: '예배자료',
              tooltip: '예배자료 탭',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.music_note),
              label: '찬송가',
              tooltip: '찬송가 탭',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.bookmark),
              label: '북마크',
              tooltip: '북마크 탭',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.settings),
              label: '설정',
              tooltip: '설정 탭',
            ),
          ],
        ),
      ),
    );
  }
}
