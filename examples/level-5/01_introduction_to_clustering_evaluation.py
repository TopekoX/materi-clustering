"""Level 5, Bab 1: Pengantar evaluasi clustering.

Jalankan dari folder utama proyek:
    python examples/level-5/01_introduction_to_clustering_evaluation.py
"""
# NB: setup=Siapkan alat | data=Tiga dataset untuk dibandingkan | fit=Menjalankan K-Means pada tiap dataset | scores=Tiga skor pertama | plot=Menggambar tiga dataset | relative=Evaluasi relatif: membandingkan beberapa nilai K | noclusters=Data tanpa kelompok alami | plotrel=Menggambar skor tiap K | mall=Evaluasi pada Mall Customers

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
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-tiga-dataset", "01-skor-tiap-k"])

# --8<-- [start:data]
# Tiga dataset dengan 300 titik dan 3 pusat yang sama.
# Bedanya hanya cluster_std: seberapa lebar sebaran tiap kelompok.
X_clear, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.6, random_state=42)
X_overlap, _ = make_blobs(n_samples=300, centers=3, cluster_std=3.0, random_state=42)

# Data tanpa kelompok alami: titik tersebar rata di sebuah persegi
rng = np.random.default_rng(42)
X_uniform = rng.uniform(low=-10, high=10, size=(300, 2))

datasets = {
    "Kelompok jelas": X_clear,
    "Kelompok tumpang tindih": X_overlap,
    "Tanpa kelompok alami": X_uniform,
}
for name, X in datasets.items():
    print(f"{name:25s} bentuk data: {X.shape}")
# --8<-- [end:data]

# --8<-- [start:fit]
labels_by_name = {}
for name, X in datasets.items():
    model = KMeans(n_clusters=3, n_init=10, random_state=42)
    labels_by_name[name] = model.fit_predict(X)
    print(f"{name:25s} ukuran kelompok: {np.bincount(labels_by_name[name]).tolist()}")
# --8<-- [end:fit]

# --8<-- [start:scores]
rows = []
for name, X in datasets.items():
    labels = labels_by_name[name]
    rows.append(
        {
            "Dataset": name,
            "Silhouette": silhouette_score(X, labels),
            "Davies-Bouldin": davies_bouldin_score(X, labels),
            "Calinski-Harabasz": calinski_harabasz_score(X, labels),
        }
    )
score_table = pd.DataFrame(rows).set_index("Dataset")
print(score_table.round(3))
# --8<-- [end:scores]

# --8<-- [start:plot]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
for ax, (name, X) in zip(axes, datasets.items()):
    labels = labels_by_name[name]
    for j in range(3):
        ax.scatter(X[labels == j, 0], X[labels == j, 1], s=14, color=palette[j])
    sil = score_table.loc[name, "Silhouette"]
    ax.set_title(f"{name}\nSilhouette = {sil:.3f}")
    ax.set_xlabel("Fitur 1")
    ax.set_ylabel("Fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:relative]
# Evaluasi relatif: jalankan K-Means dengan K berbeda, bandingkan skornya
k_values = range(2, 8)
rel_rows = []
for k in k_values:
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_clear)
    rel_rows.append({"K": k, "Silhouette": silhouette_score(X_clear, labels)})
rel_table = pd.DataFrame(rel_rows).set_index("K")
print(rel_table.round(3))
best_k = rel_table["Silhouette"].idxmax()
print("K dengan Silhouette tertinggi:", best_k)
# --8<-- [end:relative]

# --8<-- [start:noclusters]
# Data tanpa kelompok alami juga mendapat skor, dan K-Means tetap menghasilkan kelompok
uniform_rows = []
for k in range(2, 6):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_uniform)
    uniform_rows.append({"K": k, "Silhouette": silhouette_score(X_uniform, labels)})
print(pd.DataFrame(uniform_rows).set_index("K").round(3))
# --8<-- [end:noclusters]

# --8<-- [start:plotrel]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(rel_table.index, rel_table["Silhouette"], marker="o", color=palette[0], label="Kelompok jelas")
uniform_table = pd.DataFrame(uniform_rows).set_index("K")
ax.plot(uniform_table.index, uniform_table["Silhouette"], marker="s", color=palette[1], label="Tanpa kelompok alami")
ax.set_xlabel("Jumlah kelompok (K)")
ax.set_ylabel("Silhouette Score")
ax.set_title("Skor Silhouette untuk tiap nilai K")
ax.legend()
plt.tight_layout()
plt.show()
# --8<-- [end:plotrel]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

labels_mall = KMeans(n_clusters=5, n_init=10, random_state=42).fit_predict(X_mall)
print("Ukuran kelompok:", np.bincount(labels_mall).tolist())
print(f"Silhouette        : {silhouette_score(X_mall, labels_mall):.3f}")
print(f"Davies-Bouldin    : {davies_bouldin_score(X_mall, labels_mall):.3f}")
print(f"Calinski-Harabasz : {calinski_harabasz_score(X_mall, labels_mall):.1f}")
# --8<-- [end:mall]
