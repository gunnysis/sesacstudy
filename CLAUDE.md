# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 성격

새싹(SeSAC) AI 부트캠프 **학습 저장소**입니다. 빌드 시스템·테스트 스위트·CI 가 없는,
Jupyter 노트북과 단발성 Python 스크립트의 모음입니다. "통과해야 할 테스트"가 아니라
"학습 내용이 재현되는지"가 정답 기준입니다. 코드를 수정하면 해당 노트북을 실제로
실행해 결과(셀 출력, 생성되는 HTML/PNG)가 의도대로 나오는지 확인하세요.

언어는 한국어 기준입니다. 주석·마크다운·커밋 메시지 모두 한국어로 맞춥니다.

## 구조 규칙 (핵심)

- 실습은 `sesacstudy/MMDD/` (월일 4자리) 폴더 단위로 나뉘며, **각 날짜가 부트캠프 하루**에 대응합니다.
- `sesacstudy/alone/` 은 날짜 실습과 별개인 **개인 프로젝트**(eundunhealth — 멘탈헬스 앱 설계, mermaid 다이어그램)입니다.
- `memo/` 는 강의 메모(`memo.md`, `azure.md`)로 코드가 아닌 학습 노트입니다.
- 새 실습 추가 시 루트 [README.md](README.md) 의 디렉토리 구조와 학습 요약도 **함께 갱신**합니다.

## 의존성: 폴더별 격리 venv

전역 환경이 없습니다. 각 실습 폴더가 **자체 `requirements.txt` 와 `.venv/`** 를 가집니다
(`.venv/` 는 git 제외). 어떤 폴더의 노트북을 다루기 전에 그 폴더 기준으로 환경을 만듭니다.

```powershell
cd sesacstudy/0601           # 작업할 날짜 폴더
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

- `requirements.txt` 가 없는 폴더(0522, 0528)는 인접 폴더(0527/0601)의 환경을 재사용하거나 필요한 패키지만 설치합니다.
- 0527 의 **Playwright** 동적 크롤링은 브라우저 바이너리가 추가로 필요합니다: `playwright install`
- `requirements.txt` 는 직접 손으로 편집하지 말고, 해당 폴더 venv 에서 `pip freeze > requirements.txt` 로 재생성합니다.

## 데이터 파일 규칙 (git 추적 제외)

대용량 데이터셋은 git 에 올리지 않습니다. `.gitignore` 가 이를 강제합니다:

- `sesacstudy/**/*-data/*.csv`, `*.json` 은 무시, 단 같은 폴더의 `README.md` 는 추적(출처·배치 안내용).
- 데이터가 필요한 노트북은 `*-data/` 폴더 README 안내대로 사용자가 직접 파일을 배치하는 구조이므로,
  노트북이 데이터 경로에서 `FileNotFoundError` 를 내도 그것이 정상일 수 있습니다 — 임의로 데이터를 생성하지 말고 README 의 출처를 확인하세요.
- `새싹강의교안/`, `study_source_link`, `sesac_docs_link`(로컬 절대경로 심볼릭 링크)는 외부 배포 금지 자료라 추적하지 않습니다.

## 환경

- **Windows + PowerShell**. 경로 구분자·활성화 스크립트(`.ps1`)·`py` 런처를 전제로 합니다.
- 노트북 편집은 NotebookEdit 도구를 사용하고, 출력 결과물(예: 0601 `map.html`, alone `user-flow-diagram.png`)은 노트북 재실행으로 갱신됩니다.
