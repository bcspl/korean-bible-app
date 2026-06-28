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
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('교독문')),
      body: ListView.builder(
        itemCount: readings.length,
        itemBuilder: (context, i) {
          final r = readings[i];
          return ListTile(
            title: Text(r['title']!),
            subtitle: Text('${r['content']!.substring(0, 50)}...'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => _ReadingDetail(title: r['title']!, content: r['content']!),
                ),
              );
            },
          );
        },
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
    final lines = content.split('\n');
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: lines.length,
        itemBuilder: (c, i) {
          final isLeader = lines[i].startsWith('인도자:');
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 4),
            child: Text(
              lines[i],
              style: TextStyle(
                fontSize: 17,
                fontWeight: isLeader ? FontWeight.bold : FontWeight.normal,
                color: isLeader ? Colors.indigo : null,
              ),
            ),
          );
        },
      ),
    );
  }
}
