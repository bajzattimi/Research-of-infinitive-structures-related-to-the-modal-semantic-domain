import sys
import gzip
from functools import partial
from collections import deque
from argparse import ArgumentTypeError
from itertools import groupby, chain

from mosaic_lib.scoring import mosaic_to_tok
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import base_argparser_factory, existing_file
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def determine_mosaic_length(mosaic):
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        first_line = next(mosaic_fh, None)
        if first_line is None:
            return -1
        first_line = first_line.strip().split()

    return len(first_line) - 1  # Remove count!


def create_window(inp_fh, out_fh, mosaic, threshold):
    # 1. Determine the length of all mosaic from the first one
    mosaic_len = determine_mosaic_length(mosaic)
    if mosaic_len == -1:  # Empty file
        return
    # 2. Cache all examples with matching length
    example_clauses_with_matching_length = []
    for comment_lines, sent in parse_emtsv_format(inp_fh):
        clause_len = len(next((line for line in comment_lines if line.startswith('clause: ')))[8:].split())
        if clause_len != mosaic_len:
            continue
        example_clauses_with_matching_length.append((comment_lines, sent))

    mosaics_by_freq = deque()
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        # 3. Group by freq and score group elements (split will take care of \n)
        for key, group_it in groupby(mosaic_fh, key=lambda x: x.split(maxsplit=1)[0]):
            print(key, file=sys.stderr)
            if int(key) < threshold:
                break
            mosaic_group = {}
            mosaic_to_examples = {}

            # Strip freq from the line with leading spaces
            curr_mosaic = next(group_it)
            mos_group_freq_ind = curr_mosaic.find(' ', len(curr_mosaic) - len(curr_mosaic.lstrip(' ')))
            mos_group_freq_str = curr_mosaic[:mos_group_freq_ind]
            for curr_mosaic in chain((curr_mosaic,), group_it):
                # Replace previously escaped # characters before going any further
                curr_mosaic = tuple(m.replace('\\u0023', '#') for m in curr_mosaic.split()[1:])
                mosaic_toks, score = mosaic_to_tok(curr_mosaic)
                mosaic_group[curr_mosaic] = score

                # 4. For the matching clauses store the example clause  # TODO reverse index?
                curr_mosaic_to_examples = set()
                for comment_lines, sent in example_clauses_with_matching_length:
                    if all(mosaic_word.items() <= word.items() for mosaic_word, word in zip(mosaic_toks, sent)):
                        example_clause = tuple((tok['form'], tok['lemma'], tok['xpostag']) for tok in sent)
                        curr_mosaic_to_examples.add(example_clause)
                mosaic_to_examples[curr_mosaic] = curr_mosaic_to_examples

            # 5. Collect example sets mapped to mosaics describes them and have the max score (=most concrete)
            best_mosaics_by_example_sets = {}
            for mosaic_ngram, example_set in mosaic_to_examples.items():
                ex_key = frozenset(example_set)
                mos_score = mosaic_group[mosaic_ngram]

                current = best_mosaics_by_example_sets.get(ex_key)
                # If not stored or has better score -> (Drop previously stored and) store the current
                if current is None or mos_score > current[0]:
                    best_mosaics_by_example_sets[ex_key] = (mos_score, {mosaic_ngram})
                elif mos_score == current[0]:  # If stored and have equal score, add mosaic
                    current[1].add(mosaic_ngram)

            # 6. Sort mosaics with collected max score in lexicographical order
            for ex_set, (_, mosaics) in best_mosaics_by_example_sets.items():
                for mos in sorted(mosaics):
                    mosaics_by_freq.append((mos_group_freq_str, mos, ex_set))

    # 7. Create 2-level nested groups if the matching examples are subset of each other for the two mosaic
    while len(mosaics_by_freq) > 0:
        mos_group_freq_str, mos, ex_set = mosaics_by_freq.popleft()
        print('level2', mos_group_freq_str, file=sys.stderr)
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
    parser.add_argument('-f', '--min-freq', dest='min_freq', type=int, default=1, metavar='MOSAIC NGRAM FILE')

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
