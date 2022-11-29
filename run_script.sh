if [[ "$#" -ne 1 ]]; then
echo "Provide the corpus name!"
fi

CORP_NAME=$1

# Create clauses (fitered)
rm -rf out_part_filtered/${CORP_NAME}_pos/* "out_part_filtered/${CORP_NAME}_filtered.log"
mkdir -p "out_part_filtered/${CORP_NAME}_pos/"
time (for fname in ${CORP_NAME}_pos/*; do echo "REPORT: $fname" 1>&2 ; ./venv/bin/python window.py -i "$fname" -l3 -r3 -f filter_params.yaml -o "out_part_filtered/${CORP_NAME}_pos/$(basename "$fname")"; done 2> "out_part_filtered/${CORP_NAME}_filtered.log")

# Create SPL format
rm -rf "${CORP_NAME}_filtered_spl/"
mkdir "${CORP_NAME}_filtered_spl"
time (for fname in out_part_filtered/${CORP_NAME}_pos/*; do grep "^#  clause_SPL:" "$fname" | sed 's/^#  clause_SPL: //' > "${CORP_NAME}_filtered_spl/$(basename "$fname")"; done)
rm -rf "${CORP_NAME}_filtered_spl/merged.tsv"
time (for fname in out_part_filtered/${CORP_NAME}_pos/*; do grep "^#  clause_SPL:" "$fname" | sed 's/^#  clause_SPL: //' >> "${CORP_NAME}_filtered_spl/merged.tsv"; done)

# Create and count mosaic n-grams
rm -rf mosaic_${CORP_NAME}_filtered_{2..9}
mkdir mosaic_${CORP_NAME}_filtered_{2..9}
for i in $(seq 9 -1 2); do
    echo "$i"
    time (for fname in ${CORP_NAME}_filtered_spl/*; do awk "{if (NF == ${i}) print \$0}" "$fname" | ./mosaic.sh "${i}" | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 -T /data/tmp | pigz > "mosaic_${CORP_NAME}_filtered_${i}/$(basename "$fname".gz)"; done)
done

# Create mosaic n-gram classes and keep only frequent ones (>25 occurence)
rm -rf mosaic_${CORP_NAME}_filtered_{2..10}_filtered_25
mkdir mosaic_${CORP_NAME}_filtered_{2..10}_filtered_25
time (for i in $(seq 2 9); do for fname in out_part_filtered/${CORP_NAME}_pos/*; do echo "$i $(basename "$fname")"; ./venv/bin/python mosaic_filter.py -m "mosaic_${CORP_NAME}_filtered_${i}/$(basename "$fname".gz)" -f 25 < "$fname" | pigz > "mosaic_${CORP_NAME}_filtered_${i}_filtered_25/$(basename "$fname".gz)"; done; done)

# Zip the results
rm "mosaic_${CORP_NAME}_filtered_all_filt_25.zip"
zip -r "mosaic_${CORP_NAME}_filtered_all_filt_25.zip" mosaic_${CORP_NAME}_filtered_{2..9}_filtered_25
