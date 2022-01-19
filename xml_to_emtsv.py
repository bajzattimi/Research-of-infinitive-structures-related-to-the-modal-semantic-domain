from os import cpu_count
from pathlib import Path
from itertools import chain
from argparse import ArgumentParser, ArgumentTypeError
from bs4 import BeautifulSoup


def gen_sents(soup):
    get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = identify_sample_type(soup)

    yield 'form\n'
    yield from get_heading(soup)
    for line_tag in soup.find_all('line'):

        left_toks, kwic_toks, right_toks = context(line_tag, left_cont_name, kwic_name, right_cont_name)
        if len(left_toks) > 0 and left_toks[0] == '<s>':
            left_toks = left_toks[1:]
        if len(right_toks) > 0 and right_toks[-1] == '</s>':
            right_toks = right_toks[:-1]

        yield f'# ref: {find_ref_in_corp(line_tag)}\n'
        yield f'# left_length: {len(left_toks)}\n'
        yield f'# kwic_length: {len(kwic_toks)}\n'
        yield f'# right_length: {len(right_toks)}\n'
        yield f'# sent: {" ".join(chain(left_toks, kwic_toks, right_toks))}\n'
        yield '\n'.join(chain(left_toks, kwic_toks, right_toks))
        yield '\n\n'


def identify_sample_type(soup):
    if len(soup.find_all('subquery')) > 0:  # Webcorpus type sample
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            webcorpus_heading, find_ref_in_webcorpus, 'left', 'kwic', 'right'
    elif soup.find('hits') is not None:  # MNSZ type sample
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            mnsz_heading, find_ref_in_mnsz, 'left_context', 'kwic', 'right_context'
    else:
        raise ValueError('Nem tudtuk eldönteni, hogy melyik mintáról van szó')

    return get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name


def webcorpus_heading(soup):
    heading_tag = get_child(soup, 'header', recursive=True)
    yield f'# corpus: { get_tag_text(get_child(heading_tag, "corpus"))}\n'
    yield f'# subcorpus: { get_tag_text(get_child(heading_tag, "subcorpus"), can_be_empty=True)}\n'  # Subcorpus empty!
    for subquery_tag in heading_tag.find_all('subquery'):
        yield f'# subquery:\n'
        yield f'#     operation: {get_attr_from_tag(subquery_tag, "operation")}\n'
        yield f'#     size: {get_attr_from_tag(subquery_tag, "size")}\n'
        yield f'#     value: {get_tag_text(subquery_tag)}\n'


def mnsz_heading(soup):
    heading_tag = get_child(soup, 'heading', recursive=True)
    for name in ('corpus', 'hits', 'query'):
        yield f'# {name}: {get_tag_text(get_child(heading_tag, name))}\n'


def find_ref_in_webcorpus(line_tag):
    return get_attr_from_tag(line_tag, 'refs')


def find_ref_in_mnsz(line_tag):
    return get_tag_text(get_child(line_tag, 'ref'))


def context(line_tag, left_str, kwic_str, right_str):
    left = get_tag_text(get_child(line_tag, left_str), can_be_empty=True).split(' ')    # Left context can be empty!
    kwic = get_tag_text(get_child(line_tag, kwic_str)).split(' ')                       # Kwic can not be empty!
    right = get_tag_text(get_child(line_tag, right_str), can_be_empty=True).split(' ')  # Right context can be empty!
    return left, kwic, right


def get_attr_from_tag(tag, attr_name):
    value_str = tag.get(attr_name)
    if value_str is None:
        raise ValueError('What attribute is not under the tag!')
    return value_str


def get_child(soup, curr_context_str, recursive=False):
    curr_context_tag = soup.find(curr_context_str, recursive=recursive)
    if curr_context_tag is None:
        raise ValueError('Which tag is not under which tag and directly or not?!')
    return curr_context_tag


def get_tag_text(curr_context_tag, can_be_empty=False):
    curr_context_string = curr_context_tag.string
    if curr_context_string is not None:
        return curr_context_string.strip()
    elif not can_be_empty:
        raise ValueError('Which tag is empty?')
    return ''


def process_one_file(input_file, output_file):
    with open(input_file, 'rb') as inp_fh:
        soup = BeautifulSoup(inp_fh, 'lxml-xml')

    with open(output_file, 'w', encoding='UTF-8') as out_fh:
        out_fh.writelines(gen_sents(soup))


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
        val = -1  # Bad value

    if val <= 1:
        raise ArgumentTypeError(f'{string} is not an int > 1!')

    return val


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-dir', type=existing_dir_path,
                        help='Path to the input directory containing the corpus sample', required=True)
    parser.add_argument('-o', '--output-dir', type=new_dir_path,
                        help='Path to the input directory containing the corpus sample', required=True)
    # nargs=? means one or zero values allowing -p without value -> returns const, if totally omitted -> returns default
    parser.add_argument('-p', '--parallel', type=int_greater_than_1, nargs='?', const=cpu_count(), default=1,
                        help='Process in parallel in N process', metavar='N')
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

