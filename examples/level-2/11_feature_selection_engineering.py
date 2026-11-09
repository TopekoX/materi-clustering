"""Level 2, Bab 11: feature selection dan feature engineering.

Jalankan dari folder utama proyek:
    python examples/level-2/11_feature_selection_engineering.py
"""
# NB: setup=Siapkan alat dan muat data | drop_id=Membuang kolom yang bukan fitur | redundancy=Mencari fitur yang berulang (redundan) | engineer=Membuat fitur baru | judge=Menilai apakah fitur baru layak dipakai | sets=Menyusun kandidat himpunan fitur

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

# --8<-- [start:drop_id]
print("Kolom sebelum:", df.columns.tolist())

df_fitur = df.drop(columns=["CustomerID"])

print("Kolom sesudah:", df_fitur.columns.tolist())
# --8<-- [end:drop_id]

# --8<-- [start:redundancy]
angka = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
korelasi = df[angka].corr().round(2)
print(korelasi)

pasangan_kuat = []
for i, a in enumerate(angka):
    for b in angka[i + 1:]:
        if abs(korelasi.loc[a, b]) >= 0.8:
            pasangan_kuat.append((a, b))

print("\nPasangan dengan |korelasi| >= 0.8:", pasangan_kuat)
# --8<-- [end:redundancy]

# --8<-- [start:engineer]
df_baru = df_fitur.copy()
df_baru["Spend_Income_Ratio"] = (
    df_baru["Spending Score (1-100)"] / df_baru["Annual Income (k$)"]
)

print(df_baru.head())
# --8<-- [end:engineer]

# --8<-- [start:judge]
rasio = df_baru["Spend_Income_Ratio"]

print("Ringkasan fitur baru:")
print(rasio.describe().round(2))
print("\nSkewness fitur baru:", round(rasio.skew(), 2))

print("\nKorelasi fitur baru dengan fitur asal:")
print(df_baru[angka + ["Spend_Income_Ratio"]].corr().loc["Spend_Income_Ratio"].round(2))
# --8<-- [end:judge]

# --8<-- [start:sets]
X_dua = df[["Annual Income (k$)", "Spending Score (1-100)"]]
X_tiga = df[["Age", "Annual Income (k$)", "Spending Score (1-100)"]]
X_empat = pd.get_dummies(
    df[["Gender", "Age", "Annual Income (k$)", "Spending Score (1-100)"]],
    columns=["Gender"],
    dtype=int,
)

for nama, X in [("2 fitur", X_dua), ("3 fitur", X_tiga), ("3 fitur + Gender", X_empat)]:
    print(f"{nama:18s}: bentuk {X.shape}, kolom {X.columns.tolist()}")
# --8<-- [end:sets]
