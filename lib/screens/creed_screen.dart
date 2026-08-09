import 'package:flutter/material.dart';
import '../data/worship_texts.dart';
import '../models/bible_version.dart';

/// 사도신경 — 역본(언어·문체)별 전통 문안.
class CreedScreen extends StatefulWidget {
  const CreedScreen({super.key});

  @override
  State<CreedScreen> createState() => _CreedScreenState();
}

class _CreedScreenState extends State<CreedScreen> {
  BibleVersionId _lang = BibleVersionId.krv;

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    final pad = width > 900 ? 32.0 : (width > 600 ? 24.0 : 16.0);
    final text = WorshipTexts.creed(_lang);
    final caption = WorshipTexts.creedCaption(_lang);

    return Scaffold(
      appBar: AppBar(
        title: const Text('사도신경'),
        bottom: PreferredSize(
          preferredSize: const Size.fromHeight(52),
          child: Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Semantics(
              label: '사도신경 역본 선택',
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
              const SizedBox(height: 16),
              Semantics(
                label: '사도신경 ${_lang.shortLabel} 본문',
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
