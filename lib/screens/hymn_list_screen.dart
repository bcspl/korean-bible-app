import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/hymn.dart';
import '../providers/bible_provider.dart';
import 'hymn_detail_screen.dart';

class HymnListScreen extends StatefulWidget {
  const HymnListScreen({super.key});

  @override
  State<HymnListScreen> createState() => _HymnListScreenState();
}

class _HymnListScreenState extends State<HymnListScreen> {
  String _searchQuery = '';
  bool _showFavoritesOnly = false;
  Timer? _debounce;

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  void _showPdInfo(BuildContext context, BibleProvider provider) {
    final note = provider.hymnSourceNote.isNotEmpty
        ? provider.hymnSourceNote
        : '모든 찬송은 Public Domain(저작권 만료·자유 이용)입니다. '
            '라이선스 비용·이용 제한 없이 개인 예배·교육·오프라인에서 무료로 사용할 수 있습니다. '
            '한국찬송가공회 공식 판권과 무관합니다.';
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Row(
          children: [
            Icon(Icons.verified_user, color: Colors.green),
            SizedBox(width: 8),
            Expanded(child: Text('Public Domain 찬송')),
          ],
        ),
        content: SingleChildScrollView(
          child: Text(note, style: const TextStyle(height: 1.5)),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    bool matches(Hymn h) {
      final q = _searchQuery.toLowerCase();
      if (q.isEmpty) return true;
      return h.number.toLowerCase().contains(q) ||
          h.title.toLowerCase().contains(q) ||
          (h.titleEn?.toLowerCase().contains(q) ?? false) ||
          h.lyrics.toLowerCase().contains(q) ||
          (h.lyricsKo?.toLowerCase().contains(q) ?? false) ||
          (h.lyricsEn?.toLowerCase().contains(q) ?? false) ||
          (h.author?.toLowerCase().contains(q) ?? false) ||
          (h.composer?.toLowerCase().contains(q) ?? false) ||
          (h.history?.toLowerCase().contains(q) ?? false) ||
          h.category.toLowerCase().contains(q);
    }

    var hymns = _showFavoritesOnly
        ? provider.favoriteHymns.where(matches).toList()
        : provider.hymns.where(matches).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('찬송가'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            onPressed: () => _showPdInfo(context, provider),
            tooltip: 'Public Domain 안내',
          ),
          IconButton(
            icon: Icon(
                _showFavoritesOnly ? Icons.favorite : Icons.favorite_border),
            onPressed: () =>
                setState(() => _showFavoritesOnly = !_showFavoritesOnly),
            tooltip: '즐겨찾기만 보기',
          ),
        ],
      ),
      body: Builder(
        builder: (context) {
          final width = MediaQuery.of(context).size.width;
          final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 8.0);
          return Column(
            children: [
              // PD banner
              Material(
                color: Colors.green.shade50,
                child: InkWell(
                  onTap: () => _showPdInfo(context, provider),
                  child: Padding(
                    padding: EdgeInsets.symmetric(
                        horizontal: pad, vertical: 10),
                    child: Row(
                      children: [
                        Icon(Icons.verified_user,
                            color: Colors.green.shade700, size: 20),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            '전 곡 Public Domain · 무료 · 라이선스 제한 없음',
                            style: TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                              color: Colors.green.shade900,
                            ),
                          ),
                        ),
                        Icon(Icons.chevron_right,
                            size: 18, color: Colors.green.shade700),
                      ],
                    ),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(pad),
                child: TextField(
                  decoration: const InputDecoration(
                    hintText: '제목·가사·작사·작곡 검색...',
                    prefixIcon: Icon(Icons.search),
                  ),
                  onChanged: (v) {
                    if (_debounce?.isActive ?? false) _debounce!.cancel();
                    _debounce = Timer(const Duration(milliseconds: 250), () {
                      if (mounted) {
                        setState(() => _searchQuery = v);
                      }
                    });
                  },
                ),
              ),
              Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                child: Text(
                  '${hymns.length}곡 표시 중 (전체 ${provider.hymns.length}곡 · 전부 PD)',
                  style: const TextStyle(fontSize: 12, color: Colors.grey),
                ),
              ),
              Expanded(
                child: (hymns.isEmpty && provider.isLoading)
                    ? const Center(child: CircularProgressIndicator())
                    : hymns.isEmpty
                        ? Center(
                            child: Text(
                              _showFavoritesOnly
                                  ? '즐겨찾기한 찬송가가 없습니다.\n하트 버튼을 눌러 추가하세요.'
                                  : (_searchQuery.isNotEmpty
                                      ? '일치하는 찬송가가 없습니다.'
                                      : '찬송가 데이터가 없습니다.'),
                            ),
                          )
                        : ListView.builder(
                            itemCount: hymns.length,
                            itemBuilder: (context, i) {
                              final h = hymns[i];
                              final isFav = provider.isHymnFavorite(h.id);
                              return Semantics(
                                button: true,
                                label:
                                    '${h.number}. ${h.title}${isFav ? ", 즐겨찾기" : ""}, Public Domain',
                                child: ListTile(
                                  key: ValueKey(h.id),
                                  tileColor: isFav
                                      ? Colors.indigo.withAlpha(25)
                                      : null,
                                  leading: CircleAvatar(
                                    backgroundColor: Colors.green.shade50,
                                    child: Text(
                                      h.number,
                                      style: TextStyle(
                                        fontSize: 12,
                                        color: Colors.green.shade800,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ),
                                  title: Text(
                                    h.title,
                                    style: isFav
                                        ? const TextStyle(
                                            fontWeight: FontWeight.bold)
                                        : null,
                                  ),
                                  subtitle: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      if (h.titleEn != null &&
                                          h.titleEn!.isNotEmpty)
                                        Text(
                                          h.titleEn!,
                                          style: const TextStyle(
                                              fontSize: 12,
                                              color: Colors.grey),
                                        ),
                                      Text(
                                        [
                                          h.category,
                                          if (h.author != null &&
                                              h.author!.isNotEmpty)
                                            h.author!,
                                          if (h.year != null &&
                                              h.year!.isNotEmpty)
                                            h.year!,
                                        ].join(' · '),
                                        style: const TextStyle(
                                            fontSize: 11, color: Colors.grey),
                                      ),
                                      Text(
                                        'PD · 무료',
                                        style: TextStyle(
                                          fontSize: 11,
                                          color: Colors.green.shade700,
                                          fontWeight: FontWeight.w600,
                                        ),
                                      ),
                                    ],
                                  ),
                                  isThreeLine: true,
                                  trailing: Semantics(
                                    button: true,
                                    label: isFav ? '즐겨찾기 해제' : '즐겨찾기 추가',
                                    child: IconButton(
                                      icon: Icon(
                                        isFav
                                            ? Icons.favorite
                                            : Icons.favorite_border,
                                        color: isFav ? Colors.red : null,
                                      ),
                                      onPressed: () {
                                        provider.toggleHymnFavorite(h.id);
                                      },
                                    ),
                                  ),
                                  onTap: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (_) =>
                                            HymnDetailScreen(hymn: h),
                                      ),
                                    );
                                  },
                                ),
                              );
                            },
                          ),
              ),
              if (provider.hymnSourceNote.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Text(
                    provider.hymnSourceNote,
                    style: const TextStyle(fontSize: 10, color: Colors.grey),
                    textAlign: TextAlign.center,
                    maxLines: 3,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
            ],
          );
        },
      ),
    );
  }
}
