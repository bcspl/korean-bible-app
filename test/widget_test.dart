// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:provider/provider.dart';

import 'package:korean_bible_app/main.dart';
import 'package:korean_bible_app/models/bible_book.dart';
import 'package:korean_bible_app/models/bible_bookmark.dart';
import 'package:korean_bible_app/models/bible_chapter.dart';
import 'package:korean_bible_app/models/bible_verse.dart';
import 'package:korean_bible_app/providers/bible_provider.dart';
import 'package:korean_bible_app/providers/theme_provider.dart';

void main() {
  setUpAll(() async {
    var tempDir = await Directory.systemTemp.createTemp();
    Hive.init(tempDir.path);
    Hive.registerAdapter(BibleVerseAdapter());
    Hive.registerAdapter(BibleChapterAdapter());
    Hive.registerAdapter(BibleBookAdapter());
    Hive.registerAdapter(BibleBookmarkAdapter());
  });
  testWidgets('Korean Bible App smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame with required providers.
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => BibleProvider()),
          ChangeNotifierProvider(create: (_) => ThemeProvider()),
        ],
        child: const KoreanBibleApp(),
      ),
    );
    await tester.pump();

    // Verify that main navigation appears.
    expect(find.byIcon(Icons.menu_book), findsOneWidget);

    // Basic navigation bar check
    expect(find.text('성경'), findsOneWidget);
  });

  testWidgets('Bottom navigation has 5 tabs', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => BibleProvider()),
          ChangeNotifierProvider(create: (_) => ThemeProvider()),
        ],
        child: const KoreanBibleApp(),
      ),
    );
    await tester.pump();

    expect(find.text('성경'), findsOneWidget);
    expect(find.text('예배자료'), findsOneWidget);
    expect(find.text('찬송가'), findsOneWidget);
    expect(find.text('북마크'), findsOneWidget);
    expect(find.text('설정'), findsOneWidget);
  });

  testWidgets('Dark mode toggle exists in settings', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => BibleProvider()),
          ChangeNotifierProvider(create: (_) => ThemeProvider()),
        ],
        child: const KoreanBibleApp(),
      ),
    );
    await tester.pump();

    // Tap settings tab (index 4)
    await tester.tap(find.byIcon(Icons.settings));
    await tester.pump();

    expect(find.text('다크 모드'), findsOneWidget);
  });
}
