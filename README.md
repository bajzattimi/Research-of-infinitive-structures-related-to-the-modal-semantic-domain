# A (pre)modális szemantikai térrel összekapcsolódó főnévi igeneves szerkezetek vizsgálata
A jelen kutatás a segédige + főnévi igeneves szerkezetek megvalósulási környezeteit hivatott elemezni korpuszalapon, számítógépes vizsgálati eljárásokkal. Az adatokból látható mintázat-együttállásokból elméleti hipotézisek felállításával kapcsolódik ahhoz a kutatási kérdéshez, hogy a vizsgált premodális (lehetségességi relációt nem explikáló) jelentéssel asszociálódó főnévi igeneves kompozitumszerkezetek milyen nyelvi, konstrukcionális kidolgozottságban képesek átlépni a jelentésképzés során a modális szemantikai térbe. 

## Minták a korpuszokból
### Minta az MNSZ2-ből (v2.0.5)
1. ***tud*** + inf. (a minta mérete: 500)
2. ***akar*** + inf. (a minta mérete: 384)
3. ***szeret*** + inf. (a minta mérete: 384)
4. ***kíván*** + inf. (a minta mérete: 384)
5. ***képes*** + inf. (a minta mérete: 384)
6. ***mer*** + inf. (a minta mérete: 382)
7. ***képtelen*** + inf. (a minta mérete: 381)
8. ***hajlandó*** + inf. (a minta mérete: 381)
9. ***bír*** + inf. (a minta mérete: 379)
10. ***szándékozik*** + inf. (a minta mérete: 370)

-   Query    word: `[msd="(IK\.)*IGE\.INF[123]?\*?"]`
-   Positive filter    -2 2 1 `[lemma="***verb***" & msd="(IK\.)*IGE\.(_HAT\.)?[TI]?[MPF]?[et]?[123]?"]`
-   http://clara.nytud.hu/mnsz2-dev/

### Minta a Webcorpus 2.0.-ből
1. ***tud*** + inf. (a minta mérete: 500)
2. ***akar*** + inf. (a minta mérete: 500)
3. ***szeret*** + inf. (a minta mérete: 384)
4. ***kíván*** + inf. (a minta mérete: 384)
5. ***képes*** + inf. (a minta mérete: 384)
6. ***mer*** + inf. (a minta mérete: 381)
7. ***képtelen*** + inf. (a minta mérete: 377)
8. ***hajlandó*** + inf. (a minta mérete: 379)
9. ***bír*** + inf. (sample size: 379)
10. ***szándékozik*** + inf. (sample size: 357)

-   Query word: `[tag="\[/V\]\[Inf\]"]`
-   Positive filter -2 2 1 [lemma_lc="akar"]
-   https://elte-dh.hu/sketchengine/
-   https://sketchengine.elte-dh.hu/

## Útmutató a korpuszokból való mintavételhez
### Minta az MNSZ2-ből (v2.0.5)
**1.** Az első lépésben állítsuk be az MNSZ2 felületén (http://clara.nytud.hu/mnsz2-dev/) az általunk elvégezni kívánt keresés feltételeit. Ennél a lépésnél törekedjünk arra, hogy úgy adjuk meg a keresési paramétereket, hogy azt lefuttatva a számunkra lehető legoptimálisabb mintát adja a keresett nyelvi szerkezet példányaiból. 

![dokumentacio_mnsz_kereses](https://user-images.githubusercontent.com/68318997/148794376-ebbe861c-667f-4417-962a-3b66266654f6.png)

**2.** Ha lefuttattuk a keresést, akkor a bal menüsávban kattintsunk a **KWIC/mondat** ikonra. Ez a funkció a találatainkat pontosan egy mondatból álló kontextusban fogja megjeleníteni. 

![dokumentacio_mnsz_kwic](https://user-images.githubusercontent.com/68318997/148794866-4b105da2-5c74-49e3-9659-6d5b31630453.png)

**3.** Ezután célszerű ellenőrizni a megjelenítési beállításokat. Ezt a **Megjelenítés** menüpontra kattintva tudjuk megtenni. A beállításoknál a következőkre figyeljünk: 1. **attribútumok --> word**, 2. **struktúrák --> doc**, 3. **infó --> dokumentumazonosító**. 

![dokumentacio_mnsz_megj](https://user-images.githubusercontent.com/68318997/148795489-d4c8a1a1-254a-47d3-aa74-dec0f92da54b.png)

**4.** Ha a fenti pontokban leírt instrukciókat végrehajtottuk, akkor lépjünk vissza a konkordanciára. A baloldalon látható menüből válasszuk a **Véletlen minta** pontot. Itt megadhatjuk azt, hogy a konkordanciánkból hány elemű mintát szeretnénk vételezni. Ha a teljes konkordanciával szeretnénk dolgozni, akkor természetesen ezt a lépést hagyjuk ki. 

![dokumentacio_mnsz_vel_minta](https://user-images.githubusercontent.com/68318997/148796155-f937eccb-8f5e-4cc6-8644-eba5d7e3d6f7.png)

**5.** Navigáljunk vissza a konkordanciára, majd válasszuk ki a menüből a **Konkordancia mentése** opciót. A formátumot állítsuk át **XML**-re. Ha a konkordanciánk több, mint 1000 elemet tartalmaz, akkor állítsuk át a sorok számát a megfelelő mennyiségre a minta méretéhez igazodva. 

![dokumentacio_mnsz_vel_mentes](https://user-images.githubusercontent.com/68318997/148796577-b67d0854-8c82-4811-b34b-00dab4f58cb5.png)

### Minta a Webcorpus 2.0-ből
**1.** Hasonlóan az MNSZ2-ből végzett mintavételezéshez, legelőször itt is a keresési céljainkhoz megfelelő paramétereket állítsuk be a lekérdező felületen. 

![dokumentacio_webcorpus_kereses](https://user-images.githubusercontent.com/68318997/148797410-f4f7c4e6-6a27-48d5-90dd-0c368490e57f.png)

(A képen a főnévi igenevekre való CQL-lel történő keresés látható) 

**2.** A keresés lefuttatása után ellenőrizzük a felső menüsávban a megjelenítést. A pontosan egy mondatnyi megjelenítéshez válasszuk ki a **sentence** opciót. 

![dokumentacio_webcorpus_sentence](https://user-images.githubusercontent.com/68318997/148797874-588aaa81-e3d7-4eef-909e-47ecd104cb0d.png)

**3.** A következő lépésben válasszuk ki a **View options**-t (szem ikon). Itt az alábbi beállítások lesznek relevánsak: 1. **words**, 2. **For KWIC Only**, 3. **Use glue** kikapcsolása. 

![dokumentacio_webcorpus_kereses](https://user-images.githubusercontent.com/68318997/148798516-301815dc-45ef-49bb-aab3-ae9e0a9188c3.png)

**4.** A **Get a random sample** (kérdőjel ikon) kiválasztásával tudjuk beállítani a mintavétel méretét (ha a teljes konkordanciával szeretnénk dolgozni, akkor ezt a lépést hagyjuk ki). 

![dokumentacio_webcorpus_random_sample](https://user-images.githubusercontent.com/68318997/148798815-f73053ce-fcc0-455d-80d7-c25dc9385717.png)

**5.** Végül kattintsunk a **Download** pontra (lefelé mutató nyíl). Kattintsunk az **XML** gombra. 

![dokumentacio_webcorpus_xml_letoltes](https://user-images.githubusercontent.com/68318997/148799361-1a234617-2b88-4c4a-b1d8-d7459a5aa54c.png)








