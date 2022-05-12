import re
import sys
from pathlib import Path
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser, ArgumentTypeError
from collections import Counter


from emtsv2 import parse_emtsv_format


def get_int_value_for_fields_in_comment_lines(comment_lines, remaining_fields):
    fields = {}
    for comment_line in comment_lines:
        comment_line_splitted = comment_line.split(': ', maxsplit=1)
        key = comment_line_splitted[0]
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


def get_int_value_for_tok_field(tok, field_name):
    value = tok.get(field_name)
    if value is None:
        raise ValueError(f'Field ({field_name}) not in the available fields for token ({tok})!')
    try:
        value_int = int(value)
    except ValueError as e:
        e.message = f'Cannot convert value ({value}) to int in field ({field_name} for token ({tok})!'
        raise
    return value_int


def get_sent_parts(comment_lines, sent, left_window, right_window):
    fields = get_int_value_for_fields_in_comment_lines(comment_lines, {'left_length', 'kwic_length', 'right_length'})
    kwic_left = max(1, fields['left_length'] - left_window)
    kwic_right = min(len(sent), fields['left_length'] + fields['kwic_length'] + right_window)

    kwic_range = range(kwic_left, kwic_right)
    ranges = {range(1, kwic_left): 'left', kwic_range: 'kwic', range(kwic_right, len(sent)+1): 'right'}
    parts = {'left': [], 'kwic': [], 'right': [], 'left_new': [], 'kwic_new': [], 'right_new': []}

    for tok in sent:
        tokid_int = get_int_value_for_tok_field(tok, 'id')
        head_int = get_int_value_for_tok_field(tok, 'head')
        for sent_range, part in ranges.items():
            if tokid_int in sent_range:
                if head_int in kwic_range:
                    parts['kwic_new'].append(tok)
                else:
                    parts[f'{part}_new'].append(tok)
                parts[part].append(tok)
                break
        else:
            raise ValueError(f'{tok} does not appear in any range ({ranges})!')

    return parts

"""
for comment_lines, sent in parse_emtsv_format(inp_fh): # for akt_mondat in mondatok:
    for tok in sent:  # for tok in mondat:
      pass # kapcsolat(..., tok)
"""


def create_window(inp_fh, out_fh, left_window: int = 3, right_window: int = 3):
    if left_window <= 0:
        raise ArgumentTypeError(f'{left_window} must be an integer greater than 0!')
    if right_window <= 0:
        raise ArgumentTypeError(f'{right_window} must be an integer greater than 0!')

    sent_sum = 0
    for comment_lines, sent in parse_emtsv_format(inp_fh):
        c = Counter()
        ige = False
        for tok in sent:
            c[tok['xpostag']] += 1
            m = re.match(r'\[/V\]\[((_Mod/V|_Caus/V)\]\[)?(Prs|Pst|Cond|Sbjv)\.(N?Def\.[1-3](Sg|Pl)|1Sg›2)\]',
                         tok['xpostag'])
            if m and tok['lemma'] == 'gyűlöl':
                ige = True
        if '[/V][Inf]' in c and ige:
            pass   # EZEK A MONDATOK JÓK!
        else:
            print('REQUIRED WORDS NOTFOUND:', comment_lines[4])  # EZEK HIBÁK CSAK KIÍRJUK ŐKET TÁJÉKOZTATÁS JELLEGGEL!
            sent_sum += 1

        """
        # TODO Design output format
        sent_parts = get_sent_parts(comment_lines, sent, left_window, right_window)
        window = sent_parts['kwic']
        forms = []
        for tok in window:
            if tok['xpostag'] != '[/V][Inf]':
                forms.append(tok['lemma'])
            else:
                forms.append(tok['xpostag'])

        """
        """
        forms = []
        for tok in window:
            if tok['xpostag'] != '[/V][Inf]':
                forms.append(tok['lemma'])
            else:
                forms.append(tok['xpostag'])
        
        forms = [tok['form'] for tok in window]
        """
        # print(*forms, file=out_fh)

        """
        print('Original sent:', ' '.join(tok['form'] for tok in sent), file=out_fh)
        sent_parts = get_sent_parts(comment_lines, sent, left_window, right_window)
        for kwic_type in ('kwic', 'kwic_new'):
            window = sent_parts[kwic_type]
            forms = [tok['form'] for tok in window]
            print(f'\t{kwic_type}:', *forms, file=out_fh)
        """

    print(sent_sum)
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


def process_one_file(input_file, output_file, left_window, right_window):
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

    create_window(inp_fh, out_fh, left_window, right_window)

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
                                                           (args.left_window, args.right_window))

    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
