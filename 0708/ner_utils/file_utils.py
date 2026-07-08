"""NER/PII 워크플로에서 쓰는 문서 로딩 유틸리티."""

from pathlib import Path


def load_documents_from_file(path: Path) -> list[str]:
    """텍스트 파일에서 문서를 읽습니다(한 줄당 문서 하나, 빈 줄 무시)."""
    with path.open('r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
