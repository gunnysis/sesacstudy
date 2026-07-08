"""Azure NER/PII 분석을 웹 UI 로 제공하는 Gradio 앱.

텍스트박스에 한 줄당 문서 하나를 입력하면 NER(엔터티 인식) 결과 표와
요약 플롯을, 옵션에 따라 PII 인식 결과까지 보여줍니다.
플롯은 Plotly Figure 를 gr.Plot 에 전달해 인터랙티브(줌·호버 툴팁)로
렌더링합니다 — CLI(visualize_output.py)의 PNG 저장은 matplotlib 그대로.
실행: python app.py  (기본 http://127.0.0.1:7860)
"""

import dotenv
import gradio as gr
import pandas as pd

from ner_utils import (
    authenticate_client,
    build_pii_report_text,
    get_recommended_palettes,
    make_confidence_plotly,
    make_count_by_category_plotly,
    make_length_by_category_plotly,
    make_pii_top_texts_plotly,
    recognize_entities_df,
    recognize_pii_df,
    split_into_documents,
    validate_palette,
)

dotenv.load_dotenv()

EXAMPLE_TEXT = """
이름: kim minseok
전화번호: 010-1234-5678
주소: 서울특별시 강남구 테헤란로 123
신용카드 번호: 1234-5678-9012-3456
주민등록번호: 900101-1234567
"""

AUTO_LANGUAGE = 'auto'  # 서비스가 언어를 자동 감지하도록 하는 드롭다운 값
LANGUAGE_CHOICES = [AUTO_LANGUAGE, 'ko', 'en']

_client = None


def get_client():
    """Azure 클라이언트를 최초 요청 시 한 번만 생성합니다."""
    global _client
    if _client is None:
        _client = authenticate_client()
    return _client


def resolve_pii_language(language: str) -> str | None:
    """드롭다운 값('auto' 포함)을 API 에 넘길 언어 힌트로 변환합니다."""
    return None if language == AUTO_LANGUAGE else language


def make_ner_figures(entity_df, palette: str) -> tuple:
    """NER 결과 요약 Plotly Figure 3종(개수·신뢰도·길이). 결과가 없으면 None 3개."""
    if entity_df.empty:
        return None, None, None
    count_fig = make_count_by_category_plotly(
        entity_df, 'category', 'Entity Counts by Category', palette=palette)
    confidence_fig = make_confidence_plotly(entity_df, palette=palette)
    length_fig = make_length_by_category_plotly(entity_df, palette=palette)
    return count_fig, confidence_fig, length_fig


def analyze_pii(client, docs: list[str], language: str, palette: str) -> tuple:
    """PII 인식을 실행해 (결과 df, 개수 Figure, 상위 텍스트 Figure, 리포트)를 반환합니다."""
    pii_df = recognize_pii_df(client, docs, language=resolve_pii_language(language))
    if pii_df.empty:
        return pii_df, None, None, ''
    count_fig = make_count_by_category_plotly(
        pii_df, 'category', 'PII Counts by Category', palette=palette)
    top_fig = make_pii_top_texts_plotly(pii_df, palette=palette)
    report = build_pii_report_text(pii_df)
    return pii_df, count_fig, top_fig, report


def format_status(doc_count: int, entity_count: int, pii_count: int | None = None) -> str:
    """분석 결과 요약 상태 문자열을 만듭니다 (pii_count 가 None 이면 PII 생략)."""
    status = f'문서 {doc_count}개 분석 완료 — 엔터티 {entity_count}건'
    if pii_count is not None:
        status += f', PII {pii_count}건'
    return status


def analyze(text: str, run_pii: bool, language: str, palette: str):
    """NER(+선택적 PII)을 실행해 결과 표·플롯 Figure·PII 리포트를 반환합니다."""
    docs = split_into_documents(text or '')
    if not docs:
        raise gr.Error('분석할 텍스트를 입력하세요 (한 줄당 문서 하나).')

    try:
        client = get_client()
    except EnvironmentError as e:
        raise gr.Error(f'Azure 인증 실패: {e} — .env 의 LANGUAGE_KEY/LANGUAGE_ENDPOINT 를 확인하세요.')

    palette = validate_palette(palette)

    entity_df = recognize_entities_df(client, docs)
    count_fig, confidence_fig, length_fig = make_ner_figures(entity_df, palette)

    if run_pii:
        pii_df, pii_count_fig, pii_top_fig, pii_report = analyze_pii(
            client, docs, language, palette)
    else:
        pii_df, pii_count_fig, pii_top_fig, pii_report = pd.DataFrame(), None, None, ''

    pii_count = len(pii_df) if run_pii else None
    status = format_status(len(docs), len(entity_df), pii_count)

    return (status, entity_df, count_fig, confidence_fig, length_fig,
            pii_df, pii_count_fig, pii_top_fig, pii_report)


with gr.Blocks(title='Azure NER/PII 시각화') as demo:
    gr.Markdown('# Azure NER/PII 분석 시각화\n'
                '텍스트박스에 **한 줄당 문서 하나**를 입력하고 분석 버튼을 누르세요.')

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label='분석할 문서 (한 줄당 문서 하나)',
                value=EXAMPLE_TEXT,
                lines=8,
                placeholder='예) I had a wonderful trip to Seattle last week.',
            )
        with gr.Column(scale=1):
            pii_checkbox = gr.Checkbox(label='PII 인식도 실행', value=True)
            language_dropdown = gr.Dropdown(
                LANGUAGE_CHOICES, value=AUTO_LANGUAGE, label='PII 언어 힌트')
            palette_dropdown = gr.Dropdown(
                get_recommended_palettes(), value='deep', label='색상 팔레트')
            analyze_btn = gr.Button('분석 실행', variant='primary')

    status_box = gr.Textbox(label='상태', interactive=False)

    # gr.Plot 사용법은 공식 문서(https://gradio.app/docs/gradio/plot) 기준:
    # 이벤트 함수가 Plotly Figure 를 반환하면 gr.Plot 이 인터랙티브로 렌더링.
    # (format 파라미터는 matplotlib 전용이라 Plotly 에서는 지정하지 않음)
    with gr.Tab('NER 결과'):
        entity_table = gr.Dataframe(label='엔터티 목록')
        with gr.Row():
            entity_count_plot = gr.Plot(label='카테고리별 엔터티 수')
            confidence_plot = gr.Plot(label='신뢰도 분포')
            length_plot = gr.Plot(label='카테고리별 길이')

    with gr.Tab('PII 결과'):
        pii_table = gr.Dataframe(label='PII 엔터티 목록')
        with gr.Row():
            pii_count_plot = gr.Plot(label='카테고리별 PII 수')
            pii_top_plot = gr.Plot(label='상위 PII 텍스트')
        pii_report_box = gr.Textbox(label='문서별 PII 리포트', lines=10, interactive=False)

    analyze_btn.click(
        analyze,
        inputs=[text_input, pii_checkbox, language_dropdown, palette_dropdown],
        outputs=[status_box, entity_table,
                 entity_count_plot, confidence_plot, length_plot,
                 pii_table, pii_count_plot, pii_top_plot, pii_report_box],
        api_name='analyze',
    )


if __name__ == '__main__':
    demo.launch(share=True)
