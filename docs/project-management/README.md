# 프로젝트 관리 구조 (Project Management)

**목표 일정:** 2026-11 Play Store 공개  
**갱신 방식:** 매 작업 세션 종료 시 아래 파일을 순서대로 업데이트

---

## 🚀 다음 세션 시작

**무조건 먼저 읽기:** [`RESUME_HERE.md`](./RESUME_HERE.md)

작업 재개 프롬프트 예:

```text
docs/project-management/RESUME_HERE.md 읽고 이어서 작업해줘.
```

계획·절차 상세: [`PLAYSTORE_RELEASE_GUIDE_2026-08-10.md`](./PLAYSTORE_RELEASE_GUIDE_2026-08-10.md)  
공유용 PPTX: `Desktop/Bible Project/KoreanBible_PlayStore_ReleaseGuide_2026-08-24.pptx` (Linear 스타일)

---

## 폴더 구조

```
docs/project-management/
  RESUME_HERE.md            ← ★ 체크포인트 / 다음 세션 시작점
  README.md                 ← 이 파일 (운영 규칙)
  VISION_AND_PLAN.md        ← 비전 · 전체 계획 · 마일스톤
  RELEASE_CHECKLIST_PLAYSTORE.md  ← 공개 전 필수 과제 (R1–R25)
  PLAYSTORE_RELEASE_GUIDE_*.md    ← 출시 절차 상세 + 향후 작업
  SESSION_UPDATE_LOG.md    ← 세션별 작업 로그 (누적)
  VALUE_AND_USABILITY.md    ← 가치·사용성 백로그
  generate_*_pptx.py        ← 보고서 PPTX 생성 스크립트
```

## 매 작업 후 업데이트 순서 (5분)

1. **SESSION_UPDATE_LOG.md** — 오늘 한 일 / 막힌 일 / 다음 1건  
2. **RESUME_HERE.md** — §1 상태 · §3 다음 할 일 · §7 체크리스트  
3. **VALUE_AND_USABILITY.md** — 완료 항목 체크  
4. **RELEASE_CHECKLIST_PLAYSTORE.md** — 공개 전 항목 상태 변경  
5. **VISION_AND_PLAN.md** — Last updated · 진행률 %  
6. (선택) PPTX 재생성 → `Desktop/Bible Project/` + Drive `gdrive_upload`

## 상태 기호

| 기호 | 의미 |
|------|------|
| ✅ | 완료 |
| 🔄 | 진행 중 |
| ⏳ | 대기 |
| ⏸ | 보류 |
| ⛔ | 차단 (외부 의존 / 사용자 결정) |

## 산출물 위치

| 종류 | 경로 |
|------|------|
| 앱 소스 | `C:\Users\LSH\Bible App\korean-bible-app` |
| 로컬 보고서 PPTX | `Desktop\Bible Project\` |
| Git 문서 | `docs/` · `docs/project-management/` |
| Drive 백업 | `H:\내 드라이브\Korean_Bible_App_Project 0526` |
| Drive 업로드 MCP | `~/.grok/mcp-servers/gdrive-upload` (`gdrive_upload_*` 도구) |
