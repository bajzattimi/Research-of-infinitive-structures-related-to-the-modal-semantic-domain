import sys
from os import cpu_count
from pathlib import Path
from multiprocessing import Pool
from argparse import ArgumentParser

from mosaic_lib.filter import parse_filter_params, filter_sentence
from mosaic_lib.emtsv import parse_emtsv_format, format_emtsv_lines
from mosaic_lib.argparse_helpers import existing_file_or_dir_path, new_file_or_dir_path, int_greater_than_1


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
            continue

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


def process_one_file(input_file, output_file, *other_args):
    """
    Process a file into another file. Use binary files to avoid the encoding-decoidng overhead
    :param input_file: - for STDIN, filename or already opened file handle (for reading)
    :param output_file: - for STDOUT, filename or already opened file handle (for writing)
    :param other_args: Arguments to be passed to process_input_to_output() function, details in the function
    :return: Noting. Everything is written to output_file on success else exceptions are raised
    """
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
    elif isinstance(input_file, (str, Path)):
        out_fh = open(output_file, 'w', encoding='UTF-8')
        close_out_fh = True
    elif hasattr(input_file, 'writelines'):
        out_fh = output_file
    else:
        raise ValueError('Only STDOUT, filename or file-like object is allowed as output !')

    process_input_to_output(inp_fh, out_fh, *other_args)

    # Without with statement we need to close opened files manually!
    if close_inp_fh:
        inp_fh.close()

    if close_out_fh:
        out_fh.close()


# ####### END argparse helpers, needed to be moved into a common file ####### #

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_path', type=existing_file_or_dir_path,
                        help='Path to the input file or directory containing the corpus sample', default='-')
    parser.add_argument('-o', '--output', dest='output_path', type=new_file_or_dir_path,
                        help='Path to the output file or directory containing the corpus sample', default='-')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
    parser.add_argument('-f', '--filter', dest='filter_params', type=parse_filter_params,
                        help='Filter params YAML file', default=([], [], None), required=False)
    args = parser.parse_args()

    return args


# TODO this differs from processing_helpers.py one! Same as in emtsv2.py
def gen_input_output_filename_pairs(input_path, output_path, other_opts):
    if Path(input_path).is_dir() and Path(output_path).is_dir():
        for inp_fname_w_path in Path(input_path).glob('*.tsv'):
            yield inp_fname_w_path, Path(output_path) / f'{inp_fname_w_path.stem}.tsv', *other_opts
    elif ((input_path == '-' or Path(input_path).is_file()) and
          ((output_path == '-') or not Path(output_path).is_dir())):
        yield input_path, output_path, *other_opts
    else:
        raise ValueError(f'Input and output must be both files (including STDIN/STDOUT) or directories'
                         f' ({(input_path, output_path)}) !')


def main():
    args = parse_args()  # Input dir and output dir sanitized
    # Extra params to pass, currently one
    extra_params_tuple = (args.filter_params,)
    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path, extra_params_tuple)
    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
