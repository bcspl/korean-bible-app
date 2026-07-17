import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
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
              return Semantics(
                button: true,
                label: isFav ? '즐겨찾기 해제' : '즐겨찾기 추가',
                child: IconButton(
                  icon: Icon(isFav ? Icons.favorite : Icons.favorite_border, color: isFav ? Colors.red : null),
                  onPressed: () => provider.toggleHymnFavorite(hymn.id),
                  tooltip: isFav ? '즐겨찾기 해제' : '즐겨찾기 추가',
                ),
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
            Semantics(
              label: '찬송가 가사',
              child: Text(
                hymn.lyrics,
                style: const TextStyle(fontSize: 16, height: 1.6),
              ),
            ),
            const Divider(height: 32),
            const Text(
              '악보',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Semantics(
              label: '찬송가 악보 ${hymn.number} ${hymn.title}',
              child: _HymnScoreView(scoreImage: hymn.scoreImage),
            ),
            const SizedBox(height: 8),
            Text(
              '※ 교육용 간소화 PD 스타일 오선 악보입니다. 공식 한국찬송가공회 악보가 아닙니다.',
              style: TextStyle(fontSize: 11, color: Colors.grey.shade600, fontStyle: FontStyle.italic),
            ),
          ],
        ),
      ),
    );
  }
}

/// Displays SVG/PNG hymn score from assets, or a helpful placeholder.
class _HymnScoreView extends StatelessWidget {
  final String scoreImage;

  const _HymnScoreView({required this.scoreImage});

  @override
  Widget build(BuildContext context) {
    final hasPath = scoreImage.isNotEmpty;
    final isSvg = scoreImage.toLowerCase().endsWith('.svg');

    return Container(
      width: double.infinity,
      constraints: const BoxConstraints(minHeight: 180, maxHeight: 280),
      decoration: BoxDecoration(
        color: const Color(0xFFFFFEF8),
        border: Border.all(color: Colors.grey.shade300),
        borderRadius: BorderRadius.circular(8),
      ),
      clipBehavior: Clip.antiAlias,
      child: !hasPath
          ? const Center(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Text(
                  '악보 없음\n(scripts/generate_hymn_scores.py 실행 후 재빌드)',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.grey),
                ),
              ),
            )
          : SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: SingleChildScrollView(
                child: isSvg
                    ? SvgPicture.asset(
                        scoreImage,
                        fit: BoxFit.contain,
                        placeholderBuilder: (_) => const Padding(
                          padding: EdgeInsets.all(32),
                          child: CircularProgressIndicator(),
                        ),
                      )
                    : Image.asset(
                        scoreImage,
                        fit: BoxFit.contain,
                        errorBuilder: (_, __, ___) => const Padding(
                          padding: EdgeInsets.all(24),
                          child: Text(
                            '악보 이미지를 불러올 수 없습니다.',
                            style: TextStyle(color: Colors.grey),
                          ),
                        ),
                      ),
              ),
            ),
    );
  }
}
