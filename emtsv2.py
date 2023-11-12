import sys
from os import cpu_count
from pathlib import Path
from multiprocessing import Pool
from argparse import ArgumentParser

from mosaic_lib.emtsv import analyse_input
from mosaic_lib.argparse_helpers import existing_file_or_dir_path, new_file_or_dir_path, int_greater_than_1, str2bool


def process_one_file(input_file, output_file, keep_fields, modules, server_name, conll_comments, retry):
    """
    Process a file into another file. Use binary files to avoid the encoding-decoidng overhead
    :param input_file: - for STDIN, filename or already opened file handle (for reading)
    :param output_file: - for STDOUT, filename or already opened file handle (for writing)
    :param keep_fields: The name of the fields to keep, None to keep all
    :param modules: The name of the modules to use
    :param server_name: The name of the emtsv server
    :param conll_comments: Keep CoNLL-style comments on output or not
    :param retry: The number of retries
    :return: Noting. Everything is written to output_file on success else exceptions are raised
    """
    close_inp_fh, close_out_fh = False, False
    if input_file == '-':
        inp_fh = sys.stdin
    elif isinstance(input_file, (str, Path)):
        inp_fh = open(input_file, 'rb')
        close_inp_fh = True
    elif hasattr(input_file, 'read'):
        inp_fh = input_file
    else:
        raise ValueError('Only STDIN, filename or file-like object is allowed as input !')

    if output_file == '-':
        out_fh = sys.stdout
    elif isinstance(input_file, (str, Path)):
        out_fh = open(output_file, 'wb')
        close_out_fh = True
    elif hasattr(input_file, 'writelines'):
        out_fh = output_file
    else:
        raise ValueError('Only STDOUT, filename or file-like object is allowed as output !')

    analyse_input(inp_fh, out_fh, keep_fields, modules, server_name, conll_comments, retry)

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
    parser.add_argument('-m', '--modules', type=str, nargs='+', required=True,
                        help='Modules to run in emtsv (denoted by module names)', metavar='MODULE_NAME')
    parser.add_argument('-k', '--keep-fields', type=str, nargs='+', default=None, metavar='FIELD_NAME',
                        help='Fields to keep in the output (denoted by field names, default: all)')
    parser.add_argument('-s', '--server-name', type=str, default='http://localhost:5000',
                        help='emtsv server name (default: http://localhost:5000)', metavar='https://servername:port')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-c', '--conll-comments', type=str2bool, nargs='?', const=True, default=True,
                        help='Keep comment in output (default: True)', metavar='True/False')
    parser.add_argument('-r', '--retry', type=int_greater_than_1, default=5,
                        help='Number of retries if there is network error (default: 5)', metavar='N')
    args = parser.parse_args()

    return args


# TODO this differs from processing_helpers.py one!
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
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(args.input_path, args.output_path,
                                                           (args.keep_fields, args.modules, args.server_name,
                                                            args.conll_comments, args.retry))  # This is a generator
    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_inp_out_fn_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path, *other_params in gen_inp_out_fn_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path, *other_params)


if __name__ == '__main__':
    main()
