"""Azure Text Analytics 로 NER/PII 를 실행하고 결과를 플롯으로 저장하는 CLI."""

import argparse
from pathlib import Path

import dotenv

from ner_utils import (
    authenticate_client,
    choose_font,
    get_recommended_palettes,
    load_documents_from_file,
    plot_entity_overview,
    plot_pii_overview,
    recognize_entities_df,
    recognize_pii_df,
    validate_palette,
)

dotenv.load_dotenv()

DEFAULT_DOCS = ["I had a wonderful trip to Seattle last week."]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run NER and visualize output')
    parser.add_argument('--input-file', '-i', type=str,
                        help='Text file with one document per line')
    parser.add_argument('--out-dir', '-o', type=str,
                        default='plots', help='Directory to save plots')
    parser.add_argument('--pii', action='store_true',
                        help='Also run PII recognition and visualize results')
    parser.add_argument('--language', '-l', type=str,
                        default=None, help='Language hint for PII recognition (e.g. en)')
    parser.add_argument('--palette', type=str,
                        default='deep', help='Seaborn color palette to use for plots')
    parser.add_argument('--list-palettes', action='store_true',
                        help='List recommended palettes and exit')
    parser.add_argument('--font', type=str, default='Malgun Gothic',
                        help='Font name to use for plotting (helps render Korean)')
    return parser


def resolve_documents(input_file: str | None) -> list[str]:
    """--input-file 이 주어지면 파일에서, 아니면 기본 예제 문서를 반환합니다."""
    return load_documents_from_file(Path(input_file)) if input_file else DEFAULT_DOCS


def main():
    args = build_arg_parser().parse_args()

    if args.list_palettes:
        print('\n'.join(get_recommended_palettes()))
        return

    docs = resolve_documents(args.input_file)

    chosen_font, font_prop = choose_font(args.font)
    if chosen_font:
        print(f'Using font: {chosen_font}')

    palette = validate_palette(args.palette)
    out_dir = Path(args.out_dir)
    client = authenticate_client()

    entity_df = recognize_entities_df(client, docs)
    plot_entity_overview(entity_df, out_dir, palette=palette, font_prop=font_prop)

    if args.pii:
        pii_df = recognize_pii_df(client, docs, language=args.language)
        plot_pii_overview(pii_df, out_dir, palette=palette, font_prop=font_prop)


if __name__ == '__main__':
    main()
