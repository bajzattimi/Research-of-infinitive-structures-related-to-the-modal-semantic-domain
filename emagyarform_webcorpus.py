from bs4 import BeautifulSoup

def gen_sents(soup):
    subquerys = soup.find_all('subquery')
    for subquery in subquerys:
        if subquery is not None and subquery.string is not None:
            subquerys_str = subquery.string.strip()
            yield f'# subquery: {subquerys_str}'
    lines = soup.find_all("line")
    for line_tag in lines:
        if line_tag.ref is not None and line_tag.ref.string is not None:
            ref = line_tag.ref.string.strip()
            yield f'# ref: {ref}'
    for line_tag in lines:
        if line_tag.left is not None and line_tag.left.string is not None:
            for tok in line_tag.left.string.strip().split():
                yield tok
        if line_tag.kwic is not None and line_tag.kwic.string is not None:
            for tok in line_tag.kwic.string.strip().split():
                yield tok
        if line_tag.right is not None and line_tag.right.string is not None:
            for tok in line_tag.right.string.strip().split():
                yield tok



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
            print(out_line, file=out_fh)


if __name__ == '__main__':
    main('akar_fni_500_webcorpus.xml', 'akar_fni_500_webcorpus.tsv')
