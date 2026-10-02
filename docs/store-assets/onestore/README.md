# 원스토어 등록 자산 (초안) — 2026-10-03

가이드: [`../../project-management/ONESTORE_RELEASE_GUIDE.md`](../../project-management/ONESTORE_RELEASE_GUIDE.md) · 규격 출처: https://onestore-dev.gitbook.io/dev/docs/apps/product/android/app-info

| 파일 | 규격 (원스토어) | 실제 |
|------|----------------|------|
| `icon_512.png` | 512×512 JPG/PNG | 512×512 PNG RGBA(32-bit) · 115 KB · `assets/icon/icon.png`(1024²)를 LANCZOS로 축소 |
| `banner_1024x578.png` | 그래픽 이미지 1024×578 JPG/PNG | **확정 (2026-10-03 사용자 선택)**. 앱 아이콘 색(인디고 #44477A, 골드 #C9A961, 아이보리 바탕) · Gothic A1 Light/Thin(OFL) · 로고/상표 없음 · 22 KB |
| `screenshots/01~06_*.png` | 2~8장, 장당 ≤1 MB, ≤1300×1300, 권장 720×1280 | 6장 · 720×1280 PNG · 69~128 KB |
| `listing_ko.md` | 제목 ≤50 · 한 줄 ≤100 · 상세 ≤1,300 · 키워드 1~10 | 21자 · 62자 · 685자 · 10개 |

## 스크린샷 순서
1. `01_bible_reading` — 시편 1편, 개역한글 단독 읽기
2. `02_version_switch_krv_kjv_asv` — 창세기 1장, 개역한글·KJV·ASV 3역본 대조
3. `03_hymns` — 찬송가 목록 (102곡, Public Domain)
4. `04_responsive_reading` — 교독문 1 "복 있는 사람" (인도자/회중)
5. `05_lords_prayer` — 주기도문
6. `06_settings_dark_mode` — 설정 · 다크 모드 켬

## 촬영 방법 / 주의
- 같은 코드로 `flutter build web --release`를 만들고, 헤드리스 Chrome(Playwright)에서 360×640, 배율 2로 캡처했습니다. Android 실기기 화면이 아닙니다.
- 실제 Android에서는 시스템 글꼴, 상태바, 내비게이션 바가 조금 다르게 보일 수 있습니다. 화면 구성과 기능은 같습니다.
- 실기기 화면으로 바꾸려면 같은 화면을 캡처한 뒤 720×1280으로 리사이즈하고 1 MB 이하로 저장하면 됩니다.
