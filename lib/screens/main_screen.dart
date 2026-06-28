import 'package:flutter/material.dart';
import 'book_list_screen.dart';
import 'bookmark_list_screen.dart';
import 'hymn_list_screen.dart';
import 'settings_screen.dart';
import 'worship_materials_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    BookListScreen(),
    WorshipMaterialsScreen(),
    HymnListScreen(),
    BookmarkListScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (i) => setState(() => _currentIndex = i),
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.indigo,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.menu_book),
            label: '성경',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.account_balance),
            label: '예배자료',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.music_note),
            label: '찬송가',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bookmark),
            label: '북마크',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: '설정',
          ),
        ],
      ),
    );
  }
}
