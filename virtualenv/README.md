# Python 가상환경 셋업 문서

## 개요

이 디렉토리는 **Python 3.10** 기반의 격리된 가상환경(`venv`)을 포함하며,
데이터 분석을 위한 핵심 패키지(`numpy`, `pandas`)의 특정 버전을 고정하여 사용합니다.

시스템에는 Python 3.14가 기본으로 설치되어 있으나, 본 프로젝트는 호환성을 위해
Python 3.10을 사용합니다.

---

## 환경 정보

| 항목 | 버전 |
|------|------|
| Python | 3.10.11 |
| pip | 26.1.1 |
| numpy | 1.21.6 |
| pandas | 1.3.5 |
| python-dateutil | 2.9.0.post0 |
| pytz | 2026.2 |
| six | 1.17.0 |

- **가상환경 도구**: `venv` (Python 표준 라이브러리)
- **가상환경 경로**: `C:\programming\venv\venv`
- **OS**: Windows 11
- **Shell**: PowerShell

---

## 디렉토리 구조

```
C:\programming\venv\
├── venv\                  # 가상환경 본체
│   ├── Scripts\
│   │   ├── Activate.ps1   # PowerShell 활성화 스크립트
│   │   ├── activate.bat   # CMD 활성화 스크립트
│   │   ├── python.exe     # 격리된 Python 3.10 인터프리터
│   │   └── pip.exe
│   ├── Lib\site-packages\ # 설치된 패키지
│   └── pyvenv.cfg
└── README.md
```

---

## 셋업 절차 (재현용)

처음부터 다시 셋업해야 할 경우 아래 순서대로 실행합니다.

### 1. 사전 조건 확인

Python 3.10이 설치되어 있어야 합니다.

```powershell
py -0
```

출력 예시:
```
 -V:3.14 *        Python 3.14 (64-bit)
 -V:3.10          Python 3.10 (64-bit)
```

### 2. 가상환경 생성

```powershell
py -3.10 -m venv venv
```

> `py -3.10` 런처를 사용하여 기본 Python(3.14)이 아닌 3.10을 명시적으로 지정합니다.

### 3. pip 업그레이드 및 패키지 설치

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install "numpy==1.21.6" "pandas==1.3.5"
```

### 4. 설치 검증

```powershell
.\venv\Scripts\python.exe -c "import sys, numpy, pandas; print('Python :', sys.version.split()[0]); print('numpy  :', numpy.__version__); print('pandas :', pandas.__version__)"
```

정상 출력:
```
Python : 3.10.11
numpy  : 1.21.6
pandas : 1.3.5
```

---

## 일상 사용법

### 가상환경 활성화 (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

활성화되면 프롬프트 앞에 `(venv)` 가 표시됩니다.

### 가상환경 활성화 (CMD)

```cmd
.\venv\Scripts\activate.bat
```

### 가상환경 비활성화

```powershell
deactivate
```

### 활성화 없이 직접 실행

가상환경을 활성화하지 않고도 격리된 인터프리터를 직접 사용할 수 있습니다.

```powershell
.\venv\Scripts\python.exe your_script.py
.\venv\Scripts\pip.exe list
```

---

## PowerShell 실행 정책 문제 해결

`Activate.ps1` 실행 시 다음과 같은 오류가 발생하는 경우:

```
이 시스템에서 스크립트를 실행할 수 없으므로 ... 로드할 수 없습니다.
```

현재 세션에 한해 정책을 우회합니다(가장 안전한 방법):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

현재 사용자에 영구 적용하려면:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 패키지 관리

### 현재 설치된 패키지 확인

```powershell
.\venv\Scripts\pip.exe list
```

### requirements.txt 생성

```powershell
.\venv\Scripts\pip.exe freeze > requirements.txt
```

### requirements.txt 로부터 재설치

```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

---

## 버전 선택 이유

- **Python 3.10**: `pandas 1.3.5` 가 제공하는 Windows용 사전 빌드 wheel은
  Python 3.7 ~ 3.10 까지만 지원합니다. Python 3.11 이상에서는 소스 빌드가
  필요하며 빌드 도구 의존성이 발생합니다.
- **numpy 1.21.6**: `pandas 1.3.5` 와의 ABI 호환성이 검증된 마지막 1.21.x 패치
  버전입니다.
- **pandas 1.3.5**: 1.3.x 계열의 마지막 안정 릴리스로 고정.

---

## 가상환경 삭제 (초기화)

가상환경을 완전히 제거하려면 폴더를 통째로 삭제하면 됩니다.

```powershell
Remove-Item -Recurse -Force .\venv
```

> 시스템에 설치된 Python 3.10 자체는 영향을 받지 않습니다.
