import sys
from itertools import chain
from functools import partial
from argparse import ArgumentTypeError

from bs4 import BeautifulSoup

from mosaic_lib.argparse_helpers import base_argparser_factory
from mosaic_lib.processing_helpers import process_one_by_one, gen_input_output_filename_pairs


# Open BeautifulSoup library: File -> Settings -> Build, Execution, Deployment -> /
# Project Interpreter -> + -> BeautifulSoup -> Install package
# Open lxml library: File -> Settings -> Build, Execution, Deployment -> /
# Project Interpreter -> + -> lxml -> Install package
# lxml is imported automatically by BeautiflulSoup('lxml-xml')


def gen_sents(soup):
    """
    This row specifies the corpus from which the sample is taken and names the variables according to this corpus
    :param soup:
    :return:
    """
    get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = identify_sample_type(soup)

    yield 'form\n'  # Line breaks
    yield from get_heading(soup)  # Inserts heading
    for line_tag in soup.find_all('line'):
        # Inserts context
        left_toks, kwic_toks, right_toks = context(line_tag, left_cont_name, kwic_name, right_cont_name)
        if len(left_toks) > 0 and left_toks[0] == '<s>':
            left_toks = left_toks[1:]
        if len(right_toks) > 0 and right_toks[-1] == '</s>':
            right_toks = right_toks[:-1]  # Deletes unnecessary <s> tags

        yield f'# ref: {find_ref_in_corp(line_tag)}\n'  # Collects the data references (<ref>)
        yield f'# left_length: {len(left_toks)}\n'
        yield f'# kwic_length: {len(kwic_toks)}\n'
        yield f'# right_length: {len(right_toks)}\n'
        yield f'# sent: {" ".join(chain(left_toks, kwic_toks, right_toks))}\n'
        yield '\n'.join(chain(left_toks, kwic_toks, right_toks))
        yield '\n\n'


def identify_sample_type(soup):
    """
    Specifies from which corpus the sample was taken
    :param soup:
    :return:
    """
    if len(soup.find_all('subquery')) > 0:  # Webcorpus type sample
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            webcorpus_heading, find_ref_in_webcorpus, 'left', 'kwic', 'right'
    elif soup.find('hits') is not None:  # MNSz type sample
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            mnsz_heading, find_ref_in_mnsz, 'left_context', 'kwic', 'right_context'
    else:
        raise ValueError('We could not decide which sample it was')

    return get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name  # Returns the names of the tags


def webcorpus_heading(soup):  # Finds the Webcorpus type heading
    heading_tag = get_child(soup, 'header', recursive=True)
    yield f'# corpus: { get_tag_text(get_child(heading_tag, "corpus"))}\n'  # Inserts the <corpus> tag
    yield f'# subcorpus: { get_tag_text(get_child(heading_tag, "subcorpus"), can_be_empty=True)}\n'  # Subcorpus empty!
    for subquery_tag in heading_tag.find_all('subquery'):
        yield f'# subquery:\n'
        yield f'#     operation: {get_attr_from_tag(subquery_tag, "operation")}\n'
        yield f'#     size: {get_attr_from_tag(subquery_tag, "size")}\n'
        yield f'#     value: {get_tag_text(subquery_tag)}\n'


def mnsz_heading(soup):  # Finds the MNSz type heading
    heading_tag = get_child(soup, 'heading', recursive=True)
    for name in ('corpus', 'hits', 'query'):
        yield f'# {name}: {get_tag_text(get_child(heading_tag, name))}\n'


def find_ref_in_webcorpus(line_tag):  # Finds the Webcorpus type references <line refs="">
    return get_attr_from_tag(line_tag, 'refs')


def find_ref_in_mnsz(line_tag):  # Finds the MNSz type references <ref>
    return get_tag_text(get_child(line_tag, 'ref'))


def context(line_tag, left_str, kwic_str, right_str):  # Finds contexts (left, kwic and right)
    ret = []
    # Left context can be empty, KWIC can not be empty, right context can be empty
    for tag_name, can_be_empty in ((left_str, True), (kwic_str, False), (right_str, True)):
        ret.append([t for t in get_tag_text(get_child(line_tag, tag_name), can_be_empty).split(' ') if len(t) > 0])
    return ret


def get_attr_from_tag(tag, attr_name):   # This function finds the value of a specified attribute of a tag
    value_str = tag.get(attr_name)
    if value_str is None:
        raise ValueError(f'{attr_name} can not be found in {tag.name}!')
    return value_str


def get_child(soup, curr_context_str, recursive=False):
    curr_context_tag = soup.find(curr_context_str, recursive=recursive)
    if curr_context_tag is None:
        raise ValueError(f'{curr_context_str} can not be found in {soup.name} with recursive {recursive}')
    return curr_context_tag


def get_tag_text(curr_context_tag, can_be_empty=False):  # This function finds specified tags
    curr_context_string = curr_context_tag.string
    if curr_context_string is not None:
        return curr_context_string.strip()
    elif not can_be_empty:
        raise ValueError(f'{curr_context_tag.name} has no string content!')
    return ''


def encoding_fixer_beautiful_soup(inp_fh, from_enc=None, to_enc=None):
    if from_enc is not None and to_enc is not None:
        cont = inp_fh.read().decode('UTF-8').encode('latin2')
    else:
        cont = inp_fh
    # XML parser ('lxml' HTML parser, 'lxml-xml' XML parser)
    return BeautifulSoup(cont, 'lxml-xml')


def process_one_file_w_bs4(internal_fun, input_file, output_file, from_enc=None, to_enc=None):
    _ = internal_fun  # Dummy to keep API compatibility
    if input_file != '-':
        with open(input_file, 'rb') as inp_fh:
            soup = encoding_fixer_beautiful_soup(inp_fh, from_enc, to_enc)
    else:
        soup = encoding_fixer_beautiful_soup(sys.stdin, from_enc, to_enc)

    if output_file != '-':
        with open(output_file, 'w', encoding='UTF-8') as out_fh:
            out_fh.writelines(gen_sents(soup))
    else:
        sys.stdout.writelines(gen_sents(soup))
# ####### BEGIN argparse helpers ####### #


def parse_args():
    parser = base_argparser_factory()
    parser.add_argument('-f', '--from-enc', type=str, default=None, metavar='ENCODING',
                        help='From encoding if it needs to be fixed (must be mutually set with to-enc)')
    parser.add_argument('-t', '--to-enc', type=str, default=None, metavar='ENCODING',
                        help='To encoding if it needs to be fixed (must be mutually set with from-enc)')

    args = parser.parse_args()

    if (args.from_enc is None and args.to_enc is not None) or (args.from_enc is not None and args.to_enc is None):
        raise ArgumentTypeError(f'--from-enc must be mutually set with --to-enc !')

    return args


def main():
    args = parse_args()  # Input and output sanitized
    # Process_one_file's internal function with params other than input/output fixed
    process_one_file_w_bs4_partial = partial(process_one_file_w_bs4, from_enc=args.from_enc, to_enc=args.to_enc)

    # This is a generator
    gen_inp_out_fn_pairs = gen_input_output_filename_pairs(process_one_file_w_bs4_partial, args.input_path,
                                                           args.output_path, input_glob='*.xml')
    process_one_by_one(gen_inp_out_fn_pairs, args.parallel, process_one_file_fun=process_one_file_w_bs4_partial)


if __name__ == '__main__':
    main()
