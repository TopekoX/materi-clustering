"""Level 3, Bab 6: ruang fitur dan dimensi.

Jalankan dari folder utama proyek:
    python examples/level-3/06_feature_space_and_dimensionality.py
"""
# NB: setup=Titik sebagai koordinat | grow=Jarak saat fitur ditambah | plot_dims=Ruang 1D, 2D, dan 3D | curse=Efek dimensi pada jarak | noise=Fitur tak relevan mengubah tetangga | scale=Skala dan bentuk ruang fitur

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/mall_customers.csv")
cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]

p1 = df.loc[0, cols].to_numpy(dtype=float)  # pelanggan 1
p2 = df.loc[1, cols].to_numpy(dtype=float)  # pelanggan 2
print("Pelanggan 1 sebagai titik di ruang 3 dimensi:", p1)
print("Pelanggan 2 sebagai titik di ruang 3 dimensi:", p2)
print("Jumlah dimensi (fitur):", len(p1))
# --8<-- [end:setup]

import _savefig

_savefig.install(["06-ruang-1d-2d-3d", "06-efek-dimensi", "06-skala-ruang-fitur"])

# --8<-- [start:grow]
for k in range(1, 4):
    d = np.sqrt(((p1[:k] - p2[:k]) ** 2).sum())
    print(f"Jarak pelanggan 1 dan 2 memakai {k} fitur ({', '.join(cols[:k])}): {d:.2f}")
# --8<-- [end:grow]

# --8<-- [start:plot_dims]
sample = df.iloc[:60]
fig = plt.figure(figsize=(12, 3.8))

ax1 = fig.add_subplot(1, 3, 1)
ax1.scatter(sample["Age"], np.zeros(len(sample)), s=20, color="#0072B2")
ax1.set_yticks([])
ax1.set_xlabel("Age")
ax1.set_title("1 dimensi: satu garis")

ax2 = fig.add_subplot(1, 3, 2)
ax2.scatter(sample["Annual Income (k$)"], sample["Spending Score (1-100)"], s=20, color="#E69F00")
ax2.set_xlabel("Annual Income (k$)")
ax2.set_ylabel("Spending Score (1-100)")
ax2.set_title("2 dimensi: bidang")

ax3 = fig.add_subplot(1, 3, 3, projection="3d")
ax3.scatter(sample["Age"], sample["Annual Income (k$)"], sample["Spending Score (1-100)"], s=20, color="#009E73")
ax3.set_xlabel("Age")
ax3.set_ylabel("Income")
ax3.set_zlabel("Score")
ax3.set_title("3 dimensi: ruang")

fig.tight_layout()
plt.show()
# --8<-- [end:plot_dims]

# --8<-- [start:curse]
rng = np.random.default_rng(42)
rows = []
for dim in [1, 2, 5, 10, 50, 100, 500, 1000]:
    X = rng.random((200, dim))  # 200 titik acak di kubus satuan berdimensi `dim`
    d = pairwise_distances(X)
    d = d[np.triu_indices_from(d, k=1)]  # hanya satu salinan tiap pasangan
    rows.append(
        {
            "dimensi": dim,
            "jarak_min": d.min(),
            "jarak_maks": d.max(),
            "jarak_rata2": d.mean(),
            "kontras": (d.max() - d.min()) / d.min(),
        }
    )

table = pd.DataFrame(rows).round(3)
print(table.to_string(index=False))

fig, ax = plt.subplots(figsize=(5.5, 4.2))
ax.plot(table["dimensi"], table["kontras"], marker="o", color="#D55E00")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Jumlah dimensi (skala log)")
ax.set_ylabel("Kontras jarak (maks - min) / min (skala log)")
ax.set_title("Jarak makin seragam saat dimensi bertambah")
plt.show()
# --8<-- [end:curse]

# --8<-- [start:noise]
base = StandardScaler().fit_transform(df[["Annual Income (k$)", "Spending Score (1-100)"]])


def nearest(data):
    d = pairwise_distances(data)
    np.fill_diagonal(d, np.inf)
    return d.argmin(axis=1)


nn_base = nearest(base)
rng = np.random.default_rng(42)
print("Fitur acak yang ditambahkan | pelanggan yang tetangga terdekatnya berubah")
for n_noise in [0, 2, 10, 50]:
    noise = rng.standard_normal((len(df), n_noise))
    with_noise = np.hstack([base, noise])
    changed = (nearest(with_noise) != nn_base).sum()
    print(f"{n_noise:>27} | {changed} dari {len(df)}")
# --8<-- [end:noise]

# --8<-- [start:scale]
raw = df[["Age", "Annual Income (k$)"]].to_numpy(dtype=float)
std = StandardScaler().fit_transform(raw)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
axes[0].scatter(raw[:, 0], raw[:, 1], s=16, color="#0072B2")
axes[0].set_aspect("equal")
axes[0].set_xlabel("Age (tahun)")
axes[0].set_ylabel("Annual Income (k$)")
axes[0].set_title("Skala asli, sumbu sama panjang")

axes[1].scatter(std[:, 0], std[:, 1], s=16, color="#009E73")
axes[1].set_aspect("equal")
axes[1].set_xlabel("Age (terstandardisasi)")
axes[1].set_ylabel("Income (terstandardisasi)")
axes[1].set_title("Setelah standardisasi")
fig.tight_layout()
plt.show()

print("Rentang usia   :", raw[:, 0].max() - raw[:, 0].min())
print("Rentang income :", raw[:, 1].max() - raw[:, 1].min())
# --8<-- [end:scale]
