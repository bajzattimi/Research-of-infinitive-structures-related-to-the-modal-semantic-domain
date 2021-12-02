from bs4 import BeautifulSoup


def gen_sents(soup):
    if mnsz_sample_or_webcorpus_sample(soup) is None:
        yield mnsz_heading(soup)


        lines = soup.find_all('line')
        for line_tag in lines:
            yield find_ref_in_mnsz(soup, line_tag)
            yield from find_left_context(soup, line_tag)
            yield find_kwic_in_mnsz(soup, line_tag)
            yield from find_right_context(soup, line_tag)
            yield ''


    else:
        subqueries = soup.find_all('subquery')
        for subquery in subqueries:
            yield webcorpus_header(soup, subquery, subqueries)
        lines = soup.find_all('line')
        for line_tag in lines:
            ref = line_tag
            yield find_ref_in_webcorpus(soup, ref)
            yield from find_left_context(soup, line_tag)
            yield find_kwic_in_mnsz(soup, line_tag)
            yield from find_right_context(soup, line_tag)
            yield ''



def main(inp_fn, out_fn):
    with open(inp_fn, encoding='UTF-8') as inp_fh:
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


# functions in generator:


def mnsz_sample_or_webcorpus_sample(soup):
    subqueries = soup.find_all('subquery')
    for subquery in subqueries:
        if subquery is not None and subquery.string is not None:
            return True


def mnsz_heading(soup):
    hits = soup.find_all('hits')
    queries = soup.find_all('query')
    for hit in hits:
        if hit is not None and hit.string is not None:
            hits_str = hit.string.strip()
    for query in queries:
        if query is not None and query.string is not None:
            queries_str = query.string.strip()
        return f'# hit: {hits_str} \n# query: {queries_str}'


def webcorpus_header(soup, subquery, subuerys):
    if subquery is not None and subquery.string is not None:
        subquerys_str = subquery.string.strip()
        return f'# subquery: {subquerys_str}'


def find_ref_in_mnsz(soup, line_tag):
    if line_tag.ref is not None and line_tag.ref.string is not None:
        ref = line_tag.ref.string.strip()
        return f'# ref: {ref}'


def find_ref_in_webcorpus(soup, ref):
        ref_str = ref.get('refs')
        if ref_str is not None:
            return f'# ref: {ref_str}'


def find_left_context(soup, line_tag):
    if line_tag.left_context is not None and line_tag.left_context.string is not None:
        for tok in line_tag.left_context.string.strip().split():
            yield tok
    elif line_tag.left is not None and line_tag.left.string is not None:
        for tok in line_tag.left.string.strip().split():
            yield tok


def find_kwic_in_mnsz(soup, line_tag):
    if line_tag.kwic is not None and line_tag.kwic.string is not None:
        for tok in line_tag.kwic.string.strip().split():
            return tok


def find_right_context(soup, line_tag):
    if line_tag.right_context is not None and line_tag.right_context.string is not None:
        for tok in line_tag.right_context.string.strip().split():
            yield tok
    elif line_tag.right is not None and line_tag.right.string is not None:
        for tok in line_tag.right.string.strip().split():
            yield tok

# main


if __name__ == '__main__':
    main('akar_fni_500_webcorpus.xml', 'akar_fni_500_webcorpus.tsv')
