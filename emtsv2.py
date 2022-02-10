import sys
from os import cpu_count
from pathlib import Path
from multiprocessing import Pool
from requests import post as requests_post
from requests.exceptions import RequestException
from argparse import ArgumentParser, ArgumentTypeError


class EMTSVRequestException(Exception):
    pass


def execute_request(input_iterator, modules=(), server_name='http://localhost:5000', conll_comments=True, retry=5):
    if len(modules) == 0:
        raise ValueError(f'emtsv modules are empty: {modules} !')

    for i in range(1, retry+1):
        try:
            r = requests_post(f'{server_name}/{"/".join(modules)}', files={'file': input_iterator},
                              data={'conll_comments': conll_comments}, stream=True)
            if r.status_code != 200:
                print('emtsv error happened (try', i, '):', r.status_code, r.reason, file=sys.stderr)
            else:
                return r.iter_lines(decode_unicode=True)
        except RequestException as e:
            print('Network error happened (retry', i, '):', e, file=sys.stderr)
    else:
        raise EMTSVRequestException(f'Could not process input: {input_iterator}')


def parse_emtsv_format(input_iterator, keep_fields=None):
    header = next(input_iterator, None)
    if header is not None:
        header_splitted = [col for col in header.rstrip().split('\t') if len(col) > 0]  # TODO üres mezők ellenőrzése, volt-e üres mező, dobjon exceptiont, ha volt
    else:
        header_splitted = []

    if len(header_splitted) == 0:
        raise ValueError(f'Input header is not valid ({header_splitted}) !')

    if isinstance(keep_fields, set):
        header_filtered = []
        for col in header_splitted:
            if col in keep_fields:
                header_filtered.append(col)
            else:
                header_filtered.append(None)
    else:
        header_filtered = header_splitted

    comment, sent = [], []
    for i, line in enumerate(input_iterator, start=2):
        line = line.rstrip('\n')
        if len(line) == 0:  # State 1: empty line (after sentences)
            # Yield the collected sentence and start a new one
            yield comment, sent
            comment, sent = [], []
        elif line.startswith('# '):  # State 2: Comment, metadata
            comment.append(line[2:])  # Strip '# ' prefix
        else:  # State 3: A line containing a token
            line_splitted = line.split('\t')  # Split to columns
            # We filter out columns not in keep_fields therefore denoted by None in header_filtered
            token = {k: v for k, v in zip(header_filtered, line_splitted) if k is not None}
            sent.append(token)

    if len(comment) > 0 or len(sent) > 0:  # Yield all remaining tokens or metadata lines
        yield comment, sent


# TODO this will be public API Wire-out to the CLI!
def analyse_input(input_iterator, output_iterator=None, keep_fields=None, modules=(),
                  server_name='http://localhost:5000', conll_comments=True, retry=5):
    resp = execute_request(input_iterator, modules, server_name, conll_comments, retry)
    if output_iterator is not None:
        output_iterator.writelines(resp)  # Write raw output to file without parsing
    else:
        yield from parse_emtsv_format(resp, keep_fields)  # Parse and rerturn a sentence iterator


def process_one_file(input_file, output_file):
    with open(input_file, encoding='UTF-8') as inp_fh, open(output_file, 'w', encoding='UTF-8') as out_fh:
        analyse_input(inp_fh, out_fh)


def existing_dir_path(string):
    if not Path(string).is_dir():
        raise ArgumentTypeError(f'{string} is not an existing directory!')
    return string


def new_dir_path(string):
    dir_name = Path(string)
    dir_name.mkdir(parents=True, exist_ok=True)  # Create dir
    if next(Path(dir_name).iterdir(), None) is not None:
        raise ArgumentTypeError(f'{string} is not an empty directory!')
    return string


def int_greater_than_1(string):
    try:
        val = int(string)
    except ValueError:
        val = -1  # Intentional bad value if value can not be converted to int()

    if val <= 1:
        raise ArgumentTypeError(f'{string} is not an int > 1!')

    return val


# TODO process STDIN to STDOUT by default
def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-dir', type=existing_dir_path,
                        help='Path to the input directory containing the corpus sample', required=True)
    parser.add_argument('-o', '--output-dir', type=new_dir_path,
                        help='Path to the output directory', required=True)
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
    parser.add_argument('-stdin', '--stdin', type=sys.stdin, help='Standard input', required=True)
    parser.add_argument('-stdout', '--stdout', type=sys.stdout, help='Standard output', required=True)
    parser.add_argument('-stderr', '--strderr', type=sys.stderr, help='Error', required=True)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()  # Input dir and output dir sanitized
    # This is a generator
    gen_input_output_filename_pairs = ((inp_fname_w_path, Path(args.output_dir) / f'{inp_fname_w_path.stem}.tsv')
                                       for inp_fname_w_path in Path(args.input_dir).glob('*.xml'))
    if args.parallel > 1:
        with Pool(processes=args.parallel) as p:
            # Starmap allows unpackig tuples from iterator as multiple arguments
            p.starmap(process_one_file, gen_input_output_filename_pairs)
    else:
        for inp_fname_w_path, out_fname_w_path in gen_input_output_filename_pairs:
            process_one_file(inp_fname_w_path, out_fname_w_path)


if __name__ == '__main__':
    main()
