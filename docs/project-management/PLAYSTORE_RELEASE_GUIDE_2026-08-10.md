# 향후 작업 · Play Store 출시 가이드

**기준일:** 2026-08-10 (PPTX 갱신: 2026-08-24)  
**목표:** 2026-11 Google Play 공개 (1.0)  
**앱:** 한국어 성경 (KRV · KJV · ASV · PD 찬송 · 교독 · 예배)  
**PPTX:** `Desktop/Bible Project/KoreanBible_PlayStore_ReleaseGuide_2026-08-24.pptx`  
**디자인:** Linear 스타일 (다크 · Indigo `#5E6AD2`)  
**다음 세션 시작:** [`RESUME_HERE.md`](./RESUME_HERE.md)

---

## 1. 현재 위치

| 영역 | 진행 | 메모 |
|------|------|------|
| 제품 기능 | ~92% | 다역본·검증·찬송·교독·기도 완료 |
| 스토어 공개 준비 | ~20% | packageId · 서명 · 정책 · 리스팅 미완 |
| Drive 백업/업로드 | ✅ | `gdrive_upload` MCP 연결됨 |

**차단 항목 (지금 결정 필요):**
1. `applicationId` (`com.example.*` 사용 불가)
2. 업로드 키스토어 경로/생성
3. 개인정보처리방침 URL
4. 지원 이메일 · Play 개발자 계정

---

## 2. 앞으로 할 작업 (우선순위)

### Sprint A — 스토어 기술 (9월 포커스)

| # | 작업 | 상태 |
|---|------|------|
| A1 | packageId 확정 · Android/iOS 반영 | ⏳ |
| A2 | 표시명 `한국어 성경` 확정 | 🔄 |
| A3 | 키스토어 + `key.properties` (gitignore) | ⏳ |
| A4 | `flutter build appbundle --release` | ⏳ |
| A5 | 프로덕션 서명 APK/AAB 실기기 설치 | ⏳ |
| A6 | targetSdk / 64-bit Play 요구 확인 | ⏳ |

### Sprint B — 공개 전 UX (10월)

| # | 작업 | 가치 |
|---|------|------|
| B1 | 첫 실행 온보딩 (PD · 3역본 · 개역개정 미수록) | 신뢰 |
| B2 | 역본 선택 저장 | 마찰 제거 |
| B3 | 절 복사/공유 | 소그룹 |
| B4 | 설정 > 라이선스/출처 | CS 대응 |
| B5 | 비행기모드·다크·큰글씨 스모크 | 품질 |

### Sprint C — 스토어 자산·정책

| # | 작업 |
|---|------|
| C1 | 개인정보처리방침 페이지 호스팅 |
| C2 | 짧은/긴 설명 최종 카피 |
| C3 | 아이콘 512 · 피처 그래픽 |
| C4 | 폰 스크린샷 4–8장 |
| C5 | 콘텐츠 등급 Everyone · 카테고리 |
| C6 | Play Console 앱 생성 · AAB 업로드 · 출시 트랙 |

### Sprint D — 공개 후 (필수 아님)

통독 계획 · 위치 복원 · 하이라이트 · 교독 강조 · TTS · 태블릿 2열

**하지 않음:** 개역개정 · 비-PD 찬송 · 계정 강제 클라우드

---

## 3. Play Store 출시 과정 (상세 절차)

아래는 **개인/소규모 Flutter 앱** 기준 end-to-end 절차입니다.

### Phase 0 — 사전 결정 (1일)

| 결정 | 예시 / 메모 |
|------|-------------|
| Application ID | `com.lsh.koreanbible` 등 (평생 고정) |
| 앱 표시명 | 한국어 성경 |
| 개발자 계정 | Google Play Console ($25 일회) |
| 지원 이메일 | store/support용 |
| 프라이버시 URL | GitHub Pages / Notion / 개인 사이트 |
| 출시 형태 | 프로덕션 / 비공개 테스트 먼저 |

### Phase 1 — Play Console 계정 · 앱 생성

1. [Google Play Console](https://play.google.com/console) 가입 · 개발자 등록비 결제  
2. **앱 만들기** → 앱 이름 · 기본 언어(한국어) · 앱/게임 · 무료  
3. 정책 선언 설문 시작 (나중에 완성 가능)  
4. **테스트 트랙** 권장: 내부 테스트 → 비공개 → 프로덕션  

### Phase 2 — 앱 ID · 서명 준비 (로컬)

1. `android/app/build.gradle.kts`의 `applicationId` 변경 (`com.example.*` 제거)  
2. 필요 시 패키지 디렉터리/namespace 정리  
3. 키스토어 **1회** 생성 (안전한 폴더, **절대 git 커밋 금지**):

```powershell
mkdir C:\Users\LSH\secure -Force
keytool -genkey -v `
  -keystore C:\Users\LSH\secure\korean-bible-upload.jks `
  -keyalg RSA -keysize 2048 -validity 10000 `
  -alias upload
```

4. `android/key.properties` 작성 (gitignore):

```
storePassword=***
keyPassword=***
keyAlias=upload
storeFile=C:/Users/LSH/secure/korean-bible-upload.jks
```

5. `build.gradle.kts` release `signingConfigs` 연결  
6. Play App Signing: 업로드 키로 AAB 서명 → Google이 앱 서명 키 관리 (권장)

### Phase 3 — 품질 게이트 · 빌드

```powershell
cd "C:\Users\LSH\Bible App\korean-bible-app"
flutter test
python scripts\verify_bible_texts.py
flutter analyze
flutter build appbundle --release
# → build\app\outputs\bundle\release\app-release.aab
```

실기기:

```powershell
flutter build apk --release
adb install -r build\app\outputs\flutter-apk\app-release.apk
```

체크: 비행기 모드 · 다크모드 · 큰 글씨 · 성경/찬송/교독/설정 스모크

### Phase 4 — 스토어 리스팅 자산

| 자산 | 요구 |
|------|------|
| 앱 아이콘 | 512×512 PNG |
| 피처 그래픽 | 1024×500 |
| 폰 스크린샷 | 최소 2장, 권장 4–8 (16:9 또는 장치 해상도) |
| 짧은 설명 | ≤80자 |
| 긴 설명 | ≤4000자 |
| 카테고리 | Books & Reference / Lifestyle |
| 콘텐츠 등급 | Everyone 권장 |

**카피 초안**
- 짧은: `완전 오프라인 한국어 성경 · 찬송 · 예배자료`
- 긴: KRV·KJV·ASV 병렬, PD 찬송, 교독·신경·주기도문, 광고·계정 없음, **개역개정 미수록** 명시

### Phase 5 — 정책 · 개인정보

1. 개인정보처리방침 페이지 공개 URL  
   - 수집 없음 · 오프라인 · 북마크 기기 로컬 · 계정 없음  
2. Play Console **앱 콘텐츠** / **데이터 보안** 양식 작성  
3. 광고 없음 · 아동 대상 아님(해당 시) · 민감 권한 최소화 확인  
4. 콘텐츠 고지: 한국찬송가 공식 아님 · PD only  

### Phase 6 — 업로드 · 테스트 트랙

1. **프로덕션 / 테스트** → 새 버전 만들기 → AAB 업로드  
2. 릴리스 노트 (한국어)  
3. 내부 테스터 이메일 추가 → 링크 설치 검증  
4. 문제 없으면 비공개/오픈 테스트 → 프로덕션  

### Phase 7 — 심사 · 공개

1. 대시보드 **게시 전 필수 항목** 전부 완료 표시 확인  
2. 프로덕션 출시 제출  
3. 심사(보통 수일, 신규 계정은 더 길 수 있음)  
4. 반려 시: 정책/권한/설명 수정 후 재제출  
5. 공개 후: 크래시(Android Vitals) · 리뷰 모니터링 · 핫픽스 AAB  

### Phase 8 — 버전 운영

- `pubspec.yaml` version: `1.0.0+1` → 스토어마다 `+N`(versionCode) 증가  
- 키스토어 백업(오프라인·암호 관리자). 분실 시 앱 업데이트 불가에 가깝다(Play App Signing 사용 시 업로드 키 재설정 절차 가능)

---

## 4. 월별 로드맵 → 2026-11

| 월 | 포커스 |
|----|--------|
| 8월 | 문서화 · 재빌드 · 결정 수집 · Drive 백업 |
| 9월 | packageId · 키스토어 · AAB · 프라이버시 URL · Console |
| 10월 | 온보딩·역본저장·복사 · 스모크 · 스크린샷 · 내부 테스트 |
| 11월 | 프로덕션 제출 · 심사 대응 · 1.0 공개 |

---

## 5. 관련 문서

| 문서 | 용도 |
|------|------|
| `RELEASE_CHECKLIST_PLAYSTORE.md` | R1–R25 체크리스트 |
| `DEPLOY_CHECKLIST.md` | 빌드 명령 · 결정 질문 |
| `VALUE_AND_USABILITY.md` | UX 백로그 |
| `VISION_AND_PLAN.md` | 마일스톤 |
| `APPLIED_AND_ROADMAP_PLAN_2026-08-10.md` | 적용/계획 종합 |

---

*이 MD는 PPTX 원본 콘텐츠입니다. 작업 진척 시 상태만 갱신하세요.*
