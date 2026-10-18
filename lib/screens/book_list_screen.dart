import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/bible_version.dart';
import '../providers/bible_provider.dart';
import 'about_screen.dart';
import 'bookmark_list_screen.dart';
import 'creed_screen.dart';
import 'hymn_list_screen.dart';
import 'lords_prayer_screen.dart';
import 'responsive_reading_screen.dart';
import 'chapter_list_screen.dart';
import 'verse_viewer_screen.dart';
import '../widgets/bible_version_selector.dart';
import '../services/last_position_service.dart';

class BookListScreen extends StatefulWidget {
  const BookListScreen({super.key});

  @override
  State<BookListScreen> createState() => _BookListScreenState();
}

class _BookListScreenState extends State<BookListScreen> {
  String _searchQuery = '';
  int _filter = 0; // 0: 전체, 1: 구약, 2: 신약
  BibleSearchResults _results = BibleSearchResults.empty;
  Timer? _debounce;
  final TextEditingController _searchController = TextEditingController();

  @override
  void dispose() {
    _debounce?.cancel();
    _searchController.dispose();
    super.dispose();
  }

  void _onQueryChanged(BibleProvider provider, String value) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 250), () {
      if (!mounted) return;
      setState(() {
        _searchQuery = value.trim();
        _results = provider.search(_searchQuery, bookFilter: _inFilter);
      });
    });
  }

  void _setFilter(int f, BibleProvider provider) {
    setState(() {
      _filter = f;
      if (_searchQuery.isNotEmpty) {
        _results = provider.search(_searchQuery, bookFilter: _inFilter);
      }
    });
  }

  bool _inFilter(int bookIndex) {
    const otCount = 39;
    if (_filter == 1) return bookIndex < otCount;
    if (_filter == 2) return bookIndex >= otCount;
    return true;
  }

  void _openChapter(BibleProvider provider, VerseMatch m) {
    provider.setCurrentBook(m.bookIndex);
    provider.setCurrentChapter(m.chapterIndex);
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => VerseViewerScreen(
          bookIndex: m.bookIndex,
          chapterIndex: m.chapterIndex,
          initialVerseIndex: m.verseIndex >= 0 ? m.verseIndex + 1 : null,
        ),
      ),
    );
  }

  void _openBook(BibleProvider provider, int bookIndex) {
    provider.setCurrentBook(bookIndex);
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => ChapterListScreen(bookIndex: bookIndex),
      ),
    );
  }

  Widget _sectionHeader(String title, int count) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(4, 12, 4, 4),
      child: Text(
        '$title ($count)',
        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
      ),
    );
  }

  /// 검색 결과: 성경책 → 구절 바로가기 → 본문 검색(책별 묶음·개수).
  Widget _buildSearchResults(BuildContext context, BibleProvider provider) {
    final books = _results.books.where(_inFilter).toList();
    final refs = _results.references.where((m) => _inFilter(m.bookIndex)).toList();
    final text = _results.textMatches.where((m) => _inFilter(m.bookIndex)).toList();
    var textTotal = 0;
    _results.textCountsByBook.forEach((bi, c) {
      if (_inFilter(bi)) textTotal += c;
    });

    final items = <Widget>[];
    if (books.isNotEmpty) {
      items.add(_sectionHeader('성경책', books.length));
      for (final bi in books) {
        final isOT = bi < 39;
        items.add(Card(
          margin: const EdgeInsets.symmetric(vertical: 3),
          child: ListTile(
            dense: true,
            leading: Icon(Icons.menu_book_outlined,
                color: isOT ? Colors.brown : Colors.indigo),
            title: Text(provider.getBookDisplayNameForIndex(bi),
                style: const TextStyle(fontWeight: FontWeight.w600)),
            subtitle: Text('${provider.books[bi].chapters.length}장 · ${isOT ? '구약' : '신약'}'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () => _openBook(provider, bi),
          ),
        ));
      }
    }
    if (refs.isNotEmpty) {
      items.add(_sectionHeader('구절 바로가기', refs.length));
      for (final m in refs) {
        items.add(Card(
          margin: const EdgeInsets.symmetric(vertical: 3),
          color: Colors.indigo.withValues(alpha: 0.06),
          child: ListTile(
            dense: true,
            leading: const Icon(Icons.subdirectory_arrow_right, color: Colors.indigo),
            title: Text('${m.bookDisplay} ${m.snippet}',
                maxLines: 2, overflow: TextOverflow.ellipsis),
            onTap: () => _openChapter(provider, m),
          ),
        ));
      }
    }
    if (textTotal > 0) {
      items.add(_sectionHeader('본문 검색', textTotal));
      if (textTotal > text.length) {
        items.add(Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
          child: Text('앞의 ${text.length}개 구절만 표시합니다. 검색어를 더 구체적으로 입력해 보세요.',
              style: const TextStyle(fontSize: 11, color: Colors.grey)),
        ));
      }
      int? lastBook;
      for (final m in text) {
        if (m.bookIndex != lastBook) {
          lastBook = m.bookIndex;
          items.add(Padding(
            padding: const EdgeInsets.fromLTRB(8, 8, 8, 2),
            child: Text(
              '${m.bookDisplay} · ${_results.textCountsByBook[m.bookIndex] ?? 0}절',
              style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: m.bookIndex < 39 ? Colors.brown : Colors.indigo),
            ),
          ));
        }
        items.add(Card(
          margin: const EdgeInsets.symmetric(vertical: 2),
          child: ListTile(
            dense: true,
            title: Semantics(
              label: '검색 결과 ${m.bookDisplay} ${m.snippet}',
              child: Text(m.snippet,
                  style: const TextStyle(fontSize: 13),
                  maxLines: 3,
                  overflow: TextOverflow.ellipsis),
            ),
            onTap: () => _openChapter(provider, m),
          ),
        ));
      }
    }
    if (items.isEmpty) {
      items.add(const Padding(
        padding: EdgeInsets.all(24),
        child: Center(child: Text('검색 결과가 없습니다.')),
      ));
    }
    return ListView(
      padding: EdgeInsets.fromLTRB(16, 0, 16, 8 + MediaQuery.viewPaddingOf(context).bottom),
      children: items,
    );
  }

  Widget? _buildResumeCard(BuildContext context, BibleProvider provider) {
    final pos = LastPositionService.bible;
    if (pos == null || pos.bookIndex >= provider.books.length) return null;
    final book = provider.books[pos.bookIndex];
    if (pos.chapterIndex >= book.chapters.length) return null;
    final ch = book.chapters[pos.chapterIndex].chapter;
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 4),
      child: Card(
        color: Colors.indigo.withValues(alpha: 0.08),
        child: ListTile(
          dense: true,
          leading: const Icon(Icons.play_circle_outline, color: Colors.indigo),
          title: Text('이어 읽기: ${getBookKoreanName(book.book)} $ch장'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () {
            provider.setCurrentBook(pos.bookIndex);
            provider.setCurrentChapter(pos.chapterIndex);
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ChapterListScreen(bookIndex: pos.bookIndex),
              ),
            );
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => VerseViewerScreen(
                  bookIndex: pos.bookIndex,
                  chapterIndex: pos.chapterIndex,
                  initialScrollOffset: pos.scrollOffset,
                ),
              ),
            ).then((_) {
              if (mounted) setState(() {});
            });
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final books = provider.books;

    if (provider.isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    if (provider.hasError) {
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('데이터 로드 실패: ${provider.errorMessage}'),
              ElevatedButton(
                onPressed: () => provider.loadBooks(),
                child: const Text('재시도'),
              ),
            ],
          ),
        ),
      );
    }
    if (books.isEmpty) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    const otCount = 39;
    const ntCount = 27;
    const totalCount = otCount + ntCount;

    final filteredBooks = books.where((book) {
      final originalIndex = books.indexOf(book);
      final isOT = originalIndex < otCount;
      if (_filter == 1 && !isOT) return false;
      if (_filter == 2 && isOT) return false;
      return true;
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('성경'),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.bookmark),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const BookmarkListScreen()),
              );
            },
            tooltip: '북마크 목록',
          ),
          IconButton(
            icon: const Icon(Icons.music_note),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const HymnListScreen()),
              );
            },
            tooltip: '찬송가',
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.menu_book),
            tooltip: '예배 자료',
            onSelected: (v) {
              Widget screen;
              if (v == 'creed') {
                screen = const CreedScreen();
              } else if (v == 'prayer') {
                screen = const LordsPrayerScreen();
              } else if (v == 'reading') {
                screen = const ResponsiveReadingScreen();
              } else {
                screen = const AboutScreen();
              }
              Navigator.push(context, MaterialPageRoute(builder: (_) => screen));
            },
            itemBuilder: (c) => const [
              PopupMenuItem(value: 'creed', child: Text('사도신경')),
              PopupMenuItem(value: 'prayer', child: Text('주기도문')),
              PopupMenuItem(value: 'reading', child: Text('교독문')),
              PopupMenuItem(value: 'about', child: Text('이 성경앱에 대해서')),
            ],
          ),
        ],
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final isWide = constraints.maxWidth > 900;
          final isMedium = constraints.maxWidth > 600;
          final horizontalPadding = isWide ? 32.0 : (isMedium ? 24.0 : 16.0);
          return Column(
            children: [
              // Search bar
              Padding(
                padding: EdgeInsets.fromLTRB(horizontalPadding, 8, horizontalPadding, 8),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: '책·장절·본문 검색 (예: 창, 요 3:16, 사랑)',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchQuery.isEmpty
                    ? null
                    : IconButton(
                        icon: const Icon(Icons.clear),
                        tooltip: '검색어 지우기',
                        onPressed: () {
                          _debounce?.cancel();
                          _searchController.clear();
                          setState(() {
                            _searchQuery = '';
                            _results = BibleSearchResults.empty;
                          });
                        },
                      ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: Theme.of(context).cardColor,
                contentPadding: const EdgeInsets.symmetric(vertical: 12),
              ),
              onChanged: (value) => _onQueryChanged(provider, value),
            ),
          ),

          const BibleVersionSelector(dense: true),
          Padding(
            padding: const EdgeInsets.only(bottom: 4, top: 4),
            child: Consumer<BibleProvider>(
              builder: (context, provider, _) => Text(
                '기본 본문: ${provider.version} · 병렬: ${provider.activeVersions.map((v) => v.code).join(", ")} (PD)',
                style: const TextStyle(fontSize: 11, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
            ),
          ),

          // User-friendly OT/NT filter - Segmented style
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                _buildFilterButton(
                  context,
                  label: '전체',
                  count: totalCount,
                  selected: _filter == 0,
                  onTap: () => _setFilter(0, provider),
                ),
                const SizedBox(width: 8),
                _buildFilterButton(
                  context,
                  label: '구약',
                  count: otCount,
                  selected: _filter == 1,
                  onTap: () => _setFilter(1, provider),
                  color: Colors.brown,
                ),
                const SizedBox(width: 8),
                _buildFilterButton(
                  context,
                  label: '신약',
                  count: ntCount,
                  selected: _filter == 2,
                  onTap: () => _setFilter(2, provider),
                  color: Colors.indigo,
                ),
              ],
            ),
          ),

          if (_searchQuery.isEmpty)
            ...[_buildResumeCard(context, provider)].whereType<Widget>(),

          if (_searchQuery.isNotEmpty)
            Expanded(child: _buildSearchResults(context, provider))
          else
          // List of books - full scrollable
            Expanded(
            child: ListView.separated(
              padding: EdgeInsets.fromLTRB(16, 8, 16, 8 + MediaQuery.viewPaddingOf(context).bottom),
              itemCount: filteredBooks.length,
              separatorBuilder: (_, __) => const Divider(height: 1),
              itemBuilder: (context, index) {
                final book = filteredBooks[index];
                final originalIndex = books.indexOf(book);
                final isOT = originalIndex < otCount;
                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  elevation: 2,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    leading: Icon(
                      Icons.menu_book_outlined,
                      color: isOT ? Colors.brown : Colors.indigo,
                      size: 32,
                    ),
                    title: Text(
                      provider.getBookDisplayNameForIndex(originalIndex),
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15),
                    ),
                    subtitle: Text('${book.chapters.length}장'),
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: isOT ? Colors.brown.shade100 : Colors.indigo.shade100,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Text(
                        isOT ? '구약' : '신약',
                        style: TextStyle(
                          fontSize: 11,
                          color: isOT ? Colors.brown.shade700 : Colors.indigo.shade700,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    onTap: () {
                      provider.setCurrentBook(originalIndex);
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => ChapterListScreen(bookIndex: originalIndex),
                        ),
                      );
                    },
                  ),
                );
              },
            ),
          ),
        ],
      );
    },
  ),
);
  }

  Widget _buildFilterButton(
    BuildContext context, {
    required String label,
    required int count,
    required bool selected,
    required VoidCallback onTap,
    Color? color,
  }) {
    final bgColor = selected
        ? (color ?? Theme.of(context).primaryColor)
        : Colors.grey.shade200;
    final textColor = selected ? Colors.white : Colors.black87;

    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: bgColor,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: selected ? (color ?? Theme.of(context).primaryColor) : Colors.grey.shade300,
              width: 1.5,
            ),
          ),
          child: Column(
            children: [
              Text(
                label,
                style: TextStyle(
                  color: textColor,
                  fontWeight: FontWeight.bold,
                  fontSize: 15,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                '$count권',
                style: TextStyle(
                  color: textColor.withValues(alpha: 0.8),
                  fontSize: 12,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

