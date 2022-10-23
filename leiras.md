# 1. Mozaikok átteknitése

A mosaic mappában a korpusz mappáját kiválasztva a megfelelő mintafájlt kiválasztjuk és (mivel gz végű) a zcat paraccsal írjuk ki (nem a sima cat paranccsal).
A less paranccsal tudjunk föl le görgetni kiírás közben.

```bash
zcat mosaic/mnsz2_pos/akar_fni_610836.tsv.gz | less
```

vagy

```bash
zless mosaic/mnsz2_pos/akar_fni_610836.tsv.gz
```

# 2. A mozaikok szűrése

A kötőszó és ahatározó szó kategória túl tág, ezért kiszűrjük azokat a mozaikokat, amik tartalmazzák.
Az egrep-et használjunk (nem a sima grep-et), mert az e-s változatban lehet uniózni a |-jellel.

```bash
zcat mosaic/mnsz2_pos/akar_fni_610836.tsv.gz | egrep "Cnj|Adv" | less
```

HA a mi specifikus mozaikunkat keressük a listában, akkor fgrep-et használunk.
Az fgrep (szemben a renges greppel és az egreppel) nem regkifeket illeszt, hanem full-string match-et csinál (nem kell escapelni a szögletes zárójeleket)

```bash
zcat mosaic/mnsz2_pos/akar_fni_610836.tsv.gz | fgrep "lemma:és nem is lemma:akar [/V][Inf]" | less
```

# 3. Egyadott mozaikra példák kiíratása

Az out_part mappában lévő fájlokat kellnézni, a korpusz mappáját kiválasztani és azon belül a minta fájlját.
Ez lesz az -i paraméter. (A korpusz mappáját is lehet használni, csak lassabb.)
Az -m paraméterbe idézőjelek közé (!!!) beírjuk a mozaikot, amire példákat szeretnénk látni.
Nem muszáj a listából származnia, minden, ami a korpuszban van és azonos hosszúságú, arra tud példát hozni.
(Valószínűleg ott van a listában az a mozaik is, csak kevésbé gyakori valamiért.)
A példáknál a duplikációkat is kiírja! Erre figyelni kell.

```bash
./venv/bin/python mosaic_lookup.py -i out_part/mnsz2_pos/akar_fni_610836.tsv -m "[/Adj][Nom] [/Adj][Nom] [/N][Acc] lemma:akar [/V][Inf]" | less
```
