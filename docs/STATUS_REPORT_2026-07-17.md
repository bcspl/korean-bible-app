# Korean Bible App — Status & Milestone Report (EOD)

**Date:** 2026-07-17 (end of day)  
**Method:** Code + builds + docs sync  
**Session:** Ceased — remaining work tracked below  

---

## 1. Health check

| Check | Result |
|--------|--------|
| `flutter test` | **5/5 passed** |
| `flutter analyze` | **0 errors** (19 info `prefer_const` only) |
| Hymns data | **104** PD hymns, sequential #1–104 |
| Branding | `assets/icon/icon.png` present |
| Android APK release | **✅ Built** `build/app/outputs/flutter-apk/app-release.apk` (**54.9 MB**, debug-signed) |
| Web release | **✅ Built** `build/web/` (PowerShell exit 1 was stderr noise only) |
| iOS | **⛔** Needs Mac + Xcode (not this PC) |
| Hymn expand / real scores | **⏸ PARKED** |

---

## 2. Progress snapshot

```
Overall  [█████████████████░░░] ~88%
Phase 0  100% ✅  Foundation
Phase 1  100% ✅  Data layer
Phase 2  100% ✅  Reading UI
Phase 3  100% ✅  Bookmarks, hymns, worship, nav, theme
Phase 4   95% ✅  UX polish; hymns frozen
Phase 5   40% ⏳  APK + Web built; signing/store/iOS remaining
```

### Coverage

| Capability | Status |
|------------|--------|
| Responsive | 12/13 screens |
| Semantics | 13/13 screens |
| Hymns | 104 PD + fav on 북마크; SVG educational scores |
| Widget tests | 5 green |
| Deploy artifacts | APK + web present |

---

## 3. Today’s completed work (2026-07-17)

- Hymn numbers reorganized 1…104; scores regenerated  
- Favorite hymns shown on **북마크** tab  
- Hymn expansion / full Korean score images **parked** (user decision)  
- Score options researched & documented (license / PD scan / engrave)  
- Phase 5 kickoff: `flutter doctor` clean; tests green  
- **Release APK** built (first-time NDK/SDK downloads)  
- **Web release** built  
- Display name → `한국어 성경`; web PWA manifest updated  
- `CHANGELOG.md`, `docs/DEPLOY_CHECKLIST.md`, `android/key.properties.example`  
- `.gitignore` for keystore / `key.properties`  
- Roadmap PPTX earlier in day + EOD regen  

---

## 4. Milestones

| ID | Milestone | Target | Status |
|----|-----------|--------|--------|
| **M1** | Phase 0–2 MVP | 2026-06-27 | ✅ Done |
| **M2** | Phase 3 features | 2026-07-04 | ✅ Done |
| **M3** | Phase 4 UX polish | 2026-07-20 | ✅ ~95% (hymn park OK) |
| **M4** | Phase 5 multi-platform builds | 2026-07-25 | ⏳ **~40%** — APK+Web done; AAB/signing/iOS open |
| **M5** | Store release package | 2026-08-05 | ⏳ Pending decisions + signing |

### Gantt

```
Week | Focus                                         | Status
-----|-----------------------------------------------|--------
1–4  | P0–3 data, UI, bookmarks, hymns, worship      | ✅
5–6  | P4 polish; hymns expand PARKED                | ✅/⏸
7    | P5 APK + Web builds                           | ✅ done today
7–8  | P5 keystore, AAB, store, iOS (Mac)            | ⏳ NEXT session
8+   | Store submit / release                        | ⏳
```

---

## 5. Remaining work (next session)

### Top 3 (need user decisions for store)
1. **User decisions:** package ID, ship targets, keystore, privacy URL, support email  
2. **Android production:** release keystore + `appbundle` (not debug-signed)  
3. **Store package:** listing, screenshots, privacy; device smoke-test of APK  

### Phase 5 remaining checklist
- [x] `flutter build apk --release` (debug-signed)  
- [x] `flutter build web --release`  
- [ ] Device install smoke-test of APK  
- [ ] Change `applicationId` from `com.example.*`  
- [ ] Create upload keystore + wire `key.properties`  
- [ ] `flutter build appbundle --release`  
- [ ] Host / deploy `build/web` (optional)  
- [ ] iOS on Mac  
- [ ] Store listing + screenshots + privacy policy  

### Parked (do not schedule)
- More hymns / real Korean score PNG / license path  

---

## 6. Artifacts

| Path | Note |
|------|------|
| `build/app/outputs/flutter-apk/app-release.apk` | 54.9 MB |
| `build/web/` | Static web build |
| `docs/DEPLOY_CHECKLIST.md` | Decisions + commands |
| `CHANGELOG.md` | 1.0.0+1 |
| Desktop `Roadmap_korean-bible-app_2026-07-17.pptx` | Roadmap skill |
| `docs/roadmap-pptx/Korean_Bible_App_Roadmap_및_작업제안_2026-07-17.pptx` | Git archive |

---

## 7. Risks

1. Play Store needs non-`com.example` ID + real signing.  
2. iOS blocked until Mac available.  
3. Educational SVG scores only — OK while hymn agenda parked.  

---

*EOD report — work ceased 2026-07-17*
