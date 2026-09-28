# 세션 업데이트 로그

**용법:** 매 작업 종료 시 **맨 위에** 새 블록 추가 (최신순).  
**재개:** [`RESUME_HERE.md`](./RESUME_HERE.md) 를 다음 세션 시작점으로 사용.

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
