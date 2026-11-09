"""Level 3, Bab 3: centroid, medoid, dan representasi kelompok.

Jalankan dari folder utama proyek:
    python examples/level-3/03_centroid_and_representation.py
"""
# NB: setup=Data kecil untuk dihitung manual | centroid=Menghitung centroid | medoid=Menghitung medoid | outlier=Centroid vs medoid saat ada outlier | move=Centroid berpindah saat anggota berubah | mall=Centroid pada Mall Customers | plot=Visualisasi centroid

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

# Lima pelanggan kecil: (pendapatan, skor belanja)
points = np.array([[2, 3], [3, 5], [4, 4], [3, 2], [8, 8]], dtype=float)
names = ["P1", "P2", "P3", "P4", "P5"]
print(pd.DataFrame(points, index=names, columns=["x1", "x2"]))
# --8<-- [end:setup]

import _savefig

_savefig.install(["03-centroid-vs-medoid", "03-centroid-berpindah", "03-centroid-mall"])

# --8<-- [start:centroid]
n = len(points)
centroid = points.sum(axis=0) / n
print("Jumlah per kolom:", points.sum(axis=0))
print("Jumlah titik n  :", n)
print("Centroid        :", centroid)
print("Sama dengan points.mean(axis=0)?", np.allclose(centroid, points.mean(axis=0)))
# --8<-- [end:centroid]

# --8<-- [start:medoid]
def distance_matrix(X):
    diff = X[:, None, :] - X[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))

D = distance_matrix(points)
total = D.sum(axis=1)
medoid_index = total.argmin()

print("Jumlah jarak tiap titik ke semua titik lain:")
for name, value in zip(names, total.round(2)):
    print(f"  {name}: {value}")
print("Medoid:", names[medoid_index], points[medoid_index])
# --8<-- [end:medoid]

# --8<-- [start:outlier]
with_outlier = np.vstack([points, [[30, 30]]])
c_before = points.mean(axis=0)
c_after = with_outlier.mean(axis=0)

D2 = distance_matrix(with_outlier)
medoid_after = with_outlier[D2.sum(axis=1).argmin()]

print("Centroid sebelum outlier:", c_before.round(2))
print("Centroid sesudah outlier:", c_after.round(2))
print("Medoid sebelum outlier  :", points[medoid_index])
print("Medoid sesudah outlier  :", medoid_after)
# --8<-- [end:outlier]

# --8<-- [start:move]
start = np.array([[2.0, 2.0], [7.0, 7.0]])  # dua tebakan pusat awal
print("Pusat awal:\n", start)

d = np.sqrt(((points[:, None, :] - start[None, :, :]) ** 2).sum(axis=2))
assign = d.argmin(axis=1)
print("Kelompok tiap titik:", dict(zip(names, assign.tolist())))

new_centers = np.array([points[assign == k].mean(axis=0) for k in range(2)])
print("Pusat baru (rata-rata anggota):\n", new_centers)
print("Pergeseran pusat:", np.sqrt(((new_centers - start) ** 2).sum(axis=1)).round(2))
# --8<-- [end:move]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
cols = ["Annual Income (k$)", "Spending Score (1-100)"]
model = KMeans(n_clusters=5, n_init=10, random_state=42).fit(df[cols])
df["Cluster"] = model.labels_

by_mean = df.groupby("Cluster")[cols].mean()
print("Rata-rata per kelompok (groupby):")
print(by_mean.round(2))
print("\nCentroid dari KMeans:")
print(pd.DataFrame(model.cluster_centers_, columns=cols).round(2))
print("\nSama?", np.allclose(by_mean.to_numpy(), model.cluster_centers_))
# --8<-- [end:mall]

# --8<-- [start:plot]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, pts, title in [
    (axes[0], points, "Tanpa outlier"),
    (axes[1], with_outlier, "Dengan outlier (30, 30)"),
]:
    c = pts.mean(axis=0)
    m = pts[distance_matrix(pts).sum(axis=1).argmin()]
    ax.scatter(pts[:, 0], pts[:, 1], s=50, color="#555555", label="Data")
    ax.scatter(*c, marker="X", s=180, color="#D55E00", label="Centroid")
    ax.scatter(*m, marker="D", s=110, color="#0072B2", label="Medoid")
    ax.set_title(title)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
axes[0].legend(fontsize=8, loc="upper left")
fig.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.scatter(points[:, 0], points[:, 1], s=60, color="#555555", label="Data")
ax.scatter(start[:, 0], start[:, 1], marker="s", s=100, color="#E69F00", label="Pusat awal")
ax.scatter(new_centers[:, 0], new_centers[:, 1], marker="X", s=160, color="#D55E00", label="Pusat baru")
for i in range(2):
    ax.annotate("", xy=new_centers[i], xytext=start[i], arrowprops=dict(arrowstyle="->", color="black"))
ax.set_title("Pusat berpindah mengikuti anggota")
ax.legend(fontsize=8)
plt.show()

colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00"]
fig, ax = plt.subplots(figsize=(6, 4.8))
for k in range(5):
    sub = df[df["Cluster"] == k]
    ax.scatter(sub[cols[0]], sub[cols[1]], s=18, color=colors[k], alpha=0.8)
    cx, cy = model.cluster_centers_[k]
    ax.annotate(f"μ{k}", (cx, cy), fontsize=11, weight="bold", ha="center", va="center",
                bbox=dict(boxstyle="round", fc="white", ec="black"))
ax.set_xlabel(cols[0])
ax.set_ylabel(cols[1])
ax.set_title("Centroid tiap kelompok")
plt.show()
# --8<-- [end:plot]
