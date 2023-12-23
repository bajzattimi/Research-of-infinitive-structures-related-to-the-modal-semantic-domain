import sys
from itertools import chain
from functools import partial

from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.filter import parse_filter_params
from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def enum_fields_for_tok(tok, fields, prefix_lemma=True):
    ret = []
    for field in fields:
        field_val = tok.get(field)
        if field_val is not None:
            if field == 'lemma' and prefix_lemma:
                ret.append(f'lemma:{field_val}')
            else:
                ret.append(field_val)
    return ret


def create_window(inp_fh, out_fh, keep_duplicate=False, lower_sent_start=True, filter_params=((), (), None)):

    substitute_tags = filter_params[2]
    if substitute_tags is None:
        substitute_tags = {}

    all_elem = 0
    uniq_clauses = set()

    stats = {'duplicate clauses': 0}

    n = 0
    header = next(inp_fh)
    enum_fields_fun = partial(enum_fields_for_tok, fields=header.rstrip().split('\t'))
    print(header, end='', file=out_fh)
    for n, (comment_lines, sent_orig) in enumerate(parse_emtsv_format(chain([header], inp_fh)), start=1):
        sent = [{'form': tok['form'], 'lemma': tok['lemma'],
                 'xpostag': substitute_tags.get(tok['xpostag'], tok['xpostag'])}
                for tok in sent_orig]

        if lower_sent_start:
            sent[0]['form'] = sent[0]['form'].lower()  # Unify stentence start

        sent_str = ' '.join(tok['form'] for tok in sent)

        # Print
        if not keep_duplicate and sent_str not in uniq_clauses:
            uniq_clauses.add(sent_str)
            for comment_line in comment_lines:
                print('# ', comment_line, file=out_fh)
            for tok in sent:
                print(*enum_fields_fun(tok, prefix_lemma=False), sep='\t', file=out_fh)
            print(file=out_fh)
        else:
            print('INFO:', 'DUPLICATE CLAUSE', sent_str, file=sys.stderr)
            stats['duplicate clauses'] += 1
        all_elem += 1

    sent_num = all_elem - stats['duplicate clauses']
    print(f'{inp_fh.name}\tremaining {sent_num} sents {(sent_num/n)*100}%', file=sys.stderr)
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-k', '--keep-duplicate', dest='keep_duplicate', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-l', '--lower-sent-start', dest='lower_sent_start', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, lower_sent_start=args.lower_sent_start,
                                    keep_duplicate=args.keep_duplicate, filter_params=args.filter_params)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
