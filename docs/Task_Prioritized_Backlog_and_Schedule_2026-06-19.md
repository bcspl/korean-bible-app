# Korean Bible App - 우선순위별 Task 백로그 및 스케줄 (2026-06-19, Updated 2026-06-27)

> **참고**: 전체 로드맵은 `Project_Status_and_Updated_Roadmap_2026-06-19.md` 참조

## 현재 진행 상황 요약 (2026-06-27, /roadmap-pptx 재실행 - 코드 상태 검사 완료)
**전체 로드맵 대비 진행률**: ~60% 완료 (Phase 0-3 대부분 ✅)
- ✅ 완료: Phase 0-2 + Phase 3 (북마크, 찬송가 검색+즐겨찾기, 신경/기도/교독문 dual, About, BottomNav, 다크모드+글꼴 슬라이더)
- 🔄 진행중: Phase 4 고도화 시작
- ⏳ 남은 주요: Phase 4 (접근성, 로딩/에러, 반응형, 브랜딩), Phase 5 (배포)
- **당장 다음 할 일 (우선순위 Top 3)**:
  1. Phase 4: 접근성 강화 (Semantics, high contrast)
  2. Phase 4: 로딩/에러 UI + 반응형
  3. 설정 폰트 크기 완성 (이미 slider 추가됨) + 예배자료 BottomNav 통합

**시각적 진행 표시**:
```
로드맵 전체: [█████████████░░░░░░░] ~65%
Phase 0-3:   [█████████████] 95% ✅
Phase 4:     [░░] 10% ⏳
Phase 5:     [░] 0% ⏳
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

## Phase 3: 핵심 사용자 기능 + 추가 콘텐츠 (5~7일) ✅ 완료
### 북마크 ✅
- [x] Bookmark 모델 + Hive + CRUD + viewer toggle + 목록 화면

### 설정 + 폴리싱 ✅
- [x] SettingsScreen: 글꼴 크기 슬라이더 (0.8~2.0, 시스템 연동), 다크모드, 고대비 스위치
- [ ] 검색 결과 UI 하이라이트 개선 (snippets 스타일링) - remaining

### 찬송가 ✅
- [x] Hymn 모델 + hymns.json (PD samples)
- [x] 목록 (검색 + 즐겨찾기)
- [x] 상세 (가사 + placeholder)
- [ ] 즐겨찾기 하이라이트 기능 (목록 강조 + 상세 하이라이트)
- [ ] assets/images/hymns/ 실제 이미지

### 사도신경 / 주기도문 / 교독문 / About ✅
- [x] Dual version screens (개역한글/개역개정)
- [x] Responsive reading
- [x] AboutScreen
- [x] Bottom nav with 예배자료 tab + popup

### 통합 ✅
- [x] BottomNavigationBar (5 tabs)
- [x] Theme + scale + high contrast
- [x] Phase 3 scope verification (no memos)

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
- **전체 대비**: ~65% (Phase 0-3 ✅, Phase 4 시작)
- **완료된 상태**: Phase 0-3 (북마크, hymns with fav+search, dual creeds/prayers, about, bottom nav 5 tabs, theme+dark+font+highContrast, loading/error basics, responsive start)
- **추가 백로그**: 즐겨찾기 하이라이트
- **남은 것**: Phase 4 (고도화: dark polish, full accessibility, full responsive, branding, more error/loading), Phase 5 (배포)
- **당장 다음 할일 (상세, <1주 단위)**: 
  1. 즐겨찾기 하이라이트 구현 (hymn/bookmark 강조)
  2. Phase 4: dark color customization + full responsive (book/verse screens)
  3. Accessibility expansion (more Semantics, test scales)
  4. Loading/error across all screens
  5. Branding: prepare icon.png + generate
- **시각적 트래킹**:
  로드맵: [█████████████░░░░░░░] ~65%
  Phase별: 0-3 █████████████ 95% | 4 ░░░░░ 10% | 5 ░░░░░ 0%
- 주간 리뷰 시 이 파일 + PPTX 업데이트

**다음 실행 추천**: Phase 4 고도화 + favorites highlight. 모든 Phase 후 roadmap-pptx + commit.