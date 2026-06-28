import 'package:flutter/material.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('이 성경앱에 대해서')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '한국어 성경 앱',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text('완전 무료 • 오프라인 • Public Domain (개역개정)'),
              SizedBox(height: 16),
              Text(
                '주요 기능',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              Text('• 성경 읽기 (구약/신약 전체, 검색, 북마크)\n'
                  '• 찬송가 (가사 + 악보 placeholder)\n'
                  '• 사도신경, 주기도문, 교독문\n'
                  '• 접근성 (큰 글씨, 다크모드 준비)'),
              SizedBox(height: 16),
              Text(
                '데이터 출처',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              Text('한국어 성경: Public Domain (개역개정 등)\n'
                  '찬송가/신경/기도문: 공개 자료 기반 샘플'),
              SizedBox(height: 16),
              Text('버전: 1.0.0+1\nFlutter + Hive'),
              SizedBox(height: 24),
              Text('피드백 및 기여 환영'),
            ],
          ),
        ),
      ),
    );
  }
}
