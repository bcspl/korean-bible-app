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
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              decoration: const InputDecoration(
                hintText: '찬송가 제목 또는 가사 검색...',
                prefixIcon: Icon(Icons.search),
              ),
              onChanged: (v) => setState(() => _searchQuery = v),
            ),
          ),
          Expanded(
            child: hymns.isEmpty
                ? const Center(child: Text('일치하는 찬송가가 없습니다.'))
                : ListView.builder(
                    itemCount: hymns.length,
                    itemBuilder: (context, i) {
                      final h = hymns[i];
                      final isFav = provider.favoriteHymns.any((f) => f.id == h.id);
                      return ListTile(
                        leading: const Icon(Icons.music_note, color: Colors.indigo),
                        title: Text('${h.number}. ${h.title}'),
                        subtitle: Text(h.category),
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
        ],
      ),
    );
  }
}
