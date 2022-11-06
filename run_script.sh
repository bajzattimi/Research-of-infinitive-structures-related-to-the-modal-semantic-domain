if [[ "$#" -ne 1 ]]; then
echo "Provide the corpus name!"
fi

CORP_NAME=$1

# Create clauses (fitered)
rm -rf out_part_filtered/${CORP_NAME}_pos/* out_part_filtered/${CORP_NAME}_filtered.log
time (for fname in ${CORP_NAME}_pos/*; do echo "REPORT: $fname" 1>&2 ; ./venv/bin/python window.py -i "$fname" -l3 -r3 -f filter_params.yaml -o "out_part_filtered/${CORP_NAME}_pos/`basename "$fname"`"; done 2> out_part_filtered/${CORP_NAME}_filtered.log)

# Create SPL format
rm -rf ${CORP_NAME}_filtered_spl/
mkdir ${CORP_NAME}_filtered_spl
time (for fname in out_part_filtered/${CORP_NAME}_pos/*; do cat "$fname" | grep "^#  clause_SPL:" | sed 's/^#  clause_SPL: //' > "${CORP_NAME}_filtered_spl/`basename "$fname"`"; done)

# Create and count mosaic n-grams
rm -rf mosaic_${CORP_NAME}_filtered_{2..9}
mkdir mosaic_${CORP_NAME}_filtered_{2..9}
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 9) print $0}' | ./mosaic.sh 9 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_9/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 8) print $0}' | ./mosaic.sh 8 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_8/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 7) print $0}' | ./mosaic.sh 7 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_7/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 6) print $0}' | ./mosaic.sh 6 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_6/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 5) print $0}' | ./mosaic.sh 5 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_5/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 4) print $0}' | ./mosaic.sh 4 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_4/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 3) print $0}' | ./mosaic.sh 3 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_3/`basename "$fname".gz`"; done)
time (for fname in ${CORP_NAME}_filtered_spl/*; do cat "$fname" | awk '{if (NF == 2) print $0}' | ./mosaic.sh 2 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_${CORP_NAME}_filtered_2/`basename "$fname".gz`"; done)

# Create mosaic n-gram classes and keep only frequent ones (>25 occurence)
rm -rf mosaic_${CORP_NAME}_filtered_{2..10}_filtered_25
mkdir mosaic_${CORP_NAME}_filtered_{2..10}_filtered_25
time (for i in `seq 2 9`; do for fname in out_part_filtered/${CORP_NAME}_pos/*; do echo "$i `basename "$fname"`"; cat "$fname" | ./venv/bin/python mosaic_filter.py -m "mosaic_${CORP_NAME}_filtered_${i}/`basename "$fname".gz`" -f 25 | pigz > "mosaic_${CORP_NAME}_filtered_${i}_filtered_25/`basename "$fname".gz`"; done; done)

# Zip the results
rm mosaic_m${CORP_NAME}_filtered_all_filt_25.zip
zip -r mosaic_${CORP_NAME}_filtered_all_filt_25.zip mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25
