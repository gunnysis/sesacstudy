# sesac_dev

새싹(SeSAC) AI 부트캠프 학습 통합 저장소.
일자별 실습 코드와 학습 메모를 한 곳에서 관리합니다.

---

## 디렉토리 구조

```text
sesac_dev/
├── sesacstudy/                 # 일자별 실습 코드 (MMDD 형식)
│   ├── 0522/                   # 수학·시각화
│   │   ├── equation.py             # SymPy 연립방정식 풀이
│   │   ├── systemsOfEquations.py   # matplotlib 3D 그래프 (인바디 추이)
│   │   └── test.ipynb
│   ├── 0527/                   # Python 기초 + 웹 크롤링
│   │   ├── hello.ipynb             # Python 기본 문법
│   │   ├── web_crolling1.ipynb     # 정적 크롤링 (requests + BeautifulSoup)
│   │   ├── web_crolling2.ipynb     # 정적 크롤링 심화
│   │   ├── playwright-scrapping.py # 동적 크롤링 (Playwright)
│   │   └── requirements.txt
│   ├── 0528/                   # 데이터 분석 기초
│   │   ├── numpy-exercise.ipynb
│   │   ├── pandas-exercise.ipynb
│   │   ├── matplotlib-exercise.ipynb
│   │   └── seaborn-exercise.ipynb
│   ├── 0601/                   # 시각화 심화 + 시계열
│   │   ├── seaborn-exercise.ipynb
│   │   ├── timeseries-exercise.ipynb  # 시계열 (relativedelta 등)
│   │   ├── polium-exercise.ipynb      # folium 지도 시각화
│   │   ├── map.html                   # folium 결과물
│   │   ├── 병원정보.txt               # folium 실습용 병원 좌표 데이터 (git 미포함, 로컬 전용)
│   │   └── requirements.txt
│   ├── 0610/                   # 데이터 전처리 실습 (클론: Preprocessing-excersize)
│   │   └── Preprocessing-excersize-main/
│   │       └── notebooks/          # 02.x 정제·집계·결합·분할 / 03.x 수치·범주·날짜·GIS, CustomVision
│   ├── 0611/                   # OpenCV 이미지 처리
│   │   ├── cv_study.py             # 이진화(Otsu threshold) 등 OpenCV 실습
│   │   ├── assets/                 # 실습용 이미지 (RGB·soccer 등)
│   │   ├── memo.md                 # OpenCV 실습 메모
│   │   └── requirements.txt
│   ├── 0615/                   # 분류 실습용 데이터셋
│   │   └── adult.csv               # UCI Adult(Census Income) — 연소득 >50K 분류용
│   ├── mslearn-openai/         # Azure OpenAI 공식 실습 (클론 평탄화 — 내부 .git 제거)
│   │   ├── Instructions/Exercises/  # 01~06 실습 가이드
│   │   ├── Labfiles/                # 실습 코드(Python·C#) + 데이터(brochures·자체데이터 RAG 등)
│   │   └── readme.md                # ⚠ Labfiles/**/Python/.env(Azure 키)는 .gitignore 제외
│   ├── mslearn-ai-agents/      # Azure AI 에이전트(Foundry) 공식 실습 (클론 평탄화)
│   │   ├── Instructions/Exercises/  # 에이전트 구축·MCP·오케스트레이션·A2A 등
│   │   └── Labfiles/                # 실습 코드 (venv labenv/ 는 제외)
│   └── alone/                  # 개인 프로젝트 (날짜 실습과 별개)
│       ├── eundunhealth-user-flow-diagram.ipynb  # 멘탈헬스 앱 Mermaid 사용자 플로우
│       ├── karaoke_data_analyze.ipynb            # 노래연습장 인허가 공공데이터 분석
│       ├── assets/                 # 결과물 (user-flow-diagram.png 등)
│       ├── docs/                   # 메모·약관·통계 문서 + 분석용 CSV
│       └── requirements.txt
│
├── study_docs_link/            # 외부 강의교안 심볼릭 링크 (미추적·외부배포금지, ↓ VSCode 설정 참고)
├── memo.md                     # 학습 메모 (Git / 크롤링 / 라이브러리 등)
├── azure.md                    # Azure 강의 자료 메모
├── error_report.md             # 작업 중 오류·해결 기록
├── .vscode/                    # 에디터 설정 (PDF 라우팅·외부 열기 태스크 등)
├── CLAUDE.md                   # Claude Code 작업 가이드
├── .gitignore
└── README.md                   # (현재 파일)
```

> 대용량 데이터셋(CSV/JSON)은 git에 포함하지 않습니다. 데이터가 필요한 실습은
> 해당 `*-data/` 폴더의 README 안내에 따라 직접 배치하세요.
>
> **외부 클론 정리** (중복·혼란 방지):
> - `DL-Excersize/`(딥러닝 전이학습) → 대용량(`moonrockmodel.pth` 등)이라 저장소 **밖으로 이동(백업)**.
> - `sesacstudy/mslearn-openai/`(Azure OpenAI), `sesacstudy/mslearn-ai-agents/`(Azure AI 에이전트) → 내부 `.git` 만 제거해 **일반 파일로 평탄화**하여 포함. 단 가상환경(`labenv/`)·캐시·대용량 바이너리는 제외.
> - `sesacstudy/0610/Preprocessing-excersize-main/` → 이미 평탄화된 클론(자체 `.devcontainer`·`requirements.txt` 포함).
>
> ⚠ **비밀키 주의**: 클론들의 `Labfiles/**/Python/.env`(Azure 키·엔드포인트)는 `.gitignore`(`*.env`)로 반드시 제외됩니다 — 커밋 금지.

---

## 학습 내용 요약

### 0522 — 수학·시각화

- **SymPy** 로 연립방정식 풀이 (`solve([ex1, ex2])`)
- **matplotlib** 3D 플롯으로 시계열 데이터(인바디 측정값) 시각화

### 0527 — Python 기초 + 웹 크롤링

- 입출력 / 제어문 / 함수 / 클래스 / 람다 / `map`·`filter`·`zip`·`enumerate`
- 파일 입출력: **JSON**, **CSV**, 정규표현식(`re`)
- HTTP 통신: **requests** + JSONPlaceholder
- 정적 페이지 크롤링: **BeautifulSoup4**
- 동적 페이지 크롤링: **Playwright** (네이버 검색·금융뉴스 추출)

### 0528 — 데이터 분석 기초

- **NumPy** 배열 연산 / **pandas** 데이터프레임 처리
- **matplotlib** · **seaborn** 기본 시각화

### 0601 — 시각화 심화 + 시계열

- **seaborn** 통계 시각화 심화
- **시계열** 데이터 처리 (`dateutil.relativedelta` 등)
- **folium** 지도 시각화 (`map.html` 결과물, `병원정보.txt` 병원 좌표 데이터 사용)

### 0610 — 데이터 전처리 실습

- 외부 실습 패키지(`Preprocessing-excersize`) 기반
- **데이터 정제·가공**: 선택(Selection) / 집계(Aggregation) / 결합(Join) / 분할(Split) / 생성(Generate) / 전개(Spread)
- **타입별 전처리**: 수치(Number) / 범주(Category) / 날짜시간(DateTime) / 지리정보(GIS)
- **Azure Custom Vision**: 이미지 분류 · 객체 탐지(`objectdetection.ipynb`) 실습

### 0611 — OpenCV 이미지 처리

- **OpenCV**(`cv2`) 로 이미지 읽기·이진화(Otsu threshold)·표시
- `cv.imread()` 는 **현재 작업 디렉토리(cwd)** 기준으로 경로를 찾음에 유의 (스크립트 위치 아님)

### 0615 — 분류 실습용 데이터셋

- **UCI Adult (Census Income)** 데이터셋(`adult.csv`) — 인구통계 특성으로 연소득 `>50K` 여부 분류
- 현재는 데이터만 보관 (실습 노트북은 추후 추가)

### Azure AI 실습 — mslearn-openai · mslearn-ai-agents

- **mslearn-openai**: Microsoft 공식 Azure OpenAI 실습([MicrosoftLearning/mslearn-openai](https://github.com/MicrosoftLearning/mslearn-openai)) 클론을 평탄화(내부 `.git` 제거)
  - `Instructions/Exercises/` 01~06 가이드 + `Labfiles/` Python·C# 코드 (앱 개발 · 프롬프트 엔지니어링 · 코드 생성 · 이미지 생성 · 자체 데이터 RAG)
  - '자체 데이터(RAG)' 실습 보조 자료(`IT_Policy.txt`·`system_performance.csv`)는 `Labfiles/02-use-own-data/data/microsoftlearning/` 에 포함
- **mslearn-ai-agents**: Microsoft 공식 Azure AI 에이전트(Foundry) 실습 클론을 평탄화
  - 에이전트 구축 · 커스텀 도구 · MCP 통합 · 오케스트레이션 · A2A 등 (`Labfiles/`, venv `labenv/` 는 제외)
- ⚠ 모든 클론의 **Azure 키·엔드포인트(`.env`)는 `.gitignore` 로 제외** — 실습 시 본인 값으로 채워 사용

### alone — 개인 프로젝트

- 날짜별 실습과 별개로 진행하는 개인 작업 공간 (`assets/` 결과물 · `docs/` 문서·데이터)
- **은둔헬스(멘탈헬스 앱)**: **Mermaid** 로 사용자 플로우 다이어그램 작성 → [mermaid.ink](https://mermaid.ink) 원격 API 로 렌더링
- **노래연습장 데이터 분석**(`karaoke_data_analyze.ipynb`): 서울시 양천구 노래연습장 인허가 공공데이터 분석
- 사용 패키지는 `requirements.txt` 참고

학습 메모는 루트의 [memo.md](memo.md) · [azure.md](azure.md) 참고.

---

## 환경 설정

각 실습 폴더는 자체 `requirements.txt` 와 격리된 가상환경을 사용합니다.

```powershell
cd sesacstudy/0601
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Playwright 사용 시(0527) 브라우저 바이너리도 함께 설치합니다.

```powershell
playwright install
```

---

## VSCode 설정 — 심볼릭 링크 폴더의 PDF 보기

`study_docs_link/` 는 워크스페이스 **바깥**(외부배포금지 강의교안)을 가리키는 심볼릭 링크입니다.
VSCode 의 PDF 뷰어 확장은 webview 보안 정책(`localResourceRoots`)상 워크스페이스 안의 파일만
로드할 수 있어, 이 폴더의 PDF 를 내장 뷰어로 열면 `Missing PDF` (PDF.js) 에러가 납니다.

이를 위해 `.vscode/` 에 다음을 구성해 두었습니다.

- **`.vscode/settings.json`** — `workbench.editorAssociations` 로 PDF 라우팅
  - `*.pdf` → `pdf.preview` (일반 PDF 는 VSCode 내장 뷰어로 표시)
  - `**/study_docs_link/**/*.pdf` → `default` (깨진 PDF.js 에러 대신 바이너리 안내 화면)
- **`.vscode/tasks.json`** + **`.vscode/open-external.ps1`** — `현재 파일 외부 앱으로 열기` 태스크
  (OS 기본 앱으로 실행. 경로가 죽었으면 같은 파일명을 현재 트리에서 찾아 자동으로 여는 **자가 치유** 포함)
- **`%APPDATA%\Code\User\keybindings.json`** (사용자 전역) — `Ctrl+Alt+O` 단축키
  - `study_docs_link` 안의 `.pdf` 에서만 위 태스크를 실행

**사용법**: 심볼릭 링크 폴더의 PDF 클릭 → 안내 화면이 뜨면 `Ctrl+Alt+O` → 외부 앱(브라우저/Acrobat)에서 열림.
일반 PDF 는 평소대로 VSCode 안에서 바로 보입니다. (VSCode 구조상 클릭 즉시 자동 외부 실행은 불가능하여 단축키 한 번 방식)

> 특정 브라우저로 강제하려면 `tasks.json` 의 `args` 마지막 항목을 `"Start-Process msedge.exe -ArgumentList '${file}'"` 로 변경.
> 단축키를 모든 PDF 에 적용하려면 keybindings 의 `when` 에서 `&& resourcePath =~ /study_docs_link/` 제거.

**경로가 바뀌어도 자가 치유됩니다.** `study_docs_link` 가 가리키는 공유 강의자료 폴더는
수시로 재구성(폴더명 변경·계층 이동)됩니다. VSCode 세션 복원으로 떠 있는 옛 PDF 탭은 파일이
이동하면 내장 뷰어에서 `Missing PDF` 가 납니다. 이때 `Ctrl+Alt+O` 를 누르면 `open-external.ps1`
이 죽은 경로를 감지하고 **같은 파일명을 현재 트리에서 (한글 NFC 정규화 비교로) 찾아 자동으로**
외부 앱에 엽니다. 동명 파일도 못 찾으면 탐색기로 현재 트리를 열어 직접 찾도록 합니다.

### 다른 PC 에서 재사용하기 (중요)

`.vscode/` 는 기본적으로 git 제외지만, 재사용을 위해 **안전한 설정 파일만** 추적합니다
(`.gitignore` 에서 `settings.json`·`tasks.json`·`open-external.ps1`·`extensions.json` 만 화이트리스트).
이 파일들은 절대경로·비밀 없이 상대경로(`${workspaceFolder}`, `$PSScriptRoot`)만 쓰므로
clone 하면 어느 PC 에서나 그대로 동작합니다.

> **단, `Ctrl+Alt+O` 단축키는 따라오지 않습니다.** 단축키 정의는 저장소가 아니라 **사용자 전역**
> 파일(`%APPDATA%\Code\User\keybindings.json`)에 있어 git 으로 동기화되지 않습니다.
> 새 PC 에서는 그 파일에 아래를 추가해야 단축키가 동작합니다(태스크 자체는 `.vscode/` 로 따라옴).

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

> `.claude/` (Claude Code 로컬 설정)는 절대경로·자동승인 목록 등이 들어 있어 **의도적으로 git 제외**합니다 — 공유하지 마세요.

---

## 새 실습 추가 규칙

- 새 실습은 `sesacstudy/MMDD/` 폴더를 만들어 추가합니다.
- 각 실습 폴더는 자체 `requirements.txt` 와 `.venv/` 를 유지합니다 (의존성 격리).
- `venv/`, `.venv/`, `.claude/`, `__pycache__/`, `.ipynb_checkpoints/` 등은 `.gitignore` 로 제외됩니다.
- 대용량 데이터(CSV/JSON)는 git에 올리지 않고, `*-data/` 폴더에 README로 출처·배치 방법을 남깁니다.
- 폴더·파일 추가 시 이 README 의 디렉토리 구조도 함께 업데이트합니다.

---

## 참고

- GitHub: `gunnysis/sesac_dev`
- 학습 과정: 새싹(SeSAC) AI 부트캠프
