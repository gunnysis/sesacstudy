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
│   └── alone/                  # 개인 프로젝트 (날짜 실습과 별개)
│       ├── eundunhealth-user-flow-diagram.ipynb  # Mermaid 사용자 플로우 다이어그램
│       ├── user-flow-diagram.png                 # 다이어그램 결과물
│       └── memo.md                               # 작업 메모 (Notion 참고)
│
├── memo/                       # 학습 메모
│   ├── memo.md                     # Git / 크롤링 / 라이브러리 등
│   └── azure.md                    # Azure 강의 자료 메모
├── CLAUDE.md                   # Claude Code 작업 가이드
├── .gitignore
└── README.md                   # (현재 파일)
```

> 대용량 데이터셋(CSV/JSON)은 git에 포함하지 않습니다. 데이터가 필요한 실습은
> 해당 `*-data/` 폴더의 README 안내에 따라 직접 배치하세요.

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

### alone — 개인 프로젝트 (은둔헬스)

- 날짜별 실습과 별개로 진행하는 개인 작업 공간
- **Mermaid** 로 헬스 앱 사용자 플로우 다이어그램 작성 → [mermaid.ink](https://mermaid.ink) 원격 API 로 이미지 렌더링
- `requests` + `Pillow` + `matplotlib` 만 사용 (별도 가상환경 없이 노트북 내 `%pip install` 로 설치)

학습 메모는 [memo/](memo/) 폴더 참고.

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
