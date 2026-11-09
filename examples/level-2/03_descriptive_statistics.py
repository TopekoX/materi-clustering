"""Level 2, Bab 3: statistik deskriptif pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/03_descriptive_statistics.py
"""
# NB: setup=Siapkan alat dan muat data | center=Ukuran pemusatan: mean, median, modus | spread=Ukuran sebaran: rentang, simpangan baku, IQR | manual=Menghitung rata-rata dan simpangan baku dengan tangan | skew=Kemiringan sebaran | group=Statistik per kelompok | corr=Hubungan antar kolom: korelasi

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)

fitur = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
# --8<-- [end:setup]

# --8<-- [start:center]
print("Mean  :")
print(df[fitur].mean().round(2))

print("\nMedian:")
print(df[fitur].median())

print("\nModus Age :", df["Age"].mode().tolist())
# --8<-- [end:center]

# --8<-- [start:spread]
print("Rentang (max - min):")
print((df[fitur].max() - df[fitur].min()))

print("\nSimpangan baku:")
print(df[fitur].std().round(2))

q1 = df[fitur].quantile(0.25)
q3 = df[fitur].quantile(0.75)
print("\nIQR (Q3 - Q1):")
print(q3 - q1)
# --8<-- [end:spread]

# --8<-- [start:manual]
usia = df["Age"].tolist()
n = len(usia)

rata_rata = sum(usia) / n
jumlah_kuadrat = sum((x - rata_rata) ** 2 for x in usia)
simpangan_baku = (jumlah_kuadrat / (n - 1)) ** 0.5

print("Rata-rata Age (manual)        :", round(rata_rata, 2))
print("Simpangan baku Age (manual)   :", round(simpangan_baku, 2))
print("Rata-rata Age (pandas)        :", round(df["Age"].mean(), 2))
print("Simpangan baku Age (pandas)   :", round(df["Age"].std(), 2))
# --8<-- [end:manual]

# --8<-- [start:skew]
print("Skewness (kemiringan):")
print(df[fitur].skew().round(2))
# --8<-- [end:skew]

# --8<-- [start:group]
print("Rata-rata per Gender:")
print(df.groupby("Gender")[fitur].mean().round(2))

print("\nJumlah pelanggan per Gender:")
print(df.groupby("Gender").size())
# --8<-- [end:group]

# --8<-- [start:corr]
print("Matriks korelasi:")
print(df[fitur].corr().round(2))
# --8<-- [end:corr]
