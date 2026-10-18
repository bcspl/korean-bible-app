/// 성경 검색: 책 이름/약어 매칭, 장절 참조 파싱 (순수 Dart · 단위 테스트 가능).
///
/// 약어 출처: 대한성서공회 성경 약어표 (개역 계열 약어).
library;

class BookInfo {
  final String key; // JSON 책 키 (Gen, Exod …)
  final String korean;
  final String english;
  final List<String> abbreviations; // 한글 약어 + 영문 약어

  const BookInfo(this.key, this.korean, this.english, this.abbreviations);
}

const List<BookInfo> kBibleBooks = [
  BookInfo('Gen', '창세기', 'Genesis', ['창', 'gen', 'ge', 'gn']),
  BookInfo('Exod', '출애굽기', 'Exodus', ['출', 'exod', 'exo', 'ex']),
  BookInfo('Lev', '레위기', 'Leviticus', ['레', 'lev', 'lv']),
  BookInfo('Num', '민수기', 'Numbers', ['민', 'num', 'nm']),
  BookInfo('Deut', '신명기', 'Deuteronomy', ['신', 'deut', 'deu', 'dt']),
  BookInfo('Josh', '여호수아', 'Joshua', ['수', 'josh', 'jos']),
  BookInfo('Judg', '사사기', 'Judges', ['삿', 'judg', 'jdg']),
  BookInfo('Ruth', '룻기', 'Ruth', ['룻', 'ruth', 'rth', 'ru']),
  BookInfo('1Sam', '사무엘상', '1 Samuel', ['삼상', '1sam', '1sa']),
  BookInfo('2Sam', '사무엘하', '2 Samuel', ['삼하', '2sam', '2sa']),
  BookInfo('1Kgs', '열왕기상', '1 Kings', ['왕상', '1kgs', '1ki', '1kings']),
  BookInfo('2Kgs', '열왕기하', '2 Kings', ['왕하', '2kgs', '2ki', '2kings']),
  BookInfo('1Chr', '역대상', '1 Chronicles', ['대상', '1chr', '1ch']),
  BookInfo('2Chr', '역대하', '2 Chronicles', ['대하', '2chr', '2ch']),
  BookInfo('Ezra', '에스라', 'Ezra', ['스', 'ezra', 'ezr']),
  BookInfo('Neh', '느헤미야', 'Nehemiah', ['느', 'neh']),
  BookInfo('Esth', '에스더', 'Esther', ['에', 'esth', 'est']),
  BookInfo('Job', '욥기', 'Job', ['욥', 'job']),
  BookInfo('Ps', '시편', 'Psalms', ['시', 'ps', 'psa', 'psalm']),
  BookInfo('Prov', '잠언', 'Proverbs', ['잠', 'prov', 'pr', 'prv']),
  BookInfo('Eccl', '전도서', 'Ecclesiastes', ['전', 'eccl', 'ecc']),
  BookInfo('Song', '아가', 'Song of Songs', ['아', '아가서', 'song', 'sos']),
  BookInfo('Isa', '이사야', 'Isaiah', ['사', 'isa', 'is']),
  BookInfo('Jer', '예레미야', 'Jeremiah', ['렘', 'jer']),
  BookInfo('Lam', '예레미야 애가', 'Lamentations', ['애', '애가', '예레미야애가', 'lam']),
  BookInfo('Ezek', '에스겔', 'Ezekiel', ['겔', 'ezek', 'eze']),
  BookInfo('Dan', '다니엘', 'Daniel', ['단', 'dan', 'dn']),
  BookInfo('Hos', '호세아', 'Hosea', ['호', 'hos']),
  BookInfo('Joel', '요엘', 'Joel', ['욜', 'joel']),
  BookInfo('Amos', '아모스', 'Amos', ['암', 'amos']),
  BookInfo('Obad', '오바댜', 'Obadiah', ['옵', 'obad', 'oba']),
  BookInfo('Jonah', '요나', 'Jonah', ['욘', 'jonah', 'jon']),
  BookInfo('Mic', '미가', 'Micah', ['미', 'mic']),
  BookInfo('Nah', '나훔', 'Nahum', ['나', 'nah']),
  BookInfo('Hab', '하박국', 'Habakkuk', ['합', 'hab']),
  BookInfo('Zeph', '스바냐', 'Zephaniah', ['습', 'zeph', 'zep']),
  BookInfo('Hag', '학개', 'Haggai', ['학', 'hag']),
  BookInfo('Zech', '스가랴', 'Zechariah', ['슥', 'zech', 'zec']),
  BookInfo('Mal', '말라기', 'Malachi', ['말', 'mal']),
  BookInfo('Matt', '마태복음', 'Matthew', ['마', '마태', 'matt', 'mat', 'mt']),
  BookInfo('Mark', '마가복음', 'Mark', ['막', '마가', 'mark', 'mk']),
  BookInfo('Luke', '누가복음', 'Luke', ['눅', '누가', 'luke', 'lk']),
  BookInfo('John', '요한복음', 'John', ['요', 'john', 'jn']),
  BookInfo('Acts', '사도행전', 'Acts', ['행', 'acts', 'act']),
  BookInfo('Rom', '로마서', 'Romans', ['롬', 'rom']),
  BookInfo('1Cor', '고린도전서', '1 Corinthians', ['고전', '1cor', '1co']),
  BookInfo('2Cor', '고린도후서', '2 Corinthians', ['고후', '2cor', '2co']),
  BookInfo('Gal', '갈라디아서', 'Galatians', ['갈', 'gal']),
  BookInfo('Eph', '에베소서', 'Ephesians', ['엡', 'eph']),
  BookInfo('Phil', '빌립보서', 'Philippians', ['빌', 'phil', 'php']),
  BookInfo('Col', '골로새서', 'Colossians', ['골', 'col']),
  BookInfo('1Thess', '데살로니가전서', '1 Thessalonians', ['살전', '1thess', '1th']),
  BookInfo('2Thess', '데살로니가후서', '2 Thessalonians', ['살후', '2thess', '2th']),
  BookInfo('1Tim', '디모데전서', '1 Timothy', ['딤전', '1tim', '1ti']),
  BookInfo('2Tim', '디모데후서', '2 Timothy', ['딤후', '2tim', '2ti']),
  BookInfo('Titus', '디도서', 'Titus', ['딛', 'titus', 'tit']),
  BookInfo('Phlm', '빌레몬서', 'Philemon', ['몬', 'phlm', 'phm']),
  BookInfo('Heb', '히브리서', 'Hebrews', ['히', 'heb']),
  BookInfo('Jas', '야고보서', 'James', ['약', 'jas', 'james']),
  BookInfo('1Pet', '베드로전서', '1 Peter', ['벧전', '1pet', '1pe']),
  BookInfo('2Pet', '베드로후서', '2 Peter', ['벧후', '2pet', '2pe']),
  BookInfo('1John', '요한1서', '1 John', ['요일', '요1', '요1서', '요한일서', '1john', '1jn']),
  BookInfo('2John', '요한2서', '2 John', ['요이', '요2', '요2서', '요한이서', '2john', '2jn']),
  BookInfo('3John', '요한3서', '3 John', ['요삼', '요3', '요3서', '요한삼서', '3john', '3jn']),
  BookInfo('Jude', '유다서', 'Jude', ['유', 'jude']),
  BookInfo('Rev', '요한계시록', 'Revelation', ['계', '계시록', 'rev', 're']),
];

final Map<String, int> _canonicalIndex = {
  for (var i = 0; i < kBibleBooks.length; i++) kBibleBooks[i].key: i,
};

/// 공백 제거 + 소문자.
String normalizeQuery(String s) =>
    s.toLowerCase().replaceAll(RegExp(r'\s+'), '');

class BookMatch {
  final BookInfo book;
  final int score; // 낮을수록 우선
  const BookMatch(this.book, this.score);
}

/// 책 이름/약어로 책 찾기. 정렬: 약어·이름 정확 일치 → 이름 접두 → 약어 접두 → 이름 포함, 동점은 성경 순서.
List<BookMatch> matchBooks(String query) {
  final q = normalizeQuery(query);
  if (q.isEmpty) return const [];
  final out = <BookMatch>[];
  for (final b in kBibleBooks) {
    final ko = normalizeQuery(b.korean);
    final en = normalizeQuery(b.english);
    final abbrs = b.abbreviations.map(normalizeQuery).toList();
    int? score;
    if (ko == q || en == q || abbrs.contains(q)) {
      score = 0;
    } else if (ko.startsWith(q) || en.startsWith(q)) {
      score = 1;
    } else if (abbrs.any((a) => a.length > q.length && a.startsWith(q))) {
      score = 2;
    } else if (q.length >= 2 && (ko.contains(q) || en.contains(q))) {
      score = 3;
    }
    if (score != null) out.add(BookMatch(b, score));
  }
  out.sort((a, b) {
    final s = a.score.compareTo(b.score);
    if (s != 0) return s;
    return _canonicalIndex[a.book.key]!.compareTo(_canonicalIndex[b.book.key]!);
  });
  return out;
}

/// 정확히 하나의 책으로 해석 (참조 파싱용). 정확 일치 우선, 없으면 접두 일치 최상위.
BookInfo? resolveBook(String text) {
  final m = matchBooks(text);
  if (m.isEmpty) return null;
  if (m.first.score > 1) return null; // 포함 일치만으로는 참조로 보지 않음
  return m.first.book;
}

class BibleReference {
  final BookInfo book;
  final int chapter;
  final int? verse;
  const BibleReference(this.book, this.chapter, [this.verse]);

  String get label =>
      verse == null ? '${book.korean} $chapter장' : '${book.korean} $chapter:$verse';

  @override
  String toString() => '${book.key} $chapter${verse == null ? '' : ':$verse'}';
}

final RegExp _refPattern = RegExp(
    r'^(.+?)\s*(\d{1,3})(?:\s*[:：.,]\s*(\d{1,3})|\s+(\d{1,3}))?(?:\s*[-~]\s*\d{1,3})?\s*$');

/// '요 3:16', '요한복음 3장', '요한복음 3장 16절', '창1', '시 23', '1 John 4:8' 등을 파싱.
BibleReference? parseReference(String input) {
  var s = input.trim();
  if (s.isEmpty) return null;
  // '3장 16절' → '3 16', '23편' → '23'
  s = s.replaceAllMapped(RegExp(r'(\d)\s*(장|편)'), (m) => '${m[1]} ');
  s = s.replaceAll('절', '').trim();
  final m = _refPattern.firstMatch(s);
  if (m == null) return null;
  final bookPart = m.group(1)!.trim();
  if (bookPart.isEmpty || RegExp(r'^\d+$').hasMatch(bookPart)) return null;
  final book = resolveBook(bookPart);
  if (book == null) return null;
  final chapter = int.parse(m.group(2)!);
  final vs = m.group(3) ?? m.group(4);
  final verse = vs == null ? null : int.parse(vs);
  if (chapter < 1 || (verse != null && verse < 1)) return null;
  return BibleReference(book, chapter, verse);
}
