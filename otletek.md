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
- 
## Az n-gramok optimális hossza

- A 3-ngram túl kicsi, bagyon általános mintázatok (jellemzően igekötő, névszói 
igemódosító vagy *nem* tagadószó kerül a szerkezet elejére.), de érdemes bent hagyni, 
mert nem tűnik hibásnak
- 


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
- `[/Adj][_Manner/Adv]` melléknévből képzett határozó. Megtartanám egyelőre a címkét, nem vonnám össze más 
relációval. A sima `Adv` címkével ellátott elemeknék specifikusabb.
- `[/Adj][Acc]` felvethető, hogy akár egyben kezelhető lehetne az `[/N][Acc]` kategóriával, mivel itt
főnévként viselkednek ezek. De ha nem szeretnénk túláltalánosítani, akkor lehet, hogy érdemes meghagyni. 
Viszont most először talán érdemes lenne egy halmazként kezelni őket. Az alábbi táblázat összefoglalja azt, 
hogy melyik más esefekre áll még ez fenn. 

| `[/N]` ragozott alakjainak mintájára kezelhető | `[/N][Pl]` ragozott alakjainak mintájára kezelhető |
|----------------------------------|----------------------------------------------------|
| `[/Adj][Acc]`                    | `[/Adj][Pl][Acc]`                                  |
| `[/Adj][Dat]`                    | `[/Adj][Pl][Dat]`                                  |
| `[/Adj][Subl]`                   | `[/Adj][Pl][Subl]`                                 |
| `[/Adj][Transl]`                 | `[/Adj][Pl][Transl]`                               |

- `[/Adj|Pro]`esetében elég lehet a címke megtartása. Ennek mintájára lehet kezelhető a mutatónévmás
ragozott melléknévként kidolgozott példányai is. 

| `[/Adj\Pro]` ragozott alakjainak mintájára kezelhető | `[/Adj\Pro][Pl]` ragozott alakjainak mintájára kezelhető |
|------------------------------------------------------|------------------------------------------------------|
| `[/Adj\Pro][Acc]`                                    | `[/Adj\Pro][Acc]`                                    |

- `[/Adv|Pro]`esetében elég lehet a címke megtartása. Ennek mintájára lehet kezelhető a mutatónévmás
ragozott melléknévként kidolgozott példányai is. 

| `[/Adv\Pro]` mintájára kezelhető alakok | 
|-----------------------------------------|
| `[/Adv\Pro\Rel]`                        | 
| `[/Adv\Pro\Int]`                        | 



