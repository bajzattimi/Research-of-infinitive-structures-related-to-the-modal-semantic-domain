import re


def main():
    input_file_path = "test_akar_5_webkorpusz.txt"
    output_file_path1 = "output.txt"
    output_file_path2 = "output2.txt"

    regex_patterns = [(r'\[\/Adj\]\[Nom\] \[\/N\]\[Acc\]', r'\[\/N\]\[Nom\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]')]
    regex_patterns2 = [(r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]')]

    try:
        with open(input_file_path, 'r', encoding='utf-8') as input_file, \
             open(output_file_path1, 'w+', encoding='utf-8') as output_file_1, \
             open(output_file_path2, 'w+', encoding='utf-8') as output_file_2:

            result_lines1 = []
            result_lines2 = []

            for line in input_file:
                modified_line = line
                for pattern, replacement in regex_patterns:
                    modified_line = re.sub(pattern, replacement, modified_line)
                result_lines1.append(modified_line)

            for line in result_lines1:
                modified_line = line
                for pattern, replacement in regex_patterns2:
                    modified_line = re.sub(pattern, replacement, modified_line)
                result_lines2.append(modified_line)

            output_file_1.writelines(result_lines1)
            output_file_2.writelines(result_lines2)

        print("Code has completed the replacements")

    except FileNotFoundError:
        print(f"We don't find the file: {input_file_path}")


if __name__ == "__main__":
    main()