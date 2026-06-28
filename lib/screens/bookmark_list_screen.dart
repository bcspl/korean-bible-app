import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';
import 'verse_viewer_screen.dart';

class BookmarkListScreen extends StatelessWidget {
  const BookmarkListScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final bookmarks = provider.bookmarks;

    return Scaffold(
      appBar: AppBar(
        title: const Text('북마크'),
      ),
      body: bookmarks.isEmpty
          ? const Center(
              child: Text('저장된 북마크가 없습니다.\n성경 본문에서 북마크 아이콘을 눌러 추가하세요.'),
            )
          : ListView.builder(
              itemCount: bookmarks.length,
              itemBuilder: (context, index) {
                final bm = bookmarks[index];
                final isVerse = bm.isVerseBookmark;
                return ListTile(
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
                  trailing: IconButton(
                    icon: const Icon(Icons.delete_outline),
                    onPressed: () async {
                      await provider.removeBookmark(bm);
                    },
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
                );
              },
            ),
    );
  }
}
