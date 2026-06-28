import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/theme_provider.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('설정')),
      body: Consumer<ThemeProvider>(
        builder: (context, themeProvider, _) {
          return ListView(
            children: [
              ListTile(
                leading: const Icon(Icons.text_fields),
                title: const Text('글꼴 크기 (앱 배율)'),
                subtitle: Text('현재: ${(themeProvider.textScaleFactor * 100).toStringAsFixed(0)}% (시스템 배율과 합산 적용)'),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    const Text('작게'),
                    Expanded(
                      child: Slider(
                        value: themeProvider.textScaleFactor,
                        min: 0.8,
                        max: 2.0,
                        divisions: 12,
                        label: '${(themeProvider.textScaleFactor * 100).toStringAsFixed(0)}%',
                        onChanged: (value) {
                          themeProvider.setTextScaleFactor(value);
                        },
                      ),
                    ),
                    const Text('크게'),
                  ],
                ),
              ),
              ListTile(
                title: const Text('시스템 글꼴 크기로 초기화'),
                onTap: () => themeProvider.resetToSystem(),
              ),
              const Divider(),
              SwitchListTile(
                title: const Text('다크 모드'),
                subtitle: Text(themeProvider.isDarkMode ? '다크 모드 활성화' : '라이트 모드'),
                value: themeProvider.isDarkMode,
                onChanged: (value) {
                  themeProvider.toggleTheme(value);
                },
              ),
              SwitchListTile(
                title: const Text('고대비 모드'),
                subtitle: const Text('접근성 향상 (더 강한 대비)'),
                value: themeProvider.highContrast,
                onChanged: (value) {
                  themeProvider.toggleHighContrast(value);
                },
              ),
              const Divider(),
              const ListTile(
                title: Text('버전: 1.0.0 (개역개정)'),
              ),
              const ListTile(
                title: Text('데이터 출처: Public Domain'),
              ),
            ],
          );
        },
      ),
    );
  }
}
