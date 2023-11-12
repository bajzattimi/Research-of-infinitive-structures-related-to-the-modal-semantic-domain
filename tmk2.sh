./venv/bin/python xml_to_emtsv.py -i concordance_tmk_20231112202940.xml -o concordance_tmk.tsv

./venv/bin/python split_sketch_fields.py -i concordance_tmk.tsv -o concordance_tmk_splitted.tsv 2> tmk_split_errors.log

./venv/bin/python filter_window.py -i concordance_tmk_splitted.tsv -o concordance_tmk_filtered_clauses.tsv -f filter_params.yaml 2> filter_window.log
grep "^#  clause_SPL:" concordance_tmk_filtered_clauses.tsv | sed 's/^#  clause_SPL: //' > tmk_spl_clauses.tsv

for i in $(seq 9 -1 2); do
    echo "$i"
    time (awk "{if (NF == ${i}) print \$0}" tmk_spl_clauses.tsv | ./mosaic.sh "${i}" | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/aramis/tmp | uniq -c | sort -nr -S10G --parallel=5 -T /data/aramis/tmp | pigz > "mosaic_tmk_filtered_${i}.gz")
done

time (for i in $(seq 2 9); do
    echo "$i"
    ./venv/bin/python mosaic_filter.py -m "mosaic_tmk_filtered_${i}.gz" -f 2 < concordance_tmk_filtered_clauses.tsv | pigz > "mosaic_tmk_filtered_${i}_thres_2.gz"
done)

time (for i in $(seq 2 9); do
    echo "$i"
    ./venv/bin/python mosaic_filter_bow.py -m "mosaic_tmk_filtered_${i}.gz" -f 2 < concordance_tmk_filtered_clauses.tsv | pigz > "mosaic_tmk_filtered_${i}_thres_2_bow.gz"
done)
