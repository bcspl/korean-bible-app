import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/bible_bookmark.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';
import 'hymn_detail_screen.dart';
import 'verse_viewer_screen.dart';

/// Combined view: Bible bookmarks + favorite hymns.
class BookmarkListScreen extends StatelessWidget {
  const BookmarkListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final bookmarks = provider.bookmarks;
    final favoriteHymns = provider.favoriteHymns;
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final isEmpty = bookmarks.isEmpty && favoriteHymns.isEmpty;

    return Scaffold(
      appBar: AppBar(
        title: const Text('북마크'),
      ),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: pad),
        child: isEmpty
            ? const Center(
                child: Text(
                  '저장된 항목이 없습니다.\n\n'
                  '• 성경 본문에서 북마크 아이콘을 눌러 추가\n'
                  '• 찬송가에서 ♥ 아이콘으로 즐겨찾기',
                  textAlign: TextAlign.center,
                ),
              )
            : ListView(
                children: [
                  if (bookmarks.isNotEmpty) ...[
                    _SectionHeader(
                      icon: Icons.menu_book,
                      title: '성경 북마크',
                      count: bookmarks.length,
                    ),
                    ...bookmarks.map(
                      (bm) => _BibleBookmarkTile(
                        bookmark: bm,
                        onRemove: () => provider.removeBookmark(bm),
                      ),
                    ),
                    const SizedBox(height: 8),
                  ],
                  if (favoriteHymns.isNotEmpty) ...[
                    _SectionHeader(
                      icon: Icons.music_note,
                      title: '즐겨찾기 찬송가',
                      count: favoriteHymns.length,
                    ),
                    ...favoriteHymns.map(
                      (h) => _FavoriteHymnTile(
                        hymn: h,
                        onUnfavorite: () => provider.toggleHymnFavorite(h.id),
                      ),
                    ),
                    const SizedBox(height: 16),
                  ],
                ],
              ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final IconData icon;
  final String title;
  final int count;

  const _SectionHeader({
    required this.icon,
    required this.title,
    required this.count,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Padding(
      padding: const EdgeInsets.fromLTRB(4, 16, 4, 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: theme.colorScheme.primary),
          const SizedBox(width: 8),
          Text(
            title,
            style: theme.textTheme.titleMedium?.copyWith(
              fontWeight: FontWeight.bold,
              color: theme.colorScheme.primary,
            ),
          ),
          const SizedBox(width: 8),
          Semantics(
            label: '$count개',
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: theme.colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '$count',
                style: theme.textTheme.labelMedium?.copyWith(
                  color: theme.colorScheme.onPrimaryContainer,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BibleBookmarkTile extends StatelessWidget {
  final BibleBookmark bookmark;
  final Future<void> Function() onRemove;

  const _BibleBookmarkTile({
    required this.bookmark,
    required this.onRemove,
  });

  @override
  Widget build(BuildContext context) {
    final bm = bookmark;
    final isVerse = bm.isVerseBookmark;
    return Semantics(
      button: true,
      label: isVerse
          ? '절 북마크 ${bm.snippet}'
          : '장 북마크 ${bm.snippet}',
      child: ListTile(
        leading: Icon(
          isVerse ? Icons.bookmark : Icons.bookmark_border,
          color: Colors.indigo,
        ),
        title: Text(bm.snippet),
        subtitle: Text(
          isVerse
              ? '절 북마크 • ${bm.bookIndex + 1}권 ${bm.chapterIndex + 1}장 ${bm.verseIndex}절'
              : '장 북마크 • ${bm.bookIndex + 1}권 ${bm.chapterIndex + 1}장',
        ),
        trailing: Semantics(
          button: true,
          label: '북마크 삭제',
          child: IconButton(
            icon: const Icon(Icons.delete_outline),
            onPressed: () async {
              await onRemove();
            },
          ),
        ),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => VerseViewerScreen(
                bookIndex: bm.bookIndex,
                chapterIndex: bm.chapterIndex,
                initialVerseIndex: bm.verseIndex,
              ),
            ),
          );
        },
      ),
    );
  }
}

class _FavoriteHymnTile extends StatelessWidget {
  final Hymn hymn;
  final Future<void> Function() onUnfavorite;

  const _FavoriteHymnTile({
    required this.hymn,
    required this.onUnfavorite,
  });

  String _hymnSubtitle(Hymn h) {
    final parts = <String>[
      'PD 무료',
      if (h.category.isNotEmpty) h.category,
      if (h.author != null && h.author!.isNotEmpty) h.author!,
    ];
    return parts.join(' • ');
  }

  @override
  Widget build(BuildContext context) {
    final h = hymn;
    return Semantics(
      button: true,
      label: '즐겨찾기 찬송가 ${h.number}. ${h.title}',
      child: ListTile(
        leading: const Icon(Icons.favorite, color: Colors.red),
        title: Text('${h.number}. ${h.title}'),
        subtitle: Text(_hymnSubtitle(h)),
        trailing: Semantics(
          button: true,
          label: '즐겨찾기 해제',
          child: IconButton(
            icon: const Icon(Icons.favorite, color: Colors.red),
            tooltip: '즐겨찾기 해제',
            onPressed: () async {
              await onUnfavorite();
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('${h.number}. ${h.title} 즐겨찾기 해제'),
                    duration: const Duration(seconds: 2),
                  ),
                );
              }
            },
          ),
        ),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => HymnDetailScreen(hymn: h),
            ),
          );
        },
      ),
    );
  }
}
