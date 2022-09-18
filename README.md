# A (pre)modális szemantikai térrel összekapcsolódó főnévi igeneves szerkezetek vizsgálata

A jelen kutatás a segédige + főnévi igeneves szerkezetek megvalósulási környezeteit hivatott elemezni korpuszalapon,
 számítógépes vizsgálati eljárásokkal. Az adatokból látható mintázat-együttállásokból elméleti hipotézisek
 felállításával kapcsolódik ahhoz a kutatási kérdéshez, hogy a vizsgált premodális ([lehetségességi relációt](https://www.researchgate.net/publication/249926985_From_premodal_to_modal_meaning_Adjectival_pathways_in_English)
 nem explikáló) jelentéssel asszociálódó főnévi igeneves kompozitumszerkezetek milyen nyelvi, konstrukcionális
 kidolgozottságban képesek átlépni a jelentésképzés során a modális szemantikai térbe. A mintavételezés
 a [Magyar Nemzeti Szövegtár 2.0.5-ből (MNSZ2)](http://clara.nytud.hu/mnsz2-dev/)
 ([Oravecz–Váradi–Sass 2014](https://aclanthology.org/L14-1536/))
 és a [Magyar Webkorpusz 2.0-ból](https://hlt.bme.hu/hu/resources/webcorpus2)
 ([Nemeskey 2020](https://hlt.bme.hu/hu/publ/nemeskey_2020)) valósult meg két lépcsőben.
 Az első mintavétel során egy [reprezentatív](https://www.researchgate.net/figure/Krejcie-and-Morgan1970-Sampling-Ratio-Research-Instrument-According-to-Taylor-and_fig3_341908971) 
 (a korpusz méretéhez viszonyítva kis) elemszámú csoportot vételeztem,
 a másodiknál pedig törekedtem a keresési kondíciók által kiadott összes elem mentésére (a rendszer képességeinek
 határáig). A korpuszok által felkínált részletes keresési metódusok nagyon vonzónak tűntek, azonban a legprecízebb
 mintavételezéshez a [CQL kifejezésekkel](https://www.sketchengine.eu/documentation/corpus-querying/) történő szűrést
 választottam.

## Minták a korpuszokból

### Minta az MNSZ2-ből (v2.0.5)
| Segédige / predikatív melléknév + főnévi igenév | A Reprezentatív<br/> minta elemszáma (db) | A teljességre törekvő<br/> minta elemszáma (db) | Összes találat a korpuszban |
|-------------------------------|-------|---------|----------|
| ***tud*** + inf.              | 500   | 675000  | 131529   |
| ***akar*** + inf.             | 384   | 610836  | 610836   |
| ***szeret*** + inf.           | 384   | 484448  | 484448   |
| ***kíván*** + inf.            | 384   | 192678  | 192678   |
| ***képes*** + inf.            | 384   | 134843  | 134843   |
| ***-kOzik/-kOdik*** + inf.    | 384   | 255799  | 255799   |
| ***mer*** + inf.              | 382   | 63729   | 63729    |
| ***képtelen*** + inf.         | 381   | 48036   | 48036    |
| ***hajlandó*** + inf.         | 381   | 48267   | 48267    |
| ***bír*** + inf.              | 379   | 22191   | 22191    |
| ***remél*** + inf.            | 364   | 6506    | 6506     |
| ***óhajt*** + inf.            | 361   | 5500    | 5500     |
| ***hajlamos*** + inf.         | 357   | 4212    | 4212     |
| ***vágyik*** + inf.           | 313   | 1658    | 1658     |
 | ***utál*** + inf.             | 306   | 1448    | 1448     |
 | ***gyűlöl*** + inf.           | 132   | 132     | 132      |


[Az **MNSZ2** keresőfelületén](http://clara.nytud.hu/mnsz2-dev/) az alábbi CQL-eket kellett tehát megadni:

 **(1a)** `(meet [lemma="akar" & msd="(IK\.)*IGE\.(_HAT\.)?[TI]?[MPF]?[et]?[123]?"] 
 [msd="(IK\.)*IGE\.INF[123]?\*?"] -2 2)`

 **(1b)** `(meet [lemma="képes" & msd="MN.PL*.NOM"] [msd="(IK\.)*IGE\.INF[123]?\*?"] -2 2)`

 Ezek a CQL-ek (1a)--(1b) tették lehetővé a keresést a korpuszban. A segédige + főnévi igenév szerkezetre az (1a) 
 kifejezést, a predikatív melléknév + főnévi igenév konstrukció szűrésére az (1b) CQL-t használtam. illetve predikatív 
 melléknév + főnévi igenév konstrukció példányainak hatékony vételezését. 
 
 A CQL kifejezések lehetővé tették, hogy azon  példányok is elérhetővé váljanak, amelyek a részletes keresési 
 beállításokkal nem voltak megtalálhatók. A CQL `lemma=" "` kifejezésrészében, az egyenlőségjel után adjuk meg 
 az általunk keresett segédige, vagy melléknév szótári alakját (lemmáját). Ha a fentebb lévő reguláris kifejezésekre 
 tekintünk, akkor látjuk, hogy az elsőben szerepel példaként az *akar*, míg a másodikban a *képes*. Tehát láthatjuk, 
 hogy a melléknévi komponenst tartalmazó szerkezetek CQL kifejezése eltérő. Ez természetesen a kétféle szerkezet 
 a formai oldalon tapasztalható egymástól való eltérése motiválta. 

 A segédigés konstrukció esetében a segédigei komponenst szemlélve valamilyen (megkötés nincs) finit
 igealakot várunk (tartalmazhat *-hAt* deverbális verbum képzőt is), míg a melléknév/segédmelléknév megvalósulásai közül
 az egyes nominativusi, vagy többes nominativusi eseteket szeretnénk megkapni a főnévi igenévi komponens szomszédjában 
 (pl. *Peti képes úszni*). A főnévi igenévi szerkezettagra vonatkozólag nem volt megkötésünk, ez természetesen lehet 
 igekötős. Az `msd=" "` része tartalmazza a morfológiai és a szófaji annotációkat. 

 A reguláris kifejezés végén látható két darab szám (-2 és 2), amelyek azt jelentik, hogy a segédige/melléknév 
 környezetében mekkora keresési ablakban jelenhet meg a főnévi igenév. Ez megváltoztatható. 

 ### Minta a Magyar Webkorpusz 2.0-ból
 | Segédige / predikatív melléknév + főnévi igenév | A Reprezentatív<br/> minta elemszáma (db) | A teljességre törekvő<br/> minta elemszáma (db) | Összes találat a korpuszban |
|------------------------------|-------|----------|------------|
| ***tud*** + inf.             | 500   | 650000   | 10000000   |
| ***szeret*** + inf.          | 500   | 650000   | 4335004    |
| ***akar*** + inf.            | 500   | 650000   | 4221889    |
| ***képes*** + inf.           | 500   | 650000   | 1408225    |
| ***kíván*** + inf.           | 500   | 650000   | 938075     |
| ***mer*** + inf.             | 384   | 473966   | 473966     |
| ***-kOzik/-kOdik*** + inf.   | 384   | 255799   | 255799     |
| ***hajlandó*** + inf.        | 384   | 272806   | 272806     |
| ***bír*** + inf.             | 384   | 179846   | 179846     |
| ***képtelen*** + inf.        | 384   | 164909   | 164909     |
| ***hajlamos*** + inf.        | 382   | 63343    | 63343      |
| ***remél*** + inf.           | 382   | 55246    | 55246      |
| ***óhajt*** + inf.           | 379   | 21225    | 21225      |
| ***utál*** + inf.            | 379   | 16652    | 16652      |
 | ***gyűlöl*** + inf.          | 310   | 2492     | 2492       |
 | ***vágyik*** + inf.          | 310   | 1658     | 1658       |


 [Az **Magyar Webkorpusz 2.0** keresőfelületén](https://sketchengine.elte-dh.hu/) az alábbi CQL-eket kellett tehát
 megadni:

 (2a) `(meet [lemma="akar" & tag="\[/V\]\[((_Mod/V|_Caus/V)\]\[)?(Prs|Pst|Cond|Sbjv)\.(N?Def\.[1-3](Sg|Pl)|1Sg›2)\]"] 
 [tag="\[/V\]\[Inf\]"] -2 2)`

 (2b) `(meet [lemma="képes" & tag="\[/Adj\]\[Nom\]|\[/Adj\]\[Pl\]\[Nom\]"] [tag="\[/V\]\[Inf\]"] -2 2)`

 A kutatás mintavételéhez alkalmazott CQL kifejezésekről bővebben lásd [fenn.](#minta-az-mnsz2-ből-v205 (v2.0.5))  
 Az eltérés az, hogy itt a CQL `tag=" "` szegmense tartalmazza a morfológiai és a szófaji annotációkat, illetve a 
 szófaji és morfológiai jelenségek kódolása a formai oldalon eltér. A (2a) CQL a segédige + főnévi igenév szerkezeteket
 szűri, a (2b) pedig a predikatív melléknév + főnévi igenév előfordulásokat.

## Útmutató a korpuszokból való mintavételhez

### Minta az MNSZ2-ből

1. Az első lépésben az [MNSZ2 felületén](http://clara.nytud.hu/mnsz2-dev/) állítsuk át a lekérdezés típusát a **CQL**-re
    a legördülő menüből. Ide tudjuk beilleszteni a számunkra megfelelő CQL-t.  

![dokumentacio_mnsz_kereses](dokumentacio/dokumentacio_mnsz_kereses.png)

2. Ha lefuttattuk a keresést, akkor a bal menüsávban kattintsunk a **KWIC/mondat** ikonra. Ez a funkció a találatainkat 
   pontosan egy mondatból álló kontextusban fogja megjeleníteni. 

![dokumentacio_mnsz_kwic](dokumentacio/dokumentacio_mnsz_kwic.png)

3. Ezután célszerű ellenőrizni a megjelenítési beállításokat. Ezt a **Megjelenítés** menüpontra kattintva tudjuk megtenni.  
   A beállításoknál a következőkre figyeljünk: 1. **attribútumok --> word**, 2. **struktúrák --> doc**, 3. **infó --> 
   dokumentumazonosító** opciók legyenek kijelölve/bepipálva.

![dokumentacio_mnsz_megj](dokumentacio/dokumentacio_mnsz_megj.png)

4. Ha a fenti pontokban leírt instrukciókat végrehajtottuk, akkor lépjünk vissza a konkordanciára. 
 A baloldalon látható menüből válasszuk a **Véletlen minta** ikont. Itt megadhatjuk azt, hogy a konkordanciánkból 
 hány elemű mintát szeretnénk vételezni. **Ha a teljes konkordanciával szeretnénk dolgozni, akkor ezt a lépést hagyjuk 
 ki.**

![dokumentacio_mnsz_vel_minta](dokumentacio/dokumentacio_mnsz_vel_minta.png)

5. Lépjünk vissza a konkordanciára, majd válasszuk ki a menüből a **Konkordancia mentése** opciót. A formátumot
   állítsuk át **XML**-re. Ha a konkordanciánk több, mint 1000 elemet tartalmaz, akkor állítsuk át a sorok számát
   a kívánt mennyiségre a minta maximális méretéhez igazodva. A letöltés hosszú időt vehet igénybe, valamint 
   a kapott XML fájlok kódolása a deklarációjukkal ellentétben UTF-8 lesz. Ez az eltérést hibát fog okozni az ékezetek 
   feldolgozásánál. A megoldást lásd ![lenn](#a-feldolgozas-lepesei).

![dokumentacio_mnsz_vel_mentes](dokumentacio/dokumentacio_mnsz_vel_mentes.png)

### Minta a Magyar Webkorpusz 2.0-ból

1. Hasonlóan az [MNSZ2-ből végzett mintavételezéshez](#minta-az-mnsz2-bol), legelőször itt is a keresési céljainkhoz
 megfelelő paramétereket állítsuk be a lekérdező felületen. A **Query type** listában válasszuk ki a **CQL**-t. 
 Illesszük be az általunk preferált CQL kifejezést a mezőbe.

![dokumentacio_webcorpus_kereses](dokumentacio/dokumentacio_webcorpus_kereses.png)

2. A keresés lefuttatása után ellenőrizzük a felső menüsávban a megjelenítést. A soronként pontosan egy mondat
  megjelenítéshez válasszuk ki a **sentence** opciót. 

![dokumentacio_webcorpus_sentence](dokumentacio/dokumentacio_webcorpus_sentence.png)

3. A következő lépésben válasszuk ki a **View options**-t (szem ikon). Itt az alábbi beállítások lesznek fontosak:
   **words** és a **For KWIC Only** opciók kiválasztása, 2. **Use glue** kikapcsolása. 

![dokumentacio_webcorpus_kereses](dokumentacio/dokumentacio_webcorpus_glue_kikapcs.png)

4. A **Get a random sample** (kérdőjeles dobókocka ikon) kiválasztásával tudjuk beállítani a mintavétel méretét 
   (ha a lekérdezés teljes eredményével szeretnénk dolgozni, akkor ezt a lépést hagyjuk ki). 

![dokumentacio_webcorpus_random_sample](dokumentacio/dokumentacio_webcorpus_random_sample.png)

5. Végül kattintsunk a **Download**-ra (lefelé mutató nyíl). Kattintsunk az **XML** gombra. 

![dokumentacio_webcorpus_xml_letoltes](dokumentacio/dokumentacio_webcorpus_xml_letoltes.png)

## Útmutató a TSV (TAB Separated Values) formátum előállításához és az egységes nyelvi előfeldolgozáshoz

Az [e-magyar nyelvi elemzőrendszert (emtsv)](https://github.com/nytud/emtsv) ([Indig et al.]()) használjuk a minták egységes
előfeldolgozásához.

A repoziróium klónozása után a terminálból tudjuk futtatni az alábbi programokat a megfelelő paraméterek megadásával.
 A bemenet lehet egyetlen egy fájl, de akár egy egész mappa is, tehát, ha több fájlt szeretnénk feldolgoztatni,
 akkor nem muszáj egyesével elvégeznünk ezt a műveletet, hanem azonos mappába rendezve őket, 
 –– a mappát paraméterként megadva, –– egy lépésben elvégezhető a művelet rajtuk.
 A terminálban a `cd` paranccsal tudunk a könyvtárak szerkezetén belül lépkedni, valamint az `ls` paranncsal tudjuk
 lekérdezni azt, hogy az adott mappán belül milyen fájlok találhatóak. 
 Mindenekelőtt szükségünk van a virtuális python környezet ([venv](https://docs.python.org/3/library/venv.html)) 
 létrehozására a programok futtatásához.
 

 A két programban az alábbi argumentumok azok, amelyek megegyeznek:
 - `-i` : Az input fájlt/mappát jelöli, itt adjuk meg annak 
   a fájlnak/mappának az elérési útvonalát, amelyet szeretnénk átalakítani.
 - `-o` : az output fájlt/mappát kéri, olyan 
   útvonalat és mappa/fájl nevet adjunk meg, amely még nem létezik a gépünkön. 
 - `-p`: Meg tudjuk vele adni opcionálisan, hogy hány szálon fusson a program a futtatáskor.

A TSV formátum a kimeneti fájlokban olyan megjelenítést hoz létre, amely a fájl elején strukturáltan feltűnteti az adott
mintára vonatkozó metaadatokat:
- forrás (`corpus`)
- méret (`hits`),
- a lekérdezés paraméterei (`query`)

Továbbá a konkrét nyelvi adatra vonatkozó metaadatokat is: 
- dokumentumazonosító (`ref`)
- bal kontextus hossza (`left_length`)
- kwic hossza (`kwic_length`)
- jobb kontextus hossza (`right_length`)

A mondatot egyfelől egészben is megjeleníti (`sent`) valamint a tokeneket egymás alá, listába rendezi tabulátorokkal
elvászatva. 

Az emtsv nyelvi elemzőrendszer által előállított elemzési adatok (pl. lemmatizálás, szófaji címkézés, morfológiai elemzés)
az általa elemzett token mellett kap helyet tabulátorokkal elválasztva.  

### A feldolgozás lépései

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

```commandline
$ ./venv/bin/python xml_to_emtsv.py -i mnsz2_xml -o mnsz2_tsv -f latin-2 -t UTF-8
$ ./venv/bin/python xml_to_emtsv.py -i webkorpusz_xml -o webkorpusz_tsv
```

4. A következőkben az emtsvt fogjuk futtatni a TSV formátummá alakított mintáinkon. Az előzőekhez hasonlóan a parancssorban dolgozunk.

$ ./venv/bin/python xml_to_emtsv.py -i mnsz2_xml -o mnsz2_tsv -f latin-2 -t UTF-8

2. A Python megnyitásához írjuk be, először, hogy `./venv/bin/python` utána írjuk be a program nevét:
   [`emtsv2.py`](emtsv2.py). Ezután a feldolgozáshoz szükséges argumentumok a következők:
    - `-s`: az e-magyar szerverének elérési útvonala (pl. `http://emtsv.elte-dh.hu:5000`)
    - `-m`: a használandó modulok nevei (a használható modulok listájához lásd
       a [dokumentációt](https://github.com/nytud/emtsv#modules)) vesszővel elválasztva (pl. `tok,morph,pos` )
    - `-k`: azokat a mezőneveket adhatjuk meg, amelyeket a kimeneti fájlban meg kívánunk tartani (pl. `form,lemma,xpostag`)
    - `-i` és `-o`: a bemenet és kimenet meghatározására (lásd fent)
    - `-r` (opcinális): megadja, hogy a parancs hányszor próbálkozzon újra az emtsv lekérdezéssel sikertelenség esetén

```commandline
$ ./venv/bin/python emtsv2.py -s http://emtsv.elte-dh.hu:5000 -m morph pos conv-morph dep -k form lemma xpostag upostag 
feats deprel id head -i mnsz_tsv -o mnsz_dep
```

## Források és hivatkozások
- Indig Balázs – Sass Bálint – Simon Eszter –  Mittelholcz Iván –  Kundráth Péter –  Vadász Noémi 2019. emtsv – egy formátum mind felett. In: *XV. Magyar Számítógépes Nyelvészeti Konferencia.* Szegedi Tudományegyetem TTIK, Informatikai Intézet. Szeged.  235–247. [link](http://real.mtak.hu/99685/)
- Krejcie, Robert V. – Morgan, Daryle W. 1970: Determining Sample Size for Research Activities. Educational and
  Psychological Measurement 30: 607–610. [link](https://www.researchgate.net/figure/Krejcie-and-Morgan1970-Sampling-Ratio-Research-Instrument-According-to-Taylor-and_fig3_341908971)
- Magyar Nemzeti Szövegtár (v2.0.5); Oravecz Csaba – Váradi Tamás – Sass Bálint 2014. The Hungarian Gigaword Corpus. In: Calzolari, Nicoletta – Choukri, Khalid – Declerck, Thierry – Loftsson, Hrafn –Maegaard, Bente – Mariani, Joseph – Moreno, Asuncion – Odijk, Jan – Piperidis, Stelios (eds.): *Proceedings of the ninth international conference on language resources and evaluation (LREC-2014)*. Reykjavik: European Languages Resources Association (ELRA). 1719–1723. [link](http://real.mtak.hu/20143/)
- Magyar Webkorpus 2.0; Nemeskey Dávid Márk 2020. *Natural Language Processing methods for Language Modeling*. PhD thesis. Eötvös Loránd University. [link](https://hlt.bme.hu/media/pdf/nemeskey_thesis.pdf)
- Van linden, An. 2010. From premodal to modal meaning: Adjectival pathways in English. *Cognitive Linguistics 21 (3)*: 537–571. [link](https://www.researchgate.net/publication/249926985_From_premodal_to_modal_meaning_Adjectival_pathways_in_English)
