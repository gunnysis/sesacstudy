"""NER 유틸리티 패키지 — Azure 클라이언트·파일·시각화 헬퍼를 노출합니다."""

from .azure_text_analytics import (
    authenticate_client,
    collect_results_df,
    extract_entities_to_df,
    extract_pii_to_df,
)
from .file_utils import load_documents_from_file
from .visualization import (
    build_pii_report_text,
    choose_font,
    get_recommended_palettes,
    make_confidence_fig,
    make_count_by_category_fig,
    make_length_by_category_fig,
    make_pii_top_texts_fig,
    plot_entity_overview,
    plot_pii_overview,
    validate_palette,
    write_pii_report,
)

__all__ = [
    'authenticate_client',
    'collect_results_df',
    'extract_entities_to_df',
    'extract_pii_to_df',
    'load_documents_from_file',
    'build_pii_report_text',
    'choose_font',
    'get_recommended_palettes',
    'make_confidence_fig',
    'make_count_by_category_fig',
    'make_length_by_category_fig',
    'make_pii_top_texts_fig',
    'plot_entity_overview',
    'plot_pii_overview',
    'validate_palette',
    'write_pii_report',
]
