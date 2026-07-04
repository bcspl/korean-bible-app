import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
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

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    var hymns = provider.hymns.where((h) {
      final q = _searchQuery.toLowerCase();
      return h.title.toLowerCase().contains(q) ||
          h.lyrics.toLowerCase().contains(q);
    }).toList();

    if (_showFavoritesOnly) {
      hymns = provider.favoriteHymns.where((h) {
        final q = _searchQuery.toLowerCase();
        return h.title.toLowerCase().contains(q) ||
            h.lyrics.toLowerCase().contains(q);
      }).toList();
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('찬송가'),
        actions: [
          IconButton(
            icon: Icon(_showFavoritesOnly ? Icons.favorite : Icons.favorite_border),
            onPressed: () => setState(() => _showFavoritesOnly = !_showFavoritesOnly),
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
              Padding(
                padding: EdgeInsets.all(pad),
                child: TextField(
              decoration: const InputDecoration(
                hintText: '찬송가 제목 또는 가사 검색...',
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
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            child: Text(
              '${hymns.length}곡 표시 중 (전체 ${provider.hymns.length}곡, Public Domain)',
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
                      return ListTile(
                        key: ValueKey(h.id),
                        tileColor: isFav ? Colors.indigo.withAlpha(25) : null,
                        leading: const Icon(Icons.music_note, color: Colors.indigo),
                        title: Text(
                          '${h.number}. ${h.title}',
                          style: isFav ? const TextStyle(fontWeight: FontWeight.bold) : null,
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(h.category),
                            if (h.titleEn != null && h.titleEn!.isNotEmpty)
                              Text(h.titleEn!, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                            if (h.author != null && h.author!.isNotEmpty)
                              Text(h.author!, style: const TextStyle(fontSize: 11, color: Colors.grey)),
                          ],
                        ),
                        trailing: IconButton(
                          icon: Icon(isFav ? Icons.favorite : Icons.favorite_border, color: isFav ? Colors.red : null),
                          onPressed: () {
                            provider.toggleHymnFavorite(h.id);
                          },
                        ),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => HymnDetailScreen(hymn: h),
                            ),
                          );
                        },
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
                maxLines: 2,
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

