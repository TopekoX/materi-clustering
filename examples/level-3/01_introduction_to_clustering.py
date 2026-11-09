"""Level 3, Bab 1: masalah clustering pertama dengan data Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-3/01_introduction_to_clustering.py
"""
# NB: setup=Siapkan alat dan muat data | nolabel=Data tanpa label | look=Melihat data mentah | cluster=Mengelompokkan data | sizes=Ukuran tiap kelompok | profile=Profil tiap kelompok | result=Menggambar hasil pengelompokan

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)  # supaya "data/mall_customers.csv" ketemu dari mana pun skrip dijalankan
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("data/mall_customers.csv")

# Dua fitur yang akan kita pakai untuk mencari kelompok pelanggan
X = df[["Annual Income (k$)", "Spending Score (1-100)"]]
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-data-mentah", "01-hasil-clustering"])

# --8<-- [start:nolabel]
print("Kolom yang tersedia:", list(df.columns))
print("Bentuk data yang dikelompokkan (baris, kolom):", X.shape)
print("\nLima baris pertama fitur:")
print(X.head())
# --8<-- [end:nolabel]

# --8<-- [start:look]
fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.scatter(X["Annual Income (k$)"], X["Spending Score (1-100)"], s=18, color="#444444")
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1-100)")
ax.set_title("Data mentah: belum ada kelompok")
plt.show()
# --8<-- [end:look]

# --8<-- [start:cluster]
model = KMeans(n_clusters=5, n_init=10, random_state=42)
df["Cluster"] = model.fit_predict(X)
print(df[["CustomerID", "Annual Income (k$)", "Spending Score (1-100)", "Cluster"]].head())
# --8<-- [end:cluster]

# --8<-- [start:sizes]
print("\nJumlah pelanggan per kelompok:")
print(df["Cluster"].value_counts().sort_index())
# --8<-- [end:sizes]

# --8<-- [start:profile]
profile = df.groupby("Cluster")[["Annual Income (k$)", "Spending Score (1-100)"]].mean().round(1)
print("\nRata-rata tiap kelompok:")
print(profile)
# --8<-- [end:profile]

# --8<-- [start:result]
colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00"]

fig, ax = plt.subplots(figsize=(6, 4.8))
for k in range(5):
    members = df[df["Cluster"] == k]
    ax.scatter(
        members["Annual Income (k$)"],
        members["Spending Score (1-100)"],
        s=22,
        color=colors[k],
        label=f"Kelompok {k}",
    )

centers = model.cluster_centers_
ax.scatter(centers[:, 0], centers[:, 1], marker="X", s=140, color="black", label="Pusat kelompok")
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1-100)")
ax.set_title("Pelanggan dikelompokkan menjadi 5")
ax.legend(fontsize=8)
plt.show()
# --8<-- [end:result]
