import os
import re
from collections import defaultdict

folder_path = "mannheim_ngram/spok/spok_merged_proc"

lemma_pattern = re.compile(r'lemma:[^\s\]]+')

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        input_path = os.path.join(folder_path, filename)

        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        line_counter = defaultdict(int)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                count_str, rest = line.split(maxsplit=1)
                count = int(count_str)
                cleaned_rest = lemma_pattern.sub('lemma', rest)
                line_counter[cleaned_rest] += count
            except ValueError:
                continue

        sorted_lines = sorted(line_counter.items(), key=lambda x: x[1], reverse=True)

        base_name = os.path.splitext(filename)[0]
        new_filename = base_name + "_lemma_manipulated.txt"
        output_path = os.path.join(folder_path, new_filename)

        with open(output_path, 'w', encoding='utf-8') as out_file:
            for text, count in sorted_lines:
                out_file.write(f"{count}\t{text}\n")

print("The process is completed.")
