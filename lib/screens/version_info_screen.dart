import 'package:flutter/material.dart';

import '../services/update_service.dart';

class VersionInfoScreen extends StatefulWidget {
  const VersionInfoScreen({super.key});

  @override
  State<VersionInfoScreen> createState() => _VersionInfoScreenState();
}

enum _CheckState { idle, checking, upToDate, updateAvailable, failed }

class _VersionInfoScreenState extends State<VersionInfoScreen> {
  InstalledVersionInfo? _installed;
  LatestVersionInfo? _latest;
  _CheckState _state = _CheckState.idle;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final installed = await UpdateService.getInstalled();
      if (!mounted) return;
      setState(() => _installed = installed);
    } catch (_) {}
    await _check();
  }

  Future<void> _check() async {
    setState(() => _state = _CheckState.checking);
    final latest = await UpdateService.fetchLatest();
    if (!mounted) return;
    setState(() {
      _latest = latest;
      if (latest == null) {
        _state = _CheckState.failed;
      } else if (_installed != null &&
          latest.versionCode > _installed!.versionCode) {
        _state = _CheckState.updateAvailable;
      } else {
        _state = _CheckState.upToDate;
      }
    });
  }

  Future<void> _openStore() async {
    final ok = await UpdateService.openOneStore();
    if (!ok && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('원스토어를 열 수 없습니다. 원스토어 앱에서 \'한국어 성경\'을 검색해 주세요.')),
      );
    }
  }

  String _fmt(DateTime? d) {
    if (d == null) return '알 수 없음';
    final l = d.toLocal();
    String two(int v) => v.toString().padLeft(2, '0');
    return '${l.year}-${two(l.month)}-${two(l.day)}';
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final horizontalPad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final installed = _installed;
    final latest = _latest;

    String statusText;
    IconData statusIcon;
    switch (_state) {
      case _CheckState.idle:
      case _CheckState.checking:
        statusText = '업데이트 확인 중…';
        statusIcon = Icons.sync;
        break;
      case _CheckState.upToDate:
        statusText = '최신 버전을 사용 중입니다';
        statusIcon = Icons.check_circle_outline;
        break;
      case _CheckState.updateAvailable:
        statusText = '새 버전이 있습니다';
        statusIcon = Icons.system_update;
        break;
      case _CheckState.failed:
        statusText = '업데이트 확인 실패(네트워크 연결 확인)';
        statusIcon = Icons.wifi_off;
        break;
    }

    return Scaffold(
      appBar: AppBar(title: const Text('버전 정보 및 업데이트')),
      body: ListView(
        padding: EdgeInsets.fromLTRB(horizontalPad, 0, horizontalPad,
            8 + MediaQuery.viewPaddingOf(context).bottom),
        children: [
          ListTile(
            leading: const Icon(Icons.info_outline),
            title: const Text('현재 버전'),
            subtitle: Text(installed == null
                ? '확인 중…'
                : '${installed.versionName} (빌드 ${installed.versionCode})'),
          ),
          ListTile(
            leading: const Icon(Icons.event_available),
            title: const Text('이 기기 업데이트 적용일'),
            subtitle: Text(installed == null
                ? '확인 중…'
                : _fmt(installed.appliedAt) +
                    (installed.appliedAtIsFirstLaunch ? ' (첫 실행 기준)' : '')),
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.new_releases_outlined),
            title: const Text('최신 버전'),
            subtitle: Text(latest == null
                ? (_state == _CheckState.failed ? '-' : '확인 중…')
                : '${latest.versionName} (빌드 ${latest.versionCode})'),
          ),
          ListTile(
            leading: const Icon(Icons.calendar_today),
            title: const Text('최신 버전 출시일'),
            subtitle: Text(latest?.releaseDate ?? '-'),
          ),
          if (latest?.notes != null && latest!.notes!.isNotEmpty)
            ListTile(
              leading: const Icon(Icons.notes),
              title: const Text('업데이트 내용'),
              subtitle: Text(latest.notes!),
            ),
          const Divider(),
          ListTile(
            leading: Icon(statusIcon),
            title: Text(statusText),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _state == _CheckState.checking ? null : _check,
                    icon: const Icon(Icons.refresh),
                    label: const Text('다시 확인'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: FilledButton.icon(
                    onPressed: _openStore,
                    icon: const Icon(Icons.store),
                    label: Text(_state == _CheckState.updateAvailable
                        ? '원스토어에서 업데이트'
                        : '원스토어 열기'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
