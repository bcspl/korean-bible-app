import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';
import 'about_screen.dart';
import 'bookmark_list_screen.dart';
import 'creed_screen.dart';
import 'hymn_list_screen.dart';
import 'lords_prayer_screen.dart';
import 'responsive_reading_screen.dart';
import 'chapter_list_screen.dart';
import 'verse_viewer_screen.dart';

class BookListScreen extends StatefulWidget {
  const BookListScreen({super.key});

  @override
  State<BookListScreen> createState() => _BookListScreenState();
}

class _BookListScreenState extends State<BookListScreen> {
  String _searchQuery = '';
  int _filter = 0; // 0: 전체, 1: 구약, 2: 신약
  List<VerseMatch> _verseMatches = [];

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
      final display = provider.getBookDisplayNameForIndex(originalIndex).toLowerCase();
      final matchesSearch = display.contains(_searchQuery.toLowerCase());
      final isOT = originalIndex < otCount;
      if (_filter == 1 && !isOT) return false;
      if (_filter == 2 && isOT) return false;
      return matchesSearch;
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
              if (v == 'creed') screen = const CreedScreen();
              else if (v == 'prayer') screen = const LordsPrayerScreen();
              else if (v == 'reading') screen = const ResponsiveReadingScreen();
              else screen = const AboutScreen();
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
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
            child: TextField(
              decoration: InputDecoration(
                hintText: '책 이름으로 검색...',
                prefixIcon: const Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                filled: true,
                fillColor: Theme.of(context).cardColor,
                contentPadding: const EdgeInsets.symmetric(vertical: 12),
              ),
              onChanged: (value) {
                setState(() {
                  _searchQuery = value;
                  _verseMatches = provider.searchVerses(value);
                });
              },
            ),
          ),

          // Version info
          Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Consumer<BibleProvider>(
              builder: (context, provider, _) => Text(
                '버전: ${provider.version}',
                style: const TextStyle(fontSize: 12, color: Colors.grey),
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
                  onTap: () => setState(() => _filter = 0),
                ),
                const SizedBox(width: 8),
                _buildFilterButton(
                  context,
                  label: '구약',
                  count: otCount,
                  selected: _filter == 1,
                  onTap: () => setState(() => _filter = 1),
                  color: Colors.brown,
                ),
                const SizedBox(width: 8),
                _buildFilterButton(
                  context,
                  label: '신약',
                  count: ntCount,
                  selected: _filter == 2,
                  onTap: () => setState(() => _filter = 2),
                  color: Colors.indigo,
                ),
              ],
            ),
          ),

          // 본문 검색 결과 (if searching)
          if (_searchQuery.isNotEmpty && _verseMatches.isNotEmpty) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '본문 검색 결과 (${_verseMatches.length})',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
              ),
            ),
            SizedBox(
              height: 120, // limited height for results
              child: ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _verseMatches.length,
                itemBuilder: (context, i) {
                  final match = _verseMatches[i];
                  return Card(
                    child: ListTile(
                      dense: true,
                      title: Semantics(
                        label: '검색 결과 ${match.bookDisplay} ${match.snippet}',
                        child: Text(
                          '${match.bookDisplay} ${match.snippet}',
                          style: const TextStyle(fontSize: 13),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                      onTap: () {
                        provider.setCurrentBook(match.bookIndex);
                        provider.setCurrentChapter(match.chapterIndex);
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => VerseViewerScreen(
                              bookIndex: match.bookIndex,
                              chapterIndex: match.chapterIndex,
                              initialVerseIndex: match.verseIndex + 1, // 0-based -> 1-based
                            ),
                          ),
                        );
                      },
                    ),
                  );
                },
              ),
            ),
            const Divider(),
          ],

          // List of books - full scrollable
          Expanded(
            child: ListView.separated(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
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
