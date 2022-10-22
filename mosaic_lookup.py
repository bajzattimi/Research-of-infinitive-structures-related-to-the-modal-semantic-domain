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


def mosaic_to_tok(mosaic):
    ret = []
    for word in mosaic:
        if word.startswith('lemma:'):
            ret.append({'lemma': word[6:]})
        elif word.startswith('['):
            ret.append({'xpostag': word})
        else:
            ret.append({'form': word})
    return ret


def create_window(inp_fh, out_fh, mosaic):
    mosaic_toks = mosaic_to_tok(mosaic.split())
    mosaic_len = len(mosaic_toks)
    for comment_lines, sent in parse_emtsv_format(inp_fh):
        clause_len = len(next((line for line in comment_lines if line.startswith(' clause: ')))[9:].split())
        if clause_len != mosaic_len:  # TODO
            continue

        """
        for mosaic_word, word in zip(mosaic_toks, sent):
            if mosaic_word.items() > word.items():
                break
        else:
            print(' '.join(tok['form'] for tok in sent), file=out_fh)
        """
        sent[0]['form'] = sent[0]['form'].lower()  # Unify stentence start
        if all(mosaic_word.items() <= word.items() for mosaic_word, word in zip(mosaic_toks, sent)):
            print(' '.join(tok['form'] for tok in sent), file=out_fh)
            # print(' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in sent), file=out_fh)
# ####### BEGIN argparse helpers, needed to be moved into a common file ####### #


def existing_file_or_dir_path(string):
    if string != '-' and not Path(string).is_file() and not Path(string).is_dir():  # STDIN is denoted as - !
        raise ArgumentTypeError(f'{string} is not an existing file or directory!')
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
        out_fh = open(output_file, 'a', encoding='UTF-8')  # Append to a single file
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
    parser.add_argument('-o', '--output', dest='output_path', type=str,
                        help='Path to the output file containing the corpus sample', default='-')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
    parser.add_argument('-m', '--mosaic', type=str, metavar='MOSAIC NGRAM', required=True)

    args = parser.parse_args()

    return args


def gen_input_output_filename_pairs(input_path, output_path, other_opts):
    if output_path != '-':
        output_path = Path(output_path)
        if len(output_path.suffixes) == 0 or output_path.is_file():
            raise ValueError(f'Output must be a file with extension and must not exist ({output_path}) !')
    if Path(input_path).is_dir():
        for inp_fname_w_path in Path(input_path).glob('*.tsv'):
            yield inp_fname_w_path, output_path, *other_opts
    elif input_path == '-' or Path(input_path).is_file():
        yield input_path, output_path, *other_opts
    else:
        raise ValueError(f'Input and output must be both files (including STDIN/STDOUT) or directories'
                         f' ({(input_path, output_path)}) !')


def main():
    args = parse_args()
    if args.parallel > 1 and args.output_path != '-':
        raise ValueError(f'Output must be STDOUT if processing parallel ({args.output_path}) !')
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path, (args.mosaic,))

    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
