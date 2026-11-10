"""Level 4, Bab 1: mengenal keluarga algoritma clustering di scikit-learn.

Jalankan dari folder utama proyek:
    python examples/level-4/01_introduction_to_clustering_algorithms.py
"""
# NB: setup=Siapkan alat | data=Membuat dua dataset sintetis | plotdata=Melihat kedua dataset | models=Membuat lima algoritma | fit=Menjalankan semua algoritma pada data blobs | table=Membandingkan kemampuan tiap objek | grid=Menjalankan lima algoritma pada dua dataset | plotgrid=Menggambar hasil

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
from sklearn.datasets import make_blobs, make_moons
from sklearn.cluster import (
    KMeans,
    AgglomerativeClustering,
    DBSCAN,
    MeanShift,
    estimate_bandwidth,
)
from sklearn.mixture import GaussianMixture
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-dua-dataset", "01-lima-algoritma-dua-dataset"])

# --8<-- [start:data]
# Dataset 1: tiga gerombol bulat yang terpisah jelas
X_blobs, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.8, random_state=42)

# Dataset 2: dua bentuk "bulan sabit" yang saling mengait
X_moons, _ = make_moons(n_samples=300, noise=0.07, random_state=42)

print("Bentuk X_blobs:", X_blobs.shape)
print("Bentuk X_moons:", X_moons.shape)
print("\nLima baris pertama X_blobs:")
print(pd.DataFrame(X_blobs, columns=["x1", "x2"]).head().round(3))
# --8<-- [end:data]

# --8<-- [start:plotdata]
fig, axes = plt.subplots(1, 2, figsize=(9, 4))
for ax, X, title in [
    (axes[0], X_blobs, "Dataset 1: blobs (gerombol bulat)"),
    (axes[1], X_moons, "Dataset 2: moons (bulan sabit)"),
]:
    ax.scatter(X[:, 0], X[:, 1], s=18, color="#444444")
    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotdata]


# --8<-- [start:models]
def build_models(n_clusters, eps, bandwidth):
    """Membuat lima algoritma dengan pengaturan awal yang masuk akal."""
    return {
        "K-Means": KMeans(n_clusters=n_clusters, n_init=10, random_state=42),
        "Hierarchical (Ward)": AgglomerativeClustering(n_clusters=n_clusters, linkage="ward"),
        "DBSCAN": DBSCAN(eps=eps, min_samples=5),
        "GMM": GaussianMixture(n_components=n_clusters, random_state=42),
        "Mean Shift": MeanShift(bandwidth=bandwidth),
    }
# --8<-- [end:models]


# --8<-- [start:fit]
bw_blobs = estimate_bandwidth(X_blobs, quantile=0.2, random_state=42)
models = build_models(n_clusters=3, eps=0.7, bandwidth=bw_blobs)

print(f"Bandwidth Mean Shift (hasil estimate_bandwidth): {bw_blobs:.3f}\n")
for name, model in models.items():
    labels = model.fit_predict(X_blobs)
    values, counts = np.unique(labels, return_counts=True)
    print(f"{name:<20} label unik: {values.tolist()}  jumlah anggota: {counts.tolist()}")
# --8<-- [end:fit]

# --8<-- [start:table]
rows = []
for name, model in models.items():
    rows.append(
        {
            "Algoritma": name,
            "punya labels_": hasattr(model, "labels_"),
            "punya predict()": hasattr(model, "predict"),
            "punya predict_proba()": hasattr(model, "predict_proba"),
            "punya pusat": hasattr(model, "cluster_centers_") or hasattr(model, "means_"),
        }
    )
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:table]

# --8<-- [start:grid]
bw_moons = estimate_bandwidth(X_moons, quantile=0.2, random_state=42)
settings = {
    "blobs": dict(X=X_blobs, n_clusters=3, eps=0.7, bandwidth=bw_blobs),
    "moons": dict(X=X_moons, n_clusters=2, eps=0.2, bandwidth=bw_moons),
}

results = {}  # (nama dataset, nama algoritma) -> label
for data_name, cfg in settings.items():
    X = cfg["X"]
    models = build_models(cfg["n_clusters"], cfg["eps"], cfg["bandwidth"])
    for algo_name, model in models.items():
        results[(data_name, algo_name)] = model.fit_predict(X)

print("Jumlah kelompok (tanpa noise) dan jumlah noise per algoritma:")
for (data_name, algo_name), labels in results.items():
    n_clusters = len(set(labels) - {-1})
    n_noise = int(np.sum(labels == -1))
    print(f"{data_name:<6} {algo_name:<20} kelompok: {n_clusters}  noise: {n_noise}")
# --8<-- [end:grid]

# --8<-- [start:plotgrid]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]
algo_names = list(build_models(3, 0.7, 1.0).keys())

fig, axes = plt.subplots(2, 5, figsize=(15, 6.2))
for row, (data_name, cfg) in enumerate(settings.items()):
    X = cfg["X"]
    for col, algo_name in enumerate(algo_names):
        ax = axes[row, col]
        labels = results[(data_name, algo_name)]
        for k in sorted(set(labels)):
            mask = labels == k
            if k == -1:  # noise DBSCAN digambar abu-abu
                ax.scatter(X[mask, 0], X[mask, 1], s=16, color="#999999", marker="x")
            else:
                ax.scatter(X[mask, 0], X[mask, 1], s=16, color=palette[k % len(palette)])
        if row == 0:
            ax.set_title(algo_name)
        ax.set_xticks([])
        ax.set_yticks([])
    axes[row, 0].set_ylabel(data_name)
plt.tight_layout()
plt.show()
# --8<-- [end:plotgrid]
