"""Level 4, Bab 4: DBSCAN (density-based clustering).

Jalankan dari folder utama proyek:
    python examples/level-4/04_dbscan_clustering.py
"""
# NB: setup=Siapkan alat | tiny=Sembilan titik untuk hitungan manual | classify=Mengklasifikasi titik inti, tepi, dan noise | dbtiny=DBSCAN pada sembilan titik | plottiny=Menggambar sembilan titik dan lingkaran eps | moons=Data bulan sabit dengan noise | fitmoons=DBSCAN pada data bulan sabit | helper=Fungsi menggambar tipe titik | plotmoons=Menggambar titik inti, tepi, dan noise | kdist=Grafik k-distance untuk memilih eps | plotkdist=Menggambar k-distance | params=Pengaruh eps dan min_samples | plotparams=Menggambar pengaruh parameter | density=Kelompok dengan kepadatan berbeda | plotdensity=Menggambar kepadatan berbeda | options=Parameter metric, algorithm, dan leaf_size | mall=DBSCAN pada Mall Customers | gridmall=Sensitivitas parameter pada Mall | scale=Kesalahan umum: lupa skala | plotmall=Menggambar hasil Mall

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
from matplotlib.patches import Circle
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_blobs, make_moons
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(
    ["04-titik-kecil", "04-core-border-noise", "04-k-distance", "04-pengaruh-parameter",
     "04-kepadatan-berbeda", "04-mall-customers"]
)

# --8<-- [start:tiny]
# Sembilan titik: gerombol kiri bawah (A-E), satu titik sendirian (F), gerombol kanan atas (G-I)
names = list("ABCDEFGHI")
P = np.array(
    [[1, 1], [2, 1], [1, 2], [2, 2], [3, 2],     # A, B, C, D, E
     [5, 5],                                       # F
     [8, 8], [8.5, 8], [8, 8.5]],                  # G, H, I
    dtype=float,
)
eps = 1.2
min_samples = 3
# --8<-- [end:tiny]

# --8<-- [start:classify]
# Matriks jarak Euclidean antar semua pasangan titik, bentuk (9, 9)
dist = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)

# Tetangga = titik dengan jarak <= eps (termasuk titik itu sendiri, jaraknya 0)
is_neighbor = dist <= eps
n_neighbors = is_neighbor.sum(axis=1)

is_core = n_neighbors >= min_samples
# Tepi: bukan inti, tetapi bertetangga dengan setidaknya satu titik inti
is_border = ~is_core & (is_neighbor & is_core[None, :]).any(axis=1)
is_noise = ~is_core & ~is_border

for i, name in enumerate(names):
    tipe = "inti" if is_core[i] else ("tepi" if is_border[i] else "noise")
    tetangga = [names[j] for j in np.where(is_neighbor[i])[0]]
    print(f"{name}: {n_neighbors[i]} tetangga {tetangga} -> {tipe}")
# --8<-- [end:classify]

# --8<-- [start:dbtiny]
db_tiny = DBSCAN(eps=eps, min_samples=min_samples).fit(P)
print("\nlabels_              :", db_tiny.labels_.tolist())
print("core_sample_indices_ :", db_tiny.core_sample_indices_.tolist())
print("Sama dengan hitungan manual?", np.array_equal(np.sort(db_tiny.core_sample_indices_), np.where(is_core)[0]))
# --8<-- [end:dbtiny]

# --8<-- [start:plottiny]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]

fig, ax = plt.subplots(figsize=(6.5, 6))
for i, name in enumerate(names):
    label = db_tiny.labels_[i]
    color = "#999999" if label == -1 else palette[label % len(palette)]
    if is_core[i]:
        ax.add_patch(Circle(P[i], eps, fill=False, edgecolor=color, linestyle="--", alpha=0.6))
        ax.scatter(*P[i], s=120, color=color, edgecolor="black", zorder=3)
    elif is_border[i]:
        ax.scatter(*P[i], s=120, color=color, edgecolor="black", marker="s", zorder=3)
    else:
        ax.scatter(*P[i], s=120, color=color, marker="x", zorder=3)
    ax.annotate(name, P[i], textcoords="offset points", xytext=(7, 7))
ax.set_aspect("equal")
ax.set_xlim(-0.5, 10)
ax.set_ylim(-0.5, 10)
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.set_title(f"eps = {eps}, min_samples = {min_samples}: lingkaran = tetangga titik inti")
plt.tight_layout()
plt.show()
# --8<-- [end:plottiny]

# --8<-- [start:moons]
X_moons, _ = make_moons(n_samples=300, noise=0.07, random_state=42)

# Tambahkan 15 titik acak sebagai noise
rng = np.random.default_rng(42)
noise_points = rng.uniform(low=[-1.5, -1.0], high=[2.5, 1.5], size=(15, 2))
X = np.vstack([X_moons, noise_points])
print("Bentuk X:", X.shape)
# --8<-- [end:moons]

# --8<-- [start:fitmoons]
db = DBSCAN(eps=0.2, min_samples=5)
labels = db.fit_predict(X)

n_clusters = len(set(labels) - {-1})
n_noise = int(np.sum(labels == -1))
print("Label unik:", sorted(set(labels.tolist())))
print("Jumlah kelompok:", n_clusters)
print("Jumlah noise (label -1):", n_noise)
print("Ukuran tiap kelompok:", np.bincount(labels[labels >= 0]).tolist())

core_mask = np.zeros(len(X), dtype=bool)
core_mask[db.core_sample_indices_] = True
border_mask = (labels >= 0) & ~core_mask
noise_mask = labels == -1
print(f"Titik inti: {core_mask.sum()}, tepi: {border_mask.sum()}, noise: {noise_mask.sum()}")
# --8<-- [end:fitmoons]

# --8<-- [start:helper]
def plot_dbscan(ax, X, labels, core_mask, title):
    """Menggambar hasil DBSCAN: inti (bulat besar), tepi (bulat kecil), noise (x abu-abu)."""
    for k in sorted(set(labels) - {-1}):
        in_k = labels == k
        color = palette[k % len(palette)]
        ax.scatter(X[in_k & core_mask, 0], X[in_k & core_mask, 1], s=28, color=color, edgecolor="black", linewidth=0.4)
        ax.scatter(X[in_k & ~core_mask, 0], X[in_k & ~core_mask, 1], s=10, color=color)
    ax.scatter(X[labels == -1, 0], X[labels == -1, 1], s=26, color="#777777", marker="x")
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
# --8<-- [end:helper]

# --8<-- [start:plotmoons]
fig, ax = plt.subplots(figsize=(7, 5))
plot_dbscan(ax, X, labels, core_mask, f"DBSCAN (eps=0.2, min_samples=5): {n_clusters} kelompok, {n_noise} noise")
ax.set_xticks([-1, 0, 1, 2])
ax.set_yticks([-1, 0, 1])
ax.set_xlabel("x1")
ax.set_ylabel("x2")
ax.scatter([], [], s=28, color="#555555", edgecolor="black", label="Titik inti")
ax.scatter([], [], s=10, color="#555555", label="Titik tepi")
ax.scatter([], [], s=26, color="#777777", marker="x", label="Noise (-1)")
ax.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmoons]

# --8<-- [start:kdist]
k = 5  # sama dengan min_samples
nn = NearestNeighbors(n_neighbors=k).fit(X)
distances, _ = nn.kneighbors(X)       # kolom pertama = titik itu sendiri (jarak 0)
k_distance = np.sort(distances[:, -1])  # jarak ke tetangga ke-k, diurutkan naik

for q in [0, 50, 75, 90, 95, 98, 100]:
    print(f"persentil {q:>3}: jarak ke-{k} = {np.percentile(k_distance, q):.3f}")
# --8<-- [end:kdist]

# --8<-- [start:plotkdist]
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.plot(k_distance, color="#0072B2")
ax.axhline(0.2, color="#D55E00", linestyle="--", label="eps = 0.2 (dipilih)")
ax.set_xlabel("Titik data (diurutkan menurut jaraknya)")
ax.set_ylabel(f"Jarak ke tetangga ke-{k}")
ax.set_title("Grafik k-distance: cari titik tempat kurva menanjak tajam")
ax.legend()
plt.tight_layout()
plt.show()
# --8<-- [end:plotkdist]

# --8<-- [start:params]
def run_dbscan(X, eps, min_samples):
    model = DBSCAN(eps=eps, min_samples=min_samples).fit(X)
    core = np.zeros(len(X), dtype=bool)
    core[model.core_sample_indices_] = True
    return model.labels_, core

rows = []
for eps_value in [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
    lab, _ = run_dbscan(X, eps_value, 5)
    rows.append({"eps": eps_value, "min_samples": 5,
                 "kelompok": len(set(lab) - {-1}), "noise": int(np.sum(lab == -1))})
for ms in [3, 5, 10, 20, 30]:
    lab, _ = run_dbscan(X, 0.2, ms)
    rows.append({"eps": 0.2, "min_samples": ms,
                 "kelompok": len(set(lab) - {-1}), "noise": int(np.sum(lab == -1))})
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:params]

# --8<-- [start:plotparams]
fig, axes = plt.subplots(2, 4, figsize=(16, 7))
for ax, eps_value in zip(axes[0], [0.05, 0.1, 0.2, 0.5]):
    lab, core = run_dbscan(X, eps_value, 5)
    plot_dbscan(ax, X, lab, core, f"eps={eps_value}, min_samples=5\n{len(set(lab) - {-1})} kelompok, {int(np.sum(lab == -1))} noise")
for ax, ms in zip(axes[1], [3, 10, 20, 30]):
    lab, core = run_dbscan(X, 0.2, ms)
    plot_dbscan(ax, X, lab, core, f"eps=0.2, min_samples={ms}\n{len(set(lab) - {-1})} kelompok, {int(np.sum(lab == -1))} noise")
plt.tight_layout()
plt.show()
# --8<-- [end:plotparams]

# --8<-- [start:density]
# Satu gerombol rapat dan satu gerombol renggang
X_dens, _ = make_blobs(n_samples=[200, 200], centers=[[0, 0], [3, 0]],
                       cluster_std=[0.25, 0.9], random_state=42)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharex=True, sharey=True)
for ax, eps_value in zip(axes, [0.25, 0.5, 0.8]):
    lab, core = run_dbscan(X_dens, eps_value, 5)
    sizes = np.bincount(lab[lab >= 0]).tolist()
    print(f"eps = {eps_value}: {len(set(lab) - {-1})} kelompok, ukuran {sizes}, noise {int(np.sum(lab == -1))}")
    plot_dbscan(ax, X_dens, lab, core, f"eps={eps_value}: {len(set(lab) - {-1})} kelompok, {int(np.sum(lab == -1))} noise")
plt.tight_layout()
plt.show()
# --8<-- [end:density]

# --8<-- [start:options]
reference = DBSCAN(eps=0.2, min_samples=5).fit_predict(X)

for algorithm in ["auto", "ball_tree", "kd_tree", "brute"]:
    other = DBSCAN(eps=0.2, min_samples=5, algorithm=algorithm, leaf_size=10).fit_predict(X)
    print(f"algorithm={algorithm:<9} leaf_size=10 -> label sama dengan bawaan? {np.array_equal(reference, other)}")

for metric in ["euclidean", "manhattan"]:
    lab = DBSCAN(eps=0.2, min_samples=5, metric=metric).fit_predict(X)
    print(f"metric={metric:<9} -> {len(set(lab) - {-1})} kelompok, {int(np.sum(lab == -1))} noise")
# --8<-- [end:options]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

db_mall = DBSCAN(eps=0.4, min_samples=8)
df["Cluster"] = db_mall.fit_predict(X_mall)

print("Label unik:", sorted(df["Cluster"].unique().tolist()))
print("Jumlah per label:")
print(df["Cluster"].value_counts().sort_index())
print("\nRata-rata tiap kelompok (noise = -1):")
print(df.groupby("Cluster")[features].mean().round(1))
# --8<-- [end:mall]

# --8<-- [start:gridmall]
grid = {}
for eps_value in [0.2, 0.3, 0.4, 0.5]:
    for ms in [4, 5, 8]:
        lab = DBSCAN(eps=eps_value, min_samples=ms).fit_predict(X_mall)
        grid[(eps_value, ms)] = f"{len(set(lab) - {-1})} kel, {int(np.sum(lab == -1))} noise"
table = pd.Series(grid).unstack()
table.index.name = "eps"
table.columns = [f"min_samples={c}" for c in table.columns]
print(table.to_string())
# --8<-- [end:gridmall]

# --8<-- [start:scale]
# Kesalahan umum: eps = 0.3 dipakai pada data yang BELUM diskalakan (satuan: ribu dolar dan skor)
raw = DBSCAN(eps=0.3, min_samples=5).fit_predict(df[features].values)
print("Tanpa penyamaan skala, eps=0.3 ->", len(set(raw) - {-1}), "kelompok,", int(np.sum(raw == -1)), "noise dari", len(raw), "titik")
# --8<-- [end:scale]

# --8<-- [start:plotmall]
fig, ax = plt.subplots(figsize=(6.5, 5))
for k in sorted(df["Cluster"].unique()):
    members = df[df["Cluster"] == k]
    if k == -1:
        ax.scatter(members[features[0]], members[features[1]], s=30, color="#777777", marker="x", label="Noise (-1)")
    else:
        ax.scatter(members[features[0]], members[features[1]], s=22, color=palette[k % len(palette)], label=f"Kelompok {k}")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("DBSCAN (eps=0.4, min_samples=8) pada Mall Customers")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
