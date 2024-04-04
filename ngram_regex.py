import re


def main():
    input_file_path = "test.txt"
    output_file_path1 = "output.txt"
    output_file_path2 = "output2.txt"

    regex_patterns = [(r'\[\/Adj\]\[Nom\] \[\/N\]\[Acc\]', r'\[\/N\]\[Nom\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom]( egy | \[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]')]
    regex_patterns2 = [(r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]')]

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path1, 'r', encoding='utf-8') as output_file_1, \
             open(output_file_path2, 'r', encoding='utf-8') as output_file_2:

            for line in input_file:
                for pattern, replacement in regex_patterns:
                    line = re.sub(pattern, replacement, line)
                output_file_1.write(line)
            for line in output_file_1:
                for pattern, replacement in regex_patterns:
                    line = re.sub(pattern, replacement, line)
                output_file_1.write(line)
            for line in output_file_1:
                for pattern, replacement in regex_patterns2:
                    line = re.sub(pattern, replacement, line)
                output_file_2.write(line)

        print("Code has completed the replacements")

    except FileNotFoundError:
        print(f"We don't find the file: {input_file_path}")


if __name__ == "__main__":
    main()

