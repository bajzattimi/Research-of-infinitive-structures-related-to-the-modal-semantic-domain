import os
def transform_tsv(file_path, output_file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as input_file, \
                open(output_file_path, 'w', encoding='utf-8') as output_file:
            for line in input_file:
                line = line.strip()
                if line:
                    # Split at the first space to separate the number from the rest
                    parts = line.split(maxsplit=1)
                    if len(parts) < 2:
                        print(f"Skipping malformed line: {line}")
                        continue

                    number, rest_of_line = parts
                    transformed_line = f"{number}\t{rest_of_line}"
                    output_file.write(transformed_line + '\n')
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def process_files(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.tsv')]
    for file_name in files:
        input_file_path = os.path.join(directory, file_name)
        output_file_path = os.path.join(directory, f"transformed_{file_name}")
        transform_tsv(input_file_path, output_file_path)
        print(f"Processed {file_name}")


if __name__ == "__main__":
    directory = 'mannheim_ngram/spok/spok_vagyik'  # Replace with your directory path
    process_files(directory)