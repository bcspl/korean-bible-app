# Android 개발자 인증(Android developer verification) 대비 — 한국어 성경

**작성:** 2026-10-03 (KST) · **대상:** `com.lsh.koreanbible` (원스토어 심사 제출, versionCode 1)  
**관련:** [`ANDROID_RELEASE_PROCESS.md`](./ANDROID_RELEASE_PROCESS.md) (Google Play) · [`ONESTORE_RELEASE_GUIDE.md`](./ONESTORE_RELEASE_GUIDE.md) · [`RESUME_HERE.md`](./RESUME_HERE.md)

> 표기: **[공식]** = Google/원스토어 공식 문서 · **[추론]** = 공식 문서를 바탕으로 한 판단 · **[미정]** = 아직 공개되지 않음.
> 모든 출처는 2026-10-03에 확인했습니다.

---

## 1. 이게 뭔가

- **[공식]** 인증된(certified) Android 기기에 앱을 설치하려면, 앱이 **신원 인증을 마친 개발자에게 등록(package name + 서명 키)** 되어 있어야 하는 제도입니다. Play 밖에서 배포하는 앱(원스토어, 웹 APK, 사이드로드)도 대상입니다.
- 개발자가 할 일 (출처: https://developer.android.com/developer-verification/guides)
  1. 콘솔 계정 만들기 (Play 밖에서만 배포하면 Android Developer Console, Play 사용자는 Play Console)
  2. 신원 인증
  3. 패키지 이름 등록 (내 개인 키로 서명한 APK로 소유권 증명)
- **[공식]** Android 7 이상 인증 기기에 적용됩니다. 업데이트는 Google Play 서비스로 배포됩니다 (FAQ).
- **[공식]** 등록되지 않은 앱도 **ADB 설치**는 지금처럼 가능합니다. 일반 사용자는 **고급 흐름(advanced flow)** 으로만 설치할 수 있습니다: 개발자 모드 켜기 → 강요받고 있지 않은지 확인 → 재부팅 → **24시간 대기** → 생체/PIN 인증 → "Install Anyway". 고급 흐름이 꺼져 있으면 미등록 앱의 **업데이트도 실패**합니다 (FAQ).

## 2. 일정

| 시점 | 내용 | 근거 |
|------|------|------|
| 2026-03 | 인증 기능 출시 (Play·Android Developer Console) | [공식] 블로그 2026-06-18 |
| 2026-08 | 개발자 API, 제한 배포 계정, 고급 흐름 출시 | [공식] developer-verification 타임라인 |
| **2026-09-30** | **브라질·인도네시아·싱가포르·태국**에서만 시행. 대상은 참여 스토어 7곳(Google Play, HONOR, OPPO, Samsung Galaxy Store, Transsion, vivo, Xiaomi GetApps)에서의 설치 | [공식] guides · 블로그 |
| **2027년** | 전 세계 확대, 인증 기기의 **모든 앱** 대상. "곧 모든 서드파티 앱스토어로 확대" | [공식] |
| 한국 시행일 | **[미정]** — 2027년이라는 것만 공개, 날짜·월 미발표 | — |

- **[공식]** 목록에 없는 스토어(원스토어 포함)와 사이드로드는 현재 시행 대상이 아닙니다. 다만 Google은 2027년 확대 전에 인증을 마쳐 두라고 권고합니다 (FAQ 2026-06-18, 2026-07-15 항목).
- **[추론]** 원스토어는 초기 7개 스토어 목록에 없습니다. 따라서 **현재 한국 원스토어 사용자에게는 영향이 없습니다.**

## 3. 이 앱에 미치는 영향

| 항목 | 현재 (2026-10) | 2027 한국 시행 후, 미등록이면 |
|------|----------------|------------------------------|
| 원스토어 신규 설치 | 영향 없음 | 일반 사용자 설치 차단. 고급 흐름(24시간 대기) 사용자만 설치 가능 **[추론]** |
| 기존 사용자 업데이트 | 영향 없음 | 업데이트 실패 가능 (FAQ: 미등록 앱 업데이트는 고급 흐름/ADB만) |
| 개발 중 ADB 설치 | 영향 없음 | 영향 없음 |
| 원스토어 바이너리 등록 | `adi-registration.properties`가 없으면 **안내 팝업만** 표시. 등록·심사·출시에는 영향 없음 [공식 원스토어 FAQ] | — |

→ **결론:** 지금 급하지는 않지만, 한국 시행 전에 **신원 인증 + `com.lsh.koreanbible` 등록**을 반드시 끝내야 합니다.

## 4. 두 가지 경로

| | **A. Google Play Console** | **B. Android Developer Console (ADC) · 전체 배포** | (참고) ADC 제한 배포 |
|---|---|---|---|
| 대상 | Play + Play 밖 모두 배포 | Play 밖에서**만** 배포 | 학생·취미, 기기 20대까지 |
| 비용 | Play 등록비 US$25 (기존 계획대로) | **US$25** (결제 수단 상세는 콘솔에서 안내) | 무료 |
| 신원 | Play 계정 인증으로 충족 (추가 조치 거의 없음) | 정부 발급 **사진 신분증 + 주소 증빙**, 이메일·전화 OTP, Google 결제 프로필(법적 이름·주소) | 신분증 불필요 (2단계 인증 + 결제 프로필) |
| 패키지 등록 | Play에 만든 앱은 **자동 등록**. Play App Signing 앱은 자동 소유권 인정. Play 밖 키는 Play Console에서 추가 등록 | 콘솔 Package names 메뉴에서 직접 등록 | 등록 가능하지만 배포는 승인된 20대까지 |
| 이 앱에 적합? | ✅ Play 출시를 할 경우 | ✅ Play를 안 할 경우 | ❌ 스토어 배포 불가 |

- **[공식]** 제한 배포 계정은 나중에 전체 배포로 전환할 수 있지만, 반대 방향은 안 됩니다 (FAQ).
- **[공식]** 전체 배포 신원 인증은 서류가 준비되어 있으면 "보통 약 10분"이 걸립니다 (full-distribution 가이드). 공식 예시 서류는 미국 기준(여권, 운전면허, 공과금 고지서, 카드/은행 명세서 등)입니다. **한국에서 받는 서류 목록은 [미정]**입니다. 여권이나 운전면허증 + 영문/국문 주소 증빙(공과금·은행 명세서)을 준비하세요 **[추론]**.

### 권장
1. **Google Play 출시를 진행하면 (현재 계획: 2026-11 목표) → 경로 A.** Play Console 하나로 Play와 원스토어 배포를 모두 관리합니다 ([공식] FAQ: Play 계정이 있으면 Play 밖 앱도 Play Console에서 관리). 등록비 이중 지출도 없습니다.
2. **Play를 하지 않거나 무기한 미루면 → 경로 B (ADC 전체 배포, $25).**
3. 제한 배포 계정은 사용하지 않습니다.

## 5. 서명 키 관점 (이 앱의 상황)

| 항목 | 값 |
|------|----|
| 패키지 | `com.lsh.koreanbible` |
| 업로드/서명 키 | `C:\Users\LSH\secure\korean-bible-upload.jks` (PKCS12), alias `upload`, `CN=LSH, O=personal, C=KR` |
| SHA-256 | `41:9D:AA:1C:6E:72:33:EB:FC:32:9B:7B:C4:B5:FD:FE:2E:74:94:C2:69:B8:7D:42:19:57:AC:AE:94:6E:33:87` |
| 공개 인증서 (PEM) | `C:\Users\LSH\secure\korean-bible-upload-cert.pem` (2026-10-03 생성. 비밀 아님, SHA-256 일치 확인) |

- **원스토어:** 가이드는 "앱 서명 사용 안함"(직접 서명 APK)을 권장했습니다. 이 경우 원스토어 사용자 기기의 서명은 위 키입니다. 그러면 **우리가 직접 서명한 APK로 소유권을 증명할 수 있습니다.**
  - ⚠ **제출 시 실제로 고른 서명 옵션을 확인하세요.** 원스토어 서명 키를 골랐다면, 원스토어 FAQ 절차를 따라야 합니다: 스니펫을 넣어 빌드 → 원스토어 등록 → **원스토어가 서명한 최종 APK**를 내려받아 Google 콘솔에 업로드. 직접 서명한 APK로는 소유권 인증이 안 될 수 있습니다 ([공식] https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification).
- **Google Play (경로 A):**
  - Play App Signing에 **Google 생성 키**를 쓰면: Play가 Google 키로 패키지를 자동 등록합니다. 원스토어용 업로드 키는 **추가 키로 소유권 증명**을 해야 합니다. 한 패키지에 키 여러 개 등록 가능 [공식 FAQ].
  - **PEPK로 기존 키를 등록**하면: Play와 원스토어가 같은 키를 씁니다. 등록 키 1개, 스토어 간 업데이트 호환 → **권장** (원스토어 가이드 결정사항과 같음).
- **신규 vs 기존 패키지 [공식 ADC 도움말]:** 설치 이력이 없는 "새" 패키지는 **공개 인증서만** 내면 됩니다. 설치 이력이 있는 "기존" 패키지는 **스니펫을 넣은 서명 APK 업로드**가 필요합니다. 원스토어 출시 후에는 "기존"으로 취급될 가능성이 높습니다 **[추론]**. 이 경우 7단계의 APK 업로드 절차를 따릅니다.
- **키 분실 = 등록 불가** [공식 FAQ]. 키스토어와 비밀번호를 PC 밖 두 곳에 백업하세요 (미완료 항목).
- **패키지 충돌 규칙** [공식]: 같은 패키지명을 여러 키가 쓰면 설치 50% 초과 키가 우선합니다. 그다음은 50설치 이상 키, 그다음은 선착순입니다. `com.lsh.koreanbible`은 우리만 쓰므로 문제없을 것으로 예상합니다 **[추론]**.

## 6. 지문·공개 인증서 확인 방법 (비밀번호를 출력하지 않는 방법)

```powershell
$jbr = "C:\Program Files\Android\Android Studio\jbr\bin"
$bt  = "$env:LOCALAPPDATA\Android\sdk\build-tools\37.0.0"
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
cd "C:\Users\LSH\Bible App\korean-bible-app"

# (1) 서명된 APK에서 지문 확인 — 비밀번호 불필요
& "$bt\apksigner.bat" verify --print-certs build\app\outputs\flutter-apk\app-release.apk

# (2) 서명된 APK에서 공개 인증서(PEM) 추출 — 비밀번호 불필요
& "$bt\apksigner.bat" verify --print-certs-pem build\app\outputs\flutter-apk\app-release.apk
#   → -----BEGIN CERTIFICATE----- ~ -----END CERTIFICATE----- 부분을 .pem으로 저장
#   (이미 저장됨: C:\Users\LSH\secure\korean-bible-upload-cert.pem)

# (3) PEM 파일 지문 확인 — 비밀번호 불필요
& "$jbr\keytool.exe" -printcert -file C:\Users\LSH\secure\korean-bible-upload-cert.pem

# (4) 키스토어에서 직접 — keytool이 비밀번호를 '대화형으로' 물어봄 (명령줄에 -storepass 쓰지 말 것)
& "$jbr\keytool.exe" -list -v -keystore C:\Users\LSH\secure\korean-bible-upload.jks -alias upload
& "$jbr\keytool.exe" -exportcert -rfc -keystore C:\Users\LSH\secure\korean-bible-upload.jks -alias upload -file upload-cert.pem
```
- 참고: 이 APK는 v2 서명만 있어서 `keytool -printcert -jarfile`로는 인증서가 나오지 않습니다. 위 (1)·(2)처럼 `apksigner`를 쓰세요.
- 콘솔에는 **SHA-256 지문** 또는 **공개 인증서**만 입력합니다. `.jks` 파일과 비밀번호는 절대 업로드하거나 공유하지 마세요.

## 7. 단계별 실행 (실행 시점: 8절)

| # | 단계 | 담당 | 준비물 |
|---|------|------|--------|
| 1 | 경로 결정: Play 진행 → A / 미진행 → B | 사용자 | — |
| 2 | 계정 만들기 (A: Play Console 개인 계정 / B: ADC 전체 배포, $25) | 사용자 · 브라우저 | Google 계정(2단계 인증), 결제 카드, Google 결제 프로필(법적 이름·주소) |
| 3 | 신원 인증 | 사용자 | 사진 신분증(여권/운전면허), 주소 증빙, 이메일·휴대폰 OTP |
| 4 | 패키지 등록 시작: `com.lsh.koreanbible` 입력, 표시명 "한국어 성경" | 사용자 | — |
| 5 | 키 추가: 목록에서 SHA-256 `41:9D…33:87` 선택. 새 패키지라면 공개 인증서 입력 | 사용자 | `korean-bible-upload-cert.pem` / 위 SHA-256 |
| 6 | (기존 패키지) 콘솔에서 **스니펫 복사** | 사용자 → 에이전트에게 전달 | 스니펫은 계정 식별자이므로 커밋하지 않음 |
| 7 | 소유권 증명 APK 빌드 | 에이전트 · PC | `android/app/src/main/assets/adi-registration.properties`에 스니펫 저장 → `flutter build apk --release` → 서명 확인 |
| 8 | 콘솔에 APK 업로드 → 등록 완료 메일 → 상태 **Registered** 확인 | 사용자 | 7의 APK |
| 9 | (경로 A + Google 생성 키) Play 앱 서명 키와 업로드 키 **둘 다** 등록 확인 | 사용자 + 에이전트 | Play Console 앱 무결성 화면 |
| 10 | 원스토어 다음 업데이트에 `adi-registration.properties` 포함 여부 결정 (원스토어 안내 팝업 제거용, 선택) | 사용자 + 에이전트 | — |

- **[추론] Flutter 주의:** 이 파일은 APK 안의 `assets/` 바로 아래에 있어야 합니다. Flutter의 `pubspec.yaml` assets는 `assets/flutter_assets/` 아래로 들어가므로 **쓰면 안 됩니다**. Android 네이티브 assets 폴더 `android/app/src/main/assets/`에 두세요. 빌드 후 `aapt list app-release.apk | findstr adi-registration`로 경로가 `assets/adi-registration.properties`인지 확인합니다. 구조 예시: https://github.com/android/security-samples/tree/main/AndroidDeveloperVerificationAPKSigningExample
- 소유권 증명용 APK는 "빈 프로젝트 + 같은 패키지명"이어도 됩니다 [공식]. 실제 앱으로 만들어도 문제없습니다.

## 8. 언제 할까 (권장)

| 상황 | 권장 시점 |
|------|-----------|
| Google Play를 진행 (2026-11 목표) | **Play Console 계정을 만들 때 함께** — 늦어도 **2026-11-30** |
| 2026-11-30까지 Play 계정이 없음 | Play 보류로 보고 **ADC 전체 배포로 2026-12-31까지** 완료 |
| Google이 한국 시행일을 발표 | 위 일정과 관계없이 **발표 후 2주 안에** 완료 (시행 1개월 전 마감) |
| 원스토어 공지에 인증 필수화 안내 | 즉시 확인 후 같은 기준 적용 |

**[추론] 근거:** 한국 날짜는 미정이지만 "2027년"으로 공개돼 있습니다. 2027년 초 시행 가능성도 있으므로 2026년 안에 끝내 두는 편이 안전합니다. 신원 인증 자체는 약 10분[공식]이지만, 검토나 서류 보완 대기 시간은 공개돼 있지 않습니다.

## 9. 지켜볼 신호 (Watch items)

- [ ] Google의 **한국/전 세계 시행일 발표** — https://developer.android.com/developer-verification (타임라인 "2027 and beyond"), Android Developers Blog
- [ ] **서드파티 스토어 확대** ("곧 모든 서드파티 스토어로 확대") 및 원스토어 참여 여부
- [ ] **원스토어 공지** — https://dev.onestore.net (개발자센터 공지) · FAQ https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification
- [ ] 한국 신원 인증 서류 목록 공개 여부 (ADC 도움말)
- [ ] ADC 결제 수단 · 수수료 변경 (FAQ: "콘솔 출시 때 상세 안내")

## 10. 체크리스트

- [ ] 경로 결정 (A Play / B ADC)
- [ ] Google 계정 2단계 인증 + 결제 프로필(법적 이름·주소 정확히)
- [ ] 신분증 + 주소 증빙 준비
- [ ] 원스토어 제출 때 고른 서명 옵션 확인 ("앱 서명 사용 안함"인지)
- [x] SHA-256 / 공개 인증서 PEM 준비 (`C:\Users\LSH\secure\korean-bible-upload-cert.pem`)
- [ ] 키스토어 + 비밀번호 PC 밖 백업 (등록·업데이트 모두 이 키에 의존)
- [ ] 패키지 등록 → Registered
- [ ] (A) Play 앱 서명 키 방식 결정: PEPK로 기존 키 권장
- [ ] 8절 일정을 캘린더에 등록 (2026-11-30 결정 기한, 2026-12-31 완료 기한)

## 11. 출처
- 개요·타임라인: https://developer.android.com/developer-verification
- 가이드(경로·계정 유형·시행 국가/스토어): https://developer.android.com/developer-verification/guides
- FAQ(수수료 $25·ADB·고급 흐름·키·미참여 스토어): https://developer.android.com/developer-verification/guides/faq
- ADC 등록: https://developer.android.com/developer-verification/guides/android-developer-console
- Play Console 등록: https://developer.android.com/developer-verification/guides/google-play-console
- 전체 배포 신원 서류: https://developer.android.com/developer-verification/guides/full-distribution
- 제한 배포: https://developer.android.com/developer-verification/guides/limited-distribution
- 패키지 등록 절차(신규/기존, 스니펫): https://support.google.com/android-developer-console/answer/16640821
- ADC 계정 필요 정보: https://support.google.com/android-developer-console/answer/16640818
- Play Console 서명 APK 업로드(위임 서명 키): https://support.google.com/googleplay/android-developer/answer/16761055
- 블로그(2026-06-18, 7개 스토어·4개국): https://developer.android.com/blog/posts/android-developer-verification-building-a-safer-ecosystem-together
- 원스토어 FAQ: https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification
