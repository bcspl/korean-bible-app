# Korean Bible App Project - 종합 현황 및 로드맵 (Updated 2026-06-27)

**현재 진행 상황 요약 (2026-07-04 업데이트)**:
- **전체 대비**: ~85% 완료 (Phase 0-3 완전, Phase 4 대부분, Phase 5 초기)
- **시각적 진행**: [████████████████░░░░] ~85%
- **완료**:
  - Phase 0-2: 데이터 모델/Hive/로더 + 기본 읽기 UI (책/장/본문, 검색, 네비)
  - Phase 3: 북마크 (전체 CRUD + viewer), 찬송가 (35곡 PD + 다운로더 + 검색/fav/상세), 예배자료 (신경/기도/교독문 dual), About, 5탭 BottomNav, Theme (dark + scale + highContrast)
  - Phase 4:
    - Branding: icon.png + flutter_launcher_icons + native_splash:create 실행
    - Responsive: book_list, chapter_list, hymn_list, settings, bookmark_list, worship, hymn_detail, about 등에 LayoutBuilder/MediaQuery 적용
    - Accessibility: Semantics 라벨 (book, verse, settings, hymn 등), highContrast 효과 강화
    - Loading/Error: book_list + hymn/settings/worship/bookmark 등 확장
    - Dark polish + hymn list 스크롤 최적화 (debounce 250ms, O(1) fav Set, tileColor, ValueKey)
    - Hymns: scripts/hymn_downloader.py + 35곡 + 메타데이터 (title_en/author/year/source) + UI 개선
- **현재 hymns**: 35곡 (Public Domain, 2026-07-04)
- **당장 다음 (상세)**:
  1. Phase 5: Android 빌드 + 테스트 + signing
  2. Phase 5: iOS + Web (PWA) 빌드 + 테스트
  3. Hymns 추가 확장 (Hymnary CSV로 100+곡), 남은 화면 full responsive/Semantics, store assets
- **남은 주요**: Phase 5 (크로스 플랫폼 빌드/릴리스/스토어), hymns 대량, 최종 polish + 테스트

## 프로젝트 개요
**완전 무료 오프라인 한국어 성경 앱**  
Public Domain 데이터(개역개정 등)를 사용하여 인터넷 없이도 성경을 읽고, 검색하고, 북마크할 수 있는 크로스 플랫폼 앱입니다. 찬송가 가사 및 악보, 사도신경, 주기도문, 교독문을 제공하며 "이 성경앱에 대해서" 정보 페이지도 포함합니다.

- **주요 목표**: 접근성(큰 글씨, 다크모드) 중심의 편리한 성경 읽기 경험 + 기독교 예배/묵상 자료 제공
- **기술 비전**: Flutter + Hive로 모든 플랫폼(Android, iOS, Web, Windows, macOS, Linux)에서 완전 오프라인 동작
- **데이터 출처**: Public Domain 한국어 성경 (개역개정 등), 찬송가, 신경/기도/교독문 등

## 현재 상태 (2026-06-27 기준) - 시각적 요약 포함

### 진행률 시각화
```
전체 로드맵 (Phase 0-5): [████████████████░░░░] ~85% 완료
Phase 0: ██████████ 100% ✅ (기반)
Phase 1: ██████████ 100% ✅ (데이터 계층)
Phase 2: ██████████ 100% ✅ (기본 읽기 UI)
Phase 3: ██████████ 100% ✅ (북마크, hymns 35곡, 예배자료, About, BottomNav)
Phase 4: ███████████ 80% ✅ (branding, responsive, accessibility, loading/error, dark, hymns+scroll)
Phase 5: ███░░░░░░░ 10% ⏳ (빌드/배포 준비)
```

**해야할 작업 (상세, 우선순위 Top, <1-2주 단위)**:
1. **Phase 5 Android** (Day1-2): build apk/appbundle, emulator+실기기 테스트, signing config
2. **Phase 5 iOS + Web** (Day2-4): ios archive, Web PWA + offline test + deploy
3. **Hymns 확장** (100+곡): Hymnary PD CSV export → hymn_downloader.py 실행 → hymns.json 갱신
4. **Phase 4 마무리**: creed/lords/responsive_reading responsive + Semantics, 전체 화면 audit, store screenshots 준비

**상세 해야할 작업 (Granular)**:
- Android signing + keystore
- iOS provisioning profiles
- PWA manifest + service worker
- Hymn CSV 100곡+ (PD filter)
- creed/lords_prayer/responsive_reading full responsive + Semantics
- Full Semantics + accessibility test
- Store listing text + multi-device screenshots
- Version bump + CHANGELOG + artifacts
- Large JSON perf optimization (if needed)

## 마일스톤 및 상세 Gantt (일정)
**주요 마일스톤**:
- M1: Phase 0-2 완료 (MVP 읽기 UI) - 2026-06-27 ✅
- M2: Phase 3 완료 (북마크 + hymns 35곡 + 예배자료 + BottomNav) - 2026-07-04 ✅ (앞당김)
- M3: Phase 4 완료 (Branding + Responsive + Accessibility + Loading/Error + Dark + Hymns 최적화) - 2026-07-11
- M4: Phase 5 완료 (Android/iOS/Web 빌드 + Store) - 2026-07-25
- M5: 스토어 릴리스 - 2026-08-05

**상세 Gantt (주 단위 + 해야할 작업 세분화)**:
```
Week | Phase | 해야할 작업 (Granular)                                      | Status
-----|-------|-------------------------------------------------------------|--------
1-4  | 0-3   | (완료) 데이터/읽기 UI, 북마크, hymns 35곡, 예배자료, Theme | ✅
5    | 4     | (완료) downloader, 35 hymns, Branding, Scroll fix, Resp     | ✅
5-6  | 4     | hymns CSV 100+ , creed/lords/responsive full resp+Semantics | ⏳
6-7  | 5     | Android build + test + signing                              | ⏳
7    | 5     | iOS build/archive + Web PWA + deploy test                   | ⏳
7-8  | 5     | Store assets (screenshots, listing), version bump, artifacts| ⏳
8+   | 5     | Internal release, feedback, 스토어 제출                     | 
```

(상세 테이블은 백로그 MD "해야할 작업" 섹션 참조. PPTX Gantt 슬라이드에 시각화)

**세분화된 다음 작업 (Phase 4 잔여 + Phase 5)**:
- Phase 4 잔여: creed/lords/responsive_reading full responsive + Semantics, hymn CSV import (100+), remaining polish
- Phase 5: Android (build, emulator, signing) → iOS (archive) → Web (PWA deploy) → Store prep (listing, screenshots, keywords)

(간트 바는 PPTX의 "마일스톤 & 간트 차트" 슬라이드에 시각화. 백로그 MD에 Day-by-Day 상세 tasks)

(상세 Gantt는 PPTX 스킬에서 시각화)

### 완료된 작업 (2026-07-04 sync)
- Phase 0-2: 전체 데이터 (모델, Hive 어댑터, JSON 로더, BibleDataService), 기본 읽기 (book_list bilingual/search/filter, chapter grid, verse viewer RichText + prev/next/home)
- Phase 3: 북마크 (full CRUD + Hive + viewer toggle + list), hymns (35 PD + downloader.py + search/fav/detail + metadata), worship (creed/prayer/responsive dual), About, 5탭 BottomNav, ThemeProvider (dark/scale/highContrast)
- Phase 4: Branding (icon.png + generators), Responsive (8+ screens with LayoutBuilder/MediaQuery), Accessibility (Semantics + highContrast), Loading/Error extended, Dark polish, Hymn list scroll (debounce, O(1) fav, keys, tileColor), Tests (5 pass)
- Docs: MD sync, PPTX with Gantt/milestones/granular

### 현재 코드 상태
- hymns.json: 35곡, last_updated 2026-07-04
- lib/screens: responsive + some Semantics on key screens
- provider: isHymnFavorite O(1), loadHymns with source_note
- scripts/hymn_downloader.py: CSV support + built-in PD
- Branding applied, Windows build OK, analyze clean

### 문서 상태
- 본 로드맵: 2026-06-27 업데이트 (시각적 진행 + 다음 할일 명확화)
- `Task_Prioritized_Backlog_and_Schedule_2026-06-19.md`: 상세 Phase 1~5 일/주 단위 태스크 + 완료 표시 + 시각적 트래킹 섹션
- `Feature_Specification_v2.md`: Placeholder
- `bible_data_parser_and_instructions.md`: Placeholder

## 기술 스택 및 설계 결정
- **프레임워크**: Flutter (크로스 플랫폼)
- **로컬 저장소**: Hive (NoSQL, 빠른 쿼리, 오프라인 최적화)
- **상태 관리**: Provider (간단하고 충분)
- **UI**: Material Design + 접근성 고려 (폰트 크기, 다크모드)
- **데이터 포맷**: JSON (현재) → 필요시 OSIS 파서 연동
- **에셋**: `assets/data/` 전체 등록 (성경 전체 데이터 번들)

향후 고려:
- 큰 데이터 파일 최적화 (lazy load, 인덱싱)
- 추가 의존성: `shared_preferences` (설정), `intl` (날짜)

## 개발 단계 (Phase) 및 마일스톤

### Phase 0: 기반 구축 (완료)
- 프로젝트 초기화, 의존성, 기본 스켈레톤, 데이터 파일 배치, 빌드 환경 검증
- **상태**: 완료

### Phase 1: 데이터 계층 구현 (최우선 - MVP 기반)
- 성경 데이터 모델 정의 (BibleBook, Chapter, Verse 등)
- Hive 어댑터 생성 (`hive_generator` + `build_runner`)
- JSON 파서 구현 (샘플 → 전체 데이터)
- 앱 시작 시 데이터 로드 및 Hive에 시드
- 성능 테스트 (7MB+ JSON 로딩 시간)
- **목표 산출물**: "성경 데이터가 앱에서 사용 가능" 상태

### Phase 2: 핵심 읽기 기능 (MVP)
- 책 목록 화면 (구약/신약 분류)
- 장 선택 및 절 목록 뷰
- 성경 본문 뷰어 (스크롤, 큰 글씨)
- 기본 네비게이션 (이전/다음 장, 책 이동)
- 현재 읽기 위치 저장 (간단한 설정)
- **목표 산출물**: 사용자가 실제로 성경을 읽을 수 있는 앱

### Phase 3: 사용자 중심 기능
- 북마크 (Hive 저장)
- 텍스트 검색 결과 polish + 설정 화면 (글꼴 크기, 테마)
- 찬송가 가사 및 악보 보기 기능
- 사도신경, 주기도문, 교독문 추가
- "이 성경앱에 대해서" 페이지
- 하단 네비게이션 실제 연결
- **목표 산출물**: 실사용 가능한 일상 앱 (메모 기능 완전 배제)

### Phase 4: UI/UX 고도화 및 접근성
- 반응형 디자인 (모바일/데스크톱)
- 다크모드 완성 및 커스텀 테마
- 큰 글씨 / 접근성 감사
- 애니메이션 및 부드러운 네비게이션
- 에러 처리 및 로딩 상태
- **목표 산출물**: 품질 높은 사용자 경험

### Phase 5: 크로스 플랫폼 완성 및 배포
- Android / iOS 빌드 및 테스트
- Web 배포 (PWA)
- Windows/macOS/Linux 데스크톱 최적화
- 앱 아이콘, 스플래시, 릴리스 설정
- Google Play / App Store / Microsoft Store 준비
- **목표 산출물**: 실제 사용자에게 배포 가능한 제품

### Phase 6: 고급 기능 및 유지보수 (미래)
- 오디오 성경 (TTS 또는 미리 녹음)
- 여러 성경 번역 지원
- 클라우드 동기화 (선택적, Google Drive 등)
- 통계/읽기 진도 추적
- 커뮤니티 기능 (주석 공유 등)
- 지속적인 데이터 업데이트 파이프라인

## 주요 리스크 및 대응
- **대용량 데이터**: 7MB JSON → Phase 1에서 인덱싱/부분 로드 전략 수립
- **모바일 성능**: Hive + 효율적인 쿼리로 해결
- **데이터 정확성**: Public Domain 데이터 검증 필요 (다운로더 스크립트 활용)
- **플랫폼 차이**: Flutter의 장점 활용하되, 데스크톱 특화 UI 별도 고려
- **문서 부재**: 백로그와 스펙 문서를 Phase 1 초기에 실제 내용으로 채우기

## 업데이트 이력
- **2026-06-19**: 초기 프로젝트 생성, 문서 placeholder 작성
- **2026-06-20**: 전체 분석 후 본 로드맵 상세 작성. Phase 구조화, 현재 상태 업데이트, 기술 결정 기록. 기본 앱 스켈레톤 및 빌드 성공 반영.
- **2026-06-27**: 상세 일/주 단위 작업 분해 (Phase 1~5) 백로그에 반영. roadmap-pptx 스킬 재실행으로 PPTX 업데이트. Phase 1 (모델+어댑터+JSON 로더) 완료, Phase 2 UI 진행 중.

## 참고 문서
- `Task_Prioritized_Backlog_and_Schedule_2026-06-19.md` (우선순위 백로그)
- `Feature_Specification_v2.md`
- `bible_data_parser_and_instructions.md`
- `pubspec.yaml`
- `README.md`, `README_Source_Code.md`

---

**다음 단계**: 이 로드맵에 기반한 구체적인 작업 순서는 별도 제안 문서 또는 백로그에 정리합니다. (아래 응답 참조)