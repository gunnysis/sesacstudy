"""Azure Text Analytics 헬퍼 — NER/PII 인증과 결과 변환.

Azure Text Analytics 응답을 시각화에 쓰기 좋은 DataFrame 으로 변환하는
헬퍼를 제공합니다.
"""

import os

import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def authenticate_client() -> TextAnalyticsClient:
    """환경변수(LANGUAGE_KEY/LANGUAGE_ENDPOINT)로 인증된 클라이언트를 반환합니다."""
    language_key = os.getenv('LANGUAGE_KEY')
    language_endpoint = os.getenv('LANGUAGE_ENDPOINT')
    if not language_key or not language_endpoint:
        raise EnvironmentError('LANGUAGE_KEY and LANGUAGE_ENDPOINT must be set in the environment')
    return TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=AzureKeyCredential(language_key),
    )


def _entities_to_df(entities, doc_id: int, include_subcategory: bool) -> pd.DataFrame:
    """엔터티 목록을 DataFrame 으로 변환하는 공통 로직.

    PII 엔터티에는 subcategory 속성이 없어 include_subcategory 로 구분합니다.
    """
    rows = []
    for entity in entities:
        row = {
            'document_id': doc_id,
            'text': entity.text,
            'category': entity.category,
        }
        if include_subcategory:
            row['subcategory'] = entity.subcategory or ''
        row.update(
            confidence=float(entity.confidence_score),
            length=int(entity.length),
            offset=int(entity.offset),
        )
        rows.append(row)
    return pd.DataFrame(rows)


def extract_entities_to_df(result, doc_id: int = 0) -> pd.DataFrame:
    """NER(엔터티 인식) 결과를 DataFrame 으로 변환합니다."""
    return _entities_to_df(result.entities, doc_id, include_subcategory=True)


def extract_pii_to_df(pii_result, doc_id: int = 0) -> pd.DataFrame:
    """PII 인식 결과를 DataFrame 으로 변환합니다."""
    return _entities_to_df(pii_result.entities, doc_id, include_subcategory=False)


def collect_results_df(response, extractor, label: str) -> pd.DataFrame:
    """응답의 문서별 결과를 extractor 로 변환해 하나의 DataFrame 으로 합칩니다.

    오류 문서는 건너뛰고 메시지만 출력합니다.
    """
    df_list = []
    for i, doc_result in enumerate(response):
        if doc_result.is_error:
            print(f'{label} {i} error: {doc_result.error}')
            continue
        df_list.append(extractor(doc_result, doc_id=i))
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    return pd.DataFrame()
