"""Level 3, Bab 4: similarity, dissimilarity, dan matriks jarak.

Jalankan dari folder utama proyek:
    python examples/level-3/04_similarity_and_dissimilarity.py
"""
# NB: setup=Lima pelanggan nyata | matrix=Matriks jarak | similarity=Dari jarak ke kemiripan | check=Sifat matriks jarak | categorical=Data kategori dan biner | scale=Kesalahan umum: skala fitur | plot=Visualisasi matriks jarak

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
five = df.loc[:4, ["CustomerID"] + cols].set_index("CustomerID")
print(five)
# --8<-- [end:setup]

import _savefig

_savefig.install(["04-matriks-jarak"])

# --8<-- [start:matrix]
D = pairwise_distances(five.to_numpy(), metric="euclidean")
D_df = pd.DataFrame(D, index=five.index, columns=five.index).round(2)
print("Matriks jarak Euclidean (5 pelanggan):")
print(D_df)
# --8<-- [end:matrix]

# --8<-- [start:similarity]
S = 1 / (1 + D)
S_df = pd.DataFrame(S, index=five.index, columns=five.index).round(3)
print("Matriks kemiripan S = 1 / (1 + jarak):")
print(S_df)
# --8<-- [end:similarity]

# --8<-- [start:check]
print("Simetris (D sama dengan transposnya)?", np.allclose(D, D.T))
print("Diagonal semuanya nol?               ", np.allclose(np.diag(D), 0))
print("Tidak ada jarak negatif?             ", bool((D >= 0).all()))

# Pasangan paling mirip: jarak terkecil di luar diagonal
masked = D + np.diag([np.inf] * len(D))
i, j = np.unravel_index(masked.argmin(), masked.shape)
print("Pasangan paling mirip: pelanggan", five.index[i], "dan", five.index[j], "dengan jarak", round(float(masked[i, j]), 2))
# --8<-- [end:check]

# --8<-- [start:categorical]
# Dua pelanggan, lima produk (1 = membeli, 0 = tidak)
a = np.array([1, 1, 0, 0, 1])
b = np.array([1, 0, 0, 1, 1])

same = (a == b).sum()
simple_matching = same / len(a)

both_one = ((a == 1) & (b == 1)).sum()
either_one = ((a == 1) | (b == 1)).sum()
jaccard_similarity = both_one / either_one

print("Jumlah posisi yang sama:", same)
print("Simple matching similarity:", simple_matching)
print("Jumlah posisi keduanya 1:", both_one, "| salah satunya 1:", either_one)
print("Jaccard similarity:", round(float(jaccard_similarity), 3))
print("Jaccard distance  :", round(float(1 - jaccard_similarity), 3))
# --8<-- [end:categorical]

# --8<-- [start:scale]
raw = five.to_numpy()
diff = raw[0] - raw[1]
print("Selisih tiap fitur antara pelanggan 1 dan 2:", dict(zip(cols, diff.tolist())))
print("Kuadrat selisih tiap fitur:", dict(zip(cols, (diff ** 2).tolist())))

scaler = StandardScaler().fit(df[cols])
scaled = scaler.transform(five)
D_scaled = pairwise_distances(scaled)
print("\nMatriks jarak setelah standardisasi:")
print(pd.DataFrame(D_scaled, index=five.index, columns=five.index).round(2))
# --8<-- [end:scale]

# --8<-- [start:plot]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, M, title in [(axes[0], D, "Jarak data mentah"), (axes[1], D_scaled, "Jarak setelah standardisasi")]:
    ax.imshow(M, cmap="viridis_r")
    ax.set_xticks(range(5), labels=five.index)
    ax.set_yticks(range(5), labels=five.index)
    ax.set_xlabel("CustomerID")
    ax.set_title(title)
    for r in range(5):
        for c in range(5):
            color = "black" if M[r, c] < M.max() * 0.5 else "white"
            ax.text(c, r, f"{M[r, c]:.1f}", ha="center", va="center", color=color, fontsize=9)
axes[0].set_ylabel("CustomerID")
fig.tight_layout()
plt.show()
# --8<-- [end:plot]
