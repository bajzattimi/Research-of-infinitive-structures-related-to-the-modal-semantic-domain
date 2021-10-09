from bs4 import BeautifulSoup
import lxml
import requests

def gen_sents(soup):
    lines = soup.find_all("line")
    for line_tag in lines:
        ref = line_tag.ref.string.strip()
        yield f'# ref: {ref}'
        for tok in line_tag.left_context.string.strip().split():
            yield tok
        for tok in line_tag.kwic.string.strip().split():
            yield tok
        for tok in line_tag.right_context.string.strip().split():
            yield tok

with open("akar_fni_384.xml", "r", encoding="utf8") as fh:
    soup = BeautifulSoup(fh, "lxml")

    corpus = soup.find("corpus")
    if corpus is not None:
        corpus_str = corpus.string.strip()

    hits = soup.find("hits")
    if hits is not None:
        hits_str = hits.string.strip()

    query = soup.find("query")
    if query is not None:
        query_str = query.string.strip()

    print('form')
    print(f'# corpus: {corpus_str}')
    print(f'# hits: {hits_str}')
    print(f'# query: {query_str}')

    a_generator = gen_sents(soup)
    for i in a_generator:
        print(i)





