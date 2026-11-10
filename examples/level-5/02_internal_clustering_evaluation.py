"""Level 5, Bab 2: Evaluasi clustering internal (jarak dalam dan antar kelompok).

Jalankan dari folder utama proyek:
    python examples/level-5/02_internal_clustering_evaluation.py
"""
# NB: setup=Siapkan alat | tiny=Data kecil dan dua kelompoknya | functions=Empat ukuran dasar sebagai fungsi | tinyresult=Menghitung ukuran pada data kecil | neardistant=Kelompok dekat dan kelompok jauh | plotnear=Menggambar kelompok dekat dan jauh | density=Kepadatan dua kelompok | limits=Keterbatasan: label benar bisa kalah skor | plotmoons=Menggambar data moons | mall=Ukuran dasar pada Mall Customers

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
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["02-dekat-vs-jauh", "02-moons-label-benar"])

# --8<-- [start:tiny]
# Enam titik di dua kelompok yang sudah kita tentukan sendiri
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2],   # kelompok 0
        [6, 5], [7, 5], [6, 6],   # kelompok 1
    ],
    dtype=float,
)
labels_tiny = np.array([0, 0, 0, 1, 1, 1])
# --8<-- [end:tiny]


# --8<-- [start:functions]
def mean_intra_distance(X, labels):
    """Rata-rata jarak antar pasangan titik dalam kelompok yang sama, per kelompok."""
    result = {}
    for k in np.unique(labels):
        members = X[labels == k]
        d = pairwise_distances(members)
        n = len(members)
        result[k] = d.sum() / (n * (n - 1))   # tiap pasangan terhitung dua kali, diagonal nol
    return result


def cohesion(X, labels):
    """Rata-rata jarak titik ke centroid kelompoknya, per kelompok."""
    result = {}
    for k in np.unique(labels):
        members = X[labels == k]
        centroid = members.mean(axis=0)
        result[k] = np.linalg.norm(members - centroid, axis=1).mean()
    return result


def centroid_separation(X, labels):
    """Jarak antar centroid untuk setiap pasangan kelompok."""
    ks = np.unique(labels)
    centroids = np.array([X[labels == k].mean(axis=0) for k in ks])
    d = pairwise_distances(centroids)
    return {(ks[i], ks[j]): d[i, j] for i in range(len(ks)) for j in range(i + 1, len(ks))}


def min_inter_distance(X, labels):
    """Jarak terkecil antara dua titik dari kelompok berbeda, untuk setiap pasangan."""
    ks = np.unique(labels)
    result = {}
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            d = pairwise_distances(X[labels == ks[i]], X[labels == ks[j]])
            result[(ks[i], ks[j])] = d.min()
    return result
# --8<-- [end:functions]

# --8<-- [start:tinyresult]
print("Centroid kelompok 0:", X_tiny[labels_tiny == 0].mean(axis=0).round(3))
print("Centroid kelompok 1:", X_tiny[labels_tiny == 1].mean(axis=0).round(3))
print("Rata-rata jarak dalam kelompok :", {int(k): round(float(v), 3) for k, v in mean_intra_distance(X_tiny, labels_tiny).items()})
print("Cohesion (jarak ke centroid)   :", {int(k): round(float(v), 3) for k, v in cohesion(X_tiny, labels_tiny).items()})
print("Jarak antar centroid           :", {(int(a), int(b)): round(float(v), 3) for (a, b), v in centroid_separation(X_tiny, labels_tiny).items()})
print("Jarak antar titik terdekat     :", {(int(a), int(b)): round(float(v), 3) for (a, b), v in min_inter_distance(X_tiny, labels_tiny).items()})
# --8<-- [end:tinyresult]

# --8<-- [start:neardistant]
# Dua dataset dengan sebaran sama (std = 1.0), hanya jarak antar pusat yang berbeda
centers_near = [[0, 0], [3, 0]]
centers_far = [[0, 0], [10, 0]]
X_near, _ = make_blobs(n_samples=200, centers=centers_near, cluster_std=1.0, random_state=42)
X_far, _ = make_blobs(n_samples=200, centers=centers_far, cluster_std=1.0, random_state=42)

pair_data = {"Dekat (pusat 3 satuan)": X_near, "Jauh (pusat 10 satuan)": X_far}
pair_labels = {}
rows = []
for name, X in pair_data.items():
    labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X)
    pair_labels[name] = labels
    coh = np.mean(list(cohesion(X, labels).values()))
    sep = list(centroid_separation(X, labels).values())[0]
    rows.append(
        {
            "Dataset": name,
            "Cohesion rata-rata": coh,
            "Jarak antar centroid": sep,
            "Rasio separation/cohesion": sep / coh,
            "Silhouette": silhouette_score(X, labels),
        }
    )
print(pd.DataFrame(rows).set_index("Dataset").round(3).to_string())
# --8<-- [end:neardistant]

# --8<-- [start:plotnear]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
for ax, (name, X) in zip(axes, pair_data.items()):
    labels = pair_labels[name]
    for k in range(2):
        ax.scatter(X[labels == k, 0], X[labels == k, 1], s=14, color=palette[k])
        c = X[labels == k].mean(axis=0)
        ax.scatter(c[0], c[1], s=180, marker="X", color="black")
    ax.set_title(name)
    ax.set_xlabel("Fitur 1")
axes[0].set_ylabel("Fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotnear]

# --8<-- [start:density]
# Dua kelompok dengan kepadatan berbeda: kelompok 0 rapat, kelompok 1 renggang
X_dens, y_dens = make_blobs(
    n_samples=[150, 150], centers=[[0, 0], [8, 0]], cluster_std=[0.4, 1.6], random_state=42
)
for k in (0, 1):
    members = X_dens[y_dens == k]
    centroid = members.mean(axis=0)
    coh = np.linalg.norm(members - centroid, axis=1).mean()
    # n_neighbors=2: tetangga pertama adalah titik itu sendiri, jadi ambil kolom kedua
    nn = NearestNeighbors(n_neighbors=2).fit(members)
    dist, _ = nn.kneighbors(members)
    print(f"Kelompok {k}: cohesion = {coh:.3f}, rata-rata jarak ke tetangga terdekat = {dist[:, 1].mean():.3f}")
# --8<-- [end:density]

# --8<-- [start:limits]
# Keterbatasan: pada data moons, label BENAR bisa mendapat skor internal lebih rendah
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
labels_km = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_moons)

print(f"Silhouette label K-Means : {silhouette_score(X_moons, labels_km):.3f}")
print(f"Silhouette label benar   : {silhouette_score(X_moons, y_moons):.3f}")
print("Cohesion label K-Means   :", round(float(np.mean(list(cohesion(X_moons, labels_km).values()))), 3))
print("Cohesion label benar     :", round(float(np.mean(list(cohesion(X_moons, y_moons).values()))), 3))
# --8<-- [end:limits]

# --8<-- [start:plotmoons]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
for ax, labels, title in zip(
    axes,
    [labels_km, y_moons],
    [f"Hasil K-Means\nSilhouette = {silhouette_score(X_moons, labels_km):.3f}",
     f"Label benar\nSilhouette = {silhouette_score(X_moons, y_moons):.3f}"],
):
    for k in range(2):
        ax.scatter(X_moons[labels == k, 0], X_moons[labels == k, 1], s=14, color=palette[k])
    ax.set_title(title)
    ax.set_xlabel("Fitur 1")
axes[0].set_ylabel("Fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotmoons]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])
labels_mall = KMeans(n_clusters=5, n_init=10, random_state=42).fit_predict(X_mall)

coh_mall = cohesion(X_mall, labels_mall)
sizes = np.bincount(labels_mall)
table = pd.DataFrame({"Ukuran": sizes, "Cohesion": [coh_mall[k] for k in range(5)]})
print(table.round(3))
sep_mall = centroid_separation(X_mall, labels_mall)
nearest_pair = min(sep_mall, key=sep_mall.get)
farthest_pair = max(sep_mall, key=sep_mall.get)
print("Pasangan kelompok dengan centroid terdekat:", (int(nearest_pair[0]), int(nearest_pair[1])), round(float(sep_mall[nearest_pair]), 3))
print("Pasangan kelompok dengan centroid terjauh :", (int(farthest_pair[0]), int(farthest_pair[1])), round(float(sep_mall[farthest_pair]), 3))
# --8<-- [end:mall]
