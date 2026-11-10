"""Level 5, Bab 5: Silhouette Score.

Jalankan dari folder utama proyek:
    python examples/level-5/05_silhouette_score.py
"""
# NB: setup=Siapkan alat | tiny=Tujuh titik dan dua kelompok | manual=Silhouette satu titik dihitung manual | check=Mencocokkan dengan scikit-learn | blobs=Silhouette pada data tiga gerombol | silplot=Fungsi untuk silhouette plot | plotblobs=Silhouette plot untuk K = 2, 3, 4 | params=Parameter metric, sample_size, dan random_state | errors=Syarat jumlah label | noise=Silhouette pada hasil DBSCAN dengan noise | plotnoise=Menggambar hasil DBSCAN | misleading=Ketika skor tinggi menyesatkan | mall=Silhouette pada Mall Customers | plotmall=Silhouette plot Mall Customers

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
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import pairwise_distances, silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["05-silhouette-plot-k", "05-dbscan-noise", "05-silhouette-mall"])

# --8<-- [start:tiny]
# Tujuh titik. Titik terakhir (4, 3) berada di antara dua kelompok.
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2], [4, 3],   # kelompok 0
        [6, 5], [7, 5], [6, 6],           # kelompok 1
    ],
    dtype=float,
)
labels_tiny = np.array([0, 0, 0, 0, 1, 1, 1])
# --8<-- [end:tiny]

# --8<-- [start:manual]
def silhouette_manual(X, labels, i):
    """Mengembalikan a(i), b(i), s(i) untuk titik ke-i."""
    d = np.linalg.norm(X - X[i], axis=1)          # jarak titik i ke semua titik
    own = labels == labels[i]
    own[i] = False                                 # buang titik i sendiri
    a = d[own].mean()                              # rata-rata jarak ke kelompok sendiri
    other_means = [d[labels == k].mean() for k in np.unique(labels) if k != labels[i]]
    b = min(other_means)                           # rata-rata jarak ke kelompok tetangga terdekat
    s = (b - a) / max(a, b)
    return a, b, s


for i in (0, 3):
    a, b, s = silhouette_manual(X_tiny, labels_tiny, i)
    print(f"Titik {i} {X_tiny[i].tolist()}: a = {a:.3f}, b = {b:.3f}, s = {s:.3f}")
# --8<-- [end:manual]

# --8<-- [start:check]
manual_all = np.array([silhouette_manual(X_tiny, labels_tiny, i)[2] for i in range(len(X_tiny))])
sk_all = silhouette_samples(X_tiny, labels_tiny)
print("s(i) manual      :", manual_all.round(3).tolist())
print("s(i) scikit-learn:", sk_all.round(3).tolist())
print(f"Rata-rata manual       : {manual_all.mean():.3f}")
print(f"silhouette_score       : {silhouette_score(X_tiny, labels_tiny):.3f}")
# --8<-- [end:check]

# --8<-- [start:blobs]
X_blobs, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.2, random_state=42)
rows = []
for k in (2, 3, 4, 5):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_blobs)
    s = silhouette_samples(X_blobs, labels)
    rows.append(
        {
            "K": k,
            "Silhouette": s.mean(),
            "Titik negatif": int((s < 0).sum()),
            "Rata-rata per kelompok": [round(float(s[labels == c].mean()), 3) for c in range(k)],
        }
    )
print(pd.DataFrame(rows).set_index("K").to_string())
# --8<-- [end:blobs]

# --8<-- [start:silplot]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]


def silhouette_plot(ax, X, labels):
    """Silhouette plot: satu 'pita' per kelompok, titik diurutkan menurut s(i)."""
    s = silhouette_samples(X, labels)
    y_lower = 10
    for k in np.unique(labels):
        values = np.sort(s[labels == k])
        y_upper = y_lower + len(values)
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, values, color=palette[k % len(palette)], alpha=0.8)
        ax.text(-0.05, y_lower + 0.5 * len(values), str(k), fontsize=9)
        y_lower = y_upper + 10
    ax.axvline(s.mean(), color="black", linestyle="--", label=f"Rata-rata = {s.mean():.3f}")
    ax.set_xlim(-0.2, 1.0)
    ax.set_yticks([])
    ax.set_xlabel("Silhouette coefficient s(i)")
    ax.legend(fontsize=8, loc="lower right")
# --8<-- [end:silplot]

# --8<-- [start:plotblobs]
fig, axes = plt.subplots(2, 3, figsize=(14, 7.5))
for col, k in enumerate((2, 3, 4)):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_blobs)
    for c in range(k):
        axes[0, col].scatter(X_blobs[labels == c, 0], X_blobs[labels == c, 1], s=14, color=palette[c])
    axes[0, col].set_title(f"K = {k}")
    axes[0, col].set_xlabel("Fitur 1")
    silhouette_plot(axes[1, col], X_blobs, labels)
axes[0, 0].set_ylabel("Fitur 2")
axes[1, 0].set_ylabel("Kelompok (nomor di sisi kiri pita)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotblobs]

# --8<-- [start:params]
X_big, _ = make_blobs(n_samples=3000, centers=4, cluster_std=1.5, random_state=42)
labels_big = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X_big)

print(f"Penuh (3000 titik)            : {silhouette_score(X_big, labels_big):.4f}")
for seed in (0, 1, 2):
    sampled = silhouette_score(X_big, labels_big, sample_size=500, random_state=seed)
    print(f"sample_size=500, random_state={seed}: {sampled:.4f}")

print(f"metric='euclidean'            : {silhouette_score(X_big, labels_big, metric='euclidean'):.4f}")
print(f"metric='manhattan'            : {silhouette_score(X_big, labels_big, metric='manhattan'):.4f}")
print(f"Skala data x 10               : {silhouette_score(X_big * 10, labels_big):.4f}")
# --8<-- [end:params]

# --8<-- [start:errors]
for name, bad_labels in {
    "satu kelompok": np.zeros(len(X_tiny), dtype=int),
    "setiap titik kelompok sendiri": np.arange(len(X_tiny)),
}.items():
    try:
        silhouette_score(X_tiny, bad_labels)
    except ValueError as err:
        print(f"{name}: ValueError -> {err}")
# --8<-- [end:errors]

# --8<-- [start:noise]
# Tiga gerombol ditambah 40 titik noise yang tersebar di seluruh area
X_core, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.7, random_state=42)
rng = np.random.default_rng(42)
noise_points = rng.uniform(X_core.min(axis=0) - 2, X_core.max(axis=0) + 2, size=(40, 2))
X_noisy = np.vstack([X_core, noise_points])

db_labels = DBSCAN(eps=0.7, min_samples=6).fit_predict(X_noisy)
n_noise = int((db_labels == -1).sum())
clusters_found = sorted(int(c) for c in set(db_labels) - {-1})
print("Kelompok ditemukan:", clusters_found, "| titik noise (label -1):", n_noise, "dari", len(X_noisy))

# Cara 1: noise ikut dihitung sebagai satu 'kelompok' berlabel -1
print(f"Silhouette, noise dianggap kelompok : {silhouette_score(X_noisy, db_labels):.3f}")
# Cara 2: noise dikeluarkan lebih dulu
mask = db_labels != -1
print(f"Silhouette, noise dikeluarkan       : {silhouette_score(X_noisy[mask], db_labels[mask]):.3f}  ({mask.sum()} titik dinilai)")
# --8<-- [end:noise]

# --8<-- [start:plotnoise]
fig, ax = plt.subplots(figsize=(6.5, 5))
for c in clusters_found:
    ax.scatter(X_noisy[db_labels == c, 0], X_noisy[db_labels == c, 1], s=14, color=palette[c % len(palette)], label=f"Kelompok {c}")
ax.scatter(X_noisy[~mask, 0], X_noisy[~mask, 1], s=30, marker="x", color="gray", label="Noise (-1)")
ax.set_xlabel("Fitur 1")
ax.set_ylabel("Fitur 2")
ax.set_title("DBSCAN pada data dengan noise")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotnoise]

# --8<-- [start:misleading]
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
km_labels = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_moons)
db_moons = DBSCAN(eps=0.2, min_samples=5).fit_predict(X_moons)
print("DBSCAN pada moons menemukan kelompok:", sorted(int(c) for c in set(db_moons)))
print(f"Silhouette K-Means (memotong bulan) : {silhouette_score(X_moons, km_labels):.3f}")
print(f"Silhouette DBSCAN (mengikuti bulan) : {silhouette_score(X_moons, db_moons):.3f}")
# --8<-- [end:misleading]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])
labels_mall = KMeans(n_clusters=5, n_init=10, random_state=42).fit_predict(X_mall)

s_mall = silhouette_samples(X_mall, labels_mall)
summary = pd.DataFrame(
    {
        "Ukuran": np.bincount(labels_mall),
        "Rata-rata s(i)": [s_mall[labels_mall == c].mean() for c in range(5)],
        "s(i) minimum": [s_mall[labels_mall == c].min() for c in range(5)],
        "Titik s(i) < 0": [int((s_mall[labels_mall == c] < 0).sum()) for c in range(5)],
    }
)
print(summary.round(3).to_string())
print(f"Silhouette keseluruhan: {s_mall.mean():.3f}")
# --8<-- [end:mall]

# --8<-- [start:plotmall]
fig, ax = plt.subplots(figsize=(6.5, 5))
silhouette_plot(ax, X_mall, labels_mall)
ax.set_title("Silhouette plot Mall Customers (K = 5)")
ax.set_ylabel("Kelompok")
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
