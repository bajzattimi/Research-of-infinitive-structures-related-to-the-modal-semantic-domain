
input_files = ['atalakitott_hajlando_mnsz_3gram.txt', 'atalakitott_hajlando_mnsz_4gram.txt', 'atalakitott_hajlando_mnsz_5gram.txt', 'atalakitott_hajlando_mnsz_6gram.txt', 'atalakitott_hajlando_mnsz_7gram.txt', 'atalakitott_hajlando_mnsz_8gram.txt']
output_file = 'merged_output_hajlando_mnsz.txt'


def merge_files(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())


merge_files(input_files, output_file)
print("Files merged successfully!")