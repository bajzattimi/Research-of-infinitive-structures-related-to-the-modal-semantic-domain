# A mozaik n-gram és a mozaik szózsák előállítása

## A mozaik n-gram és a mozaik szózsák

A mozaik n-gram [Indig (2017)](http://real.mtak.hu/73335/) és a mozaik szózsák olyan  modellezése a nyelvi adatoknak,
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

## A mozaik n-gramok és a szózsákok előállítása
Az előfeldolgozott minták (tehát a POS-tagekből, lemmákból és tokenekből álló egységek) 
elemzéséhez (a mozaik n-gramok és a szózsákok elállításához)
a [`workflow.sh`](workflow.sh.sh) nevű program futtásához van szükség, 
A futtatáshoz szükségünk van a virtuális python környezet 
([venv](https://docs.python.org/3/library/venv.html)) 
létehozására, valamint a [`requirements.txt`](requirements.txt) fájlban lévő modulok telepítésére. 
A [`workflow.sh`](workflow.sh) indításakor a feldolgozásra szánt mintáinkat tartalmazó 
mappa nevét kell megadnunk.

```bash
$ ./workflow.sh pelda_korpusz 
```

### Paraméterek
A programban több paraméter-beállítást is el  kell végeznünk. Ezeket az alábbi leírás ismerteti: 

1. `CORP_NAME` a korpusz nevét adjuk meg, amelyből a mintáinkat kinyertük
2. `XML_EXTRA_OPTS=('-f' 'latin-2 '-t' 'UTF-8')` opcionális paraméter, az MNSZ2 korpuszból kinyert XML formátumú fájlok karakterkódolását módosítja `latin-2`-ről
 `UTF-8`-ra. Az MNSZ2-ből vételezett XML fájlok feldolgozozásához elengedhetetlen ez a paraméter. Ha mintáink forrása nem az MNSZ2, akkor üres tömb marad. 
3. `EMTSV_SERVER='http://emtsv.elte-dh.hu:5000'` az emtsv szervert hívja meg, az MNSZ2 és a Webkorpusz 2.0-ból vett minták újraelemzését végzi el.
4. `FILTER_PARAMS_YAML='filter_params.yaml'` ez a paraméter az általunk létrehozott [YAML](#A-YAML-fájl-módosítása.-A-POS-tagek-relációinak-módosítása)
5. `LEFT_WINDOW` az elemi mondat kinyeréséhez használt kontextusablak. A csomótól (kwic) határozhatjuk meg balra a kontextus méretét egész számokban. 
(pl. `LEFT_WINDOW=3` esetén a kwic-től három lexéma távolságban határozza meg az elemi mondat kiterjedését)
6. `RIGHT_WINDOW` az elemi mondat kinyeréséhez használt kontextusablak. A csomótól (kwic) határozhatjuk meg jobbra a kontextus méretét egész számokban. 
(pl. `RIGHT_WINDOW=3` esetén a kwic-től három lexéma távolságban határozza meg az elemi mondat kiterjedését)
7. `NPROC=40` A mozaik n-gramok létrehozására és számolására szolgáló rendezési lehetőség. Alapértelmezett értéke `40`.
8. `MEM_USE='40G'` A mozaik n-gramok létrehozására és számolására szolgáló rendezési lehetőség. Alapértelmezett értéke `40`.
9. `TMP_DIR='/data/aramis/tmp'` A mozaik n-gramok létrehozására és számolására szolgáló rendezési lehetőség egyik beállítása. 
 Alapértelmezett értéke `/data/aramis/tmp`.
10. `NPROC2=5` Rendezési lehetőség a megszámlált mozaik n-grammok rangsorolásához. Alapértelmezett értéke `5`.
11. `MEM_USE2='10G'` Rendezési lehetőség a megszámlált mozaik n-grammok rangsorolásához. Alapértelmezett értéke `10`.
12. `TMP_DIR2='/data/aramis/tmp'` Rendezési lehetőség a megszámlált mozaik n-grammok rangsorolásához. Alapértelmezett értéke `/data/aramis/tmp`.
13. `MOSAIC_FREQ_THRESHOLD=` Megjelenítési beállítás a mozaik n-gramok és a mozaik szózsákok kimenetéhez. Azt a minimum küszöbértéket adhatjuk meg, 
amely gyakorisági értékekben megjelenő absztrakciókat még látni szeretnénk a kimenetként kapott fájlban.

### Az XML formátum TSV formátummá alakítása

Az alábbi kódrész az XML bemeneti fájlok TSV formátumú fájlok átalakításért felel

1. `rm -rf` `"${CORP_NAME}_tsv"`
2. `mkdir -p` `"${CORP_NAME}_tsv"`

```bash
./venv/bin/python xml_to_emtsv.py -i "${CORP_NAME}_xml" -o "${CORP_NAME}_tsv" "${XML_EXTRA_OPTS[@]}"
```

### Újraelemzése a TSV fájloknak az emtsv elemzőlánccal  (opcionális)

```bash
rm -rf "${CORP_NAME}_emtsv"
mkdir -p "${CORP_NAME}_emtsv"
./venv/bin/python emtsv_client.py -s ${EMTSV_SERVER} -m morph pos -k form lemma xpostag \
    -i "${CORP_NAME}_tsv" -o "${CORP_NAME}_emtsv"
    
```

Az újraelemzés természetesen csak opcionális lépés, hiszen nem minden korpusz esetén működtethető az emtsv (történeti korpuszok).
Ha nem kívánjuk újraelemeztetni a mintáinkat, akkor az alábbi paraméterekre van szükségünk:

- `-i` : a feldolgozni kívánt (bemeneti) mappa vagy fájl neve
- `-o`: a várzt kimeneti mappa vagy fájl neve

### A YAML fájlban lévő szabályok alkalmazása

1. `--lower-sent-start` A mondat első karakterét kisbetűsíti.
2. `--keep-duplicates` A duplum mondatok megtartása azért, hogy az összes általa tartalmazott elemi mondat feldolgozásra
kerüljön.

```bash
rm -rf "${CORP_NAME}_emtsv_subs"
mkdir -p "${CORP_NAME}_emtsv_subs"
./venv/bin/python substitute_tags.py -f "${FILTER_PARAMS_YAML}" --lower-sent-start --keep-duplicates \
    -i "${CORP_NAME}_emtsv" -o "${CORP_NAME}_emtsv_subs"
    
```



### Az elemi mondatok létrehozása

Az alábbi kódrész hozza létre az elemi mondatokat, valamint a YAML fájlban megfogalmazott törlési szabályokat is végrehajtja. Ezt minden esetben az esettanulmányhoz kell igazítani. 

```bash
rm -rf "${CORP_NAME}_emtsv_clauses" "${CORP_NAME}_emtsv_clauses.tsv"
mkdir -p "${CORP_NAME}_emtsv_clauses"
time (for fname in "${CORP_NAME}_emtsv_subs/"*; do
          echo "REPORT: $fname" 1>&2
          ./venv/bin/python fin_inf_window.py -l"${LEFT_WINDOW}" -r"${RIGHT_WINDOW}" -f "${FILTER_PARAMS_YAML}" \
              -i "$fname" -o "${CORP_NAME}_emtsv_clauses/$(basename "$fname")"
      done 2> "${CORP_NAME}_emtsv_clauses.log")
## Merged into one file
### Must clean individual files from Sketch Engine query info and TSV header before processing
time (echo "REPORT: merged.tsv" 1>&2
      cat "${CORP_NAME}_emtsv_subs/"* | grep -Fv '# corpus: ' | grep -Fv '# hits: ' | grep -Fv '# query: ' | \
          awk '{ if (NR == 1 || $0 != "form\tlemma\txpostag") print $0}' | \
          ./venv/bin/python fin_inf_window.py -l"${LEFT_WINDOW}" -r"${RIGHT_WINDOW}" -f "${FILTER_PARAMS_YAML}" \
              -o "${CORP_NAME}_emtsv_clauses/merged.tsv" 2> "${CORP_NAME}_emtsv_clauses_merged.log")
## NOTE: There are alternative window creation methods
# ./venv/bin/python punct_window.py -i ${CORP_NAME}_emtsv_subs.tsv -o ${CORP_NAME}_emtsv_clauses.tsv \
#     -f "${FILTER_PARAMS_YAML}" 2> ${CORP_NAME}_emtsv_clauses_merged.log


```

### Az SPL formátum létrehozása a megmaradt mondatokhoz, tokenekhez és mezőkhöz

```bash
rm -rf "${CORP_NAME}_emtsv_clauses_spl"
mkdir -p "${CORP_NAME}_emtsv_clauses_spl"
time (for fname in "${CORP_NAME}_emtsv_clauses/"*; do
          grep "^# clause_SPL:" "$fname" | sed 's/^# clause_SPL: //' \
              > "${CORP_NAME}_emtsv_clauses_spl/$(basename "$fname")"
      done)

```

### A mozaik n-gramok létrehozása és a létrehozott mozaikok megszámlálása

```bash
rm -rf "${CORP_NAME}_mosaic_{2..9}"
THIS_SCRIPT_DIR=$( dirname -- "$( readlink -f -- "$0" )" )
for i in $(seq 9 -1 2); do
    echo "$i"
    mkdir -p "${CORP_NAME}_mosaic_${i}"
    time (for fname in "${CORP_NAME}_emtsv_clauses_spl/"*; do
              awk -v N="${i}" '{if (NF == N) print $0}' "$fname" | "${THIS_SCRIPT_DIR}/"mosaic.sh "${i}" | \
                  LC_ALL=C.UTF-8 sort --parallel="${NPROC}" -S "${MEM_USE}" -T "${TMP_DIR}" | uniq -c | \
                  LC_ALL=C.UTF-8 sort -nr -S"${MEM_USE2}" --parallel="${NPROC2}" -T "${TMP_DIR2}" | \
                  pigz > "${CORP_NAME}_mosaic_${i}/$(basename "$fname".gz)"
          done)
done

```

Az `-rf ${CORP_NAME}_mosaic_{2..9}`módosításával meg tudjuk változtatni a létrehozni kívánt mozaik n-gramjaink hosszát. 

### A mozaik n-gramok osztályainak létrehozása a gyakorisági értékek alapján

```bash
rm -rf "${CORP_NAME}_mosaic_"{2..9}"_filtered_${MOSAIC_FREQ_THRESHOLD}" \
    "${CORP_NAME}_mosaic_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip"
time (for i in $(seq 2 9); do
          echo "$i"
          mkdir -p "${CORP_NAME}_mosaic_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}"
          for fname in "${CORP_NAME}_emtsv_clauses/"*; do
              echo "$i $(basename "$fname")"
              ./venv/bin/python mosaic_filter.py -m "${CORP_NAME}_mosaic_${i}/$(basename "$fname".gz)" \
                  -f "${MOSAIC_FREQ_THRESHOLD}" -i "$fname" | \
              pigz > "${CORP_NAME}_mosaic_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}/$(basename "$fname".gz)"
          done
      done)
## Zip the results
zip -r "${CORP_NAME}_mosaic_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip" \
    "${CORP_NAME}_mosaic_"{2..9}"_filtered_${MOSAIC_FREQ_THRESHOLD}"

```

### A mozaik szózsákok létrehozása

```bash
rm -rf "${CORP_NAME}_bow_"{2..9}"_filtered_${MOSAIC_FREQ_THRESHOLD}" \
    "${CORP_NAME}_bow_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip"
time (for i in $(seq 2 9); do
          echo "$i"
          mkdir -p "${CORP_NAME}_bow_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}"
          for fname in "${CORP_NAME}_emtsv_clauses/"*; do
              echo "$i $(basename "$fname")"
              ./venv/bin/python mosaic_filter_bow.py -m "${CORP_NAME}_mosaic_${i}/$(basename "$fname".gz)" \
                   -f ${MOSAIC_FREQ_THRESHOLD} -i "$fname" | \
              pigz > "${CORP_NAME}_bow_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}/$(basename "$fname".gz)"
          done
      done)
## Zip the results
zip -r "${CORP_NAME}_bow_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip" \

```


## A `YAML` fájl módosítása. A POS-tagek relációinak módosítása

A POS-tag kombinációk redukálására szükségünk lehet a mozaik n-gramok előállításánál, hiszen így tudjuk befolyásolni azt, hogy az általunk végrehajtott műveletek a lehető
leghatékonyabban kínálják fel a konstrukció-jelölteket. Mintául tekintsük meg a [`workflow.sh`](workflow.sh) shell szkript által alkalmazott `YAML` formátumú fájlt: [`filter_params.yaml`](filter_params.yaml). Láthatjuk, hogy a POS-tagek módosítása hierarchikusan történik, valamint kétféle alapművelet áll rendelkezésünkre. Egyfelől törölhetünk címkéket általunk felállított szabályok szerint, valamint kicserélhetünk címkéket más címkékre. Ezzekkel tudjuk csökkenteni a nagy variabilitást, és a számunkra nem releváns szófaji annotációs együttállásokat nagyobb csoportokhoz rendelni. A törlésben (`delete`) rendelkezésünkre áll többféle metódus:
	
- `[example]`: ekkor maga a példány kerül törlésre. Ezzel lehetőségünk van a hibás, furcsa találatokat törölni a megadott POS-tag kombináció alapján
- `[lemma]`: ekkor az absztrakciós szintek közül csak a lemmát töröljük (az adott példány szóalakja és morfológiai címkéje részt vesz továbbra is a mozaikok létrehozásában)
- `[form]`: a tokent töröljük, a lemma és a morfológiai címke marad
- `[xpostag]`: a morfológiai címkét töröljük, a lemma és a szóalak marad

Fontos, hogy egy törlési szabály definiálásánál lehetőségünk van két típust is megadni a `[ ]` zárójelek között a `to_delete:` sorban. Például dönthetünk úgy, hogy egy típusnak csak a morfológiai címkéjét hagyjuk meg, ilyenkor a `[form, lemma]` kitöltést kell alkalmaznunk. 

A szabályok definiálásakor számít a sorrend. Ha valamit törlünk, akkor a következő lépésben arra már nem tudunk hivatkozni. A `value` sor kitöltésével tudjuk megadni azt az értéket, amelyet a kód figyelembe vesz a keresési művelet során. A `field_name` a `value` típusát rögzíti. A `cond` sorban két kitöltés között választhatunk (`any_tok` és `cur_tok`). Az `any_tok` bármely tokenre utal, a `cur_tok` az aktuális tokenre. A `not` sorban a `false` és a `true` értékek használatával tudjuk változtatni a művelet hatókörét. Ha `true` értékre változtatjuk, akkor a`value`-ban definiált értéken kívül minden talált adaton módosítást hajtunk végre, ha az alapértelmezett `false` marad a beállítás, akkor pedig a `value`-ban definiált értékkel azonosított adatokon történik módosítás. A  `name` mezőben tudjuk elnevezni a létrehozott szabályainkat azért, hogy az adatstruktúra a lehető legátláthatóbb maradjon.

 
## Források és hivatkozások
- Indig, Balázs 2017. Mosaic n-grams: Avoiding combinatorial explosion in corpus pattern mining for agglutinative languages. In: Vetulani, Zygmunt – Paroubek, Patrick – Kubis, Marek (eds.): Human Language Technologies as a Challenge for Computer Science and Linguistics. Adam Mickiewicz University. Poznan. [link](http://real.mtak.hu/73335/)
 - Indig Balázs – Sass Bálint – Simon Eszter –  Mittelholcz Iván –  Kundráth Péter –  Vadász Noémi 2019. emtsv – egy formátum mind felett. In: *XV. Magyar Számítógépes Nyelvészeti Konferencia.* Szegedi Tudományegyetem TTIK, Informatikai Intézet. Szeged.  235–247. [link](http://real.mtak.hu/99685/)
- Indig, Balázs – Bajzát, Tímea 2023. Bags and Mosaics: Semi-automatic Identification of Auxiliary Verbal Constructions for Agglutinative Languages. In: Vetulani, Zygmunt – Paroubek, Patrick – Kubis, Marek (eds.): Human Language Technologies as a Challenge for Computer Science and Linguistics  2023. Adam Mickiewicz University. Poznan.
- Magyar Nemzeti Szövegtár (v2.0.5); Oravecz Csaba – Váradi Tamás – Sass Bálint 2014. The Hungarian Gigaword Corpus. In: Calzolari, Nicoletta – Choukri, Khalid – Declerck, Thierry – Loftsson, Hrafn –Maegaard, Bente – Mariani, Joseph – Moreno, Asuncion – Odijk, Jan – Piperidis, Stelios (eds.): *Proceedings of the ninth international conference on language resources and evaluation (LREC-2014)*. Reykjavik: European Languages Resources Association (ELRA). 1719–1723. [link](http://real.mtak.hu/20143/)
- Magyar Webkorpus 2.0; Nemeskey Dávid Márk 2020. *Natural Language Processing methods for Language Modeling*. PhD thesis. Eötvös Loránd University. [link](https://hlt.bme.hu/media/pdf/nemeskey_thesis.pdf)
- Van linden, An. 2010. From premodal to modal meaning: Adjectival pathways in English. *Cognitive Linguistics 21 (3)*: 537–571. [link](https://www.researchgate.net/publication/249926985_From_premodal_to_modal_meaning_Adjectival_pathways_in_English)
