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
