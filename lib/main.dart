import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';

import 'models/bible_book.dart';
import 'models/bible_bookmark.dart';
import 'models/bible_chapter.dart';
import 'models/bible_verse.dart';
import 'providers/bible_provider.dart';
import 'providers/theme_provider.dart';
import 'screens/main_screen.dart';
import 'services/bible_data_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();

  // Register Hive adapters for Bible data models
  Hive.registerAdapter(BibleVerseAdapter());
  Hive.registerAdapter(BibleChapterAdapter());
  Hive.registerAdapter(BibleBookAdapter());
  Hive.registerAdapter(BibleBookmarkAdapter());

  // Load JSON data and seed Hive (Phase 1 - JSON loader)
  final bibleService = BibleDataService();
  await bibleService.loadAndSeedBibleData();

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => BibleProvider()..loadBooks(),
        ),
        ChangeNotifierProvider(
          create: (_) => ThemeProvider(),
        ),
      ],
      child: const KoreanBibleApp(),
    ),
  );
}

class KoreanBibleApp extends StatelessWidget {
  const KoreanBibleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, _) {
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
          darkTheme: ThemeData(
            brightness: Brightness.dark,
            primarySwatch: Colors.indigo,
            textTheme: const TextTheme(
              bodyLarge: TextStyle(fontSize: 18.0),
            ),
          ),
          themeMode: themeProvider.themeMode,
          builder: (context, child) {
            final mediaQuery = MediaQuery.of(context);
            final effectiveScale = themeProvider.textScaleFactor * mediaQuery.textScaler.scale(1.0);
            return MediaQuery(
              data: mediaQuery.copyWith(
                textScaler: TextScaler.linear(effectiveScale),
              ),
              child: child!,
            );
          },
          home: const HomeScreen(),
        );
      },
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const MainScreen();  // Phase 3: Bottom nav with 성경 / 찬송가 / 북마크 / 설정
  }
}

