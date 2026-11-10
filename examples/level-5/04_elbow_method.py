"""Level 5, Bab 4: Elbow Method.

Jalankan dari folder utama proyek:
    python examples/level-5/04_elbow_method.py
"""
# NB: setup=Siapkan alat | data=Tiga dataset dengan kejelasan berbeda | curve=Menghitung kurva Inertia | drops=Persentase penurunan tiap langkah | plotcurve=Menggambar tiga kurva elbow | elbowfunc=Mencari siku dengan jarak ke garis | findelbow=Siku menurut heuristik | range=Siku berubah bila rentang K berubah | mall=Elbow pada Mall Customers | plotmall=Menggambar elbow Mall Customers

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
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["04-tiga-kurva-elbow", "04-elbow-mall"])

# --8<-- [start:data]
# Tiga dataset, semuanya 400 titik
X_clear, _ = make_blobs(n_samples=400, centers=4, cluster_std=0.8, random_state=42)
X_overlap, _ = make_blobs(n_samples=400, centers=4, cluster_std=2.5, random_state=42)
X_uniform = np.random.default_rng(42).uniform(-10, 10, size=(400, 2))

datasets = {
    "4 gerombol jelas": X_clear,
    "4 gerombol tumpang tindih": X_overlap,
    "Tanpa kelompok alami": X_uniform,
}
# --8<-- [end:data]

# --8<-- [start:curve]
k_values = list(range(1, 11))


def inertia_curve(X, k_values):
    """Inertia K-Means untuk tiap nilai K."""
    return [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_ for k in k_values]


curves = {name: inertia_curve(X, k_values) for name, X in datasets.items()}

table = pd.DataFrame(curves, index=k_values)
table.index.name = "K"
print(table.round(1).to_string())
# --8<-- [end:curve]

# --8<-- [start:drops]
# Penurunan sebagai persen dari Inertia sebelumnya
drop_pct = table.pct_change().mul(-100)
print(drop_pct.round(1).to_string())
# --8<-- [end:drops]

# --8<-- [start:plotcurve]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, (name, values) in zip(axes, curves.items()):
    ax.plot(k_values, values, marker="o", color=palette[0])
    ax.set_title(name)
    ax.set_xlabel("Jumlah kelompok (K)")
    ax.set_xticks(k_values)
axes[0].set_ylabel("Inertia (WCSS)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotcurve]

# --8<-- [start:elbowfunc]
def elbow_by_line(k_values, inertias):
    """Heuristik siku: titik yang paling jauh dari garis lurus antara titik pertama dan terakhir.

    Kedua sumbu diskalakan ke rentang 0-1 dulu supaya satuan K dan Inertia setara.
    Ini hanya heuristik pembantu, bukan penentu jumlah kelompok yang benar.
    """
    x = np.array(k_values, dtype=float)
    y = np.array(inertias, dtype=float)
    x = (x - x.min()) / (x.max() - x.min())
    y = (y - y.min()) / (y.max() - y.min())
    start, end = np.array([x[0], y[0]]), np.array([x[-1], y[-1]])
    line = end - start
    line = line / np.linalg.norm(line)
    points = np.column_stack([x, y]) - start
    # jarak tegak lurus titik ke garis = panjang komponen yang tegak lurus garis
    distances = np.abs(points[:, 0] * line[1] - points[:, 1] * line[0])
    return k_values[int(distances.argmax())], distances
# --8<-- [end:elbowfunc]

# --8<-- [start:findelbow]
for name, values in curves.items():
    k_elbow, distances = elbow_by_line(k_values, values)
    top_two = np.sort(distances)[-2:][::-1]
    print(f"{name:27s} siku heuristik: K = {k_elbow}   (jarak terbesar {top_two[0]:.3f}, kedua {top_two[1]:.3f})")
# --8<-- [end:findelbow]

# --8<-- [start:range]
# Heuristik yang sama, tetapi rentang K dibuat berbeda
print("Rentang K      Dataset                     Siku heuristik")
for k_max in (6, 10, 15):
    ks = list(range(1, k_max + 1))
    for name, X in datasets.items():
        k_elbow, _ = elbow_by_line(ks, inertia_curve(X, ks))
        print(f"1 sampai {k_max:<4d}  {name:27s} K = {k_elbow}")
# --8<-- [end:range]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

mall_k = list(range(1, 11))
mall_inertia = inertia_curve(X_mall, mall_k)
mall_elbow, _ = elbow_by_line(mall_k, mall_inertia)
print("Siku heuristik Mall Customers: K =", mall_elbow)

# Pembanding: Silhouette (dibahas di Bab 5), tidak bisa dihitung pada K = 1
mall_sil = {k: silhouette_score(X_mall, KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_mall))
            for k in range(2, 11)}
best_sil_k = max(mall_sil, key=mall_sil.get)
print("Silhouette tertinggi pada K =", best_sil_k, f"({mall_sil[best_sil_k]:.3f})")
print({k: round(v, 3) for k, v in mall_sil.items()})
# --8<-- [end:mall]

# --8<-- [start:plotmall]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(mall_k, mall_inertia, marker="o", color=palette[0])
axes[0].plot([mall_k[0], mall_k[-1]], [mall_inertia[0], mall_inertia[-1]],
             linestyle="--", color="gray", label="Garis awal-akhir")
axes[0].scatter([mall_elbow], [mall_inertia[mall_elbow - 1]], s=160, marker="o",
                facecolors="none", edgecolors=palette[4], linewidths=2, label=f"Siku heuristik (K = {mall_elbow})")
axes[0].set_xlabel("Jumlah kelompok (K)")
axes[0].set_ylabel("Inertia (WCSS)")
axes[0].set_title("Elbow pada Mall Customers")
axes[0].set_xticks(mall_k)
axes[0].legend(fontsize=8)

axes[1].plot(list(mall_sil.keys()), list(mall_sil.values()), marker="s", color=palette[1])
axes[1].set_xlabel("Jumlah kelompok (K)")
axes[1].set_ylabel("Silhouette Score")
axes[1].set_title("Pembanding: Silhouette")
axes[1].set_xticks(list(mall_sil.keys()))
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
