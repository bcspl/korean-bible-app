# Korean Bible App - 우선순위별 Task 백로그 및 스케줄 (2026-06-19, Updated 2026-06-20)

> **참고**: 전체 로드맵은 `Project_Status_and_Updated_Roadmap_2026-06-19.md` 참조

## Phase 1: 데이터 계층 (최우선, 4~5일)
### Day 1: 모델 정의 (0.5~1일)
- [ ] lib/models/bible_verse.dart 생성 및 BibleVerse 클래스 정의 (verse: int, text: String, @HiveType(0), @HiveField)
- [ ] lib/models/bible_chapter.dart 생성 및 BibleChapter 클래스 정의 (chapter: int, verses: List<BibleVerse>)
- [ ] lib/models/bible_book.dart 생성 및 BibleBook 클래스 정의 (name: String, chapters: List<BibleChapter>)

### Day 2: 어댑터 및 코드 생성 (0.5~1일)
- [ ] 모델에 Hive 어댑터 어노테이션 추가
- [ ] main.dart에 Hive.registerAdapter 호출 추가
- [ ] flutter pub run build_runner build 실행으로 어댑터 .g.dart 생성

### Day 3: 파서 구현 (1일)
- [ ] lib/services/bible_data_service.dart 생성
- [ ] rootBundle으로 kor_bible_full.json 로드
- [ ] JSON을 BibleBook 리스트로 파싱하는 함수 구현 (샘플 + 풀 데이터)

### Day 3~4: 초기화 및 시드 (1일)
- [ ] main.dart async init에서 Hive.initFlutter + openBox('bible')
- [ ] 데이터 로드 후 Hive에 시드 (이미 있으면 skip)
- [ ] 로드 완료 후 UI에 데이터 바인딩 placeholder

### Day 4~5: 검증 및 프로파일 (0.5~1일)
- [ ] parser 단위 테스트 작성 (flutter test)
- [ ] 앱 시작 시 로딩 시간 측정 및 콘솔 로그
- [ ] 7MB JSON 로딩 최적화 (필요시 인덱스 고려)

## Phase 2: 핵심 읽기 UI (MVP, 5~7일)
### Day 1~2: 책 목록 (1~2일)
- [ ] lib/screens/book_list_screen.dart 생성
- [ ] 구약/신약 분류 탭 또는 ListView 구현 (BibleBook 리스트 사용)
- [ ] 검색바 추가 (책 이름 필터)

### Day 2~3: 장 선택 (1일)
- [ ] Chapter selection screen
- [ ] 그리드 또는 List로 장 번호 표시
- [ ] 선택 시 해당 장으로 이동

### Day 3~5: 본문 뷰어 (2~3일)
- [ ] Bible text viewer widget
- [ ] ListView.builder로 절 표시 (verse + text)
- [ ] 큰 글씨 지원 (theme text scale)
- [ ] 스크롤 위치 저장

### Day 5~6: 네비게이션 (1~2일)
- [ ] 이전/다음 장 버튼
- [ ] 책 변경 드롭다운 또는 네비
- [ ] 현재 위치 Provider로 관리 (book, chapter, verse)

### Day 6~7: 네비 연결 (1일)
- [ ] BottomNavigationBar를 실제 Screen으로 연결
- [ ] HomeScreen을 Bible reader로 대체
- [ ] State management with Provider for current reading position

## Phase 3: 핵심 사용자 기능 (5~7일)
### Day 1~2: 북마크 (1~2일)
- [ ] Bookmark model + Hive box
- [ ] 북마크 추가/삭제 버튼 in viewer
- [ ] 북마크 목록 화면

### Day 2~3: 하이라이트/메모 (1~2일)
- [ ] Highlight + note per verse
- [ ] Text selection in viewer
- [ ] 저장 및 표시

### Day 3~5: 검색 (2일)
- [ ] In-app text search across books/chapters
- [ ] 검색 결과 리스트 (verse match)
- [ ] 결과 클릭 시 해당 위치 이동

### Day 5~6: 설정 (1일)
- [ ] Settings screen with font size slider
- [ ] Dark mode toggle (ThemeData switch)
- [ ] Shared preferences save

### Day 6~7: 결과 화면 및 통합 (1일)
- [ ] Search results UI polish
- [ ] Bottom nav to settings and bookmarks
- [ ] Integration testing

## Phase 4: UI/UX 고도화 (4~6일)
### Day 1: 다크모드 (1일)
- [ ] Theme provider with light/dark
- [ ] Color scheme customization

### Day 1~2: 접근성 (1~2일)
- [ ] Font size scaling test
- [ ] Screen reader labels
- [ ] High contrast mode

### Day 2~3: 상태 처리 (1일)
- [ ] Loading indicator during data load
- [ ] Error handling and retry UI

### Day 3~5: 반응형 (2일)
- [ ] LayoutBuilder for mobile/desktop
- [ ] Responsive padding/sizes

### Day 5~6: 브랜딩 (1일)
- [ ] App icon design
- [ ] Splash screen
- [ ] Launcher name update

## Phase 5: 플랫폼 확장 및 배포 (5~7일)
### Day 1~2: Android (2일)
- [ ] flutter build apk/appbundle
- [ ] Device testing on Android emulator/phone
- [ ] Signing config

### Day 2~4: iOS (2일)
- [ ] flutter build ios
- [ ] Xcode setup and test on simulator
- [ ] Provisioning profiles

### Day 4~5: Web (1~2일)
- [ ] flutter build web
- [ ] PWA manifest
- [ ] Deploy to GitHub pages or Netlify test

### Day 5~6: 릴리스 설정 (1일)
- [ ] pubspec version bump
- [ ] Build release artifacts
- [ ] CHANGELOG update

### Day 6~7: 스토어 (1일)
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

## 진행 상황 추적
- 현재: Phase 0 완료, Phase 1 상세 태스크 정리 완료
- 각 태스크는 하루 이하 단위로 분해하여 실행 가능
- 주간 리뷰 시 이 파일 업데이트

**다음 실행 추천**: Phase 1 첫 3~4개 태스크부터 (모델 정의 → 어댑터 → 파서 → 로드) 순차로 시작. 모든 Phase 완료 후 오늘자 스킬 재실행 및 git 업데이트.