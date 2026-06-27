import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';
import 'verse_viewer_screen.dart';

class ChapterListScreen extends StatelessWidget {
  final int bookIndex;

  const ChapterListScreen({super.key, required this.bookIndex});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final book = provider.books[bookIndex];

    return Scaffold(
      appBar: AppBar(
        title: Text(provider.getBookDisplayNameForIndex(bookIndex)),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(20),
          child: Text(provider.version, style: const TextStyle(fontSize: 12, color: Colors.white70)),
        ),
      ),
      body: GridView.builder(
        padding: const EdgeInsets.all(12),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 6,  // denser grid for smaller, more tappable items
          childAspectRatio: 1.0,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        itemCount: book.chapters.length,
        itemBuilder: (context, index) {
          return InkWell(
            onTap: () {
              provider.setCurrentChapter(index);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => VerseViewerScreen(bookIndex: bookIndex, chapterIndex: index),
                ),
              );
            },
            child: Container(
              decoration: BoxDecoration(
                color: Theme.of(context).cardColor,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.grey.shade300, width: 1),
              ),
              child: Center(
                child: Text(
                  '${index + 1}',
                  style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
