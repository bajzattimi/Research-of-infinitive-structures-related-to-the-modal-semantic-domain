# Create clauses (fitered)
rm -rf out_part_filtered/mnsz2_pos/* out_part_filtered/mnsz2_filtered.log
time (for fname in mnsz2_pos/*; do echo "REPORT: $fname" 1>&2 ; ./venv/bin/python window.py -i "$fname" -l3 -r3 -f filter_params.yaml -o "out_part_filtered/mnsz2_pos/`basename "$fname"`"; done 2> out_part_filtered/mnsz2_filtered.log)

# Create SPL format
rm -rf mnsz2_filtered_spl/
mkdir mnsz2_filtered_spl
time (for fname in out_part_filtered/mnsz2_pos/*; do cat "$fname" | grep "^#  clause_SPL:" | sed 's/^#  clause_SPL: //' > "mnsz2_filtered_spl/`basename "$fname"`"; done)

# Create and count mosaic n-grams
rm -rf mosaic_mnsz2_filtered_{2..9}
mkdir mosaic_mnsz2_filtered_{2..9}
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 9) print $0}' | ./mosaic.sh 9 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_9/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 8) print $0}' | ./mosaic.sh 8 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_8/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 7) print $0}' | ./mosaic.sh 7 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_7/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 6) print $0}' | ./mosaic.sh 6 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_6/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 5) print $0}' | ./mosaic.sh 5 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_5/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 4) print $0}' | ./mosaic.sh 4 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_4/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 3) print $0}' | ./mosaic.sh 3 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_3/`basename "$fname".gz`"; done)
time (for fname in mnsz2_filtered_spl/*; do cat "$fname" | awk '{if (NF == 2) print $0}' | ./mosaic.sh 2 | LC_ALL=C.UTF-8 sort --parallel=40 -S 40G -T /data/tmp | uniq -c | sort -nr -S10G --parallel=5 | pigz > "mosaic_mnsz2_filtered_2/`basename "$fname".gz`"; done)

# Create mosaic n-gram classes and keep only frequent ones (>25 occurence)
rm -rf mosaic_mnsz2_filtered_{2..10}_filtered_25
mkdir mosaic_mnsz2_filtered_{2..10}_filtered_25
time (for i in `seq 2 9`; do for fname in out_part_filtered/mnsz2_pos/*; do echo "$i `basename "$fname"`"; cat "$fname" | ./venv/bin/python mosaic_filter.py -m "mosaic_mnsz2_filtered_${i}/`basename "$fname".gz`" -f 25 | pigz > "mosaic_mnsz2_filtered_${i}_filtered_25/`basename "$fname".gz`"; done; done)
