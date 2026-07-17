# Korean Bible App - 우선순위별 Task 백로그 및 스케줄 (2026-06-19, Updated 2026-06-27)

> **참고**: 전체 로드맵은 `Project_Status_and_Updated_Roadmap_2026-06-19.md` 참조

## 현재 진행 상황 요약 (2026-07-17 EOD — session ceased)
**전체 로드맵 대비 진행률**: **~88%** 완료
- ✅ 완료: Phase 0–4 (hymn expand frozen) + Phase 5 partial
  - hymns: **104 PD**, renumber, fav on 북마크, educational SVG (**PARKED** further work)
  - **APK release** 54.9 MB ✅ · **Web release** `build/web` ✅
  - Tests 5/5 · analyze 0 errors · label `한국어 성경`
- ⏸ **PARKED:** more hymns, real Korean score images
- ⏳ **NEXT session:** production signing, AAB, store decisions, device smoke-test
- **당장 다음 할 일 (Top 3)**:
  1. User decisions (package ID, ship target, keystore, privacy URL, email)
  2. Android production signing + `appbundle`
  3. Store listing + APK device smoke-test

**시각적 진행 표시**:
```
로드맵 전체: [█████████████████░░░] ~88%
Phase 0-3:   [█████████████] 100% ✅
Phase 4:     [████████████] ~95% ✅ (hymns frozen)
Phase 5:     [████░░░░░░] ~40% ⏳ (APK+Web done)
```

**마일스톤 (2026-07-17 EOD)**:
- M1 Phase 0-2 MVP ✅ 2026-06-27
- M2 Phase 3 features ✅ 2026-07-04
- M3 Phase 4 polish ✅ ~95%
- M4 Phase 5 builds ⏳ ~40% (APK+Web ✅; AAB/signing/iOS open) target 2026-07-25
- M5 Store package ⏳ target 2026-08-05 (blocked on user decisions)

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

### 찬송가 ✅ (current scope frozen — expansion PARKED)
- [x] Hymn 모델 + hymns.json (**104 PD**, renumbered 1..N)
- [x] 목록 (검색 + 즐겨찾기) / 상세 (가사 + SVG placeholder 악보)
- [x] 즐겨찾기 하이라이트 + **북마크 탭에 즐겨찾기 찬송 표시**
- [x] `scripts/generate_hymn_scores.py` (교육용 간소화 SVG — 공식 악보 아님)
- [ ] ~~추가 찬송 / CSV 확장~~ → **PARKED (later)**
- [ ] ~~실제 한국 찬송가 전체 악보 이미지~~ → **PARKED (later; license / PD scan / engrave)**

### 사도신경 / 주기도문 / 교독문 / About ✅
- [x] Dual version screens (개역한글/개역개정)
- [x] Responsive reading
- [x] AboutScreen
- [x] Bottom nav with 예배자료 tab + popup

### 통합 ✅
- [x] BottomNavigationBar (5 tabs)
- [x] Theme + scale + high contrast
- [x] Phase 3 scope verification (no memos)

## Phase 4: UI/UX 고도화 (4~6일) - ✅ 80% (2026-07-04)
### Day 1: 다크모드 + HighContrast (1일) ✅
- [x] ThemeProvider + 다크모드 + text scale
- [x] 고대비 모드 + verse/bookmark highlight
- [x] Dark polish (readability)

### Day 1~2: Accessibility + Responsive (2일) ✅
- [x] Semantics (book_list, verse_viewer, settings, hymn_list/detail)
- [x] highContrast 적용
- [x] LayoutBuilder/MediaQuery on book, chapter, hymn_list, settings, bookmark, worship, hymn_detail, about (pad 16/24/32)

### Day 2~3: Loading/Error + Scroll (1일) ✅
- [x] Loading/error on hymn/settings/worship/bookmark + book_list
- [x] Hymn list scroll fix (debounce 250ms, provider.isHymnFavorite O(1) Set, tileColor, ValueKey)

### Day 3~5: Hymns + Branding (2일) ✅
- [x] hymn_downloader.py (CSV support)
- [x] 35 PD hymns + metadata + UI (author, count, better empty states)
- [x] Branding: icon.png placed + flutter_launcher_icons + native_splash:create

### Day 5~6: Tests + Docs (1일) ✅
- [x] 5 widget tests (incl. hymn tab, highContrast)
- [x] MD + PPTX sync (Gantt, granular)

## Phase 5: 플랫폼 확장 및 배포 (5~7일) - ⏳ 10% (2026-07-04)
### Day 1~2: Android (2일) ⏳
- [ ] flutter build apk/appbundle
- [ ] Emulator + real device test
- [ ] Signing + keystore setup

### Day 2~4: iOS + Desktop (2일) ⏳
- [ ] flutter build ios (sim + archive)
- [ ] Desktop (Windows) build + verify icons/splash
- [ ] Certificates / provisioning

### Day 4~5: Web + PWA (1~2일) ⏳
- [ ] flutter build web --release
- [ ] PWA manifest + offline test
- [ ] Deploy test (e.g. Netlify)

### Day 5~6: Release + Assets (1일) ⏳
- [ ] Version + changelog
- [ ] Artifacts for all platforms
- [ ] Store listing text + screenshots (multi-device)

### Granular next (Phase 4 remain + 5)
- [ ] Hymn CSV 100+ via downloader (Hymnary PD filter)
- [ ] creed/lords/responsive_reading full responsive + Semantics
- [ ] Full Semantics audit + accessibility test
- [ ] Large JSON perf (if needed)
- [ ] Store graphics + keywords + privacy

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

## 해야할 작업 (To-Do, 2026-07-17 EOD — session ceased)
**Status:** 오늘 작업 종료. 다음 세션 = Phase 5 잔여 + 스토어 결정 대기.

### 즉시 우선 (Top 3) — next session
1. **User decisions** (see `docs/DEPLOY_CHECKLIST.md`): package ID, ship target, keystore, privacy URL, support email  
2. **Android production**: keystore + `key.properties` + `flutter build appbundle --release`  
3. **Ship package**: device APK smoke-test + store listing/screenshots/privacy  

### Phase 4 residual
- [ ] Optional: clear remaining `prefer_const` analyze infos  
- [x] Semantics / responsive on worship materials  

### ⏸ PARKED — Hymn expansion (later)
Do **not** schedule until user reopens:
- [ ] More hymns (CSV / Hymnary / expand scripts)
- [ ] Real full-page Korean score **images** (PNG)
- [ ] Score source: license 찬송가공회 | PD Hymnary scans | MuseScore/LilyPond
- [ ] Zoomable multi-page score UI  

**Frozen:** 104 PD hymns, #1–104, SVG scores, fav on 북마크  

### Phase 5 (deploy)
- [x] `flutter build apk --release` → `build/app/outputs/flutter-apk/app-release.apk` (54.9 MB, **debug-signed**)  
- [x] `flutter build web --release` → `build/web/`  
- [x] CHANGELOG + DEPLOY_CHECKLIST + key.properties.example  
- [ ] Device install / smoke-test APK  
- [ ] Change applicationId from `com.example.korean_bible_app`  
- [ ] Release keystore + signingConfig (not debug)  
- [ ] `flutter build appbundle --release`  
- [ ] Web host/deploy (optional)  
- [ ] iOS build (Mac only)  
- [ ] Store listing + multi-device screenshots + keywords/privacy  

### Phase 6+ (future)
- TTS, multi-translation, cloud sync, reading stats  
- **Resume hymn agenda** when unparked  

**시각적 트래킹**: [█████████████████░░░] ~88% | P0-3 100% | P4 ~95% | P5 ~40% | hymns ⏸  
**마일스톤**: M1✅ M2✅ M3✅~95% | M4⏳~40% | M5⏳ store  
**Last updated**: 2026-07-17 EOD — work **ceased**