./venv/bin/python xml_to_emtsv.py -i concordance_tmk_20231112202940.xml -o tmk_concordance.tsv

./venv/bin/python split_sketch_fields.py -i tmk_concordance.tsv -o tmk_concordance_emtsv.tsv 2> tmk_split_errors.log

./venv/bin/python substitute_tags.py -f filter_params.yaml --lower-sent-start --keep-duplicates -i tmk_concordance_emtsv.tsv -o tmk_concordance_emtsv_subs.tsv

./venv/bin/python punct_window.py -i tmk_concordance_emtsv_subs.tsv -o tmk_concordance_emtsv_clauses.tsv -f filter_params.yaml 2> punct_window.log
grep "^# clause_SPL:" tmk_concordance_emtsv_clauses.tsv | sed 's/^# clause_SPL: //' > tmk_concordance_spl_clauses.tsv


THIS_SCRIPT_DIR=$( dirname -- "$( readlink -f -- "$0" )" )
for i in $(seq 9 -1 2); do
    echo "$i"
    time (awk -v N="${i}" '{if (NF == N) print $0}' tmk_concordance_spl_clauses.tsv | \
          "${THIS_SCRIPT_DIR}/"mosaic.sh "${i}" | \
          LC_ALL=C.UTF-8 sort --parallel=2 -S 1G -T /tmp | uniq -c | \
          LC_ALL=C.UTF-8 sort -nr -S1G --parallel=2 -T /tmp | \
          pigz > "tmk_mosaic_${i}.gz")
done

time (for i in $(seq 2 9); do
          echo "$i"
          ./venv/bin/python mosaic_filter.py -m "tmk_mosaic_${i}.gz" -f 2 -i tmk_concordance_emtsv_clauses.tsv | \
              pigz > "tmk_mosaic_${i}_filtered_2.gz"
      done)

time (for i in $(seq 2 9); do
          echo "$i"
          ./venv/bin/python mosaic_filter_bow.py -m "tmk_mosaic_${i}.gz" -f 2 < tmk_concordance_emtsv_clauses.tsv | \
              pigz > "tmk_bow_${i}_filtered_2.gz"
      done)
