"""Azure Text Analytics 로 NER/PII 를 실행하고 결과를 플롯으로 저장하는 CLI."""

import argparse
from pathlib import Path

import dotenv

from ner_utils import (
    authenticate_client,
    choose_font,
    collect_results_df,
    extract_entities_to_df,
    extract_pii_to_df,
    get_recommended_palettes,
    load_documents_from_file,
    plot_entity_overview,
    plot_pii_overview,
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


def main():
    args = build_arg_parser().parse_args()

    if args.list_palettes:
        for p in get_recommended_palettes():
            print(p)
        return

    if args.input_file:
        docs = load_documents_from_file(Path(args.input_file))
    else:
        docs = DEFAULT_DOCS

    chosen_font, font_prop = choose_font(args.font)
    if chosen_font:
        print(f'Using font: {chosen_font}')

    palette = validate_palette(args.palette)
    out_dir = Path(args.out_dir)
    client = authenticate_client()

    ner_response = client.recognize_entities(documents=docs)
    entity_df = collect_results_df(ner_response, extract_entities_to_df, 'Document')
    plot_entity_overview(entity_df, out_dir, palette=palette, font_prop=font_prop)

    if args.pii:
        pii_kwargs = {'language': args.language} if args.language else {}
        pii_response = client.recognize_pii_entities(documents=docs, **pii_kwargs)
        pii_df = collect_results_df(pii_response, extract_pii_to_df, 'PII Document')
        plot_pii_overview(pii_df, out_dir, palette=palette, font_prop=font_prop)


if __name__ == '__main__':
    main()
