# sesacstudy

새싹(SeSAC) AI 부트캠프 **일자별 실습 저장소**.
`MMDD`(월일 4자리) 폴더 하나가 부트캠프 **하루**에 대응하며, 그 외 개인 프로젝트(`alone/`)와
Microsoft 공식 실습 클론(`mslearn-*`)을 함께 보관합니다.

> 언어는 한국어 기준입니다(주석·마크다운·커밋 메시지 모두 한국어).
> 이 폴더가 git 저장소 루트(GitHub `gunnysis/sesacstudy`)입니다. 작업 가이드(`CLAUDE.md`)·
> 에디터 설정(`.vscode/`)·강의교안 심볼릭 링크(`study_docs_link/`)도 이 루트에 함께 있습니다.

---

## 디렉토리 구조

```text
sesacstudy/
├── 0522/                       # 수학·시각화
│   ├── equation.py                 # SymPy 연립방정식 풀이
│   ├── systemsOfEquations.py       # matplotlib 3D 그래프 (인바디 추이)
│   └── test.ipynb
├── 0527/                       # Python 기초 + 웹 크롤링
│   ├── hello.ipynb                 # Python 기본 문법
│   ├── web_crolling1.ipynb         # 정적 크롤링 (requests + BeautifulSoup)
│   ├── web_crolling2.ipynb         # 정적 크롤링 심화
│   ├── playwright-scrapping.py     # 동적 크롤링 (Playwright)
│   └── requirements.txt
├── 0528/                       # 데이터 분석 기초
│   ├── numpy-exercise.ipynb
│   ├── pandas-exercise.ipynb
│   ├── matplotlib-exercise.ipynb
│   └── seaborn-exercise.ipynb
├── 0601/                       # 시각화 심화 + 시계열
│   ├── seaborn-exercise.ipynb
│   ├── timeseries-exercise.ipynb   # 시계열 (relativedelta 등)
│   ├── polium-exercise.ipynb       # folium 지도 시각화
│   ├── map.html                    # folium 결과물
│   ├── 병원정보.txt                # folium 실습용 병원 좌표 데이터 (git 미포함, 로컬 전용)
│   └── requirements.txt
├── 0610/                       # 데이터 전처리 실습 (클론: Preprocessing-excersize)
│   └── Preprocessing-excersize-main/
│       └── notebooks/              # 02.x 정제·집계·결합·분할 / 03.x 수치·범주·날짜·GIS, CustomVision
├── 0611/                       # OpenCV 이미지 처리
│   ├── cv_study.py                 # 이진화(Otsu threshold) 등 OpenCV 실습
│   ├── assets/                     # 실습용 이미지 (RGB·soccer 등)
│   ├── memo.md                     # OpenCV 실습 메모
│   └── requirements.txt
├── 0615/                       # 분류 실습용 데이터셋
│   └── adult.csv                   # UCI Adult(Census Income) — 연소득 >50K 분류용
├── 0701/                       # Azure AI Document Intelligence + Gradio 입문
│   ├── sample_analyze_read.py      # Prebuilt Read — 문서 텍스트·좌표 추출 (endpoint/key 필요)
│   ├── sample.ipynb                # Gradio 입문 (Interface·ChatInterface 실습)
│   └── requirements.txt            # azure-ai-documentintelligence · numpy 등
├── 0702/                       # Azure Document Intelligence — 인보이스·영수증 추출
│   ├── receipts.py                 # Prebuilt Invoice — uploads/ 이미지 일괄 분석 → docs/receipts_output.csv
│   ├── invoices.py                 # Prebuilt Document — URL 문서 key-value 추출 (azure-ai-formrecognizer)
│   ├── uploads/                    # 분석 대상 영수증·인보이스 이미지
│   ├── docs/receipts_output.csv    # 추출 결과 CSV
│   ├── .env                        # END_POINT·API_KEY (git 제외)
│   └── requirements.txt
├── 0703/                       # Azure Speech Services (STT·TTS·번역) + OpenAI 챗봇
│   ├── speech_synthesis.py         # TTS — SSML(ssml.xml) → audiofile.wav 합성
│   ├── ssml.xml                    # 다국어 음성 합성용 SSML 입력
│   ├── translate.py                # 음성 번역 (ko-KR → it, 마이크 입력)
│   ├── audiofile.wav               # TTS 결과물
│   ├── speech-services/
│   │   ├── stt.py                  # 마이크 STT (ko-KR)
│   │   ├── test_stt.py             # Speech 인증 확인용 스크립트
│   │   └── speech-chatbot.ipynb    # Gradio STT + Azure OpenAI 챗봇 UI
│   └── .env                        # SPEECH_KEY·REGION·AZURE_OPENAI_* (git 제외, venv/ 도 제외)
├── 0706/                       # Azure Custom Vision — 객체 탐지 (fork·scissors·glasses)
│   └── custom-vision/
│       ├── main.py                 # 파이프라인 엔트리포인트 (argparse CLI: --refresh-glasses·--force)
│       ├── cvpipeline/             # 기능별 모듈 패키지
│       │   ├── config.py               # .env·클라이언트·상수
│       │   ├── project_setup.py        # 도메인/프로젝트/태그 get-or-create (+ObjectDetection 도메인 검증)
│       │   ├── regions.py              # fork·scissors 고정 바운딩 박스 좌표
│       │   ├── glasses_detect.py       # OpenCV Haar cascade 안경 박스 자동 검출
│       │   ├── glasses_labels.py       # glasses 라벨 소스 우선순위(YOLO .txt > CSV > cascade)
│       │   ├── images.py               # 업로드 엔트리 구성·삭제·배치 업로드
│       │   ├── audit.py                # 학습 전 라벨링 점검(진단)
│       │   ├── training.py             # 진행중 대기·완료 폴링(20분 타임아웃)·이터레이션 정리
│       │   ├── publish.py              # 이터레이션 게시(이름 점유 시 재게시)
│       │   ├── prediction.py           # 예측 + 바운딩 박스 시각화
│       │   └── pipeline.py             # 위 단계 조립(train_and_publish·predict_images)
│       ├── augment_glasses.py      # glasses 오프라인 증강(반전·밝기 — 권장 50장 확보)
│       ├── augment_forkscissors.py # fork·scissors 증강(반전 시 박스 좌표 변환 → YOLO .txt 사이드카)
│       ├── validate_retrain.py     # 재학습 격리 검증용 임시 러너
│       ├── TROUBLESHOOTING.md      # 학습 stuck 장애 디버깅 기록(원인·수정·검증·재발방지)
│       ├── Images/                 # fork·scissors·glasses 학습용 + test(입력)·predictions(출력)
│       │                           #   ⚠ test·predictions 는 인물사진 보호로 git 미추적(README 만 추적)
│       ├── requirements.txt        # azure-...-customvision·opencv-python 등
│       ├── .env.example            # 채울 환경변수 목록(키 없음)
│       └── .env                    # VISION_TRAINING/PREDICTION_*·VISION_PROJECT_NAME (git 제외)
│
├── 0708/                       # Azure AI Language — NER·PII 인식 + 시각화 + Gradio 웹앱
│   ├── quick_start/                # 공식 퀵스타트 원형 (ner.py·pii.py)
│   ├── ner_utils/                  # 공용 패키지 (Azure 클라이언트·문서 로딩·플롯 헬퍼)
│   ├── visualize_output.py         # CLI: NER/PII 실행 → plots/ 에 요약 플롯 저장
│   ├── app.py                      # Gradio 웹앱 — 텍스트박스 입력 → 결과 표·플롯·PII 리포트
│   ├── test.txt                    # 예시 입력 (한 줄당 문서 하나)
│   ├── plots/                      # CLI 출력 결과물 (플롯 PNG·PII 리포트)
│   ├── .env.example                # 채울 환경변수 목록(키 없음)
│   └── .env                        # LANGUAGE_KEY·LANGUAGE_ENDPOINT (git 제외)
│
├── alone/                      # 개인 프로젝트 (날짜 실습과 별개)
│   ├── eundunhealth-user-flow-diagram.ipynb  # 멘탈헬스 앱 Mermaid 사용자 플로우
│   ├── karaoke_data_analyze.ipynb            # 노래연습장 인허가 공공데이터 분석
│   ├── assets/                     # 결과물 (user-flow-diagram.png 등)
│   ├── docs/                       # 메모·약관·통계 문서 + 분석용 CSV
│   └── requirements.txt
├── mslearn-openai/             # Azure OpenAI 공식 실습 (클론 평탄화 — 내부 .git 제거)
│   ├── Instructions/Exercises/     # 01~06 실습 가이드
│   ├── Labfiles/                   # 실습 코드(Python·C#) + 데이터(brochures·자체데이터 RAG 등)
│   └── readme.md                   # ⚠ Labfiles/**/Python/.env(Azure 키)는 .gitignore 제외
├── mslearn-ai-agents/          # Azure AI 에이전트(Foundry) 공식 실습 (클론 평탄화)
│   ├── Instructions/Exercises/     # 에이전트 구축·MCP·오케스트레이션·A2A 등
│   └── Labfiles/                   # 실습 코드 (venv labenv/ 는 제외)
│
├── memo.md                     # 학습 메모 (Git / 크롤링 / 라이브러리 등)
├── CLAUDE.md                   # Claude Code 작업 가이드 (저장소 성격·구조 규칙·환경·VSCode PDF 설정)
├── study_docs_link             # 외부배포금지 강의교안 심볼릭 링크 (내용은 미추적)
├── .vscode/                    # 에디터 설정 (심볼릭 링크 PDF 외부 열기 태스크 등 · 자세히는 CLAUDE.md)
├── .gitignore                  # 데이터·venv·.env·.gradio 등 무시 규칙
└── README.md                   # (현재 파일)
```

> 대용량 데이터셋(CSV/JSON)은 git에 포함하지 않습니다. 데이터가 필요한 실습은
> 해당 `*-data/` 폴더의 README 안내에 따라 직접 배치하세요.
>
> **외부 클론 정리** (중복·혼란 방지):
>
> - `DL-Excersize/`(딥러닝 전이학습) → 대용량(`moonrockmodel.pth` 등)이라 저장소 **밖(`../backup/`)으로 이동(백업)**.
> - `mslearn-openai/`(Azure OpenAI), `mslearn-ai-agents/`(Azure AI 에이전트) → 내부 `.git` 만 제거해 **일반 파일로 평탄화**하여 포함. 단 가상환경(`labenv/`)·캐시·대용량 바이너리는 제외.
> - `0610/Preprocessing-excersize-main/` → 이미 평탄화된 클론(자체 `.devcontainer`·`requirements.txt` 포함).
>
> ⚠ **비밀키 주의**: 클론들의 `Labfiles/**/Python/.env`(Azure 키·엔드포인트)와 각 날짜 폴더의 `.env` 는 `.gitignore`(`*.env`)로 반드시 제외됩니다 — 커밋 금지.

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
- `cv.imshow`/`cv.waitKey` 로 GUI 창을 띄우므로 노트북이 아닌 `py` 실행 전제

### 0615 — 분류 실습용 데이터셋

- **UCI Adult (Census Income)** 데이터셋(`adult.csv`) — 인구통계 특성으로 연소득 `>50K` 여부 분류
- 현재는 데이터만 보관 (실습 노트북은 추후 추가)

### 0701 — Azure AI Document Intelligence + Gradio 입문

- **Azure AI Document Intelligence**(구 Form Recognizer) SDK 로 **Prebuilt Read** 모델 실습
- `sample_analyze_read.py`: 원격 문서(URL)를 분석해 페이지별 텍스트 라인·단어·신뢰도와 **바운딩 박스 좌표**(numpy 로 정형화) 추출
- `sample.ipynb`: **Gradio** 입문 — `gr.Interface`(텍스트 인사) · `gr.ChatInterface`(간단 챗봇) 로 UI 프로토타입 실습
- 실행 전 코드의 `endpoint`·`key` 를 본인 Azure 리소스 값으로 채워야 함 — 키는 커밋 금지(운영 시 환경변수/`.env` 사용 권장)
- 사용 패키지: `azure-ai-documentintelligence`(→ `azure-core`)·`numpy` (`requirements.txt` 참고)

### 0702 — Azure Document Intelligence (인보이스·영수증 추출)

- **Prebuilt Invoice·Document** 모델로 문서에서 구조화된 필드를 추출하는 실습
- `receipts.py`: `uploads/` 폴더의 영수증·인보이스 이미지(`.jpg/.png/.pdf` 등)를 **일괄 분석**해 공급자·고객·금액·품목 등 수십 개 필드를 `docs/receipts_output.csv`(UTF-8-SIG) 로 저장
- `invoices.py`: 샘플 문서(URL)를 **Prebuilt Document** 로 분석해 **key-value 쌍** 출력 — 구버전 `azure-ai-formrecognizer` SDK(`DocumentAnalysisClient`) 사용
- 키·엔드포인트는 `.env`(`END_POINT`·`API_KEY`)에서 로드 — `python-dotenv` 사용, `.env` 는 git 제외

### 0703 — Azure Speech Services (STT·TTS·번역) + OpenAI 챗봇

- **Azure Cognitive Services Speech SDK** 로 음성 기능 전반 실습 (언어 `ko-KR` 기준)
  - `speech-services/stt.py`: 기본 마이크 입력을 **음성 → 텍스트(STT)** 로 인식
  - `speech-services/test_stt.py`: 푸시 스트림으로 **Speech 리소스 인증·연결만 빠르게 점검**하는 스크립트
  - `speech_synthesis.py`: **SSML**(`ssml.xml`, 다국어 voice 지정) 입력을 **텍스트 → 음성(TTS)** 합성해 `audiofile.wav` 로 저장
  - `translate.py`: **음성 번역** — 마이크 한국어 입력을 이탈리아어(`it`)로 실시간 번역
- `speech-services/speech-chatbot.ipynb`: **Gradio** UI 로 STT + **Azure OpenAI** 챗봇 결합 — 마이크 녹음을 STT 로 인식해 텍스트박스에 넣고, `AzureOpenAI` chat completions 로 대화. `demo.launch(share=True)` 로 공유 링크 생성
- 환경변수(`.env`): `SPEECH_KEY`·`REGION`/`SERVICE_REGION`·`ENDPOINT`, 챗봇은 추가로 `AZURE_OPENAI_ENDPOINT`·`AZURE_OPENAI_KEY`·`DEPLOY_NAME` 필요 — 모두 git 제외
- 노트북은 셀에서 `%pip install` 로 의존성(`gradio`·`azure-cognitiveservices-speech`·`openai`·`ipywidgets` 등)을 직접 설치, `speech-services/venv/` 가상환경은 git 제외

### 0706 — Azure Custom Vision (객체 탐지)

- **Azure Custom Vision** 으로 **객체 탐지(Object Detection)** 모델을 학습·게시·예측하는 실습 — `fork`·`scissors`·`glasses` 3개 태그 (도메인: General / ObjectDetection)
- 원본은 공식 [객체 탐지 퀵스타트](https://learn.microsoft.com/ko-kr/azure/ai-services/custom-vision-service/quickstarts/object-detection?pivots=programming-language-python) 기반 단일 파일이었으며, 이를 **기능별 모듈 패키지(`cvpipeline/`) + 엔트리포인트(`main.py`)로 리팩토링**
  - `config`(설정)·`project_setup`(프로젝트/태그)·`regions`(fork·scissors 고정 좌표)·`glasses_detect`(안경 박스 자동 검출)·`glasses_labels`(라벨 소스 우선순위)·`images`(업로드)·`audit`(라벨 점검)·`training`(학습)·`publish`(게시)·`prediction`(시각화)·`pipeline`(조립)
- **fork·scissors** 는 이미지마다 정밀 바운딩 박스 좌표를 지정하고, **glasses** 는 실제 어노테이션(YOLO `.txt`/`_annotations.csv`)이 있으면 그것을, 없으면 **OpenCV Haar cascade**(안경 대응 눈 검출기)로 안경 영역을 자동 검출해 박스를 만든다(파일별 자동 — 좌표 하드코딩 불필요). 폴더에 사진을 넣기만 하면 반영됨
  - 현재 glasses 50장은 원본 데이터셋의 **실제 어노테이션**(`Images/glasses/_annotations.csv`, 픽셀 xyxy → 정규화 변환)을 사용 — cascade 추정보다 정확
  - 세 태그 모두 **권장 50장** 충족: fork·scissors 는 `augment_forkscissors.py` 증강(반전 시 `left' = 1 - left - width` 로 박스도 변환, YOLO `.txt` 사이드카로 저장)으로 20→50장
- 재실행 안전 설계(트러블슈팅 반영 — 상세는 [TROUBLESHOOTING.md](0706/custom-vision/TROUBLESHOOTING.md)): **진행 중 학습을 이미지 변경 '전'에 대기**(학습 중 참조 이미지 삭제로 인한 백엔드 stuck 방지 — 근본 원인), 변경 없으면 학습 생략하고 기존 모델 재사용(`Nothing changed` 정상 처리), 프로젝트/태그 **get-or-create** + **ObjectDetection 도메인 검증**(Classification 프로젝트 오지정 시 조기 실패), 학습 폴링 **20분 타임아웃**, **이터레이션 자동 정리**(프로젝트당 20개 상한 보호), 이름 점유 시 unpublish 후 재게시
- 학습 전 **라벨 자동 점검**(`audit.py`): 리전 없는 이미지·너무 작은/이미지 밖 박스·규격(최소 256px)·권장(태그당 50+) 미달을 경고
- 실행: `python main.py [임계값 0~1] [테스트이미지경로]` (인자 없으면 `Images/test/` 의 모든 이미지 예측 — 파일명 제한 없음) — 결과는 입력과 분리된 `Images/predictions/prediction_<이름>.png` 로 저장. glasses 박스 로직을 바꿨으면 `--refresh-glasses`(삭제 후 재업로드), 강제 재학습은 `--force`
- **개인정보 보호**: `Images/test/`(테스트 입력)와 `Images/predictions/`(예측 결과)는 인물 사진이 포함될 수 있어 **git 미추적**(각 폴더 안내 README 만 추적) — 테스트 이미지는 사용자가 직접 배치
- 환경변수(`.env`, 목록은 `.env.example` 참고): `VISION_TRAINING_ENDPOINT`·`VISION_TRAINING_KEY`·`VISION_PREDICTION_ENDPOINT`·`VISION_PREDICTION_KEY`·`VISION_PREDICTION_RESOURCE_ID`·`VISION_PROJECT_NAME`(선택 `VISION_PROJECT_ID`) (git 제외)
- 사용 패키지: `azure-cognitiveservices-vision-customvision`·`opencv-python`·`matplotlib`·`Pillow`·`python-dotenv` (`requirements.txt` 참고)
- ⚠ Azure Custom Vision 은 **2028-09-25 지원 종료 예정**(공식 공지) — 장기적으로 Azure Machine Learning AutoML 등으로 전환 권장

### 0708 — Azure AI Language (NER·PII) + Gradio 웹앱

- **Azure AI Language(Text Analytics)** 로 **NER(엔터티 인식)** 과 **PII(개인정보) 인식**을 실행하고 결과를 시각화하는 실습
- `quick_start/`(공식 퀵스타트 원형) → `ner_utils/` 공용 패키지 + `visualize_output.py` CLI 로 리팩토링 → `app.py` **Gradio 웹앱**으로 확장하는 3단계 구성
  - `ner_utils/`: `azure_text_analytics`(인증·응답→DataFrame 변환·문서별 병합), `file_utils`(문서 로딩), `visualization`(한글 폰트 선택·팔레트 검증·요약 플롯·PII 리포트)
- CLI: `python visualize_output.py -i test.txt --pii` — 카테고리별 개수·신뢰도 분포·길이 분포·PII 상위 텍스트 플롯과 문서별 PII 리포트를 `plots/` 에 저장 (`--list-palettes`·`--palette`·`--font` 옵션)
- **Gradio 웹앱**(`python app.py` → `http://127.0.0.1:7860`): 파일 대신 **텍스트박스에 한 줄당 문서 하나**를 입력받아 NER/PII 결과 표(DataFrame)·요약 플롯(**gr.Plot** — matplotlib Figure 직접 렌더링)·문서별 PII 리포트를 탭으로 표시. PII 실행 여부·언어 힌트·팔레트를 UI 에서 선택, `demo.launch(share=True)` 로 공유 링크 생성 가능
- seaborn 0.13+ 대응: `hue` 없이 `palette` 만 넘기는 deprecated 패턴을 `hue=…, legend=False` 로 정리
- 환경변수(`.env`, 목록은 `.env.example` 참고): `LANGUAGE_KEY`·`LANGUAGE_ENDPOINT` (git 제외)
- 사용 패키지: `azure-ai-textanalytics`·`pandas`·`matplotlib`·`seaborn`·`gradio`·`python-dotenv` (`requirements.txt` 참고)

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

학습 메모는 [memo.md](memo.md) 참고.

---

## 환경 설정 — 폴더별 격리 venv

전역 환경이 없습니다. 각 실습 폴더가 **자체 `requirements.txt` 와 `.venv/`** 를 가집니다
(`.venv/` 는 git 제외). 어떤 폴더의 노트북을 다루기 전에 그 폴더 기준으로 환경을 만듭니다.

```powershell
cd 0601                       # 작업할 날짜 폴더
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- `requirements.txt` 가 없는 폴더(0522, 0528)는 인접 폴더(0527/0601)의 환경을 재사용하거나 필요한 패키지만 설치합니다.
- 평탄화 클론(`mslearn-openai/`, `mslearn-ai-agents/`, `0610/Preprocessing-excersize-main/`)은 `requirements.txt`·`.env` 가 **패키지/실습 하위 루트**에 있으니 그 위치에서 venv(`labenv/` 등, git 제외)를 만들고 키를 채웁니다.
- **Playwright**(0527) 동적 크롤링은 브라우저 바이너리가 추가로 필요합니다: `playwright install`
- **OpenCV**(0611, `cv2`)는 GUI 창을 띄우는 스크립트라 노트북이 아닌 `py` 실행 전제이며, `cv.imread()` 는 **현재 작업 디렉토리(cwd)** 기준으로 경로를 찾습니다.
- `requirements.txt` 는 직접 손으로 편집하지 말고, 해당 폴더 venv 에서 `pip freeze > requirements.txt` 로 재생성합니다.

> **설치 환경 = 실행 환경** 을 반드시 일치시키세요. 다른 venv 가 활성화된 상태로 실행하면
> 설치한 패키지를 못 찾는 `ModuleNotFoundError` 가 납니다. 프롬프트의 `(.venv)` 표시로 활성 환경을 확인하세요.

---

## 🔐 비밀키·환경변수 (public 저장소)

이 저장소는 **공개**입니다. Azure 키·엔드포인트·토큰을 **코드나 노트북에 절대 하드코딩하지 마세요.**

- 실제 값은 각 폴더의 **`.env`** 에 넣고 `os.getenv(...)` 로 읽습니다(`python-dotenv`). `.env` 는 `.gitignore` 로 전역 제외됩니다.
- 필요한 변수 이름은 각 폴더의 **`.env.example`**(0701·0702·0703 등)을 복사해 `.env` 로 채우세요.
- **커밋 전 시크릿 차단 훅**을 활성화하면 실수로 키를 커밋하는 것을 막아 줍니다(한 번만):

  ```powershell
  git config core.hooksPath .githooks
  ```

  `.githooks/pre-commit` 이 스테이징된 변경에서 Azure 키·`sk-` 토큰·개인키 등을 탐지해 커밋을 차단합니다.
- 노트북 **출력 셀**에도 키가 남을 수 있으니 커밋 전 확인하세요. 이미 유출된 키는 파일에서 지워도 히스토리에 남으니 **Azure 포털에서 즉시 재발급**하세요.

---

## 데이터 파일 규칙 (git 추적 제외)

대용량 데이터셋은 git 에 올리지 않습니다. 저장소 루트 `.gitignore` 가 이를 강제합니다:

- `**/*-data/*.csv`, `*.json` 은 무시, 단 같은 폴더의 `README.md` 는 추적(출처·배치 안내용).
- 데이터가 필요한 노트북은 `*-data/` 폴더 README 안내대로 사용자가 직접 파일을 배치하는 구조이므로,
  노트북이 데이터 경로에서 `FileNotFoundError` 를 내도 그것이 정상일 수 있습니다 — 임의로 데이터를 생성하지 말고 README 의 출처를 확인하세요.

---

## 새 실습 추가 규칙

- 새 실습은 `MMDD/` 폴더를 만들어 추가합니다 (각 날짜 = 부트캠프 하루).
- 각 실습 폴더는 자체 `requirements.txt` 와 `.venv/` 를 유지합니다 (의존성 격리).
- `venv/`, `.venv/`, `.claude/`, `__pycache__/`, `.ipynb_checkpoints/`, `.gradio/` 등은 `.gitignore` 로 제외됩니다.
- 대용량 데이터(CSV/JSON)는 git 에 올리지 않고, `*-data/` 폴더에 README 로 출처·배치 방법을 남깁니다.
- 폴더·파일 추가 시 이 README 의 디렉토리 구조와 학습 요약도 함께 업데이트합니다.

---

## 저장소 루트 부속 파일

- **`CLAUDE.md`** — Claude Code 작업 가이드(저장소 성격·구조 규칙·환경 + VSCode PDF 설정 상세).
- **`study_docs_link`** — 외부배포금지 강의교안 심볼릭 링크(내용은 미추적). 대상 폴더명·계층이 수시로 재구성되니 경로 하드코딩 금지, 그때그때 탐색(한글 NFC/NFD 정규화 차이 주의).
- **`.vscode/`** — 심볼릭 링크 폴더의 PDF 를 외부 앱으로 여는 자가 치유 태스크(`open-external.ps1` + `Ctrl+Alt+O`). 자세한 원리는 `CLAUDE.md` 참고.

---

## 참고

- GitHub: `gunnysis/sesacstudy`
- 학습 과정: 새싹(SeSAC) AI 부트캠프
