"""Level 4, Bab 3: Hierarchical (agglomerative) clustering, dendrogram, dan linkage.

Jalankan dari folder utama proyek:
    python examples/level-4/03_hierarchical_clustering.py
"""
# NB: setup=Siapkan alat | tiny=Lima titik dan matriks jarak | linkmat=Matriks linkage dengan SciPy | wardcheck=Memeriksa rumus Ward | plottiny=Dendrogram empat linkage | blobs=AgglomerativeClustering pada data blobs | threshold=Memotong dengan distance_threshold | shapes=Linkage pada data berbentuk berbeda | plotshapes=Menggambar hasil linkage | mall=Dendrogram Mall Customers | plotmall=Menggambar dendrogram Mall | cut=Memotong dendrogram di tinggi berbeda | metric=Parameter metric | memory=Biaya memori matriks jarak | plotresult=Menggambar kelompok Mall

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
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs, make_moons
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist, squareform
# --8<-- [end:setup]

import _savefig

_savefig.install(["03-dendrogram-kecil", "03-linkage-bentuk", "03-dendrogram-mall", "03-hasil-mall"])

# --8<-- [start:tiny]
# Lima titik pada satu garis (satu fitur), diberi nama A sampai E
X_line = np.array([[0.0], [1.0], [3.5], [7.0], [9.0]])
names = ["A", "B", "C", "D", "E"]

# pdist menghitung jarak semua pasangan, squareform mengubahnya menjadi matriks persegi
dist_matrix = squareform(pdist(X_line))
print(pd.DataFrame(dist_matrix, index=names, columns=names))
# --8<-- [end:tiny]

# --8<-- [start:linkmat]
for method in ["single", "complete", "average", "ward"]:
    Z = linkage(X_line, method=method)
    print(f"\nLinkage: {method}")
    print(pd.DataFrame(Z, columns=["klaster_1", "klaster_2", "jarak_gabung", "ukuran"]).round(3).to_string())
# --8<-- [end:linkmat]

# --8<-- [start:wardcheck]
# Rumus Ward (tinggi gabung di SciPy): sqrt(2 * nA * nB / (nA + nB)) * jarak antar-rata-rata
A = X_line[[0, 1, 2]]   # klaster {A, B, C}
B = X_line[[3, 4]]      # klaster {D, E}
nA, nB = len(A), len(B)
ward_height = np.sqrt(2 * nA * nB / (nA + nB)) * np.linalg.norm(A.mean(axis=0) - B.mean(axis=0))
print(f"Rata-rata A,B,C = {A.mean():.3f}; rata-rata D,E = {B.mean():.3f}")
print(f"Tinggi gabung Ward terakhir (rumus) = {ward_height:.3f}")
# --8<-- [end:wardcheck]

# --8<-- [start:plottiny]
fig, axes = plt.subplots(1, 4, figsize=(16, 3.8), sharey=False)
for ax, method in zip(axes, ["single", "complete", "average", "ward"]):
    Z = linkage(X_line, method=method)
    dendrogram(Z, labels=names, ax=ax, color_threshold=0, above_threshold_color="#0072B2")
    ax.set_title(f"Linkage: {method}")
    ax.set_xlabel("Titik")
axes[0].set_ylabel("Jarak saat digabung")
plt.tight_layout()
plt.show()
# --8<-- [end:plottiny]

# --8<-- [start:blobs]
X, _ = make_blobs(n_samples=150, centers=3, cluster_std=0.8, random_state=42)

agg = AgglomerativeClustering(n_clusters=3, linkage="ward", compute_distances=True)
labels = agg.fit_predict(X)

print("Ukuran kelompok:", np.bincount(labels).tolist())
print("n_clusters_ :", agg.n_clusters_)
print("n_leaves_   :", agg.n_leaves_)
print("children_ (3 baris pertama, pasangan yang digabung):")
print(agg.children_[:3])
print("distances_ (3 pertama dan 2 terakhir):", agg.distances_[:3].round(3).tolist(), agg.distances_[-2:].round(3).tolist())
# --8<-- [end:blobs]

# --8<-- [start:threshold]
for threshold in [1, 3, 8, 30]:
    model = AgglomerativeClustering(n_clusters=None, distance_threshold=threshold, linkage="ward").fit(X)
    print(f"distance_threshold = {threshold:<3} -> n_clusters_ = {model.n_clusters_}")
# --8<-- [end:threshold]

# --8<-- [start:shapes]
X_moons, _ = make_moons(n_samples=200, noise=0.06, random_state=42)

# Dua gerombol bulat yang "dijembatani" enam titik di antaranya
X_two, _ = make_blobs(n_samples=150, centers=[[-3, 0], [3, 0]], cluster_std=0.7, random_state=42)
bridge = np.column_stack([np.linspace(-1.2, 1.2, 6), np.zeros(6)])
X_bridge = np.vstack([X_two, bridge])

datasets = {"moons": X_moons, "bridge": X_bridge}
linkages = ["single", "complete", "average", "ward"]

shape_labels = {}
for data_name, data in datasets.items():
    for method in linkages:
        lab = AgglomerativeClustering(n_clusters=2, linkage=method).fit_predict(data)
        shape_labels[(data_name, method)] = lab
        print(f"{data_name:<7} {method:<9} ukuran kelompok: {np.bincount(lab).tolist()}")
# --8<-- [end:shapes]

# --8<-- [start:plotshapes]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(2, 4, figsize=(15, 6.5))
for row, (data_name, data) in enumerate(datasets.items()):
    for col, method in enumerate(linkages):
        ax = axes[row, col]
        lab = shape_labels[(data_name, method)]
        for k in sorted(set(lab)):
            ax.scatter(data[lab == k, 0], data[lab == k, 1], s=14, color=palette[k % len(palette)])
        if row == 0:
            ax.set_title(f"Linkage: {method}")
        ax.set_xticks([])
        ax.set_yticks([])
    axes[row, 0].set_ylabel(data_name)
plt.tight_layout()
plt.show()
# --8<-- [end:plotshapes]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

Z_mall = linkage(X_mall, method="ward")
print("Bentuk matriks linkage:", Z_mall.shape, "(n - 1 baris, 4 kolom)")
print("Tinggi gabung 5 langkah terakhir:", Z_mall[-5:, 2].round(2).tolist())
# --8<-- [end:mall]

# --8<-- [start:plotmall]
cut_height = 7.0
fig, ax = plt.subplots(figsize=(10, 4.5))
dendrogram(Z_mall, truncate_mode="lastp", p=16, ax=ax, color_threshold=cut_height,
           above_threshold_color="#444444", show_leaf_counts=True)
ax.axhline(cut_height, color="#D55E00", linestyle="--", label=f"Garis potong (tinggi = {cut_height})")
ax.set_xlabel("Cabang (angka dalam kurung = jumlah pelanggan)")
ax.set_ylabel("Jarak Ward saat digabung")
ax.set_title("Dendrogram Mall Customers (dipangkas ke 16 cabang terakhir)")
ax.legend()
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]

# --8<-- [start:cut]
for height in [3, 5, 7, 10, 20]:
    cut_labels = fcluster(Z_mall, t=height, criterion="distance")
    print(f"Potong di tinggi {height:<2} -> {len(set(cut_labels))} kelompok")

agg5 = AgglomerativeClustering(n_clusters=5, linkage="ward")
df["Cluster"] = agg5.fit_predict(X_mall)
print("\nUkuran 5 kelompok (urut):", sorted(np.bincount(df["Cluster"]).tolist()))
print(df.groupby("Cluster")[features].mean().round(1))
# --8<-- [end:cut]

# --8<-- [start:metric]
for metric in ["euclidean", "manhattan", "cosine"]:
    model = AgglomerativeClustering(n_clusters=5, linkage="average", metric=metric).fit(X_mall)
    print(f"linkage=average, metric={metric:<9} -> ukuran kelompok: {sorted(np.bincount(model.labels_).tolist())}")
# --8<-- [end:metric]

# --8<-- [start:memory]
print(f"{'n (jumlah data)':>16} {'pasangan n(n-1)/2':>20} {'memori (GiB, float64)':>22}")
for n in [200, 10_000, 100_000]:
    pairs = n * (n - 1) // 2
    gib = pairs * 8 / 1024**3
    print(f"{n:>16,} {pairs:>20,} {gib:>22.4f}")
# --8<-- [end:memory]

# --8<-- [start:plotresult]
fig, ax = plt.subplots(figsize=(6.5, 5))
for k in range(5):
    members = df[df["Cluster"] == k]
    ax.scatter(members[features[0]], members[features[1]], s=22,
               color=palette[k % len(palette)], label=f"Kelompok {k}")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("Agglomerative (Ward, 5 kelompok) pada Mall Customers")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotresult]
