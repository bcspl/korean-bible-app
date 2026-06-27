# Korean Bible App - 우선순위별 Task 백로그 및 스케줄 (2026-06-19, Updated 2026-06-27)

> **참고**: 전체 로드맵은 `Project_Status_and_Updated_Roadmap_2026-06-19.md` 참조

## 현재 진행 상황 요약 (2026-06-27)
**전체 로드맵 대비 진행률**: Phase 0~2 완료 (약 40% 완료)
- ✅ 완료: Phase 0 (기반), Phase 1 (데이터 계층: 모델+어댑터+JSON 로더+시드), Phase 2 (기본 읽기 UI: 책목록/장선택/뷰어 + 검색 + 네비 + 홈)
- 🔄 진행중: UI/UX 폴리싱 (검색 강화, 디자인 개선 완료 직전)
- ⏳ 남은 주요: Phase 3 (사용자 기능: 북마크/하이라이트/설정), Phase 4 (고도화), Phase 5 (배포)
- **당장 다음 할 일 (우선순위 Top 3)**:
  1. Phase 3 Day1~2: 북마크 기능 (model + Hive + viewer 버튼 + 목록 화면)
  2. Phase 3 Day2~3: 하이라이트 + 메모 (verse selection + 저장)
  3. Phase 3 Day3~5: 본문 검색 결과 화면 polish + 설정 화면 (글꼴/다크모드)

**시각적 진행 표시**:
```
로드맵 전체: [████████░░░░░░░░░░░░] 40% (Phase 0-2 완료)
Phase 1:     [██████████] 100% ✅
Phase 2:     [██████████] 100% ✅
Phase 3:     [░░░░░░░░░░]   0% ⏳ (다음 집중)
Phase 4-5:   [░░░░░░░░░░]   0%
```

## Phase 1: 데이터 계층 (최우선, 4~5일) - ✅ 완료 (2026-06-27)
### Day 1: 모델 정의 (0.5~1일) ✅
- [x] lib/models/bible_verse.dart 생성 및 BibleVerse 클래스 정의 (verse: int, text: String, @HiveType(0), @HiveField)
- [x] lib/models/bible_chapter.dart 생성 및 BibleChapter 클래스 정의 (chapter: int, verses: List<BibleVerse>)
- [x] lib/models/bible_book.dart 생성 및 BibleBook 클래스 정의 (name: String, chapters: List<BibleChapter>)

### Day 2: 어댑터 및 코드 생성 (0.5~1일) ✅
- [x] 모델에 Hive 어댑터 어노테이션 추가
- [x] main.dart에 Hive.registerAdapter 호출 추가
- [x] flutter pub run build_runner build 실행으로 어댑터 .g.dart 생성

### Day 3: 파서 구현 (1일) ✅
- [x] lib/services/bible_data_service.dart 생성
- [x] rootBundle으로 kor_bible_full.json 로드
- [x] JSON을 BibleBook 리스트로 파싱하는 함수 구현 (샘플 + 풀 데이터)

### Day 3~4: 초기화 및 시드 (1일) ✅
- [x] main.dart async init에서 Hive.initFlutter + openBox('bible')
- [x] 데이터 로드 후 Hive에 시드 (이미 있으면 skip)
- [x] 로드 완료 후 UI에 데이터 바인딩 placeholder

### Day 4~5: 검증 및 프로파일 (0.5~1일) ✅
- [x] parser 단위 테스트 작성 (flutter test)
- [x] 앱 시작 시 로딩 시간 측정 및 콘솔 로그
- [x] 7MB JSON 로딩 최적화 (필요시 인덱스 고려)

## Phase 2: 핵심 읽기 UI (MVP, 5~7일) - ✅ 완료 (2026-06-27)
### Day 1~2: 책 목록 (1~2일) ✅
- [x] lib/screens/book_list_screen.dart 생성 (한글/영문 이름, 검색, OT/NT 필터, 본문 검색)
- [x] 구약/신약 분류 탭 또는 ListView 구현 (BibleBook 리스트 사용)
- [x] 검색바 추가 (책 이름 필터) + 본문 검색

### Day 2~3: 장 선택 (1일) ✅
- [x] Chapter selection screen (grid, compact)
- [x] 그리드 또는 List로 장 번호 표시
- [x] 선택 시 해당 장으로 이동

### Day 3~5: 본문 뷰어 (2~3일) ✅
- [x] Bible text viewer widget (RichText, line height, prev/next)
- [x] ListView.builder로 절 표시 (verse + text)
- [x] 큰 글씨 지원 (theme text scale) + 홈 버튼

### Day 5~6: 네비게이션 (1~2일) ✅
- [x] 이전/다음 장 버튼 (AppBar + top bar)
- [x] 책 변경 드롭다운 또는 네비
- [x] 현재 위치 Provider로 관리 (book, chapter, verse)

### Day 6~7: 네비 연결 (1일) ✅
- [x] BottomNavigationBar를 실제 Screen으로 연결
- [x] HomeScreen을 Bible reader로 대체 (BookList 직접 진입)
- [x] State management with Provider for current reading position

## Phase 3: 핵심 사용자 기능 (5~7일) - ⏳ 미완료 (다음 집중)
### Day 1~2: 북마크 (1~2일) ⏳
- [ ] Bookmark model + Hive box
- [ ] 북마크 추가/삭제 버튼 in viewer
- [ ] 북마크 목록 화면

### Day 2~3: 하이라이트/메모 (1~2일) ⏳
- [ ] Highlight + note per verse
- [ ] Text selection in viewer
- [ ] 저장 및 표시

### Day 3~5: 검색 (2일) ⏳ (기본은 있음)
- [ ] In-app text search across books/chapters (이미 기본 구현, polish 필요)
- [ ] 검색 결과 리스트 (verse match) + 하이라이트
- [ ] 결과 클릭 시 해당 위치 이동

### Day 5~6: 설정 (1일) ⏳
- [ ] Settings screen with font size slider
- [ ] Dark mode toggle (ThemeData switch)
- [ ] Shared preferences save

### Day 6~7: 결과 화면 및 통합 (1일) ⏳
- [ ] Search results UI polish
- [ ] Bottom nav to settings and bookmarks
- [ ] Integration testing
- [ ] Integration testing

## Phase 4: UI/UX 고도화 (4~6일) - ⏳ 미완료
### Day 1: 다크모드 (1일) ⏳
- [ ] Theme provider with light/dark
- [ ] Color scheme customization

### Day 1~2: 접근성 (1~2일) ⏳
- [ ] Font size scaling test
- [ ] Screen reader labels
- [ ] High contrast mode

### Day 2~3: 상태 처리 (1일) ⏳
- [ ] Loading indicator during data load
- [ ] Error handling and retry UI

### Day 3~5: 반응형 (2일) ⏳
- [ ] LayoutBuilder for mobile/desktop
- [ ] Responsive padding/sizes

### Day 5~6: 브랜딩 (1일) ⏳
- [ ] App icon design
- [ ] Splash screen
- [ ] Launcher name update

## Phase 5: 플랫폼 확장 및 배포 (5~7일) - ⏳ 미완료
### Day 1~2: Android (2일) ⏳
- [ ] flutter build apk/appbundle
- [ ] Device testing on Android emulator/phone
- [ ] Signing config

### Day 2~4: iOS (2일) ⏳
- [ ] flutter build ios
- [ ] Xcode setup and test on simulator
- [ ] Provisioning profiles

### Day 4~5: Web (1~2일) ⏳
- [ ] flutter build web
- [ ] PWA manifest
- [ ] Deploy to GitHub pages or Netlify test

### Day 5~6: 릴리스 설정 (1일) ⏳
- [ ] pubspec version bump
- [ ] Build release artifacts
- [ ] CHANGELOG update

### Day 6~7: 스토어 (1일) ⏳
- [ ] App store listing text
- [ ] Screenshots
- [ ] Description and keywords prepare

## 추후 (Phase 6+, 2~4주 단위로)
### 오디오 (1주)
- [ ] TTS integration for verse reading
- [ ] Audio play controls in viewer

### 다중 번역 (1주)
- [ ] Support additional translations (if data available)
- [ ] Version selector in settings

### 동기화 (1~2주)
- [ ] Optional Google Drive sync for bookmarks
- [ ] Cloud backup for user data

### 통계 (1주)
- [ ] Reading progress tracking
- [ ] Stats screen (chapters read, time)

## 진행 상황 추적 (시각적 명확화)
- **전체 대비**: Phase 0-2 완료 (~40%)
- **완료된 상태**: Phase 1 (데이터 계층 전체 ✅), Phase 2 (기본 UI 전체 ✅, 검색/홈/디자인 개선 포함)
- **남은 것**: Phase 3 (사용자 기능 ⏳), Phase 4 (고도화 ⏳), Phase 5 (배포 ⏳)
- **당장 다음 할일 (상세, <1주 단위)**: 
  1. Phase 3 Day1: Bookmark model + Hive box + viewer 버튼
  2. Phase 3 Day2: Highlight + note per verse
  3. Phase 3 Day3: 본문 검색 결과 polish + 하이라이트
- **시각적 트래킹** (매 스킬 실행시 갱신):
  로드맵: [████████░░░░░░░░░░░░░░░░] 40% 완료
  Phase별: Phase1 ██████████ 100% | Phase2 ██████████ 100% | Phase3 ░░░░░░░░░░ 0% | ...
- 주간 리뷰 시 이 파일 + PPTX 업데이트

**다음 실행 추천**: Phase 3부터 순차 (북마크 → 하이라이트 → 설정). 모든 주요 Phase 완료 후 스킬 재실행.