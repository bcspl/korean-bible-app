import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:provider/provider.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';

class HymnDetailScreen extends StatefulWidget {
  final Hymn hymn;

  const HymnDetailScreen({super.key, required this.hymn});

  @override
  State<HymnDetailScreen> createState() => _HymnDetailScreenState();
}

class _HymnDetailScreenState extends State<HymnDetailScreen> {
  /// 0 = Korean, 1 = English
  int _lyricsLang = 0;

  Hymn get hymn => widget.hymn;

  @override
  void initState() {
    super.initState();
    // Prefer Korean when available; otherwise English
    if (!hymn.hasKoreanLyrics && hymn.hasEnglishLyrics) {
      _lyricsLang = 1;
    }
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final showLangToggle = hymn.hasKoreanLyrics && hymn.hasEnglishLyrics;
    final lyricsText = _lyricsLang == 1 && hymn.hasEnglishLyrics
        ? hymn.displayLyricsEn
        : hymn.displayLyricsKo;

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
                  icon: Icon(
                    isFav ? Icons.favorite : Icons.favorite_border,
                    color: isFav ? Colors.red : null,
                  ),
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
            // PD badge
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.green.shade50,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Colors.green.shade600),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.verified_user,
                          size: 16, color: Colors.green.shade700),
                      const SizedBox(width: 4),
                      Text(
                        hymn.license ?? 'Public Domain',
                        style: TextStyle(
                          color: Colors.green.shade800,
                          fontWeight: FontWeight.bold,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: Colors.indigo.withAlpha(20),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '무료 · 라이선스 제한 없음',
                    style: TextStyle(
                      color: Colors.indigo.shade700,
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                if (hymn.category.isNotEmpty)
                  Chip(
                    label: Text(hymn.category, style: const TextStyle(fontSize: 12)),
                    visualDensity: VisualDensity.compact,
                    materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Consumer<BibleProvider>(
              builder: (context, provider, _) {
                final isFav = provider.isHymnFavorite(hymn.id);
                return Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (isFav)
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 4),
                        margin: const EdgeInsets.only(bottom: 8),
                        decoration: BoxDecoration(
                          color: Colors.indigo.withAlpha(25),
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Text(
                          '⭐ 즐겨찾기',
                          style: TextStyle(color: Colors.indigo, fontSize: 12),
                        ),
                      ),
                    Text(
                      hymn.title,
                      style:
                          Theme.of(context).textTheme.headlineSmall?.copyWith(
                                fontWeight: isFav
                                    ? FontWeight.bold
                                    : FontWeight.w600,
                                color: Colors.indigo,
                              ),
                    ),
                  ],
                );
              },
            ),
            if (hymn.titleEn != null && hymn.titleEn!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  hymn.titleEn!,
                  style: const TextStyle(fontSize: 15, color: Colors.black54),
                ),
              ),
            if (hymn.author != null ||
                hymn.composer != null ||
                hymn.year != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  [
                    if (hymn.author != null && hymn.author!.isNotEmpty)
                      '작사: ${hymn.author}',
                    if (hymn.composer != null && hymn.composer!.isNotEmpty)
                      '작곡: ${hymn.composer}',
                    if (hymn.year != null && hymn.year!.isNotEmpty)
                      '연도: ${hymn.year}',
                  ].join('  ·  '),
                  style: const TextStyle(fontSize: 13, color: Colors.grey),
                ),
              ),

            // History / origin
            if (hymn.history != null && hymn.history!.trim().isNotEmpty) ...[
              const Divider(height: 28),
              const Text(
                '유래 · 역사',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              const SizedBox(height: 8),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.amber.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.amber.shade200),
                ),
                child: Text(
                  hymn.history!,
                  style: const TextStyle(fontSize: 14, height: 1.55),
                ),
              ),
            ],

            // License explanation
            const Divider(height: 28),
            const Text(
              '라이선스 (Public Domain)',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.green.shade50,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.green.shade200),
              ),
              child: Text(
                hymn.licenseNote?.trim().isNotEmpty == true
                    ? hymn.licenseNote!
                    : '이 찬송은 Public Domain입니다. 저작권 비용·이용 제한 없이 개인 예배·교육·오프라인에서 무료로 사용할 수 있습니다. 한국찬송가공회 공식 판권과 무관합니다.',
                style: TextStyle(
                  fontSize: 13,
                  height: 1.5,
                  color: Colors.green.shade900,
                ),
              ),
            ),
            if (hymn.source != null && hymn.source!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  '출처: ${hymn.source}',
                  style: const TextStyle(
                    fontSize: 11,
                    color: Colors.indigo,
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ),

            const Divider(height: 32),
            Row(
              children: [
                const Text(
                  '가사',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                const Spacer(),
                if (showLangToggle)
                  SegmentedButton<int>(
                    segments: const [
                      ButtonSegment(value: 0, label: Text('한국어')),
                      ButtonSegment(value: 1, label: Text('English')),
                    ],
                    selected: {_lyricsLang},
                    onSelectionChanged: (s) {
                      setState(() => _lyricsLang = s.first);
                    },
                    style: const ButtonStyle(
                      visualDensity: VisualDensity.compact,
                      tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                    ),
                  ),
              ],
            ),
            if (!showLangToggle && hymn.hasEnglishLyrics && !hymn.hasKoreanLyrics)
              const Padding(
                padding: EdgeInsets.only(top: 4),
                child: Text(
                  'English lyrics (한국어 전문 미수록)',
                  style: TextStyle(fontSize: 12, color: Colors.grey),
                ),
              ),
            const SizedBox(height: 8),
            Semantics(
              label: _lyricsLang == 1 ? 'English hymn lyrics' : '찬송가 가사',
              child: Text(
                lyricsText,
                style: const TextStyle(fontSize: 16, height: 1.65),
              ),
            ),

            // Show other language below when only one toggle state and both exist
            // (user can switch via toggle — no duplicate needed)

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
              style: TextStyle(
                fontSize: 11,
                color: Colors.grey.shade600,
                fontStyle: FontStyle.italic,
              ),
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
