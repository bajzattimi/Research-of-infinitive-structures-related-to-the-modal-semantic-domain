import re

def main():
    file_path = "test_akar_5_webkorpusz.txt"

    regex_patterns = [(r'\[\/Adj\]\[Nom\] \[\/N\]\[Acc\]', r'\[\/N\]\[Nom\]')]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            for pattern, replacement in regex_patterns:
                lines = [re.sub(pattern, replacement, line) for line in lines]

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        print("Code has completed the replacements")

    except FileNotFoundError:
        print(f"We don't find the file: {file_path}")


if __name__ == "__main__":
    main()