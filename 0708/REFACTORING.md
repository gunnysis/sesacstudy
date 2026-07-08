# 0708 리팩토링 기록 — NER/PII 시각화 (app.py · ner_utils · visualize_output.py)

[CodeSee — Python Refactoring](https://www.codesee.io/learning-center/python-refactoring) 문서의
기법을 기준으로 2026-07-08 실습 코드를 리팩토링한 기록입니다.
동작(출력 포맷·플롯·CLI 옵션·Gradio UI)은 그대로 유지하고 내부 구조만 개선했습니다.

> 이 문서의 1~6장은 리팩토링 시점 기준입니다. 같은 날 후속 작업으로
> **Gradio 앱의 플롯이 matplotlib → Plotly 로 전환**됐습니다(7장 참고) —
> `app.py` 관련 서술 중 Figure 는 이제 Plotly Figure 를 뜻합니다. CLI 는 matplotlib 그대로.

## 적용한 기법 요약

| 문서의 기법 | 적용 위치 |
| --- | --- |
| 메서드 추출 (Extract Method) | `app.py` `analyze()` 분해, `ner_utils` 공용 함수 추출로 중복 제거 |
| 조건문 단순화 (Decompose Conditional / Guard Clause) | `choose_font()` 탐색 루프, `visualize_output.py` 문서 결정, 기존 guard clause 유지 |
| 리스트/제너레이터 컴프리헨션 | `_entities_to_df()`, `build_pii_report_text()`, `choose_font()` |
| 매직 넘버 → 명명 상수 (Symbolic Constants) | 팔레트 목록, 막대 라벨 스타일, `'auto'` 센티널, 오류 라벨 문자열 |
| 의미 있는 이름 사용 | `df_list`→`frames`, `p`→`bar`, `i`→`doc_index`, `f`→`font`, `grp`→`group` 등 |
| Pythonic 수열 검사 | `pd.concat(frames, …) if frames else pd.DataFrame()` 조건 표현식 |

## 파일별 상세

### 1. `ner_utils/azure_text_analytics.py`

**함수 추출 + 리스트 컴프리헨션** — `_entities_to_df()` 의 행 조립 루프에서
엔터티 1건→dict 변환을 `_entity_to_row()` 로 추출하고, 루프를 컴프리헨션으로 교체.

```python
# Before
rows = []
for entity in entities:
    row = {...}          # 15줄의 조립 로직이 루프 안에
    rows.append(row)

# After
rows = [_entity_to_row(entity, doc_id, include_subcategory) for entity in entities]
```

**중복 제거를 위한 함수 추출(핵심)** — `app.py` 와 `visualize_output.py` 에 각각 있던
"API 호출 → `collect_results_df` 병합" 2단계와 PII 언어 kwargs 조립이 중복이었음.
`recognize_entities_df()` / `recognize_pii_df()` 로 추출해 두 진입점이 공유.

```python
# Before — app.py 와 visualize_output.py 양쪽에 반복
pii_kwargs = {'language': language} if language != 'auto' else {}
pii_response = client.recognize_pii_entities(documents=docs, **pii_kwargs)
pii_df = collect_results_df(pii_response, extract_pii_to_df, 'PII Document')

# After — 한 곳으로
pii_df = recognize_pii_df(client, docs, language=...)
```

**의미 있는 이름 + Pythonic 반환** — `collect_results_df()` 에서
`df_list`→`frames`, `i`→`doc_index`, 마지막 `if/return` 두 줄을 조건 표현식으로.
`'Document'`/`'PII Document'` 오류 라벨 문자열은 `NER_ERROR_LABEL`/`PII_ERROR_LABEL` 상수로.

### 2. `ner_utils/file_utils.py`

**함수 추출로 중복 제거** — "한 줄당 문서 하나, 빈 줄 무시" 분리 로직이
`app.py` 의 `split_documents()` 와 `load_documents_from_file()` 에 중복.
`split_into_documents(text)` 로 추출하고 파일 로딩은 이를 재사용
(`path.read_text()` 로 단순화). `app.py` 는 자체 구현을 지우고 이 함수를 임포트.

### 3. `ner_utils/visualization.py`

**매직 값 → 명명 상수** — 함수 안에 흩어져 있던 팔레트 목록을 모듈 상수
`SEABORN_PALETTES`/`QUALITATIVE_PALETTES`/`MATPLOTLIB_COLORMAPS`/`RECOMMENDED_PALETTES` 로 승격.
`validate_palette()` 의 경고 예시 목록(추천 목록의 부분 중복이었음)도 이 상수를 재사용.
막대 라벨의 `fontsize=9`, `xytext=(0, 3)` 은 `BAR_LABEL_FONTSIZE`/`BAR_LABEL_OFFSET_POINTS` 로.

**제너레이터 표현식으로 조건문 단순화** — `choose_font()` 의
"루프 + `continue` + 루프 안 return" 구조를 `next()` + 제너레이터 표현식으로 교체하고,
못 찾은 경우를 guard clause 로 먼저 처리. rcParams 적용은 `_apply_font_rcparams()` 로 추출.

```python
# Before
for name in candidates:
    if name not in available:
        continue
    plt.rcParams[...] = ...   # 적용 + 반환이 루프 안에
    ...
    return name, ...
# (루프를 다 돌면) 경고 후 return '', None

# After
chosen = next((name for name in candidates if name in available), None)
if chosen is None:            # guard clause
    ...경고...
    return '', None
_apply_font_rcparams(chosen)
```

**컴프리헨션 + 함수 추출** — `build_pii_report_text()` 의 이중 루프를
한 줄 포맷터 `_format_pii_entity_line()` 추출 후 중첩 컴프리헨션으로 재구성(출력 동일).

**루프 밖으로 반복 제거(데이터 주도 루프)** — `plot_entity_overview()`/`plot_pii_overview()` 의
"빌더 호출 → `save_fig`" 반복을 `(Figure, 파일명)` 목록 + 단일 저장 루프로 정리.

**이름 정리** — `p`→`bar`(막대 패치), `f`→`font`(폰트 목록 순회).

### 4. `app.py`

**긴 함수 분해 (Extract Method)** — 44줄짜리 `analyze()` 를 역할별 함수로 분해:

- `resolve_pii_language()` — `'auto'` 드롭다운 값 → API 언어 힌트(None) 변환
- `make_ner_figures()` — NER 요약 Figure 3종 생성(빈 df 면 guard clause 로 None 3개)
- `analyze_pii()` — PII 실행 → (df, Figure 2종, 리포트) 반환
- `format_status()` — 상태 문자열 조립

분해 후 `analyze()` 는 "입력 검증 → 인증 → NER → (옵션)PII → 상태" 흐름만 남아
Gradio outputs 와의 대응이 한눈에 보임. NER/PII 호출은 새 공용 함수
`recognize_entities_df`/`recognize_pii_df` 로 교체.

**매직 값 → 명명 상수** — `'auto'` 센티널을 `AUTO_LANGUAGE` 상수로
(`LANGUAGE_CHOICES`·드롭다운 기본값·언어 변환이 모두 이 상수를 참조).

**이름 정리** — `conf_fig`→`confidence_fig`, `split_documents`(자체 구현)
→ `split_into_documents`(패키지 공용) 등.

### 5. `visualize_output.py`

- 문서 결정 `if/else` 4줄을 `resolve_documents()` 함수 추출 + 조건 표현식으로.
- PII 3단계 중복 로직을 `recognize_pii_df()` 호출 한 줄로 교체 (NER 도 동일).
- `--list-palettes` 출력 루프를 `print('\n'.join(...))` 한 줄로.

### 6. `ner_utils/__init__.py`

새 공용 함수 `recognize_entities_df`·`recognize_pii_df`·`split_into_documents` 를
패키지 공개 API(`__all__`)에 추가.

## 검증

동작 보존을 다음으로 확인했습니다 (0708 `.venv` 사용):

1. **스모크 테스트** — `split_into_documents`·`validate_palette`·플롯 빌더 4종·
   `build_pii_report_text`(리팩토링 전과 바이트 단위 동일 출력)·
   `collect_results_df`(오류 문서 건너뛰기, mock 응답)·`app` 모듈 임포트(Gradio Blocks 구성)·
   `resolve_pii_language`/`format_status`/`make_ner_figures` — 전부 통과.
2. **CLI 엔드투엔드** — `python visualize_output.py --list-palettes`,
   기본 문서 NER 플롯 3종 저장, PII 포함 샘플 파일로 `--pii --language en` 실행 시
   PII 플롯 2종 + `pii_redacted_texts.txt` 까지 정상 저장.

## 7. 후속 작업 (같은 날) — Gradio 앱 Plotly 전환

[gr.Plot 공식 문서](https://gradio.app/docs/gradio/plot) 기준으로,
**Gradio 를 사용할 때만** 플롯을 matplotlib → **Plotly** 로 전환했습니다.
gr.Plot 은 Plotly Figure 를 반환하면 줌·호버 툴팁이 되는 인터랙티브 차트로 렌더링합니다.

### 변경 내용

- **`ner_utils/plotly_figures.py` 신규** — 기존 matplotlib 빌더와 1:1 대응하는
  Plotly 빌더 4종(`make_count_by_category_plotly`·`make_confidence_plotly`·
  `make_length_by_category_plotly`·`make_pii_top_texts_plotly`).
  - 팔레트 드롭다운(seaborn 팔레트 이름)은 `sns.color_palette(...).as_hex()` 로
    Plotly 색 목록으로 변환해 그대로 동작.
  - 한글은 브라우저 폰트로 렌더링되므로 matplotlib 의 `font_prop` 지정이 불필요.
- **`app.py`** — `make_ner_figures()`/`analyze_pii()` 가 Plotly 빌더 사용.
  이에 따라 `matplotlib` 임포트·`matplotlib.use('Agg')`·`choose_font()`/`FONT_PROP`·
  `sns.set_theme()` 제거.
  - `gr.Plot(format='png')` 의 `format` 제거 — 공식 문서상 **`format` 은 matplotlib
    전용 파라미터**라 Plotly 에는 적용되지 않음.
- **CLI(`visualize_output.py`)와 `ner_utils/visualization.py` 는 변경 없음** —
  PNG 저장은 matplotlib 유지. Plotly 는 웹앱에서만 사용.
- `requirements.txt` 에 `plotly==6.8.0` 추가 (venv 에서 `pip freeze` 재생성).

### 검증 (Plotly 전환)

1. Plotly 빌더 4종이 샘플 DataFrame 으로 `plotly.graph_objects.Figure` 정상 생성
   (무효 팔레트 → `validate_palette` 폴백 경로 포함).
2. **실서버 엔드투엔드** — 앱을 로컬(포트 7861)로 기동 후 `gradio_client` 로
   `/analyze` API 호출(실제 Azure NER+PII 실행): 상태 문자열 정상,
   플롯 5개 모두 `type: 'plotly'` 로 직렬화, PII 리포트 정상 반환.
