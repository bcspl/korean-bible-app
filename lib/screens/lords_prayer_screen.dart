import 'package:flutter/material.dart';
import '../data/worship_texts.dart';
import '../models/bible_version.dart';

/// 주기도문 — 역본별 **기도 본문만** 표시 (마 6 서사·설명 문구 제외).
class LordsPrayerScreen extends StatefulWidget {
  const LordsPrayerScreen({super.key});

  @override
  State<LordsPrayerScreen> createState() => _LordsPrayerScreenState();
}

class _LordsPrayerScreenState extends State<LordsPrayerScreen> {
  BibleVersionId _lang = BibleVersionId.krv;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final text = WorshipTexts.lordsPrayer(_lang);
    final caption = WorshipTexts.lordsPrayerCaption(_lang);

    return Scaffold(
      appBar: AppBar(
        title: const Text('주기도문'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(52),
          child: Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Semantics(
              label: '주기도문 역본 선택',
              child: Wrap(
                spacing: 6,
                children: [
                  for (final v in BibleVersionId.values)
                    ChoiceChip(
                      label: Text(v.shortLabel),
                      selected: _lang == v,
                      onSelected: (_) => setState(() => _lang = v),
                    ),
                ],
              ),
            ),
          ),
        ),
      ),
      body: Padding(
        padding: EdgeInsets.all(pad),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                caption,
                style: TextStyle(fontSize: 12, color: Colors.grey.shade700),
              ),
              const SizedBox(height: 6),
              Text(
                '기도문만 표시 · 성경 서술(“이렇게 기도하라” 등)은 제외',
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.indigo.shade700,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 16),
              Semantics(
                label: '주기도문 ${_lang.shortLabel} 기도 본문',
                child: SelectableText(
                  text.trim(),
                  style: const TextStyle(fontSize: 18, height: 1.9),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
