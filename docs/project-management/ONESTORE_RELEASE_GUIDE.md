# 원스토어(ONE store) 출시 가이드 — 한국어 성경

**작성일:** 2026-10-03 (KST) · **대상:** `com.lsh.koreanbible` 1.0.0 (versionCode 1) · 무료 · 인앱결제/광고 없음  
**관련 문서:** [`ANDROID_RELEASE_PROCESS.md`](./ANDROID_RELEASE_PROCESS.md) (Google Play 정본) · [`RESUME_HERE.md`](./RESUME_HERE.md) · [`../privacy/privacy-policy.md`](../privacy/privacy-policy.md) · [`../privacy/README.md`](../privacy/README.md)

> **범례**
> - 👤 **사용자(브라우저)**: 원스토어 개발자센터 / ONEconsole에서 본인이 직접 해야 하는 일 (로그인·본인정보·약관 동의·업로드·심사 요청)
> - 🤖 **에이전트(PC)**: 이 PC에서 에이전트가 대신 할 수 있는 일 (빌드·서명 검증·이미지 리사이즈·문구 초안)
> - ⏱ **추정**: 표시된 소요 시간은 **모두 추정치**입니다. 공식 문서에 기재된 시간은 "공식"으로 따로 표시하고 출처 URL을 붙였습니다.
> - 에이전트는 가입·업로드·심사 요청을 **하지 않았습니다**.

---

## 0. 현재 준비 상태 요약 (2026-10-03 확인)

| 항목 | 상태 | 근거 |
|------|------|------|
| 서명된 릴리스 APK | ✅ `build\app\outputs\flutter-apk\app-release.apk` · 60,871,249 bytes (≈58.1 MB) · 2026-10-03 02:08 KST 빌드 | `flutter build apk --release` |
| APK 서명 인증서 | ✅ `CN=LSH, O=personal, C=KR` · SHA-256 `41:9D:AA:1C:…:6E:33:87` = 업로드 키와 일치 · APK Signature Scheme v2 | `apksigner verify --print-certs` |
| 패키지/버전 | ✅ `com.lsh.koreanbible` · versionCode 1 · versionName 1.0.0 | `aapt dump badging` |
| minSdk / targetSdk | ✅ 24 / 36 (원스토어 최소 targetSdk 33, 2026-09-01부터) | 원스토어 공지 (아래 출처) |
| 서명된 AAB | ✅ `build\app\outputs\bundle\release\app-release.aab` (≈56.9 MB) — 원스토어는 APK 권장(아래 2-3 참고) | 2026-09-29 빌드 |
| Google Play 전용 의존성 | ✅ 없음 (GMS/Play Core/Firebase/Billing/AdMob 없음, 코드에 `market://`·`play.google` 링크 없음) | `pubspec.lock`·`lib/`·`android/`·병합 매니페스트 검색 |
| 네트워크 권한 | ✅ 없음 (INTERNET 권한 없음 → 데이터 외부 전송 없음) | 병합 매니페스트 |
| 원스토어 SDK | ✅ 불필요 (무료·인앱결제 없음. IAP SDK는 인앱결제 시에만, ALC는 선택) | 원스토어 개발자 문서 |
| 아이콘 원본 | 🟡 `assets/icon/icon.png` 1024×1024 → 512×512로 리사이즈만 하면 됨 | |
| 스크린샷 (2~8장) | ❌ 없음 | |
| 그래픽 이미지 1024×578 | ❌ 없음 (Play의 1024×500과 크기가 다름) | |
| 상세 설명/키워드 문구 | ❌ 초안 필요 | |
| 개인정보처리방침 URL | 🟡 초안 있음 (`docs/privacy/`), **미게시** — 원스토어에서는 개인정보 미수집 시 필수 아님(아래 2-6) | |
| 원스토어 개발자 계정 | ❌ 미가입 (사용자 결정) | |

---

## 1. 전체 순서 + 소요 시간 (⏱ 모두 추정)

| # | 단계 | 담당 | ⏱ 작업 시간(추정) | 공식 기준 |
|---|------|------|------------------|-----------|
| 1 | 원스토어 개발자 회원가입 (개인개발자) + 이메일 인증 | 👤 | 15~30분 | 공식 시간 기재 없음 |
| 2 | (무료앱이므로) 정산정보 등록 **생략** | — | 0분 | 유료/인앱결제일 때만 필요 |
| 3 | 릴리스 APK 빌드·서명 검증 | 🤖 | ✅ 완료 (빌드 약 1~3분) | — |
| 4 | 그래픽 자산 준비 (아이콘 512, 스크린샷 2~8장, 그래픽 1024×578) | 🤖 초안 + 👤 캡처/검토 | 2~4시간 | — |
| 5 | 판매 문구 (제목·한줄·상세 설명·키워드·권한 설명) | 🤖 초안 + 👤 검토 | 30~60분 | — |
| 6 | (선택·권장) 개인정보처리방침 URL 게시 | 👤 (GitHub Pages 켜기) | 10~20분 + 반영 수 분 | — |
| 7 | ONEconsole 상품 등록 (기본정보→바이너리→판매정보→수집정보→연령등급→배포국가/가격) | 👤 | 1~1.5시간 (APK 58 MB 업로드 포함) | — |
| 8 | 심사 요청 → 심사 | 👤 요청 / 원스토어 심사 | 대기 | **공식: 최대 5영업일**, 경우에 따라 더 걸릴 수 있음 · 미국 배포 시 약 5영업일 추가 |
| 9 | 출시 적용 (즉시/직접/예약) | 👤 | 5분 | AAB 업로드 시 기기별 APK 생성 **최대 약 30분(공식)** · APK 업로드 시 해당 없음 |
| 10 | 출시 후 확인·업데이트 운영 | 👤 + 🤖 | 회당 30분~1시간 | 업데이트도 심사 있음 |

**합계 (⏱ 추정)**
- **실제 작업 시간:** 약 **4~7시간** → 하루 안에 마칠 수 있는 분량 (1·4·5·7단계가 대부분)
- **달력 기준:** 작업 1일 + 심사 **최대 5영업일(공식)** ≈ **약 1~2주** (주말·공휴일·보완 요청 시 더 늘어남)
- 참고: 2024년 개인 블로그(velog)에는 하루 안에 심사가 끝났다는 후기가 있으나 **비공식 사례**입니다.

---

## 2. 단계별 상세

### 1단계 — 회원가입 👤 ⏱ 15~30분(추정)
1. https://dev.onestore.net 접속 → 회원가입
2. 약관 동의 → 아이디·비밀번호·보안 질문·국가(대한민국) 입력
3. **회원 유형: `개인개발자`** 선택 (개인사업자/법인사업자 아님)
4. 기본정보: 이름, 휴대폰 번호, 이메일, 전화번호, 주소, 생년월일
5. 이메일 인증으로 가입 완료
- 가입 **무료**, 만 14세 이상
- 준비물: 본인 휴대폰, 이메일, 주소
- 출처: https://onestore-dev.gitbook.io/dev/docs/member/sign-up · https://onestore-dev.gitbook.io/dev/docs/member/info/basic-info
- ⚠ 불명확: 원스토어 GitHub 위키에는 가입 시 "본인인증"(서류 불필요)이라고 되어 있으나 공식 가입 페이지에는 이메일 인증만 나옵니다. 휴대폰 본인인증 화면이 나올 수 있으니 본인 명의 휴대폰을 준비하세요.

### 2단계 — 정산정보 (생략) — ⏱ 0분
- 무료 앱은 필요 없습니다. 유료 앱이나 인앱결제를 하게 되면 그때 등록합니다. 개인개발자는 **범용 공인인증서**로 계좌를 인증해야 하고, 유료 판매는 운영자 승인이 필요합니다.
- FAQ: 무료/유료 앱 등록 절차는 동일
- 출처: https://onestore-dev.gitbook.io/dev/docs/member/info/settlement-info · https://onestore-dev.gitbook.io/dev/docs/apps/product/monetization/price-info · https://onestore-dev.gitbook.io/dev/help/faq/apps

### 3단계 — 바이너리 준비 🤖 ✅ 완료
- 파일: `C:\Users\LSH\Bible App\korean-bible-app\build\app\outputs\flutter-apk\app-release.apk`
- 재빌드 명령 (에이전트가 실행 가능):
  ```powershell
  cd "C:\Users\LSH\Bible App\korean-bible-app"
  flutter build apk --release
  & "$env:LOCALAPPDATA\Android\sdk\build-tools\37.0.0\apksigner.bat" verify --print-certs build\app\outputs\flutter-apk\app-release.apk
  ```
  → `certificate SHA-256 digest: 419daa1c…946e3387` 이 나와야 함 (디버그 서명 APK는 원스토어가 받지 않음)
- 원스토어 바이너리 규칙 (출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/binary)
  - APK 또는 AAB 가능. APK→AAB 전환은 되지만 **AAB→APK는 불가**. AAB는 minSdk 21 이상. 최대 2 GB
  - 업로드 시 바이러스·패키지명 중복·서명 키·버전 코드 검사
  - 업데이트는 **같은 키로 서명 + 더 높은 versionCode** 필수 (https://onestore-dev.gitbook.io/dev/docs/review/one-store-review-guideline/undefined-5)
  - 디버그 서명 불가 (https://onestore-dev.gitbook.io/dev/help/faq/tools)
- 최소 targetSdk: 31 이상(2026-05-01부터), **33 이상(2026-09-01부터)**. 이후 상향은 별도 공지 예정. 우리 앱 36 → 충족. 출처: https://dev.onestore.net/devpoc/support/news/noticeView.omp?noticeId=33671 (2026-02-19 공지)

#### ★ 결정 필요: 앱 서명 방식 (권장안)
바이너리 등록 화면의 서명 키 옵션 4가지:
1. 원스토어가 키 생성·관리 (신규 상품만)
2. 계정의 다른 앱과 같은 키
3. PEPK 도구로 내 키 업로드
4. **앱 서명 사용 안함 — 직접 서명한 APK 업로드 (APK만 가능)**

**권장: 4번 "앱 서명 사용 안함" + 위 APK 업로드.**
- 이유: 사용자 기기에 설치되는 서명이 우리 업로드 키(`SHA-256 41:9D…33:87`)와 같아집니다. 원스토어 AAB FAQ도 "다른 마켓과 같은 앱으로 업데이트하려면 서명 키가 같아야 하므로 스토어 생성 키 대신 자기 키를 등록하라"고 안내합니다 (https://onestore-dev.gitbook.io/dev/help/faq/apps/one-store-android-app-bundle).
- 나중에 Google Play: Play 앱 서명에서 Google이 만든 키를 쓰면 Play 버전 서명이 원스토어 버전과 **달라집니다**. 그러면 한 스토어에서 받은 앱을 다른 스토어 버전으로 업데이트할 수 없습니다. 두 스토어 서명을 맞추려면 Play Console에서 **"기존 앱 서명 키 사용(PEPK로 업로드)"**을 선택하세요. 이 결정은 `ANDROID_RELEASE_PROCESS.md` 쪽에도 반영해야 합니다.
- 1번(원스토어 생성 키)은 한 번 정하면 되돌리기 어렵고 Play와 서명이 달라지므로 **비추천**합니다.

#### ⚠ Play 프로텍트 차단 위험
- 공식 바이너리 페이지: 패키지명이 Google Play에 배포된 적이 없거나 Play와 패키지명/서명이 다르면 설치 시 "Play 프로텍트에 의해 차단됨"이 뜰 수 있습니다. 미리 Google에 소명(이의 제기)하라고 안내합니다. targetSdk가 낮으면 "안전하지 않은 앱" 경고도 뜰 수 있는데, 33 이상이면 피할 수 있습니다.
- 우리 앱은 **아직 Play에 출시되지 않아** 첫 번째 위험에 해당합니다. targetSdk 36이라 두 번째 위험은 해당 없습니다.
- 대응: (a) Google Play 출시를 먼저 하거나 동시에 진행, (b) 원스토어 출시 후 실기기에서 설치 테스트, (c) 차단되면 Google에 소명. ⚠ 공식 페이지의 소명 링크가 문서에 비어 있어 정확한 URL을 확인하지 못했습니다.

#### 참고: Google 안드로이드 개발자 인증
- 2026-09-30부터는 브라질·인도네시아·싱가포르·태국에서만 시행되고, 전 세계 확대는 2027년 예정(날짜 미정)입니다. **한국 배포는 현재 영향 없음.**
- 대비책으로 `com.lsh.koreanbible`을 Play Console 또는 Android Developer Console에 서명 APK와 함께 등록해 두면 좋습니다.
- 원스토어는 `assets/adi-registration.properties`가 없으면 안내 팝업만 띄우며, 심사와는 무관합니다.
- 출처: https://developer.android.com/developer-verification · https://developer.android.com/developer-verification/guides/faq · https://onestore-dev.gitbook.io/dev/help/faq/apps/developer-verification

### 4단계 — 그래픽 자산 🤖 초안 + 👤 캡처/검토 ⏱ 2~4시간(추정)
출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/app-info · 이미지 가이드 https://onestore-dev.gitbook.io/dev/tools/icon-guide

| 자산 | 규격 (공식) | 필수 | 준비 방법 | ⏱ 추정 |
|------|-------------|------|-----------|--------|
| 아이콘 | **512×512**, JPG/PNG (아이콘 가이드 PDF 참고) | 필수 | 🤖 `assets/icon/icon.png`(1024²)를 리사이즈 | 10분 |
| 스크린샷 | **2~8장**, JPG/PNG, 장당 **1 MB 이하**, 최대 **1300×1300 px**, 권장 **720×1280(세로)** 또는 1280×720(가로) | 필수 | 👤 실기기/에뮬레이터로 캡처 → 🤖 720×1280 리사이즈·1 MB 이하 압축 | 1~2시간 |
| 그래픽 이미지 | **1024×578**, JPG/PNG | 필수로 안내됨 | 🤖 아이콘+앱 이름으로 배너 초안 → 👤 검토 | 30~60분 |
| 동영상 | MP4, 최대 500 MB, 15초~10분 | 선택 | 생략 권장 | — |

추천 스크린샷 구성 (6장): ① 성경 본문 읽기 ② 역본 선택(KRV/KJV/ASV) ③ 찬송가 ④ 교독문 ⑤ 북마크 ⑥ 다크 모드/글자 크기

### 5단계 — 판매 문구 🤖 초안 + 👤 검토 ⏱ 30~60분(추정)
| 항목 | 제한 (공식) | 메모 |
|------|-------------|------|
| 앱 제목 | 50자 이하 | 예: `한국어 성경 - 개역한글·찬송가·교독문` (실제 앱 라벨: `한국어 성경`) |
| 한 줄 설명 | 100자 이하 | |
| 상세 설명 | 1,300자 이하 | 오프라인·무료·광고 없음 강조. **다른 앱마켓 링크/언급 금지** (반려 사유) |
| 검색 키워드 | 1~10개 | 성경, 개역한글, 찬송가, 교독문, KJV, 오프라인 성경 … |
| 권한 설명 | 권한별 | 위험 권한 없음 (INTERNET 권한도 없음) |
| 카테고리 | 자유 선택 (게임↔비게임 전환만 재심사) | ⚠ 공식 카테고리 목록은 문서에서 찾지 못함 — 콘솔에서 확인. 후보: 생활/라이프스타일·도서/참고 계열 |
| 판매자 정보 | 판매자명, 공식 이메일, 전화, 웹사이트 | 👤 공개되는 연락처이므로 본인이 결정 |
출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/app-info · https://onestore-dev.gitbook.io/dev/docs/apps/product/common-info/main-info

### 6단계 — 개인정보처리방침 URL (선택·권장) 👤 ⏱ 10~20분(추정)
- 원스토어 수집정보 페이지 기준: 데이터가 **기기 밖으로 전송·공유될 때만** "예"를 선택합니다. 우리 앱은 설정·북마크·즐겨찾기를 기기 안(SharedPreferences/Hive)에만 저장하고 INTERNET 권한도 없으므로 → **"아니오"**.
- 개인정보처리방침 URL은 **개인정보를 수집하는 경우에** 필수입니다. 우리 앱은 해당하지 않지만 등록을 권장합니다. 미국 배포 시에는 개인정보 URL이나 웹사이트가 필요합니다.
- 게시 방법: `docs/privacy/README.md` (GitHub Pages → `https://bcspl.github.io/korean-bible-app/privacy/`). 게시 전에 `[개발자 이름] [지원 이메일] [게시일] [시행일]` 자리표시자를 채워야 합니다. Pages 켜기는 저장소 설정 변경이므로 👤 사용자가 직접 해야 합니다.
- 출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/common-info/main-info/data · https://onestore-dev.gitbook.io/dev/docs/review/one-store-review-guideline/undefined-2
- ⚠ 불명확: 데이터를 수집하지 않는 앱이 URL 칸을 비워 둬도 되는지 콘솔 UI에서 최종 확인 필요

### 7단계 — ONEconsole 상품 등록 👤 ⏱ 1~1.5시간(추정)
출처: https://onestore-dev.gitbook.io/dev/docs/apps/register-app · https://onestore-dev.gitbook.io/dev/docs/apps/product/android/main-info

1. **새 상품 등록**
   - 출시 유형: **정식 출시** (베타 아님 — **나중에 변경 불가**)
   - OS: Android
   - 앱 제목 (50자)
   - 패키지명: `com.lsh.koreanbible` (**나중에 변경 불가**, 바이너리와 같아야 함)
2. **기본정보**
   - 광고 SDK 적용 여부 → **아니오**
   - Android Auto → **아니오**
   - "Google Play 패키지 네임"(선택) → Play 출시 후 `com.lsh.koreanbible` 입력
3. **바이너리**: 서명 옵션 **"앱 서명 사용 안함"** → `app-release.apk` 업로드 (3단계 참고)
4. **판매정보**: 4·5단계 자산과 문구 입력
5. **수집정보**
   - 데이터 수집/공유 → **아니오**
   - 지식재산권: 공개 저작물(KRV/KJV/ASV, 찬송가 등). 제3자 권리를 증빙할 대상 없음 — 📝 단, 출처·라이선스 문서는 손에 둘 것
   - **외부결제 사용 여부 → "사용안함"** (영구 설정이므로 주의)
6. **연령등급**
   - IARC 설문 작성 (또는 기존 IARC ID 재사용)
   - 한국 비게임 앱은 **원스토어 앱 등급**(3+/7+/12+/16+/19+)도 설정 → 예상 **3+**
   - 게임위(GRAC) 등급은 게임만 해당 → 불필요
   - 출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/common-info/age-rating · …/age-rating/iarc · …/age-rating/onestorerating
7. **배포 국가/가격**: 대한민국, **무료** (기본값 한국·KRW). 미국 배포는 심사 약 5영업일 추가 + 개인정보 URL 필요 → 1.0은 **한국만** 권장

#### 패키지명 관련 메모 (결정 필요)
- 공식 등록 문서는 "다른 Android 앱마켓의 앱과 **패키지 네임은 분리**하고 버전 코드는 동일하게 운영하는 것을 **권장**"한다고 되어 있습니다.
- 반면 기본정보에는 "Google Play 패키지 네임" 입력란이 있고, 심사 FAQ는 Google Play에 출시한 바이너리를 그대로 올려도 된다고 합니다 (https://onestore-dev.gitbook.io/dev/help/faq/review).
- 또한 Play 프로텍트 안내는 패키지명이나 서명이 Play와 **다를 때** 차단 위험이 있다고 합니다.
- → **권장(에이전트 의견): 같은 패키지명 `com.lsh.koreanbible` + 같은 서명 키.** 분리 권장은 "권장"일 뿐 필수 규칙이 아닙니다. 다만 두 문서가 서로 다르게 안내하므로 사용자가 최종 결정하세요.

### 8단계 — 심사 요청 👤 / 심사 ⏱ 공식 최대 5영업일
- 흐름: 심사 요청 → 시스템 검수(바이러스 등) → 가이드라인 심사 → **이메일로 결과 + 리포트**
- 기간: **공식 최대 5영업일** (경우에 따라 더 걸릴 수 있음), 미국 배포 시 약 5영업일 추가
- 출처: https://onestore-dev.gitbook.io/dev/docs/apps/request-for-review · https://onestore-dev.gitbook.io/dev/docs/review
- 자주 나오는 반려 사유와 우리 앱 점검 (https://onestore-dev.gitbook.io/dev/help/faq/review · https://onestore-dev.gitbook.io/dev/docs/review/one-store-review-guideline/undefined-5 · …/undefined-7)

| 반려 사유 | 우리 앱 |
|-----------|---------|
| 실행 안 됨/강제 종료 | 🟡 실기기 스모크 테스트 필요 (Sprint A5/R11 미완) |
| 다른 앱마켓 링크·언급 | ✅ 없음 (코드 검색 확인) — 상세 설명에도 넣지 말 것 |
| 인앱/외부 결제 문제 | ✅ 결제 없음 |
| 개인정보 수집하면서 동의 누락 | ✅ 수집 없음 |
| 부적절한 메타데이터, 테스트용 앱 | 🟡 설명·스크린샷이 실제 기능과 일치해야 함 |

### 9단계 — 출시 적용 👤 ⏱ 5분(추정)
- 승인 후 적용 방식: **즉시 적용 / 직접 적용 / 예약 적용** (https://onestore-dev.gitbook.io/dev/docs/apps/distribution-management)
- 상태 변화: 등록중 → 판매대기 → **판매중** (https://onestore-dev.gitbook.io/dev/docs/apps/product/android/displayed-info)
- AAB로 올렸다면 기기별 APK 생성에 최대 약 30분(공식). APK 업로드는 해당 없음.

### 10단계 — 출시 후 운영 👤 + 🤖
- 원스토어 앱에서 검색하고 실기기에 설치해 보기 → Play 프로텍트 경고가 뜨는지 확인
- 업데이트 절차: 🤖 `pubspec.yaml` 버전 올리기 (예: `1.0.1+2`) → `flutter build apk --release` → 서명 SHA-256 확인 → 👤 콘솔에 새 바이너리 업로드 → 심사
- Google Play에 올릴 때도 **versionCode를 같게** 운영하세요 (원스토어 권장)
- ⚠ 키스토어 `C:\Users\LSH\secure\korean-bible-upload.jks`와 비밀번호 백업을 **반드시 보관**하세요. "앱 서명 사용 안함"을 쓰면 키를 잃어버렸을 때 업데이트가 **불가능**합니다.

---

## 3. 체크리스트

### 사용자가 준비할 것 👤
- [ ] 원스토어 개발자 계정 (개인개발자) — 본인 휴대폰, 이메일, 주소
- [ ] 공개할 판매자 정보: 판매자명, 이메일, 전화번호, 웹사이트(선택)
- [ ] 스크린샷 캡처 2~8장 (실기기 또는 에뮬레이터)
- [ ] 결정: 서명 방식 ("앱 서명 사용 안함" 권장)
- [ ] 결정: 패키지명 (같은 `com.lsh.koreanbible` 권장)
- [ ] 결정: 개인정보처리방침 URL 게시 여부 (GitHub Pages)
- [ ] 결정: 배포 국가 (한국만 권장)
- [ ] 결정: 카테고리
- [ ] 실기기 설치 스모크 테스트 (강제 종료 없음 확인)

### 에이전트가 할 수 있는 것 🤖
- [x] 서명된 릴리스 APK 빌드 + 서명/패키지/targetSdk 검증
- [x] Google Play 전용 의존성 / 다른 마켓 링크 점검
- [ ] 아이콘 512×512 생성
- [ ] 그래픽 이미지 1024×578 초안
- [ ] 스크린샷을 720×1280, 1 MB 이하로 변환
- [ ] 제목/한 줄 설명/상세 설명(1,300자)/키워드 초안
- [ ] 개인정보처리방침 자리표시자 채우기 (사용자 정보 받은 뒤)

### 등록 직전 최종 확인
- [ ] APK SHA-256 = `41:9D:AA:1C:6E:72:33:EB:FC:32:9B:7B:C4:B5:FD:FE:2E:74:94:C2:69:B8:7D:42:19:57:AC:AE:94:6E:33:87`
- [ ] versionCode 1, targetSdk ≥ 33
- [ ] 출시 유형 "정식" · 외부결제 "사용안함" (둘 다 변경 불가)
- [ ] 수집정보 "아니오" · 광고 SDK "아니오"
- [ ] 연령등급: IARC + 원스토어 3+

---

## 4. 공식 문서에서 불명확한 점
1. **카테고리 전체 목록**이 공개 문서에 없음 → 콘솔에서 확인
2. **가입 시 본인인증 방식**: GitHub 위키는 "본인인증", 공식 가입 페이지는 이메일 인증만 언급
3. **개인정보 미수집 앱의 처리방침 URL**: 필수 아님으로 읽히지만 콘솔 UI에서 확인 필요
4. **패키지명**: "다른 마켓과 분리 권장" vs "Google Play 패키지 네임 입력란 / Play 바이너리 그대로 가능 / 다르면 Play 프로텍트 위험" — 서로 다르게 안내
5. **Play 프로텍트 소명 링크**: 공식 페이지에 링크 자리만 있고 URL이 비어 있음
6. **심사 소요**: 공식은 "최대 5영업일"만 기재, 평균치는 공개되지 않음
7. **그래픽 이미지(1024×578)**가 필수인지 선택인지 문서 표현이 분명하지 않음

## 5. 주요 출처 (2026-10-03 확인)
- 개발자 문서 색인: https://onestore-dev.gitbook.io/dev/llms.txt
- 가입: https://onestore-dev.gitbook.io/dev/docs/member/sign-up
- 상품 등록: https://onestore-dev.gitbook.io/dev/docs/apps/register-app
- 바이너리: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/binary
- 판매정보: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/app-info
- 수집정보: https://onestore-dev.gitbook.io/dev/docs/apps/product/common-info/main-info/data
- 연령등급: https://onestore-dev.gitbook.io/dev/docs/apps/product/common-info/age-rating
- 심사: https://onestore-dev.gitbook.io/dev/docs/apps/request-for-review · https://onestore-dev.gitbook.io/dev/docs/review
- 심사 FAQ: https://onestore-dev.gitbook.io/dev/help/faq/review
- AAB FAQ: https://onestore-dev.gitbook.io/dev/help/faq/apps/one-store-android-app-bundle
- targetSdk 공지: https://dev.onestore.net/devpoc/support/news/noticeView.omp?noticeId=33671
- Google 개발자 인증: https://developer.android.com/developer-verification
