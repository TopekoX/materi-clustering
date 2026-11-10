"""Level 5, Bab 6: Davies-Bouldin Index (DBI).

Jalankan dari folder utama proyek:
    python examples/level-5/06_davies_bouldin_index.py
"""
# NB: setup=Siapkan alat | tiny=Sembilan titik dan tiga kelompok | manual=DBI dihitung manual | check=Mencocokkan dengan scikit-learn | blobs=DBI untuk beberapa nilai K | scale=DBI tidak bergantung pada skala keseluruhan | spread=Sebaran dan jarak antar kelompok | plotk=Menggambar DBI terhadap K | limits=Keterbatasan: moons dan data tanpa kelompok | plotmoons=Menggambar moons | mall=DBI pada Mall Customers

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
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["06-dbi-vs-k", "06-moons-dbi"])

# --8<-- [start:tiny]
# Sembilan titik di tiga kelompok
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2],   # kelompok 0
        [6, 5], [7, 5], [6, 6],   # kelompok 1
        [1, 8], [2, 8], [1, 9],   # kelompok 2
    ],
    dtype=float,
)
labels_tiny = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
# --8<-- [end:tiny]

# --8<-- [start:manual]
def dbi_manual(X, labels, verbose=False):
    """Davies-Bouldin Index dihitung langkah demi langkah."""
    ks = np.unique(labels)
    centroids = np.array([X[labels == k].mean(axis=0) for k in ks])

    # S_i: rata-rata jarak titik ke centroid kelompoknya (sebaran kelompok)
    S = np.array([np.linalg.norm(X[labels == k] - centroids[idx], axis=1).mean() for idx, k in enumerate(ks)])

    # M_ij: jarak antar centroid
    M = np.linalg.norm(centroids[:, None, :] - centroids[None, :, :], axis=2)

    # R_ij = (S_i + S_j) / M_ij untuk i != j; D_i = nilai R_ij terbesar
    n = len(ks)
    R = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                R[i, j] = (S[i] + S[j]) / M[i, j]
    D = R.max(axis=1)

    if verbose:
        print("Centroid:\n", centroids.round(3))
        print("S_i      :", S.round(3).tolist())
        print("M_ij:\n", M.round(3))
        print("R_ij:\n", R.round(3))
        print("D_i      :", D.round(3).tolist())
    return D.mean()


dbi_tiny = dbi_manual(X_tiny, labels_tiny, verbose=True)
print(f"DBI manual = {dbi_tiny:.4f}")
# --8<-- [end:manual]

# --8<-- [start:check]
print(f"davies_bouldin_score = {davies_bouldin_score(X_tiny, labels_tiny):.4f}")
# --8<-- [end:check]

# --8<-- [start:blobs]
X_blobs, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=42)
rows = []
for k in range(2, 9):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_blobs)
    rows.append({"K": k, "Davies-Bouldin": davies_bouldin_score(X_blobs, labels),
                 "Silhouette": silhouette_score(X_blobs, labels)})
blob_table = pd.DataFrame(rows).set_index("K")
print(blob_table.round(3).to_string())
print("K dengan DBI terendah       :", int(blob_table["Davies-Bouldin"].idxmin()))
print("K dengan Silhouette tertinggi:", int(blob_table["Silhouette"].idxmax()))
# --8<-- [end:blobs]

# --8<-- [start:scale]
labels_blobs4 = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X_blobs)
print(f"DBI data asli      : {davies_bouldin_score(X_blobs, labels_blobs4):.4f}")
print(f"DBI data x 10      : {davies_bouldin_score(X_blobs * 10, labels_blobs4):.4f}")
# --8<-- [end:scale]

# --8<-- [start:spread]
# Dua pasang kelompok: sebaran sama, jarak antar pusat berbeda
rows = []
for gap in (3, 6, 12):
    X_pair, _ = make_blobs(n_samples=300, centers=[[0, 0], [gap, 0]], cluster_std=1.0, random_state=42)
    labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_pair)
    rows.append({"Jarak antar pusat": gap, "Davies-Bouldin": davies_bouldin_score(X_pair, labels)})
print(pd.DataFrame(rows).set_index("Jarak antar pusat").round(3).to_string())

# Dua pasang kelompok: jarak sama, sebaran berbeda
rows = []
for std in (0.5, 1.0, 2.0):
    X_pair, _ = make_blobs(n_samples=300, centers=[[0, 0], [8, 0]], cluster_std=std, random_state=42)
    labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_pair)
    rows.append({"Sebaran (std)": std, "Davies-Bouldin": davies_bouldin_score(X_pair, labels)})
print(pd.DataFrame(rows).set_index("Sebaran (std)").round(3).to_string())
# --8<-- [end:spread]

# --8<-- [start:plotk]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])
mall_dbi = {k: davies_bouldin_score(X_mall, KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_mall))
            for k in range(2, 11)}

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(blob_table.index, blob_table["Davies-Bouldin"], marker="o", color=palette[0])
axes[0].set_title("Empat gerombol jelas")
axes[1].plot(list(mall_dbi.keys()), list(mall_dbi.values()), marker="o", color=palette[1])
axes[1].set_title("Mall Customers")
for ax in axes:
    ax.set_xlabel("Jumlah kelompok (K)")
    ax.set_ylabel("Davies-Bouldin Index (lebih rendah lebih baik)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotk]

# --8<-- [start:limits]
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
km_moons = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_moons)
print(f"DBI K-Means (memotong bulan) : {davies_bouldin_score(X_moons, km_moons):.3f}")
print(f"DBI label benar              : {davies_bouldin_score(X_moons, y_moons):.3f}")

# Data tanpa kelompok alami
X_uniform = np.random.default_rng(42).uniform(-10, 10, size=(400, 2))
uniform_dbi = {k: davies_bouldin_score(X_uniform, KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_uniform))
               for k in range(2, 9)}
print("DBI data acak:", {k: round(v, 3) for k, v in uniform_dbi.items()})
# --8<-- [end:limits]

# --8<-- [start:plotmoons]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
panels = [
    (km_moons, f"Hasil K-Means\nDBI = {davies_bouldin_score(X_moons, km_moons):.3f}"),
    (y_moons, f"Label benar\nDBI = {davies_bouldin_score(X_moons, y_moons):.3f}"),
]
for ax, (labels, title) in zip(axes, panels):
    for k in range(2):
        ax.scatter(X_moons[labels == k, 0], X_moons[labels == k, 1], s=14, color=palette[k])
    ax.set_title(title)
    ax.set_xlabel("Fitur 1")
axes[0].set_ylabel("Fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotmoons]

# --8<-- [start:mall]
print({k: round(v, 3) for k, v in mall_dbi.items()})
best_k = min(mall_dbi, key=mall_dbi.get)
print("K dengan DBI terendah pada Mall Customers:", best_k, f"({mall_dbi[best_k]:.3f})")
# --8<-- [end:mall]
