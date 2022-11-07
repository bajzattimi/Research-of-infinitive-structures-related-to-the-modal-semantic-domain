import sys
from pathlib import Path
from copy import deepcopy
from functools import partial
from collections import Counter
from re import compile as re_compile
from itertools import tee, islice, chain
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser, ArgumentTypeError

from yamale import make_schema, make_data, validate, YamaleError

from emtsv2 import parse_emtsv_format


def load_and_validate(schema_fname, inp_data, strict=True):
    with open(schema_fname, encoding='UTF-8') as fh:
        schemafile_content = fh.read()
    config_schema = make_schema(content=schemafile_content)

    if isinstance(inp_data, (str, Path)):
        with open(inp_data, encoding='UTF-8') as fh:
            inp_data_str = fh.read()
    else:
        inp_data_str = inp_data.read()
    data = make_data(content=inp_data_str)

    try:
        validate(config_schema, data, strict)
    except YamaleError as e:
        for result in e.results:
            print('Error validating data {0} with {1}:'.format(result.data, result.schema), file=sys.stderr)
            for error in result.errors:
                print('', error, sep='\t', file=sys.stderr)
        exit(1)
    return data[0][0]


def cond_fun(not_value, regex, tok_field_val):
    # not_value XOR regex.search(tok[field_name])
    return (not_value and not regex.search(tok_field_val)) or (not not_value and regex.search(tok_field_val))


def filter_sentence(clause_window, any_tok, cur_tok, clause_str):
    delete_ex = False
    for tok in clause_window:
        for name, not_value, regex, to_delete, field_name in any_tok:
            curr_tok_field = tok.get(field_name)
            if curr_tok_field is not None and cond_fun(not_value, regex, curr_tok_field):
                if 'example' in to_delete:
                    print('INFO:', f'FILTERED SENT ({name})', clause_str, file=sys.stderr)
                    delete_ex = True
                    break
        else:  # Continue if the inner loop wasn't broken
            # Source: https://stackoverflow.com/questions/189645/how-can-i-break-out-of-multiple-loops/189685#189685
            for name, not_value, regex, to_delete, field_name in cur_tok:  # Delete matching fields for current token
                curr_tok_field = tok.get(field_name)
                if curr_tok_field is not None and cond_fun(not_value, regex, curr_tok_field):
                    for field in to_delete:
                        tok.pop(field, None)
            if len(tok) == 0:
                print('ERROR: NO FIELD LEFT FOR TOKEN!')
                exit(1)
            continue
        break  # Inner loop was broken, break the outer
    return delete_ex


def parse_filter_params(inp_data):
    config = load_and_validate(Path(__file__).parent / 'filter_params_schema.yaml', inp_data)
    any_tok = []
    cur_tok = []
    for config_elem in config[0]['delete']:
        name = config_elem['name']
        value = re_compile(config_elem['value'])
        if config_elem['cond'] == 'any_tok':
            any_tok.append((name, config_elem['not'], value, config_elem['to_delete'], config_elem['field_name']))
        else:
            cur_tok.append((name, config_elem['not'], value, config_elem['to_delete'], config_elem['field_name']))

    subs_dict = config[1]['substitute']
    return any_tok, cur_tok, subs_dict


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


def ngram(it, n):
    return zip(*(islice(it, i, None) for i, it in enumerate(tee(it, n))))


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
# ####### BEGIN argparse helpers, needed to be moved into a common file ####### #


def existing_file_or_dir_path(string):
    if string != '-' and not Path(string).is_file() and not Path(string).is_dir():  # STDIN is denoted as - !
        raise ArgumentTypeError(f'{string} is not an existing file or directory!')
    return string


def new_file_or_dir_path(string):
    name = Path(string)
    if string != '-':
        if len(name.suffixes) == 0:
            name.mkdir(parents=True, exist_ok=True)
            if next(name.iterdir(), None) is not None:
                raise ArgumentTypeError(f'{string} is not an empty directory!')
    return string


def process_one_file(input_file, output_file, *other_args):
    close_inp_fh, close_out_fh = False, False
    if input_file == '-':
        inp_fh = sys.stdin
    elif isinstance(input_file, (str, Path)):
        inp_fh = open(input_file, encoding='UTF-8')
        close_inp_fh = True
    elif hasattr(input_file, 'read'):
        inp_fh = input_file
    else:
        raise ValueError('Only STDIN, filename or file-like object is allowed as input !')

    if output_file == '-':
        out_fh = sys.stdout
    elif isinstance(output_file, (str, Path)):
        out_fh = open(output_file, 'w', encoding='UTF-8')
        close_out_fh = True
    elif hasattr(output_file, 'writelines'):
        out_fh = output_file
    else:
        raise ValueError('Only STDOUT, filename or file-like object is allowed as output !')

    create_window(inp_fh, out_fh, *other_args)

    # Without with statement we need to close opened files manually!
    if close_inp_fh:
        inp_fh.close()

    if close_out_fh:
        out_fh.close()


def int_greater_or_equal_than_0(string):
    try:
        val = int(string)
    except ValueError:
        val = -1  # Intentional bad value if value can not be converted to int()

    if val < 0:
        raise ArgumentTypeError(f'{string} is not an int >= 0!')

    return val


def int_greater_than_1(string):
    try:
        val = int(string)
    except ValueError:
        val = -1  # Intentional bad value if value can not be converted to int()

    if val <= 1:
        raise ArgumentTypeError(f'{string} is not an int > 1!')

    return val


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_path', type=existing_file_or_dir_path,
                        help='Path to the input file or directory containing the corpus sample', default='-')
    parser.add_argument('-o', '--output', dest='output_path', type=new_file_or_dir_path,
                        help='Path to the output file or directory containing the corpus sample', default='-')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
    parser.add_argument('-l', '--left_window', type=int_greater_or_equal_than_0, default=1, metavar='LEFT_WINDOW')
    parser.add_argument('-r', '--right_window', type=int_greater_or_equal_than_0, default=1, metavar='RIGHT_WINDOW')
    parser.add_argument('-k', '--keep-duplicate', dest='keep_duplicate', action='store_true',
                        help='Keep duplicate clauses', default=False, required=False)
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)

    args = parser.parse_args()

    return args


def gen_input_output_filename_pairs(input_path, output_path, other_opts):
    if Path(input_path).is_dir() and Path(output_path).is_dir():
        for inp_fname_w_path in Path(input_path).glob('*.tsv'):
            yield inp_fname_w_path, Path(output_path) / f'{inp_fname_w_path.stem}.tsv', *other_opts
    elif ((input_path == '-' or Path(input_path).is_file()) and
          ((output_path == '-') or not Path(output_path).is_dir())):
        yield input_path, output_path, *other_opts
    else:
        raise ValueError(f'Input and output must be both files (including STDIN/STDOUT) or directories'
                         f' ({(input_path, output_path)}) !')


def main():
    args = parse_args()
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path,
                                                           (args.left_window, args.right_window, args.keep_duplicate,
                                                            args.filter_params))

    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
