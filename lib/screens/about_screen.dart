import 'package:flutter/material.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    return Scaffold(
      appBar: AppBar(title: const Text('이 성경앱에 대해서')),
      body: Padding(
        padding: EdgeInsets.all(pad),
        child: Semantics(
          label: '이 성경앱에 대해서 안내',
          child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '한국어 성경 앱',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text('완전 무료 • 오프라인 • Public Domain (개역한글 / KRV)'),
              SizedBox(height: 16),
              Text(
                '주요 기능',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              Text('• 성경 읽기 (구약/신약 전체, 검색, 북마크)\n'
                  '• 찬송가 (Public Domain 전 곡 · 한/영 가사 · 유래)\n'
                  '• 사도신경, 주기도문, 교독문\n'
                  '• 접근성 (큰 글씨, 다크모드 준비)'),
              SizedBox(height: 16),
              Text(
                '데이터 출처',
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              Text('성경: 개역한글(KRV) · KJV · ASV (모두 Public Domain)\n'
                  'KRV: 성경전서 개역한글판 (대한성서공회) PD\n'
                  'KJV/ASV: open-bibles 등 PD 원문 검증\n'
                  '병렬 열람: 절 단위 최대 3개 역본 동시 표시\n'
                  '찬송가·교독문: PD 전용 (찬송가 공식 판권·개역개정 미사용)'),
              SizedBox(height: 16),
              Text('버전: 1.0.0+1\nFlutter + Hive'),
              SizedBox(height: 24),
              Text('피드백 및 기여 환영'),
            ],
          ),
        ),
        ),
      ),
    );
  }
}
