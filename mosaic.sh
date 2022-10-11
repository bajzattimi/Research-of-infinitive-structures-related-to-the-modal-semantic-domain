#!/bin/bash

# From: https://github.com/dlazesz/mosaic-n-gram-benchmark/blob/main/awk_recursive.sh

mosaic_ngram="mawk -v maxn=$1 -v delimit='#' -v padding_token='DUMMY_WORD' 'function permute(words, actind, maxind, actWLTind, temp) {
                                                                                cWLT = split(words[actind], WLT, delimit);
                                                                                # WLT[2] = \"lemma:\" WLT[2];
                                                                                if (actind < maxind) {
                                                                                    while (actWLTind <= cWLT) {
                                                                                        permute(words, actind + 1, maxind, 1, temp WLT[actWLTind] \" \");
                                                                                        cWLT = split(words[actind], WLT, delimit);
                                                                                        # Distinguish lemmas from words
                                                                                        WLT[2] = \"lemma:\" WLT[2];
                                                                                        actWLTind += 1
                                                                                    }
                                                                                } else {
                                                                                    while (actWLTind <= cWLT) {
                                                                                        print temp WLT[actWLTind]
                                                                                        actWLTind += 1
                                                                                    }
                                                                                }
                                                                            }
                                                                            {
                                                                                # Add padding
                                                                                old_NF = NF;
                                                                                NF += maxn - 1;
                                                                                for (i = old_NF + 1; i <= NF; i++) {
                                                                                    \$i = padding_token;
                                                                                }
                                                                                # Create mosaic n-grams
                                                                                split(\$0, words);
                                                                                for (i = 1; i <= NF - maxn + 1; i++) {
                                                                                    permute(words, i, i + maxn - 1, 1, \"\")
                                                                                }
                                                                            }'"
# echo '<s> Az#az#DET alma#alma#FN.NOM nem#nem#HA esett#esik#IGE.MULT messze#messze#HAT a#a#DET fájától#fa#FN.POSS.TÓL !#!#PUNCT </s>' |
eval "${mosaic_ngram}"
