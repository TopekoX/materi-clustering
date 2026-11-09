"""Level 3, Bab 2: memahami kelompok (cluster) lewat data sintetis dan Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-3/02_understanding_clusters.py
"""
# NB: setup=Membuat data sintetis | plot_two=Menggambar dua dataset | compact=Kekompakan (compactness) | separate=Keterpisahan (separation) | density=Kepadatan (density) | shape=Bentuk dan ukuran | member=Keanggotaan (membership) | mall=Kelompok Mall Customers

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
from sklearn.cluster import KMeans

COLORS = ["#0072B2", "#E69F00", "#009E73"]

# Dataset A: tiga gerombol berjauhan. Dataset B: tiga gerombol yang saling menumpuk.
centers = [(0, 0), (6, 0), (3, 5)]
XA, yA = make_blobs(n_samples=150, centers=centers, cluster_std=0.6, random_state=42)
XB, yB = make_blobs(n_samples=150, centers=centers, cluster_std=1.8, random_state=42)

print("Bentuk XA:", XA.shape, "| Bentuk XB:", XB.shape)
print("Jumlah anggota per kelompok (A):", np.bincount(yA))
# --8<-- [end:setup]

import _savefig

_savefig.install(["02-terpisah-vs-tumpang-tindih", "02-bentuk-dan-ukuran", "02-keanggotaan-batas"])

# --8<-- [start:plot_two]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharex=True, sharey=True)
for ax, X, y, title in [
    (axes[0], XA, yA, "A: terpisah jelas"),
    (axes[1], XB, yB, "B: tumpang tindih"),
]:
    for k in range(3):
        ax.scatter(X[y == k, 0], X[y == k, 1], s=20, color=COLORS[k], label=f"Kelompok {k}")
    ax.set_title(title)
    ax.set_xlabel("Fitur 1")
axes[0].set_ylabel("Fitur 2")
axes[0].legend(fontsize=8)
fig.tight_layout()
plt.show()
# --8<-- [end:plot_two]

# --8<-- [start:compact]
def compactness(X, y):
    """Rata-rata jarak setiap titik ke pusat kelompoknya, per kelompok."""
    result = []
    for k in np.unique(y):
        members = X[y == k]
        center = members.mean(axis=0)
        dist = np.sqrt(((members - center) ** 2).sum(axis=1))
        result.append(dist.mean())
    return np.array(result)

print("Kekompakan dataset A:", compactness(XA, yA).round(2))
print("Kekompakan dataset B:", compactness(XB, yB).round(2))
# --8<-- [end:compact]

# --8<-- [start:separate]
def center_distances(X, y):
    """Jarak antar pusat kelompok untuk setiap pasangan kelompok."""
    centers = np.array([X[y == k].mean(axis=0) for k in np.unique(y)])
    pairs = {}
    for i in range(len(centers)):
        for j in range(i + 1, len(centers)):
            pairs[(i, j)] = np.sqrt(((centers[i] - centers[j]) ** 2).sum())
    return pairs

for name, X, y in [("A", XA, yA), ("B", XB, yB)]:
    pairs = center_distances(X, y)
    print(f"Jarak antar pusat dataset {name}:", {k: round(float(v), 2) for k, v in pairs.items()})
    ratio = min(pairs.values()) / compactness(X, y).mean()
    print(f"  Jarak pusat terdekat / rata-rata kekompakan = {ratio:.2f}")
# --8<-- [end:separate]

# --8<-- [start:density]
def mean_nearest_neighbor(X):
    """Rata-rata jarak setiap titik ke tetangga terdekatnya. Makin kecil, makin padat."""
    diff = X[:, None, :] - X[None, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    np.fill_diagonal(dist, np.inf)
    return dist.min(axis=1).mean()

rng = np.random.default_rng(42)
padat = rng.normal(loc=(0, 0), scale=0.3, size=(60, 2))
jarang = rng.normal(loc=(0, 0), scale=1.5, size=(60, 2))
print("Jarak tetangga terdekat, kelompok padat  :", round(mean_nearest_neighbor(padat), 3))
print("Jarak tetangga terdekat, kelompok jarang :", round(mean_nearest_neighbor(jarang), 3))
# --8<-- [end:density]

# --8<-- [start:shape]
Xm, ym = make_moons(n_samples=200, noise=0.07, random_state=42)

rng = np.random.default_rng(42)
besar = rng.normal(loc=(0, 0), scale=1.6, size=(150, 2))
kecil = rng.normal(loc=(6, 0), scale=0.3, size=(15, 2))

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for k in range(2):
    axes[0].scatter(Xm[ym == k, 0], Xm[ym == k, 1], s=20, color=COLORS[k])
axes[0].set_title("Bentuk melengkung (bukan bola)")
axes[1].scatter(besar[:, 0], besar[:, 1], s=20, color=COLORS[0], label="150 titik")
axes[1].scatter(kecil[:, 0], kecil[:, 1], s=20, color=COLORS[1], label="15 titik")
axes[1].set_title("Ukuran dan kepadatan berbeda")
axes[1].legend(fontsize=8)
fig.tight_layout()
plt.show()
# --8<-- [end:shape]

# --8<-- [start:member]
centers_B = np.array([XB[yB == k].mean(axis=0) for k in range(3)])
# Titik tepat di tengah antara pusat kelompok 0 dan 1 (bagian batas kelompok)
titik = (centers_B[0] + centers_B[1]) / 2 + np.array([0.0, 0.3])
dist = np.sqrt(((centers_B - titik) ** 2).sum(axis=1))
print("Titik uji:", titik.round(2))
print("Jarak titik ke pusat tiap kelompok:", dist.round(2))
print("Kelompok terdekat:", dist.argmin())

fig, ax = plt.subplots(figsize=(5.5, 4.5))
for k in range(3):
    ax.scatter(XB[yB == k, 0], XB[yB == k, 1], s=18, color=COLORS[k], alpha=0.7)
ax.scatter(*titik, marker="*", s=300, color="black", label="Titik di batas")
ax.scatter(centers_B[:, 0], centers_B[:, 1], marker="X", s=100, color="black")
ax.set_title("Titik di dekat batas: keanggotaannya ambigu")
ax.legend(fontsize=8)
plt.show()
# --8<-- [end:member]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
X = df[["Annual Income (k$)", "Spending Score (1-100)"]].to_numpy()
labels = KMeans(n_clusters=5, n_init=10, random_state=42).fit_predict(X)

table = pd.DataFrame(
    {
        "Jumlah": np.bincount(labels),
        "Kekompakan": compactness(X, labels).round(1),
    }
)
print(table)
# --8<-- [end:mall]
