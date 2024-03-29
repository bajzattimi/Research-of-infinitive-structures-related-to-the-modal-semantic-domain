import sys
from itertools import chain
from functools import partial
from collections import Counter

from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.clause_splitter import get_clauses
from mosaic_lib.filter import parse_filter_params, filter_sentence
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


def create_window(inp_fh, out_fh, keep_duplicates=False,
                  filter_params=((), (), None)):

    any_tok, cur_tok = filter_params[0:2]

    c = Counter()
    all_elem = 0
    uniq_clauses = set()

    stats = {'deleted by rule': 0, 'duplicate clauses': 0
             }

    n = 0
    header = next(inp_fh)
    enum_fields_fun = partial(enum_fields_for_tok, fields=header.rstrip().split('\t'))
    print(header, end='', file=out_fh)
    for n, (comment_lines, sent) in enumerate(parse_emtsv_format(chain([header], inp_fh)), start=1):

        # From punct to punct
        clause, kwic_start, kwic_stop = get_clauses(comment_lines, sent)

        clause_window = clause
        """
        # Debug
        if kwic_inf_window_stop - kwic_inf_window_start > 5:
            print(kwic_inf_window_stop - kwic_inf_window_start,
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause_window))
        """
        clause_str = ' '.join(tok['form'] for tok in clause_window)
        clause_window_orig_str = '\n'.join('\t'.join(enum_fields_fun(tok, prefix_lemma=False)) for tok in clause_window)
        # Filter clauses
        delete_ex = filter_sentence(clause_window, any_tok, cur_tok, clause_str)
        if delete_ex:
            stats['deleted by rule'] += 1
            continue

        # Print
        if keep_duplicates or clause_str not in uniq_clauses:
            uniq_clauses.add(clause_str)
            for comment_line in comment_lines:
                print('# ', comment_line, file=out_fh)
            print('# clause:', clause_str, file=out_fh)
            # Replace # characters before converting it to '#SV' format
            print('# clause_SPL:',
                  ' '.join('#'.join(enum_fields_fun({k: v.replace('#', '\\u0023') for k, v in tok.items()}))
                           for tok in clause_window), file=out_fh)
            # This is the vertical formated part
            print(clause_window_orig_str, file=out_fh)
            print(file=out_fh)
        else:
            print('INFO:', 'DUPLICATE CLAUSE', clause_str, file=sys.stderr)
            stats['duplicate clauses'] += 1
        c[len(clause_window)] += 1
        all_elem += 1

    print('', *range(2, 10), sep='\t', file=sys.stderr)
    # 1st column of the first row
    print(inp_fh.name, end='\t', file=sys.stderr)
    for i in range(2, 10):
        print(f'{(c[i]/all_elem)*100}%', end='\t', file=sys.stderr)
    print(file=sys.stderr)
    stats['remaining'] = all_elem - stats['duplicate clauses']
    for name, sent_num in stats.items():
        print('REPORT:', name, sent_num, 'sents', f'{(sent_num/n)*100}%', file=sys.stderr)
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-k', '--keep-duplicates', dest='keep_duplicates', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, keep_duplicates=args.keep_duplicates,
                                    filter_params=args.filter_params)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
