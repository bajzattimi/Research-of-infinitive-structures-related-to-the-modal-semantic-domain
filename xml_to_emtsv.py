from os import cpu_count
from pathlib import Path
from itertools import chain
from multiprocessing import Pool
from argparse import ArgumentParser, ArgumentTypeError #python beépített könyvtárak

from bs4 import BeautifulSoup #BeautifulSoup könyvtár elérése: File -> Settings -> Build, Execution, Deployment ->/
# Project Interpreter -> + -> BeautifulSoup -> Install package


def gen_sents(soup): #generátor, ez hívja meg a függvényeket
    get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = identify_sample_type(soup) #ez a sor/
    # dönti el, hogy melyik korpuszból történt a mintavétel, és az adott korpuszhoz megfelelően nevezi el a változókat

    yield 'form\n' #sortörések beillesztése
    yield from get_heading(soup) #heading beillesztése
    for line_tag in soup.find_all('line'): #ciklus, ami végigiterál a sorokon

        left_toks, kwic_toks, right_toks = context(line_tag, left_cont_name, kwic_name, right_cont_name) #a kontextust/
        # kiszedő függvény meghívása
        if len(left_toks) > 0 and left_toks[0] == '<s>': #ha az első token <s>, akkkor a 2. tokentől printel
            left_toks = left_toks[1:]
        if len(right_toks) > 0 and right_toks[-1] == '</s>': #ha az utolsó token <s>, akkor az utolsó előtti tokenig/
            # printel
            right_toks = right_toks[:-1]

        yield f'# ref: {find_ref_in_corp(line_tag)}\n' #az adat azonosítóját (ref) gyűjti össze
        yield f'# left_length: {len(left_toks)}\n' #a bal kontextus méretét összesíti
        yield f'# kwic_length: {len(kwic_toks)}\n' #a kwic méretét összesíti
        yield f'# right_length: {len(right_toks)}\n' #a jobb kontextus méretét összesíti
        yield f'# sent: {" ".join(chain(left_toks, kwic_toks, right_toks))}\n' #összefűzi a tokeneket
        yield '\n'.join(chain(left_toks, kwic_toks, right_toks)) #mondatok összefűzése(??)
        yield '\n\n' #egy sor kihagyása a mondatok végén


def identify_sample_type(soup): #a minta típusát(melyik korpuszból történt a mintavétel) eldöntő függvény
    if len(soup.find_all('subquery')) > 0:  # Webcorpus típus, mert csak itt van 'subquery' tag
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            webcorpus_heading, find_ref_in_webcorpus, 'left', 'kwic', 'right' #egységesen nevet rendel a tag-ekhez
    elif soup.find('hits') is not None:  # MNSZ type sample
        get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name = \
            mnsz_heading, find_ref_in_mnsz, 'left_context', 'kwic', 'right_context' #egységesen nevet rendel a tag-ekhez
    else:
        raise ValueError('We could not decide which sample it was') #hibaüzenet,/
        # ha nem tudja eldönteni a bemeneti fájlról, hogy melyik minta

    return get_heading, find_ref_in_corp, left_cont_name, kwic_name, right_cont_name #visszaadja a tag-ek elnevezését,/
    # ezek már "függetlenek" a bementi minta típusától


def webcorpus_heading(soup): #webcorpusz heading kiszedő függvény
    heading_tag = get_child(soup, 'header', recursive=True) #a heading tag gyerekelemének kiszedője
    yield f'# corpus: { get_tag_text(get_child(heading_tag, "corpus"))}\n' #korpusz
    yield f'# subcorpus: { get_tag_text(get_child(heading_tag, "subcorpus"), can_be_empty=True)}\n'  # Subcorpus empty!
    for subquery_tag in heading_tag.find_all('subquery'): #subquery tag-eken iterál végig
        yield f'# subquery:\n' #sortörés
        yield f'#     operation: {get_attr_from_tag(subquery_tag, "operation")}\n' #operation
        yield f'#     size: {get_attr_from_tag(subquery_tag, "size")}\n' #size
        yield f'#     value: {get_tag_text(subquery_tag)}\n' #value


def mnsz_heading(soup): #mnsz típusú minta heading kiszedő függvénye
    heading_tag = get_child(soup, 'heading', recursive=True) #heading tag gyerekelemeinek kiszedése
    for name in ('corpus', 'hits', 'query'): #végigiterál a corpus, a hits és a query tag-eken
        yield f'# {name}: {get_tag_text(get_child(heading_tag, name))}\n' #külön sorba printeli ezeket 


def find_ref_in_webcorpus(line_tag): #webcorpus azonosítókat kiszedő függvény
    return get_attr_from_tag(line_tag, 'refs') #visszaadja a ref attribútum értékét


def find_ref_in_mnsz(line_tag): #mnsz típusú azonosítót kiszedő függvény
    return get_tag_text(get_child(line_tag, 'ref')) #text 'ref' gyerekelemének visszaadása


def context(line_tag, left_str, kwic_str, right_str): #kontextust kiszedő függvény
    left = get_tag_text(get_child(line_tag, left_str), can_be_empty=True).split(' ')    # Left context can be empty!
    kwic = get_tag_text(get_child(line_tag, kwic_str)).split(' ')                       # Kwic can not be empty!
    right = get_tag_text(get_child(line_tag, right_str), can_be_empty=True).split(' ')  # Right context can be empty!
    return left, kwic, right


def get_attr_from_tag(tag, attr_name): #a tag egy meghatározott attribútumának értékét kiszedő függvény/
    # (ezt használja a find_ref_in_webcorpus függvény
    value_str = tag.get(attr_name) #attr_name a keresett attribútum neve
    if value_str is None: #ha ez üres
        raise ValueError(f'{attr_name} can not be found in {tag.name}!') #nem található ez az attribútum/
        # a megadott tag-en belül
    return value_str #attribútum érték visszaadása


def get_child(soup, curr_context_str, recursive=False): #gyerekelemet kiszedő függvény/
    # (ezt használja a context és a find_ref_in_mnsz függvény
    curr_context_tag = soup.find(curr_context_str, recursive=recursive) #az aktuális kontextus tag megkeresése
    if curr_context_tag is None:
        raise ValueError(f'{curr_context_str} can not be found in {soup.name} with recusive {recursive}') #ha ez nem/
        # található, akkor hibaüzenetet küld
    return curr_context_tag


def get_tag_text(curr_context_tag, can_be_empty=False): #tag kiszedő függvény a get_child függvény használja
    curr_context_string = curr_context_tag.string
    if curr_context_string is not None:
        return curr_context_string.strip()
    elif not can_be_empty:
        raise ValueError(f'{curr_context_tag.name} has no string content!') #ha nem találja a tag-et, akkor/
        # hibaüzenetet küld
    return ''


def process_one_file(input_file, output_file): #a bemenetet és a kimenetet meghatározó függvény/
    # (input_file, karakterkódolás)/
    # soup hívása
    with open(input_file, 'rb') as inp_fh:
        soup = BeautifulSoup(inp_fh, 'lxml-xml') #bemenet

    with open(output_file, 'w', encoding='UTF-8') as out_fh: #kimenet output_file, karakterkódolás,/
        # generátor gen_sents szerinti printelés a kimenetbe
        out_fh.writelines(gen_sents(soup))


def existing_dir_path(string):  #(már létező) mapppa elérési útvonalának megtalálása
    if not Path(string).is_dir():
        raise ArgumentTypeError(f'{string} is not an existing directory!')
    return string #stringként adja vissza az elérési útvonalat


def new_dir_path(string): #új kimeneti mappa létrehozása, egy stringet vár paraméterként
    dir_name = Path(string)
    dir_name.mkdir(parents=True, exist_ok=True)  # Create dir
    if next(Path(dir_name).iterdir(), None) is not None:
        raise ArgumentTypeError(f'{string} is not an empty directory!') #szól, ha ez a mappa nem üres
    return string


def int_greater_than_1(string): #Ha a bemeneti string nem alakítható át int-té, akkor továbblép és -1 értéket ad. /
    # Ha a val kevesebb vagy egyenlő, mint 1, akkor ArgumentTypeErrort ad, ha skerül, akkor értéket ad neki./
    # Hibakezelésre használjuk.
    try:
        val = int(string)
    except ValueError:
        val = -1  # Bad value

    if val <= 1:
        raise ArgumentTypeError(f'{string} is not an int > 1!')

    return val


def parse_args(): #kimeneti fájlok elérése?
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


def main(): #a main függvény definiálása
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
