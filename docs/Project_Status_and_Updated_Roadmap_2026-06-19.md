# Korean Bible App Project - 종합 현황 및 로드맵

**Verified status: 2026-07-17 EOD** (code + APK/Web builds + docs)  
**Session closed** — next session starts at Phase 5 remaining / store decisions  

## Executive summary
| Item | Value |
|------|--------|
| Overall progress | **~88%** |
| Phase 0–3 | **100% ✅** |
| Phase 4 | **~95% ✅** (hymn expand/scores PARKED) |
| Phase 5 | **~40% ⏳** (APK + Web built; signing/store/iOS open) |
| Hymns (PD) | **104** sequential; educational SVG scores |
| Screens | **13** (Semantics 13/13, Responsive 12/13) |
| Branding | icon + launcher + splash; label **한국어 성경** |
| Tests | **5/5 passed** |
| Analyze | **0 errors** (19 prefer_const infos) |
| APK | ✅ `app-release.apk` 54.9 MB (debug-signed) |
| Web | ✅ `build/web/` |

```
전체: [█████████████████░░░] ~88%
P0  ██████████ 100% ✅
P1  ██████████ 100% ✅
P2  ██████████ 100% ✅
P3  ██████████ 100% ✅
P4  █████████░  95% ✅
P5  ████░░░░░░  40% ⏳
```

---

## Verified completed work

### Phase 0–3 ✅
- Bible data/Hive, book/chapter/verse UI, search, OT/NT
- Bookmarks CRUD; 5-tab nav; theme (dark/scale/highContrast)
- Worship: creed, Lord’s Prayer, responsive reading
- Hymns: 104 PD, search/fav/detail, fav on 북마크, renumber 1–104

### Phase 4 ✅ (~95%)
- Branding, responsive, Semantics, scroll/perf, loading/error
- Hymn expansion + real full Korean scores: **PARKED** (user 2026-07-17)

### Phase 5 partial ✅ (today)
- Release APK build succeeded
- Web release build succeeded
- Deploy checklist, CHANGELOG, key.properties.example
- Gitignore for signing secrets

---

## Immediate Top 3 (next session)

1. **User decisions** — package ID, display name confirm, ship target (Play / APK / Web / iOS later), keystore, privacy URL, support email  
2. **Android production signing** — keystore + AAB (Play)  
3. **Store package + APK smoke-test** on real device  

See `docs/DEPLOY_CHECKLIST.md`.

### ⏸ PARKED — Hymn expansion (later)
- More hymns / CSV  
- Real full-page Korean score images (license | PD scans | self-engrave)  
- Zoomable multi-page score UI  

### Phase 5 remaining
- [x] APK release (debug-signed)  
- [x] Web release  
- [ ] Device smoke-test  
- [ ] applicationId ≠ `com.example.*`  
- [ ] Release keystore + appbundle  
- [ ] Web host (optional)  
- [ ] iOS (Mac)  
- [ ] Store listing / screenshots / privacy  

### Phase 6+ (future)
- TTS, multi-translation, cloud sync, reading stats  
- Resume hymn agenda when unparked  

---

## Milestones

| ID | Milestone | Target | Status |
|----|-----------|--------|--------|
| **M1** | Phase 0–2 MVP | 2026-06-27 | ✅ Done |
| **M2** | Phase 3 features | 2026-07-04 | ✅ Done |
| **M3** | Phase 4 polish | 2026-07-20 | ✅ ~95% |
| **M4** | Phase 5 builds | 2026-07-25 | ⏳ ~40% (APK+Web; AAB/iOS open) |
| **M5** | Store release | 2026-08-05 | ⏳ Pending decisions |

### Gantt

```
Week | Focus                                      | Status
-----|--------------------------------------------|--------
1–4  | P0–3                                       | ✅
5–6  | P4; hymn expand PARKED                     | ✅/⏸
7    | P5 APK + Web                               | ✅ 2026-07-17
7–8  | Signing, AAB, store, iOS                   | ⏳ NEXT
8+   | Release submit                             | ⏳
```

---

## References
- `docs/STATUS_REPORT_2026-07-17.md` — EOD detail  
- `docs/Task_Prioritized_Backlog_and_Schedule_2026-06-19.md` — task list  
- `docs/DEPLOY_CHECKLIST.md` — deploy + decisions  
- `CHANGELOG.md` — 1.0.0+1  
