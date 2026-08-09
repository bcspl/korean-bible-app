import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/bible_version.dart';
import '../providers/bible_provider.dart';

/// Filter chips to enable up to 3 PD Bible versions (KRV / KJV / ASV).
class BibleVersionSelector extends StatelessWidget {
  final bool dense;
  final ValueChanged<List<BibleVersionId>>? onChanged;

  /// When [standalone] is true, manages local selection (for worship screens
  /// that don't use BibleProvider active set). Provide [selected] + [onChanged].
  final bool standalone;
  final List<BibleVersionId>? selected;

  const BibleVersionSelector({
    super.key,
    this.dense = false,
    this.onChanged,
    this.standalone = false,
    this.selected,
  });

  @override
  Widget build(BuildContext context) {
    if (standalone) {
      final sel = selected ?? const [BibleVersionId.krv];
      return _buildBar(
        context,
        sel,
        (id, enable) {
          final next = List<BibleVersionId>.from(sel);
          if (enable) {
            if (!next.contains(id) && next.length < 3) next.add(id);
          } else {
            if (next.length > 1) next.remove(id);
          }
          onChanged?.call(next);
        },
      );
    }

    return Consumer<BibleProvider>(
      builder: (context, provider, _) {
        return _buildBar(
          context,
          provider.activeVersions,
          (id, enable) {
            provider.setVersionEnabled(id, enable);
            onChanged?.call(provider.activeVersions);
          },
        );
      },
    );
  }

  Widget _buildBar(
    BuildContext context,
    List<BibleVersionId> active,
    void Function(BibleVersionId id, bool enable) toggle,
  ) {
    return Material(
      color: Colors.blueGrey.withValues(alpha: 0.08),
      child: Padding(
        padding: EdgeInsets.symmetric(
          horizontal: dense ? 8 : 12,
          vertical: dense ? 6 : 10,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!dense)
              Padding(
                padding: const EdgeInsets.only(bottom: 6),
                child: Text(
                  '성경 역본 (최대 3개 · 모두 Public Domain)',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade700,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            Wrap(
              spacing: 6,
              runSpacing: 4,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                for (final v in BibleVersionId.values)
                  FilterChip(
                    label: Text(v.shortLabel),
                    selected: active.contains(v),
                    onSelected: (sel) {
                      if (sel && active.length >= 3 && !active.contains(v)) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('동시에 최대 3개 역본까지 선택할 수 있습니다.'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                        return;
                      }
                      if (!sel && active.length <= 1) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('최소 1개 역본은 선택되어 있어야 합니다.'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                        return;
                      }
                      toggle(v, sel);
                    },
                    visualDensity: dense
                        ? VisualDensity.compact
                        : VisualDensity.standard,
                    materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                  ),
                Text(
                  active.map((e) => e.code).join(' + '),
                  style: TextStyle(fontSize: 11, color: Colors.grey.shade600),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
