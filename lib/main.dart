import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  // TODO: Register adapters for Bible data models when implementing full models
  // e.g. Hive.registerAdapter(BibleBookAdapter());
  runApp(const KoreanBibleApp());
}

class KoreanBibleApp extends StatelessWidget {
  const KoreanBibleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '한국어 성경',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        brightness: Brightness.light,
        // Large fonts for accessibility (as planned in docs)
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: 18.0),
        ),
      ),
      darkTheme: ThemeData.dark(),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('한국어 성경'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.menu_book, size: 64, color: Colors.indigo),
            SizedBox(height: 16),
            Text(
              '완전 무료 오프라인 한국어 성경 앱',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 8),
            Text(
              'Public Domain 데이터 사용\n'
              'Hive 로컬 저장소 준비됨\n\n'
              '다음 단계: 데이터 파싱, 책 목록, 장/절 UI 구현',
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.book), label: '성경'),
          BottomNavigationBarItem(icon: Icon(Icons.bookmark_border), label: '북마크'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: '검색'),
        ],
        currentIndex: 0,
      ),
    );
  }
}

