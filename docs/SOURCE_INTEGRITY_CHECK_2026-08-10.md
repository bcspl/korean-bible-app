# 소스·에셋 반영 무결성 점검

**Date:** 2026-08-10  
**Purpose:** 세션에서 구현한 기능이 디스크 소스/에셋에 실제 존재하는지 확인  

---

## 1. 핵심 소스 파일

| Path | Status | Role |
|------|--------|------|
| `lib/models/bible_version.dart` | ✅ | KRV/KJV/ASV enum |
| `lib/services/bible_data_service.dart` | ✅ | 다역본 로드, revision reseed |
| `lib/providers/bible_provider.dart` | ✅ | activeVersions 1–3, verseTextFor |
| `lib/widgets/bible_version_selector.dart` | ✅ | 역본 칩 UI |
| `lib/screens/verse_viewer_screen.dart` | ✅ | 절 병렬 표시 |
| `lib/screens/book_list_screen.dart` | ✅ | 역본 선택 포함 |
| `lib/data/worship_texts.dart` | ✅ | 기도·신경 역본 문안 |
| `lib/screens/lords_prayer_screen.dart` | ✅ | WorshipTexts 사용 |
| `lib/screens/creed_screen.dart` | ✅ | WorshipTexts 사용 |
| `lib/screens/responsive_reading_screen.dart` | ✅ | 구절 참조 렌더 |
| `lib/screens/hymn_list_screen.dart` | ✅ | PD 배너 |
| `lib/screens/hymn_detail_screen.dart` | ✅ | history/license/한영 |
| `scripts/verify_bible_texts.py` | ✅ | 본문 회귀 검증 |
| `scripts/download_pd_bibles.py` | ✅ | KJV/ASV 생성 |
| `scripts/build_pd_hymn_catalog.py` | ✅ | 찬송 생성 |
| `scripts/build_responsive_readings.py` | ✅ | 교독 참조 생성 |

## 2. 에셋

| Asset | Status | Notes |
|-------|--------|-------|
| `assets/data/kor_bible_full.json` | ✅ | KRV · ~7.1 MB · revision holybible-pd |
| `assets/data/eng_kjv_full.json` | ✅ | ~4.9 MB |
| `assets/data/eng_asv_full.json` | ✅ | ~4.9 MB |
| `assets/data/hymns.json` | ✅ | count 102 |
| `assets/data/responsive_readings.json` | ✅ | count 51 |
| `assets/images/hymns/score_*.svg` | ✅ | catalog-aligned |
| `pubspec.yaml` `assets/data/` | ✅ | 폴더 통째 등록 |

## 3. 런타임 품질

| Check | Result |
|-------|--------|
| `flutter test` | 5/5 PASS |
| `python scripts/verify_bible_texts.py` | PASS |
| analyze errors | 0 |

## 4. 문서

| Doc | Status |
|-----|--------|
| `docs/PROJECT_REPORT_2026-08-10.md` | ✅ |
| `docs/STATUS_REPORT_2026-08-10.md` | ✅ |
| `docs/SOURCE_INTEGRITY_CHECK_2026-08-10.md` | ✅ (this file) |
| `README.md` | ✅ updated |
| `CHANGELOG.md` | ✅ updated |
| Roadmap / backlog / deploy checklist | ✅ updated |

## 5. 결론

**구현 코드와 데이터가 프로젝트 소스 트리에 반영되어 있으며**, 테스트·본문 검증이 통과한 상태이다.  
배포용 APK/Web은 콘텐츠 변경 이후 **재빌드**를 권장한다.

---

*Integrity check completed 2026-08-10*
