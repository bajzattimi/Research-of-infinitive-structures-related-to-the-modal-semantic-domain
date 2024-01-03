# A mozaik n-gram és a mozaik szózsák előállítása

## A mozaik n-gram és a mozaik szózsák

A mozaik n-gram (Indig 2017) és a mozaik szózsák olyan  modellezése a nyelvi adatoknak,
amely az egymással valamilyen szempontból funkcionálisan összetartozó mintázatok kinyerését
teszi lehetővé nagyméretű nyelvi korpuszból (Indig–Bajzát 2023).

A nyelvi adatokat értelmezhetjük n-gramokként, tehát olyan folyamatos szekvenciákként,
amelyekben n darab szó fordul elő. Az alábbi példákban ((**1a**)-(**1c**)) és (**2a**)-(**2c**), 
5-gramokra látunk példát.
Az (**1a**) és a (**2a**) szó 5-gramok, az (**1b**) és (**2b**) lemma 5-gramok, míg az (**1c**) 
és a (**2c**) POS-tagekből álló 5-gramok.

- (**1a**)  `a` `kertben` `nyílik`  `a` `tulipán`

- (**2b**)  `a` `kertben`  `alszik`  `a` `malac`

- (**1b**)  `a` `kert` `nyíl` `a` `tulipán`

- (**2b**)  `a` `kertben` `alszik` `a` `malac`

- (**1c**) `[\Det|Art.Def]` `[\N][Ine]` `[\V][Prs.NDef.3Sg]` `[\Det|Art.Def]` `[\N][Nom]`

- (**2c**) `[\Det|Art.Def]` `[\N][Ine]` `[\V][Prs.NDef.3Sg]` `[\Det|Art.Def]` `[\N][Nom]`

### A mozaik n-gramok

A mozaik n-gramok esetében a szekvencia elemei eltérő reprezentációs szinteken jeleníthetők meg 
(pl. POS-tag, lemma, szóalak) attól függően, hogy milyen nyelvtechnológiai apparátust alkalmazunk 
a feldolgozás során. A mozaik n-gramok megtartják a bemeneti példányok szórendi sémáit, a példányok
közötti hasonlóságokat és különbségeket a szekvencián belüli slotokat kitöltő elemek típusainak
eltérő szintű mértékű absztrahálása fedi fel. A fent bemutatott n-gram példák mozaikolása szemlélteti
egyszerűen a mozaik n-gramok koncepcióját. A (3a)-(3c) példák az (1) ésa (2) példányok közös
mozaikjaiból mutat be néhányat, ezzel szemléltetve, hogy a két különböző elemi mondat megfelelő
absztrakcióiban az egyező mintázati sémák kinyerhetők a bemutatott módszerrel

- (**3a**) `[\Det|Art.Def]` `lemma:kert` `[\V][Prs.NDef.3Sg]` `[\Det|Art.Def]` `[\N][Nom]`

- (**3b**) `a` `[/N][Ine]` `[\V][Prs.NDef.3Sg]` `[\Det|Art.Def]` `[\N][Nom]`

- (**3c**) `a` `kertben` `a` `[\Det|Art.Def]` `[\N][Nom]`

### A mozaik szózsákok

A mozaik szózsákok szintén előre meghatározott elemből álló adatreprezentácók. A szózsákban
az elemek sorrendje nem számít, tehát a konstrukciójelöltek szórendi vizsgálatára nem alkalmas, 
viszont képes az együttesen előforduló elemek csoportjait bemutatni a vizsgált nyelvi anyagban.
A fent bevezetett példányok ((**1**) és (**2**)) közös szózsákjai a következők lehetnek 
((**4a**)-(**4b**)):

- (**4a**) `[\Det|Art.Def]` `lemma:kert` `[\V][Prs.NDef.3Sg]` `[\Det|Art.Def]` `[\N][Nom]`

- (**4b**) `a` `kertben` `[\V][Prs.NDef.3Sg]` `a` `[\N][Nom]`

- (**4c**) `[\Det|Art.Def]` `[/N][Ine]` `[\Det|Art.Def]` `[\Det|Art.Def]` `[\N][Nom]`

Látható, hogy a módszerrel tudunk úgy csoportokat létrehozni, hogy a valamilyen szempontból
(jelen esetben az elemek típusai szerint) összetartozó példányok azonosíthatóvá válnak az
absztrakcióik mentén.

## Az előfeldolgozás lépései és az annotációs séma egységesítése

1. Ahhoz, hogy az emtsv képes legyen feldolgozni a korpuszokból kinyert adatainkat, TSV formátummá kell alakítanunk
   a [NoSketch Engine korpuszlekérdezőből](https://nlp.fi.muni.cz/trac/noske) kapott XML fájlokat. Ehhez ebben
   a repozitóriumban megtalálható [`xml_to_emtsv.py`](xml_to_emtsv.py) nevű programot fogjuk használni. Nyissuk meg
   a terminált, lépjünk be a klónozott könyvtárba.


2. A Python megnyitásához írjuk be, először, hogy `./venv/bin/python` utána írjuk be a program nevét:
   [`xml_to_emtsv.py`](xml_to_emtsv.py).
   Ezután adjuk meg a bemeneti és kimeneti adatokra vonatkozó paramétereket (lásd fent).  Az `-f` és a `-t`
   argumentumok abban az esetben szükségesek, amikor a karakterkódolás deklarációja az egyes XML dokumentumokban
   nem felel meg az adott fájl tényleges kódolásának (az MNSZ2-ből vett minta esetén). Ekkor Az `-f latin-2` és
   `-t UTF-8` paraméterekkel érhető el a kívánt kódolás.

```bash
$ ./venv/bin/python xml_to_emtsv.py -i mnsz2_xml -o mnsz2_tsv -f latin-2 -t UTF-8
$ ./venv/bin/python xml_to_emtsv.py -i webkorpusz_xml -o webkorpusz_tsv
```

3. A következőkben az emtsv-t fogjuk futtatni a TSV formátummá alakított mintáinkon. Az előzőekhez hasonlóan a parancssorban dolgozunk.

```bash
$ ./venv/bin/python xml_to_emtsv.py -i mnsz2_xml -o mnsz2_tsv -f latin-2 -t UTF-8
```

4. A Python megnyitásához írjuk be először, hogy `./venv/bin/python`, majd írjuk be a program nevét:
   [`emtsv_client.py`](emtsv_client.py). Ezután a feldolgozáshoz szükséges argumentumok a következők:
    - `-s`: Az ELTE DH e-magyar szerverének elérési útvonala (pl. `http://emtsv.elte-dh.hu:5000`)
    - `-m`: A használandó modulok nevei (a használható modulok listájához lásd
       a [dokumentációt](https://github.com/nytud/emtsv#modules)) vesszővel elválasztva (pl. `tok`, `morph`, `pos` )
    - `-k`: Azokat a mezőneveket adhatjuk meg, amelyeket a kimeneti fájlban meg kívánunk tartani
    (pl. `form`, `lemma`, `xpostag`)
    - `-i` és `-o`: A bemenet és kimenet meghatározására (lásd fent)
    - `-r` (opcionális): Megadja, hogy a parancs hányszor próbálkozzon újra az emtsv lekérdezéssel sikertelenség esetén

```bash
$ ./venv/bin/python emtsv_client.py -s http://emtsv.elte-dh.hu:5000 -m morph pos conv-morph dep -k form lemma xpostag upostag
feats deprel id head -i mnsz_tsv -o mnsz_dep
```

## A mozaik n-gramok és a szózsákok előállítása
A minták feldolgozásához (a mozaik n-gramok és a szózsákok elállításához) a [`run_script.sh`](run_script.sh) nevű shell szkriptet futtatjuk. A futtatáshoz szükségünk van a virtuális python környezet ([venv](https://docs.python.org/3/library/venv.html)) létehozására, valamint a [`requirements.txt`](requirements.txt) fájlban lévő modulok telepítésére. A [`run_script.sh`](run_script.sh) indításakor a feldolgozásra szánt mintáinkat tartalmazó mappa nevét kell megadnunk.

```bash
$ ./run_script.sh pelda_korpusz 
```

A szkriptben több paraméter-beállítás is megváltoztatható a vizsgálatunk céljaival összehangolva. Ezeket az alábbi leírás ismerteti: 

1. Megváltoztathatjuk az elemi mondatok szűrését biztosító kontextusablakok méretét:
- `-l` alapértelmezetten a balkontextus mérete 3 token a nódusztól, ez módosítható. 0-nál nagyobb egész számokat adhatunk meg.
- `-r` alapértelmezetten a jobbkontextus mérete 3 token a nódusztól ez módosítható. 0-nál nagyobb egész számokat adhatunk meg.
- `-f` a `YAML` kiterjesztésű fájlt hívja meg ezen paraméter. A repozitóriumban található és a kód által alapértelmezettként használt `filter_params.yaml` a bevezetőben ismertetett vizsgálat célkitűzéseihez igazodik, ezért javasolt az általa tartalmazott relációk és műveletek felülvizsgálata.

2. A mozaikok létrehozásakor lehetőségünk van azok hosszának megváltoztatására. Alapértelmezetten a kód bi-; tri-; 4-; 5-; 6-; 7-; 8- és 9-gramokat hoz létre, tehát a legalább kettő és a maximum kilenc hosszúságú elemi mondatok és azok annotációjának feldolgozását végzi el. A szkriptben látható `9` és `2` szám átírásával változtathatjuk a hosszúságokat. A `-1` érték a lépésközt jelöli, ez a lépésköz a jelen esetben azt jelenti, hogy a kód a 9 és a 2 hosszúság között minden hosszúságú példányt kezel. 

```bash
rm -rf mosaic_${CORP_NAME}_filtered_{2..9}
mkdir mosaic_${CORP_NAME}_filtered_{2..9}
for i in $(seq 9 -1 2); do
    echo "$i"
    time (for fname in ${CORP_NAME}_filtered_spl/*; do awk "{if (NF == ${i}) print \$0}" "$fname" | ./mosaic.sh "${i}" | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 -T /data/tmp | pigz > "mosaic_${CORP_NAME}_filtered_${i}/$(basename "$fname".gz)"; done)
done
``` 

3. Lehetőségünk van módosítani a küszöbértéken. A kód alapértelmezetten a 25-nél kevesebbszer előforduló mintákat elveti. Az alábbi kódrészletben megváltoztathatjuk a küszöbértéket.

```bash
rm -rf mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25
mkdir mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25
time (for i in $(seq 2 9); do for fname in out_part_filtered/${CORP_NAME}_pos/*; do echo "$i $(basename "$fname")"; ./venv/bin/python mosaic_filter.py -m "mosaic_${CORP_NAME}_filtered_${i}/$(basename "$fname".gz)" -f 25 < "$fname" | pigz > "mosaic_${CORP_NAME}_filtered_${i}_filtered_25/$(basename "$fname".gz)"; done; done)
```
A kódrészletben lévő `25 < "$fname"` kifejezés értékét változtassuk meg. Olyan egész számot válasszunk, amely nagyobb vagy egyenlő, mint nulla.

4. A mozaik n-gramok küszöbértékéhez hasonlóan, a BoW-ok, vagyis a szózsákok gyakorisági küszöbértékét is módosíthatjuk a következő kódrészletben:

```bash
rm -rf mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25_bow
mkdir mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25_bow
time (for i in $(seq 2 9); do for fname in out_part_filtered/${CORP_NAME}_pos/*; do echo "$i $(basename "$fname")"; ./venv/bin/python mosaic_filter_bow.py -m "mosaic_${CORP_NAME}_filtered_${i}/$(basename "$fname".gz)" -f 25 < "$fname" | pigz > "mosaic_${CORP_NAME}_filtered_${i}_filtered_25_bow/$(basename "$fname".gz)"; done; done)
```
A kódrészletben lévő `25 < "$fname"` kifejezés értékét változtassuk meg. Olyan egész számot válasszunk, amely nagyobb vagy egyenlő, mint nulla.

## A `YAML` fájl módosítása. A POS-tagek relációinak módosítása

A POS-tag kombinációk redukálására szükségünk lehet a mozaik n-gramok előállításánál, hiszen így tudjuk befolyásolni azt, hogy az általunk végrehajtott műveletek a lehető
leghatékonyabban kínálják fel a konstrukció-jelölteket. Mintául tekintsük meg a [`run_script.sh`](run_script.sh) shell szkript által alkalmazott `YAML` formátumú fájlt: [`filter_params.yaml`](filter_params.yaml). Láthatjuk, hogy a POS-tagek módosítása hierarchikusan történik, valamint kétféle alapművelet áll rendelkezésünkre. Egyfelől törölhetünk címkéket általunk felállított szabályok szerint, valamint kicserélhetünk címkéket más címkékre. Ezzekkel tudjuk csökkenteni a nagy variabilitást, és a számunkra nem releváns szófaji annotációs együttállásokat nagyobb csoportokhoz rendelni. A törlésben (`delete`) rendelkezésünkre áll többféle metódus:
	
- `[example]`: ekkor maga a példány kerül törlésre. Ezzel lehetőségünk van a hibás, furcsa találatokat törölni a megadott POS-tag kombináció alapján
- `[lemma]`: ekkor az absztrakciós szintek közül csak a lemmát töröljük (az adott példány szóalakja és morfológiai címkéje részt vesz továbbra is a mozaikok létrehozásában)
- `[form]`: a tokent töröljük, a lemma és a morfológiai címke marad
- `[xpostag]`: a morfológiai címkét töröljük, a lemma és a szóalak marad

Fontos, hogy egy törlési szabály definiálásánál lehetőségünk van két típust is megadni a `[ ]` zárójelek között a `to_delete:` sorban. Például dönthetünk úgy, hogy egy típusnak csak a morfológiai címkéjét hagyjuk meg, ilyenkor a `[form, lemma]` kitöltést kell alkalmaznunk. 

A szabályok definiálásakor számít a sorrend. Ha valamit törlünk, akkor a következő lépésben arra már nem tudunk hivatkozni. A `value` sor kitöltésével tudjuk megadni azt az értéket, amelyet a kód figyelembe vesz a keresési művelet során. A `field_name` a `value` típusát rögzíti. A `cond` sorban két kitöltés között választhatunk (`any_tok` és `cur_tok`). Az `any_tok` bármely tokenre utal, a `cur_tok` az aktuális tokenre. A `not` sorban a `false` és a `true` értékek használatával tudjuk változtatni a művelet hatókörét. Ha `true` értékre változtatjuk, akkor a`value`-ban definiált értéken kívül minden talált adaton módosítást hajtunk végre, ha az alapértelmezett `false` marad a beállítás, akkor pedig a `value`-ban definiált értékkel azonosított adatokon történik módosítás. A  `name` mezőben tudjuk elnevezni a létrehozott szabályainkat azért, hogy az adatstruktúra a lehető legátláthatóbb maradjon.

### Mit rejtenek a mozaikok és a szózsákok?

Lehetőségünk van a mozaikok és a szózsákok alapján lekérdezni a példányokat. Ehhez a feladathoz a `mosaic_lookup.py` és a `mosaic_lookup_bow.py` szkripteket használjuk. A Python megnyitásához írjuk be először, hogy `./venv/bin/python` utána írjuk be azt a szkriptet, amelyet használni szeretnénk:

- `mosaic_lookup.py`: a mozaik n-gramok nyelvi adatainak visszakereséséhez tudjuk használni
- `mosaic_lookup_bow.py`: a szózsákok nyelvi adatainak visszakereséséhez tudjuk használni

A közös argumentumokon kívül az alábbi argumentumot szükséges megadnunk: 

- `-m`: ennek a típusa sztring, azt a mozaik n-gramot vagy szózsákot kell beírnunk, amelynek nyelvi adatait szeretnénk lekérdezni
 
## Források és hivatkozások
- Indig, Balázs 2017. Mosaic n-grams: Avoiding combinatorial explosion in corpus pattern mining for agglutinative languages. In: Vetulani, Zygmunt – Paroubek, Patrick – Kubis, Marek (eds.): Human Language Technologies as a Challenge for Computer Science and Linguistics. Adam Mickiewicz University. Poznan. [link](http://real.mtak.hu/73335/)
 - Indig Balázs – Sass Bálint – Simon Eszter –  Mittelholcz Iván –  Kundráth Péter –  Vadász Noémi 2019. emtsv – egy formátum mind felett. In: *XV. Magyar Számítógépes Nyelvészeti Konferencia.* Szegedi Tudományegyetem TTIK, Informatikai Intézet. Szeged.  235–247. [link](http://real.mtak.hu/99685/)
- Indig, Balázs – Bajzát, Tímea 2023. Bags and Mosaics: Semi-automatic Identification of Auxiliary Verbal Constructions for Agglutinative Languages. In: Vetulani, Zygmunt – Paroubek, Patrick – Kubis, Marek (eds.): Human Language Technologies as a Challenge for Computer Science and Linguistics  2023. Adam Mickiewicz University. Poznan.
- Magyar Nemzeti Szövegtár (v2.0.5); Oravecz Csaba – Váradi Tamás – Sass Bálint 2014. The Hungarian Gigaword Corpus. In: Calzolari, Nicoletta – Choukri, Khalid – Declerck, Thierry – Loftsson, Hrafn –Maegaard, Bente – Mariani, Joseph – Moreno, Asuncion – Odijk, Jan – Piperidis, Stelios (eds.): *Proceedings of the ninth international conference on language resources and evaluation (LREC-2014)*. Reykjavik: European Languages Resources Association (ELRA). 1719–1723. [link](http://real.mtak.hu/20143/)
- Magyar Webkorpus 2.0; Nemeskey Dávid Márk 2020. *Natural Language Processing methods for Language Modeling*. PhD thesis. Eötvös Loránd University. [link](https://hlt.bme.hu/media/pdf/nemeskey_thesis.pdf)
- Van linden, An. 2010. From premodal to modal meaning: Adjectival pathways in English. *Cognitive Linguistics 21 (3)*: 537–571. [link](https://www.researchgate.net/publication/249926985_From_premodal_to_modal_meaning_Adjectival_pathways_in_English)
