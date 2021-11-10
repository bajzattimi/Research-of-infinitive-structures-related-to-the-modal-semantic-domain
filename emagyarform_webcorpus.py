from bs4 import BeautifulSoup


def gen_sents(soup):
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
        if line_tag.left is not None and line_tag.left.string is not None:
            for tok in line_tag.left.string.strip().split():
                yield tok
        if line_tag.kwic is not None and line_tag.kwic.string is not None:
            for tok in line_tag.kwic.string.strip().split():
                yield tok
        if line_tag.right is not None and line_tag.right.string is not None:
            for tok in line_tag.right.string.strip().split():
                yield tok
        yield ''


def main(inp_fn, out_fn):
    with open(inp_fn, encoding='UTF-8') as inp_fh:
        soup = BeautifulSoup(inp_fh, 'lxml')

        corpus = soup.find('corpus')
        if corpus is not None:
            corpus_str = corpus.string.strip()

        #subquerys = soup.find('subquery')#
        #if subquerys is not None:#
            #subquerys_str = hits.string.strip()#

    with open(out_fn, 'w', encoding='UTF-8') as out_fh:
        print('form', file=out_fh)
        print(f'# corpus: {corpus_str}', file=out_fh)
        #print(f'# hits: {hits_str}', file=out_fh)#
        #print(f'# subquery: {subquerys}', file=out_fh)

        for out_line in gen_sents(soup):
            if out_line not in {'<s>', '</s>'}:
                print(out_line, file=out_fh)


if __name__ == '__main__':
    main('akar_fni_500_webcorpus.xml', 'akar_fni_500_webcorpus.tsv')