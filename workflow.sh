#!/bin/bash

set -e
set -o pipefail

# PARAMETERS
# Corpus name. Used all over the workflow
CORP_NAME='mnsz2'
# The extra options for fixing MNSZ2 XML export. Used in step 1 (XML to TSV)
XML_EXTRA_OPTS=('-f' 'latin-2' '-t' 'UTF-8')
# Alternative: Empty array
# XML_EXTRA_OPTS=()
# The address of the emtsv server used. Used in step 2 (reanalyse TSV with emtsv)
EMTSV_SERVER='http://emtsv.elte-dh.hu:5000'
# The filename of the token/sentence filter and tag substitution configuration.
#  Used in step 3 (Substitute tags) and 4 (Create clauses)
FILTER_PARAMS_YAML='filter_params.yaml'
# The number of tokens to allow outwards from FIN-INF if not finding a "[/Punct]" tag. Used in step 4 (Create clauses)
LEFT_WINDOW=3
RIGHT_WINDOW=3
# The sort options for creating and counting mosaic n-grams (step 6) (Used in parallel with the next sort and pigz!)
NPROC=40
MEM_USE=40G
TMP_DIR='/data/aramis/tmp'
# The sort options for ranking counted mosaic n-grams (step 6) (Used in parallel with the previous sort and pigz!)
NPROC2=5
MEM_USE2='10G'
TMP_DIR2='/data/aramis/tmp'
# The minimum frequency of mosaic n-grams to avoid being discarded as too rare.
#  Used in step 7 (Create mosaic n-gram classes)and 8 (The BOW variant of create mosaic n-gram classes)
MOSAIC_FREQ_THRESHOLD=25


# 1. XML to TSV format
## Notice the extra options for fixing MNSZ2 (they can be ommitted with newer versions of Sketch Engine)
rm -rf "${CORP_NAME}_tsv"
mkdir -p "${CORP_NAME}_tsv"
./venv/bin/python xml_to_emtsv.py -i "${CORP_NAME}_xml" -o "${CORP_NAME}_tsv" "${XML_EXTRA_OPTS[@]}"

# 2. Reanalyse TSV with emtsv (keep tokenisation)
rm -rf "${CORP_NAME}_emtsv"
mkdir -p "${CORP_NAME}_emtsv"
./venv/bin/python emtsv_client.py -s ${EMTSV_SERVER} -m morph pos -k form lemma xpostag \
    -i "${CORP_NAME}_tsv" -o "${CORP_NAME}_emtsv"
# Note: There is an alternative if one wants to keep the annotation
# ./venv/bin/python split_sketch_fields.py -i tmk_concordance.tsv -o tmk_concordance_emtsv.tsv 2> tmk_split_errors.log

# 3. Substitute tags from config, (optionally) keep duplicates, (optionally) lowercase sentance start tokens
#  by default both options are turned off
rm -rf "${CORP_NAME}_emtsv_subs"
mkdir -p "${CORP_NAME}_emtsv_subs"
./venv/bin/python substitute_tags.py -f "${FILTER_PARAMS_YAML}" --lower-sent-start \
    -i "${CORP_NAME}_emtsv" -o "${CORP_NAME}_emtsv_subs"

# 4. Create clauses (and apply token filters)
## File by file
rm -rf "${CORP_NAME}_emtsv_clauses" "${CORP_NAME}_emtsv_clauses.tsv"
mkdir -p "${CORP_NAME}_emtsv_clauses"
time (for fname in "${CORP_NAME}_emtsv_subs/"*; do
          echo "REPORT: $fname" 1>&2
          ./venv/bin/python fin_inf_window.py -l"${LEFT_WINDOW}" -r"${RIGHT_WINDOW}" -f "${FILTER_PARAMS_YAML}" \
              -i "$fname" -o "${CORP_NAME}_emtsv_clauses/$(basename "$fname")"
      done 2> "${CORP_NAME}_emtsv_clauses.log")
## Merged into one file
### Must clean individual files from Sketch Engine query info and TSV header before processing
time (echo "REPORT: merged.tsv" 1>&2
      cat "${CORP_NAME}_emtsv_subs/"* | grep -Fv '# corpus: ' | grep -Fv '# hits: ' | grep -Fv '# query: ' | \
          awk '{ if (NR == 1 || $0 != "form\tlemma\txpostag") print $0}' | \
          ./venv/bin/python fin_inf_window.py -l"${LEFT_WINDOW}" -r"${RIGHT_WINDOW}" -f "${FILTER_PARAMS_YAML}" \
              -o "${CORP_NAME}_emtsv_clauses/merged.tsv" 2> "${CORP_NAME}_emtsv_clauses_merged.log")
## NOTE: There are alternative window creation methods
# ./venv/bin/python punct_window.py -i ${CORP_NAME}_emtsv_subs.tsv -o ${CORP_NAME}_emtsv_clauses.tsv \
#     -f "${FILTER_PARAMS_YAML}" 2> ${CORP_NAME}_emtsv_clauses_merged.log

# 5. Create SPL form of the remaining sentences, tokens and fields
rm -rf "${CORP_NAME}_emtsv_clauses_spl"
mkdir -p "${CORP_NAME}_emtsv_clauses_spl"
time (for fname in "${CORP_NAME}_emtsv_clauses/"*; do
          grep "^# clause_SPL:" "$fname" | sed 's/^# clause_SPL: //' \
              > "${CORP_NAME}_emtsv_clauses_spl/$(basename "$fname")"
      done)

# 6. Create and count mosaic n-grams (by separated by the size of the input)
rm -rf "${CORP_NAME}_mosaic_{2..9}"
THIS_SCRIPT_DIR=$( dirname -- "$( readlink -f -- "$0" )" )
for i in $(seq 9 -1 2); do
    echo "$i"
    mkdir -p "${CORP_NAME}_mosaic_${i}"
    time (for fname in "${CORP_NAME}_emtsv_clauses_spl/"*; do
              awk -v N="${i}" '{if (NF == $N) print $0}' "$fname" | "${THIS_SCRIPT_DIR}/"mosaic.sh "${i}" | \
                  LC_ALL=C.UTF-8 sort --parallel="${NPROC}" -S "${MEM_USE}" -T "${TMP_DIR}" | uniq -c | \
                  LC_ALL=C.UTF-8 sort -nr -S"${MEM_USE2}" --parallel="${NPROC2}" -T "${TMP_DIR2}" | \
                  pigz > "${CORP_NAME}_mosaic_${i}/$(basename "$fname".gz)"
          done)
done

# 7. Create mosaic n-gram classes and keep only frequent ones (>=MOSAIC_FREQ_THRESHOLD occurence)
#  (Reuse the output of step 4 (window creation))
rm -rf "${CORP_NAME}_mosaic"{2..9}"filtered_${MOSAIC_FREQ_THRESHOLD}" \
    "${CORP_NAME}_mosaic_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip"
time (for i in $(seq 2 9); do
          echo "$i"
          mkdir -p "${CORP_NAME}_mosaic_${i}"
          for fname in "${CORP_NAME}_emtsv_clauses/"*; do
              echo "$i $(basename "$fname")"
              ./venv/bin/python mosaic_filter.py -m "${CORP_NAME}_mosaic_${i}/$(basename "$fname".gz)" \
                  -f "${MOSAIC_FREQ_THRESHOLD}" -i "$fname" | \
              pigz > "${CORP_NAME}_mosaic_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}/$(basename "$fname".gz)"
          done
      done)
## Zip the results
zip -r "${CORP_NAME}_mosaic_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip" \
    "${CORP_NAME}_mosaic"{2..9}"filtered_${MOSAIC_FREQ_THRESHOLD}"

# 8. The BOW variant of create mosaic n-gram classes and keep only frequent ones (>=MOSAIC_FREQ_THRESHOLD occurence)
rm -rf "${CORP_NAME}_bow"{2..9}"filtered_${MOSAIC_FREQ_THRESHOLD}" \
    "${CORP_NAME}_bow_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip"
time (for i in $(seq 2 9); do
          for fname in "${CORP_NAME}_emtsv_clauses/"*; do
              echo "$i $(basename "$fname")"
              ./venv/bin/python mosaic_filter_bow.py -m "${CORP_NAME}_bow_${i}/$(basename "$fname".gz)" \
                   -f ${MOSAIC_FREQ_THRESHOLD} -i "$fname" | \
              pigz > "${CORP_NAME}_bow_${i}_filtered_${MOSAIC_FREQ_THRESHOLD}/$(basename "$fname".gz)"
          done
      done)
## Zip the results
zip -r "${CORP_NAME}_bow_2-9_filtered_${MOSAIC_FREQ_THRESHOLD}.zip" \
    "${CORP_NAME}_bow_"{2..9}"_filtered_${MOSAIC_FREQ_THRESHOLD}"
