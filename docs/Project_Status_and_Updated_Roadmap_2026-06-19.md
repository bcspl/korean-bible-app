# Korean Bible App Project - 종합 현황 및 로드맵 (Updated 2026-06-20)

## 프로젝트 개요
**완전 무료 오프라인 한국어 성경 앱**  
Public Domain 데이터(개역개정 등)를 사용하여 인터넷 없이도 성경을 읽고, 검색하고, 북마크/메모할 수 있는 크로스 플랫폼 앱입니다.

- **주요 목표**: 접근성(큰 글씨, 다크모드) 중심의 편리한 성경 읽기 경험 제공
- **기술 비전**: Flutter + Hive로 모든 플랫폼(Android, iOS, Web, Windows, macOS, Linux)에서 완전 오프라인 동작
- **데이터 출처**: Public Domain 한국어 성경 (개역개정 등)

## 현재 상태 (2026-06-27 기준)

### 완료된 작업
- Flutter 프로젝트 기본 구조 생성 및 다중 플랫폼 지원 준비 완료
- 의존성 설정: `hive`, `hive_flutter`, `path_provider`, `provider`, `hive_generator`, `build_runner`
- `assets/data/`에 성경 데이터 파일 배치 (`kor_bible_full.json`, `kor-korean.osis.xml`, 샘플)
- 기본 앱 스켈레톤 구현 (`lib/main.dart`)
  - Hive 초기화 + 어댑터 등록 (BibleVerse/Chapter/Book)
  - 한국어 제목 및 기본 테마 (indigo + 큰 글씨)
  - 하단 네비게이션 (성경 / 북마크 / 검색 placeholder)
- `flutter analyze` 클린 (lint 경고 해결 완료)
- Windows 데스크톱 빌드 성공 (`korean_bible_app.exe` 생성)
- 기존 테스트 업데이트 및 통과
- 불필요한 중복 `main.dart` 정리
- 프로젝트 문서 구조 생성 (docs/ 폴더)
- Phase 1 상세 구현: 데이터 모델 + Hive 어댑터 + JSON 로더 (BibleDataService) + 초기화/시드 완료
- 상세 일/주 단위 작업 분해 백로그에 반영 (Phase 1~5)

### 현재 코드 상태
- `lib/main.dart`: Hive init + 어댑터 + JSON 로더 호출 + 기본 HomeScreen (BookList로 진입)
- 데이터 구조: JSON (`version`, `books[]` → `chapters[]` → `verses[]`) + Hive 모델
- Phase 2: 기본 성경 읽기 UI (책 목록, 장 선택, 본문 뷰어 + 네비) 구현 진행/완료
- 검색: 한글/영문 책명 + 본문 검색 지원

### 문서 상태
- 본 로드맵: 2026-06-27 업데이트 (상세 작업 포함)
- `Task_Prioritized_Backlog_and_Schedule_2026-06-19.md`: 상세 Phase 1~5 일/주 단위 태스크로 확장
- `Feature_Specification_v2.md`: Placeholder
- `bible_data_parser_and_instructions.md`: Placeholder

## 기술 스택 및 설계 결정
- **프레임워크**: Flutter (크로스 플랫폼)
- **로컬 저장소**: Hive (NoSQL, 빠른 쿼리, 오프라인 최적화)
- **상태 관리**: Provider (간단하고 충분)
- **UI**: Material Design + 접근성 고려 (폰트 크기, 다크모드)
- **데이터 포맷**: JSON (현재) → 필요시 OSIS 파서 연동
- **에셋**: `assets/data/` 전체 등록 (성경 전체 데이터 번들)

향후 고려:
- 큰 데이터 파일 최적화 (lazy load, 인덱싱)
- 추가 의존성: `shared_preferences` (설정), `intl` (날짜)

## 개발 단계 (Phase) 및 마일스톤

### Phase 0: 기반 구축 (완료)
- 프로젝트 초기화, 의존성, 기본 스켈레톤, 데이터 파일 배치, 빌드 환경 검증
- **상태**: 완료

### Phase 1: 데이터 계층 구현 (최우선 - MVP 기반)
- 성경 데이터 모델 정의 (BibleBook, Chapter, Verse 등)
- Hive 어댑터 생성 (`hive_generator` + `build_runner`)
- JSON 파서 구현 (샘플 → 전체 데이터)
- 앱 시작 시 데이터 로드 및 Hive에 시드
- 성능 테스트 (7MB+ JSON 로딩 시간)
- **목표 산출물**: "성경 데이터가 앱에서 사용 가능" 상태

### Phase 2: 핵심 읽기 기능 (MVP)
- 책 목록 화면 (구약/신약 분류)
- 장 선택 및 절 목록 뷰
- 성경 본문 뷰어 (스크롤, 큰 글씨)
- 기본 네비게이션 (이전/다음 장, 책 이동)
- 현재 읽기 위치 저장 (간단한 설정)
- **목표 산출물**: 사용자가 실제로 성경을 읽을 수 있는 앱

### Phase 3: 사용자 중심 기능
- 북마크 (Hive 저장)
- 하이라이트 + 메모/기도장
- 텍스트 검색 (책/장/본문)
- 설정 화면 (글꼴 크기, 테마, 버전 선택)
- 하단 네비게이션 실제 연결
- **목표 산출물**: 실사용 가능한 일상 앱

### Phase 4: UI/UX 고도화 및 접근성
- 반응형 디자인 (모바일/데스크톱)
- 다크모드 완성 및 커스텀 테마
- 큰 글씨 / 접근성 감사
- 애니메이션 및 부드러운 네비게이션
- 에러 처리 및 로딩 상태
- **목표 산출물**: 품질 높은 사용자 경험

### Phase 5: 크로스 플랫폼 완성 및 배포
- Android / iOS 빌드 및 테스트
- Web 배포 (PWA)
- Windows/macOS/Linux 데스크톱 최적화
- 앱 아이콘, 스플래시, 릴리스 설정
- Google Play / App Store / Microsoft Store 준비
- **목표 산출물**: 실제 사용자에게 배포 가능한 제품

### Phase 6: 고급 기능 및 유지보수 (미래)
- 오디오 성경 (TTS 또는 미리 녹음)
- 여러 성경 번역 지원
- 클라우드 동기화 (선택적, Google Drive 등)
- 통계/읽기 진도 추적
- 커뮤니티 기능 (주석 공유 등)
- 지속적인 데이터 업데이트 파이프라인

## 주요 리스크 및 대응
- **대용량 데이터**: 7MB JSON → Phase 1에서 인덱싱/부분 로드 전략 수립
- **모바일 성능**: Hive + 효율적인 쿼리로 해결
- **데이터 정확성**: Public Domain 데이터 검증 필요 (다운로더 스크립트 활용)
- **플랫폼 차이**: Flutter의 장점 활용하되, 데스크톱 특화 UI 별도 고려
- **문서 부재**: 백로그와 스펙 문서를 Phase 1 초기에 실제 내용으로 채우기

## 업데이트 이력
- **2026-06-19**: 초기 프로젝트 생성, 문서 placeholder 작성
- **2026-06-20**: 전체 분석 후 본 로드맵 상세 작성. Phase 구조화, 현재 상태 업데이트, 기술 결정 기록. 기본 앱 스켈레톤 및 빌드 성공 반영.
- **2026-06-27**: 상세 일/주 단위 작업 분해 (Phase 1~5) 백로그에 반영. roadmap-pptx 스킬 재실행으로 PPTX 업데이트. Phase 1 (모델+어댑터+JSON 로더) 완료, Phase 2 UI 진행 중.

## 참고 문서
- `Task_Prioritized_Backlog_and_Schedule_2026-06-19.md` (우선순위 백로그)
- `Feature_Specification_v2.md`
- `bible_data_parser_and_instructions.md`
- `pubspec.yaml`
- `README.md`, `README_Source_Code.md`

---

**다음 단계**: 이 로드맵에 기반한 구체적인 작업 순서는 별도 제안 문서 또는 백로그에 정리합니다. (아래 응답 참조)