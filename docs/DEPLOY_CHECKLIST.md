# Phase 5 — Deploy Checklist

**Updated:** 2026-08-10  
**App version:** `1.0.0+1` (`pubspec.yaml`) — bump before store submit after content release  

---

## Status snapshot

| Item | Status | Notes |
|------|--------|--------|
| `flutter test` | ✅ | 5/5 (2026-08-10) |
| `flutter analyze` | ✅ | 0 errors |
| Bible text verify | ✅ | `python scripts/verify_bible_texts.py` PASS |
| Content | ✅ | KRV+KJV+ASV · hymns 102 · readings 51 |
| Android release APK | ⚠️ | Prior 2026-07-17 build; **rebuild** after multi-version assets |
| Android App Bundle (Play) | ⏳ | Needs **release keystore** |
| Web release | ⚠️ | Rebuild `flutter build web --release` recommended |
| iOS archive | ⛔ | macOS + Xcode |
| Store listing | ⏳ | IDs + privacy + screenshots |
| Hymn official scores | ⏸ PARKED | |

### Store listing notes (content claims)

- Bible: **개역한글(KRV), KJV, ASV** — Public Domain; **not** 개역개정  
- Hymns/readings: PD only; not affiliated with 한국찬송가공회 official hymnal  
- Full description may mention offline multi-version parallel reading  

---

## Decisions needed from you

Reply with choices so we can finish release config:

1. **Application ID / package name**  
   Current: `com.example.korean_bible_app` (Play Store **rejects** `com.example.*` for production).  
   Suggest: `com.lsh.koreanbible` or your domain reverse DNS.  
   → **Your final ID?**

2. **Display name (home screen)**  
   Current Android label: `korean_bible_app`.  
   Suggest: `한국어 성경`.  
   → **Confirm or provide name.**

3. **Release signing (Android)**  
   Create a keystore once; never commit it.  
   → Prefer: (A) I generate a **template + commands** and you run keytool locally, or (B) you already have a keystore path?

4. **Stores to target first**  
   - [ ] Google Play only  
   - [ ] Sideload APK only (no store)  
   - [ ] Web host (Firebase / GitHub Pages / other)  
   - [ ] iOS later (Mac required)  

5. **Privacy policy URL** (required by Play/App Store)  
   Where will it live? (GitHub Pages, Notion, your site…)

6. **Contact email** for store listing / support.

---

## Android — local release (debug-signed, for device test)

```powershell
cd "C:\Users\LSH\Bible App\korean-bible-app"
flutter build apk --release
# Output: build\app\outputs\flutter-apk\app-release.apk
```

Install on device (USB debugging):

```powershell
flutter install --release
# or: adb install -r build\app\outputs\flutter-apk\app-release.apk
```

### Production signing (after you choose package ID)

1. Generate keystore (once):

```powershell
keytool -genkey -v -keystore C:\Users\LSH\secure\korean-bible-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

2. Copy `android/key.properties.example` → `android/key.properties` (gitignored) and fill passwords.

3. Wire `android/app/build.gradle.kts` release `signingConfig` (done when you confirm).

4. Build Play bundle:

```powershell
flutter build appbundle --release
# Output: build\app\outputs\bundle\release\app-release.aab
```

---

## Web

```powershell
flutter build web --release
# Output: build\web\
```

Host `build/web` on any static host. PWA bits: `web/manifest.json` + icons already present.

---

## iOS (Mac only)

```bash
flutter build ipa
# or open ios/Runner.xcworkspace in Xcode
```

Needs Apple Developer account + bundle ID (not `com.example.*`).

---

## Store listing draft (fill before submit)

| Field | Draft |
|-------|--------|
| Title | 한국어 성경 (오프라인) |
| Short description | 완전 오프라인 한국어 성경 · 찬송 · 예배자료 |
| Full description | 개역한글(KRV)·KJV·ASV 오프라인 병렬 열람, 북마크, Public Domain 찬송가, 사도신경·주기도문·교독문. 광고·계정 없음. 개역개정 미수록. |
| Category | Books & Reference / Lifestyle |
| Content rating | Everyone |
| Privacy | Offline-first; bookmarks/favorites on device; no account required (confirm analytics: currently none) |
| Screenshots | Phone: 성경 목록, 본문, 찬송, 북마크, 설정 (dark) |

---

## Do not do before decisions

- Do not upload `com.example.*` to Play Store  
- Do not commit keystore / `key.properties`  
- Do not scrape/add official 새찬송가 scores (hymn agenda parked)
