import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../models/bible_version.dart';
import '../providers/bible_provider.dart';
import '../widgets/bible_version_selector.dart';

/// 교독문 — KRV/KJV/ASV scripture passages as leader/congregation readings.
class ResponsiveReadingScreen extends StatefulWidget {
  const ResponsiveReadingScreen({super.key});

  @override
  State<ResponsiveReadingScreen> createState() =>
      _ResponsiveReadingScreenState();
}

class _ResponsiveReadingScreenState extends State<ResponsiveReadingScreen> {
  List<Map<String, dynamic>> _readings = [];
  String _sourceNote = '';
  List<String> _categories = [];
  String _filterCategory = '전체';
  bool _loading = true;
  String? _error;
  BibleVersionId _displayVersion = BibleVersionId.krv;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final raw =
          await rootBundle.loadString('assets/data/responsive_readings.json');
      final map = jsonDecode(raw) as Map<String, dynamic>;
      final list = (map['readings'] as List<dynamic>)
          .map((e) => Map<String, dynamic>.from(e as Map))
          .toList();
      final cats = (map['categories'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [];
      if (!mounted) return;
      setState(() {
        _readings = list;
        _sourceNote = map['source_note'] as String? ?? '';
        _categories = ['전체', ...cats];
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = e.toString();
        _loading = false;
      });
    }
  }

  void _showScopeInfo() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('교독문 수록 범위'),
        content: SingleChildScrollView(
          child: Text(
            _sourceNote.isNotEmpty
                ? _sourceNote
                : '개역한글(KRV)·KJV·ASV 성경 구절로 구성한 앱 자체 교독문입니다.',
            style: const TextStyle(height: 1.5),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('확인'),
          ),
        ],
      ),
    );
  }

  List<Map<String, dynamic>> get _filtered {
    if (_filterCategory == '전체') return _readings;
    return _readings
        .where((r) => (r['category'] as String?) == _filterCategory)
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 8.0);
    final filtered = _filtered;

    return Scaffold(
      appBar: AppBar(
        title: const Text('교독문'),
        actions: [
          IconButton(
            icon: const Icon(Icons.info_outline),
            tooltip: '수록 범위 · 라이선스',
            onPressed: _showScopeInfo,
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(child: Text('교독문을 불러오지 못했습니다.\n$_error'))
              : Column(
                  children: [
                    Material(
                      color: Colors.green.shade50,
                      child: InkWell(
                        onTap: _showScopeInfo,
                        child: Padding(
                          padding: EdgeInsets.symmetric(
                              horizontal: pad + 8, vertical: 10),
                          child: Row(
                            children: [
                              Icon(Icons.verified_user,
                                  size: 18, color: Colors.green.shade800),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Text(
                                  'PD 성경 구절 교독 · 찬송가/개역개정 교독문 미사용 · ${_readings.length}편',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.green.shade900,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.fromLTRB(8, 8, 8, 0),
                      child: Wrap(
                        spacing: 6,
                        children: [
                          for (final v in BibleVersionId.values)
                            ChoiceChip(
                              label: Text(v.shortLabel),
                              selected: _displayVersion == v,
                              onSelected: (_) =>
                                  setState(() => _displayVersion = v),
                              visualDensity: VisualDensity.compact,
                            ),
                        ],
                      ),
                    ),
                    if (_categories.isNotEmpty)
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 8),
                        child: Row(
                          children: [
                            for (final c in _categories)
                              Padding(
                                padding: const EdgeInsets.only(right: 6),
                                child: FilterChip(
                                  label: Text(c),
                                  selected: _filterCategory == c,
                                  onSelected: (_) =>
                                      setState(() => _filterCategory = c),
                                  visualDensity: VisualDensity.compact,
                                ),
                              ),
                          ],
                        ),
                      ),
                    Expanded(
                      child: ListView.builder(
                        padding:
                            EdgeInsets.symmetric(horizontal: pad, vertical: 4),
                        itemCount: filtered.length,
                        itemBuilder: (context, i) {
                          final r = filtered[i];
                          final title = (r['title_ko'] as String?) ??
                              (r['title'] as String?) ??
                              '';
                          final titleEn = r['title_en'] as String? ?? '';
                          final cat = r['category'] as String? ?? '';
                          return Card(
                            margin: const EdgeInsets.symmetric(vertical: 4),
                            child: ListTile(
                              leading: CircleAvatar(
                                backgroundColor: Colors.indigo.shade50,
                                child: Text(
                                  '${r['number'] ?? i + 1}',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.indigo.shade800,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                              title: Text(title),
                              subtitle: Text(
                                [
                                  if (cat.isNotEmpty) cat,
                                  if (titleEn.isNotEmpty) titleEn,
                                  _displayVersion.code,
                                ].join(' · '),
                              ),
                              trailing: const Icon(Icons.chevron_right),
                              onTap: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => _ReadingDetail(
                                      reading: r,
                                      initialVersion: _displayVersion,
                                    ),
                                  ),
                                );
                              },
                            ),
                          );
                        },
                      ),
                    ),
                  ],
                ),
    );
  }
}

class _ReadingDetail extends StatefulWidget {
  final Map<String, dynamic> reading;
  final BibleVersionId initialVersion;

  const _ReadingDetail({
    required this.reading,
    required this.initialVersion,
  });

  @override
  State<_ReadingDetail> createState() => _ReadingDetailState();
}

class _ReadingDetailState extends State<_ReadingDetail> {
  late List<BibleVersionId> _versions;

  @override
  void initState() {
    super.initState();
    _versions = [widget.initialVersion];
  }

  List<Map<String, String>> _buildLines(BibleProvider provider) {
    final passages =
        (widget.reading['passages'] as List<dynamic>? ?? const []);
    final lines = <Map<String, String>>[];
    var roleToggle = true; // true = 인도자 first

    for (final p in passages) {
      final map = Map<String, dynamic>.from(p as Map);
      final book = map['book'] as String? ?? '';
      final chapter = map['chapter'] as int? ?? 1;
      List<int> verseNums;
      if (map['verses'] is List) {
        verseNums =
            (map['verses'] as List).map((e) => int.parse(e.toString())).toList();
      } else {
        verseNums = provider.verseNumbersForChapter(
          book,
          chapter,
          versions: _versions,
        );
        if (verseNums.isEmpty) {
          verseNums = [
            for (var v = 1; v <= 200; v++)
              if (provider.verseTextFor(_versions.first, book, chapter, v) !=
                  null)
                v
          ];
        }
      }

      for (final vNum in verseNums) {
        final parts = <String>[];
        for (final ver in _versions) {
          final t = provider.verseTextFor(ver, book, chapter, vNum);
          if (t != null && t.isNotEmpty) {
            if (_versions.length > 1) {
              parts.add('[${ver.code}] $t');
            } else {
              parts.add(t);
            }
          }
        }
        if (parts.isEmpty) continue;
        final role = roleToggle ? '인도자' : '회중';
        roleToggle = !roleToggle;
        lines.add({
          'role': role,
          'text': parts.join('\n'),
          'ref': '$book $chapter:$vNum',
        });
      }
    }
    return lines;
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<BibleProvider>(context);
    final title = (widget.reading['title_ko'] as String?) ??
        (widget.reading['title'] as String?) ??
        '교독문';
    final titleEn = widget.reading['title_en'] as String? ?? '';
    final lines = _buildLines(provider);
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);

    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: Column(
        children: [
          BibleVersionSelector(
            standalone: true,
            dense: true,
            selected: _versions,
            onChanged: (v) => setState(() => _versions = v),
          ),
          if (titleEn.isNotEmpty)
            Padding(
              padding: EdgeInsets.fromLTRB(pad, 8, pad, 0),
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(titleEn,
                    style: const TextStyle(color: Colors.grey, fontSize: 13)),
              ),
            ),
          Padding(
            padding: EdgeInsets.fromLTRB(pad, 4, pad, 0),
            child: Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'PD · ${_versions.map((e) => e.code).join(" + ")} · 찬송가 교독문 아님',
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.green.shade800,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ),
          Expanded(
            child: lines.isEmpty
                ? const Center(child: Text('해당 역본 본문을 찾을 수 없습니다.'))
                : ListView.builder(
                    padding: EdgeInsets.all(pad),
                    itemCount: lines.length,
                    itemBuilder: (c, i) {
                      final line = lines[i];
                      final isLeader = line['role'] == '인도자';
                      return Container(
                        margin: const EdgeInsets.symmetric(vertical: 4),
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: isLeader
                              ? Colors.indigo.withValues(alpha: 0.08)
                              : Colors.grey.withValues(alpha: 0.08),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${line['role']} · ${line['ref']}',
                              style: TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                color: isLeader
                                    ? Colors.indigo.shade800
                                    : Colors.grey.shade700,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              line['text']!,
                              style: const TextStyle(fontSize: 16.5, height: 1.5),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
