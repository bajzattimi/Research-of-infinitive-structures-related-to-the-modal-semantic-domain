# A (pre)modális szemantikai térrel összekapcsolódó főnévi igeneves szerkezetek vizsgálata
A jelen kutatás a segédige + főnévi igeneves szerkezetek megvalósulási környezeteit hivatott elemezni korpuszalapon, számítógépes vizsgálati eljárásokkal. Az adatokból látható mintázat-együttállásokból elméleti hipotézisek felállításával kapcsolódik ahhoz a kutatási kérdéshez, hogy a vizsgált premodális (lehetségességi relációt nem explikáló) jelentéssel asszociálódó főnévi igeneves kompozitumszerkezetek milyen nyelvi, konstrukcionális kidolgozottságban képesek átlépni a jelentésképzés során a modális szemantikai térbe. A mintavételezés az MNSZ2-ből (Oravecz–Váradi–Sass 2014) és a Webcorpusból valósult meg két lépcsőben. Az első mintavétel során egy reprezentatív (a korpusz méretéhez viszonyítva) elemszámú csoportot vételeztem, a másodiknál pedig törekedtem a keresési kondíciók által kiadott összes elem mentésére. Ezen utóbbi eljárás nem minden esetben tudott megvalósulni, ekkor a lehető legnagyobb konkordancia kinyerése volt a cél. Ugyan a korpuszok által felkínált részletes keresési metódusok nagyon kedvezőnek tűnnek, azonban a legprecízebb mintavételezési módnak a cql kifejezéssel történő szűrés bizonyult.

## Minták a korpuszokból
### Minta az MNSZ2-ből (v2.0.5)
1. ***tud*** + inf. (a minta mérete: 500) / ***tud*** + inf. (a minta mérete: 675000) | teljes minta: 1315296
2. ***akar*** + inf. (a minta mérete: 384) / ***akar*** + inf. (a minta mérete: 610836) | teljes minta: 610836
3. ***szeret*** + inf. (a minta mérete: 384) / ***szeret*** + inf. (a minta mérete: 484448) | teljes minta: 484448
4. ***kíván*** + inf. (a minta mérete: 384) / ***kíván*** + inf. (a minta mérete: 192678) | teljes minta: 192678
5. ***képes*** + inf. (a minta mérete: 384) / ***képes*** + inf. (a minta mérete: 134843) | teljes minta: 134843
6. ***-kOzik|-kOdik*** + inf. (a minta mérete: 382) / ***-kOzik|-kOdik*** + inf. (a minta mérete: 255799) | teljes minta: 255799
7. ***mer*** + inf. (a minta mérete: 382) / ***mer*** + inf. (a minta mérete: 63729) | teljes minta: 63729
8. ***képtelen*** + inf. (a minta mérete: 381) / ***képtelen*** + inf. (a minta mérete: 48036) | teljes minta: 48036
9. ***hajlandó*** + inf. (a minta mérete: 381) / ***hajlandó*** + inf. (a minta mérete: 48267) | teljes minta: 48267
10. ***bír*** + inf. (a minta mérete: 379) / ***bír*** + inf. (a minta mérete: 22191) | teljes minta: 22191
11. ***remél*** + inf. (a minta mérete: 364) / ***remél*** + inf. (a minta mérete: 6506) | teljes minta: 6506
12. ***óhajt*** + inf. (a minta mérete: 361) / ***óhajt*** + inf. (a minta mérete: 5500) | teljes minta: 5500
13. ***hajlamos*** + inf. (a minta mérete: 357) / ***hajlamos*** + inf. (a minta mérete: 4212) | teljes minta: 4212
14. ***vágyik*** + inf. (a minta mérete: 313) / ***vágyik*** + inf. (a minta mérete: 1658) | teljes minta: 1658
14. ***utál*** + inf. (a minta mérete: 306) / ***utál*** + inf. (a minta mérete: 1448) | teljes minta: 1448
15. ***gyűlöl*** + inf. (a minta mérete: 132) / ***gyűlöl*** + inf. (a minta mérete: 132) | teljes minta: 188

`(meet [lemma="akar" & msd="(IK\.)*IGE\.(_HAT\.)?[TI]?[MPF]?[et]?[123]?"] [msd="(IK\.)*IGE\.INF[123]?\*?"] -2 2)`

`(meet [lemma="képes" & msd="MN.PL*.NOM"] [msd="(IK\.)*IGE\.INF[123]?\*?"] -2 2)`

**MNSZ2** [link](http://clara.nytud.hu/mnsz2-dev/)

### Minta a Webkorpus 2.0.-ből
1. ***tud*** + inf. (a minta mérete: 500) / ***tud*** + inf. (a minta mérete: 650000) | teljes minta: 10000000
2. ***szeret*** + inf. (a minta mérete: 500) / ***szeret*** + inf. (a minta mérete: 650000) | teljes minta: 4335004
3. ***akar*** + inf. (a minta mérete: 500) / ***akar*** + inf. (a minta mérete: 650000) | teljes minta: 4221889
4. ***képes*** + inf. (a minta mérete: 500) / ***képes*** + inf. (a minta mérete: 650000) | teljes minta: 1408225
5. ***kíván*** + inf. (a minta mérete: 500) / ***kíván*** + inf. (a minta mérete: 650000) | teljes minta: 938075
6. ***mer*** + inf. (a minta mérete: 384) / ***mer*** + inf. (a minta mérete: 473966) | teljes minta: 473966
7. ***-kOzik|-kOdik*** + inf. (a minta mérete: 384) / ***-kOzik|-kOdik*** + inf. (a minta mérete: 255799) | teljes minta: 255799
8. ***hajlandó*** + inf. (a minta mérete: 384) / ***hajlandó*** + inf. (a minta mérete: 272806) | teljes minta: 272806
9. ***bír*** + inf. (sample size: 384) / ***bír*** + inf. (a minta mérete: 179846) | teljes minta: 179846
10. ***képtelen*** + inf. (a minta mérete: 384) / ***képtelen*** + inf. (a minta mérete: 164909) | teljes minta: 164909
11. ***hajlamos*** + inf. (a minta mérete: 382) / ***hajlamos*** + inf. (a minta mérete: 63343) | teljes minta: 63343
12. ***remél*** + inf. (a minta mérete: 382) / ***remél*** + inf. (a minta mérete: 55246) | teljes minta: 55246
13. ***óhajt*** + inf. (a minta mérete: 379) / ***óhajt*** + inf. (a minta mérete: 21225) | teljes minta: 21225
14. ***utál*** + inf. (a minta mérete: 379) / ***utál*** + inf. (a minta mérete: 16652) | teljes minta: 16652
15. ***gyűlöl*** + inf. (a minta mérete: 310) / ***gyűlöl*** + inf. (a minta mérete: 2492) | teljes minta: 2492
16. ***vágyik*** + inf. (a minta mérete: 379) / ***vágyik*** + inf. (a minta mérete: 1658) | teljes minta: 1658

`(meet [lemma="akar" & tag="\[/V\]\[((_Mod/V|_Caus/V)\]\[)?(Prs|Pst|Cond|Sbjv)\.(N?Def\.[1-3](Sg|Pl)|1Sg›2)\]"] [tag="\[/V\]\[Inf\]"] -2 2)`

`(meet [lemma="képes" & tag="\[/Adj\]\[Nom\]|\[/Adj\]\[Pl\]\[Nom\]"] [tag="\[/V\]\[Inf\]"] -2 2)`

**Webkorpus 2.0** [link](https://sketchengine.elte-dh.hu/)

## Útmutató a korpuszokból való mintavételhez
### Minta az MNSZ2-ből (v2.0.5) (Oravecz – Váradi – Sass 2014)
1. Az első lépésben az MNSZ2 felületén (http://clara.nytud.hu/mnsz2-dev/) állítsuk át a lekérdezés típusát a **CQL**-re a legördülő menüből. Ide tudjuk beilleszteni a számunkra megfelelő cql-t. A jelen dokumentációban a Magyar Nemteti Szövegtár felületén a segédigék és segédmelléknevek elérése olyan cql-t kínálunk, amellyel -2 +2 (a nódusztól/kwictől jobbra és balra 2–2 pozícióban) ablakban tudjuk lekérni a segédigés komponenst a főnévi igenévhez viszonyítva. Természetesen ezt az ablakot opcionálisan tudjuk állítani, ehhez írjuk át a cql kód végén szereplő számokat). 

![dokumentacio_mnsz_kereses](dokumentacio/dokumentacio_mnsz_kereses.png)

2. Ha lefuttattuk a keresést, akkor a bal menüsávban kattintsunk a **KWIC/mondat** ikonra. Ez a funkció a találatainkat pontosan egy mondatból álló kontextusban fogja megjeleníteni. 

![dokumentacio_mnsz_kwic](dokumentacio/dokumentacio_mnsz_kwic.png)

3. Ezután célszerű ellenőrizni a megjelenítési beállításokat. Ezt a **Megjelenítés** menüpontra kattintva tudjuk megtenni. A beállításoknál a következőkre figyeljünk: 1. **attribútumok --> word**, 2. **struktúrák --> doc**, 3. **infó --> dokumentumazonosító**. 

![dokumentacio_mnsz_megj](dokumentacio/dokumentacio_mnsz_megj.png)

4. Ha a fenti pontokban leírt instrukciókat végrehajtottuk, akkor lépjünk vissza a konkordanciára. A baloldalon látható menüből válasszuk a **Véletlen minta** ikont. Itt megadhatjuk azt, hogy a konkordanciánkból hány elemű mintát szeretnénk vételezni. Ha a teljes konkordanciával szeretnénk dolgozni, akkor ezt a lépést hagyjuk ki. 

![dokumentacio_mnsz_vel_minta](dokumentacio/dokumentacio_mnsz_vel_minta.png)

5. Navigáljunk vissza a konkordanciára, majd válasszuk ki a menüből a **Konkordancia mentése** opciót. A formátumot állítsuk át **XML**-re. Ha a konkordanciánk több, mint 1000 elemet tartalmaz, akkor állítsuk át a sorok számát a megfelelő mennyiségre a minta méretéhez igazodva. 

![dokumentacio_mnsz_vel_mentes](dokumentacio/dokumentacio_mnsz_vel_mentes.png)

### Minta a Webkorpus 2.0-ból (Nemeskey 2020)
1. Hasonlóan az MNSZ2-ből végzett mintavételezéshez, legelőször itt is a keresési céljainkhoz megfelelő paramétereket állítsuk be a lekérdező felületen. A **Query type** listában válasszuk ki a **CQL**-t. Illesszük be az általunk preferált cql kifejezést a mezőbe. Ahogyan az MNSZ2 esetében, itt is tudjuk állítani a keresési ablakot azzal, ha a -2 2 értékeket megváltoztatjuk.

![dokumentacio_webcorpus_kereses](dokumentacio/dokumentacio_webcorpus_kereses.png)

2. A keresés lefuttatása után ellenőrizzük a felső menüsávban a megjelenítést. A pontosan egy mondatnyi megjelenítéshez válasszuk ki a **sentence** opciót. 

![dokumentacio_webcorpus_sentence](dokumentacio/dokumentacio_webcorpus_sentence.png)

3. A következő lépésben válasszuk ki a **View options**-t (szem ikon). Itt az alábbi beállítások lesznek relevánsak: 1. **words**, 2. **For KWIC Only**, 3. **Use glue** kikapcsolása. 

![dokumentacio_webcorpus_kereses](dokumentacio/dokumentacio_webcorpus_glue_kikapcs.png)

4. A **Get a random sample** (kérdőjeles dobókocka ikon) kiválasztásával tudjuk beállítani a mintavétel méretét (ha a teljes konkordanciával szeretnénk dolgozni, akkor ezt a lépést hagyjuk ki). 

![dokumentacio_webcorpus_random_sample](dokumentacio/dokumentacio_webcorpus_random_sample.png)

5. Végül kattintsunk a **Download**-ra (lefelé mutató nyíl). Kattintsunk az **XML** gombra. 

![dokumentacio_webcorpus_xml_letoltes](dokumentacio/dokumentacio_webcorpus_xml_letoltes.png)

## Útmutató a tsv formátum eléréséhez

1. Ahhoz, hogy az e-magyar nyelvi elemző képes legyen feldolgozni a korpuszokból kinyert adatainkat, tsv formátummá kell alakítanunk az xml-eket. Ehhez a repozitóriumban megtalálható **xml_to_tsv** nevű programot fogjuk használni. A repoziróium klónozása után a terminálból tudjuk futtatni a programot a megfelelő paraméterek megadásával. Az input lehet egyetlen egy fájl, de akár egy egész mappa is, tehát, ha több fájlt szeretnénk feldolgoztatni, akkor nem muszáj egyesével elvégeznünk ezt, hanem egy közös mappába rendezve őket egy lépésben elvégezhető a művelet rajtuk. Nyissuk meg a terminált, navigáljunk a klónozott könyvtárba. A terminálban a `cd` paranccsal tudunk a könyvtárak szerkezetén belül navigálni, valamint az `ls` paranncsal tudjuk lekérdezni azt, hogy az adott mappán belül milyen fájlok találhatóak. 

![dokumentacio_tsv_parancssor.png](dokumentacio/dokumentacio_tsv_parancssor.png) 

2. A Python megnyitásához írjuk be, először, hogy `./venv/bin/python` utána írjuk be a program nevét: `xml_to_emtsv.py`. Ezután az argumentumok felvitele történik. Az `-i` az input fájlt/mappát jelöli, itt adjuk meg annak a fájlnak/mappának az elérési útvonalát, amelyet szeretnénk átalakítani. Az `-o` az output fájlt/mappát kéri, olyan útvonalat és mappa/fájl nevet adjunk meg, amely még nem létezik a gépünkön. A `-p` azt jelenti, hogy hány szálon fusson a program a futtatáskor. Az `-f` és a `-t` argumentum abban az esetben szükséges, amikor a karakterkódolása a mintáinknak nem alapértelmezetten **UTF-8**.

![dokumentacio_tsv_mutatvany.png](dokumentacio/dokumentacio_tsv_mutatvany.png)

3. Ha megnyitjuk a kimeneti tsv fájlt a számítógépünkön (táblázatkezelő szoftverben pl.), akkor látjuk, hogy az adatok előtt a metaadatokat is megtaláljuk.

## Útmutató az emtsv (Indig et al. 2019) használatához

1. A következőkben az e-magyar nyelvi elemzőt fogjuk futtatni a tsv formátummá alakított mintáinkon. Az előzőekhez hasonlóan a parancssorban dolgozunk.

![dokumentacio_emtsv_parancssor.png](dokumentacio/dokumentacio_emtsv_parancssor.png)

2. A Python megnyitásához írjuk be, először, hogy `./venv/bin/python` utána írjuk be a program nevét: `emtsv2.py`. Ezután az argumentumok felvitele történik. Az `-s` az e-magyar szerverének elérési útvonalát kéri: `http://emtsv.elte-dh.hu:5000` az `-m` argumentumban meg fel tudjuk vinni azokat a modulokat, amelyeket használni kívánunk. A `-k` argumentumban azokat a mezőket adhatjuk meg, amelyeket a kimeneti fájlban kívánunk megtartani. Az `-i` az input fájlt/mappát jelöli, itt adjuk meg annak a fájlnak/mappának az elérési útvonalát, amelyet szeretnénk átalakítani. Az `-o` az output fájlt/mappát kéri, olyan útvonalat és mappa/fájl nevet adjunk meg, amely még nem létezik a gépünkön. Ha kívánjuk állítani azon, hogy hány szálon fusson a program akkor a `-p` argumentum megadásával ezt meg tudjuk tenni. Használhatjuk az `-r` argumentumot is, amelyben be tudjuk állítani, hogy a parancs hányszor próbálkozzon meg a program futtatásával sikertelenség esetén. 

![dokumentacio_emtsv_mutatvany.png](dokumentacio/dokumentacio_emtsv_mutatvany.png)


## Források és hivatkozások
- Indig Balázs – Sass Bálint – Simon Eszter –  Mittelholcz Iván –  Kundráth Péter –  Vadász Noémi 2019. emtsv – egy formátum mind felett. In: *XV. Magyar Számítógépes Nyelvészeti Konferencia.* Szegedi Tudományegyetem TTIK, Informatikai Intézet. Szeged.  235–247. [link](http://real.mtak.hu/99685/)
- Magyar Nemzeti Szövegtár (v2.0.5); Oravecz Csaba – Váradi Tamás – Sass Bálint 2014. The Hungarian Gigaword Corpus. In: Calzolari, Nicoletta – Choukri, Khalid – Declerck, Thierry – Loftsson, Hrafn –Maegaard, Bente – Mariani, Joseph – Moreno, Asuncion – Odijk, Jan – Piperidis, Stelios (eds.): *Proceedings of the ninth international conference on language resources and evaluation (LREC-2014)*. Reykjavik: European Languages Resources Association (ELRA). 1719–1723. [link](http://real.mtak.hu/20143/)
- Webkorpus 2.0; Nemeskey Dávid Márk 2020. *Natural Language Processing methods for Language Modeling*. PhD thesis. Eötvös Loránd University. [link](https://hlt.bme.hu/media/pdf/nemeskey_thesis.pdf)

