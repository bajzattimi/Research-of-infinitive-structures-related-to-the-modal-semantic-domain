from itertools import chain
from functools import partial
from collections import Counter
from argparse import ArgumentTypeError

from mosaic_lib.ngram import ngram
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def mosaic_bow_to_tuple(mosaic):
    ret = []
    mosaic_len = 0
    skip = False
    for first, second in ngram(chain(mosaic, ['']), 2):
        if skip:
            skip = False
            continue  # Skip count elems (e.g. (2) ) as "first"
        if first.startswith('lemma:'):
            feat_val = ('lemma', first[6:])
        elif first.startswith('['):
            feat_val = ('xpostag', first)
        else:
            feat_val = ('form', first)
        if second.startswith('(') and second.endswith(')') and second[1:-1].isnumeric():
            count = int(second[1:-1])
            skip = True
        else:
            count = 1
        mosaic_len += count
        ret.append((feat_val, count))

    return tuple(ret), mosaic_len


def create_window(inp_fh, out_fh, mosaic):
    # Replace previously escaped # characters before going any further
    mosaic = mosaic.replace('\\u0023', '#')
    mosaic_toks, mosaic_len = mosaic_bow_to_tuple(mosaic.split())
    for sent_id, (comment_lines, sent) in enumerate(parse_emtsv_format(inp_fh)):
        clause_len = len(next((line for line in comment_lines if line.startswith('clause: ')))[8:].split())
        if clause_len != mosaic_len:  # TODO
            continue
        # Assign every field_val_count triplet the sent_ids they are observed
        # Add every (field, value) pair for every token to the counter
        sent_tok_field_val_counter = Counter()
        for tok in sent:
            sent_tok_field_val_counter.update(tok.items())
        field_val_count = set()
        for field_val, count in sent_tok_field_val_counter.items():
            # Add lower counts too to allow matching with fewer elements!
            #  e.g. mosaic contains a lemma which originally had the same POS tag as some other element making count 2
            #   We care only for ONE occurrence of the POS tag so we need to add the sent id in the dict
            #   with both counts for exact match!
            for fewer in range(count, 0, -1):
                field_val_count.add((field_val, fewer))

        # The sent (which has equal length as the mosaic n-gram) should have at least
        #  the number of mosaic elems as in the mosaic n-gram e.g. simple bag of words with counts
        #  WARNING: We can count a tok in the sent twice because the different abstractions (should be rare)
        #   Handling this would lead to an NP-time constraint satisfaction task :(
        #
        # We do exact lookup! So count == 2 should match count == 1 to get count <= 2 !
        if all(triplet in field_val_count for triplet in mosaic_toks):
            print(sent_id, ' '.join(tok['form'] for tok in sent), sep='\t', file=out_fh)
            # print(' '.join('#'.join((tok['form'], tok['lemma'], tok['xpostag'])) for tok in sent), file=out_fh)


# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-m', '--mosaic', type=str, metavar='MOSAIC NGRAM', required=True)

    args = parser.parse_args()

    if args.parallel > 1 and args.output_path != '-':
        raise ArgumentTypeError(f'Output must be STDOUT if processing parallel ({args.output_path}) !')

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    create_window_partial = partial(create_window, mosaic=args.mosaic)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(create_window_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
