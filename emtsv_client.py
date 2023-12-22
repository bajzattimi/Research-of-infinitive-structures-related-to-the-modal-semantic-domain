from functools import partial

from mosaic_lib.emtsv import analyse_input
from mosaic_lib.argparse_helpers import base_argparser_factory, int_greater_or_equal_than, str2bool
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs, \
    process_one_file


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-m', '--modules', type=str, nargs='+', required=True,
                        help='Modules to run in emtsv (denoted by module names)', metavar='MODULE_NAME')
    parser.add_argument('-k', '--keep-fields', type=str, nargs='+', default=None, metavar='FIELD_NAME',
                        help='Fields to keep in the output (denoted by field names, default: all)')
    parser.add_argument('-s', '--server-name', type=str, default='http://localhost:5000',
                        help='emtsv server name (default: http://localhost:5000)', metavar='https://servername:port')
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-c', '--conll-comments', type=str2bool, nargs='?', const=True, default=True,
                        help='Keep comment in output (default: True)', metavar='True/False')
    parser.add_argument('-r', '--retry', type=partial(int_greater_or_equal_than, min_val=1), default=5,
                        help='Number of retries if there is network error (default: 5)', metavar='N')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    analyse_input_partial = partial(analyse_input, keep_fields=args.keep_fields, modules=args.modules,
                                    server_name=args.server_name, conll_comments=args.conll_comments, retry=args.retry)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(analyse_input_partial, args.input_path, args.output_path)
    # We use binary mode as text is actually processed only on the remote side
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel,
                       process_one_file_fun=partial(process_one_file, mode='binary'))


if __name__ == '__main__':
    main()
