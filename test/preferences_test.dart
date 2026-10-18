import 'package:flutter_test/flutter_test.dart';
import 'package:korean_bible_app/models/bible_version.dart';
import 'package:korean_bible_app/providers/bible_provider.dart';
import 'package:korean_bible_app/services/last_position_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('기본 역본', () {
    test('저장값 없음 → 개역한글만', () {
      expect(BibleProvider.resolveInitialVersions(null), [BibleVersionId.krv]);
      expect(BibleProvider.resolveInitialVersions([]), [BibleVersionId.krv]);
      expect(BibleProvider.resolveInitialVersions(['XYZ']),
          [BibleVersionId.krv]);
    });

    test('저장된 선택 유지 (순서·중복·최대 3)', () {
      expect(BibleProvider.resolveInitialVersions(['KRV', 'KJV']),
          [BibleVersionId.krv, BibleVersionId.kjv]);
      expect(BibleProvider.resolveInitialVersions(['ASV', 'KRV', 'ASV']),
          [BibleVersionId.asv, BibleVersionId.krv]);
      expect(BibleProvider.resolveInitialVersions(['KJV']),
          [BibleVersionId.kjv]);
    });

    test('새 provider 기본값은 KRV만, 변경 시 저장', () async {
      SharedPreferences.setMockInitialValues({});
      final p = BibleProvider();
      expect(p.activeVersions, [BibleVersionId.krv]);
      p.setVersionEnabled(BibleVersionId.kjv, true);
      await Future<void>.delayed(Duration.zero);
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getStringList(BibleProvider.activeVersionsPrefsKey),
          ['KRV', 'KJV']);
    });
  });

  group('마지막 위치', () {
    test('성경 위치 인코딩', () {
      final pos = BiblePosition.decode(const BiblePosition(42, 2, 815.4).encode())!;
      expect(pos.bookIndex, 42);
      expect(pos.chapterIndex, 2);
      expect(pos.scrollOffset, 815);
      expect(BiblePosition.decode('3:4')!.scrollOffset, 0);
      expect(BiblePosition.decode('x:1'), isNull);
      expect(BiblePosition.decode(null), isNull);
    });

    test('예배자료 위치 인코딩', () {
      expect(WorshipPosition.decode('reading:5')!.readingNumber, 5);
      expect(WorshipPosition.decode('creed')!.screen, 'creed');
      expect(WorshipPosition.decode('creed:3')!.readingNumber, isNull);
      expect(WorshipPosition.decode('bogus'), isNull);
    });

    test('저장 후 다시 불러오기', () async {
      SharedPreferences.setMockInitialValues({});
      LastPositionService.resetForTest();
      LastPositionService.saveHymn(305);
      LastPositionService.saveBible(const BiblePosition(0, 2, 120));
      await LastPositionService.flush();
      LastPositionService.resetForTest();
      await LastPositionService.load();
      expect(LastPositionService.section, AppSection.bible);
      expect(LastPositionService.bible!.chapterIndex, 2);
      expect(LastPositionService.hymnId, 305);
      expect(LastPositionService.hasPosition(AppSection.worship), isFalse);
    });

    test('처음 사용자는 섹션 없음', () async {
      SharedPreferences.setMockInitialValues({});
      LastPositionService.resetForTest();
      await LastPositionService.load();
      expect(LastPositionService.section, isNull);
    });
  });
}
