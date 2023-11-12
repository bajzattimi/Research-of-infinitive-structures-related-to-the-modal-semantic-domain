import sys
import gzip
from pathlib import Path
from collections import defaultdict, deque, Counter
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser

from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import int_greater_than_1, existing_file_or_dir_path, existing_file


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


def mosaic_to_bow(mosaic_fh):
    for curr_mosaic in mosaic_fh:
        freq = int(curr_mosaic.strip().split()[0])
        curr_mosaic = tuple(curr_mosaic.strip().split()[1:])
        mosaic_toks, score = mosaic_to_tok(curr_mosaic)

        # Add every (field, value) pair for every token to the counter
        mosaic_tok_counter = Counter()
        for tok in mosaic_toks:
            mosaic_tok_counter.update(tok.items())
        # Sum freqs of same BOW mosaic n-grams
        mosaic_bow_tuple = tuple(sorted(mosaic_tok_counter.items(), key=lambda x: (x[0], -x[1])))
        # We do care only for no. of the matching sentences, not n-gram freqs
        yield freq, score, mosaic_bow_tuple


def mosaic_bow_tuple_to_printable(curr_mosaic):
    curr_mosaic_bow_printable = []
    for (mos_field, mos_val), mos_tok_field_value_count in curr_mosaic:
        if mos_field == 'lemma':  # # Normal fields(form, xpostag) are left alone, lemma field gets lemma: prefix!
            mos_val = f'lemma:{mos_val}'
        freq_printable = ''
        if mos_tok_field_value_count > 1:
            freq_printable = f' ({mos_tok_field_value_count})'
        curr_mosaic_bow_printable.append(f'{mos_val}{freq_printable}')
    return tuple(curr_mosaic_bow_printable)


def get_matching_sent_ids(curr_mosaic, field_val_count_to_sent_id):
    # The sent (which has equal length as the mosaic n-gram) should have at least
    #  the number of masaic elems as in the mosaic n-gram e.g. simple bag of words with counts
    #  WARNING: We can count a tok in the sent twice because the different abstractions (should be rare)
    #   Handling this would lead to an NP-time contraint satisfaction task :(
    #
    # We do exact lookup! So count == 2 should match count == 1 to get count <= 2 !
    matching_sent_ids = field_val_count_to_sent_id.get(curr_mosaic[0], set())
    for triplet in curr_mosaic[1:]:
        sent_ids = field_val_count_to_sent_id.get(triplet, set())
        # We must copy the set to keep the original unmodified...
        matching_sent_ids = matching_sent_ids & sent_ids  # all()
        if len(matching_sent_ids) == 0:
            return frozenset()

    return frozenset(matching_sent_ids)


def cache_sent_ids_w_matching_len(inp_fh, mosaic_len, threshold):
    field_val_count_to_sent_id = defaultdict(set)
    for sent_id, (comment_lines, sent) in enumerate(parse_emtsv_format(inp_fh)):
        clause_len = len(next((line for line in comment_lines if line.startswith(' clause: ')))[9:].split())
        if clause_len != mosaic_len:
            continue
        # Assing every field_val_count triplet the sent_ids they are observed
        # Add every (field, value) pair for every token to the counter
        sent_tok_field_val_counter = Counter()
        for tok in sent:
            sent_tok_field_val_counter.update(tok.items())
        for field_val, count in sent_tok_field_val_counter.items():
            # Add lower counts too to allow matcing with fewer elements!
            #  e.g. mosaic contains a lemma which originally had the same POS tag as some other element making count 2
            #   We care only for ONE occurence of the POS tag so we need to add the sent id in the dict
            #   with both counts for exact match!
            for fewer in range(count, 0, -1):
                field_val_count_to_sent_id[(field_val, fewer)].add(sent_id)

    field_val_count_to_sent_id_pruned = {field_val_count: sent_ids
                                         for field_val_count, sent_ids in field_val_count_to_sent_id.items()
                                         if len(sent_ids) >= threshold}
    return field_val_count_to_sent_id_pruned


def create_window(inp_fh, out_fh, mosaic, threshold):
    # 1. Determine the lehgth of all mosaic from the first one
    mosaic_len = determine_mosaic_length(mosaic)
    if mosaic_len == -1:  # Empty file
        return
    # 2. Cache all examples with matching length
    field_val_count_to_sent_id = cache_sent_ids_w_matching_len(inp_fh, mosaic_len, threshold)

    mosaic_to_examples = {}
    with gzip.open(mosaic, 'rt', encoding='UTF-8') as mosaic_fh:
        # 3. Group by freq and score group elements
        # We do not utilise the increased frequency beyond ordering after the mozaic->BOW conversion,
        # as the no. of matching examples will be used as the final decision
        for freq, mosaic_score, curr_mosaic in mosaic_to_bow(mosaic_fh):
            # 4. For the matching clauses store the example clause
            matching_sent_ids = get_matching_sent_ids(curr_mosaic, field_val_count_to_sent_id)
            len_matching_sent_ids = len(matching_sent_ids)

            assert threshold > freq or freq <= len_matching_sent_ids, \
                f'Mosaic ({curr_mosaic}) should not match less examples with BOW ({len_matching_sent_ids}) ' \
                f'than with n-grams ({freq})!'
            #  As field val count triplets are pruned to minimum freq threshold
            #  non-matching and rare elaments can be treated the same way
            if len_matching_sent_ids == 0:
                continue  # Mosaic matches too few examples

            # We do not interpet the mosaic's value from here on!
            curr_mosaic_bow_printable = mosaic_bow_tuple_to_printable(curr_mosaic)
            mosaic_to_examples[(curr_mosaic_bow_printable, mosaic_score)] = (len_matching_sent_ids, matching_sent_ids)

    mosaics_by_freq = deque()
    # 5. Group by example sets
    examples_to_mosaic = defaultdict(set)
    for mosaic_ngram_and_score, len_example_set_and_example_set in mosaic_to_examples.items():
        examples_to_mosaic[len_example_set_and_example_set].add(mosaic_ngram_and_score)
    # 6. Get max score per "example set" and print mosaics with that score
    #    For BOW the number of matched examples means the new frequency, not the added freq of the n-grams
    for (len_ex_set, ex_set), mosaic_set in sorted(examples_to_mosaic.items(),
                                                   key=lambda x: (-x[0][0], x[0][1], x[1])):
        # The first elem will be the maximum as they are sorted
        mosaic_set_sorted = sorted(mosaic_set, key=lambda x: (-x[1], x[0]))
        max_score = mosaic_set_sorted[0][1]
        for mos, mos_score in mosaic_set:
            if mos_score == max_score:
                mosaics_by_freq.append((len_ex_set, mos, ex_set))
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
