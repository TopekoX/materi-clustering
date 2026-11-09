"""Level 3, Bab 7: alur kerja clustering dari awal sampai laporan.

Jalankan dari folder utama proyek:
    python examples/level-3/07_clustering_workflow.py
"""
# NB: understand=Memahami dataset | prepare=Menyiapkan fitur | scale=Menyamakan skala | choose=Memilih jumlah kelompok | fit=Melatih model dan memberi nomor kelompok | stability=Memeriksa kestabilan | interpret=Menafsirkan kelompok | plot=Visualisasi akhir | report=Laporan ringkas

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

import _savefig

_savefig.install(["07-pemilihan-k", "07-segmentasi-akhir"])

# Langkah 1 (definisi masalah) ditulis di bab. Pertanyaannya:
# "Adakah kelompok pelanggan menurut pendapatan dan perilaku belanja?"

# --8<-- [start:understand]
df = pd.read_csv("data/mall_customers.csv")

print("Ukuran:", df.shape)
print("Nilai kosong total:", int(df.isna().sum().sum()))
print("Baris duplikat:", int(df.duplicated().sum()))
print(df.describe().round(1).loc[["min", "mean", "max"]])
# --8<-- [end:understand]

# --8<-- [start:prepare]
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X = df[features]
print("Fitur untuk clustering:", features)
print("Kolom yang tidak dipakai:", [c for c in df.columns if c not in features])
# --8<-- [end:prepare]

# --8<-- [start:scale]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Rata-rata setelah skala:", (X_scaled.mean(axis=0).round(2) + 0.0))
print("Simpangan baku setelah skala:", X_scaled.std(axis=0).round(2))
# --8<-- [end:scale]

# --8<-- [start:choose]
scores = {}
for k in range(2, 9):
    labels_k = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_scaled)
    scores[k] = silhouette_score(X_scaled, labels_k)

for k, s in scores.items():
    print(f"k = {k}: silhouette = {s:.3f}")
best_k = max(scores, key=scores.get)
print("k dengan silhouette tertinggi:", best_k)

fig, ax = plt.subplots(figsize=(5.5, 4))
ax.plot(list(scores), list(scores.values()), marker="o", color="#0072B2")
ax.set_xlabel("Jumlah kelompok (k)")
ax.set_ylabel("Silhouette score")
ax.set_title("Memilih jumlah kelompok")
plt.show()
# --8<-- [end:choose]

# --8<-- [start:fit]
model = KMeans(n_clusters=best_k, n_init=10, random_state=42)
df["Cluster"] = model.fit_predict(X_scaled)
print(df["Cluster"].value_counts().sort_index())
# --8<-- [end:fit]

# --8<-- [start:stability]
for seed in range(5):
    other = KMeans(n_clusters=best_k, n_init=10, random_state=seed).fit_predict(X_scaled)
    ari = adjusted_rand_score(df["Cluster"], other)
    print(f"random_state = {seed}: kesamaan dengan hasil utama (ARI) = {ari:.3f}")
# --8<-- [end:stability]

# --8<-- [start:interpret]
profile = df.groupby("Cluster")[features + ["Age"]].mean().round(1)
profile.insert(0, "Jumlah", df["Cluster"].value_counts().sort_index())
print(profile)
# --8<-- [end:interpret]

# --8<-- [start:plot]
colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#999999", "#000000"]
centers_original = scaler.inverse_transform(model.cluster_centers_)

fig, ax = plt.subplots(figsize=(6, 4.8))
for k in range(best_k):
    sub = df[df["Cluster"] == k]
    ax.scatter(sub[features[0]], sub[features[1]], s=22, color=colors[k], label=f"Kelompok {k}")
ax.scatter(centers_original[:, 0], centers_original[:, 1], marker="X", s=140, color="black", label="Centroid")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("Segmentasi pelanggan Mall Customers")
ax.legend(fontsize=8)
plt.show()
# --8<-- [end:plot]

# --8<-- [start:report]
for k, row in profile.iterrows():
    share = row["Jumlah"] / len(df) * 100
    print(
        f"Kelompok {k}: {int(row['Jumlah'])} pelanggan ({share:.1f}%), "
        f"pendapatan rata-rata {row[features[0]]}, skor belanja rata-rata {row[features[1]]}, "
        f"usia rata-rata {row['Age']}"
    )
# --8<-- [end:report]
