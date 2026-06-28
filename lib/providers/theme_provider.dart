import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeProvider with ChangeNotifier {
  static const String _themeKey = 'isDarkMode';
  static const String _textScaleKey = 'textScaleFactor';
  static const String _highContrastKey = 'highContrast';

  bool _isDarkMode = false;
  double _textScaleFactor = 1.0;
  bool _highContrast = false;

  bool get isDarkMode => _isDarkMode;
  double get textScaleFactor => _textScaleFactor;
  bool get highContrast => _highContrast;

  ThemeMode get themeMode => _isDarkMode ? ThemeMode.dark : ThemeMode.light;

  ThemeProvider() {
    _loadPreferences();
  }

  Future<void> _loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();
    _isDarkMode = prefs.getBool(_themeKey) ?? false;
    _textScaleFactor = prefs.getDouble(_textScaleKey) ?? 1.0;
    _highContrast = prefs.getBool(_highContrastKey) ?? false;
    notifyListeners();
  }

  Future<void> toggleTheme(bool value) async {
    _isDarkMode = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_themeKey, _isDarkMode);
    notifyListeners();
  }

  Future<void> setTextScaleFactor(double scale) async {
    _textScaleFactor = scale.clamp(0.8, 2.0);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_textScaleKey, _textScaleFactor);
    notifyListeners();
  }

  // Optional: reset to system default
  Future<void> resetToSystem() async {
    _textScaleFactor = 1.0;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble(_textScaleKey, _textScaleFactor);
    notifyListeners();
  }

  Future<void> toggleHighContrast(bool value) async {
    _highContrast = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_highContrastKey, _highContrast);
    notifyListeners();
  }
}
