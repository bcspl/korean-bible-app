# 세션 업데이트 로그

**용법:** 매 작업 종료 시 **맨 위에** 새 블록 추가 (최신순).  
**재개:** [`RESUME_HERE.md`](./RESUME_HERE.md) 를 다음 세션 시작점으로 사용.

---

## 2026-10-03 (3) — 배너 확정 · 원스토어 출시 PPTX

### 한 일
- 배너: 인디고/골드 `banner_1024x578.png` 확정, 흑백/빨강 대안 삭제 (repo + Desktop)
- `docs/roadmap-pptx/KoreanBible_ONEstore_Release_Process_2026-10-03.pptx` 19장 (+ Desktop) · 생성기 `generate_onestore_release_pptx.py` (9/29 덱 스타일 재사용) · PowerPoint 렌더 검수

### 다음 1건
- 사용자: 원스토어 가입 → 콘솔 등록 → 심사 요청

---
## 2026-10-03 (2) — 원스토어 등록 자산 초안

### 한 일
- `docs/store-assets/onestore/`: 아이콘 512² RGBA · 그래픽 1024×578(브랜드 인디고/골드 권장안 + 흑백/빨강 대안) · 스크린샷 6장 720×1280(웹 빌드를 헤드리스 Chrome으로 캡처) · `listing_ko.md`(제목 21자/한 줄 62자/상세 685자/키워드 10개/카테고리 제안)
- 같은 폴더를 `Desktop\Bible Project\onestore-assets\`에 복사

### 리스크
- 스크린샷은 Android 실기기가 아닌 웹 렌더링 (글꼴/상태바 차이 가능)
- 앱 번들에 `kor-korean.osis.xml`(5.7 MB) · `hymns.json.bak` 등 미사용 추정 자산이 포함되어 APK 크기가 늘어남 → 정리 검토

### 다음 1건
- 사용자: 원스토어 가입 · 판매자 정보 · 카테고리 확인 → 콘솔 등록

---
## 2026-10-03 — 원스토어(ONE store) 출시 조사 · 서명 APK 재빌드 · 가이드

### 한 일
- 원스토어 공식 개발자 문서(GitBook)·공지 조사 → `ONESTORE_RELEASE_GUIDE.md` (단계별 담당 👤/🤖 · 추정 소요시간 · 자산 규격 · 체크리스트 · 출처)
- `flutter build apk --release` 재빌드 → `build\app\outputs\flutter-apk\app-release.apk` 60,871,249 B · 업로드 키 서명(v2) SHA-256 일치 · com.lsh.koreanbible vc1 · min 24 / target 36
- Google Play 전용 의존성·타 마켓 링크 없음 확인 (원스토어 SDK 불필요: 무료·IAP 없음)

### 막힌 일 / 리스크
- 원스토어 가입·등록·심사 요청은 사용자 몫 (에이전트 미실행)
- Play 미출시 패키지 → 원스토어 설치 시 Play 프로텍트 차단 가능성
- 결정 필요: 서명 방식("앱 서명 사용 안함" 권장) · 패키지명 동일 여부 · Play 앱 서명 키를 PEPK로 맞출지

### 다음 1건
- 원스토어 자산(아이콘 512 · 그래픽 1024×578 · 스크린샷 720×1280) + 문구 초안

---
## 2026-09-29 — GitHub push · 개인정보처리방침 초안 · Android 출시 정본 + PPTX

### 한 일
- 비밀정보 재점검(키·.jks 미추적, push 대상/전체 이력에 비밀번호 없음) 후 `git push origin main` (`ae7b2b1..fae983b`)
- 코드 조사 기반 개인정보처리방침 한/영 초안: `docs/privacy/privacy-policy.md` · `index.html` · 호스팅 안내 `README.md`
  - release 매니페스트 INTERNET 권한 없음 · 제3자 SDK 없음 · 기기 내 저장만(SharedPreferences 3개 설정, Hive 북마크/찬송 즐겨찾기/본문 캐시) · allowBackup 기본값 명시
- `ANDROID_RELEASE_PROCESS.md` (Phase 0–8 정본 · 완료 내역 · 명령 · 정책 출처)
- PPTX 27장 `docs/roadmap-pptx/KoreanBible_Android_Release_Process_2026-09-29.pptx` (+ Desktop) · 생성기 `generate_android_release_pptx.py`
- 정책 웹 확인: 비공개 테스트 12명×14일(2023-11-13 이후 개인 계정) · 타겟 API 36(2026-08-31~) · Data safety/방침 필수 · $25 등록비
- PLAYSTORE 가이드·체크리스트 상태 갱신 (R2 🔄, R9 ✅, R21 ⛔)

### 막힌 일 / 리스크
- Play Console 계정·본인 인증 (사용자) — 11월 공개의 critical path
- 비공개 테스터 12명+ 모집 필요 · 10월 중순 시작해야 11월 공개 가능
- Play 정책상 **앱 내부에도** 개인정보처리방침 텍스트/링크 필요 → 미구현
- 키스토어 PC 밖 백업 미완

### 다음 1건
- R11 실기기 스모크 + 앱 내 방침/라이선스 화면 → Pages 게시 → Console 내부 테스트

---

## 2026-09-29 — Sprint A3/A4: 업로드 키스토어 + 서명 AAB (R7, R8)

### 한 일
- 업로드 키스토어 생성: `C:\Users\LSH\secure\korean-bible-upload.jks` (PKCS12 · RSA 2048 · alias `upload` · CN=LSH, O=personal, C=KR · ~2054-02-14 유효)
  - SHA-1: `AA:71:3A:D2:54:66:1C:37:1C:3B:18:D6:60:57:65:F6:54:39:9F:A7`
  - SHA-256: `41:9D:AA:1C:6E:72:33:EB:FC:32:9B:7B:C4:B5:FD:FE:2E:74:94:C2:69:B8:7D:42:19:57:AC:AE:94:6E:33:87`
- 비밀번호: 무작위 24자 (store=key) — `android/key.properties`(gitignore) + `C:\Users\LSH\secure\korean-bible-key.properties.backup.txt`에만 저장, 출력/커밋 없음
- `android/app/build.gradle.kts`: `key.properties` 있으면 `signingConfigs.release` 사용, 없으면 debug 서명 fallback
- `flutter build appbundle --release` 성공 → `build\app\outputs\bundle\release\app-release.aab` (56.9MB), 인증서 지문 일치 확인

### 막힌 일 / 리스크
- 키스토어 + 비밀번호를 **PC 밖에 백업** 필요 (USB/암호관리자). 분실 시 Play 업로드 키 재설정 절차 필요
- Privacy URL (R2) · 개발자 계정 (R21) 미정

### 다음 1건
- 서명 APK 실기기 설치 스모크 (R11) → Privacy URL → Play Console 내부 테스트 AAB 업로드

---
## 2026-09-28 — Sprint A1: applicationId → com.lsh.koreanbible (R5)

### 한 일
- 8/24 미커밋 문서 작업 커밋 (`docs: 2026-08-24 Play Store release guide checkpoint`)
- Android `applicationId`/`namespace`를 `com.lsh.koreanbible`로 변경
- `MainActivity.kt` 패키지 디렉터리 이동 (`com/example/korean_bible_app` → `com/lsh/koreanbible`)
- `flutter pub get` · `flutter analyze` (기존 info 19건, 신규 이슈 없음) · `flutter build apk --release` 성공
- APK: `build\app\outputs\flutter-apk\app-release.apk` (~58.1MB), package=`com.lsh.koreanbible`
- R5 체크리스트·RESUME_HERE·본 로그 갱신

### 막힌 일 / 리스크
- R7 키스토어: 사용자 비밀번호 필요 — 생성·`key.properties`는 다음 세션
- iOS/macOS/linux/windows 번들 ID는 아직 `com.example.*` (Android만 변경)

### 다음 1건
- 키스토어 생성 (`C:\Users\LSH\secure\korean-bible-upload.jks`, alias `upload`) + `android/key.properties` + release `signingConfigs` → AAB (R7→R8)

---

## 2026-08-24 — 체크포인트 저장 (RESUME_HERE)

### 한 일
- 향후 작업 계획을 **Play Store Phase 0–8 + Sprint A–D** 방식으로 확정·문서화
- Linear PPTX 출시 가이드 생성·QA·Desktop/docs/Drive 저장
- **`RESUME_HERE.md`** 체크포인트 작성 — 다음 세션은 이 파일부터 시작
- `README.md`를 RESUME 우선으로 갱신

### 막힌 일 / 리스크
- packageId · 키스토어 · Privacy URL · 지원 이메일 — 사용자 결정 대기 (⛔)

### 다음 1건
- `RESUME_HERE.md` §3: packageId 확정 → applicationId 변경 → 키스토어 → AAB (R5→R7→R8)
- 결정 대기 중이면 Sprint B(온보딩·역본저장·절복사) 병행 가능

---

## 2026-08-24 — Play Store 출시 가이드 문서화 (Linear PPTX)

### 한 일
- 향후 작업 + Play Store Phase 0–8 상세 절차 MD 작성 (`PLAYSTORE_RELEASE_GUIDE_2026-08-10.md`)
- Linear 스타일 PPTX 15장 생성 → Desktop/Bible Project + docs/
- gdrive_upload MCP로 바이너리 Drive 업로드 가능 상태 유지

### 막힌 일 / 리스크
- packageId · 키스토어 · Privacy URL 사용자 결정 대기

### 다음 1건
- packageId 확정 후 applicationId 변경 + 키스토어/AAB

---

## 2026-08-10 — PM 구조 · 바이낸스 스타일 보고서 · Drive 백업

### 한 일
- 프로젝트 관리 폴더 구조 신설 (`docs/project-management/`)
- 비전·11월 플레이스토어 일정·공개 전 필수 과제 문서화
- 바이낸스 디자인 스타일 PPTX 보고서 생성 → Desktop/Bible Project
- 소스·문서 백업 패키징 및 Google Drive 폴더 연동 시도

### 이미 반영되어 있던 제품 (누적)
- KRV/KJV/ASV 병렬, 본문 검증 PASS, PD 찬송 102, 교독 51, 기도 본문만
- 진행 ~92% (제품) / 스토어 공개 준비 ~20%

### 막힌 일 / 리스크
- Google Drive MCP에 바이너리 업로드 도구 없음 → zip 로컬 생성 후 Drive 폴더 구조만 준비 가능

### 다음 1건
- packageId 확정 + 키스토어 생성 명령 실행 (R5/R7)

---

<!-- 템플릿
## YYYY-MM-DD — 제목
### 한 일
- 
### 막힌 일
- 
### 다음 1건
- 
-->
