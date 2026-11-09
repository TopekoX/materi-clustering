"""Level 2, Bab 6: menganalisis data duplikat.

Dataset asli tidak punya baris duplikat penuh, jadi kita membuat salinan
dan MENAMBAHKAN baris ganda secara sengaja (simulasi, seed tetap).

Jalankan dari folder utama proyek:
    python examples/level-2/06_duplicate_data.py
"""
# NB: setup=Siapkan alat dan muat data | real=Periksa data asli | partial=Duplikat tanpa memperhitungkan CustomerID | simulate=Buat salinan dengan baris ganda buatan | detect=Temukan baris ganda | drop=Buang baris ganda | verify=Pastikan hasilnya benar

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)

kolom_sifat = ["Gender", "Age", "Annual Income (k$)", "Spending Score (1-100)"]
# --8<-- [end:setup]

# --8<-- [start:real]
print("Baris ganda penuh pada data asli  :", df.duplicated().sum())
print("CustomerID yang muncul lebih dari sekali:", df["CustomerID"].duplicated().sum())
# --8<-- [end:real]

# --8<-- [start:partial]
sama_sifat = df.duplicated(subset=kolom_sifat, keep=False)

print("Baris dengan sifat yang sama persis (tanpa CustomerID):", sama_sifat.sum())
print()
print(df[sama_sifat].sort_values(kolom_sifat))
# --8<-- [end:partial]

# --8<-- [start:simulate]
tambahan = df.sample(n=8, random_state=42)  # 8 baris acak, seed tetap
df_ganda = pd.concat([df, tambahan], ignore_index=True)

print("Ukuran data asli     :", df.shape)
print("Ukuran setelah ditambah:", df_ganda.shape)
# --8<-- [end:simulate]

# --8<-- [start:detect]
print("Jumlah baris ganda:", df_ganda.duplicated().sum())

print("\nSemua baris yang terlibat (aslinya dan salinannya):")
terlibat = df_ganda[df_ganda.duplicated(keep=False)]
print(terlibat.sort_values("CustomerID"))
# --8<-- [end:detect]

# --8<-- [start:drop]
df_bersih = df_ganda.drop_duplicates()

print("Sebelum:", df_ganda.shape)
print("Sesudah:", df_bersih.shape)
# --8<-- [end:drop]

# --8<-- [start:verify]
print("Baris ganda tersisa:", df_bersih.duplicated().sum())
print("Jumlah baris sama dengan data asli?", len(df_bersih) == len(df))
# --8<-- [end:verify]
