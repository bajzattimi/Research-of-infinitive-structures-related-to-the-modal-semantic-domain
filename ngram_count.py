def merge_duplicate_ngrams(input_file, output_file):
    ngram_dict = {}

    with open(input_file, 'r') as file:
        for line in file:
            frequency, ngram = line.strip().split('\t')
            frequency = int(frequency)
            if ngram in ngram_dict:
                ngram_dict[ngram] += frequency
            else:
                ngram_dict[ngram] = frequency

    sorted_ngrams = sorted(ngram_dict.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w') as file:
        for ngram, frequency in sorted_ngrams:
            file.write(f"{frequency}\t{ngram}\n")


merge_duplicate_ngrams('merged_output_tud_mnsz.txt', 'output_file.txt')