# Korean Bible App Project - 종합 현황 및 로드맵

**Verified status: 2026-08-10** (code + multi-version PD texts + tests + docs)  
**Previous checkpoint:** 2026-07-17 EOD  

## Executive summary

| Item | Value |
|------|--------|
| Overall progress | **~92%** |
| Phase 0–3 | **100% ✅** |
| Phase 4 | **~96% ✅** (PD multi-version + worship/hymns) |
| Phase 5 | **~40% ⏳** (APK + Web; signing/store open) |
| Bible versions | **KRV · KJV · ASV** (parallel, max 3) |
| Hymns (PD) | **102** + history/license + KO/EN |
| Responsive readings | **51** (시편·성탄·부활·이사야·누가) |
| Text QA | `verify_bible_texts.py` **PASS** |
| Tests | **5/5 passed** |
| Analyze | **0 errors** |
| APK / Web | Prior builds exist; rebuild after content change recommended |

```
전체: [██████████████████░░] ~92%
P0  ██████████ 100% ✅
P1  ██████████ 100% ✅
P2  ██████████ 100% ✅
P3  ██████████ 100% ✅
P4  █████████░  96% ✅
P5  ████░░░░░░  40% ⏳
```

---

## Verified completed work

### Phase 0–3 ✅
- Bible data/Hive, book/chapter/verse UI, search, OT/NT  
- Bookmarks; 5-tab nav; theme  
- Worship + hymns foundation  

### Phase 4 ✅ (~96%)
- Branding, responsive, Semantics  
- **2026-08-10:** Multi-version PD Bibles, verified KRV complete text, PD hymns rebuild, scripture-based 교독문, prayer-only Lord’s Prayer  

### Phase 5 partial
- Release APK / Web (2026-07-17)  
- Deploy checklist, CHANGELOG, key.properties.example  

### Content integrity (2026-08-10) ✅
- KRV: holybible PD complete (fixed incomplete OSIS)  
- KJV/ASV: open-bibles reparse match  
- Golden verses pass  

---

## Immediate Top 3 (next)

1. **User decisions** — package ID, ship target, keystore, privacy URL, support email  
2. **Android production signing** — keystore + AAB  
3. **UX polish** — remember version selection, verse copy/share, optional onboarding  

See `docs/DEPLOY_CHECKLIST.md`, `docs/PROJECT_REPORT_2026-08-10.md` §6–7.

### ⏸ PARKED
- Official Korean full-page hymn scores / large non-PD catalog  

### Phase 5 remaining
- [x] APK release (debug-signed)  
- [x] Web release  
- [ ] Device smoke-test (after rebuild with new assets)  
- [ ] applicationId ≠ `com.example.*`  
- [ ] Release keystore + appbundle  
- [ ] Web host (optional)  
- [ ] iOS (Mac)  
- [ ] Store listing / screenshots / privacy  

### Phase 6+ (future)
- Reading plans, last-position restore, highlights  
- TTS (optional)  
- Resume hymn score agenda when unparked  

---

## 현재 적용 vs 향후 계획 (사용성·가치)

**단일 기준 문서:** `docs/APPLIED_AND_ROADMAP_PLAN_2026-08-10.md`

| 구분 | 내용 |
|------|------|
| **적용됨** | KRV/KJV/ASV 병렬, 본문 검증 PASS, PD 찬송 102, 교독 51, 기도 본문만, 테스트 5/5 |
| **다음 Top3** | ① 스토어/서명 ② 역본 선택 저장+온보딩 ③ 절 복사/공유 + 기기 스모크 |
| **이후** | 위치 복원·통독·하이라이트·라이선스 화면 |
| **비권장** | 개역개정·비-PD 찬송·강제 계정 |

See also **`docs/PROJECT_REPORT_2026-08-10.md` §6**.  

---

## Related docs

- `docs/STATUS_REPORT_2026-08-10.md`  
- `docs/PROJECT_REPORT_2026-08-10.md`  
- `docs/STATUS_REPORT_2026-07-17.md` (historical)  
