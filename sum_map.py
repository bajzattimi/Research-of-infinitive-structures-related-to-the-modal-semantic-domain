import os
from collections import defaultdict

folder_path = "mannheim_ngram\merged_9"

total_counter = defaultdict(int)

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        input_path = os.path.join(folder_path, filename)

        with open(input_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    count_str, rest = line.split(maxsplit=1)
                    count = int(count_str)
                    total_counter[rest] += count
                except ValueError:
                    continue

sorted_total = sorted(total_counter.items(), key=lambda x: x[1], reverse=True)

output_path = os.path.join(folder_path, "merged_total.txt")

with open(output_path, 'w', encoding='utf-8') as out_file:
    for text, count in sorted_total:
        out_file.write(f"{count} {text}\n")

print(f"You can find the results: {output_path}")
