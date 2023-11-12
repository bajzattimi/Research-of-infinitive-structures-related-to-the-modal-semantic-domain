from functools import partial

from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.filter import parse_filter_params, filter_sentence
from mosaic_lib.emtsv import parse_emtsv_format, format_emtsv_lines
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def filter_data(emtsv_sent_it, filter_params=((), (), None)):

    any_tok, cur_tok, substitute_tags = filter_params
    if substitute_tags is None:
        substitute_tags = {}

    deleted_per_rule_num = 0

    for n, (comment_lines, sent_orig) in enumerate(emtsv_sent_it, start=1):
        sent = []
        for tok in sent_orig:
            tok['xpostag'] = substitute_tags[tok['ORIGPOS']]
            sent.append(tok)
        clause_str = ' '.join(tok['form'] for tok in sent)
        delete_ex = filter_sentence(sent, any_tok, cur_tok, clause_str)
        if delete_ex:
            deleted_per_rule_num += 1
            continue  # TODO valahogy mégis bennemarad az üres mondat helye! tmk_cat.tsv 407-os sor.

        yield comment_lines, sent


def process_input_to_output(input_fh, output_fh, *other_args):
    """
    Process a file handle into another file handle or to a python structured form as a geneator on sentences.
     Use binary files to avoid the encoding-decoidng overhead (applies only if no field filtering i.e. keep_fields=None)
    :param input_fh: An already opened file handle (for reading)
    :param output_fh: An already opened file handle (for writing)
    :param other_args: Arguments to be passed to filter_data() function, details in the function
    :return: The stentence generator where every token is a dict in a list (=sentence) for all sentences OR
             Noting. Writes output to output_fh
    """
    orig_sent_it = parse_emtsv_format(input_fh)  # Format lines to sents
    converted_sent_it = filter_data(orig_sent_it, *other_args)  # Convert POS tags
    converted_lines_it = format_emtsv_lines(converted_sent_it)  # Format sent to lines

    output_fh.writelines(converted_lines_it)  # It actually writes an iterable only (not adding newlines)
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    process_i_to_o_partial = partial(process_input_to_output, filter_params=args.filter_params)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(process_i_to_o_partial, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
