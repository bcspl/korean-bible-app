import 'package:flutter/material.dart';

class ResponsiveReadingScreen extends StatelessWidget {
  const ResponsiveReadingScreen({super.key});

  final List<Map<String, String>> readings = const [
    {
      'title': '교독문 1 (시편 23편)',
      'content': '인도자: 여호와는 나의 목자시니\n회중: 내가 부족함이 없으리로다\n\n인도자: 그가 나를 푸른 초장에 누이시며\n회중: 잔잔한 물가로 인도하시는도다',
    },
    {
      'title': '교독문 2 (시편 100편)',
      'content': '인도자: 온 땅이여 여호와께 즐거이 부를지어다\n회중: 기쁨으로 여호와를 섬기며\n\n인도자: 노래하면서 그 앞에 나아갈지어다\n회중: 여호와가 우리 하나님이심을 알지어다',
    },
    {
      'title': '교독문 3 (시편 121편)',
      'content': '인도자: 내가 산을 향하여 눈을 들리라\n회중: 나의 도움이 어디서 올까\n\n인도자: 나의 도움이 천지를 지으신 여호와에게서로다\n회중: 여호와께서 너를 지켜 실족하지 않게 하시며',
    },
  ];

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);

    return Scaffold(
      appBar: AppBar(title: const Text('교독문')),
      body: Semantics(
        label: '교독문 목록',
        child: ListView.builder(
          padding: EdgeInsets.symmetric(horizontal: pad, vertical: 8),
          itemCount: readings.length,
          itemBuilder: (context, i) {
            final r = readings[i];
            final preview = r['content']!.length > 50
                ? '${r['content']!.substring(0, 50)}...'
                : r['content']!;
            return Semantics(
              button: true,
              label: '${r['title']}, 탭하여 전체 보기',
              child: Card(
                margin: const EdgeInsets.symmetric(vertical: 4),
                child: ListTile(
                  title: Text(r['title']!),
                  subtitle: Text(preview),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => _ReadingDetail(
                          title: r['title']!,
                          content: r['content']!,
                        ),
                      ),
                    );
                  },
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _ReadingDetail extends StatelessWidget {
  final String title;
  final String content;

  const _ReadingDetail({required this.title, required this.content});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final lines = content.split('\n');

    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Semantics(
        label: '$title 본문',
        child: ListView.builder(
          padding: EdgeInsets.all(pad),
          itemCount: lines.length,
          itemBuilder: (c, i) {
            if (lines[i].trim().isEmpty) {
              return const SizedBox(height: 8);
            }
            final isLeader = lines[i].startsWith('인도자:');
            return Semantics(
              label: lines[i],
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Text(
                  lines[i],
                  style: TextStyle(
                    fontSize: 17,
                    fontWeight: isLeader ? FontWeight.bold : FontWeight.normal,
                    color: isLeader ? Colors.indigo : null,
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
