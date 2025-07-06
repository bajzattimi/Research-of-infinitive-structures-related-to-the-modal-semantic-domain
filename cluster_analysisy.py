import os
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler

# Mappa beállítása
folder_path = "mannheim_ngram/merged_5"  # <-- módosítsd szükség szerint

# Top n-gramok beolvasása
total_file = os.path.join(folder_path, "merged_total.txt")
with open(total_file, 'r', encoding='utf-8') as f:
    top_lines = [line.strip().split(maxsplit=1)[1] for _, line in zip(range(30), f)]

# Gyakorisági mátrix létrehozása
data = []
file_names = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt") and filename != "merged_total.txt":
        file_path = os.path.join(folder_path, filename)
        freqs = {}
        total_count = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(maxsplit=1)
                if len(parts) != 2:
                    continue
                count, ngram = parts
                count = int(count)
                total_count += count
                freqs[ngram] = count

        # Normalizált relatív gyakoriság
        vector = [freqs.get(ngram, 0) / total_count for ngram in top_lines]
        data.append(vector)

        # Csak műfaj rövidítést mentjük (pl. 'lit')
        genre = filename.split('_')[-1].replace('.txt', '')
        file_names.append(genre)

# Adatok standardizálása (opcionális, de ajánlott)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Hierarchikus klaszterezés (linkage matrix)
linked = linkage(data_scaled, method='ward')

# Dendrogram kirajzolása
plt.figure(figsize=(12, 6))
dendrogram(linked, labels=file_names)
plt.title('Register clusters (based on mosaic 5-grams)')
plt.xlabel("Registers")
plt.ylabel("Distance")
plt.tight_layout()
plt.show()
