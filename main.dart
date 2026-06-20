import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  // TODO: Register adapters for Bible data
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
        // Large fonts for accessibility
        textTheme: const TextTheme(
          bodyLarge: TextStyle(fontSize: 18.0),
        ),
      ),
      darkTheme: ThemeData.dark(),
      home: const HomeScreen(),
      localizationsDelegates: const [
        // Add Korean localization
      ],
      supportedLocales: const [
        Locale('ko', 'KR'),
      ],
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('성경')),
      body: const Center(
        child: Text('성경 읽기 화면 (Flutter 오프라인 지원)'),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.book), label: '성경'),
          BottomNavigationBarItem(icon: Icon(Icons.music_note), label: '찬양'),
          BottomNavigationBarItem(icon: Icon(Icons.mic), label: '설교'),
        ],
      ),
    );
  }
}
