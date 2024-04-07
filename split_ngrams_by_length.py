def split_results_by_ngram_length(input_file):
    ngram_files = {}

    with open(input_file, 'r') as file:
        for line in file:
            frequency, ngram = line.strip().split('\t')
            n = len(ngram.split())
            if n not in ngram_files:
                ngram_files[n] = []
            ngram_files[n].append((frequency, ngram))

    for n, ngrams in ngram_files.items():
        output_file = f"{n}_gram_results.txt"
        with open(output_file, 'w') as file:
            for frequency, ngram in ngrams:
                file.write(f"{frequency}\t{ngram}\n")


split_results_by_ngram_length('output_file.txt')