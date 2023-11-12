import gzip
from itertools import groupby
from functools import partial
from argparse import ArgumentTypeError
from collections import defaultdict, deque

from mosaic_lib.ngram import ngram
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import base_argparser_factory, existing_file
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


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
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-m', '--mosaic', type=existing_file, metavar='MOSAIC NGRAM FILE', required=True)
    parser.add_argument('-f', '--min-freq', dest='min_freq', type=int, default=1,  metavar='MOSAIC NGRAM FILE')

    args = parser.parse_args()

    if args.parallel > 1 and args.output_path != '-':
        raise ArgumentTypeError(f'Output must be STDOUT if processing parallel ({args.output_path}) !')

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, mosaic=args.mosaic, threshold=args.min_freq)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
