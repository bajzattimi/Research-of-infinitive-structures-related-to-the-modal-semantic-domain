import os

# Mappa, ahol a fájlokat keressük
folder_path = "mannheim_ngram\merged_3"  # <-- módosítsd

# A total fájl elérési útja
total_file = os.path.join(folder_path, "merged_total.txt")

# Total fájl beolvasása
with open(total_file, 'r', encoding='utf-8') as f:
    all_lines = [line.strip() for line in f if line.strip()]

# Negyedek kiszámítása
n = len(all_lines)
start = n // 4
end = n // 2
second_quarter_lines = all_lines[start:end]  # teljes sorok, pl. "321 akar [V][Inf]"

# Most keressük ezeket a sorokat a többi fájlban
for filename in os.listdir(folder_path):
    if filename.endswith(".txt") and filename != "merged_total.txt":
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            file_lines = [line.strip() for line in f if line.strip()]

        print(f"\n📄 Fájl: {filename}")
        for target in second_quarter_lines:
            try:
                position = file_lines.index(target) + 1  # 1-alapú index
                print(f"  '{target}' => {position}. sor")
            except ValueError:
                print(f"  '{target}' => nincs benne")