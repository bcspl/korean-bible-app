# Changelog

## 1.0.1+2 — 2026-10-10

### Fixed (Android)
- 화면 하단이 시스템 내비게이션/제스처 바에 가려 마지막 절이 안 보이던 문제 (targetSdk 36 edge-to-edge 강제). edge-to-edge 유지, 각 스크롤 본문 하단 패딩에 `MediaQuery.viewPaddingOf(context).bottom` 추가 (성경 본문·장/책 목록·찬송가 상세/목록·사도신경·주기도문·교독문·예배자료·북마크·설정·앱 정보). 본문 화면은 FAB 높이만큼 추가 여유. MainScreen 탭 안에서는 BottomNavigationBar가 inset을 제거하므로 이중 패딩 없음.
- versionCode 1 → 2 (원스토어 업데이트)

## Unreleased

### Docs (2026-08-10)
- `docs/PROJECT_REPORT_2026-08-10.md` — comprehensive project report + UX/value recommendations  
- `docs/APPLIED_AND_ROADMAP_PLAN_2026-08-10.md` — applied vs planned (usability/value matrix)  
- `docs/STATUS_REPORT_2026-08-10.md` — status snapshot  
- README, roadmap, backlog, deploy checklist updated  
- Roadmap PPTX via roadmap-pptx skill (Desktop + `docs/roadmap-pptx/`)  

### Worship materials
- **사도신경 / 주기도문**: **개역한글 · KJV · ASV** (`lib/data/worship_texts.dart`)  
- **주기도문**: 마 6 서사 제외, **기도 본문만** 표시  
- **교독문**: 앱 자체 구성 51편 (시편·성탄·부활·이사야·누가); KRV/KJV/ASV 렌더  

### Changed
- **Bible source**: **개역한글(KRV)** only for Korean (not NKRV); Hive re-seed on wrong label / data_revision  
- About / Settings version strings  

### Multi-version Bible (KRV / KJV / ASV)
- Offline PD English Bibles: `eng_kjv_full.json`, `eng_asv_full.json`
- Verse viewer: select **up to 3 versions** and read verse-by-verse in parallel
- Book list version chips + multi-version search

### Text verification (2026-08-10)
- **KJV / ASV**: re-parsed from seven1m/open-bibles — 0 text diffs vs source; 31,102 verses; classic book totals match
- **KRV**: replaced incomplete open-bibles OSIS dump with complete **개역한글 PD** (`crizin/bible-db` holybible, 31,101 verses, 0 empty)
- Fixed missing books/chapters in old KRV (e.g. 2Chr was only 20 ch, Job 41, 1Pet 4)
- Golden verses (Gen 1:1, John 3:16, Ps 23:1, Rom 8:28, …) all pass
- Script: `python scripts/verify_bible_texts.py`

### Hymns (Public Domain expansion)
- Rebuilt catalog with **verified Public Domain** hymns (full multi-stanza **English + Korean** lyrics where available)
- Each hymn includes: author, composer, year, **history/origin**, **license + PD note**
- UI: PD banner on hymn list, PD badge / history / license panel on detail, **KO/EN lyrics toggle**
- Search: title, lyrics (both languages), author, composer, history
- Removed non-PD entries (e.g. How Great Thou Art EN 1949, 1960s folk hymns)
- Regenerated educational PD-style score SVGs to match catalog count

## 1.0.0+1 — 2026-07-17

### Added
- Offline Korean Bible reading (book / chapter / verse)
- Bookmarks (verse + chapter)
- Worship materials: Apostles’ Creed, Lord’s Prayer, responsive readings
- Public Domain hymns (104): list, search, favorites, educational SVG scores
- Favorite hymns also listed on Bookmarks tab
- Settings: dark mode, text scale, high contrast
- 5-tab navigation; branding icon + splash

### Notes
- Hymn catalog expansion and real Korean full-page scores: **parked**
- Android release currently uses **debug signing** until production keystore is configured
- Package ID still `com.example.korean_bible_app` (change before Play Store)

### Dev / ops
- `docs/DEPLOY_CHECKLIST.md` — Phase 5 deploy path
- Roadmap PPTX: Desktop + `docs/roadmap-pptx/`
