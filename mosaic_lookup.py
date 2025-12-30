from functools import partial
from argparse import ArgumentTypeError

from mosaic_lib.scoring import mosaic_to_tok
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def create_window(inp_fh, out_fh, mosaic):
    # Replace previously escaped # characters before going any further
    mosaic = mosaic.replace('\\u0023', '#')
    mosaic_toks = mosaic_to_tok(mosaic.split())[0]  # Drop score
    mosaic_len = len(mosaic_toks)
    for sent_id, (comment_lines, sent) in enumerate(parse_emtsv_format(inp_fh)):
        clause_len = len(next((line for line in comment_lines if line.startswith('clause: ')))[8:].split())
        if clause_len != mosaic_len:  # TODO
            continue

        """
        for mosaic_word, word in zip(mosaic_toks, sent):
            if mosaic_word.items() > word.items():
                break
        else:
            print(' '.join(tok['form'] for tok in sent), file=out_fh)
        """
        if all(mosaic_word.items() <= word.items() for mosaic_word, word in zip(mosaic_toks, sent)):
            print(sent_id, ' '.join(tok['form'] for tok in sent), sep='\t', file=out_fh)
            # print(' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in sent), file=out_fh)


# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-m', '--mosaic', type=str, metavar='MOSAIC NGRAM', required=True)

    args = parser.parse_args()

    if args.parallel > 1 and args.output_path != '-':
        raise ArgumentTypeError(f'Output must be STDOUT if processing parallel ({args.output_path}) !')

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, mosaic=args.mosaic)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
