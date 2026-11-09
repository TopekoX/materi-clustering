"""Level 2, Bab 1: eksplorasi pertama dataset Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/01_explore_mall_customers.py
"""
# NB: setup=Siapkan alat dan muat data | glance=Lihat sekilas isi data | summary=Ringkasan statistik | quality=Pemeriksaan kualitas dasar | hist=Histogram | scatter=Scatter plot

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)  # supaya "data/mall_customers.csv" ketemu dari mana pun skrip dijalankan

# --8<-- [start:setup]
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-distribusi-fitur", "01-scatter-income-spending"])

# --8<-- [start:glance]
print("Lima baris pertama:")
print(df.head())

print("\nUkuran (baris, kolom):", df.shape)

print("\nTipe data per kolom:")
print(df.dtypes)
# --8<-- [end:glance]

# --8<-- [start:summary]
print("\nRingkasan statistik:")
print(df.describe().round(2))
# --8<-- [end:summary]

# --8<-- [start:quality]
print("\nJumlah nilai kosong per kolom:")
print(df.isna().sum())

print("\nJumlah baris duplikat:", df.duplicated().sum())

print("\nJumlah per Gender:")
print(df["Gender"].value_counts())
# --8<-- [end:quality]

# --8<-- [start:hist]
features = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, col in zip(axes, features):
    ax.hist(df[col], bins=15, edgecolor="white")
    ax.set_title(col)
    ax.set_ylabel("Jumlah pelanggan")
fig.tight_layout()
plt.show()
# --8<-- [end:hist]

# --8<-- [start:scatter]
fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.scatter(df["Annual Income (k$)"], df["Spending Score (1-100)"], s=18)
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1-100)")
ax.set_title("Pendapatan vs skor belanja")
plt.show()
# --8<-- [end:scatter]
