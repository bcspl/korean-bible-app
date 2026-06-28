import 'package:flutter/material.dart';
import 'creed_screen.dart';
import 'lords_prayer_screen.dart';
import 'responsive_reading_screen.dart';

class WorshipMaterialsScreen extends StatelessWidget {
  const WorshipMaterialsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('예배 자료')),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.account_balance),
            title: const Text('사도신경'),
            subtitle: const Text('개역한글 / 개역개정'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const CreedScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.people),
            title: const Text('주기도문'),
            subtitle: const Text('개역한글 / 개역개정'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const LordsPrayerScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.menu_book),
            title: const Text('교독문'),
            subtitle: const Text('인도자/회중 구분'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ResponsiveReadingScreen())),
          ),
          const Divider(),
          const ListTile(
            title: Text('힌트: 찬송가는 별도 탭에서 이용하세요'),
          ),
        ],
      ),
    );
  }
}
