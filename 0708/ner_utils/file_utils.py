"""NER/PII 워크플로에서 쓰는 문서 로딩 유틸리티."""

from pathlib import Path


def split_into_documents(text: str) -> list[str]:
    """여러 줄 텍스트를 문서 목록으로 분리합니다(한 줄당 문서 하나, 빈 줄 무시)."""
    return [line.strip() for line in text.splitlines() if line.strip()]


def load_documents_from_file(path: Path) -> list[str]:
    """텍스트 파일에서 문서를 읽습니다(한 줄당 문서 하나, 빈 줄 무시)."""
    return split_into_documents(path.read_text(encoding='utf-8'))
