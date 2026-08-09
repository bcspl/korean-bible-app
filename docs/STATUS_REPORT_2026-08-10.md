# Korean Bible App — Status Report

**Date:** 2026-08-10  
**Method:** Code + assets + `flutter test` + `verify_bible_texts.py`  
**Related:** `docs/PROJECT_REPORT_2026-08-10.md`

---

## 1. Health check

| Check | Result |
|--------|--------|
| `flutter test` | **5/5 passed** |
| `flutter analyze` | **0 errors** (prefer_const infos only) |
| `verify_bible_texts.py` | **PASS** |
| KRV | 66 books · **31,101** verses · empty **0** |
| KJV | 66 books · **31,102** verses · empty **0** · reparse diff **0** |
| ASV | 66 books · **31,102** verses · empty **0** · reparse diff **0** |
| Hymns | **102** PD · KO/EN · history/license |
| Responsive readings | **51** · categories 시편/성탄/부활/이사야/누가 |
| Worship texts | `lib/data/worship_texts.dart` (기도 본문만) |
| Branding | icon + splash; label 한국어 성경 |
| Android APK | 이전 빌드 유지 (debug-signed) — 재빌드 권장 |
| Web | 이전 `build/web/` 유지 |
| iOS | ⛔ Mac + Xcode 필요 |

---

## 2. Progress snapshot

```
Overall  [██████████████████░░] ~92%
Phase 0–3  100% ✅
Phase 4     96% ✅  (PD content + multi-version)
Phase 5     40% ⏳  APK+Web; store/signing open
```

| Milestone | Status |
|-----------|--------|
| M1–M3 | ✅ |
| M4 multi-platform | ⏳ ~45% (builds exist) |
| M5 store | ⏳ blocked on decisions |
| Multi-version + text QA | ✅ |

---

## 3. Work completed since 2026-07-17

### Bible
- [x] Label/source: **개역한글(KRV)** not NKRV  
- [x] Full KRV rebuild (holybible PD) — fixed incomplete OSIS (2Chr/Job/1Pet etc.)  
- [x] KJV + ASV offline assets  
- [x] Parallel verse UI (max 3 versions)  
- [x] Automated verification script  

### Hymns
- [x] PD catalog rebuild (102)  
- [x] History, license banner, KO/EN lyrics  

### Worship
- [x] Creed / Lord’s Prayer: KRV · KJV · ASV  
- [x] Lord’s Prayer: **prayer body only** (no “pray ye” narrative)  
- [x] Responsive readings 51, app-owned categories  

### Docs
- [x] PROJECT_REPORT_2026-08-10  
- [x] APPLIED_AND_ROADMAP_PLAN_2026-08-10 (현재 적용 vs 향후 계획 · 사용성·가치)  
- [x] This status report  
- [x] README / roadmap / backlog / CHANGELOG updates  
- [x] Roadmap PPTX skill: Desktop + `docs/roadmap-pptx/*_2026-08-10.pptx`  

---

## 4. Remaining (next session)

### Top 3
1. User decisions: package ID, store targets, keystore, privacy URL, support email  
2. Production Android signing + AAB  
3. Device smoke-test + optional onboarding / version preference persistence  

### Parked
- Hymn official scores / large catalog expansion beyond PD set  

---

## 5. How to re-verify

```powershell
cd "C:\Users\LSH\Bible App\korean-bible-app"
python scripts/verify_bible_texts.py
flutter test
```

---

*Status report — 2026-08-10*
