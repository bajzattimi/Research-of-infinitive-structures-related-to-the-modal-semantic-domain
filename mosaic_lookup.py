from functools import partial
from argparse import ArgumentTypeError

from mosaic_lib.ngram import ngram
from mosaic_lib.emtsv import parse_emtsv_format
from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


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
    for sent_id, (comment_lines, sent) in enumerate(parse_emtsv_format(inp_fh)):
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
        if all(mosaic_word.items() <= word.items() for mosaic_word, word in zip(mosaic_toks, sent)):
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
