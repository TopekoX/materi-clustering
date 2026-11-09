"""Level 2, Bab 9: transformasi dan encoding data pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/09_transformation_encoding.py
"""
# NB: setup=Siapkan alat dan muat data | binary=Encoding biner dengan map | onehot=One-hot encoding dengan get_dummies | order=Mengapa urutan kode bisa menipu | log=Transformasi logaritma | plot=Melihat efek transformasi pada grafik | binning=Mengelompokkan angka (binning)

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

import _savefig

_savefig.install(["09-log-transform"])

# --8<-- [start:binary]
df_biner = df.copy()
df_biner["Gender_code"] = df_biner["Gender"].map({"Female": 0, "Male": 1})

print(df_biner[["Gender", "Gender_code"]].head())
print("\nJumlah per kode:")
print(df_biner["Gender_code"].value_counts())
# --8<-- [end:binary]

# --8<-- [start:onehot]
df_onehot = pd.get_dummies(df, columns=["Gender"], dtype=int)

print(df_onehot.head())
print("\nKolom sekarang:", df_onehot.columns.tolist())
# --8<-- [end:onehot]

# --8<-- [start:order]
# Bayangkan tiga kategori tanpa urutan, diberi kode 0, 1, 2.
kode = {"Jakarta": 0, "Bandung": 1, "Surabaya": 2}

jarak_jakarta_bandung = abs(kode["Jakarta"] - kode["Bandung"])
jarak_jakarta_surabaya = abs(kode["Jakarta"] - kode["Surabaya"])

print("Jarak Jakarta-Bandung :", jarak_jakarta_bandung)
print("Jarak Jakarta-Surabaya:", jarak_jakarta_surabaya)
print("Padahal ketiganya setara, tanpa urutan.")
# --8<-- [end:order]

# --8<-- [start:log]
income = df["Annual Income (k$)"]
income_log = np.log1p(income)  # log(1 + x)

print("Skewness sebelum log:", round(income.skew(), 2))
print("Skewness sesudah log:", round(income_log.skew(), 2))

print("\nRentang sebelum:", income.min(), "sampai", income.max())
print("Rentang sesudah:", round(income_log.min(), 2), "sampai", round(income_log.max(), 2))
# --8<-- [end:log]

# --8<-- [start:plot]
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
axes[0].hist(income, bins=15, edgecolor="white")
axes[0].set_title("Annual Income (k$): asli")
axes[1].hist(income_log, bins=15, edgecolor="white")
axes[1].set_title("Annual Income (k$): setelah log1p")
fig.tight_layout()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:binning]
df_bin = df.copy()
df_bin["Age Group"] = pd.cut(
    df_bin["Age"],
    bins=[17, 30, 45, 60, 70],
    labels=["18-30", "31-45", "46-60", "61-70"],
)

print(df_bin[["Age", "Age Group"]].head())
print("\nJumlah pelanggan per kelompok usia:")
print(df_bin["Age Group"].value_counts().sort_index())
# --8<-- [end:binning]
