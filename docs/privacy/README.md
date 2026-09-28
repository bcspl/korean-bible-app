# 개인정보처리방침 호스팅 (GitHub Pages)

| 파일 | 용도 |
|---|---|
| `privacy-policy.md` | 원문 (한국어 + English). 수정은 여기서 먼저 |
| `index.html` | GitHub Pages로 게시할 정적 페이지 (md 내용과 동일하게 유지) |

게시 전 채워야 할 자리표시자: `[개발자 이름]` · `[지원 이메일]` · `[게시일]` · `[시행일]` (영문 섹션의 `[Developer name]` 등 포함). `privacy-policy.md`와 `index.html` **둘 다** 수정하세요.

## 방법 A — `main` 브랜치 `/docs` 폴더 (권장 · 가장 간단)

1. GitHub → `bcspl/korean-bible-app` → **Settings → Pages**
2. **Build and deployment → Source: Deploy from a branch**
3. **Branch: `main`**, 폴더 **`/docs`** → **Save**
4. 1–2분 후 게시 URL:

```
https://bcspl.github.io/korean-bible-app/privacy/
```

주의:
- `/docs` 폴더 전체가 웹으로 공개됩니다 (예: `docs/project-management/*.md`, PPTX). 저장소가 이미 공개(public)라 노출 범위는 동일하지만, 비밀정보(키·비밀번호)는 절대 `docs/`에 두지 마세요.
- 기본적으로 Jekyll이 `.md`도 페이지로 변환합니다. 원치 않으면 빈 파일 `docs/.nojekyll`을 추가하세요 (`index.html`은 그대로 동작).

## 방법 B — `gh-pages` 브랜치 (개인정보 페이지만 공개)

```powershell
cd "C:\Users\LSH\Bible App\korean-bible-app"
git switch --orphan gh-pages
git rm -rf --cached . 2>$null
# 작업 트리에서 docs\privacy\index.html 만 privacy\index.html 로 복사 후
git add privacy/index.html
git commit -m "Publish privacy policy"
git push origin gh-pages
git switch main
```

Settings → Pages → Branch: **`gh-pages`**, 폴더 **`/ (root)`** → 동일 URL `https://bcspl.github.io/korean-bible-app/privacy/`

(주의: orphan 브랜치 전환 시 작업 트리의 미추적 파일 상태를 먼저 확인하세요.)

## 게시 후

1. 브라우저에서 URL 열어 확인 (모바일 포함)
2. Play Console → **정책 → 앱 콘텐츠 → 개인정보처리방침**에 URL 입력
3. 스토어 등록정보의 개인정보처리방침 링크에도 동일 URL
4. 앱 내부(설정/정보 화면)에도 방침 텍스트 또는 링크 추가 (Play 사용자 데이터 정책)
