# sesac_dev

새싹(SeSAC) AI 부트캠프 학습 통합 저장소.
일자별 실습 코드, 강의 교안 PDF, Python 가상환경 셋업 노트를 한 곳에서 관리합니다.

---

## 디렉토리 구조

```
sesac_dev/
├── sesacstudy/                 # 일자별 실습 코드 (MMDD 형식)
│   ├── 0522/                   # 5월 22일 실습
│   │   ├── equation.py             # SymPy 를 이용한 연립방정식 풀이
│   │   ├── systemsOfEquations.py   # matplotlib 3D 그래프 (인바디 추이 시각화)
│   │   └── test.ipynb
│   └── 0527/                   # 5월 27일 실습 (Python 기초 + 웹 크롤링)
│       ├── README.md
│       ├── requirements.txt        # 0527 실습용 패키지 목록
│       ├── hello.ipynb             # Python 기본 문법 실습
│       ├── web_crolling1.ipynb     # 정적 페이지 크롤링 (requests + BeautifulSoup)
│       ├── web_crolling2.ipynb     # 정적 페이지 크롤링 심화
│       └── playwright-scrapping.py # 동적 페이지 크롤링 (Playwright)
│
├── virtualenv/                 # Python 3.10 기반 격리 가상환경
│   ├── venv/                       # (gitignore 대상)
│   └── README.md                   # 가상환경 셋업 절차 문서
│
│
├── memo.md                     # 학습 메모 (크롤링 라이브러리, winget 명령어 등)
├── git clone with personal access token.pdf
├── .gitignore
└── README.md                   # (현재 파일)
```

---

## 학습 내용 요약

### 0522 — 수학·시각화
- **SymPy** 로 연립방정식 풀이 (`solve([ex1, ex2])`)
- **matplotlib** 3D 플롯으로 시계열 데이터 (인바디 측정값) 시각화

### 0527 — Python 기초 + 웹 크롤링
- 입출력 / 제어문 / 함수 / 클래스 / 람다 / `map` · `filter` · `zip` · `enumerate`
- 파일 입출력: **JSON**, **CSV**, 정규표현식(`re`)
- HTTP 통신: **requests** + JSONPlaceholder
- 정적 페이지 크롤링: **BeautifulSoup4**
- 동적 페이지 크롤링: **Playwright** (네이버 검색·금융뉴스 추출)

크롤링 관련 메모는 [memo.md](memo.md) 참고.

---

## 환경 설정

### 1. 일자별 실습 환경 (sesacstudy/MMDD)

각 실습 폴더는 자체 `requirements.txt` 와 격리된 venv 를 사용합니다.

```powershell
cd sesacstudy/0527
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Playwright 사용 시 브라우저 바이너리도 함께 설치합니다.

```powershell
playwright install
```

### 2. 데이터 분석용 공용 가상환경 (virtualenv/)

`numpy 1.21.6` + `pandas 1.3.5` 조합을 Python 3.10 으로 고정한 환경입니다.
상세 셋업 절차는 [virtualenv/README.md](virtualenv/README.md) 를 참고하세요.

---

## 주요 패키지 (0527 실습 기준)

| 분류 | 패키지 |
|------|--------|
| HTTP / 파싱 | `requests`, `beautifulsoup4`, `lxml` |
| 동적 크롤링 | `playwright`, `selenium` |
| 데이터 처리 | `numpy`, `pandas`, `openpyxl` |
| 시각화 | `matplotlib`, `pillow`, `wordcloud` |
| 한국어 NLP | `konlpy`, `jpype1` |
| 노트북 | `ipykernel`, `ipywidgets`, `jupyter_client` |
| 수식 | `sympy` |

전체 목록은 [sesacstudy/0527/requirements.txt](sesacstudy/0527/requirements.txt) 참조.

---

## 새 실습 추가 규칙

- 새 실습은 `sesacstudy/MMDD/` 폴더를 만들어 추가합니다.
- 각 실습 폴더는 자체 `requirements.txt` 와 `venv/` 를 유지합니다 (의존성 격리).
- `venv/`, `.venv/`, `.claude/`, `__pycache__/`, `.ipynb_checkpoints/` 등은 `.gitignore` 로 제외됩니다.
- 교안 PDF 는 `새싹강의교안/` 하위에 주제별 폴더로 정리합니다.
- 폴더·파일 추가 시 이 README 의 디렉토리 구조 표도 함께 업데이트합니다.

---

## 참고

- GitHub: `gunnysis/sesac_dev`
- 학습 과정: 새싹(SeSAC) AI 부트캠프
