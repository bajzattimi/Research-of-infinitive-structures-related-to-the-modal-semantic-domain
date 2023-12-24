# Unzip
unzip mhc_letokenizált.zip -d mhc_letokenizált
# Cat and add header (suppress consecutive empty lines)
cat mhc_letokenizált/mhc/doc_{0..2136}.tsv | sed '1s/.*/ID\tORIG\tNORM\tform\tlemma\tORIGPOS/' | cat -s > tmk_cat.tsv
# Filter and convert to e-magyar tags
./venv/bin/python tmk2emtsv_tags.py -f filter_tmk_to_emagyar.yaml -i tmk_cat.tsv -o tmk_cat_emtsv.tsv \
    2> tmk2emtsv_errors.txt
cut -f4,5,7 < tmk_cat_subs.tsv | sed '1s/.*//; s/^$/<\/s>\n<s>/g' | \
    awk -F '\t' 'BEGIN {last_line="<doc>"}
                 NR>1 {print last_line; last_line=$0}
                 END {print "</doc>"}' > tmk_vert.tsv

# Create TMK NoSke registry file
# Note: Bash "here document" feature
cat > tmk_registry <<END_OF_FILE
MAINTAINER "nobody@nowhere.notld"
INFO "TMK W/ e-magyar tagset"
NAME "TMK corpus with e-magyar tagset"
PATH tmk
ENCODING "UTF-8"
LANGUAGE "Hungarian"

PATH   '/corpora/tmk/indexed/'
VERTICAL  '/corpora/tmk/vertical/tmk_vert.tsv'

INFOHREF "XXX"
TAGSETDOC "http://e-magyar.hu/hu/textmodules/emmorph_codelist"

FULLREF "doc.file,doc.n"

ATTRIBUTE   word {
        TYPE "FD_FGD"
}

ATTRIBUTE   lemma {
        TYPE "FD_FGD"
}

ATTRIBUTE   tag {
        TYPE "FD_FGD"
}

ATTRIBUTE lc {
  LABEL      "word:lowercase"
  DYNAMIC    utf8lowercase
  DYNLIB     internal
  ARG1       "C"
  FUNTYPE    s
  FROMATTR   word
  TYPE       index
  TRANSQUERY yes
}

ATTRIBUTE lemma_lc {
  LABEL      "lemma:lowercase"
  DYNAMIC    utf8lowercase
  DYNLIB     internal
  ARG1       "C"
  FUNTYPE    s
  FROMATTR   lemma
  TYPE       index
  TRANSQUERY yes
}

STRUCTURE doc {
  ATTRIBUTE file
  ATTRIBUTE wordcount
  ATTRIBUTE n
}

STRUCTURE s
END_OF_FILE