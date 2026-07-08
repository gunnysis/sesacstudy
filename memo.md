# 메모

- relativedelta(dateutil 패키지)가 timedelta의 역할을 모두 대체 가능

## 1. Git

### 1.1. 로그인 정보 저장

```bash
git config --global user.name "사용자이름"
git config --global user.email "이메일정보"
```

### 1.2. 로그인 정보 영구 저장

```bash
git config --global credential.helper store
```

### 1.3. 사용자 설정 에러 시 remote URL 재설정

특정 폴더에서만 git 레포 변경 및 저장 방법

```bash
git config --local credential.helper store
git remote set-url origin
```


## 2. PowerShell

### 2.1. 심볼릭 링크 생성

```powershell
New-Item -ItemType SymbolicLink -Path "생성할링크경로" -Target "원본폴더경로"
```

## 3. 데이터셋 사이트

- [AI Hub](https://aihub.or.kr/)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

## 4. 크롤링

### 4.1. 정적 페이지 크롤링

- `requests`
- `BeautifulSoup`

### 4.2. 동적 페이지 크롤링

- `playwright`
- `selenium`

### 4.3. 필요한 라이브러리 설치

```bash
pip install requests
pip install beautifulsoup4
pip install selenium
pip install openpyxl
pip install lxml
pip install pillow
pip install konlpy
pip install wordcloud
```

## 5. C++ 빌드 도구 설치

Windows 패키지 관리자(winget)로 Visual Studio Build Tools를 사용자 개입 없이 자동 설치한다.

```powershell
winget install Microsoft.VisualStudio.BuildTools --override " --passive --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

## 6. 재발생 시 사용법

- 증상 예시: `ModuleNotFoundError: No module named 'cv2'` 같은 패키지 관련 오류가 발생할 때.

- 빠른 대응 절차:

	1. 작업 폴더로 이동

		 ```powershell
		 cd 0611   # 저장소 루트 기준
		 ```

	2. 가상환경이 없으면 생성 (Windows에서):

		 ```powershell
		 py -3 -m venv .venv
		 ```

		 또는 특정 Python 실행파일을 지정해서 생성:

		 ```powershell
		 C:\Path\To\python.exe -m venv .venv
		 ```

	3. 가상환경 활성화

		 - PowerShell:

			 ```powershell
			 .\.venv\Scripts\Activate.ps1
			 ```


		 - Git Bash / WSL:

			 ```bash
			 source .venv/Scripts/activate
			 ```

	4. 의존성 설치

		 - 프로젝트 루트에 `requirements.txt`가 있으면:

			 ```bash
			 pip install -r requirements.txt
			 ```

		 - 특정 패키지만 필요하면 직접 설치 (예: OpenCV):

			 ```bash
			 pip install opencv-python
			 ```

	5. 실행 예시

		 ```powershell
		 .\.venv\Scripts\python.exe Ch.01\1-1.py
		 ```

	6. 환경 동기화(권장)

		 - 패키지 변경 후 `requirements.txt` 갱신:

			 ```bash
			 pip freeze > requirements.txt
			 ```

- 추가 팁:

	- `Activate.ps1` 실행 권한 문제가 있으면 PowerShell에서 다음을 실행한 뒤 활성화하세요:

		```powershell
		Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
		.\.venv\Scripts\Activate.ps1
		```

	- pip 문제가 있으면 업그레이드:

		```bash
		python -m pip install --upgrade pip
		```


## 7. Azure Custom Vision — 학습이 몇 시간씩 안 끝날 때 (2026-07-08)

- 정상 학습 시간 기준: 태그 3개 × 이미지 ~90장 규모에서 **약 9분** (폴링 타임아웃 20분 권장). 이보다 크게 초과하면 백엔드 wedge 를 의심.
- 흔한 원인 3가지:
	1. **학습이 돌고 있는데 그 프로젝트의 이미지를 삭제/변경** → 이터레이션이 `Training` 에서 수 시간 멈추고 프로젝트 학습 큐가 wedge 됨. 반드시 이전 이터레이션이 Completed/Failed 된 뒤 데이터 변경.
	2. 매 실행 `force_train=True` → 불필요한 재학습 반복 + **이터레이션 상한(프로젝트당 20개, F0/S0 공통)** 도달 시 학습 거부. 변경 없으면 `Nothing changed` 를 정상 처리해 기존 모델 재사용.
	3. 포털에서 만든 프로젝트의 **도메인 종류 불일치** — Classification 프로젝트에는 객체탐지(리전 업로드·detect_image) 불가, 타입은 생성 후 변경 불가라 새로 만들어야 함.
- 상세 기록: [0706/custom-vision/TROUBLESHOOTING.md](0706/custom-vision/TROUBLESHOOTING.md)
