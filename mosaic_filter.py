import sys
import gzip
from pathlib import Path
from collections import defaultdict, deque
from itertools import tee, islice, groupby
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
    score = 0
    for word in mosaic:
        if word.startswith('lemma:'):
            ret.append({'lemma': word[6:]})
            score += 2
        elif word.startswith('['):
            ret.append({'xpostag': word})
            score += 1
        else:
            ret.append({'form': word})
            score += 4
    return ret, score


def determine_mosaic_length(mosaic):
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        first_line = next(mosaic_fh, None)
        if first_line is None:
            return -1
        first_line = first_line.strip().split()

    return len(first_line) - 1  # Remove count!


def create_window(inp_fh, out_fh, mosaic, threshold):
    # 1. Determine the lehgth of all mosaic from the first one
    mosaic_len = determine_mosaic_length(mosaic)
    if mosaic_len == -1:  # Empty file
        return
    # 2. Cache all examples with matching length
    example_clauses_with_matching_length = []
    for comment_lines, sent in parse_emtsv_format(inp_fh):
        clause_len = len(next((line for line in comment_lines if line.startswith(' clause: ')))[9:].split())
        if clause_len != mosaic_len:
            continue
        sent[0]['form'] = sent[0]['form'].lower()  # Unify stentence start
        example_clauses_with_matching_length.append((comment_lines, sent))

    mosaics_by_freq = deque()
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        # 3. Group by freq and score group elements
        for key, group_it in groupby(mosaic_fh, key=lambda x: x.strip().split()[0]):
            if int(key) < threshold:
                break
            mosaic_group = {}
            mosaic_to_examples = defaultdict(set)
            mos_group_freq_str = ''
            for curr_mosaic in group_it:
                # Strip freq from the line with leading spaces
                mos_group_freq_ind = next(n for n, char_bigram in enumerate(ngram(curr_mosaic, 2), start=2)
                                          if char_bigram[0].isnumeric() and char_bigram[1] == ' ')
                mos_group_freq_str = curr_mosaic[:mos_group_freq_ind]
                curr_mosaic = tuple(curr_mosaic.strip().split()[1:])
                mosaic_toks, score = mosaic_to_tok(curr_mosaic)
                mosaic_group[curr_mosaic] = score
                # 4. For the matching clauses store the example clause
                for comment_lines, sent in example_clauses_with_matching_length:
                    if all(mosaic_word.items() <= word.items() for mosaic_word, word in zip(mosaic_toks, sent)):
                        example_clause = tuple((tok['form'], tok['lemma'], tok['xpostag'])for tok in sent)
                        mosaic_to_examples[curr_mosaic].add(example_clause)
            # 5. Group by example sets
            examples_to_mosaic = defaultdict(set)
            for mosaic_ngram, example_set in mosaic_to_examples.items():
                examples_to_mosaic[frozenset(example_set)].add((mosaic_ngram, mosaic_group[mosaic_ngram]))
            # 6. Get max score per example set and print mosaics with that score
            for ex_set, mosaic_set in examples_to_mosaic.items():
                max_score = max(mos_score for _, mos_score in mosaic_set)
                for mos, mos_score in sorted(mosaic_set, key=lambda x: (-x[1], x[0])):
                    if mos_score == max_score:
                        mosaics_by_freq.append((mos_group_freq_str, mos, ex_set))
                    else:
                        break  # Sorted by max score -> Reaching the first non-max scrore means no more max score
    # 7. Create 2-level nested groups if the matching examples are subset of each other for the two mosaic
    while len(mosaics_by_freq) > 0:
        mos_group_freq_str, mos, ex_set = mosaics_by_freq.popleft()
        print(mos_group_freq_str, ' '.join(mos), sep='', file=out_fh)
        mosaics_by_freq_new = deque()
        while len(mosaics_by_freq) > 0:
            mos_group_freq_str2, mos2, ex_set2 = mosaics_by_freq.popleft()
            if ex_set > ex_set2:
                print('\t', mos_group_freq_str2, ' '.join(mos2), sep='', file=out_fh)
            else:
                mosaics_by_freq_new.append((mos_group_freq_str2, mos2, ex_set2))
        mosaics_by_freq = mosaics_by_freq_new  # Update with shortened list
# ####### BEGIN argparse helpers, needed to be moved into a common file ####### #


def existing_file(string):
    if not Path(string).is_file():
        raise ArgumentTypeError(f'{string} is not an existing file!')
    return string


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
    parser.add_argument('-m', '--mosaic', type=existing_file, metavar='MOSAIC NGRAM FILE', required=True)
    parser.add_argument('-f', '--min-freq', dest='min_freq', type=int, default=1,  metavar='MOSAIC NGRAM FILE')

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
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path,
                                                           (args.mosaic, args.min_freq))

    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
