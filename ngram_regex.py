import re


def main():
    input_file_path = "test_akar_5_webkorpusz.txt"
    output_file_path1 = "output.txt"
    output_file_path2 = "output2.txt"

    regex_patterns = [
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Subl\]', r'\[\/N\]\[Subl\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Nom\]', r'\[\/N\]\[Nom\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Ins\]', r'\[\/N\]\[Ins\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Acc\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Acc\]', r'\[\/N\]\[Acc\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Ine\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Ine\]', r'\[\/N\]\[Ine\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Supe\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Supe\]', r'\[\/N\]\[Supe\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Subl\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Subl\]', r'\[\/N\]\[Subl\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Ill\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Ill\]', r'\[\/N\]\[Ill\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Ter\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Ter\]', r'\[\/N\]\[Ter\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Dat\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Dat\]', r'\[\/N\]\[Dat\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[All\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[All\]', r'\[\/N\]\[All\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Del\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Del\]', r'\[\/N\]\[Del\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Transl\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Transl\]', r'\[\/N\]\[Transl\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Ins\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Ins\]', r'\[\/N\]\[Ins\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Ela\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Ela\]', r'\[\/N\]\[Ela\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Abl\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Abl\]', r'\[\/N\]\[Abl\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[EssFor\:ként\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[EssFor\:ként\]', r'\[\/N\]\[EssFor\:ként\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |\[\/Num\]\[Nom\] |egy |(\[\/Det\|Pro\]\[Nom\] \[\/Det\|Art\.Def\] ))+\[\/N\]\[Nom\]', r'\[\/N\]\[Nom\]'),
                      ]
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

