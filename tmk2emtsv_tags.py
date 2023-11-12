import sys
from os import cpu_count
from pathlib import Path
from multiprocessing import Pool
from itertools import chain
from re import compile as re_compile
from argparse import ArgumentParser, ArgumentTypeError

from yamale import make_schema, make_data, validate, YamaleError


def parse_emtsv_format(input_iterator, keep_fields=None):
    """
    Parse the emtsv raw format into a Python sturcture
     (iterator, sentences as lists, tokens as dicts, keys field names, values the token's properties)
    :param input_iterator: str iterator on lines of emtsv raw data
    :param keep_fields: list or set of field names to keep or None to keep all fields
    :return: iterator: sentences as lists, tokens as dicts, keys field names, values the token's properties
    """
    header = next(input_iterator, '')
    header_splitted = [col for col in header.rstrip('\n').split('\t') if len(col) > 0]
    # Check duplicate or empty fields in header!
    if header.count('\t') + 1 != len(set(header_splitted)):
        raise ValueError(f'Input header is not valid ({header_splitted}) !')

    header_filtered, len_header_filtered = header_splitted, len(header_splitted)
    if isinstance(keep_fields, list):  # Argparse returns list which must be cast to set
        keep_fields = set(keep_fields)
    if isinstance(keep_fields, set):
        header_filtered = []
        for col in header_splitted:
            if col in keep_fields:
                header_filtered.append(col)  # Fields to keep are denoted with their name
            else:
                header_filtered.append(None)  # Fields to omit are denoted with None

    comment, sent = [], []
    for i, line in enumerate(input_iterator, start=2):  # Header is already processed, the loop starts from the 2nd line
        line = line.rstrip('\n')
        if len(line) == 0:  # State 1: empty line (after sentences)
            yield comment, sent  # Yield the collected sentence and start a new empty one
            comment, sent = [], []
        elif line.startswith('# '):  # State 2: Comment, metadata
            comment.append(line[2:])  # Strip '# ' prefix and add the comments line by line withot further processing
        else:  # State 3: A line containing a token
            line_splitted = line.split('\t')  # Split to columns
            # Filter out columns not in keep_fields therefore denoted by None in header_filtered

            # zip(*_,strict=True) is available to raise ValueError in Python >=3.10
            if len_header_filtered != len(line_splitted):
                ValueError(f'For line {i} fields length ({len(line_splitted)}) does not match'
                           f' the length of the header ({len(header_splitted)}: {(header_splitted, line_splitted)} !',)

            # The others are put into a token dictionary with their field name as key
            token = {k: v for k, v in zip(header_filtered, line_splitted) if k is not None}
            sent.append(token)

    if len(comment) > 0 or len(sent) > 0:  # Yield all remaining tokens or metadata lines
        yield comment, sent


def format_emtsv_lines(it):
    """
    Format the input iterator of Python sturctured emtsv output into emtsv formatted lines
    :param it: The input iterator of Python sturctured emtsv output
    :return: Generator of emtsv formatted lines
    """
    tab = '\t'  # Store tab
    first_comment, first_sent = next(it)  # Can not be empty! All checks are performed in parse_emtsv_format()
    yield f'{tab.join(first_sent[0].keys())}\n'  # Header (in insertion order!)
    for comment, sent in chain([(first_comment, first_sent)], it):  # Push back first sentence into the iterator
        for comment_line in comment:
            yield f'#  {comment_line}\n'  # Write comment and add '# ' to the begining
        for token in sent:
            yield f'{tab.join(token.values())}\n'  # Write token (in insertion order!)
        yield '\n'  # Write empty line after sentences


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


def cond_fun(not_value, regex, tok_field_val):
    # not_value XOR regex.search(tok[field_name])
    return (not_value and not regex.search(tok_field_val)) or (not not_value and regex.search(tok_field_val))


def filter_sentence(sent, any_tok, cur_tok, clause_str):
    delete_ex = False
    for tok in sent:
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


def filter_data(emtsv_sent_it, filter_params=((), (), None)):

    any_tok, cur_tok, substitute_tags = filter_params
    if substitute_tags is None:
        substitute_tags = {}

    deleted_per_rule_num = 0

    for n, (comment_lines, sent_orig) in enumerate(emtsv_sent_it, start=1):
        sent = []
        for tok in sent_orig:
            tok['xpostag'] = substitute_tags[tok['ORIGPOS']]
            sent.append(tok)
        clause_str = ' '.join(tok['form'] for tok in sent)
        delete_ex = filter_sentence(sent, any_tok, cur_tok, clause_str)
        if delete_ex:
            deleted_per_rule_num += 1
            continue

        yield comment_lines, sent


def process_input_to_output(input_fh, output_fh, *other_args):
    """
    Process a file handle into another file handle or to a python structured form as a geneator on sentences.
     Use binary files to avoid the encoding-decoidng overhead (applies only if no field filtering i.e. keep_fields=None)
    :param input_fh: An already opened file handle (for reading)
    :param output_fh: An already opened file handle (for writing)
    :param other_args: Arguments to be passed to filter_data() function, details in the function
    :return: The stentence generator where every token is a dict in a list (=sentence) for all sentences OR
             Noting. Writes output to output_fh
    """
    orig_sent_it = parse_emtsv_format(input_fh)  # Format lines to sents
    converted_sent_it = filter_data(orig_sent_it, *other_args)  # Convert POS tags
    converted_lines_it = format_emtsv_lines(converted_sent_it)  # Format sent to lines

    output_fh.writelines(converted_lines_it)  # It actually writes an iterable only (not adding newlines)


def process_one_file(input_file, output_file, *other_args):
    """
    Process a file into another file. Use binary files to avoid the encoding-decoidng overhead
    :param input_file: - for STDIN, filename or already opened file handle (for reading)
    :param output_file: - for STDOUT, filename or already opened file handle (for writing)
    :param other_args: Arguments to be passed to process_input_to_output() function, details in the function
    :return: Noting. Everything is written to output_file on success else exceptions are raised
    """
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
    elif isinstance(input_file, (str, Path)):
        out_fh = open(output_file, 'w', encoding='UTF-8')
        close_out_fh = True
    elif hasattr(input_file, 'writelines'):
        out_fh = output_file
    else:
        raise ValueError('Only STDOUT, filename or file-like object is allowed as output !')

    process_input_to_output(inp_fh, out_fh, *other_args)

    # Without with statement we need to close opened files manually!
    if close_inp_fh:
        inp_fh.close()

    if close_out_fh:
        out_fh.close()


# ####### BEGIN argparse helpers, needed to be moved into a common file ####### #

def existing_file(string):
    if not Path(string).is_file():
        raise ArgumentTypeError(f'{string} is not an existing file!')
    return string

def existing_file_or_dir_path(string):
    if string != '-' and not Path(string).is_file() and not Path(string).is_dir():  # STDIN is denoted as - !
        raise ArgumentTypeError(f'{string} is not an existing file or directory!')
    return string


def new_file_or_dir_path(string):
    name = Path(string)
    if string != '-':
        if len(name.suffixes) == 0:  # Directory as has no suffixes else a File as it has suffixes
            name.mkdir(parents=True, exist_ok=True)
            if next(name.iterdir(), None) is not None:
                raise ArgumentTypeError(f'{string} is not an empty directory!')
    return string


def int_greater_than_1(string):
    try:
        val = int(string)
    except ValueError:
        val = -1  # Intentional bad value if value can not be converted to int()

    if val <= 1:
        raise ArgumentTypeError(f'{string} is not an int > 1!')

    return val


# ####### END argparse helpers, needed to be moved into a common file ####### #

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_path', type=existing_file_or_dir_path,
                        help='Path to the input file or directory containing the corpus sample', default='-')
    parser.add_argument('-o', '--output', dest='output_path', type=new_file_or_dir_path,
                        help='Path to the output file or directory containing the corpus sample', default='-')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
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
    args = parse_args()  # Input dir and output dir sanitized
    # Extra params to pass, currently one
    extra_params_tuple = (args.filter_params,)
    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path, extra_params_tuple)
    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
