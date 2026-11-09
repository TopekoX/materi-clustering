"""Level 3, Bab 5: jarak Euclidean, Manhattan, Minkowski, dan cosine.

Jalankan dari folder utama proyek:
    python examples/level-3/05_distance_metrics.py
"""
# NB: setup=Dua titik contoh | manual=Menghitung dengan rumus | sklearn=Memeriksa dengan scikit-learn | cosine=Cosine similarity dan cosine distance | shape=Bentuk jarak sama pada setiap metrik | scale=Pengaruh skala fitur | plot=Visualisasi arah vektor

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

A = np.array([1.0, 2.0])
B = np.array([4.0, 6.0])
print("Selisih per fitur (B - A):", B - A)
print("Selisih mutlak           :", np.abs(B - A))
# --8<-- [end:setup]

import _savefig

_savefig.install(["05-bentuk-jarak", "05-cosine-arah"])

# --8<-- [start:manual]
euclidean = np.sqrt(np.sum((A - B) ** 2))
manhattan = np.sum(np.abs(A - B))
p = 3
minkowski_p3 = np.sum(np.abs(A - B) ** p) ** (1 / p)
chebyshev = np.max(np.abs(A - B))

print("Euclidean       :", round(float(euclidean), 4))
print("Manhattan       :", round(float(manhattan), 4))
print("Minkowski (p=3) :", round(float(minkowski_p3), 4))
print("Chebyshev (max) :", round(float(chebyshev), 4))
print("Minkowski p=1 sama dengan Manhattan?", np.isclose(np.sum(np.abs(A - B) ** 1) ** 1, manhattan))
print("Minkowski p=2 sama dengan Euclidean?", np.isclose(np.sum(np.abs(A - B) ** 2) ** (1 / 2), euclidean))
# --8<-- [end:manual]

# --8<-- [start:sklearn]
pair = np.vstack([A, B])
for name, kwargs in [
    ("euclidean", {}),
    ("manhattan", {}),
    ("minkowski", {"p": 3}),
]:
    value = pairwise_distances(pair, metric=name, **kwargs)[0, 1]
    print(f"scikit-learn {name:<10}:", round(float(value), 4))
# --8<-- [end:sklearn]

# --8<-- [start:cosine]
u = np.array([1.0, 2.0])
v = np.array([2.0, 4.0])   # arah sama dengan u, panjang dua kali lipat
w = np.array([2.0, -1.0])  # tegak lurus terhadap u


def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))


for name, other in [("v (searah)", v), ("w (tegak lurus)", w)]:
    cs = cosine_similarity(u, other)
    print(
        f"u dan {name}: cosine similarity = {cs:.4f}, "
        f"cosine distance = {1 - cs:.4f}, Euclidean = {np.linalg.norm(u - other):.4f}"
    )
# --8<-- [end:cosine]

# --8<-- [start:shape]
theta = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(5, 5))
for p_val, color, label in [
    (1, "#0072B2", "Manhattan (p=1)"),
    (2, "#E69F00", "Euclidean (p=2)"),
    (8, "#009E73", "Minkowski (p=8)"),
]:
    c, s = np.cos(theta), np.sin(theta)
    # titik-titik yang berjarak 1 dari pusat menurut metrik Minkowski p
    r = 1 / (np.abs(c) ** p_val + np.abs(s) ** p_val) ** (1 / p_val)
    ax.plot(r * c, r * s, color=color, label=label)
ax.set_aspect("equal")
ax.set_title("Titik-titik yang berjarak 1 dari pusat")
ax.legend(fontsize=8)
plt.show()
# --8<-- [end:shape]

# --8<-- [start:scale]
df = pd.read_csv("data/mall_customers.csv")
cols = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
X = df[cols].to_numpy(dtype=float)
Xs = StandardScaler().fit_transform(X)


def nearest_neighbors(data):
    d = pairwise_distances(data)
    np.fill_diagonal(d, np.inf)
    return d.argmin(axis=1)


nn_raw = nearest_neighbors(X)
nn_scaled = nearest_neighbors(Xs)
changed = np.where(nn_raw != nn_scaled)[0]
print("Pelanggan yang tetangga terdekatnya berubah setelah standardisasi:", len(changed), "dari", len(df))

print("\nStandar deviasi tiap fitur (mentah):", dict(zip(cols, X.std(axis=0).round(2).tolist())))
print("Standar deviasi tiap fitur (standardisasi):", dict(zip(cols, Xs.std(axis=0).round(2).tolist())))

# Pilih pelanggan pertama yang tetangganya berubah dengan selisih jarak yang jelas (bukan seri)
D_raw = pairwise_distances(X)
D_std = pairwise_distances(Xs)
i = next(int(k) for k in changed if D_raw[k, nn_scaled[k]] - D_raw[k, nn_raw[k]] > 1)
rows = [i, int(nn_raw[i]), int(nn_scaled[i])]
print("\nContoh pelanggan yang tetangganya berubah: pelanggan", df.loc[i, "CustomerID"])
print("Tetangga terdekat (mentah)       : pelanggan", df.loc[nn_raw[i], "CustomerID"])
print("Tetangga terdekat (standardisasi): pelanggan", df.loc[nn_scaled[i], "CustomerID"])
print(df.loc[rows, ["CustomerID"] + cols].to_string(index=False))
print("Jarak mentah ke tetangga mentah / tetangga standardisasi :", round(float(D_raw[i, nn_raw[i]]), 2), "/", round(float(D_raw[i, nn_scaled[i]]), 2))
print("Jarak standardisasi ke tetangga mentah / tetangga standardisasi:", round(float(D_std[i, nn_raw[i]]), 2), "/", round(float(D_std[i, nn_scaled[i]]), 2))
# --8<-- [end:scale]

# --8<-- [start:plot]
fig, ax = plt.subplots(figsize=(5, 4.5))
origin = np.zeros(2)
for vec, label, color in [(u, "u = (1, 2)", "#0072B2"), (v, "v = (2, 4)", "#E69F00"), (w, "w = (2, -1)", "#D55E00")]:
    ax.annotate("", xy=vec, xytext=origin, arrowprops=dict(arrowstyle="->", color=color, lw=2))
    ax.text(vec[0] + 0.1, vec[1] + 0.1, label, color=color, fontsize=10)
ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-1.5, 5)
ax.axhline(0, color="gray", lw=0.5)
ax.axvline(0, color="gray", lw=0.5)
ax.set_title("Cosine membandingkan arah, bukan panjang")
plt.show()
# --8<-- [end:plot]
