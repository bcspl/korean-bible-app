import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';

class VerseViewerScreen extends StatefulWidget {
  final int bookIndex;
  final int chapterIndex;

  const VerseViewerScreen({
    super.key,
    required this.bookIndex,
    required this.chapterIndex,
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
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
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
