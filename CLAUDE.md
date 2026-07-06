# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 성격

새싹(SeSAC) AI 부트캠프 **학습 저장소**입니다. 빌드 시스템·테스트 스위트·CI 가 없는,
Jupyter 노트북과 단발성 Python 스크립트의 모음입니다. "통과해야 할 테스트"가 아니라
"학습 내용이 재현되는지"가 정답 기준입니다. 코드를 수정하면 해당 노트북을 실제로
실행해 결과(셀 출력, 생성되는 HTML/PNG)가 의도대로 나오는지 확인하세요.

언어는 한국어 기준입니다. 주석·마크다운·커밋 메시지 모두 한국어로 맞춥니다.

## 구조 규칙 (핵심)

- 실습은 `MMDD/` (월일 4자리) 폴더 단위로 나뉘며, **각 날짜가 부트캠프 하루**에 대응합니다.
- `alone/` 은 날짜 실습과 별개인 **개인 프로젝트** 공간입니다(eundunhealth — 멘탈헬스 앱 mermaid 다이어그램, karaoke — 노래연습장 공공데이터 분석).
- 학습 메모는 `memo.md` 입니다(코드가 아닌 학습 노트).
- 프로젝트 README 는 **`README.md`** 하나로 통합돼 있습니다(루트에는 별도 README 없음). 새 실습 추가 시 [README.md](README.md) 의 디렉토리 구조와 학습 요약도 **함께 갱신**합니다.

### 외부에서 받아온 실습 패키지 (단순 MMDD 폴더와 다름)

일부 실습은 강사/공식 과정이 배포한 패키지를 통째로 받아온 것이라 **중첩된 `notebooks/`·`Labfiles/`·`data/` 구조와 자체 `.devcontainer`·`requirements.txt`** 를 가집니다. 이런 외부 클론은 **중복·혼란을 줄이기 위해** 다음 방침으로 정리합니다 — *임베디드 repo(중첩 `.git`)로 두지 않습니다.*

- **저장소 밖으로 이동(백업)**: `DL-Excersize/`(딥러닝 전이학습 — 우주 암석 분류). `moonrockmodel.pth` 등 대용량이고 upstream 에서 재현 가능하여 부모 저장소에 포함하지 않습니다.
- **내부 `.git` 만 제거해 평탄화 후 포함**: `mslearn-openai/`(Azure OpenAI 공식 실습), `mslearn-ai-agents/`(Azure AI 에이전트/Foundry 공식 실습). 중첩 `.git` 을 지워 일반 파일로 합치되, **가상환경(`labenv/`)·`__pycache__`·대용량 바이너리는 제외**합니다. ⚠ `Labfiles/**/Python/.env` 의 Azure 키·엔드포인트는 `.gitignore`(`*.env`)로 **반드시 제외** — 절대 커밋하지 마세요.
- `0610/Preprocessing-excersize-main/`(데이터 전처리)도 같은 평탄화 클론입니다.
- 이런 패키지는 노트북·데이터·`requirements.txt` 가 **MMDD 폴더가 아니라 패키지 루트** 기준으로 배치됩니다 — 환경 구성·경로도 패키지 루트를 기준으로 잡으세요.

## 의존성: 폴더별 격리 venv

전역 환경이 없습니다. 각 실습 폴더가 **자체 `requirements.txt` 와 `.venv/`** 를 가집니다
(`.venv/` 는 git 제외). 어떤 폴더의 노트북을 다루기 전에 그 폴더 기준으로 환경을 만듭니다.

```powershell
cd 0601           # 작업할 날짜 폴더
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- `requirements.txt` 가 없는 폴더(0522, 0528)는 인접 폴더(0527/0601)의 환경을 재사용하거나 필요한 패키지만 설치합니다.
- 평탄화 클론(`mslearn-openai/`, `mslearn-ai-agents/`, `0610/Preprocessing-excersize-main/`)은 `requirements.txt`·`.env` 가 **패키지/실습 하위 루트**에 있으니 그 위치에서 venv(`labenv/` 등, git 제외)를 만들고 키를 채웁니다. (`DL-Excersize/` 는 대용량이라 저장소 밖으로 이동됨)
- 0527 의 **Playwright** 동적 크롤링은 브라우저 바이너리가 추가로 필요합니다: `playwright install`
- 0611 의 **OpenCV**(`cv2`)는 `cv.imshow`/`cv.waitKey` 로 **GUI 창**을 띄우는 스크립트라 노트북이 아닌 `py` 실행 전제이며, `cv.imread()` 는 스크립트 위치가 아니라 **현재 작업 디렉토리(cwd)** 기준으로 경로를 찾습니다.
- `requirements.txt` 는 직접 손으로 편집하지 말고, 해당 폴더 venv 에서 `pip freeze > requirements.txt` 로 재생성합니다.

## 데이터 파일 규칙 (git 추적 제외)

대용량 데이터셋은 git 에 올리지 않습니다. `.gitignore` 가 이를 강제합니다:

- `**/*-data/*.csv`, `*.json` 은 무시, 단 같은 폴더의 `README.md` 는 추적(출처·배치 안내용).
- 데이터가 필요한 노트북은 `*-data/` 폴더 README 안내대로 사용자가 직접 파일을 배치하는 구조이므로,
  노트북이 데이터 경로에서 `FileNotFoundError` 를 내도 그것이 정상일 수 있습니다 — 임의로 데이터를 생성하지 말고 README 의 출처를 확인하세요.
- `study_docs_link/` (루트의 심볼릭 링크 → `…\공유내부문서_외부배포금지\새싹강의교안`)는 외부 배포 금지 강의교안이라 추적하지 않습니다(`.gitignore` 에 명시). **이 공유 폴더는 수시로 폴더명·계층이 재구성**되니, 경로를 문자열로 하드코딩하지 말고 그때그때 탐색하세요 — 한글 경로의 NFC/NFD 정규화 차이로 손으로 친 경로가 디스크와 안 맞을 수 있습니다(검색 시 ASCII 부분으로 필터하면 안전).

## 비밀키 관리 (재발방지)

이 저장소는 **public** 입니다. 절대 키·엔드포인트·토큰을 커밋하지 마세요.

- 키·엔드포인트·토큰은 **코드/노트북에 하드코딩 금지**. 각 폴더 `.env` 에 넣고 `os.getenv(...)` 로 읽습니다(`python-dotenv`). `.env` 는 `.gitignore`(`*.env`)로 전역 제외되며, 채울 변수 목록은 각 폴더 `.env.example` 참고.
- **커밋 전 시크릿 차단 훅**: `.githooks/pre-commit` 이 스테이징된 변경에서 Azure 키 시그니처·`sk-` 토큰·개인키 등을 탐지해 커밋을 막습니다. clone 후 한 번 활성화하세요 — `git config core.hooksPath .githooks` (오탐이면 `git commit --no-verify`).
- 노트북 **출력 셀**에도 키가 남을 수 있으니 커밋 전 출력을 지우거나 확인하세요.
- 이미 커밋된 키는 파일에서 지워도 **히스토리에 남습니다** — 유출 시 해당 키를 **Azure 포털에서 즉시 재발급(revoke)** 하고, 필요하면 히스토리 재작성으로 제거하세요.

## 환경

- **Windows + PowerShell**. 경로 구분자·활성화 스크립트(`.ps1`)·`py` 런처를 전제로 합니다.
- 노트북 편집은 NotebookEdit 도구를 사용하고, 출력 결과물(예: 0601 `map.html`, alone `user-flow-diagram.png`)은 노트북 재실행으로 갱신됩니다.
- 루트 `.vscode/` 는 기본적으로 `.gitignore` 제외지만, **안전한 설정 파일만 화이트리스트로 추적**합니다(`settings.json`·`tasks.json`·`open-external.ps1`·`extensions.json` — 절대경로·비밀 없이 상대경로만 사용해 어느 PC 에서나 clone 후 동작). 여기엔 심볼릭 링크 폴더(`study_docs_link/`)의 PDF 를 외부 앱으로 여는 자가 치유 태스크(`open-external.ps1` + `Ctrl+Alt+O`)가 들어 있습니다 — 동작·원리는 아래 "VSCode 설정 — 심볼릭 링크 폴더의 PDF 보기" 참고.
  - `.claude/`(Claude Code 로컬 설정)는 절대경로·자동승인 목록 등이 들어 있어 **의도적으로 git 제외**합니다 — 공유하지 마세요.

## VSCode 설정 — 심볼릭 링크 폴더의 PDF 보기

루트 `study_docs_link/` 는 워크스페이스 **바깥**(외부배포금지 강의교안)을 가리키는 심볼릭 링크입니다.
VSCode 의 PDF 뷰어 확장은 webview 보안 정책(`localResourceRoots`)상 워크스페이스 안의 파일만
로드할 수 있어, 이 폴더의 PDF 를 내장 뷰어로 열면 `Missing PDF`(PDF.js) 에러가 납니다. 이를 위해 루트 `.vscode/` 에 다음을 구성해 두었습니다.

- **`settings.json`** — `workbench.editorAssociations` 로 PDF 라우팅: `*.pdf` → `pdf.preview`(일반 PDF 는 내장 뷰어), `**/study_docs_link/**/*.pdf` → `default`(깨진 에러 대신 바이너리 안내 화면).
- **`tasks.json`** + **`open-external.ps1`** — `현재 파일 외부 앱으로 열기` 태스크(OS 기본 앱 실행). 경로가 죽었으면 같은 파일명을 현재 트리에서 (한글 NFC 정규화 비교로) 찾아 자동으로 여는 **자가 치유** 포함.
- **`%APPDATA%\Code\User\keybindings.json`**(사용자 전역) — `Ctrl+Alt+O` 단축키. `study_docs_link` 안의 `.pdf` 에서만 위 태스크 실행.

**사용법**: 심볼릭 링크 폴더의 PDF 클릭 → 안내 화면이 뜨면 `Ctrl+Alt+O` → 외부 앱에서 열림. 일반 PDF 는 평소대로 VSCode 안에서 보입니다.

> **단축키는 저장소에 따라오지 않습니다** — keybindings 정의는 `.vscode/` 가 아니라 사용자 전역 파일에 있어 git 동기화 안 됨. 새 PC 에서는 아래를 `%APPDATA%\Code\User\keybindings.json` 에 추가해야 동작합니다(태스크 자체는 `.vscode/` 로 따라옴).

```jsonc
// %APPDATA%\Code\User\keybindings.json
[
  {
    "key": "ctrl+alt+o",
    "command": "workbench.action.tasks.runTask",
    "args": "현재 파일 외부 앱으로 열기",
    "when": "resourceExtname == .pdf && resourcePath =~ /study_docs_link/"
  }
]
```
