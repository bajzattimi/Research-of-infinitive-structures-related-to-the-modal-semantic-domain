# Unzip
unzip mhc_letokenizált.zip -d mhc_letokenizált
# Cat and add header
cat mhc_letokenizált/mhc/doc_{0..2136}.tsv | sed '1s/.*/ID\tORIG\tNORM\tform\tlemma\tORIGPOS/' > tmk_cat.tsv
# Filter and convert to e-magyar tags
./venv/bin/python tmk2emtsv_tags.py -f filter_tmk_to_emagyar.yaml -i tmk_cat.tsv -o tmk_cat_subs.tsv 2> tmk_to_emagyar_errors.txt
cat tmk_cat_subs.tsv | cut -f4,5,7 | sed '1s/.*//; s/^$/<\/s>\n<s>/g' | awk -F '\t' 'BEGIN {last_line="<doc>"}
                                                                                     NR>1 {print last_line; last_line=$0}
                                                                                     END {print "</doc>"}' > tmk_vert.tsv
