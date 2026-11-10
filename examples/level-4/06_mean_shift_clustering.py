"""Level 4, Bab 6: Mean Shift clustering, KDE, dan bandwidth.

Jalankan dari folder utama proyek:
    python examples/level-4/06_mean_shift_clustering.py
"""
# NB: setup=Siapkan alat | kde=Kernel Density Estimation satu dimensi | plotkde=Menggambar KDE untuk tiga bandwidth | tiny=Pergeseran satu dimensi langkah demi langkah | scratch=Mean Shift dari nol | blobs=Data blobs dan estimasi bandwidth | paths=Jalur pergeseran beberapa seed | plotpaths=Menggambar jalur pergeseran | fit=MeanShift scikit-learn | compare=Membandingkan dengan versi buatan sendiri | sweep=Pengaruh bandwidth | plotsweep=Menggambar pengaruh bandwidth | plotcenters=Menggambar pusat kelompok | options=Parameter seeds, bin_seeding, min_bin_freq, cluster_all | moons=Mean Shift pada bulan sabit | mall=Mean Shift pada Mall Customers | newpoint=Label pelanggan baru | plotmall=Menggambar hasil Mall

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
from sklearn.cluster import MeanShift, estimate_bandwidth, get_bin_seeds
from sklearn.datasets import make_blobs, make_moons
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(
    ["06-kde-bandwidth", "06-jalur-pergeseran", "06-pusat-kelompok", "06-pengaruh-bandwidth", "06-mall-customers"]
)

# --8<-- [start:kde]
def gaussian_kde_1d(grid, data, bandwidth):
    """KDE dengan kernel Gaussian: rata-rata dari 'lonceng' yang dipasang di tiap titik data."""
    u = (grid[:, None] - data[None, :]) / bandwidth            # bentuk (jumlah grid, jumlah data)
    kernel = np.exp(-0.5 * u**2) / np.sqrt(2 * np.pi)          # kernel Gaussian baku
    return kernel.sum(axis=1) / (len(data) * bandwidth)

def count_modes(density):
    """Menghitung puncak (maksimum lokal) pada kurva kepadatan."""
    return int(np.sum((density[1:-1] > density[:-2]) & (density[1:-1] > density[2:])))

rng = np.random.default_rng(42)
data_1d = np.concatenate([rng.normal(2.0, 0.6, 60), rng.normal(6.0, 0.8, 40)])  # dua gerombol
grid = np.linspace(-1, 10, 600)

for h in [0.15, 0.6, 2.5]:
    density = gaussian_kde_1d(grid, data_1d, h)
    print(f"bandwidth = {h:<4} -> jumlah puncak kepadatan = {count_modes(density)}")
# --8<-- [end:kde]

# --8<-- [start:plotkde]
fig, axes = plt.subplots(1, 3, figsize=(15, 3.8), sharey=True)
for ax, h in zip(axes, [0.15, 0.6, 2.5]):
    density = gaussian_kde_1d(grid, data_1d, h)
    ax.plot(grid, density, color="#0072B2")
    ax.plot(data_1d, np.full_like(data_1d, -0.01), "|", color="#444444", markersize=10)
    ax.set_title(f"Bandwidth = {h}: {count_modes(density)} puncak")
    ax.set_xlabel("x")
axes[0].set_ylabel("Estimasi kepadatan")
plt.tight_layout()
plt.show()
# --8<-- [end:plotkde]

# --8<-- [start:tiny]
x_tiny = np.array([1.0, 2.0, 3.0, 4.0, 10.0, 11.0, 12.0])
h_tiny = 3.0

for start in [5.0, 10.0]:
    position = start
    print(f"Mulai dari {position}")
    for step in range(1, 10):
        neighbors = x_tiny[np.abs(x_tiny - position) <= h_tiny]   # titik dalam radius bandwidth
        new_position = neighbors.mean()                            # rata-rata tetangga
        shift = new_position - position                            # vektor mean shift
        print(f"  langkah {step}: tetangga = {neighbors.tolist()}, rata-rata = {new_position}, pergeseran = {shift:+.2f}")
        position = new_position
        if abs(shift) < 1e-9:
            break
    print(f"  -> berhenti di puncak {position}\n")
# --8<-- [end:tiny]

# --8<-- [start:scratch]
def shift_seed(X, seed, bandwidth, tol=1e-3, max_iter=300):
    """Menggeser satu titik awal (seed) sampai berhenti. Mengembalikan jalur dan jumlah tetangga akhir."""
    position = seed.copy()
    path = [position.copy()]
    for _ in range(max_iter):
        distances = np.linalg.norm(X - position, axis=1)
        neighbors = X[distances <= bandwidth]            # flat kernel: semua titik dalam radius
        new_position = neighbors.mean(axis=0)            # rata-rata tetangga
        moved = np.linalg.norm(new_position - position)  # panjang vektor mean shift
        position = new_position
        path.append(position.copy())
        if moved <= tol * bandwidth:                     # hampir tidak bergeser: konvergen
            break
    return np.array(path), len(neighbors)

def mean_shift_scratch(X, bandwidth):
    """Mean Shift sederhana: semua titik data dipakai sebagai seed."""
    modes, counts = [], []
    for seed in X:
        path, n_neighbors = shift_seed(X, seed, bandwidth)
        modes.append(path[-1])
        counts.append(n_neighbors)
    modes, counts = np.array(modes), np.array(counts)

    # Mode yang berdekatan (jarak <= bandwidth) dianggap puncak yang sama.
    # Urutkan dari mode dengan tetangga terbanyak, lalu buang mode lain di dekatnya.
    order = np.lexsort((modes[:, 1], modes[:, 0], -counts))
    centers = []
    for i in order:
        if all(np.linalg.norm(modes[i] - c) > bandwidth for c in centers):
            centers.append(modes[i])
    centers = np.array(centers)

    labels = np.linalg.norm(X[:, None, :] - centers[None, :, :], axis=2).argmin(axis=1)
    return centers, labels
# --8<-- [end:scratch]

# --8<-- [start:blobs]
X, _ = make_blobs(n_samples=300, centers=3, cluster_std=1.0, random_state=42)

# estimate_bandwidth: rata-rata jarak tiap titik ke tetangga ke-k, dengan k = quantile * jumlah titik
quantile = 0.2
bw_estimated = estimate_bandwidth(X, quantile=quantile, random_state=42)

k = int(len(X) * quantile)
dist_to_kth, _ = NearestNeighbors(n_neighbors=k).fit(X).kneighbors(X)
bw_manual = dist_to_kth[:, -1].mean()

print(f"estimate_bandwidth(quantile={quantile}) = {bw_estimated:.4f}")
print(f"Hitungan manual (rata-rata jarak ke tetangga ke-{k}) = {bw_manual:.4f}")
# --8<-- [end:blobs]

# --8<-- [start:paths]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]
bandwidth = 2.0

seed_ids = np.random.default_rng(1).choice(len(X), size=12, replace=False)
seed_paths = [shift_seed(X, X[i], bandwidth)[0] for i in seed_ids]
for i, path in zip(seed_ids, seed_paths):
    print(f"seed {i:>3}: {len(path) - 1} langkah, dari {path[0].round(2).tolist()} ke puncak {path[-1].round(2).tolist()}")
# --8<-- [end:paths]

# --8<-- [start:plotpaths]
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(X[:, 0], X[:, 1], s=10, color="#BBBBBB")
for path in seed_paths:
    ax.plot(path[:, 0], path[:, 1], "-o", markersize=3, linewidth=1.2, color="#0072B2")
    ax.scatter(*path[0], s=30, color="#444444", zorder=3)
    ax.scatter(*path[-1], s=90, marker="*", color="#D55E00", zorder=4)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_title("Jalur pergeseran 12 seed (titik hitam) menuju puncak kepadatan (bintang)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotpaths]

# --8<-- [start:fit]
ms = MeanShift(bandwidth=bandwidth, bin_seeding=False)
labels = ms.fit_predict(X)

print("Jumlah kelompok :", len(ms.cluster_centers_))
print("Ukuran kelompok :", np.bincount(labels).tolist())
print("cluster_centers_:\n", ms.cluster_centers_.round(3))
print("n_iter_         :", ms.n_iter_)

ms_est = MeanShift(bandwidth=bw_estimated, bin_seeding=False).fit(X)
print(f"\nDengan bandwidth hasil estimate_bandwidth ({bw_estimated:.3f}): {len(ms_est.cluster_centers_)} kelompok, "
      f"ukuran {np.bincount(ms_est.labels_).tolist()}")
# --8<-- [end:fit]

# --8<-- [start:compare]
centers_me, labels_me = mean_shift_scratch(X, bandwidth)

sorted_me = centers_me[np.lexsort((centers_me[:, 1], centers_me[:, 0]))]
sorted_sk = ms.cluster_centers_[np.lexsort((ms.cluster_centers_[:, 1], ms.cluster_centers_[:, 0]))]

print("Versi buatan sendiri: jumlah kelompok =", len(centers_me), "| ukuran =", np.bincount(labels_me).tolist())
print("Selisih terbesar antar pusat:", round(float(np.abs(sorted_me - sorted_sk).max()), 4))
# --8<-- [end:compare]

# --8<-- [start:plotcenters]
fig, ax = plt.subplots(figsize=(7, 6))
for j in range(len(ms.cluster_centers_)):
    ax.scatter(X[labels == j, 0], X[labels == j, 1], s=14, color=palette[j])
    center = ms.cluster_centers_[j]
    ax.scatter(*center, s=220, marker="X", color="black")
    ax.add_patch(plt.Circle(center, bandwidth, fill=False, linestyle="--", edgecolor="black", alpha=0.6))
ax.set_aspect("equal")
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_title(f"Mean Shift (bandwidth = {bandwidth}): {len(ms.cluster_centers_)} kelompok; lingkaran = radius bandwidth")
plt.tight_layout()
plt.show()
# --8<-- [end:plotcenters]

# --8<-- [start:sweep]
rows = []
for bw in [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0]:
    model = MeanShift(bandwidth=bw, bin_seeding=False).fit(X)
    sizes = sorted(np.bincount(model.labels_).tolist(), reverse=True)
    rows.append({"bandwidth": bw, "kelompok": len(model.cluster_centers_), "ukuran terbesar (maks. 5)": sizes[:5]})
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:sweep]

# --8<-- [start:plotsweep]
fig, axes = plt.subplots(1, 4, figsize=(17, 4.2), sharex=True, sharey=True)
for ax, bw in zip(axes, [0.5, 1.0, 2.0, 8.0]):
    model = MeanShift(bandwidth=bw, bin_seeding=False).fit(X)
    n_found = len(model.cluster_centers_)
    for j in range(n_found):
        ax.scatter(X[model.labels_ == j, 0], X[model.labels_ == j, 1], s=10, color=palette[j % len(palette)])
    ax.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], s=90, marker="X", color="black")
    ax.set_title(f"bandwidth = {bw}: {n_found} kelompok")
    ax.set_xlabel("x1")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotsweep]

# --8<-- [start:options]
# Data blobs ditambah 10 titik acak di sekitar sebagai pencilan
outliers = np.random.default_rng(0).uniform(-12, 12, size=(10, 2))
X_out = np.vstack([X, outliers])
bw = 2.5

n_seeds_binned = len(get_bin_seeds(X_out, bw, min_bin_freq=5))
print(f"Jumlah seed: semua titik = {len(X_out)}, bin_seeding=True dengan min_bin_freq=5 = {n_seeds_binned}\n")

settings = [
    ("bin_seeding=False, cluster_all=True ", dict(bin_seeding=False, cluster_all=True)),
    ("bin_seeding=True,  min_bin_freq=5, cluster_all=True ", dict(bin_seeding=True, min_bin_freq=5, cluster_all=True)),
    ("bin_seeding=True,  min_bin_freq=5, cluster_all=False", dict(bin_seeding=True, min_bin_freq=5, cluster_all=False)),
]
for name, kwargs in settings:
    model = MeanShift(bandwidth=bw, **kwargs).fit(X_out)
    n_orphans = int(np.sum(model.labels_ == -1))
    sizes = np.bincount(model.labels_[model.labels_ >= 0]).tolist()
    print(f"{name}: {len(model.cluster_centers_)} pusat, label -1 = {n_orphans}, ukuran = {sizes}")
# --8<-- [end:options]

# --8<-- [start:moons]
X_moons, _ = make_moons(n_samples=300, noise=0.07, random_state=42)
bw_moons = estimate_bandwidth(X_moons, quantile=0.2, random_state=42)
ms_moons = MeanShift(bandwidth=bw_moons).fit(X_moons)
print(f"Bulan sabit: bandwidth = {bw_moons:.3f} -> {len(ms_moons.cluster_centers_)} kelompok, "
      f"ukuran {np.bincount(ms_moons.labels_).tolist()}")
# --8<-- [end:moons]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
scaler = StandardScaler()
X_mall = scaler.fit_transform(df[features])

rows = []
for q in [0.1, 0.15, 0.2, 0.3]:
    bw_q = estimate_bandwidth(X_mall, quantile=q, random_state=42)
    model = MeanShift(bandwidth=bw_q).fit(X_mall)
    rows.append({"quantile": q, "bandwidth": round(bw_q, 3), "kelompok": len(model.cluster_centers_),
                 "ukuran": np.bincount(model.labels_).tolist()})
print(pd.DataFrame(rows).to_string(index=False))

bw_mall = estimate_bandwidth(X_mall, quantile=0.15, random_state=42)
ms_mall = MeanShift(bandwidth=bw_mall).fit(X_mall)
df["Cluster"] = ms_mall.labels_

print(f"\nDipakai: quantile = 0.15, bandwidth = {bw_mall:.3f}, {len(ms_mall.cluster_centers_)} kelompok")
print("Pusat dalam satuan asli:")
print(pd.DataFrame(scaler.inverse_transform(ms_mall.cluster_centers_), columns=features).round(1))
print("Ukuran kelompok:", np.bincount(df["Cluster"]).tolist())
# --8<-- [end:mall]

# --8<-- [start:newpoint]
new_customers = scaler.transform(pd.DataFrame([[30, 80], [60, 50], [90, 15]], columns=features))
print("Label pelanggan baru:", ms_mall.predict(new_customers).tolist())
# --8<-- [end:newpoint]

# --8<-- [start:plotmall]
centers_original = scaler.inverse_transform(ms_mall.cluster_centers_)
fig, ax = plt.subplots(figsize=(6.5, 5))
for j in range(len(ms_mall.cluster_centers_)):
    members = df[df["Cluster"] == j]
    ax.scatter(members[features[0]], members[features[1]], s=22, color=palette[j % len(palette)], label=f"Kelompok {j}")
ax.scatter(centers_original[:, 0], centers_original[:, 1], s=200, marker="X", color="black", label="Pusat (puncak)")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("Mean Shift pada Mall Customers")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
