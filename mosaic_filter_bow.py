import sys
import gzip
from pathlib import Path
from collections import defaultdict, deque, Counter
from itertools import tee, islice, groupby
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser, ArgumentTypeError

from emtsv2 import parse_emtsv_format


def ngram(it, n):
    return zip(*(islice(it, i, None) for i, it in enumerate(tee(it, n))))


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


def mosaic_to_bow(mosaic_fh, threshold):
    mosaic_to_score = {}
    mosaic_bow_to_freq = Counter()
    for curr_mosaic in mosaic_fh:
        # Strip freq from the line with leading spaces
        mos_group_freq_ind = next(n for n, char_bigram in enumerate(ngram(curr_mosaic, 2), start=2)
                                  if char_bigram[0].isnumeric() and char_bigram[1] == ' ')
        mos_group_freq = int(curr_mosaic[:mos_group_freq_ind])
        curr_mosaic = tuple(curr_mosaic.strip().split()[1:])
        mosaic_toks, score = mosaic_to_tok(curr_mosaic)

        # Add every (field, value) pair for every token to the counter
        mosaic_tok_counter = Counter()
        for tok in mosaic_toks:
            mosaic_tok_counter.update(tok.items())
        # Sum freqs of same BOW mosaic n-grams
        mosaic_bow_tuple = tuple(sorted(mosaic_tok_counter.items(), key=lambda x: (-x[1], x[0])))
        mosaic_bow_to_freq[mosaic_bow_tuple] += mos_group_freq
        # (((field_name, value), freq),...): moz_freq
        mosaic_to_score[mosaic_bow_tuple] = score  # The score is the same as without BOW-ing

    # mosaic_bow_to_freq_filtered = [(mos, freq) for mos, freq in mosaic_bow_to_freq.items() if freq >= threshold]
    # mosaic_bow_to_freq_filtered.sort(key=lambda x: (-x[1], x[0]))
    mosaic_bow_to_freq_filtered = sorted(mosaic_bow_to_freq, key=lambda x: (-x[1], x[0]))

    return mosaic_to_score, mosaic_bow_to_freq_filtered


def mosaic_bow_tuple_to_printable(curr_mosaic):
    curr_mosaic_bow_printable = []
    for (mos_field, mos_val), mos_tok_field_value_count in curr_mosaic:
        if mos_field == 'lemma':  # # Normal fields(form, xpostag) are left alone, lemma field gets lemma: prefix!
            mos_val = f'lemma:{mos_val}'
        freq_printable = ''
        if mos_tok_field_value_count > 1:
            freq_printable = ' ({mos_tok_field_value_count})'
        curr_mosaic_bow_printable.append(f'{mos_val}{freq_printable}')
    return tuple(curr_mosaic_bow_printable)


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
        # Add every (field, value) pair for every token to the counter
        sent_tok_field_val_counter = Counter()
        for tok in sent:
            sent_tok_field_val_counter.update(tok.items())
        example_clauses_with_matching_length.append((comment_lines,
                                                     tuple((tok['form'], tok['lemma'], tok['xpostag']) for tok in sent),
                                                     sent_tok_field_val_counter))

    mosaics_by_freq = deque()
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        # 3. Group by freq and score group elements
        mosaic_to_score, mosaic_bow_to_freq_sorted = mosaic_to_bow(mosaic_fh, threshold)
        # We do not utilise the increased frequency beyond ordering after the mozaic->BOW conversion,
        # as the no. of matching examples will be used as the final decision
        for _, group_it in groupby(mosaic_bow_to_freq_sorted, key=lambda x: x[1]):
            mosaic_to_examples = defaultdict(set)
            for curr_mosaic in group_it:
                curr_mosaic = curr_mosaic[0]  # Strip freq!
                curr_mosaic_bow_printable = mosaic_bow_tuple_to_printable(curr_mosaic)
                # 4. For the matching clauses store the example clause
                for _, example_clause, sent_tok_field_val_counter in example_clauses_with_matching_length:
                    # The sent (which has equal length as the mosaic n-gram) should have at least
                    #  the number of masaic elems as in the mosaic n-gram e.g. simple bag of words with counts
                    #  WARNING: We can count a tok in the sent twice because the different abstractions (should be rare)
                    #   Handling this would lead to an NP-time contraint satisfaction task :(
                    if all(mosaic_tok_field_value_count <= sent_tok_field_val_counter[mosaic_tok_field_value]
                           for mosaic_tok_field_value, mosaic_tok_field_value_count in curr_mosaic):
                        # We do not interpet the mosaic's value from here on!
                        mosaic_to_examples[(curr_mosaic_bow_printable,
                                            mosaic_to_score[curr_mosaic])].add(example_clause)
            # 5. Group by example sets
            examples_to_mosaic = defaultdict(set)
            for mosaic_ngram_and_score, example_set in mosaic_to_examples.items():
                examples_to_mosaic[frozenset(example_set)].add(mosaic_ngram_and_score)
            # 6. Get max score per example set and print mosaics with that score
            #    For BOW the number of matched examples means the new frequency, not the added freq of the n-grams
            for ex_set, mosaic_set in sorted(examples_to_mosaic.items(), key=lambda x: (-len(x[1]), x[0])):
                if len(ex_set) < threshold:
                    break  # After this element, only smaller groups will come which should be filtered
                max_score = max(mos_score for _, mos_score in mosaic_set)
                for mos, mos_score in sorted(mosaic_set, key=lambda x: (-x[1], x[0])):
                    if mos_score == max_score:
                        mosaics_by_freq.append((len(ex_set), mos, ex_set))
                    else:
                        break  # Sorted by max score -> Reaching the first non-max scrore means no more max score
    # 7. Create 2-level nested groups if the matching examples are subset of each other for the two mosaic
    while len(mosaics_by_freq) > 0:
        mos_group_freq, mos, ex_set = mosaics_by_freq.popleft()
        print(mos_group_freq, *mos, file=out_fh)
        mosaics_by_freq_new = deque()
        while len(mosaics_by_freq) > 0:
            mos_group_freq_str2, mos2, ex_set2 = mosaics_by_freq.popleft()
            if ex_set > ex_set2:
                print('\t', mos_group_freq_str2, ' ', ' '.join(mos2), sep='', file=out_fh)
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
