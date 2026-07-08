"""Azure NER/PII 분석을 웹 UI 로 제공하는 Gradio 앱.

텍스트박스에 한 줄당 문서 하나를 입력하면 NER(엔터티 인식) 결과 표와
요약 플롯을, 옵션에 따라 PII 인식 결과까지 보여줍니다.
플롯은 matplotlib Figure 를 gr.Plot 에 직접 전달해 렌더링합니다.
실행: python app.py  (기본 http://127.0.0.1:7860)
"""

import dotenv
import gradio as gr
import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use('Agg')  # 서버 환경 — GUI 백엔드 없이 이미지로만 렌더링

from ner_utils import (
    authenticate_client,
    build_pii_report_text,
    choose_font,
    collect_results_df,
    extract_entities_to_df,
    extract_pii_to_df,
    get_recommended_palettes,
    make_confidence_fig,
    make_count_by_category_fig,
    make_length_by_category_fig,
    make_pii_top_texts_fig,
    validate_palette,
)

dotenv.load_dotenv()

_, FONT_PROP = choose_font()

EXAMPLE_TEXT = """
이름: kim minseok
전화번호: 010-1234-5678
주소: 서울특별시 강남구 테헤란로 123
신용카드 번호: 1234-5678-9012-3456
주민등록번호: 900101-1234567
"""

LANGUAGE_CHOICES = ['auto', 'ko', 'en']

_client = None


def get_client():
    """Azure 클라이언트를 최초 요청 시 한 번만 생성합니다."""
    global _client
    if _client is None:
        _client = authenticate_client()
    return _client


def split_documents(text: str) -> list[str]:
    """텍스트박스 입력을 한 줄당 문서 하나로 분리합니다(빈 줄 무시)."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def analyze(text: str, run_pii: bool, language: str, palette: str):
    """NER(+선택적 PII)을 실행해 결과 표·플롯 Figure·PII 리포트를 반환합니다."""
    docs = split_documents(text or '')
    if not docs:
        raise gr.Error('분석할 텍스트를 입력하세요 (한 줄당 문서 하나).')

    try:
        client = get_client()
    except EnvironmentError as e:
        raise gr.Error(f'Azure 인증 실패: {e} — .env 의 LANGUAGE_KEY/LANGUAGE_ENDPOINT 를 확인하세요.')

    palette = validate_palette(palette)
    sns.set_theme(style='whitegrid', palette=palette)

    ner_response = client.recognize_entities(documents=docs)
    entity_df = collect_results_df(ner_response, extract_entities_to_df, 'Document')

    count_fig = conf_fig = length_fig = None
    if not entity_df.empty:
        count_fig = make_count_by_category_fig(
            entity_df, 'category', 'Entity Counts by Category',
            palette=palette, font_prop=FONT_PROP)
        conf_fig = make_confidence_fig(entity_df, palette=palette, font_prop=FONT_PROP)
        length_fig = make_length_by_category_fig(entity_df, palette=palette, font_prop=FONT_PROP)

    pii_df = pd.DataFrame()
    pii_count_fig = pii_top_fig = None
    pii_report = ''
    if run_pii:
        pii_kwargs = {'language': language} if language != 'auto' else {}
        pii_response = client.recognize_pii_entities(documents=docs, **pii_kwargs)
        pii_df = collect_results_df(pii_response, extract_pii_to_df, 'PII Document')
        if not pii_df.empty:
            pii_count_fig = make_count_by_category_fig(
                pii_df, 'category', 'PII Counts by Category',
                palette=palette, font_prop=FONT_PROP)
            pii_top_fig = make_pii_top_texts_fig(pii_df, palette=palette, font_prop=FONT_PROP)
            pii_report = build_pii_report_text(pii_df)

    status = f'문서 {len(docs)}개 분석 완료 — 엔터티 {len(entity_df)}건'
    if run_pii:
        status += f', PII {len(pii_df)}건'

    return (status, entity_df, count_fig, conf_fig, length_fig,
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
                LANGUAGE_CHOICES, value='auto', label='PII 언어 힌트')
            palette_dropdown = gr.Dropdown(
                get_recommended_palettes(), value='deep', label='색상 팔레트')
            analyze_btn = gr.Button('분석 실행', variant='primary')

    status_box = gr.Textbox(label='상태', interactive=False)

    # gr.Plot 사용법은 공식 문서(https://gradio.app/docs/gradio/plot) 기준:
    # 이벤트 함수가 matplotlib Figure 를 반환하면 gr.Plot 이 렌더링.
    # format 은 matplotlib 플롯의 전송 형식(기본 webp) — 문서 데모와 같이 png 지정.
    with gr.Tab('NER 결과'):
        entity_table = gr.Dataframe(label='엔터티 목록')
        with gr.Row():
            entity_count_plot = gr.Plot(label='카테고리별 엔터티 수', format='png')
            confidence_plot = gr.Plot(label='신뢰도 분포', format='png')
            length_plot = gr.Plot(label='카테고리별 길이', format='png')

    with gr.Tab('PII 결과'):
        pii_table = gr.Dataframe(label='PII 엔터티 목록')
        with gr.Row():
            pii_count_plot = gr.Plot(label='카테고리별 PII 수', format='png')
            pii_top_plot = gr.Plot(label='상위 PII 텍스트', format='png')
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
