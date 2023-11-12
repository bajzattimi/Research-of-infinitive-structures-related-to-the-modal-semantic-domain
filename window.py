import sys
from copy import deepcopy
from itertools import chain
from functools import partial
from collections import Counter
from argparse import ArgumentTypeError

from mosaic_lib.ngram import  ngram
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.filter import parse_filter_params, filter_sentence
from mosaic_lib.argparse_helpers import base_argparser_factory, int_greater_or_equal_than_0
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


def get_int_value_for_fields_in_comment_lines(comment_lines, remaining_fields):
    fields = {}
    for comment_line in comment_lines:
        comment_line_splitted = comment_line.split(': ', maxsplit=1)
        key = comment_line_splitted[0].strip()
        if key in remaining_fields and len(comment_line_splitted) == 2:
            value = comment_line_splitted[1]
            try:
                value_int = int(value)
            except ValueError as e:
                e.message = f'Cannot convert value ({value}) to int in comment line ({comment_line})!'
                raise
            fields[key] = value_int
            remaining_fields.discard(key)

            if len(remaining_fields) == 0:
                break
    else:
        raise ValueError(f'Some required fields ({remaining_fields}) not found in comment lines ({comment_lines})!')

    return fields


def get_clauses(comment_lines, sent):
    fields = get_int_value_for_fields_in_comment_lines(comment_lines, {'left_length', 'kwic_length', 'right_length'})
    # Start with id 1
    kwic_left = max(1, fields['left_length'] + 1)
    if fields['right_length'] > 0:
        kwic_right = min(len(sent), fields['left_length'] + fields['kwic_length'] + 1)
    else:
        kwic_right = kwic_left + fields['kwic_length']
    puncts = [tokid_int for tokid_int, tok in enumerate(sent, start=1) if tok['xpostag'] == '[Punct]']
    # Sentence ending punct
    if len(puncts) == 0 or puncts[-1] != len(sent):
        puncts.append(len(sent) + 1)
    # "Sentence starting" punct
    puncts.insert(0, 0)

    # Determine the right clause from the sentence
    for punct_start, punct_end in ngram(puncts, 2):
        if punct_start < kwic_left < kwic_right <= punct_end:
            break
    else:
        raise ValueError(f'{kwic_left} and {kwic_right} does not appear in any range ({list(ngram(puncts, 2))})!')
    clause = sent[punct_start:punct_end - 1]

    return clause, kwic_left - punct_start - 1, kwic_right - punct_start - 1


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


def create_window(inp_fh, out_fh, left_window: int = 3, right_window: int = 3, keep_duplicate=False,
                  filter_params=((), (), None)):
    if left_window <= 0:
        raise ArgumentTypeError(f'{left_window} must be an integer greater than 0!')
    if right_window <= 0:
        raise ArgumentTypeError(f'{right_window} must be an integer greater than 0!')

    any_tok, cur_tok, substitute_tags = filter_params
    if substitute_tags is None:
        substitute_tags = {}
    c = Counter()
    all_elem = 0
    uniq_clauses = set()

    inf_too_far_num = 0
    wo_inf_num = 0
    deleted_per_rule_num = 0
    duplicate_num = 0

    n = 0
    header = next(inp_fh)
    enum_fields_fun = partial(enum_fields_for_tok, fields=header.rstrip().split('\t'))
    print(header, end='', file=out_fh)
    for n, (comment_lines, sent_orig) in enumerate(parse_emtsv_format(chain([header], inp_fh)), start=1):
        sent = [{'form': tok['form'], 'lemma': tok['lemma'],
                 'xpostag': substitute_tags.get(tok['xpostag'], tok['xpostag'])}
                for tok in sent_orig]

        clause, kwic_start, kwic_stop = get_clauses(comment_lines, sent)
        inf_in_clause, inf_in_window, inf_ind = check_clause(clause, kwic_start, kwic_stop)

        if not inf_in_window and inf_in_clause:
            print("WARNING: INF IS TO FAR FROM THE FINITE VERB:",
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause), file=sys.stderr)
            inf_too_far_num += 1
            continue
        elif not inf_in_clause:
            print("WARNING: FILTERING CLAUSES WITHOUT INF:",
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause), file=sys.stderr)
            wo_inf_num += 1
            continue

        # Sent clause start or (inf/kwic (either comes first) minus the left window size)
        kwic_inf_window_start = max(0, min(inf_ind, kwic_start) - left_window)
        # Sent clause end (len(clause) or (inf/kwic (either comes last) plus the right window size)
        kwic_inf_window_stop = min(len(clause), max(inf_ind + 1, kwic_stop) + right_window)

        clause_window = clause[kwic_inf_window_start:kwic_inf_window_stop]
        clause_window[0]['form'] = clause_window[0]['form'].lower()  # Unify stentence start
        clause_str = ' '.join(tok['form'] for tok in clause_window)
        """
        # Debug
        if kwic_inf_window_stop - kwic_inf_window_start > 5:
            print(kwic_inf_window_stop - kwic_inf_window_start,
                  ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause_window))
        """
        clause_window_orig = deepcopy(clause_window)
        delete_ex = filter_sentence(clause_window, any_tok, cur_tok, clause_str)
        if delete_ex:
            deleted_per_rule_num += 1
            continue

        # Print
        if not keep_duplicate and clause_str not in uniq_clauses:
            uniq_clauses.add(clause_str)
            for comment_line in comment_lines:
                print('#', comment_line, file=out_fh)
            print('#  clause:', clause_str, file=out_fh)
            print('#  clause_SPL:', ' '.join('#'.join(enum_fields_fun(tok)) for tok in clause_window), file=out_fh)
            for tok in clause_window_orig:
                print(*enum_fields_fun(tok, prefix_lemma=False), sep='\t', file=out_fh)
            print(file=out_fh)
        else:
            print('INFO:', 'DUPLICATE CLAUSE', clause_str, file=sys.stderr)
            duplicate_num += 1
        c[len(clause_window)] += 1
        all_elem += 1

    print('', *range(2, 10), sep='\t', file=sys.stderr)
    print(inp_fh.name, end='\t', file=sys.stderr)
    for i in range(2, 10):
        print(f'{(c[i]/all_elem)*100}%', end='\t', file=sys.stderr)
    print(file=sys.stderr)
    for name, sent_num in (('inf too far', inf_too_far_num), ('without inf',wo_inf_num),
                           ('deleted by rule', deleted_per_rule_num), ('duplicate clauses', duplicate_num),
                           ('remaining', all_elem-duplicate_num)):
        print('REPORT:', name, sent_num, 'sents', f'{(sent_num/n)*100}%', file=sys.stderr)
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-l', '--left_window', type=int_greater_or_equal_than_0, default=1, metavar='LEFT_WINDOW')
    parser.add_argument('-r', '--right_window', type=int_greater_or_equal_than_0, default=1, metavar='RIGHT_WINDOW')
    parser.add_argument('-k', '--keep-duplicate', dest='keep_duplicate', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, left_window=args.left_window, right_window=args.right_window,
                                    keep_duplicate=args.keep_duplicate, filter_params=args.filter_params)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
