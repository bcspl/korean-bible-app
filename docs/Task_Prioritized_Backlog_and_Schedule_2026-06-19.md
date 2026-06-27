# Korean Bible App - 우선순위별 Task 백로그 및 스케줄 (2026-06-19, Updated 2026-06-27)

> **참고**: 전체 로드맵은 `Project_Status_and_Updated_Roadmap_2026-06-19.md` 참조

## 현재 진행 상황 요약 (2026-06-27)
**전체 로드맵 대비 진행률**: Phase 0~2 완료 (약 40% 완료)
- ✅ 완료: Phase 0 (기반), Phase 1 (데이터 계층: 모델+어댑터+JSON 로더+시드), Phase 2 (기본 읽기 UI: 책목록/장선택/뷰어 + 검색 + 네비 + 홈)
- 🔄 진행중: UI/UX 폴리싱 (검색 강화, 디자인 개선 완료 직전)
- ⏳ 남은 주요: Phase 3 (사용자 기능: 북마크/설정 + 추가 콘텐츠: 찬송가 가사 및 악보 / 사도신경 / 주기도문 / 교독문 + "이 성경앱에 대해서"), Phase 4 (고도화), Phase 5 (배포)
- **당장 다음 할 일 (우선순위 Top 3)**:
  1. Phase 3 Day1~2: 북마크 기능 구현 (model + Hive + viewer 버튼 + 목록 화면)
  2. Phase 3 Day2~3: 설정 화면 구현 + 본문 검색 결과 polish (글꼴 크기/다크모드 토글)
  3. 찬송가 가사+악보 화면, 사도신경, 주기도문, 교독문, "이 성경앱에 대해서" 페이지 추가 (메모 기능 완전 배제)

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

## Phase 3: 핵심 사용자 기능 + 추가 콘텐츠 (5~7일) - ⏳ 미완료 (다음 집중)
### Day 1~2: 북마크 (1~2일) ⏳
- [ ] Bookmark model + Hive box
- [ ] 북마크 추가/삭제 버튼 in viewer
- [ ] 북마크 목록 화면

### Day 1~2: 북마크 기능 (1~2일) ⏳
- [ ] Bookmark 모델 (lib/models/bible_bookmark.dart) 생성 + @HiveType 어노테이션
- [ ] Hive box 'bookmarks' 열기 및 CRUD 메서드 구현 (BibleProvider에 추가)
- [ ] VerseViewerScreen에 북마크 토글 버튼 추가 (현재 장/절 저장)
- [ ] 북마크 목록 전용 화면 구현 (리스트 + 클릭 시 해당 verse로 이동)

### Day 2~3: 설정 화면 + 검색 결과 polish (1~2일) ⏳ (기본 검색 있음)
- [ ] SettingsScreen 생성: 글꼴 크기 슬라이더, 다크모드 스위치 (shared_preferences 사용 준비)
- [ ] 검색 결과 카드 UI 개선 (snippets 하이라이트 스타일링)
- [ ] VerseMatch 클릭 시 정확한 장/절 이동 + 스크롤 로직 강화
- [ ] AppBar/설정에서 테마 즉시 적용

### Day 3~4: 찬송가 가사 및 악보 보기 (2일) ⏳
- [ ] Hymn 모델 정의 + assets/data/hymns.json (또는 간단 샘플 데이터) 준비
- [ ] 찬송가 목록 화면 (제목/가사 검색 필터)
- [ ] 가사 상세 보기 화면 구현 (텍스트 + 악보 이미지 표시 지원)
- [ ] assets/images/hymns/ 폴더 구조 + 샘플 악보 이미지 경로 연결

### Day 4~5: 사도신경 / 주기도문 / 교독문 (1~2일) ⏳
- [ ] ApostlesCreedScreen 구현 (전문 표시, 복사 버튼, 읽기 편한 스타일)
- [ ] LordsPrayerScreen 구현
- [ ] ResponsiveReadingScreen: 교독문 목록 + 상세 (인도자/회중 구분 표시)
- [ ] "예배 자료" 메뉴 또는 별도 탭으로 3개 콘텐츠 통합 접근

### Day 5~6: "이 성경앱에 대해서" + 통합 + 범위 검증 (1일) ⏳
- [ ] AboutScreen 구현: 앱 설명, Public Domain 데이터 출처, 버전 표시, 라이선스, 피드백 링크
- [ ] BottomNavigationBar 재설계 (성경 | 예배자료 | 북마크 | 설정)
- [ ] Integration test 및 "메모/하이라이트 메모 기능 완전 배제" 확인, 불필요 코드 삭제

## Phase 4: UI/UX 고도화 (4~6일) - ⏳ 미완료
### Day 1: 다크모드 구현 (1일) ⏳
- [ ] ThemeProvider 생성 및 light/dark 모드 지원 (Provider로 전환)
- [ ] 다크모드 색상 스키마 커스터마이즈 및 즉시 토글

### Day 1~2: 접근성 강화 (1~2일) ⏳
- [ ] 글꼴 크기 동적 스케일 테스트 및 설정 연동
- [ ] Screen reader 라벨 추가 (Semantics)
- [ ] 고대비 모드 옵션 추가

### Day 2~3: 상태 처리 개선 (1일) ⏳
- [ ] 데이터 로딩 중 인디케이터 추가 (로딩 화면)
- [ ] 에러 처리 및 재시도 UI 구현

### Day 3~5: 반응형 레이아웃 (2일) ⏳
- [ ] LayoutBuilder 사용 모바일/데스크톱 대응
- [ ] 패딩/사이즈 반응형 조정

### Day 5~6: 브랜딩 (1일) ⏳
- [ ] 앱 아이콘 디자인 적용
- [ ] 스플래시 화면 구현
- [ ] 런처 이름 업데이트 (pubspec + 플랫폼 설정)

## Phase 5: 플랫폼 확장 및 배포 (5~7일) - ⏳ 미완료
### Day 1~2: Android 빌드 (2일) ⏳
- [ ] flutter build apk / appbundle 실행
- [ ] 에뮬레이터/실기기에서 Android 테스트 수행
- [ ] 서명 설정 (signing config)

### Day 2~4: iOS 빌드 (2일) ⏳
- [ ] flutter build ios 실행
- [ ] Xcode에서 시뮬레이터 테스트
- [ ] Provisioning profiles 설정

### Day 4~5: Web 배포 (1~2일) ⏳
- [ ] flutter build web 실행
- [ ] PWA manifest 설정
- [ ] GitHub Pages 또는 Netlify 테스트 배포

### Day 5~6: 릴리스 설정 (1일) ⏳
- [ ] pubspec.yaml 버전 bump
- [ ] 릴리스 빌드 아티팩트 생성
- [ ] CHANGELOG 업데이트

### Day 6~7: 스토어 준비 (1일) ⏳
- [ ] App store listing 텍스트 작성
- [ ] 스크린샷 준비
- [ ] 설명 및 키워드 작성

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
  1. Phase 3 Day1~2: Bookmark model + Hive box + viewer 버튼 + 목록 구현
  2. Phase 3 Day2~3: Settings screen + 검색 결과 polish 구현
  3. 찬송가/사도신경/주기도문/교독문/About 페이지 추가
- **시각적 트래킹** (매 스킬 실행시 갱신):
  로드맵: [████████░░░░░░░░░░░░░░░░] 40% 완료
  Phase별: Phase1 ██████████ 100% | Phase2 ██████████ 100% | Phase3 ░░░░░░░░░░ 0% | ...
- 주간 리뷰 시 이 파일 + PPTX 업데이트

**다음 실행 추천**: Phase 3부터 순차 (북마크 → 설정/검색 → 찬송가/신경/기도/교독문/About). 메모 기능 완전 제외. 모든 주요 Phase 완료 후 스킬 재실행.