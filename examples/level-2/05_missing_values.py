"""Level 2, Bab 5: menangani nilai kosong (missing values).

Dataset asli tidak punya nilai kosong, jadi kita membuat salinan dan
MENGOSONGKAN sebagian nilainya secara sengaja (simulasi, seed tetap).

Jalankan dari folder utama proyek:
    python examples/level-2/05_missing_values.py
"""
# NB: setup=Siapkan alat dan muat data | real=Periksa data asli | simulate=Buat salinan dengan nilai kosong buatan | detect=Temukan nilai kosong | dropna=Strategi 1: buang baris yang kosong | fillna=Strategi 2: isi dengan median | compare=Bandingkan hasil dengan data asli | imputer=Strategi 2 dengan scikit-learn

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import numpy as np
import pandas as pd

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

# --8<-- [start:real]
print("Nilai kosong pada data asli:", df.isna().sum().sum())
# --8<-- [end:real]

# --8<-- [start:simulate]
rng = np.random.default_rng(42)  # seed tetap, hasil selalu sama

df_kosong = df.copy()  # salinan, data asli tidak berubah
for kolom in ["Age", "Annual Income (k$)"]:
    baris_terpilih = rng.choice(df_kosong.index, size=10, replace=False)
    df_kosong.loc[baris_terpilih, kolom] = np.nan

print("Nilai kosong pada salinan:")
print(df_kosong.isna().sum())
# --8<-- [end:simulate]

# --8<-- [start:detect]
print("Jumlah kosong per kolom:")
print(df_kosong.isna().sum())

print("\nPersentase kosong per kolom:")
print((df_kosong.isna().mean() * 100).round(1))

print("\nJumlah baris yang punya minimal satu nilai kosong:",
      df_kosong.isna().any(axis=1).sum())

print("\nContoh baris yang kosong:")
print(df_kosong[df_kosong.isna().any(axis=1)].head())
# --8<-- [end:detect]

# --8<-- [start:dropna]
df_buang = df_kosong.dropna()

print("Ukuran sebelum:", df_kosong.shape)
print("Ukuran sesudah:", df_buang.shape)
# --8<-- [end:dropna]

# --8<-- [start:fillna]
df_isi = df_kosong.copy()
for kolom in ["Age", "Annual Income (k$)"]:
    median = df_isi[kolom].median()
    df_isi[kolom] = df_isi[kolom].fillna(median)
    print(f"Median {kolom}: {median}")

print("\nNilai kosong tersisa:", df_isi.isna().sum().sum())
print("Ukuran:", df_isi.shape)
# --8<-- [end:fillna]

# --8<-- [start:compare]
kolom_cek = ["Age", "Annual Income (k$)"]
tabel = pd.DataFrame(
    {
        "asli": df[kolom_cek].mean(),
        "buang baris": df_buang[kolom_cek].mean(),
        "isi median": df_isi[kolom_cek].mean(),
    }
).round(2)
print("Rata-rata:")
print(tabel)
# --8<-- [end:compare]

# --8<-- [start:imputer]
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy="median")
df_sklearn = df_kosong.copy()
df_sklearn[kolom_cek] = imputer.fit_transform(df_sklearn[kolom_cek])

print("Nilai kosong tersisa:", df_sklearn.isna().sum().sum())
print("Median yang dipakai :", imputer.statistics_)
# --8<-- [end:imputer]
