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

def main(inp_fn, out_fn):
    with open(inp_fn, 'rb') as inp_fh:
        soup = BeautifulSoup(inp_fh, 'lxml')

        corpus = soup.find('corpus')
        if corpus is not None:
            corpus_str = corpus.string.strip()

    with open(out_fn, 'w', encoding='UTF-8') as out_fh:
        print('form', file=out_fh)
        print(f'# corpus: {corpus_str}', file=out_fh)

        for out_line in gen_sents(soup):
            if out_line not in {'<s>', '</s>'}:
                print(out_line, file=out_fh)


def mnsz_sample_or_webcorpus_sample(soup):
    subqueries = soup.find_all('subquery')
    for subquery in subqueries:
        if subquery is not None and subquery.string is not None:
            return True


def mnsz_heading(soup):
    hits = soup.find('hits')
    queries = soup.find('query')
    hits_str, queries_str = '', ''
    for hit in hits:
        if hit is not None and hit.string is not None:
            hits_str = hit.string.strip()
    for query in queries:
        if query is not None and query.string is not None:
            queries_str = query.string.strip()
    return f'# hit: {hits_str} \n# query: {queries_str}'


def webcorpus_header(subquery):
    if subquery is not None and subquery.string is not None:
        subqueries_str = subquery.string.strip()
        return f'# subquery: {subqueries_str}'


def find_ref_in_mnsz(line_tag):
    if line_tag.ref is not None and line_tag.ref.string is not None:
        ref = line_tag.ref.string.strip()
        return f'# ref: {ref}'


def find_ref_in_webcorpus(ref):
        ref_str = ref.get('refs')
        if ref_str is not None:
            return f'# ref: {ref_str}'


left_context()
right_context()


def context(line_tag):

    if line_tag.left_context is not None:
        yield from get_side(line_tag.left_context)
    elif line_tag.left is not None:
        yield from get_side(line_tag.left)

    if line_tag.kwic is not None:
        yield from get_side(line_tag.kwic)

    if line_tag.right_context is not None:
        yield from get_side(line_tag.right_context)
    elif line_tag.right is not None:
        yield from get_side(line_tag.right)

def get_side(curr_context):
    if curr_context is not None and curr_context.string is not None:
        for tok in curr_context.string.strip().split():
            yield tok
    else:
        raise ValueError('VALAMI HIBAÜZENET!')


if __name__ == '__main__':
    main('akar_fni_500_webcorpus.xml', 'akar_fni_500_webcorpus.tsv')

