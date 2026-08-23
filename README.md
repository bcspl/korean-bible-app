# 한국어 성경 앱 (korean-bible-app)

완전 **무료 · 오프라인** 성경·예배 보조 앱.  
**Public Domain** 데이터만 사용합니다. **개역개정(NKRV) 미수록.**

## 역본

| 코드 | 이름 | 비고 |
|------|------|------|
| **KRV** | 개역한글 | 성경전서 개역한글판 계열 PD · 기본 |
| **KJV** | King James Version | PD (미국 기준) |
| **ASV** | American Standard Version 1901 | PD |

- 절 화면에서 **최대 3개 역본**을 동시에 볼 수 있습니다.
- 본문 검증: `python scripts/verify_bible_texts.py`

## 주요 기능

- 성경 66권 읽기 · 검색 · 북마크 · 구약/신약 필터  
- 찬송가 (PD, 한/영 가사, 유래·라이선스, 교육용 악보)  
- 예배 자료: 사도신경 · 주기도문(기도 본문만) · 교독문(시편·성탄·부활 등)  
- 다크 모드 · 글자 크기 · 고대비  

## 빠른 시작

```powershell
cd "C:\Users\LSH\Bible App\korean-bible-app"
flutter pub get
flutter run
flutter test
```

## 데이터 재생성 (선택)

```powershell
python scripts/download_pd_bibles.py          # KJV / ASV
python scripts/build_pd_hymn_catalog.py       # 찬송
python scripts/generate_hymn_scores.py
python scripts/build_responsive_readings.py   # 교독문 참조
python scripts/verify_bible_texts.py          # 본문 검증
```

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PROJECT_REPORT_2026-08-10.md](docs/PROJECT_REPORT_2026-08-10.md) | **종합 보고서 · 권장사항** |
| [docs/APPLIED_AND_ROADMAP_PLAN_2026-08-10.md](docs/APPLIED_AND_ROADMAP_PLAN_2026-08-10.md) | **현재 적용 vs 향후 계획** (사용성·가치) |
| [docs/project-management/](docs/project-management/) | **PM 구조** · 11월 스토어 · 세션 로그 |
| [docs/STATUS_REPORT_2026-08-10.md](docs/STATUS_REPORT_2026-08-10.md) | 최신 상태 |
| [docs/DEPLOY_CHECKLIST.md](docs/DEPLOY_CHECKLIST.md) | 배포 체크리스트 |
| [docs/Project_Status_and_Updated_Roadmap_2026-06-19.md](docs/Project_Status_and_Updated_Roadmap_2026-06-19.md) | 로드맵 |
| [CHANGELOG.md](CHANGELOG.md) | 변경 이력 |

## 라이선스 고지 (요약)

- **KRV:** 성경전서 개역한글판 (대한성서공회) — 저작재산권 만료 PD. 동일성·출처 표기 권장.  
- **KJV / ASV:** Public Domain (배포 지역별 관행 확인).  
- **찬송·교독:** 앱 자체 PD 선별·구성. 한국찬송가공회 공식 판권과 **무관**.  
- **악보 SVG:** 교육용 간소화 · 공식 악보 아님.

## 프로젝트 상태 (2026-08-10)

- 콘텐츠·다역본·검증: 완료  
- 스토어 배포: 패키지 ID·서명·리스팅 대기  
- 테스트: `flutter test` 5/5  

---

산출물 동기화: Google Drive Korean_Bible_App_Project 등 (기존 운영 방식 유지)
