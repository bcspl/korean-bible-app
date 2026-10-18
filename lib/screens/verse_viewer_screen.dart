import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/bible_bookmark.dart';
import '../models/bible_version.dart';
import '../providers/bible_provider.dart';
import '../providers/theme_provider.dart';
import '../services/last_position_service.dart';
import '../widgets/bible_version_selector.dart';

class VerseViewerScreen extends StatefulWidget {
  final int bookIndex;
  final int chapterIndex;
  final int? initialVerseIndex;

  /// 이어 읽기: 마지막 스크롤 위치 (px).
  final double? initialScrollOffset;

  const VerseViewerScreen({
    super.key,
    required this.bookIndex,
    required this.chapterIndex,
    this.initialVerseIndex,
    this.initialScrollOffset,
  });

  @override
  State<VerseViewerScreen> createState() => _VerseViewerScreenState();
}

class _VerseViewerScreenState extends State<VerseViewerScreen> {
  late ScrollController _scrollController;
  Timer? _saveDebounce;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    _scrollController.addListener(_onScroll);
    _savePosition(widget.initialScrollOffset ?? 0);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.initialVerseIndex != null) {
        final targetIndex = widget.initialVerseIndex! - 1;
        if (targetIndex >= 0) {
          _scrollController.animateTo(
            targetIndex * 90.0,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          );
        }
      } else if ((widget.initialScrollOffset ?? 0) > 0) {
        _restoreOffset(widget.initialScrollOffset!, 0);
      }
    });
  }

  /// 지연 생성 리스트라 최대 범위가 점차 늘어나므로 몇 프레임에 걸쳐 복원.
  void _restoreOffset(double target, int attempt) {
    if (!mounted || !_scrollController.hasClients) return;
    final pos = _scrollController.position;
    final to = target.clamp(0.0, pos.maxScrollExtent);
    _scrollController.jumpTo(to);
    if (to < target && attempt < 8) {
      WidgetsBinding.instance
          .addPostFrameCallback((_) => _restoreOffset(target, attempt + 1));
      WidgetsBinding.instance.scheduleFrame();
    }
  }

  void _onScroll() {
    _saveDebounce?.cancel();
    _saveDebounce = Timer(const Duration(milliseconds: 600), () {
      if (mounted && _scrollController.hasClients) {
        _savePosition(_scrollController.offset);
      }
    });
  }

  void _savePosition(double offset) {
    LastPositionService.saveBible(
        BiblePosition(widget.bookIndex, widget.chapterIndex, offset));
  }

  @override
  void dispose() {
    _saveDebounce?.cancel();
    // 다음/이전 장으로 교체된 경우 새 화면의 위치를 덮어쓰지 않도록 같은 장일 때만 저장
    final last = LastPositionService.bible;
    if (_scrollController.hasClients &&
        last != null &&
        last.bookIndex == widget.bookIndex &&
        last.chapterIndex == widget.chapterIndex) {
      _savePosition(_scrollController.offset);
    }
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    if (widget.bookIndex < 0 || widget.bookIndex >= provider.books.length) {
      return const Scaffold(body: Center(child: Text('책을 찾을 수 없습니다.')));
    }
    final book = provider.books[widget.bookIndex];
    if (widget.chapterIndex < 0 ||
        widget.chapterIndex >= book.chapters.length) {
      return const Scaffold(body: Center(child: Text('장을 찾을 수 없습니다.')));
    }
    final chapter = book.chapters[widget.chapterIndex];
    final bookKey = book.book;
    final chNum = chapter.chapter;
    final displayName = provider.getBookDisplayNameForIndex(widget.bookIndex);
    final active = provider.activeVersions;
    final verseNums = provider.verseNumbersForChapter(bookKey, chNum);
    // Prefer KRV verse order if available
    final orderedNums = verseNums.isNotEmpty
        ? verseNums
        : chapter.verses.map((v) => v.verse).toList();

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '$displayName $chNum장',
              style: const TextStyle(fontSize: 18),
            ),
            Text(
              active.map((v) => v.code).join(' · '),
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
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
                  final snippet = '${book.book} $chNum장';
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
          const BibleVersionSelector(dense: true),
          Consumer<BibleProvider>(
            builder: (context, provider, _) => Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              color: provider.isChapterBookmarked(
                      widget.bookIndex, widget.chapterIndex)
                  ? Colors.yellow.withValues(alpha: 0.15)
                  : Colors.grey.shade100,
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
                          style: TextButton.styleFrom(
                              foregroundColor: Colors.indigo),
                        ),
                        Text(
                          '$chNum장',
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        TextButton.icon(
                          onPressed: () {
                            provider.goToNextChapter();
                            _navigateToCurrent(context, provider);
                          },
                          icon: const Icon(Icons.arrow_forward, size: 18),
                          label: const Text('다음 장'),
                          style: TextButton.styleFrom(
                              foregroundColor: Colors.indigo),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            child: Builder(
              builder: (context) {
                final width = MediaQuery.of(context).size.width;
                final horizontalPad =
                    width > 900 ? 32.0 : (width > 600 ? 24.0 : 12.0);
                return ListView.builder(
                  controller: _scrollController,
                  padding: EdgeInsets.fromLTRB(horizontalPad, 12, horizontalPad,
                      12 + 72 + MediaQuery.viewPaddingOf(context).bottom),
                  itemCount: orderedNums.length,
                  itemBuilder: (context, index) {
                    final vNum = orderedNums[index];
                    return Consumer2<BibleProvider, ThemeProvider>(
                      builder: (context, bibleProvider, themeProvider, _) {
                        final isBookmarked = bibleProvider.isVerseBookmarked(
                            widget.bookIndex, widget.chapterIndex, vNum);
                        final versions = bibleProvider.activeVersions;
                        return Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          decoration: BoxDecoration(
                            color: isBookmarked
                                ? (themeProvider.highContrast
                                    ? Colors.yellow.withValues(alpha: 0.35)
                                    : Colors.yellow.withValues(alpha: 0.18))
                                : null,
                            border: Border(
                              bottom: BorderSide(color: Colors.grey.shade300),
                            ),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              SizedBox(
                                width: 36,
                                child: Text(
                                  '$vNum',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.indigo,
                                    fontSize: 15,
                                  ),
                                ),
                              ),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    for (final ver in versions)
                                      _VersionVerseLine(
                                        version: ver,
                                        text: bibleProvider.verseTextFor(
                                              ver, bookKey, chNum, vNum) ??
                                            '—',
                                        multi: versions.length > 1,
                                      ),
                                  ],
                                ),
                              ),
                              IconButton(
                                icon: Icon(
                                  isBookmarked
                                      ? Icons.bookmark
                                      : Icons.bookmark_border,
                                  size: 18,
                                  color: isBookmarked
                                      ? Colors.indigo
                                      : Colors.grey,
                                ),
                                onPressed: () async {
                                  final primary = bibleProvider.verseTextFor(
                                          versions.first,
                                          bookKey,
                                          chNum,
                                          vNum) ??
                                      '';
                                  final snippet =
                                      '$vNum ${primary.length > 30 ? '${primary.substring(0, 30)}...' : primary}';
                                  final bm = BibleBookmark(
                                    bookIndex: widget.bookIndex,
                                    chapterIndex: widget.chapterIndex,
                                    verseIndex: vNum,
                                    snippet: snippet,
                                    createdAt: DateTime.now(),
                                  );
                                  if (isBookmarked) {
                                    await bibleProvider.removeBookmark(bm);
                                  } else {
                                    await bibleProvider.addBookmark(bm);
                                  }
                                },
                                padding: EdgeInsets.zero,
                                constraints: const BoxConstraints(
                                    minWidth: 32, minHeight: 32),
                              ),
                            ],
                          ),
                        );
                      },
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

class _VersionVerseLine extends StatelessWidget {
  final BibleVersionId version;
  final String text;
  final bool multi;

  const _VersionVerseLine({
    required this.version,
    required this.text,
    required this.multi,
  });

  Color get _badgeColor {
    switch (version) {
      case BibleVersionId.krv:
        return Colors.indigo;
      case BibleVersionId.kjv:
        return Colors.brown;
      case BibleVersionId.asv:
        return Colors.teal;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Semantics(
        label: '${version.code}: $text',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (multi)
              Container(
                margin: const EdgeInsets.only(bottom: 2),
                padding:
                    const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                decoration: BoxDecoration(
                  color: _badgeColor.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  version.shortLabel,
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    color: _badgeColor,
                  ),
                ),
              ),
            Text(
              text,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    fontSize: 16.5,
                    height: 1.55,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
