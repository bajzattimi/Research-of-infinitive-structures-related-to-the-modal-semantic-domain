import sys
from itertools import chain
from functools import partial
from collections import Counter

from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.clause_splitter import get_clauses
from mosaic_lib.filter import parse_filter_params, filter_sentence
from mosaic_lib.argparse_helpers import base_argparser_factory, int_greater_or_equal_than
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


def check_clause(clause, kwic_start, kwic_stop):
    inf_loc_min = max(0, kwic_start - 2)
    inf_loc_max = min(len(clause), kwic_stop + 2)
    # Sanity check: Has the sent clause or the window INF
    inf_in_clause = any(tok['xpostag'].startswith('[/V]') and tok['xpostag'].endswith('[Inf]')
                        for tok in clause)
    inf_ind = -1
    for inf_ind, tok in enumerate(clause[inf_loc_min:inf_loc_max], start=inf_loc_min):
        if tok['xpostag'].startswith('[/V]') and tok['xpostag'].endswith('[Inf]'):
            inf_in_window = True
            break
    else:
        inf_in_window = False
    return inf_in_clause, inf_in_window, inf_ind


def create_window(inp_fh, out_fh, left_window: int = 3, right_window: int = 3, keep_duplicates=False,
                  filter_params=((), (), None)):

    any_tok, cur_tok = filter_params[0:2]

    c = Counter()
    all_elem = 0
    uniq_clauses = set()

    stats = {'deleted by rule': 0, 'duplicate clauses': 0,
             'inf too far': 0, 'without inf': 0
             }

    n = 0
    header = next(inp_fh)
    enum_fields_fun = partial(enum_fields_for_tok, fields=header.rstrip().split('\t'))
    print(header, end='', file=out_fh)
    for n, (comment_lines, sent) in enumerate(parse_emtsv_format(chain([header], inp_fh)), start=1):

        clause, kwic_start, kwic_stop = get_clauses(comment_lines, sent)

        # Make additional checks based on FIN-INF distance
        inf_in_clause, inf_in_window, inf_ind = check_clause(clause, kwic_start, kwic_stop)
        if not inf_in_window and inf_in_clause:
            print("WARNING: INF IS TO FAR FROM THE FINITE VERB:",
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause), file=sys.stderr)
            stats['inf too far'] += 1
            continue
        elif not inf_in_clause:
            print("WARNING: FILTERING CLAUSES WITHOUT INF:",
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause), file=sys.stderr)
            stats['without inf'] += 1
            continue

        # Sent clause start or (inf/kwic (either comes first) minus the left window size)
        kwic_inf_window_start = max(0, min(inf_ind, kwic_start) - left_window)
        # Sent clause end (len(clause) or (inf/kwic (either comes last) plus the right window size)
        kwic_inf_window_stop = min(len(clause), max(inf_ind + 1, kwic_stop) + right_window)

        clause_window = clause[kwic_inf_window_start:kwic_inf_window_stop]
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
    parser.add_argument('-l', '--left_window', type=partial(int_greater_or_equal_than, min_val=0), default=1,
                        metavar='LEFT_WINDOW')
    parser.add_argument('-r', '--right_window', type=partial(int_greater_or_equal_than, min_val=0), default=1,
                        metavar='RIGHT_WINDOW')
    parser.add_argument('-k', '--keep-duplicates', dest='keep_duplicates', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, left_window=args.left_window, right_window=args.right_window,
                                    keep_duplicates=args.keep_duplicates, filter_params=args.filter_params)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
