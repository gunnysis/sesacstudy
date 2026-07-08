"""NER/PII 결과 시각화 유틸리티.

matplotlib/seaborn 기반의 요약 플롯 헬퍼와, 한글 렌더링을 위한
폰트 선택 유틸리티를 제공합니다.

플롯은 Figure 를 반환하는 make_*_fig 빌더와, 그것을 PNG 로 저장하는
plot_*_overview(CLI 용)로 나뉩니다 — Gradio 앱은 빌더가 반환한 Figure 를
gr.Plot 에 그대로 전달합니다.
"""

from pathlib import Path

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns

DEFAULT_PALETTE = 'deep'

# 추천 팔레트 — seaborn 기본, 정성적(qualitative), matplotlib 컬러맵 순
SEABORN_PALETTES = ['deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind']
QUALITATIVE_PALETTES = ['Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2']
MATPLOTLIB_COLORMAPS = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
RECOMMENDED_PALETTES = SEABORN_PALETTES + QUALITATIVE_PALETTES + MATPLOTLIB_COLORMAPS

# 막대 위 값 라벨 스타일
BAR_LABEL_FONTSIZE = 9
BAR_LABEL_OFFSET_POINTS = (0, 3)

# 한글 지원 가능성이 높은 폰트 후보 (우선순위 순)
KOREAN_FONT_CANDIDATES = [
    'Malgun Gothic',
    'Malgun Gothic Semilight',
    'Noto Sans KR',
    'Noto Serif KR',
    'Yu Gothic',
    'Yu Gothic UI',
    'Yu Gothic UI Semibold',
    'Yu Gothic UI Semilight',
    'MS Gothic',
    'MS PGothic',
    'MS UI Gothic',
    'NanumGothic',
    'Noto Sans CJK KR',
    'AppleGothic',
]


def save_fig(fig, path: Path) -> None:
    """Figure 를 path 에 저장합니다. 출력 폴더도 함께 보장합니다."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    print('Saved', path)


def add_bar_labels(ax, font_prop=None) -> None:
    """막대그래프의 각 막대 위에 값을 표시합니다."""
    for bar in ax.patches:
        height = int(bar.get_height())
        if height <= 0:
            continue
        kwargs = dict(
            ha='center',
            va='bottom',
            fontsize=BAR_LABEL_FONTSIZE,
            color='black',
            xytext=BAR_LABEL_OFFSET_POINTS,
            textcoords='offset points',
        )
        if font_prop is not None:
            kwargs['fontproperties'] = font_prop
        ax.annotate(f'{height}', (bar.get_x() + bar.get_width() / 2., height), **kwargs)


def style_axes(ax, title: str, xlabel: str | None = None, ylabel: str | None = None, font_prop=None, rotate_xticks: bool = False) -> None:
    """제목·축 라벨·눈금 라벨에 일관된 스타일(폰트 포함)을 적용합니다."""
    ax.set_title(title, fontproperties=font_prop)
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontproperties=font_prop)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontproperties=font_prop)
    if rotate_xticks:
        ax.tick_params(axis='x', rotation=45)
    if font_prop is not None:
        for lbl in ax.get_xticklabels() + ax.get_yticklabels():
            lbl.set_fontproperties(font_prop)


def _apply_font_rcparams(font_name: str) -> None:
    """선택된 폰트를 matplotlib 전역 설정에 적용합니다."""
    plt.rcParams['font.family'] = font_name
    plt.rcParams['font.sans-serif'] = [font_name]
    plt.rcParams['axes.unicode_minus'] = False


def choose_font(preferred: str | None = None):
    """한글을 지원하는 폰트를 선택해 matplotlib 전역에 적용합니다.

    preferred 가 설치돼 있으면 우선 사용하고, 없으면 후보 목록에서 찾습니다.
    (font_name, FontProperties 또는 None) 튜플을 반환합니다.
    """
    available = {font.name for font in fm.fontManager.ttflist}
    candidates = ([preferred] if preferred else []) + KOREAN_FONT_CANDIDATES
    chosen = next((name for name in candidates if name in available), None)

    if chosen is None:
        plt.rcParams['axes.unicode_minus'] = False
        print(
            'Warning: No known Korean-capable fonts found in the system font list. '
            'Korean text may render incorrectly.'
        )
        return '', None

    _apply_font_rcparams(chosen)
    try:
        font_path = fm.findfont(chosen)
        return chosen, fm.FontProperties(fname=font_path, family=chosen)
    except Exception:
        return chosen, fm.FontProperties(family=chosen)


def validate_palette(palette_name: str) -> str:
    """seaborn 에서 유효한 팔레트면 그대로, 아니면 경고 후 기본값을 반환합니다."""
    try:
        sns.color_palette(palette_name)
        return palette_name
    except Exception:
        print(
            f"Warning: '{palette_name}' is not a valid palette. "
            f"Falling back to '{DEFAULT_PALETTE}'. Try: {', '.join(RECOMMENDED_PALETTES)}"
        )
        return DEFAULT_PALETTE


def get_recommended_palettes() -> list[str]:
    """추천 seaborn/matplotlib 팔레트 이름 목록을 반환합니다."""
    return list(RECOMMENDED_PALETTES)


# ---------------------------------------------------------------------------
# Figure 빌더 — Figure 를 반환만 하고 저장하지 않습니다 (Gradio gr.Plot 호환).
# plt.close(fig) 는 pyplot 전역 상태에서 분리할 뿐, 이후 savefig/렌더링은 가능합니다.
# ---------------------------------------------------------------------------

def make_count_by_category_fig(df, category_col: str, title: str,
                               palette: str = DEFAULT_PALETTE, font_prop=None):
    """카테고리별 개수 countplot Figure (공통 스타일 + 값 라벨)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    order = df[category_col].value_counts().index
    # seaborn 0.13+: hue 없이 palette 만 주면 deprecated — hue 지정 후 범례 숨김
    sns.countplot(data=df, x=category_col, order=order,
                  hue=category_col, hue_order=order,
                  palette=palette, legend=False, ax=ax)
    style_axes(ax, title, xlabel='Category', ylabel='Count',
               font_prop=font_prop, rotate_xticks=True)
    add_bar_labels(ax, font_prop=font_prop)
    fig.tight_layout()
    plt.close(fig)
    return fig


def make_confidence_fig(df, palette: str = DEFAULT_PALETTE, font_prop=None):
    """신뢰도 점수 분포 histplot Figure."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['confidence'], bins=20, kde=True,
                 color=sns.color_palette(palette)[0], ax=ax)
    style_axes(ax, 'Confidence Score Distribution',
               xlabel='Confidence', ylabel='Count', font_prop=font_prop)
    fig.tight_layout()
    plt.close(fig)
    return fig


def make_length_by_category_fig(df, palette: str = DEFAULT_PALETTE, font_prop=None):
    """카테고리별 엔터티 길이 boxplot Figure."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='category', y='length',
                hue='category', palette=palette, legend=False, ax=ax)
    style_axes(ax, 'Entity Length by Category',
               xlabel='Category', ylabel='Length (chars)',
               font_prop=font_prop, rotate_xticks=True)
    fig.tight_layout()
    plt.close(fig)
    return fig


def make_pii_top_texts_fig(df, palette: str = DEFAULT_PALETTE, font_prop=None, top_n: int = 20):
    """상위 PII 텍스트 가로 barplot Figure."""
    top = df['text'].value_counts().head(top_n)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=top.values, y=top.index,
                hue=top.index, palette=palette, legend=False, ax=ax)
    style_axes(ax, 'Top PII Entity Texts', xlabel='Count', font_prop=font_prop)
    add_bar_labels(ax, font_prop=font_prop)
    fig.tight_layout()
    plt.close(fig)
    return fig


def _format_pii_entity_line(row) -> str:
    """PII 엔터티 한 건을 리포트 한 줄로 포맷합니다."""
    return f"  - {row['text']} ({row['category']}, conf={row['confidence']:.2f})"


def build_pii_report_text(df) -> str:
    """문서별 PII 엔터티 목록을 리포트 문자열로 만듭니다."""
    lines = [
        line
        for doc_id, group in df.groupby('document_id')
        for line in (
            [f'Document {doc_id} PII entities:']
            + [_format_pii_entity_line(row) for _, row in group.iterrows()]
            + ['']
        )
    ]
    return '\n'.join(lines) + '\n' if lines else ''


# ---------------------------------------------------------------------------
# CLI 용 — 빌더가 만든 Figure 를 PNG/텍스트 파일로 저장합니다.
# ---------------------------------------------------------------------------

def plot_entity_overview(df, out_dir: Path, palette: str = DEFAULT_PALETTE, font_prop=None):
    """NER 결과 요약 플롯 3종(카테고리별 개수·신뢰도 분포·길이 분포)을 저장합니다."""
    if df.empty:
        print('No entities to plot.')
        return

    sns.set_theme(style='whitegrid', palette=palette)

    figures = [
        (make_count_by_category_fig(df, 'category', 'Entity Counts by Category',
                                    palette=palette, font_prop=font_prop),
         'entity_counts_by_category.png'),
        (make_confidence_fig(df, palette=palette, font_prop=font_prop),
         'confidence_distribution.png'),
        (make_length_by_category_fig(df, palette=palette, font_prop=font_prop),
         'length_by_category.png'),
    ]
    for fig, filename in figures:
        save_fig(fig, out_dir / filename)


def write_pii_report(df, out_path: Path) -> None:
    """문서별 PII 엔터티 목록을 텍스트 파일로 기록합니다."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_pii_report_text(df), encoding='utf-8')
    print('Saved', out_path)


def plot_pii_overview(df, out_dir: Path, palette: str = DEFAULT_PALETTE, font_prop=None):
    """PII 결과 요약 플롯과 문서별 엔터티 리포트를 저장합니다."""
    if df.empty:
        print('No PII entities to plot.')
        return

    sns.set_theme(style='whitegrid', palette=palette)

    figures = [
        (make_count_by_category_fig(df, 'category', 'PII Counts by Category',
                                    palette=palette, font_prop=font_prop),
         'pii_counts_by_category.png'),
        (make_pii_top_texts_fig(df, palette=palette, font_prop=font_prop),
         'pii_top_texts.png'),
    ]
    for fig, filename in figures:
        save_fig(fig, out_dir / filename)

    write_pii_report(df, out_dir / 'pii_redacted_texts.txt')
