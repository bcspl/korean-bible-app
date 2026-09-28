# Android 출시 전체 프로세스 — 한국어 성경 (Google Play)

**작성일:** 2026-09-29  
**목표:** 2026-11 Google Play 1.0 공개  
**앱:** 한국어 성경 · `com.lsh.koreanbible` · Flutter  
**관련 문서:** [`PLAYSTORE_RELEASE_GUIDE_2026-08-10.md`](./PLAYSTORE_RELEASE_GUIDE_2026-08-10.md) (요약 가이드) · [`RELEASE_CHECKLIST_PLAYSTORE.md`](./RELEASE_CHECKLIST_PLAYSTORE.md) (R1–R25) · [`RESUME_HERE.md`](./RESUME_HERE.md) (재개 지점) · [`../privacy/privacy-policy.md`](../privacy/privacy-policy.md) (개인정보처리방침 초안)  
**PPTX:** `docs/roadmap-pptx/KoreanBible_Android_Release_Process_2026-09-29.pptx`

> 이 문서는 Phase 0–8 전 과정을 **실행 가능한 수준**으로 정리한 “정본(master)” 가이드입니다.  
> 상태 표기: ✅ 완료 · 🔄 진행 중 · ⏭ 다음 · ⛔ 사용자 결정/행동 필요 · ⏳ 대기

---

## 0. 한눈에 보기 (2026-09-29 기준)

| Phase | 내용 | 상태 |
|---|---|---|
| 0 | 사전 결정 (ID · 표시명 · 계정 · 이메일 · Privacy URL) | 🔄 ID ✅ / 이메일·계정·URL ⛔ |
| 1 | Play Console 계정 · 본인 인증 · 앱 생성 | ⛔ 사용자 (계정 미생성) |
| 2 | 앱 ID · 업로드 키 · 서명 | ✅ **완료 (R5, R7)** |
| 3 | 품질 게이트 · 빌드 (AAB) | ✅ AAB 빌드 (R8) · 실기기 ⏭ (R11) |
| 4 | 스토어 리스팅 자산 | ⏳ 아이콘만 있음 |
| 5 | 정책 · 개인정보 · Data safety · 등급 | 🔄 Privacy 초안 ✅ · 호스팅 ⛔ |
| 6 | 테스트 트랙 (내부 → **비공개 12명·14일**) | ⏳ Phase 1 이후 |
| 7 | 프로덕션 액세스 신청 · 심사 · 공개 | ⏳ |
| 8 | 운영 (업데이트 · 크래시 · 키 백업) | ⚠️ **키 백업 즉시 필요** |

### 오늘까지 끝난 것 (상세)

| 항목 | 값 |
|---|---|
| applicationId / namespace | `com.lsh.koreanbible` (이전 `com.example.korean_bible_app`) |
| MainActivity | `android/app/src/main/kotlin/com/lsh/koreanbible/MainActivity.kt` |
| 업로드 키스토어 | `C:\Users\LSH\secure\korean-bible-upload.jks` (PKCS12 · RSA 2048 · 유효 ~2054-02-14) |
| 키 alias | `upload` |
| 인증서 소유자 | `CN=LSH, O=personal, C=KR` |
| SHA-1 | `AA:71:3A:D2:54:66:1C:37:1C:3B:18:D6:60:57:65:F6:54:39:9F:A7` |
| SHA-256 | `41:9D:AA:1C:6E:72:33:EB:FC:32:9B:7B:C4:B5:FD:FE:2E:74:94:C2:69:B8:7D:42:19:57:AC:AE:94:6E:33:87` |
| 비밀번호 위치 (값은 문서에 절대 기록 안 함) | `android\key.properties` (gitignore) · `C:\Users\LSH\secure\korean-bible-key.properties.backup.txt` |
| 서명 설정 | `android/app/build.gradle.kts` — `key.properties` 있으면 release 키, 없으면 debug 서명 fallback |
| 서명 AAB | `build\app\outputs\bundle\release\app-release.aab` — 59,709,077 bytes (~56.9 MB), 업로드 키 지문 일치 확인 |
| 스모크 APK | `build\app\outputs\flutter-apk\app-release.apk` — ~58.1 MB (R5 시점, debug 서명) |
| 버전 | `1.0.0+1` (versionName 1.0.0 · versionCode 1) |
| SDK | minSdk 24 · targetSdk 36 · compileSdk 36 |
| 툴체인 | Flutter 3.44.4 (`C:\Users\LSH\flutter`) · AGP 9.0.1 · Gradle 9.1.0 · Kotlin 2.3.20 · JDK = Android Studio jbr 21 (`C:\Program Files\Android\Android Studio\jbr`) |
| 커밋 (GitHub push 완료) | `c89d4e8` 문서 체크포인트 · `b091778` applicationId (R5) · `6e10341` 문서 · `fcdf025` release 서명 (R7) · `fae983b` 문서 (R7/R8) |

### ⛔ 사용자가 해야 할 일 (차단 항목)

1. **Play Console 개발자 계정 생성** ($25 · 신분증 · 기기 인증) — 가장 오래 걸리는 경로(critical path)
2. **지원 이메일** 결정 (스토어 공개 · 개인정보처리방침에 기재)
3. **개인정보처리방침 게시** — GitHub Pages 활성화 (설정 방법: `docs/privacy/README.md`)
4. **키스토어 + 비밀번호 PC 밖 백업** (USB/암호관리자)
5. 비공개 테스트 **테스터 12명 이상** 모집 (가족·교회·지인 Gmail)

### ⏱ 11월 공개를 위한 역산 일정

비공개 테스트 **14일 연속** + 프로덕션 액세스 심사(보통 7일 이내) + 앱 심사(수일)가 필요합니다.

| 목표일 | 할 일 |
|---|---|
| ~10/05 | Play Console 계정 가입 · 본인 인증 시작 · 이메일 확정 · Privacy URL 게시 |
| ~10/10 | 앱 생성 · 앱 콘텐츠(정책) 작성 · 내부 테스트 AAB 업로드 |
| **~10/14** | **비공개 테스트 시작 (12명+ opt-in)** — 늦어질수록 공개일이 밀림 |
| ~10/28 | 14일 충족 → 프로덕션 액세스 신청 |
| ~11/04 | 액세스 승인 → 프로덕션 출시 제출 |
| 11월 중 | 심사 통과 · 1.0 공개 |

---

## Phase 0 — 사전 결정

| 결정 | 값 / 상태 |
|---|---|
| Application ID (평생 고정, 변경 불가) | ✅ `com.lsh.koreanbible` |
| 앱 표시명 | 🔄 `한국어 성경` (AndroidManifest `android:label` 적용됨 · 스토어 앱 이름 최대 30자) |
| 개발자 계정 유형 | ⛔ **개인(Personal)** 권장 — 조직 계정은 D-U-N-S 필요 |
| 지원 이메일 | ⛔ `[지원 이메일]` |
| 개인정보처리방침 URL | ⛔ 예정: `https://bcspl.github.io/korean-bible-app/privacy/` |
| 출시 방식 | 내부 테스트 → 비공개 테스트(필수) → 프로덕션 |
| 가격 | 무료 (한 번 무료로 게시하면 유료 전환 불가) |
| 광고 | 없음 |

---

## Phase 1 — Play Console 계정 · 본인 인증 · 앱 생성 (⛔ 사용자)

### 1-1. 계정 가입

1. https://play.google.com/console 접속 → 사용할 Google 계정으로 로그인 (장기 사용할 계정 선택)
2. **계정 유형: 개인(Personal)** 선택
3. **등록비 US$25 (1회)** 신용/체크카드 결제
4. 개발자 이름(스토어에 공개됨), 연락처 이메일·전화 입력

### 1-2. 본인 인증 (개인 계정)

- Google 결제 프로필에 **법적 이름·주소**가 신분증과 **정확히 일치**해야 함
- **정부 발급 신분증** 제출 (여권 · 운전면허 · 주민등록증 등)
- **실제 Android 기기 인증**: 신규 개인 계정은 Play Console 모바일 앱으로 Android 기기(비루팅) 접근을 인증해야 앱 공개 가능
- 인증 처리 기간은 고정되어 있지 않음 → **가장 먼저 시작**

### 1-3. 앱 만들기

Play Console → **앱 만들기**

| 항목 | 입력 |
|---|---|
| 앱 이름 | 한국어 성경 |
| 기본 언어 | 한국어 – ko-KR |
| 앱 또는 게임 | 앱 |
| 무료 또는 유료 | 무료 |
| 선언 | 개발자 프로그램 정책 · 미국 수출법 동의 |

### 1-4. 신규 개인 계정 테스트 요건 (중요)

> **2023-11-13 이후 생성된 개인 개발자 계정은, 프로덕션 공개 전에 비공개 테스트(Closed testing)에 최소 12명의 테스터가 14일 연속 opt-in 되어 있어야** 프로덕션 액세스를 신청할 수 있습니다.  
> - 내부 테스트(Internal)는 **카운트되지 않음**  
> - 테스터가 중간에 opt-out 하면 연속 14일이 끊김 → 15명 이상 여유 있게 모집 권장  
> - 요건 충족 후 대시보드에서 **프로덕션 액세스 신청** (테스트·앱·준비 상태 질문에 답변). 심사는 보통 7일 이내  
> 출처: Play Console 고객센터 https://support.google.com/googleplay/android-developer/answer/14151465 (2026-09-29 확인)

---

## Phase 2 — 앱 ID · 서명 (✅ 완료)

### 2-1. applicationId 변경 ✅ (R5 · `b091778`)

```kotlin
// android/app/build.gradle.kts
android {
    namespace = "com.lsh.koreanbible"
    defaultConfig {
        applicationId = "com.lsh.koreanbible"
    }
}
```

- `MainActivity.kt` → `android/app/src/main/kotlin/com/lsh/koreanbible/`, `package com.lsh.koreanbible`
- iOS/macOS/Linux/Windows 번들 ID는 아직 `com.example.*` (Android 출시와 무관 · iOS 출시 시 변경)
- ⚠️ PowerShell 5 `Set-Content -Encoding UTF8`은 **BOM**을 붙여 Gradle 스크립트 컴파일을 깨뜨림 → 항상 `[IO.File]::WriteAllText(path, text, (New-Object Text.UTF8Encoding $false))` 사용

### 2-2. 업로드 키스토어 생성 ✅ (R7 · 2026-09-29)

실제 실행한 방식 (비밀번호는 무작위 24자, 출력하지 않음, store=key 동일 — PKCS12 요구):

```powershell
$kt = "C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe"
mkdir C:\Users\LSH\secure -Force
& $kt -genkeypair -v `
  -keystore C:\Users\LSH\secure\korean-bible-upload.jks `
  -storetype PKCS12 -keyalg RSA -keysize 2048 -validity 10000 `
  -alias upload -dname "CN=LSH, O=personal, C=KR" `
  -storepass <비밀번호> -keypass <비밀번호>
```

`android/key.properties` (gitignore, **절대 커밋 금지**, BOM 없이 저장):

```properties
storePassword=<비밀번호>
keyPassword=<비밀번호>
keyAlias=upload
storeFile=C:/Users/LSH/secure/korean-bible-upload.jks
```

템플릿: `android/key.properties.example` (자리표시자만 · 커밋됨)

지문 확인:

```powershell
& $kt -list -v -keystore C:\Users\LSH\secure\korean-bible-upload.jks
# 비밀번호 입력 프롬프트 → Alias name: upload / SHA1 / SHA256 확인
```

### 2-3. Gradle release 서명 ✅ (`fcdf025`)

```kotlin
import java.io.FileInputStream
import java.util.Properties

val keystorePropertiesFile = rootProject.file("key.properties")
val keystoreProperties = Properties()
val hasReleaseKeystore = keystorePropertiesFile.exists()
if (hasReleaseKeystore) {
    FileInputStream(keystorePropertiesFile).use { keystoreProperties.load(it) }
}

android {
    signingConfigs {
        if (hasReleaseKeystore) {
            create("release") {
                keyAlias = keystoreProperties.getProperty("keyAlias")
                keyPassword = keystoreProperties.getProperty("keyPassword")
                storeFile = file(keystoreProperties.getProperty("storeFile"))
                storePassword = keystoreProperties.getProperty("storePassword")
            }
        }
    }
    buildTypes {
        release {
            signingConfig = if (hasReleaseKeystore) signingConfigs.getByName("release")
                            else signingConfigs.getByName("debug")
        }
    }
}
```

### 2-4. Play App Signing (앱 생성 후 · ⏭)

- 신규 앱은 **Play App Signing**이 기본 · AAB 업로드 필수
- 우리가 가진 키 = **업로드 키** · 실제 사용자 기기용 **앱 서명 키는 Google이 보관**
- 첫 AAB 업로드 시 Play Console → **테스트 및 출시 → 설정 → 앱 무결성 → 앱 서명**에서 “Google에서 생성한 키 사용”(권장) 유지
- 업로드 키 분실 시: Play Console에서 **업로드 키 재설정** 요청 가능 (앱 서명 키는 Google 보관이라 앱 자체는 유지)
- 업로드 키 인증서 SHA-1/SHA-256이 위 표와 일치하는지 앱 무결성 화면에서 확인

---

## Phase 3 — 품질 게이트 · 빌드

### 3-1. 버전 올리기 (매 업로드마다)

`pubspec.yaml`:

```yaml
version: 1.0.0+1   # versionName+versionCode
```

- **versionCode(+N)는 업로드할 때마다 반드시 증가** (같은 번호 재업로드 불가)
- 예: 첫 내부 테스트 `1.0.0+1` → 수정본 `1.0.0+2` → 프로덕션 `1.0.0+3` → 업데이트 `1.0.1+4`
- ⚠️ `lib/screens/about_screen.dart`, `settings_screen.dart`에 버전 문자열(`1.0.0+1`)이 하드코딩되어 있음 → 버전 변경 시 같이 수정 (또는 추후 `package_info_plus` 도입 검토)

### 3-2. 품질 게이트 명령

```powershell
[Console]::OutputEncoding=[Text.Encoding]::UTF8
cd "C:\Users\LSH\Bible App\korean-bible-app"
flutter pub get
flutter test
python scripts\verify_bible_texts.py
flutter analyze            # 현재 info 19건 (about_screen const) — 오류/경고 0
```

### 3-3. 빌드

```powershell
flutter build appbundle --release
# → build\app\outputs\bundle\release\app-release.aab   (Play 업로드용)

flutter build apk --release
# → build\app\outputs\flutter-apk\app-release.apk      (실기기 설치용)
```

서명 검증:

```powershell
$jbr = "C:\Program Files\Android\Android Studio\jbr\bin"
& "$jbr\jarsigner.exe" -verify -verbose -certs build\app\outputs\bundle\release\app-release.aab
# AAB의 META-INF/UPLOAD.RSA 인증서 SHA-256 = 업로드 키 SHA-256 인지 확인
```

### 3-4. 실기기 테스트 (R11 · ⏭ 다음)

```powershell
$adb = "$env:LOCALAPPDATA\Android\sdk\platform-tools\adb.exe"
& $adb devices
& $adb install -r build\app\outputs\flutter-apk\app-release.apk
```

체크리스트: 비행기 모드 전 기능 · 다크모드 · 큰 글씨 · 고대비 · 성경(병렬 3역본)/찬송/교독/예배/북마크/설정 · 첫 실행 로딩 시간 · 앱 재시작 후 설정 유지

> 참고: 기존 `com.example.korean_bible_app` 설치본과는 **다른 앱**으로 인식됨 (나란히 설치됨). 이전 앱은 수동 삭제.

---

## Phase 4 — 스토어 리스팅 자산

| 자산 | 요구 사항 | 상태 |
|---|---|---|
| 앱 이름 | ≤ 30자 · `한국어 성경` | 🔄 |
| 간단한 설명 | ≤ 80자 | ⏳ 초안: `완전 오프라인 한국어 성경 · 찬송 · 예배자료 (광고·계정 없음)` |
| 자세한 설명 | ≤ 4000자 · PD · KRV/KJV/ASV · **개역개정 미수록** 명시 | ⏳ |
| 앱 아이콘 | **512×512 · 32-bit PNG(알파) · ≤1MB** | 🔄 `assets/icon/icon.png` 기반으로 내보내기 |
| 피처 그래픽 | **1024×500 · JPEG 또는 24-bit PNG(알파 없음)** · 필수 | ⏳ |
| 휴대전화 스크린샷 | **2–8장** · JPEG/24-bit PNG · 변 320–3840px · 긴 변 ≤ 짧은 변×2 · 권장 1080×1920 | ⏳ 성경·병렬·찬송·교독·설정 |
| 태블릿 스크린샷 | 선택 (태블릿 지원 시 권장) | ⏳ |
| 카테고리 | 도서/참고자료 (Books & Reference) | ⏳ |
| 연락처 | 이메일 필수 · 웹사이트 선택 | ⛔ |

출처: https://support.google.com/googleplay/android-developer/answer/9866151

스크린샷 촬영 (실기기/에뮬레이터):

```powershell
& $adb shell screencap -p /sdcard/s1.png
& $adb pull /sdcard/s1.png docs\store\screenshots\s1.png
```

---

## Phase 5 — 정책 · 개인정보 · 앱 콘텐츠

Play Console → **정책 → 앱 콘텐츠**에서 모두 작성해야 출시 가능.

### 5-1. 개인정보처리방침 (R2)

- 초안: `docs/privacy/privacy-policy.md` (한/영) · 웹 페이지: `docs/privacy/index.html` ✅
- 코드 조사 결과 (2026-09-29):
  - release 매니페스트에 **INTERNET 권한 없음** (debug/profile에만 존재) → 외부 전송 불가
  - 광고·분석·크래시 SDK **없음** (의존성: hive, shared_preferences, path_provider, provider, flutter_svg, flutter_native_splash)
  - 기기 내 저장만: SharedPreferences(다크모드·글꼴배율·고대비), Hive(북마크: 책/장/절·미리보기·생성시각, 찬송 즐겨찾기 번호, 성경 본문 캐시)
  - 위험 권한 없음 · 계정 없음
  - `android:allowBackup` 미설정 → Android 자동 백업(사용자 Google 계정) 대상일 수 있음 → 방침에 명시함
- 게시: GitHub Pages → `https://bcspl.github.io/korean-bible-app/privacy/` (절차: `docs/privacy/README.md`) ⛔
- **Play 정책: 모든 앱은 Play Console에 개인정보처리방침 링크 + 앱 내부에도 링크 또는 텍스트 필요** (데이터 미수집 앱 포함)  
  → ⏭ 앱 설정/정보 화면에 “개인정보처리방침” 항목(텍스트) 추가 필요 (B4 라이선스 화면과 함께)  
  출처: https://support.google.com/googleplay/android-developer/answer/10144311

### 5-2. 데이터 보안(Data safety) 양식

데이터를 수집하지 않는 앱도 **반드시 작성** + 개인정보처리방침 링크 필요.  
출처: https://support.google.com/googleplay/android-developer/answer/10787469

예상 답변:

| 질문 | 답 |
|---|---|
| 필수 사용자 데이터 유형을 수집 또는 공유하나요? | **아니요** (기기 밖으로 전송하지 않음 — Google 정의상 “수집” 아님) |
| 전송 중 암호화 | 해당 없음 (전송 없음) |
| 계정 생성 | 없음 → 계정 삭제 URL 불필요 |
| 데이터 삭제 요청 | 앱 삭제/앱 데이터 삭제로 즉시 삭제 |

### 5-3. 기타 앱 콘텐츠 선언

| 항목 | 답 |
|---|---|
| 광고 포함 여부 | **아니요** |
| 앱 액세스 권한 | 모든 기능 로그인 없이 사용 가능 |
| 콘텐츠 등급 (IARC 설문) | 폭력·성·도박 등 없음 → 전체이용가 / Everyone 예상 |
| 타겟층 및 콘텐츠 | **13세 이상** 연령대 선택 권장 (13세 미만 포함 시 가족 정책 추가 요건 적용). 전 연령 이용은 가능 |
| 뉴스 앱 | 아니요 |
| 정부 앱 | 아니요 |
| 금융 기능 / 건강 | 없음 |
| 데이터 보안 | 위 5-2 |

### 5-4. 타겟 API 수준 (확인됨)

- **2026-08-31부터 신규 앱·업데이트는 Android 16 (API 36) 이상 타겟 필수** (연장 요청 시 2026-11-01까지)
- 현재 `targetSdk = flutter.targetSdkVersion` = **36** ✅ (aapt로 확인: targetSdkVersion 36)
- 출처: https://support.google.com/googleplay/android-developer/answer/11926878

### 5-5. 콘텐츠 고지

- 한국찬송가 공식 악보/가사 아님 · PD 전용 (앱 내 반영됨 ✅ R4)
- 개역개정 미수록 (스토어 설명에 명시)

---

## Phase 6 — 테스트 트랙

| 트랙 | 목적 | 인원 | 비고 |
|---|---|---|---|
| 내부 테스트 | 업로드·설치 즉시 확인 | ≤100 | 프로덕션 요건에 **카운트 안 됨** |
| **비공개 테스트** | 신규 개인 계정 필수 | **≥12명 · 14일 연속 opt-in** | Google 그룹 또는 이메일 목록 |
| 공개 테스트 | 선택 | 제한 없음 | |
| 프로덕션 | 일반 공개 | | 액세스 승인 후 |

절차:

1. **테스트 및 출시 → 테스트 → 내부 테스트 → 새 버전 만들기** → `app-release.aab` 업로드 → 출시 노트(ko-KR) → 검토 및 출시
2. 테스터 이메일 목록 추가 → 참여 링크 공유 → 설치 확인
3. **비공개 테스트 → 트랙 만들기** → 같은(또는 versionCode 증가) AAB → 국가: 대한민국 → 테스터 목록(15명+ 권장) → 출시
4. 테스터에게: 링크에서 **“테스터 되기(opt-in)”** 누르고 **14일간 유지**, 실제로 앱 사용·피드백 요청
5. 피드백 반영 버전 업로드 시 versionCode 증가

출시 노트 예:

```
<ko-KR>
첫 테스트 버전입니다.
- 개역한글·KJV·ASV 병렬 성경 (완전 오프라인)
- 공개 도메인 찬송 102곡 · 교독문 51편 · 사도신경/주기도문
</ko-KR>
```

---

## Phase 7 — 프로덕션 액세스 · 심사 · 공개

1. 비공개 테스트 요건 충족(12명·14일) → 대시보드 **프로덕션 액세스 신청**
2. 질문 답변: 테스터 모집 방법, 받은 피드백, 개선 사항, 출시 준비 상태 → 구체적으로 작성
3. 승인(보통 7일 이내) 후 **프로덕션 → 새 버전 만들기** → AAB → 국가/지역 → 출시 제출
4. 앱 심사 (수일, 신규 계정은 더 길 수 있음)
5. 반려 시: 사유(정책/메타데이터/권한) 수정 → versionCode 올려 재제출

---

## Phase 8 — 운영

### 8-1. 업데이트

```powershell
# 1) pubspec.yaml version 올리기 (예: 1.0.1+5)
# 2) 품질 게이트
flutter test; flutter analyze; python scripts\verify_bible_texts.py
# 3) 빌드
flutter build appbundle --release
# 4) Play Console: 프로덕션(또는 테스트) → 새 버전 → AAB 업로드 → 출시 노트 → 단계적 출시(예: 20%)
```

### 8-2. 모니터링

- **Android Vitals**: 비정상 종료율 · ANR · 시작 시간
- 리뷰·평점 응답 (Play Console → 평점 및 리뷰)
- 매년 8월 말 타겟 API 상향 요구 확인 (2027년 예상: API 37)

### 8-3. ⚠️ 키 백업 (즉시)

| 백업 대상 | 위치 |
|---|---|
| 키스토어 | `C:\Users\LSH\secure\korean-bible-upload.jks` |
| 비밀번호 | `C:\Users\LSH\secure\korean-bible-key.properties.backup.txt` · `android\key.properties` |

- 현재 **이 PC 한 곳에만** 존재 → PC 고장/분실 시 업로드 불가
- 권장: 암호화 USB 1개 + 암호관리자(비밀번호) · 클라우드 업로드 시 반드시 암호화
- 업로드 키 분실 시 Play App Signing 덕분에 **업로드 키 재설정** 가능하지만 Google 지원 요청·대기 필요
- 절대 git/Drive 공개 폴더/메일에 평문으로 올리지 말 것

---

## 부록 A. 체크리스트 매핑 (R1–R25)

| Phase | 체크리스트 |
|---|---|
| 0–1 | R21 (이메일·계정) |
| 2 | ✅ R5 · ✅ R7 · 🔄 R6 |
| 3 | ✅ R8 · R9 ✅(API 36) · R10 · R11 · R12–R17 |
| 4 | R18–R20 |
| 5 | R1–R4 (R2 초안 ✅) |
| 사전 UX | R22–R25 (+ 앱 내 개인정보처리방침 텍스트) |

## 부록 B. 확인한 정책 출처 (2026-09-29)

| 사실 | 출처 |
|---|---|
| 신규 개인 계정: 비공개 테스트 12명 · 14일 연속 | https://support.google.com/googleplay/android-developer/answer/14151465 |
| 등록비 US$25 · 본인 인증 · 기기 인증 | https://support.google.com/googleplay/android-developer/answer/6112435 |
| 타겟 API 36 (2026-08-31~, 연장 11-01) | https://support.google.com/googleplay/android-developer/answer/11926878 |
| Data safety: 미수집 앱도 작성 + 방침 링크 | https://support.google.com/googleplay/android-developer/answer/10787469 |
| 개인정보처리방침: Console + 앱 내 링크/텍스트 | https://support.google.com/googleplay/android-developer/answer/10144311 |
| 그래픽 자산 규격 | https://support.google.com/googleplay/android-developer/answer/9866151 |

*정책은 수시로 바뀝니다. 각 Phase 착수 시 출처 링크를 다시 확인하세요.*
