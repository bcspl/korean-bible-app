import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';

class HymnDetailScreen extends StatelessWidget {
  final Hymn hymn;

  const HymnDetailScreen({super.key, required this.hymn});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${hymn.number}. ${hymn.title}'),
        actions: [
          Consumer<BibleProvider>(
            builder: (context, provider, _) {
              final isFav = provider.favoriteHymns.any((f) => f.id == hymn.id);
              return IconButton(
                icon: Icon(isFav ? Icons.favorite : Icons.favorite_border, color: isFav ? Colors.red : null),
                onPressed: () => provider.toggleHymnFavorite(hymn.id),
                tooltip: isFav ? '즐겨찾기 해제' : '즐겨찾기 추가',
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              hymn.title,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.indigo,
                  ),
            ),
            const SizedBox(height: 8),
            Text('카테고리: ${hymn.category}', style: const TextStyle(color: Colors.grey)),
            const Divider(height: 32),
            const Text(
              '가사',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Text(
              hymn.lyrics,
              style: const TextStyle(fontSize: 16, height: 1.6),
            ),
            const Divider(height: 32),
            const Text(
              '악보',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Container(
              height: 300,
              width: double.infinity,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey.shade300),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.image, size: 48, color: Colors.grey),
                    const SizedBox(height: 8),
                    Text(
                      '악보 이미지: ${hymn.scoreImage.isNotEmpty ? hymn.scoreImage : "없음 (PD 데이터)"}',
                      style: const TextStyle(color: Colors.grey),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      '(실제 이미지 파일을 assets/images/hymns/ 에 추가하거나 텍스트 악보 사용)',
                      style: TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
