import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';

class HymnDetailScreen extends StatelessWidget {
  final Hymn hymn;

  const HymnDetailScreen({super.key, required this.hymn});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    return Scaffold(
      appBar: AppBar(
        title: Text('${hymn.number}. ${hymn.title}'),
        actions: [
          Consumer<BibleProvider>(
            builder: (context, provider, _) {
              final isFav = provider.isHymnFavorite(hymn.id);
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
        padding: EdgeInsets.all(pad),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Consumer<BibleProvider>(
              builder: (context, provider, _) {
                final isFav = provider.isHymnFavorite(hymn.id);
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (isFav)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        margin: const EdgeInsets.only(bottom: 8),
                        decoration: BoxDecoration(
                          color: Colors.indigo.withAlpha(25),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Text('⭐ 즐겨찾기', style: TextStyle(color: Colors.indigo, fontSize: 12)),
                      ),
                    Text(
                      hymn.title,
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                            fontWeight: isFav ? FontWeight.bold : FontWeight.normal,
                            color: Colors.indigo,
                          ),
                    ),
                  ],
                );
              },
            ),
            const SizedBox(height: 8),
            Text('카테고리: ${hymn.category}', style: const TextStyle(color: Colors.grey)),
            if (hymn.author != null || hymn.composer != null || hymn.year != null)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  [
                    if (hymn.author != null) '작사: ${hymn.author}',
                    if (hymn.composer != null) '작곡: ${hymn.composer}',
                    if (hymn.year != null) hymn.year,
                  ].join('  •  '),
                  style: const TextStyle(fontSize: 13, color: Colors.grey),
                ),
              ),
            if (hymn.titleEn != null && hymn.titleEn!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text('English: ${hymn.titleEn}', style: const TextStyle(fontSize: 13, color: Colors.grey)),
              ),
            if (hymn.source != null && hymn.source!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  hymn.source!,
                  style: const TextStyle(fontSize: 11, color: Colors.indigo, fontStyle: FontStyle.italic),
                ),
              ),
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
