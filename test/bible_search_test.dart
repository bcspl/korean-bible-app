import 'package:flutter_test/flutter_test.dart';
import 'package:korean_bible_app/services/bible_search.dart';

List<String> keys(String q) => matchBooks(q).map((m) => m.book.key).toList();

void main() {
  group('matchBooks (성경책 순위)', () {
    test('66권 모두 정의', () {
      expect(kBibleBooks.length, 66);
      expect(kBibleBooks.map((b) => b.key).toSet().length, 66);
    });

    test('약어 정확 일치가 최상위', () {
      expect(keys('창').first, 'Gen');
      expect(keys('마').first, 'Matt');
      expect(keys('요').first, 'John');
      expect(keys('시').first, 'Ps');
      expect(keys('계').first, 'Rev');
      expect(keys('롬').first, 'Rom');
      expect(keys('고전').first, '1Cor');
      expect(keys('요일').first, '1John');
    });

    test('이름 접두 일치', () {
      expect(keys('창세'), ['Gen']);
      expect(keys('요한').first, 'John');
      expect(keys('요한'),
          containsAllInOrder(['John', '1John', '2John', '3John', 'Rev']));
      expect(keys('마').take(2), ['Matt', 'Mark']);
    });

    test('영문 이름/약어', () {
      expect(keys('gen').first, 'Gen');
      expect(keys('John').first, 'John');
      expect(keys('1 John').first, '1John');
    });

    test('일치 없음', () {
      expect(keys('사랑'), isEmpty);
      expect(keys(''), isEmpty);
    });
  });

  group('parseReference (구절 바로가기)', () {
    String? p(String s) => parseReference(s)?.toString();

    test('장:절', () {
      expect(p('요 3:16'), 'John 3:16');
      expect(p('요3:16'), 'John 3:16');
      expect(p('요한복음 3:16'), 'John 3:16');
      expect(p('1 John 4:8'), '1John 4:8');
      expect(p('창 1:1-5'), 'Gen 1:1');
    });

    test('장/편/절 표기', () {
      expect(p('요한복음 3장'), 'John 3');
      expect(p('요한복음 3장 16절'), 'John 3:16');
      expect(p('시편 23편'), 'Ps 23');
      expect(p('창세기 1장1절'), 'Gen 1:1');
    });

    test('붙여쓰기·공백', () {
      expect(p('창1'), 'Gen 1');
      expect(p('시 23'), 'Ps 23');
      expect(p('요1서 3'), '1John 3');
      expect(p('요일 4:8'), '1John 4:8');
      expect(p('창 1 3'), 'Gen 1:3');
    });

    test('참조가 아닌 입력', () {
      expect(p('사랑'), isNull);
      expect(p('창'), isNull);
      expect(p('123'), isNull);
      expect(p('하나님 3'), isNull);
      expect(p('요 0'), isNull);
    });

    test('라벨', () {
      expect(parseReference('요 3:16')!.label, '요한복음 3:16');
      expect(parseReference('시 23')!.label, '시편 23장');
    });
  });
}
