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
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Ine\]', r'\[\/N\]\[Ine\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Dat\]', r'\[\/N\]\[Dat\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Supe\]', r'\[\/N\]\[Supe\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Ill\]', r'\[\/N\]\[Ill\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Del\]', r'\[\/N\]\[Del\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Transl\]', r'\[\/N\]\[Transl\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[All\]', r'\[\/N\]\[All\]'),
                      (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] )*\[\/N\]\[Nom] (egy |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[EssFor\:ként\]', r'\[\/N\]\[EssFor\:ként\]'),
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
                      (r'(\[\/Det\|Art\.Def\] |\[\/Adj\]\[Nom\] )*\[\/N\]\[Nom\] (\[\/N\]\[Poss\]\[Nom\] )?\[\/Post\](\[Poss\])?', r'\[\/N\]\[Nom\] \[/Post\]'),
                      (r'(\[\/Det\|Art\.Def\] |\[\/Adj\]\[Nom\] )*\[\/N\]\[Nom\] (\[\/N\]\[Poss\]\[Nom\] )?\[\/Post\](\[Supe\])?', r'\[\/N\]\[Nom\] \[/Post\]\[Supe\]'),
                      (r'\[\/N\]\[Acc\] \[\/Cnj\] \[\/N\]\[Acc\]', r'\[\/N\]\[Acc\]'),
                      (r'\[\/N\]\[Nom\] \[\/Cnj\] \[\/N\]\[Nom\]', r'\[\/N\]\[Acc\]'),
                      (r'\[\/N\]\[Ins\] \[\/Cnj\] \[\/N\]\[Ins\]', r'\[\/N\]\[Ins\]'),
                      (r'\[\/N\]\[Ine\] \[\/Cnj\] \[\/N\]\[Ine\]', r'\[\/N\]\[Acc\]'),
                      (r'\[\/N\]\[Ill\] \[\/Cnj\] \[\/N\]\[Ill\]', r'\[\/N\]\[Ill\]'),
                      (r'\[\/N\]\[Supe\] \[\/Cnj\] \[\/N\]\[Supe\]', r'\[\/N\]\[Supe\]'),
                      (r'\[\/N\]\[Subl\] \[\/Cnj\] \[\/N\]\[Subl\]', r'\[\/N\]\[Subl\]'),
                      (r'\[\/N\]\[Transl\] \[\/Cnj\] \[\/N\]\[Transl\]', r'\[\/N\]\[Transl\]'),
                      (r'\[\/Adj\]\[Nom\] \[\/Cnj\] \[\/Adj\]\[Nom\]', r'\[\/Adj\]\[Nom\]'),
                      (r'\[\/Adj\]\[\_Manner\/Adv\] \[\/Cnj\] \[\/Adj\]\[\_Manner\/Adv\]', r'\[\/Adj\]\[\_Manner\/Adv\]')
                      ]
    regex_patterns2 = [(r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Acc\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Nom\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Nom\]', r'\[\/N\]\[Nom\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Subl\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Subl\]', r'\[\/N\]\[Subl\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Ins\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Ins\]', r'\[\/N\]\[Ins\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Ine\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Ine\]', r'\[\/N\]\[Ine\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Dat\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Dat\]', r'\[\/N\]\[Dat\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Ill\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Ill\]', r'\[\/N\]\[Ill\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Supe\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Supe\]', r'\[\/N\]\[Supe\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[All\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[All\]', r'\[\/N\]\[All\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[Transl\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[Transl\]', r'\[\/N\]\[Transl\]'),
                       (r'(\[\/Adj\]\[Nom\] |\[\/Det\|Art\.Def\] |egy |\[\/Num\]\[Nom\] |\[\/Det\|Pro\]\[EssFor\:ként\] \[\/Det\|Art\.Def\] )*\[\/N\]\[Poss\]\[EssFor\:ként\]', r'\[\/N\]\[EssFor\:ként\]'),
                       (r'(\[\/Det\|Art\.Def\] |\[\/Adj\]\[Nom\] )*\[\/N\]\[Poss\]\[Nom\] \[\/Post\](\[Poss\])?', r'\[\/N\]\[Nom\] \[/Post\]'),
                       (r'(\[\/Det\|Art\.Def\] |\[\/Adj\]\[Nom\] )+ \[\/Adj\]\[Nom\]', r'\[\/Adj\]\[Nom\]'),
                       (r'\[\/N\]\[Poss\]\[Acc\] \[\/Cnj\] \[\/N\]\[Poss\]\[Acc\]', r'\[\/N\]\[Acc\]'),
                       (r'\[\/N\]\[Poss\]\[Nom\] \[\/Cnj\] \[\/N\]\[Poss\]\[Nom\]', r'\[\/N\]\[Acc\]'),
                       (r'\[\/N\]\[Poss\]\[Ins\] \[\/Cnj\] \[\/N\]\[Poss\]\[Ins\]', r'\[\/N\]\[Ins\]'),
                       (r'\[\/N\]\[Poss\]\[Ine\] \[\/Cnj\] \[\/N\]\[Poss\]\[Ine\]', r'\[\/N\]\[Acc\]'),
                       (r'\[\/N\]\[Poss\]\[Ill\] \[\/Cnj\] \[\/N\]\[Poss\]\[Ill\]', r'\[\/N\]\[Ill\]'),
                       (r'\[\/N\]\[Poss\]\[Supe\] \[\/Cnj\] \[\/N\]\[Poss\]\[Supe\]', r'\[\/N\]\[Supe\]'),
                       (r'\[\/N\]\[Poss\]\[Subl\] \[\/Cnj\] \[\/N\]\[Poss\]\[Subl\]', r'\[\/N\]\[Subl\]'),
                       (r'\[\/N\]\[Poss\]\[Transl\] \[\/Cnj\] \[\/N\]\[Poss\]\[Transl\]', r'\[\/N\]\[Transl\]')]

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
            result_lines2 = [line.replace('\\', '') for line in result_lines2]
            output_file_2.writelines(result_lines2)

        print("Code has completed the replacements")

    except FileNotFoundError:
        print(f"We don't find the file: {input_file_path}")


if __name__ == "__main__":
    main()

