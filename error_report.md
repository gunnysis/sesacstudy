
Notebook execute error
`> Jupyter: restart Kernel`

---

## 2026-07-01 — `ModuleNotFoundError` (설치했는데 못 찾음, 0701)

**증상**: `pip install azure-ai-documentintelligence` 성공 후에도
`sample_analyze_read.py` 실행 시 `ModuleNotFoundError: No module named 'azure.ai.documentintelligence'`.

**원인**: 설치한 환경 ≠ 실행하는 환경.

- 설치는 루트 `sesac\dev\.venv` 로 들어감
- 실행 셸엔 엉뚱한 `mslearn-ai-agents\...\labenv` 가 활성화돼 있었음
- 같은 이름 패키지라도 파이썬마다 별도 설치라, 다른 venv 에서 실행하면 못 찾음

**해결**: CLAUDE.md 폴더별 격리 venv 규칙대로 `sesacstudy/0701/.venv` 생성 →
그 안에 설치 → `pip freeze > requirements.txt` 로 고정.

**재발 방지**:

- `install` 과 `실행` 은 **반드시 같은 (활성화된) venv** 에서. 프롬프트의 `(.venv)` 표시 확인.
- VS Code: `Python: Select Interpreter` 로 해당 폴더 `.venv` 지정(터미널·실행 버튼 통일).
- import 에러 나면 먼저 "지금 활성 venv 가 이 폴더 것 맞나?" 부터 점검.
