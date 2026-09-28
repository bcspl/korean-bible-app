# RESUME HERE — 다음 세션 시작점

**체크포인트:** 2026-09-29  
**작업 방식:** Play Store Phase 0→8 가이드 + Sprint A→D 우선순위 (Linear PPTX에 문서화됨)  
**목표:** 2026-11 Google Play 1.0 공개

> **다음 세션 첫 문장 예시**  
> `docs/project-management/RESUME_HERE.md 읽고 Sprint A5(실기기 설치/R11)부터 이어서 해줘.`

---

## 1. 한 줄 상태

| 영역 | % | 메모 |
|------|---|------|
| 제품 기능 | ~92% | KRV/KJV/ASV · 찬송102 · 교독51 · 기도 · 검증 PASS |
| 스토어 공개 준비 | ~40% | packageId · 키스토어 · 서명 AAB 완료 · **Privacy URL·Console 대기** |
| Drive 업로드 | ✅ | `gdrive_upload` MCP (H:\내 드라이브 동기화) |

**제품은 거의 끝 · 병목은 Play 기술/정책 결정.**

---

## 2. 확정된 작업 계획 (이 방식으로 진행)

상세: `PLAYSTORE_RELEASE_GUIDE_2026-08-10.md`  
PPTX: `Desktop/Bible Project/KoreanBible_PlayStore_ReleaseGuide_2026-08-24.pptx`

### Sprint 순서

| Sprint | 내용 | 시기 |
|--------|------|------|
| **A** | 스토어 기술: packageId · 키스토어 · AAB · 실기기 | 9월 |
| **B** | 공개 전 UX: 온보딩 · 역본저장 · 복사/공유 · 라이선스 · 스모크 | 10월 |
| **C** | 자산·정책: Privacy URL · 카피 · 아이콘/스크린샷 · Console | 9–10월 |
| **D** | 공개 후: 통독 · 위치복원 · 하이라이트 · TTS … | 12월+ |

### Play 절차 (Phase)

`0 결정 → 1 Console → 2 서명 → 3 빌드 → 4 리스팅 → 5 정책 → 6 테스트 → 7 심사 → 8 운영`

---

## 3. 다음 세션에서 할 일 (우선순위)

### ⛔ 사용자 결정이 있어야 진행 (지금 막힘)

1. ~~**packageId**~~ — ✅ `com.lsh.koreanbible` (2026-09-28, R5)
2. **표시명** — `한국어 성경` 확정 여부
3. ~~**키스토어**~~ — ✅ `C:\Users\LSH\secure\korean-bible-upload.jks` · alias `upload` (2026-09-29, R7) · 비밀번호는 `android/key.properties`(gitignore) + `C:\Users\LSH\secure\korean-bible-key.properties.backup.txt` → **오프라인/암호관리자 백업 필요**
4. **Privacy URL** — 호스팅처 (GitHub Pages / Notion / 기타)
5. **지원 이메일** · Play 개발자 계정 준비 여부

### ✅ 결정 없이 바로 할 수 있는 것 (대기 중 병행)

- 온보딩 1화면 UI 초안 (문구만 플레이스홀더)
- 역본 선택 SharedPreferences 저장
- 절 복사(단일 역본) 
- 설정 > 라이선스/출처 화면
- `flutter build apk --release` 스모크용 재빌드 (debug/upload 키 전)

**권장 다음 1건:** 서명 APK 실기기 설치 스모크 (R11) → Privacy URL (R2) → Play Console 앱 생성·내부 테스트에 AAB 업로드.

체크리스트 ID: **R11 → R2 → R21** (R5·R7·R8 ✅) (`RELEASE_CHECKLIST_PLAYSTORE.md`)

---

## 4. 하지 말 것

- `com.example.*` 로 Play 업로드
- 키스토어 / `key.properties` git 커밋
- 개역개정·비-PD 찬송 추가
- 계정 강제 클라우드 (오프라인 원칙 훼손)

---

## 5. 경로 치트시트

| 무엇 | 경로 |
|------|------|
| 앱 루트 | `C:\Users\LSH\Bible App\korean-bible-app` |
| PM / 이 파일 | `docs\project-management\RESUME_HERE.md` |
| 출시 가이드 MD | `docs\project-management\PLAYSTORE_RELEASE_GUIDE_2026-08-10.md` |
| R1–R25 체크 | `docs\project-management\RELEASE_CHECKLIST_PLAYSTORE.md` |
| UX 백로그 | `docs\project-management\VALUE_AND_USABILITY.md` |
| 세션 로그 | `docs\project-management\SESSION_UPDATE_LOG.md` |
| PPTX (로컬) | `Desktop\Bible Project\KoreanBible_PlayStore_ReleaseGuide_2026-08-24.pptx` |
| Drive 프로젝트 | `H:\내 드라이브\Korean_Bible_App_Project 0526\` |
| gdrive MCP | `C:\Users\LSH\.grok\mcp-servers\gdrive-upload\` · config.toml 등록됨 |

---

## 6. 세션 시작 체크리스트 (에이전트용)

1. [ ] 이 파일(`RESUME_HERE.md`) 읽기  
2. [ ] `SESSION_UPDATE_LOG.md` 최신 블록 확인  
3. [ ] 사용자에게 Privacy URL·지원 이메일·개발자 계정 등 미결정 항목 확인 (없으면 Sprint B 병행 제안)  
4. [ ] 작업 후: SESSION 로그 맨 위 갱신 + 이 파일 §1·§3 상태 수정  
5. [ ] (선택) Linear/로드맵 PPTX 날짜 갱신 + `gdrive_upload_file`로 Drive 백업  

---

## 7. 체크포인트 스냅샷 (2026-09-29)

- [x] Play Store Phase 0–8 + Sprint A–D 문서화 (MD + Linear PPTX 15장)
- [x] PPTX → Desktop / docs / Drive(`roadmap-pptx/2026-08-24`) 저장
- [x] managed `google_drive`에 없던 **업로드** → 로컬 `gdrive_upload` MCP로 해결
- [x] 제품: 다역본·검증·PD 예배 콘텐츠 반영 (스토어 AAB는 미완)
- [x] packageId (com.lsh.koreanbible)
- [x] 업로드 키스토어 + release signingConfig (R7)
- [x] 서명 AAB uild\app\outputs\bundle\release\app-release.aab (R8)
- [ ] Privacy URL / Console 업로드 / 실기기(R11)
- [ ] 온보딩 · 역본 저장 · 절 복사 · 스크린샷

---

*이 파일이 “저장 지점”이다. 다음 작업은 여기서 시작한다.*
