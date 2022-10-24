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
| `[/N][Supe]`        | `[/N][Pl][Supe]`        |
| `[/N][Subl]`        | `[/N][Pl][Subl]`        |
| `[/N][Transl]`      | `[/N][Pl][Transl]`      |
| `[/N][Temp]`        |                         |
| `[/N][Ter]`         | `[/N][Pl][Ter]`         |

- `[/N][Fam.Pl][Nom]` -*ék* többesszám jel. Összevonható lehet az `[/N][Pl][Nom]` példányokkal.  
- `[/N][Nom][Punct]` rövidített alakokat jelöli így (pl. *Mo.*). Összevonható az `[/N][Nom]`
példányokkal. 
- A birtokos személyjjellel ellátott alakok lehetségesen összevonhatóak a paradigmában megfelelő 
birtokos személyjel nélküli példányokkal (pl. `[\N][Acc]` -- `[\N][Poss.1Sg][Acc]`). Ugyanígy járhatunk
el a többes számú alakokkal is. 

| `[/N][Nom]`           | `[/N][Acc]`             | `[/N][Del]`           | `[/N][Ela]`           | `[/N][Ins]`           |
|-----------------------|-------------------------|-----------------------|-----------------------|-----------------------|
| `[\N][Poss.1Sg][Nom]` | `[\N][Poss.1Sg][Acc]`   | `[\N][Poss.1Sg][Del]` | `[\N][Poss.1Sg][Ela]` | `[/N][Poss.1Sg][Ins]` |
| `[\N][Poss.2Sg][Nom]` | `[\N][Poss.2Sg][Acc]`   | `[\N][Poss.2Sg][Del]` | `[\N][Poss.2Sg][Ela]` | `[/N][Poss.2Sg][Ins]` |
| `[\N][Poss.3Sg][Nom]` | `[\N][Poss.3Sg][Acc]`   | `[\N][Poss.3Sg][Del]` | `[\N][Poss.3Sg][Ela]` | `[/N][Poss.3Sg][Ins]` |
| `[\N][Poss.1Pl][Nom]` | `[\N][Poss.1Pl][Acc]`   | `[\N][Poss.1Pl][Del]` | `[\N][Poss.1Pl][Ela]` | `[/N][Poss.1Pl][Ins]` |
| `[\N][Poss.2Pl][Nom]` | `[\N][Poss.2Pl][Acc]`   | `[\N][Poss.2Pl][Del]` | `[\N][Poss.2Pl][Ela]` | `[/N][Poss.2Pl][Ins]` |
| `[\N][Poss.3Pl][Nom]` | `[\N][Poss.3Pl][Acc]`   | `[\N][Poss.3Pl][Del]` | `[\N][Poss.3Pl][Ela]` | `[/N][Poss.3Pl][Ins]` |

| `[/N][Abl]`           | `[/N][Ade]`           | `[/N][All]`           | `[/N][Cau]`           | `[/N][Dat]`           |
|-----------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| `[\N][Poss.1Sg][Abl]` | `[\N][Poss.1Sg][Ade]` | `[\N][Poss.1Sg][All]` | `[\N][Poss.1Sg][Cau]` | `[/N][Poss.1Sg][Dat]` |
| `[\N][Poss.2Sg][Abl]` | `[\N][Poss.2Sg][Ade]` | `[\N][Poss.2Sg][All]` | `[\N][Poss.2Sg][Cau]` | `[/N][Poss.2Sg][Dat]` |
| `[\N][Poss.3Sg][Abl]` | `[\N][Poss.3Sg][Ade]` | `[\N][Poss.3Sg][All]` | `[\N][Poss.3Sg][Cau]` | `[/N][Poss.3Sg][Dat]` |
| `[\N][Poss.1Pl][Abl]` | `[\N][Poss.1Pl][Ade]` | `[\N][Poss.1Pl][All]` | `[\N][Poss.1Pl][Cau]` | `[/N][Poss.1Pl][Dat]` |
| `[\N][Poss.2Pl][Abl]` | `[\N][Poss.2Pl][Ade]` | `[\N][Poss.2Pl][All]` | `[\N][Poss.2Pl][Cau]` | `[/N][Poss.2Pl][Dat]` |
| `[\N][Poss.3Pl][Abl]` | `[\N][Poss.3Pl][Ade]` | `[\N][Poss.3Pl][All]` | `[\N][Poss.3Pl][Cau]` | `[/N][Poss.3Pl][Dat]` |

| `[/N][EssFor:ként]`           | `[/N][Ine]`           | `[/N][Ess]`           | `[/N][Ill]`           |
|-------------------------------|-----------------------|-----------------------|-----------------------|
| `[\N][Poss.1Sg][EssFor:ként]` | `[\N][Poss.1Sg][Ine]` | `[\N][Poss.1Sg][Ess]` | `[/N][Poss.1Sg][Ill]` |
| `[\N][Poss.2Sg][EssFor:ként]` | `[\N][Poss.2Sg][Ine]` | `[\N][Poss.2Sg][Ess]` | `[/N][Poss.1Sg][Ill]` | 
| `[\N][Poss.3Sg][EssFor:ként]` | `[\N][Poss.3Sg][Ine]` | `[\N][Poss.3Sg][Ess]` | `[\N][Poss.3Sg][Ill]` | 
| `[\N][Poss.1Pl][EssFor:ként]` | `[\N][Poss.1Pl][Ine]` | `[\N][Poss.1Pl][Ess]` | `[\N][Poss.1Pl][Ill]` |
| `[\N][Poss.2Pl][EssFor:ként]` | `[\N][Poss.2Pl][Ine]` | `[\N][Poss.2Pl][Ess]` | `[\N][Poss.2Pl][Ill]` |
| `[\N][Poss.3Pl][EssFor:ként]` | `[\N][Poss.3Pl][Ine]` | `[\N][Poss.3Pl][Ess]` | `[\N][Poss.3Pl][Ill]` |

| `[/N][Supe]`           | `[/N][Subl]`           | `[/N][Transl]`           | `[/N][Temp]`           |
|------------------------|------------------------|--------------------------|------------------------|
| `[\N][Poss.1Sg][Supe]` | `[\N][Poss.1Sg][Subl]` | `[\N][Poss.1Sg][Transl]` | `[\N][Poss.1Sg][Temp]` |
| `[\N][Poss.2Sg][Supe]` | `[\N][Poss.2Sg][Subl]` | `[\N][Poss.2Sg][Transl]` | `[\N][Poss.2Sg][Temp]` |
| `[\N][Poss.3Sg][Supe]` | `[\N][Poss.3Sg][Subl]` | `[\N][Poss.3Sg][Transl]` | `[\N][Poss.3Sg][Temp]` |
| `[\N][Poss.1Pl][Supe]` | `[\N][Poss.1Pl][Subl]` | `[\N][Poss.1Pl][Transl]` | `[\N][Poss.1Pl][Temp]` |
| `[\N][Poss.2Pl][Supe]` | `[\N][Poss.2Pl][Subl]` | `[\N][Poss.2Pl][Transl]` | `[\N][Poss.2Pl][Temp]` |
| `[\N][Poss.3Pl][Supe]` | `[\N][Poss.3Pl][Subl]` | `[\N][Poss.3Pl][Transl]` | `[\N][Poss.3Pl][Temp]` |

| `[/N][Ter]`           | 
|-----------------------|
| `[\N][Poss.1Sg][Ter]` | 
| `[\N][Poss.2Sg][Ter]` | 
| `[\N][Poss.3Sg][Ter]` |
| `[\N][Poss.1Pl][Ter]` |
| `[\N][Poss.2Pl][Ter]` |
| `[\N][Poss.3Pl][Ter]` |

| `[/N][Pl][Nom]`          | `[/N][Pl][Acc]`          | `[/N][Pl][Del]`          | `[/N][Pl][Ela]`          | `[/N][Pl][Ins]`          |
|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| `[\N][Pl.Poss.1Sg][Nom]` | `[\N][Pl.Poss.1Sg][Acc]` | `[\N][Pl.Poss.1Sg][Del]` | `[\N][Pl.Poss.1Sg][Ela]` | `[/N][Pl.Poss.1Sg][Ins]` |
| `[\N][Pl.Poss.2Sg][Nom]` | `[\N][Pl.Poss.2Sg][Acc]` | `[\N][Pl.Poss.2Sg][Del]` | `[\N][Pl.Poss.2Sg][Ela]` | `[/N][Pl.Poss.2Sg][Ins]` |
| `[\N][Pl.Poss.3Sg][Nom]` | `[\N][Pl.Poss.3Sg][Acc]` | `[\N][Pl.Poss.3Sg][Del]` | `[\N][Pl.Poss.3Sg][Ela]` | `[/N][Pl.Poss.3Sg][Ins]` |
| `[\N][Pl.Poss.1Pl][Nom]` | `[\N][Pl.Poss.1Pl][Acc]` | `[\N][Pl.Poss.1Pl][Del]` | `[\N][Pl.Poss.1Pl][Ela]` | `[/N][Pl.Poss.1Pl][Ins]` |
| `[\N][Pl.Poss.2Pl][Nom]` | `[\N][Pl.Poss.2Pl][Acc]` | `[\N][Pl.Poss.2Pl][Del]` | `[\N][Pl.Poss.2Pl][Ela]` | `[/N][Pl.Poss.2Pl][Ins]` |
| `[\N][Pl.Poss.3Pl][Nom]` | `[\N][Pl.Poss.3Pl][Acc]` | `[\N][Pl.Poss.3Pl][Del]` | `[\N][Pl.Poss.3Pl][Ela]` | `[/N][Pl.Poss.3Pl][Ins]` |

| `[/N][Pl][Abl]`          | `[/N][Pl][Ade]`          | `[/N][Pl][All]`          | `[/N][Pl][Cau]`          | `[/N][Pl][Dat]`          |
|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|
| `[\N][Pl.Poss.1Sg][Abl]` | `[\N][Pl.Poss.1Sg][Ade]` | `[\N][Pl.Poss.1Sg][All]` | `[\N][Pl.Poss.1Sg][Cau]` | `[/N][Pl.Poss.1Sg][Dat]` |
| `[\N][Pl.Poss.2Sg][Abl]` | `[\N][Pl.Poss.2Sg][Ade]` | `[\N][Pl.Poss.2Sg][All]` | `[\N][Pl.Poss.2Sg][Cau]` | `[/N][Pl.Poss.2Sg][Dat]` |
| `[\N][Pl.Poss.3Sg][Abl]` | `[\N][Pl.Poss.3Sg][Ade]` | `[\N][Pl.Poss.3Sg][All]` | `[\N][Pl.Poss.3Sg][Cau]` | `[/N][Pl.Poss.3Sg][Dat]` |
| `[\N][Pl.Poss.1Pl][Abl]` | `[\N][Pl.Poss.1Pl][Ade]` | `[\N][Pl.Poss.1Pl][All]` | `[\N][Pl.Poss.1Pl][Cau]` | `[/N][Pl.Poss.1Pl][Dat]` |
| `[\N][Pl.Poss.2Pl][Abl]` | `[\N][Pl.Poss.2Pl][Ade]` | `[\N][Pl.Poss.2Pl][All]` | `[\N][Pl.Poss.2Pl][Cau]` | `[/N][Pl.Poss.2Pl][Dat]` |
| `[\N][Pl.Poss.3Pl][Abl]` | `[\N][Pl.Poss.3Pl][Ade]` | `[\N][Pl.Poss.3Pl][All]` | `[\N][Pl.Poss.3Pl][Cau]` | `[/N][Pl.Poss.3Pl][Dat]` |


| `[/N][Pl][EssFor:ként]`            | `[/N][Pl][Ine]`          | `[/N][Pl][Ess]`          | `[/N][Pl][Ill]`           |
|------------------------------------|--------------------------|--------------------------|---------------------------|
| `[\N][Pl.Poss.1Sg][EssFor:ként]`   | `[\N][Pl.Poss.1Sg][Ine]` | `[\N][Pl.Poss.1Sg][Ess]` | `[/N][Pl.Poss.1Sg][Ill]`  |
| `[\N][Pl.Poss.2Sg][EssFor:ként]`   | `[\N][Pl.Poss.2Sg][Ine]` | `[\N][Pl.Poss.2Sg][Ess]` | `[/N][Pl.Poss.1Sg][Ill]`  | 
| `[\N][Pl.Poss.3Sg][EssFor:ként]`   | `[\N][Pl.Poss.3Sg][Ine]` | `[\N][Pl.Poss.3Sg][Ess]` | `[\N][Pl.Poss.3Sg][Ill]`  | 
| `[\N][Pl.Poss.1Pl][EssFor:ként]`   | `[\N][Pl.Poss.1Pl][Ine]` | `[\N][Pl.Poss.1Pl][Ess]` | `[\N][Pl.Poss.1Pl][Ill]`  |
| `[\N][Pl.Poss.2Pl][EssFor:ként]`   | `[\N][Pl.Poss.2Pl][Ine]` | `[\N][Pl.Poss.2Pl][Ess]` | `[\N][Pl.Poss.2Pl][Ill]`  |
| `[\N][Pl.Poss.3Pl][EssFor:ként]`   | `[\N][Pl.Poss.3Pl][Ine]` | `[\N][Pl.Poss.3Pl][Ess]` | `[\N][Pl.Poss.3Pl][Ill]`  |

| `[/N][Pl][Supe]`          | `[/N][Pl][Subl]`          | `[/N][Pl][Transl]`          | `[/N][Pl][Temp]`          |
|---------------------------|---------------------------|-----------------------------|---------------------------|
| `[\N][Pl.Poss.1Sg][Supe]` | `[\N][Pl.Poss.1Sg][Subl]` | `[\N][Pl.Poss.1Sg][Transl]` | `[\N][Pl.Poss.1Sg][Temp]` |
| `[\N][Pl.Poss.2Sg][Supe]` | `[\N][Pl.Poss.2Sg][Subl]` | `[\N][Pl.Poss.2Sg][Transl]` | `[\N][Pl.Poss.2Sg][Temp]` |
| `[\N][Pl.Poss.3Sg][Supe]` | `[\N][Pl.Poss.3Sg][Subl]` | `[\N][Pl.Poss.3Sg][Transl]` | `[\N][Pl.Poss.3Sg][Temp]` |
| `[\N][Pl.Poss.1Pl][Supe]` | `[\N][Pl.Poss.1Pl][Subl]` | `[\N][Pl.Poss.1Pl][Transl]` | `[\N][Pl.Poss.1Pl][Temp]` |
| `[\N][Pl.Poss.2Pl][Supe]` | `[\N][Pl.Poss.2Pl][Subl]` | `[\N][Pl.Poss.2Pl][Transl]` | `[\N][Pl.Poss.2Pl][Temp]` |
| `[\N][Pl.Poss.3Pl][Supe]` | `[\N][Pl.Poss.3Pl][Subl]` | `[\N][Pl.Poss.3Pl][Transl]` | `[\N][Pl.Poss.3Pl][Temp]` |

| `[/N][Pl][Ter]`          | 
|--------------------------|
| `[\N][Pl.Poss.1Sg][Ter]` | 
| `[\N][Pl.Poss.2Sg][Ter]` | 
| `[\N][Pl.Poss.3Sg][Ter]` |
| `[\N][Pl.Poss.1Pl][Ter]` |
| `[\N][Pl.Poss.2Pl][Ter]` |
| `[\N][Pl.Poss.3Pl][Ter]` |

- `[/N|Pro][1][Pl]` a személyes névmási paradigma T/1.-hez lehorgonyzódó tagja. A címkét tartanám
csak meg, mivel nem változatos az általa lefedett példányok formai és szemantikai kidolgozása. Ugyanígy
járnék el a paradigma összes tagjával. Ez a személyes névmási paradigma, nagyon hasonló a visszaható
névmási paradigma morfológiai címkéjével. Ezek egymással nem vonhatók össze. 
A személyes névmási paradigmába tartozó tagoknak csak a morfológiai címkéjüket őrizzük meg! Érdekes, 
mert csak bizonyos tagok kapnak a két paradigmán belül eltérő morfológiai címkét. Ezek lesznek azok a
tag-ek, ahol csak a címkét őrizzük meg: 

| Csak a tag-et őrizzük meg          | 
|------------------------------------|
| `[\N][Pro][1Sg][Nom]`              | 
| `[\N][Pro][1Sg][Acc]`              | 
| `[\N][Pro][1Sg][Del]`              |
| `[\N][Pro][1Sg][Ela]`              |
| `[\N][Pro][1Sg][Ins]`              |
| `[\N][Pro][1Sg][Abl]`              |
| `[\N][Pro][1Sg][Ade]`              | 
| `[\N][Pro][1Sg][All]`              | 
| `[\N][Pro][1Sg][Cau]`              |
| `[\N][Pro][1Sg][Dat]`              |
| `[\N][Pro][1Sg][EssFor:ként]`      |
| `[\N][Pro][1Sg][Ess]`              |
| `[\N][Pro][1Sg][Ill]`              | 
| `[\N][Pro][1Sg][Supe]`             |
| `[\N][Pro][1Sg][Subl]`             |
| `[\N][Pro][1Sg][Transl]`           |
| `[\N][Pro][1Sg][Temp]`             | 
| `[\N][Pro][2Sg][Nom]`              | 
| `[\N][Pro][2Sg][Acc]`              | 
| `[\N][Pro][2Sg][Del]`              |
| `[\N][Pro][2Sg][Ela]`              |
| `[\N][Pro][2Sg][Ins]`              |
| `[\N][Pro][2Sg][Abl]`              |
| `[\N][Pro][2Sg][Ade]`              | 
| `[\N][Pro][2Sg][All]`              | 
| `[\N][Pro][2Sg][Cau]`              |
| `[\N][Pro][2Sg][Dat]`              |
| `[\N][Pro][2Sg][EssFor:ként]`      |
| `[\N][Pro][2Sg][Ess]`              |
| `[\N][Pro][2Sg][Ill]`              | 
| `[\N][Pro][2Sg][Supe]`             |
| `[\N][Pro][2Sg][Subl]`             |
| `[\N][Pro][2Sg][Transl]`           |
| `[\N][Pro][2Sg][Temp]`             | 
| `[\N][Pro][3Sg][Nom]`              | 
| `[\N][Pro][3Sg][Acc]`              | 
| `[\N][Pro][3Sg][Del]`              |
| `[\N][Pro][3Sg][Ela]`              |
| `[\N][Pro][3Sg][Ins]`              |
| `[\N][Pro][3Sg][Abl]`              |
| `[\N][Pro][3Sg][Ade]`              | 
| `[\N][Pro][3Sg][All]`              | 
| `[\N][Pro][3Sg][Cau]`              |
| `[\N][Pro][3Sg][Dat]`              |
| `[\N][Pro][3Sg][EssFor:ként]`      |
| `[\N][Pro][3Sg][Ess]`              |
| `[\N][Pro][3Sg][Ill]`              | 
| `[\N][Pro][3Sg][Supe]`             |
| `[\N][Pro][3Sg][Subl]`             |
| `[\N][Pro][3Sg][Transl]`           |
| `[\N][Pro][3Sg][Temp]`             |
| `[\N][Pro][1][Pl[Nom]`             | 
| `[\N][Pro][1][Pl][Acc]`            | 
| `[\N][Pro][1][Pl][Del]`            |
| `[\N][Pro][1][Pl][Ela]`            |
| `[\N][Pro][1][Pl][Ins]`            |
| `[\N][Pro][1][Pl][Abl]`            |
| `[\N][Pro][1][Pl][Ade]`            | 
| `[\N][Pro][1][Pl][All]`            | 
| `[\N][Pro][1][Pl][Cau]`            |
| `[\N][Pro][1][Pl][Dat]`            |
| `[\N][Pro][1][Pl][EssFor:ként]`    |
| `[\N][Pro][1][Pl][Ess]`            |
| `[\N][Pro][1][Pl][Ill]`            | 
| `[\N][Pro][1][Pl][Supe]`           |
| `[\N][Pro][1][Pl][Subl]`           |
| `[\N][Pro][1][Pl][Transl]`         |
| `[\N][Pro][1][Pl][Temp]`           |
| `[\N][Pro][1][Pl][Ter]`            |
| `[\N][Pro][2][Pl][Nom]`            | 
| `[\N][Pro][2][Pl][Acc]`            | 
| `[\N][Pro][2][Pl][Del]`            |
| `[\N][Pro][2][Pl][Ela]`            |
| `[\N][Pro][2][Pl][Ins]`            |
| `[\N][Pro][2][Pl][Abl]`            |
| `[\N][Pro][2][Pl][Ade]`            | 
| `[\N][Pro][2][Pl][All]`            | 
| `[\N][Pro][2][Pl][Cau]`            |
| `[\N][Pro][2][Pl][Dat]`            |
| `[\N][Pro][2][Pl][EssFor:ként]`    |
| `[\N][Pro][2][Pl][Ess]`            |
| `[\N][Pro][2][Pl][Ill]`            | 
| `[\N][Pro][2][Pl][Supe]`           |
| `[\N][Pro][2][Pl][Subl]`           |
| `[\N][Pro][2][Pl][Transl]`         |
| `[\N][Pro][2][Pl][Temp]`           |
| `[\N][Pro][2][Pl][Ter]`            |
| `[\N][Pro][3][Pl][Nom]`            | 
| `[\N][Pro][3][Pl][Acc]`            | 
| `[\N][Pro][3][Pl][Del]`            |
| `[\N][Pro][3][Pl][Ela]`            |
| `[\N][Pro][3][Pl][Ins]`            |
| `[\N][Pro][3][Pl][Abl]`            |
| `[\N][Pro][3][Pl][Ade]`            | 
| `[\N][Pro][3][Pl][All]`            | 
| `[\N][Pro][3][Pl][Cau]`            |
| `[\N][Pro][3][Pl][Dat]`            |
| `[\N][Pro][3][Pl][EssFor:ként]`    |
| `[\N][Pro][3][Pl][Ess]`            |
| `[\N][Pro][3][Pl][Ill]`            | 
| `[\N][Pro][3][Pl][Supe]`           |
| `[\N][Pro][3][Pl][Subl]`           |
| `[\N][Pro][3][Pl][Transl]`         |
| `[\N][Pro][3][Pl][Temp]`           |
| `[\N][Pro][3][Pl][Ter]`            |
| `[\N][Pro][1Pl][Nom]`              | 
| `[\N][Pro][1Pl][Acc]`              | 
| `[\N][Pro][1Pl][Del]`              |
| `[\N][Pro][1Pl][Ela]`              |
| `[\N][Pro][1Pl][Ins]`              |
| `[\N][Pro][1Pl][Abl]`              |
| `[\N][Pro][1Pl][Ade]`              | 
| `[\N][Pro][1Pl][All]`              | 
| `[\N][Pro][1Pl][Cau]`              |
| `[\N][Pro][1Pl][Dat]`              |
| `[\N][Pro][1Pl][EssFor:ként]`      |
| `[\N][Pro][1Pl][Ess]`              |
| `[\N][Pro][1Pl][Ill]`              | 
| `[\N][Pro][1Pl][Supe]`             |
| `[\N][Pro][1Pl][Subl]`             |
| `[\N][Pro][1Pl][Transl]`           |
| `[\N][Pro][1Pl][Temp]`             |
| `[\N][Pro][1Pl][Ter]`              |
| `[\N][Pro][2Pl][Nom]`              | 
| `[\N][Pro][2Pl][Acc]`              | 
| `[\N][Pro][2Pl][Del]`              |
| `[\N][Pro][2Pl][Ela]`              |
| `[\N][Pro][2Pl][Ins]`              |
| `[\N][Pro][2Pl][Abl]`              |
| `[\N][Pro][2Pl][Ade]`              | 
| `[\N][Pro][2Pl][All]`              | 
| `[\N][Pro][2Pl][Cau]`              |
| `[\N][Pro][2Pl][Dat]`              |
| `[\N][Pro][2Pl][EssFor:ként]`      |
| `[\N][Pro][2Pl][Ess]`              |
| `[\N][Pro][2Pl][Ill]`              | 
| `[\N][Pro][2Pl][Supe]`             |
| `[\N][Pro][2Pl][Subl]`             |
| `[\N][Pro][2Pl][Transl]`           |
| `[\N][Pro][2Pl][Temp]`             |
| `[\N][Pro][2Pl][Ter]`              |
| `[\N][Pro][3Pl][Nom]`              | 
| `[\N][Pro][3Pl][Acc]`              | 
| `[\N][Pro][3Pl][Del]`              |
| `[\N][Pro][3Pl][Ela]`              |
| `[\N][Pro][3Pl][Ins]`              |
| `[\N][Pro][3Pl][Abl]`              |
| `[\N][Pro][3Pl][Ade]`              | 
| `[\N][Pro][3Pl][All]`              | 
| `[\N][Pro][3Pl][Cau]`              |
| `[\N][Pro][3Pl][Dat]`              |
| `[\N][Pro][3Pl][EssFor:ként]`      |
| `[\N][Pro][3Pl][Ess]`              |
| `[\N][Pro][3Pl][Ill]`              | 
| `[\N][Pro][3Pl][Supe]`             |
| `[\N][Pro][3Pl][Subl]`             |
| `[\N][Pro][3Pl][Transl]`           |
| `[\N][Pro][3Pl][Temp]`             |
| `[\N][Pro][3Pl][Ter]`              |
| `[/N\Pro][1Sg][AnP][Nom]`          |
| `[\N][Pro][1Sg][AnP][Acc]`         | 
| `[\N][Pro[1Sg][AnP][Del]`          |
| `[\N][Pro][1Sg][AnP][Ela]`         |
| `[\N][Pro][1Sg][AnP][Ins]`         |
| `[\N][Pro[1Sg][AnP][Abl]`          |
| `[\N][Pro][1Sg][AnP][Ade]`         | 
| `[\N][Pro[1Sg][AnP][All]`          | 
| `[\N][Pro][1Sg][AnP][Cau]`         |
| `[\N][Pro][1Sg][AnP][Dat]`         |
| `[\N][Pro][1Sg][AnP][EssFor:ként]` |
| `[\N][Pro][1Sg][AnP][Ess]`         |
| `[\N][Pro][1Sg][AnP][Ill]`         | 
| `[\N][Pro][1Sg][AnP][Supe]`        |
| `[\N][Pro][1Sg][AnP][Subl]`        |
| `[\N][Pro][1Sg][AnP][Transl]`      |
| `[\N][Pro][1Sg][AnP][Temp]`        |
| `[\N][Pro][1Sg][AnP][Ter]`         |
| `[/N\Pro][2Sg][AnP][Nom]`          |
| `[\N][Pro][2Sg][AnP][Acc]`         | 
| `[\N][Pro[2Sg][AnP][Del]`          |
| `[\N][Pro][2Sg][AnP][Ela]`         |
| `[\N][Pro][2Sg][AnP][Ins]`         |
| `[\N][Pro[2Sg][AnP][Abl]`          |
| `[\N][Pro][2Sg][AnP][Ade]`         | 
| `[\N][Pro[2Sg][AnP][All]`          | 
| `[\N][Pro][2Sg][AnP][Cau]`         |
| `[\N][Pro][2Sg][AnP][Dat]`         |
| `[\N][Pro][2Sg][AnP][EssFor:ként]` |
| `[\N][Pro][2Sg][AnP][Ess]`         |
| `[\N][Pro][2Sg][AnP][Ill]`         | 
| `[\N][Pro][2Sg][AnP][Supe]`        |
| `[\N][Pro][2Sg][AnP][Subl]`        |
| `[\N][Pro][2Sg][AnP][Transl]`      |
| `[\N][Pro][2Sg][AnP][Temp]`        |
| `[\N][Pro][2Sg][AnP][Ter]`         |
| `[/N\Pro][3Sg][AnP][Nom]`          |
| `[\N][Pro][3Sg][AnP][Acc]`         | 
| `[\N][Pro[3Sg][AnP][Del]`          |
| `[\N][Pro][3Sg][AnP][Ela]`         |
| `[\N][Pro][3Sg][AnP][Ins]`         |
| `[\N][Pro[3Sg][AnP][Abl]`          |
| `[\N][Pro][3Sg][AnP][Ade]`         | 
| `[\N][Pro[3Sg][AnP][All]`          | 
| `[\N][Pro][3Sg][AnP][Cau]`         |
| `[\N][Pro][3Sg][AnP][Dat]`         |
| `[\N][Pro][3Sg][AnP][EssFor:ként]` |
| `[\N][Pro][3Sg][AnP][Ess]`         |
| `[\N][Pro][3Sg][AnP][Ill]`         | 
| `[\N][Pro][3Sg][AnP][Supe]`        |
| `[\N][Pro][3Sg][AnP][Subl]`        |
| `[\N][Pro][3Sg][AnP][Transl]`      |
| `[\N][Pro][3Sg][AnP][Temp]`        |
| `[\N][Pro][3Sg][AnP][Ter]`         |
