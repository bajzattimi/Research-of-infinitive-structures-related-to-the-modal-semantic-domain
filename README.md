# Research-of-infinitive-structures-related-to-the-modal-semantic-domain
## Samples
### Samples from MNSZ2 (v2.0.5)
1. ***tud*** + inf. (sample size: 500)
2. ***akar*** + inf. (sample size: 384)
3. ***szeret*** + inf. (sample size: 384)
4. ***kíván*** + inf. (sample size: 384)
5. ***képes*** + inf. (sample size: 384)
6. ***mer*** + inf. (sample size: 382)
7. ***képtelen*** + inf. (sample size: 381)
8. ***hajlandó*** + inf. (sample size: 381)
9. ***bír*** + inf. (sample size: 379)
10. ***szándékozik*** + inf. (sample size: 370)

- Query    word, [msd="(IK\.)*IGE\.INF[123]?\*?"] 
-   Positive filter    -2 2 1 [lemma="***verb***" & msd="(IK\.)*IGE\.(_HAT\.)?[TI]?[MPF]?[et]?[123]?"] 
-   http://clara.nytud.hu/mnsz2-dev/

### Samples from Webcorpus 2.0.
1. ***tud*** + inf. (sample size: 500)
2. ***akar*** + inf. (sample size: 500)
3. ***szeret*** + inf. (sample size: 384)
4. ***kíván*** + inf. (sample size: 384)
5. ***képes*** + inf. (sample size: 384)
6. ***mer*** + inf. (sample size: 381)
7. ***képtelen*** + inf. (sample size: 377)
8. ***hajlandó*** + inf. (sample size: 379)
9. ***bír*** + inf. (sample size: 379)
10. ***szándékozik*** + inf. (sample size: 357)

## Sampling
### Samples from MNSZ2 (v2.0.5)
**1.** Az első lépésben állítsuk be az MNSZ2 felületén (http://clara.nytud.hu/mnsz2-dev/) az általunk elvégezni kívánt keresés feltételeit. Ennél a lépésnél törekedjünk arra, hogy úgy adjuk meg a keresési paramétereket, hogy azt lefuttatva, a számunkra lehető legoptimálisabb mintát adja a keresett nyelvi szerkezet példányaiból. 

![dokumentacio_mnsz_kereses](https://user-images.githubusercontent.com/68318997/148794376-ebbe861c-667f-4417-962a-3b66266654f6.png)

**2.** Ha lefuttattuk a keresést, akkor a bal menüsávban kattintsunk a **KWIC/mondat** ikonra. Ez a funkció a találatainkat pontosan egy mondatból álló kontextusablakban fogja megjeleníteni. 

![dokumentacio_mnsz_kwic](https://user-images.githubusercontent.com/68318997/148794866-4b105da2-5c74-49e3-9659-6d5b31630453.png)

**3.** Ezután célszerű ellenőrizni a megjelenítési beállításokat. Ezt a **Megjelenítés** menüpontra kattintva tudjuk megtenni. A beállításoknál a következőkre figyeljünk: 1. **attribútumok --> word**, 2. **struktúrák --> doc**, 3. **infó --> dokumentumazonosító**. 

![dokumentacio_mnsz_megj](https://user-images.githubusercontent.com/68318997/148795489-d4c8a1a1-254a-47d3-aa74-dec0f92da54b.png)

**4.** Ha a fenti pontokban leírt instrukciókat végrehajtottuk, akkor lépjünk vissza a konkordanciára. A baloldalon látható menüből válasszik a **Véletlen minta** pontot. Itt megadhatjuk azt, hogy a konkordanciánkból hány elemű mintát szeretnénk vételezni. Ha a teljes konkordanciával szeretnénk dolgozni, akkor természetesen ezt a lépést hagyjuk ki. 

![dokumentacio_mnsz_vel_minta](https://user-images.githubusercontent.com/68318997/148796155-f937eccb-8f5e-4cc6-8644-eba5d7e3d6f7.png)

**5.** Navigáljunk vissza a konkordanciára, majd válasszuk ki a menüből a **Konkordancia mentése** opciót. A formátumot állítsuk át **XML**-re. Ha a konkordanciánk több, mint 1000 elemet tartalmaz, akkor állítsuk át a sorok számát a megfelelő mennyiségre a minta méretéhez igazodva. 

![dokumentacio_mnsz_vel_mentes](https://user-images.githubusercontent.com/68318997/148796577-b67d0854-8c82-4811-b34b-00dab4f58cb5.png)

### Samples from Webcorpus 2.0
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












