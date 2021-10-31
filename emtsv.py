import requests


def parse_response(resp):
    # Ez a függvény feldolgozza a választ az resp.text-ben van a szöveg, mintha read()-el beolvasnál egy fájlt
    with open('tud_fni_500_webcorpus.txt', 'w', encoding='UTF-8') as fh:
        # Gyakorlatilag beleprinteljük a fájlba egyben (a print parancs file paraméterével megmondhatjuk,
        # hogy a képernyőre vagy fájlba printeljen)
        print(resp.text, file=fh)

    # Vagy feldolgozhatjuk, ilyenkor jobb a resp.iter_lines() ami a fájlon soronként iterálásnak felel meg
    # annyi a különbség, hogy nem szövegként olvassa be ezért a line-okat decode('UTF-8')-al át kell alakítani

    # Az oszlopneveket definiáljuk későbbre
    field_names = ('form', 'anas', 'lemma', 'xpostag', 'upostag', 'feats', 'id', 'deprel', 'head')

    # Csinálunk egy kezdeti üres listát a mondatnak
    sent = []

    # Az enumerate azt csinálja, hogy minden elemnek ad egy sorszámot 0-tól kezdve
    # így az i, line "tuple-ön" iterálunk
    for i, line in enumerate(resp.iter_lines()):
        line = line.decode('UTF-8').strip()  # A sorvéget leszedjük ugyebár, ahogy a fájloknál

        # Innen jön egy véges automata szerű több állapotú feldolgozás
        # (az állapotok exkluzívak, csak egy fut le egy ciklus lépésben)

        # 1. állapot: üres sor (mondatközi szünet)
        if len(line) == 0:
            # Kiírjuk az összegyűtjött mondatot és csinálunk egy új listát a következő mondatnak
            yield sent
            sent = []

        # 2. állapot: header
        elif i == 0:
            # A header nem érdekes, ezért eldobjuk azaz a for ciklus következő körébe lépünk a continue-val
            continue

        # 3. állapot: komment, metaadat
        elif line.startswith('# '):
            # Ez most nem kell, ezért ugorhatunk a következő input sorra (ezt csinálja a continue)
            continue

        # 4. állapot: A tokent tartalmazó sorok
        else:
            # Ha nem ilyennel van dolgunk, akkor hiba nélkül felvágható a sor mezőkre a tab karakter mentén:
            # form, anas, lemma, xpostag, upostag, feats, token_id, deprel, head = line.split('\t')
            # De mi át akarjuk alakítani őket egy dict-be a következőképpen:
            token = {}  # Ez egy dict
            # A mezők sorrendje adott, így a mezőneveket és az értékeket össze zip-eljük,
            # mint a zipzár két oldalát így a név-érték párok lesznek, ami a kulcs-érték párja lesz a dict-nek.
            for k, v in zip(field_names, line.split('\t')):
                token[k] = v

            # A kész token-t hozzáadjuk a mondat szavait tartalmazó listához így gyűjtjük őket
            sent.append(token)

    # Ha az utolsó mondat után nincs üres sor,
    # akkor benne marad az utolsó mondat a sent változóban és ki kell írni
    if len(sent) > 0:
        yield sent


r = requests.post('http://emtsv.elte-dh.hu:5000/morph/pos/conv-morph/dep',
                  files={'file': open('tud_fni_500_webcorpus.tsv', encoding='UTF-8')},
                  data={'conll_comments': True})   # EZ a fontos sor!


# Fontos tulajdonsága a yield-es generátoroknak, hogy ha csak értékül adod őket, akkor nem csinálnak semmit,
# mert várják, hogy végigiteráljanak rajtuk. A listává castolással list(parse_response(r)) lehet elérni,
# hogy lista legyen belőlük. Ez általában nem szükséges.
for sentence in parse_response(r):
    print(sentence)