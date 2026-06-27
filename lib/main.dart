import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';

import 'models/bible_book.dart';
import 'models/bible_chapter.dart';
import 'models/bible_verse.dart';
import 'providers/bible_provider.dart';
import 'screens/book_list_screen.dart';
import 'services/bible_data_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();

  // Register Hive adapters for Bible data models
  Hive.registerAdapter(BibleVerseAdapter());
  Hive.registerAdapter(BibleChapterAdapter());
  Hive.registerAdapter(BibleBookAdapter());

  // Load JSON data and seed Hive (Phase 1 - JSON loader)
  final bibleService = BibleDataService();
  await bibleService.loadAndSeedBibleData();

  runApp(
    ChangeNotifierProvider(
      create: (_) => BibleProvider()..loadBooks(),
      child: const KoreanBibleApp(),
    ),
  );
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
    return const BookListScreen();  // Phase 2: 기본 성경 읽기 UI entry
  }
}

