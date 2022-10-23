# Ötletek a szűréshez

## Általános szempontok a duplumok szűréséhez


- Kis- és nagybetű érzékenység megoldásához a sorok első tokenjét kisbetűsítjük
- A `lemma` taget tartalmazó sorok csak az igei komponensszerkezet esetében
maradjon meg, mert a többi esetben több információt tartalmaz a konkrét szóalakkal
történő kidolgozás, illetve a részletes morfológiai mintázatok 
- A `Cnj` morfológiai taget tartalmazó sorokat kiszűrjük, mivel nem alkotnak egy
függőségi láncot
- Az `Adv` címkét tartalmazó sorokat töröltük, mivel ez a címke túl általános, 
nem ad elég információt a mintázatról, mivel a tagadószavak, tiltószavak, kiterjesztő
operátorok, névszóból képzett határozók is belekerülnek, tehát olyan típusok, amelyek
funkcionálisan egymástól elkülönböznek 
- Azonos gyakoriságokat célszerű szűrni, és az adott szerkezet legkevésbé absztrakt
mintáját meghagyni 
- Maradhatnak kötőjeles töredékek a sorok elején. Ezek olyan példányokból származnak,
ahol a konstruáló valamilyen morfológiai vagy helyesírási tudatosságból motiválva az n-gram előtt
közvetlenül előforduló lexémához kötőjellel elválasztva kapcsolja a ragot. Ezeket érdemes
talán törölni. 
- Több írásjel egymás mellett törölhető (pl. *:)* )
- `[/Cnj|Abbr][Punct]` törölhető. Ugyan nem lenne vele baj, mert általában ezek a rövidített 
mellérendelői kötőszavak mondatrészek közötti viszonyt dolgoznak ki nyelvileg, de mivel a kötőszavak
törlése mellett döntöttünk, ez a következetes lépés. 
- `[/Inj-Utt]` törölhető

## Az n-gramok optimális hossza

- A 3-ngram túl kicsi, bagyon általános mintázatok (jellemzően igekötő, névszói 
igemódosító vagy *nem* tagadószó kerül a szerkezet elejére.), de érdemes bent hagyni, 
mert nem tűnik hibásnak


## Tartalmazási relációk 
- *A* és *az* határozott névelők esetében érdemesebb megtartani a címkét, mivel ezek
variabilitása mindig az adott hangsortól válik függővé. 
- `[/Adj][_Comp/Adj][_Manner/Adv]`címke valamilyen határozóragos középfok jellel ellátott melléknevet
címkéz fel. Mivel ez is a határozóknak egy típusa, más ragot nem kaphat, de nem venném ki a szűrés során,
mert egyfajta kosntrukcionálódási mintát mutathat, specifikusabb, mint az önmagában álló `Adv` címke
- `[/Adj][_Comp/Adj][Nom]` címke középfok jellel ellátott melléknevet tartalmaz. A melléknevekkel (`Adj`)
lehetne egy részhalmazban kezelni, de talán jobb megtartani először, mert funckióelkülönbözés van. 
- `[/Adj][_Comp/Adj][Transl]` címke a transzlatívuszi raggal ellátott középfok jelet viselő melléknevek
et jelenti. Ezek szintén megfeleltethetők azokkal az esetekkel, amikor jel nélküli melléknév kap
transzlatívuszi ragot, de talán érdemes még először megtartani.
- `[/Adj][_Comp/Adj][Acc]` címke az akkuzatívuszi raggal ellátott középfok jelet viselő melléknevek
et jelenti. Ezek szintén megfeleltethetők azokkal az esetekkel, amikor jel nélküli melléknév kap
akkuzatívuszi ragot, de talán érdemes még először megtartani.
- `[/Adj][_Comp/Adj][Dat]` címke a datívuszi raggal ellátott középfok jelet viselő melléknevek
et jelenti. Ezek szintén megfeleltethetők azokkal az esetekkel, amikor jel nélküli melléknév kap
datívuszi ragot, de talán érdemes még először megtartani.
- `[/Adj][_Comp/Adj][Subl]` címke a szublatívuszi raggal ellátott középfok jelet viselő melléknevek
et jelenti. Ezek szintén megfeleltethetők azokkal az esetekkel, amikor jel nélküli melléknév kap
szublatívuszi ragot, de talán érdemes még először megtartani.
- `[/Adj][_Manner/Adv]` melléknévből képzett határozó. Megtartanám egyelőre a címkét, nem vonnám össze más 
relációval. A sima `Adv` címkével ellátott elemeknék specifikusabb.
- `[/Adj][Acc]` felvethető, hogy akár egyben kezelhető lehetne az `[/N][Acc]` kategóriával, mivel itt
főnévként viselkednek ezek. De ha nem szeretnénk túláltalánosítani, akkor lehet, hogy érdemes meghagyni. 
Viszont most először talán érdemes lenne egy halmazként kezelni őket. Az alábbi táblázat összefoglalja azt, 
hogy melyik más esefekre áll még ez fenn. 

| `[/N]` ragozott alakjainak mintájára kezelhető | `[/N][Pl]` ragozott alakjainak mintájára kezelhető |
|------------------------------------------------|----------------------------------------------------|
| `[/Adj][Acc]`                                  | `[/Adj][Pl][Acc]`                                  |
| `[/Adj][Dat]`                                  | `[/Adj][Pl][Dat]`                                  |
| `[/Adj][Subl]`                                 | `[/Adj][Pl][Subl]`                                 |
| `[/Adj][Transl]`                               | `[/Adj][Pl][Transl]`                               |
| `[/Adj][EssFor:ként]`                          | `[/Adj][Pl][EssFor:ként]`                          |
| `[/Adj][Ill]`                                  | `[/Adj][Pl][Ill]`                                  |
| `[/Adj][Subl]`                                 | `[/Adj][Pl][Subl]`                                 |
| `[/Adj][Transl]`                               | `[/Adj][Pl][Transl]`                               |

- `[/Adj|Pro]` mutatónévmásból képzett melléknévi forma. Akár kezelhető lehetne a melléknevek kategóriájában.
- `[/Adj\Pro][Acc]` címke példányai kezelhetőek lennének az `[Adj]` címke határozóraggal ellátott alakjainak
mintájára.
- `[/Adj\Pro][Dat]` címke példányai kezelhetőek lennének az `[Adj]` címke határozóraggal ellátott alakjainak
mintájára.
- `[/Adj\Pro][Ill]` címke példányai kezelhetőek lennének az `[Adj]` címke határozóraggal ellátott alakjainak
mintájára.
- `[/Adj\Pro][Pl][Acc]` címke példányai kezelhetőek lennének az `[Adj]` címke határozóraggal ellátott alakjainak
mintájára.
- `[/Adj\Pro][Pl][Nom]` mutatónévmásból képzett melléknévi forma többes száma. Nem absztrahálnám tovább. 
- `[/Adv|Pro]`az `[Adv]` mintájára lenne kezelhető.
- `[/Adv\Pro\Rel]` vonatkozó névmási alárendelés, megtartanám.                     
- `[/Adv\Pro\Int]` kérdőszavak nagy halmaza, megtartanám
- `[/Det|Pro]` csak a címkét lenne érdemes megtartani, mert az *az* és az *ez* lehet alternációja

| `[/Det\Pro]` mintájára kezelhető még | `[/N][Pl]` ragozott alakjainak mintájára kezelhető |
|-------------------------------------|----------------------------------------------------|
| `[/Det\Pro][Acc]`                   | `[/Adj][Pl][Acc]`                                  |
| `[/Det\Pro][Del]`                   | `[/Adj][Pl][Dat]`                                  |
| `[/Adj][Subl]`                      | `[/Adj][Pl][Subl]`                                 |
| `[/Adj][Transl]`                    | `[/Adj][Pl][Transl]`                               |

- `[/Adj|Attr][Nom]` ez összevonható az `Adj` kategóriával
- `[/Adj|Pro|Int][Pl][Nom]` A címként hagynám csak meg, mert ez a *milyenek* kérdőszó lesz a mintában
- `[/Adj|Pro|Rel][Acc]` Vonatkozói névmási alárendelés akkuzítavuszi formája. A címkét tartanám csak meg.

| `[/Adj\Pro\Rel][Acc]` mintájára kezelhető még |
|-----------------------------------------------|
| `[/Adj\Pro\Rel][Dat]`                         | 

- `[/Adv][_Comp/Adv]` Határozóraggal ellátott középfok jeles melléknevek. Megtartanám mind a címkét mind
pedig a konrkét példányokat. Természetesen felvethető a redukció is.
- `[/Adv][Del]` Egy típusa a határozóknak, a morfológiai mintázat ellenére kevésbé tűnik már szerkezetileg
transzparensnek, de mivel egy típusát fedi le a határozóknak (pl. *kívül*, *belül*, *távol*) ezért
meghagynám mind a címkét mind pedig a konkrét szóalakokat. 
- `[/Adv|Pro]` Névmásból képzett határozó. Szerintem a címkét lenne érdemes megtartani. 
- `[/Adv|Pro|Int]` A konkrét szóalakokat tartanám meg, mert rendkívül vegyes az, ami ebbe a kategóriába
kerül. Pl. *ott*, *éppúgy*, *néhányan*
- `[/Det|Pro][Abl]`Elég lenne csak a címkét megtartani, és ugyanígy a `[Pl]` többes számú eseteket
kezelni,

| `[Det\Pro][Abl]` mintájára kezelhető még | `[Det\Pro][Pl][Abl]` mintájára |
|------------------------------------------|--------------------------------|
| `[/Det\Pro][Acc]`                        | `[/Det\Pro][Pl][Acc]`          |
| `[/Det\Pro][All]`                        | `[/Det\Pro][Pl][All]`          |
| `[/Det\Pro][Del]`                        | `[/Det\Pro][Pl][Del]`          |
| `[/Det\Pro][Ela]`                        | `[/Det\Pro][Pl][Ela]`          |
| `[/Det\Pro][Ine]`                        | `[/Det\Pro][Pl][Ine]`          |
| `[/Det\Pro][Ill]`                        | `[/Det\Pro][Pl][Ill]`          |
| `[/Det\Pro][Del]`                        | `[/Det\Pro][Pl][Del]`          |
| `[/Det\Pro][Ela]`                        | `[/Det\Pro][Pl][Ela]`          |
| `[/Det\Pro][Ine]`                        | `[/Det\Pro][Pl][Ine]`          |
| `[/Det\Pro][Ins]`                        | `[/Det\Pro][Pl][Ins]`          |
| `[/Det\Pro][Nom]`                        | `[/Det\Pro][Pl][Nom]`          | 

- `[/N]`címke önmagában megfeleltethető az `[/N][Nom]` címkének
- `[/N][_Tmp_Loc/Adv]` Szerintem ez maradjon, és a példányai is, mert időt kifejező határozókat jelöl.
Ennek akár lehet konstrukcionális mintázatbeli jelentősége. 
- Ezek maradjanak címkével és példányokkal is: 

| `[/N][Nom]`         | `[/N][Pl][Nom]`         |
|---------------------|-------------------------|
| `[/N][Abl]`         | `[/N][Pl][Abl]`         |
| `[/N][Acc]`         | `[/N][Pl][All]`         |
| `[/N][Ade]`         | `[/N][Pl][Ade]`         |
| `[/N][All]`         | `[/N][Pl][Ela]`         |
| `[/N][Cau]`         | `[/N][Pl][Cau]`         |
| `[/N][Dat]`         | `[/N][Pl][Dat]`         |
| `[/N][Del]`         | `[/N][Pl][Del]`         |
| `[/N][Ela]`         | `[/N][Pl][Ela]`         |
| `[/N][Ess]`         | `[/N][Pl][Ess]`         |
| `[/N][EssFor:ként]` | `[/N][Pl][EssFor:ként]` |
| `[/N][Ill]`         | `[/N][Pl][Ill]`         | 
| `[/N][Ine]`         | `[/N][Pl][Ine]`         |
| `[/N][Ins]`         | `[/N][Pl][Ins]`         |
| `[/N][Ess]`         | `[/N][Pl][Ess]`         |

- `[/N][Fam.Pl][Nom]` -*ék* többesszám jel. Összevonható lehet az `[/N][Pl][Nom]` példányokkal.  
- `[/N][Nom][Punct]` rövidített alakokat jelöli így (pl. *Mo.*). Összevonható az `[/N][Nom]`
példányokkal. 
- A birtokos személyjjellel ellátott alakok lehetségesen összevonhatóak a paradigmában megfelelő 
birtokos személyjel nélküli példányokkal (pl. `[\N][Acc]` -- `[\N][Poss.1Sg][Acc]`)

| `[/N][Nom]`           | `[/N][Acc]`             | `[/N][Del]`           | `[/N][Ela]`           | `[/N][Ins]`           | `[/N][Ill]`           |
|-----------------------|-------------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| `[\N][Poss.1Sg][Nom]` | `[\N][Poss.1Sg][Acc]`   | `[\N][Poss.1Sg][Del]` | `[\N][Poss.1Sg][Ela]` | `[/N][Poss.1Sg][Ins]` | `[/N][Poss.1Sg][Ill]` |
| `[\N][Poss.2Sg][Nom]` | `[\N][Poss.2Sg][Acc]`   | `[\N][Poss.2Sg][Del]` | `[\N][Poss.2Sg][Ela]` | `[/N][Poss.2Sg][Ins]` | `[/N][Poss.2Sg][Ill]` |
| `[\N][Poss.3Sg][Nom]` | `[\N][Poss.3Sg][Acc]`   | `[\N][Poss.3Sg][Del]` | `[\N][Poss.3Sg][Ela]` | `[/N][Poss.3Sg][Ins]` | `[/N][Poss.3Sg][Ill]` |
| `[\N][Poss.1Pl][Nom]` | `[\N][Poss.1Pl][Acc]`   | `[\N][Poss.1Pl][Del]` | `[\N][Poss.1Pl][Ela]` | `[/N][Poss.1Pl][Ins]` | `[/N][Poss.1Pl][Ill]` |
| `[\N][Poss.2Pl][Nom]` | `[\N][Poss.2Pl][Acc]`   | `[\N][Poss.2Pl][Del]` | `[\N][Poss.2Pl][Ela]` | `[/N][Poss.2Pl][Ins]` | `[/N][Poss.2Pl][Ill]` |
| `[\N][Poss.3Pl][Nom]` | `[\N][Poss.3Pl][Acc]`   | `[\N][Poss.3Pl][Del]` | `[\N][Poss.3Pl][Ela]` | `[/N][Poss.3Pl][Ins]` | `[/N][Poss.3Pl][Ill]` |


