import sys

from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.emtsv import parse_emtsv_format, format_emtsv_lines
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


def split_fields(emtsv_sent_it):
    for n, (comment_lines, sent_orig) in enumerate(emtsv_sent_it, start=1):
        sent = []
        for tok in sent_orig:
            form_orig = tok['form']
            try:
                form, lemma, tag = form_orig.split('/', maxsplit=2)
            except ValueError:
                form, lemma, tag = '', '', ''
            if not tag.startswith('['):
                print(form_orig, file=sys.stderr)
            tok['form'] = form
            tok['lemma'] = lemma
            tok['xpostag'] = tag
            sent.append(tok)
        comment_lines[-1] = f'sent: {" ".join(tok["form"] for tok in sent)}'

        yield comment_lines, sent


def process_input_to_output(input_fh, output_fh):
    """
    Process a file handle into another file handle or to a python structured form as a generator on sentences.
     Use binary files to avoid the encoding-decoding overhead (applies only if no field filtering i.e. keep_fields=None)
    :param input_fh: An already opened file handle (for reading)
    :param output_fh: An already opened file handle (for writing)
    :return: The sentence generator where every token is a dict in a list (=sentence) for all sentences OR
             Noting. Writes output to output_fh
    """
    orig_sent_it = parse_emtsv_format(input_fh)  # Format lines to sents
    converted_sent_it = split_fields(orig_sent_it)  # Convert POS tags
    converted_lines_it = format_emtsv_lines(converted_sent_it)  # Format sent to lines

    output_fh.writelines(converted_lines_it)  # It actually writes an iterable only (not adding newlines)


# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(process_input_to_output, args.input_path, args.output_path)
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel)


if __name__ == '__main__':
    main()
