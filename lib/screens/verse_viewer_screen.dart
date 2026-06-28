import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/bible_bookmark.dart';
import '../providers/bible_provider.dart';

class VerseViewerScreen extends StatefulWidget {
  final int bookIndex;
  final int chapterIndex;
  final int? initialVerseIndex; // 북마크에서 특정 절로 이동 시

  const VerseViewerScreen({
    super.key,
    required this.bookIndex,
    required this.chapterIndex,
    this.initialVerseIndex,
  });

  @override
  State<VerseViewerScreen> createState() => _VerseViewerScreenState();
}

class _VerseViewerScreenState extends State<VerseViewerScreen> {
  late ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.initialVerseIndex != null) {
        final chapter = Provider.of<BibleProvider>(context, listen: false)
            .books[widget.bookIndex]
            .chapters[widget.chapterIndex];
        final targetIndex = widget.initialVerseIndex! - 1; // 1-based to 0
        if (targetIndex >= 0 && targetIndex < chapter.verses.length) {
          // approximate scroll, each item ~ 40-60px
          _scrollController.animateTo(
            targetIndex * 55.0,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final book = provider.books[widget.bookIndex];
    final chapter = book.chapters[widget.chapterIndex];

    final displayName = provider.getBookDisplayNameForIndex(widget.bookIndex);
    final version = provider.version;

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('$displayName ${widget.chapterIndex + 1}장', style: const TextStyle(fontSize: 18)),
            Text(version, style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ],
        ),
        actions: [
          Consumer<BibleProvider>(
            builder: (context, provider, _) {
              final isBookmarked = provider.isChapterBookmarked(
                widget.bookIndex, widget.chapterIndex);
              return IconButton(
                icon: Icon(
                  isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                  color: isBookmarked ? Colors.indigo : null,
                ),
                onPressed: () async {
                  final book = provider.books[widget.bookIndex];
                  final snippet = '${book.book} ${widget.chapterIndex + 1}장';
                  final bm = BibleBookmark(
                    bookIndex: widget.bookIndex,
                    chapterIndex: widget.chapterIndex,
                    verseIndex: null,
                    snippet: snippet,
                    createdAt: DateTime.now(),
                  );
                  if (isBookmarked) {
                    await provider.removeBookmark(bm);
                  } else {
                    await provider.addBookmark(bm);
                  }
                },
                tooltip: isBookmarked ? '장 북마크 해제' : '현재 장 북마크',
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.home),
            onPressed: () {
              Navigator.popUntil(context, (route) => route.isFirst);
            },
            tooltip: '성경 목록으로',
          ),
          IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () {
              provider.goToPreviousChapter();
              _navigateToCurrent(context, provider);
            },
          ),
          IconButton(
            icon: const Icon(Icons.arrow_forward),
            onPressed: () {
              provider.goToNextChapter();
              _navigateToCurrent(context, provider);
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Direct prev/next chapter navigation + home
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            color: Colors.grey.shade100,
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.home, size: 20),
                  onPressed: () {
                    Navigator.popUntil(context, (route) => route.isFirst);
                  },
                  tooltip: '성경 목록으로',
                  color: Colors.indigo,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      TextButton.icon(
                        onPressed: () {
                          provider.goToPreviousChapter();
                          _navigateToCurrent(context, provider);
                        },
                        icon: const Icon(Icons.arrow_back, size: 18),
                        label: const Text('이전 장'),
                        style: TextButton.styleFrom(foregroundColor: Colors.indigo),
                      ),
                      Text(
                        '${widget.chapterIndex + 1}장',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      TextButton.icon(
                        onPressed: () {
                          provider.goToNextChapter();
                          _navigateToCurrent(context, provider);
                        },
                        icon: const Icon(Icons.arrow_forward, size: 18),
                        label: const Text('다음 장'),
                        style: TextButton.styleFrom(foregroundColor: Colors.indigo),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: chapter.verses.length,
              itemBuilder: (context, index) {
                final verse = chapter.verses[index];
                return Consumer<BibleProvider>(
                  builder: (context, provider, _) {
                    final isBookmarked = provider.isVerseBookmarked(
                        widget.bookIndex, widget.chapterIndex, verse.verse);
                    return Padding(
                      padding: const EdgeInsets.symmetric(vertical: 4),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Expanded(
                            child: Semantics(
                              label: '절 ${verse.verse}: ${verse.text}',
                              child: RichText(
                                text: TextSpan(
                                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(fontSize: 17, height: 1.7),
                                  children: [
                                    TextSpan(
                                      text: '${verse.verse} ',
                                      style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.indigo, fontSize: 15),
                                    ),
                                    TextSpan(text: verse.text),
                                  ],
                                ),
                              ),
                            ),
                          ),
                          IconButton(
                            icon: Icon(
                              isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                              size: 18,
                              color: isBookmarked ? Colors.indigo : Colors.grey,
                            ),
                            onPressed: () async {
                              final snippet = '${verse.verse} ${verse.text.length > 30 ? '${verse.text.substring(0, 30)}...' : verse.text}';
                              final bm = BibleBookmark(
                                bookIndex: widget.bookIndex,
                                chapterIndex: widget.chapterIndex,
                                verseIndex: verse.verse,
                                snippet: snippet,
                                createdAt: DateTime.now(),
                              );
                              if (isBookmarked) {
                                await provider.removeBookmark(bm);
                              } else {
                                await provider.addBookmark(bm);
                              }
                            },
                            padding: EdgeInsets.zero,
                            constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
                          ),
                        ],
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          provider.goToNextChapter();
          _navigateToCurrent(context, provider);
        },
        child: const Icon(Icons.arrow_forward),
      ),
    );
  }

  void _navigateToCurrent(BuildContext context, BibleProvider provider) {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (_) => VerseViewerScreen(
          bookIndex: provider.currentBookIndex,
          chapterIndex: provider.currentChapterIndex,
        ),
      ),
    );
  }
}
