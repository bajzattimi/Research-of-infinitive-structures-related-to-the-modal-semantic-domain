import sys
from pathlib import Path
from itertools import tee, islice
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser, ArgumentTypeError

from emtsv2 import parse_emtsv_format


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


def get_sent_parts(comment_lines, sent):
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

    # Determine sentence part
    for punct_start, punct_end in ngram(puncts, 2):
        if punct_start < kwic_left < kwic_right <= punct_end:
            break
    else:
        raise ValueError(f'{kwic_left} and {kwic_right} does not appear in any range ({list(ngram(puncts, 2))})!')
    part = sent[punct_start:punct_end - 1]

    return part, kwic_left - punct_start - 1, kwic_right - punct_start - 1


def create_window(inp_fh, out_fh, left_window: int = 3, right_window: int = 3):
    if left_window <= 0:
        raise ArgumentTypeError(f'{left_window} must be an integer greater than 0!')
    if right_window <= 0:
        raise ArgumentTypeError(f'{right_window} must be an integer greater than 0!')

    uniq_parts = set()
    filtered_sents_num = 0
    duplicate_num = 0
    n = 0
    for n, (comment_lines, sent) in enumerate(parse_emtsv_format(inp_fh), start=1):
        part, kwic_start, kwic_stop = get_sent_parts(comment_lines, sent)
        inf_loc_min = max(0, kwic_start - 2)
        inf_loc_max = min(len(part), kwic_stop + 2)
        # Sanity check: Has the  sent part or the window INF
        inf_in_part = any(tok['xpostag'].startswith('[/V]') and tok['xpostag'].endswith('[Inf]')
                          for tok in part)
        inf_ind = -1
        for inf_ind, tok in enumerate(part[inf_loc_min:inf_loc_max], start=inf_loc_min):
            if tok['xpostag'].startswith('[/V]') and tok['xpostag'].endswith('[Inf]'):
                inf_in_window = True
                break
        else:
            inf_in_window = False

        if not inf_in_window and inf_in_part:
            print("WARNING: INF IS TO FAR FROM THE FINITE VERB:",
                  ' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in part), file=sys.stderr)
            filtered_sents_num += 1
            continue
        elif not inf_in_part:
            print("WARNING: FILTERING SENT PARTS WITHOUT INF:",
                  ' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in part), file=sys.stderr)
            filtered_sents_num += 1
            continue

        # Sent part start or (inf/kwic (either comes first) minus the left window size)
        kwic_inf_window_start = max(0, min(inf_ind, kwic_start) - left_window)
        # Sent part end (len(part) or (inf/kwic (either comes last) plus the right window size)
        kwic_inf_window_stop = min(len(part), max(inf_ind + 1, kwic_stop) + right_window)

        part_window = part[kwic_inf_window_start:kwic_inf_window_stop]
        part_str = ' '.join(tok['form'] for tok in part_window)
        """
        # Debug
        if kwic_inf_window_stop - kwic_inf_window_start > 5:
            print(kwic_inf_window_stop - kwic_inf_window_start,
                  ' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in part_window))
        """
        # Print
        if part_str not in uniq_parts:
            uniq_parts.add(part_str)
            for comment_line in comment_lines:
                print('#', comment_line, file=out_fh)
            print('#  part:', part_str, file=out_fh)
            print('#  part_SPL:',
                  ' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in part_window), file=out_fh)
            for tok in part_window:
                print(tok['form'], tok['lemma'], tok['xpostag'], sep='\t', file=out_fh)
            print()
        else:
            print('INFO:', 'DUPLICATE SENT PART', part_str, file=sys.stderr)
            duplicate_num += 1

    print('filtered', filtered_sents_num, 'sents', (filtered_sents_num/n)*100, '%', file=sys.stderr)
    print('filtered', duplicate_num, 'duplicate parts', (duplicate_num/n)*100, '%', file=sys.stderr)
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
