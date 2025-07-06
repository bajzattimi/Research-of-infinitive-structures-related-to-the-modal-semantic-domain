import os

def extract_main_sets(input_filepath, output_filepath):
    with open(input_filepath, 'r', encoding='utf-8') as infile, open(output_filepath, 'w', encoding='utf-8') as outfile:
        for line in infile:
            if not line.startswith("\t"):
                outfile.write(line)


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.tsv'):
            input_filepath = os.path.join(directory, filename)
            output_filename = f"{os.path.splitext(filename)[0]}_fohalmaz.tsv"
            output_filepath = os.path.join(directory, output_filename)

            extract_main_sets(input_filepath, output_filepath)
            print(f"Processed {filename} to {output_filename}")


directory = 'mannheim_ngram/lit/lit_mosaic_3_filtered_2'
process_directory(directory)

