"""NER/PII 결과의 Plotly Figure 빌더 — Gradio 앱(gr.Plot) 전용.

gr.Plot 은 Plotly Figure 를 반환하면 인터랙티브 차트(줌·호버 툴팁)로
렌더링합니다(https://gradio.app/docs/gradio/plot). CLI 의 PNG 저장은
matplotlib 기반 visualization 모듈이 그대로 담당하고, 이 모듈은
웹 UI 에서만 사용합니다.

한글 텍스트는 브라우저 폰트로 렌더링되므로 matplotlib 처럼
폰트(font_prop)를 따로 지정할 필요가 없습니다.
"""

import plotly.express as px
import seaborn as sns

from .visualization import DEFAULT_PALETTE

PLOTLY_TEMPLATE = 'plotly_white'  # seaborn whitegrid 와 유사한 밝은 배경
XTICK_ANGLE = -45


def _palette_hex(palette: str, n_colors: int) -> list[str]:
    """seaborn 팔레트 이름을 Plotly 용 hex 색 목록으로 변환합니다."""
    return sns.color_palette(palette, n_colors).as_hex()


def make_count_by_category_plotly(df, category_col: str, title: str,
                                  palette: str = DEFAULT_PALETTE):
    """카테고리별 개수 막대 차트 Figure (값 라벨 포함)."""
    counts = df[category_col].value_counts()
    fig = px.bar(
        x=counts.index, y=counts.values,
        color=counts.index,
        color_discrete_sequence=_palette_hex(palette, len(counts)),
        text=counts.values,
        title=title,
        labels={'x': 'Category', 'y': 'Count'},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, xaxis_tickangle=XTICK_ANGLE)
    return fig


def make_confidence_plotly(df, palette: str = DEFAULT_PALETTE):
    """신뢰도 점수 분포 히스토그램 Figure."""
    fig = px.histogram(
        df, x='confidence', nbins=20,
        color_discrete_sequence=_palette_hex(palette, 1),
        title='Confidence Score Distribution',
        labels={'confidence': 'Confidence'},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(yaxis_title='Count')
    return fig


def make_length_by_category_plotly(df, palette: str = DEFAULT_PALETTE):
    """카테고리별 엔터티 길이 박스플롯 Figure."""
    categories = df['category'].nunique()
    fig = px.box(
        df, x='category', y='length',
        color='category',
        color_discrete_sequence=_palette_hex(palette, categories),
        title='Entity Length by Category',
        labels={'category': 'Category', 'length': 'Length (chars)'},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_layout(showlegend=False, xaxis_tickangle=XTICK_ANGLE)
    return fig


def make_pii_top_texts_plotly(df, palette: str = DEFAULT_PALETTE, top_n: int = 20):
    """상위 PII 텍스트 가로 막대 차트 Figure."""
    top = df['text'].value_counts().head(top_n)
    fig = px.bar(
        x=top.values, y=top.index, orientation='h',
        color=top.index,
        color_discrete_sequence=_palette_hex(palette, len(top)),
        text=top.values,
        title='Top PII Entity Texts',
        labels={'x': 'Count', 'y': 'Text'},
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition='outside')
    # value_counts 내림차순이 위에서부터 보이도록 y 축 반전
    fig.update_layout(showlegend=False, yaxis=dict(autorange='reversed'))
    return fig
