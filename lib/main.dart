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

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();

  // Register Hive adapters for Bible data models
  Hive.registerAdapter(BibleVerseAdapter());
  Hive.registerAdapter(BibleChapterAdapter());
  Hive.registerAdapter(BibleBookAdapter());
  Hive.registerAdapter(BibleBookmarkAdapter());

  // Note: Bible data seeding moved to BibleProvider.loadBooks() to avoid blocking app start.
  // UI will show loading indicator while large JSON/Hive seed happens on first run.

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) {
            final provider = BibleProvider();
            // Fire-and-forget load; errors are caught inside loadBooks() and exposed via hasError
            provider.loadBooks().catchError((_) {});
            return provider;
          },
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
        final isHighContrast = themeProvider.highContrast;
        final darkBase = ThemeData(
          brightness: Brightness.dark,
          primarySwatch: Colors.indigo,
          scaffoldBackgroundColor: isHighContrast ? Colors.black : const Color(0xFF121212),
          cardColor: isHighContrast ? const Color(0xFF1A1A1A) : const Color(0xFF2C2C2C),
          textTheme: TextTheme(
            bodyLarge: TextStyle(
              fontSize: 18.0,
              color: isHighContrast ? Colors.white : const Color(0xFFEEEEEE),
              height: 1.5,
            ),
            bodyMedium: TextStyle(
              color: isHighContrast ? const Color(0xFFCCCCCC) : const Color(0xFFBBBBBB),
            ),
          ),
          colorScheme: ColorScheme.dark(
            primary: Colors.indigo,
            secondary: Colors.indigoAccent,
            surface: isHighContrast ? const Color(0xFF1A1A1A) : const Color(0xFF2C2C2C),
            onSurface: isHighContrast ? Colors.white : const Color(0xFFEEEEEE),
          ),
          iconTheme: IconThemeData(
            color: isHighContrast ? Colors.white : const Color(0xFFBBBBBB),
          ),
        );
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
          darkTheme: darkBase,
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

