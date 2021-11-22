from bs4 import BeautifulSoup


def gen_sents(soup):
    hits = soup.find_all('hits')
    for hit in hits:
        if hit is not None and hit.string is not None:
            hits_str = hit.string.strip()
        yield f'# hit: {hits_str}'
    subquerys = soup.find_all('subquery')
    for subquery in subquerys:
        if subquery is not None and subquery.string is not None:
            subquerys_str = subquery.string.strip()
        yield f'# subquery: {subquerys_str}'
    lines = soup.find_all('line')
    for ref in lines:
        if ref is not None:
            ref_str = ref.get('refs')
            if ref_str is not None:
                yield f'# ref: {ref_str}'
        line_tag = ref
        if line_tag.ref is not None and line_tag.ref.string is not None:
            ref = line_tag.ref.string.strip()
            yield f'# ref: {ref}'
        if line_tag.left is not None and line_tag.left.string is not None:
            for tok in line_tag.left.string.strip().split():
                yield tok
        if line_tag.left_context is not None and line_tag.left_context.string is not None:
            for tok in line_tag.left_context.string.strip().split():
                yield tok
        if line_tag.kwic is not None and line_tag.kwic.string is not None:
            for tok in line_tag.kwic.string.strip().split():
                yield tok
        if line_tag.right is not None and line_tag.right.string is not None:
            for tok in line_tag.right.string.strip().split():
                yield tok
        if line_tag.right_context is not None and line_tag.right_context.string is not None:
            for tok in line_tag.right_context.string.strip().split():
                yield tok
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
        #print(f'# hits: {hits_str}', file=out_fh)
        #print(f'# query: {queries_str}', file=out_fh)


        for out_line in gen_sents(soup):
            if out_line not in {'<s>', '</s>'}:
                print(out_line, file=out_fh)


if __name__ == '__main__':
    main('kepes_fni_384.xml', 'akar_fni_500_webcorpus.tsv')
