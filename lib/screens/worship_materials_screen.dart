import 'package:flutter/material.dart';
import 'creed_screen.dart';
import 'lords_prayer_screen.dart';
import 'responsive_reading_screen.dart';

class WorshipMaterialsScreen extends StatelessWidget {
  const WorshipMaterialsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    return Scaffold(
      appBar: AppBar(title: const Text('예배 자료')),
      body: Padding(
        padding: EdgeInsets.symmetric(horizontal: pad),
        child: Semantics(
          label: '예배 자료 목록',
          child: ListView(
            children: [
              Semantics(
                button: true,
                label: '사도신경, 개역한글과 영어',
                child: ListTile(
                  leading: const Icon(Icons.account_balance),
                  title: const Text('사도신경'),
                  subtitle: const Text('개역한글 · KJV · ASV'),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CreedScreen()),
                  ),
                ),
              ),
              Semantics(
                button: true,
                label: '주기도문, 개역한글 KJV ASV',
                child: ListTile(
                  leading: const Icon(Icons.people),
                  title: const Text('주기도문'),
                  subtitle: const Text('개역한글 · KJV · ASV'),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const LordsPrayerScreen()),
                  ),
                ),
              ),
              Semantics(
                button: true,
                label: '교독문, KRV KJV ASV, 인도자와 회중 구분',
                child: ListTile(
                  leading: const Icon(Icons.menu_book),
                  title: const Text('교독문'),
                  subtitle: const Text('시편·성탄·부활·이사야·누가 · KRV/KJV/ASV · PD'),
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const ResponsiveReadingScreen()),
                  ),
                ),
              ),
              const Divider(),
              const ListTile(
                title: Text('힌트: 찬송가는 별도 탭에서 이용하세요'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
