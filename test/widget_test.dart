// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:korean_bible_app/main.dart';

void main() {
  testWidgets('Korean Bible App smoke test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const KoreanBibleApp());

    // Verify that the app title or main text appears.
    expect(find.text('한국어 성경'), findsOneWidget);
    expect(find.byIcon(Icons.menu_book), findsOneWidget);

    // Basic navigation bar check
    expect(find.text('성경'), findsOneWidget);
  });
}
