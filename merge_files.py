
input_files = ['atalakitott_akar_webkorpusz_3gram.txt', 'atalakitott_akar_webkorpusz_4gram.txt', 'atalakitott_akar_webkorpusz_5gram.txt', 'atalakitott_akar_webkorpusz_6gram.txt', 'atalakitott_akar_webkorpusz_7gram.txt', 'atalakitott_akar_webkorpusz_8gram.txt']
output_file = 'merged_output_akar_webkorpusz.txt'

def merge_files(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())

merge_files(input_files, output_file)
print("Files merged successfully!")