import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

/// 원스토어 상품 ID (PID) — 한국어 성경 (com.lsh.koreanbible).
/// 앱 링크: onestore://common/product/{PID} (원스토어 연동규격 가이드)
/// 웹: https://m.onestore.co.kr/ko-kr/apps/appsDetail.omp?prodId={PID}
const String kOneStoreProductId = '0001009901';

/// 최신 버전 정보 JSON (GitHub main 브랜치).
const String kVersionJsonUrl =
    'https://raw.githubusercontent.com/bcspl/korean-bible-app/main/app_version.json';

const String _kAppSearchName = '한국어 성경';

class LatestVersionInfo {
  final String versionName;
  final int versionCode;
  final String? releaseDate;
  final String? notes;

  const LatestVersionInfo({
    required this.versionName,
    required this.versionCode,
    this.releaseDate,
    this.notes,
  });

  static LatestVersionInfo? tryParse(Map<String, dynamic> json) {
    final name = json['versionName'];
    final code = json['versionCode'];
    final parsedCode = code is int ? code : int.tryParse('$code');
    if (name is! String || parsedCode == null) return null;
    return LatestVersionInfo(
      versionName: name,
      versionCode: parsedCode,
      releaseDate: json['releaseDate'] as String?,
      notes: json['notes'] as String?,
    );
  }
}

class InstalledVersionInfo {
  final String versionName;
  final int versionCode;
  /// 이 기기에 현재 버전이 적용(설치/업데이트)된 날짜.
  final DateTime? appliedAt;
  /// appliedAt 이 실제 시스템 업데이트 시각이 아닌 '첫 실행 기록'인지 여부.
  final bool appliedAtIsFirstLaunch;

  const InstalledVersionInfo({
    required this.versionName,
    required this.versionCode,
    this.appliedAt,
    this.appliedAtIsFirstLaunch = false,
  });
}

class UpdateService {
  static const _prefsPrefix = 'version_first_launch_';

  /// 현재 버전의 첫 실행 날짜를 기록합니다 (앱 시작 시 호출, 실패해도 무시).
  static Future<void> recordFirstLaunchOfCurrentVersion() async {
    try {
      final info = await PackageInfo.fromPlatform();
      final prefs = await SharedPreferences.getInstance();
      final key = '$_prefsPrefix${info.buildNumber}';
      if (!prefs.containsKey(key)) {
        await prefs.setString(key, DateTime.now().toIso8601String());
      }
    } catch (_) {}
  }

  static Future<InstalledVersionInfo> getInstalled() async {
    final info = await PackageInfo.fromPlatform();
    DateTime? applied = info.updateTime ?? info.installTime;
    var isFirstLaunch = false;
    if (applied == null) {
      try {
        final prefs = await SharedPreferences.getInstance();
        final s = prefs.getString('$_prefsPrefix${info.buildNumber}');
        if (s != null) {
          applied = DateTime.tryParse(s);
          isFirstLaunch = applied != null;
        }
      } catch (_) {}
    }
    return InstalledVersionInfo(
      versionName: info.version,
      versionCode: int.tryParse(info.buildNumber) ?? 0,
      appliedAt: applied,
      appliedAtIsFirstLaunch: isFirstLaunch,
    );
  }

  /// 최신 버전 정보 조회. 네트워크 오류/형식 오류 시 null.
  static Future<LatestVersionInfo?> fetchLatest({
    Duration timeout = const Duration(seconds: 8),
  }) async {
    final client = HttpClient()..connectionTimeout = timeout;
    try {
      final uri = Uri.parse(
          '$kVersionJsonUrl?t=${DateTime.now().millisecondsSinceEpoch}');
      final req = await client.getUrl(uri).timeout(timeout);
      final res = await req.close().timeout(timeout);
      if (res.statusCode != 200) return null;
      final body = await res.transform(utf8.decoder).join().timeout(timeout);
      final decoded = jsonDecode(body);
      if (decoded is! Map<String, dynamic>) return null;
      return LatestVersionInfo.tryParse(decoded);
    } catch (_) {
      return null;
    } finally {
      client.close(force: true);
    }
  }

  /// 원스토어 앱 페이지 열기. 앱 → 웹 → 검색 순으로 시도.
  static Future<bool> openOneStore() async {
    final candidates = <Uri>[
      if (kOneStoreProductId.isNotEmpty) ...[
        Uri.parse('onestore://common/product/$kOneStoreProductId'),
        Uri.parse(
            'https://m.onestore.co.kr/ko-kr/apps/appsDetail.omp?prodId=$kOneStoreProductId'),
      ],
      Uri.parse(
          'https://m.onestore.co.kr/ko-kr/search?keyword=${Uri.encodeComponent(_kAppSearchName)}'),
    ];
    for (final uri in candidates) {
      try {
        if (await launchUrl(uri, mode: LaunchMode.externalApplication)) {
          return true;
        }
      } catch (_) {}
    }
    return false;
  }
}
