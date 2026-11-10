"""Level 4, Bab 2: K-Means dari nol dengan NumPy, lalu dengan scikit-learn.

Jalankan dari folder utama proyek:
    python examples/level-4/02_k_means_clustering.py
"""
# NB: setup=Siapkan alat | tiny=Data kecil untuk hitungan manual | scratch=K-Means dari nol | trace=Menjalankan K-Means dari nol langkah demi langkah | plotiter=Menggambar perpindahan centroid | blobs=Data blobs dan K-Means scikit-learn | compare=Membandingkan buatan sendiri dan scikit-learn | kvalues=Pengaruh jumlah kelompok K | elbow=WCSS terhadap K | init=Inisialisasi random vs k-means++ | plusplus=k-means++ dari nol | converge=Konvergensi | plotconv=Menggambar konvergensi | mall=K-Means pada Mall Customers | newpoint=Memberi label pada data baru | mistake=Kesalahan umum: lupa menyamakan skala | plotmall=Menggambar hasil Mall Customers

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
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["02-iterasi-kmeans", "02-pengaruh-k", "02-elbow", "02-konvergensi", "02-mall-customers"])

# --8<-- [start:tiny]
# Delapan titik di dua gerombol: kiri bawah dan kanan atas
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2], [2, 2],   # gerombol kiri bawah
        [6, 5], [7, 5], [6, 6], [7, 6],   # gerombol kanan atas
    ],
    dtype=float,
)
# Centroid awal sengaja dipilih buruk: dua-duanya di gerombol kiri
initial_centroids = np.array([[1.0, 1.0], [2.0, 1.0]])
print("Bentuk X_tiny:", X_tiny.shape)
print("Centroid awal:\n", initial_centroids)
# --8<-- [end:tiny]


# --8<-- [start:scratch]
def kmeans_scratch(X, initial_centroids, max_iter=100, tol=1e-6):
    """K-Means sederhana. Mengembalikan label, centroid akhir, dan riwayat tiap iterasi."""
    centroids = initial_centroids.copy()
    k = len(centroids)
    history = []

    for iteration in range(1, max_iter + 1):
        # Langkah 1 (assignment): jarak setiap titik ke setiap centroid, bentuk (n, k)
        distances = np.linalg.norm(X[:, None, :] - centroids[None, :, :], axis=2)
        labels = distances.argmin(axis=1)

        # WCSS: jumlah kuadrat jarak titik ke centroid kelompoknya (centroid sebelum diperbarui)
        wcss = ((X - centroids[labels]) ** 2).sum()

        # Langkah 2 (update): centroid baru = rata-rata anggota. Kelompok kosong: centroid tetap
        new_centroids = np.array(
            [
                X[labels == j].mean(axis=0) if np.any(labels == j) else centroids[j]
                for j in range(k)
            ]
        )

        # Seberapa jauh centroid bergeser pada iterasi ini
        shift = np.linalg.norm(new_centroids - centroids, axis=1).max()
        history.append(
            {"iteration": iteration, "labels": labels, "centroids": centroids.copy(),
             "wcss": wcss, "shift": shift}
        )
        centroids = new_centroids

        if shift <= tol:  # centroid tidak bergerak lagi: berhenti
            break

    return labels, centroids, history
# --8<-- [end:scratch]


# --8<-- [start:trace]
labels_tiny, centroids_tiny, hist_tiny = kmeans_scratch(X_tiny, initial_centroids)

for step in hist_tiny:
    print(f"Iterasi {step['iteration']}:")
    print("  centroid yang dipakai :", step["centroids"].round(3).tolist())
    print("  label tiap titik      :", step["labels"].tolist())
    print(f"  WCSS                  : {step['wcss']:.3f}")
    print(f"  pergeseran centroid   : {step['shift']:.3f}")

print("\nCentroid akhir:", centroids_tiny.round(3).tolist())
# --8<-- [end:trace]

# --8<-- [start:plotiter]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, len(hist_tiny), figsize=(4 * len(hist_tiny), 4), sharex=True, sharey=True)
for ax, step in zip(axes, hist_tiny):
    for j in range(2):
        pts = X_tiny[step["labels"] == j]
        ax.scatter(pts[:, 0], pts[:, 1], s=60, color=palette[j])
        cx, cy = step["centroids"][j]
        ax.scatter(cx, cy, s=200, marker="X", color=palette[j], edgecolor="black")
    ax.set_title(f"Iterasi {step['iteration']} (WCSS = {step['wcss']:.2f})")
    ax.set_xlabel("x1")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotiter]

# --8<-- [start:blobs]
X, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=42)

kmeans = KMeans(n_clusters=4, init="k-means++", n_init=10, max_iter=300, tol=1e-4, random_state=42)
labels_sk = kmeans.fit_predict(X)

print("Ukuran kelompok:", np.bincount(labels_sk).tolist())
print("Centroid (cluster_centers_):\n", kmeans.cluster_centers_.round(3))
print("Inertia (WCSS):", round(kmeans.inertia_, 3))
print("Jumlah iterasi (n_iter_):", kmeans.n_iter_)
# --8<-- [end:blobs]

# --8<-- [start:compare]
# Jalankan versi buatan sendiri dari centroid awal yang kita pilih sendiri
rng = np.random.default_rng(42)
start = X[rng.choice(len(X), size=4, replace=False)]
labels_me, centroids_me, hist_me = kmeans_scratch(X, start)

# Urutkan centroid supaya nomor kelompok tidak mengganggu perbandingan
sorted_me = centroids_me[np.lexsort((centroids_me[:, 1], centroids_me[:, 0]))]
sorted_sk = kmeans.cluster_centers_[np.lexsort((kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 0]))]

print("Iterasi versi buatan sendiri:", len(hist_me))
print("WCSS versi buatan sendiri   :", round(hist_me[-1]["wcss"], 3))
print("Selisih terbesar antar centroid:", np.abs(sorted_me - sorted_sk).max().round(6))
# --8<-- [end:compare]

# --8<-- [start:kvalues]
fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharex=True, sharey=True)
for ax, k in zip(axes, [2, 3, 4, 6]):
    model = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    for j in range(k):
        pts = X[model.labels_ == j]
        ax.scatter(pts[:, 0], pts[:, 1], s=14, color=palette[j % len(palette)])
    ax.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1],
               s=160, marker="X", color="black")
    ax.set_title(f"K = {k}  (WCSS = {model.inertia_:.0f})")
    ax.set_xlabel("x1")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:kvalues]

# --8<-- [start:elbow]
k_values = range(1, 9)
wcss_values = [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_ for k in k_values]
for k, w in zip(k_values, wcss_values):
    print(f"K = {k}: WCSS = {w:.1f}")

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(list(k_values), wcss_values, marker="o", color="#0072B2")
ax.set_xlabel("Jumlah kelompok K")
ax.set_ylabel("WCSS (inertia)")
ax.set_title("WCSS terhadap K: penurunan tajam berhenti di K = 4")
plt.tight_layout()
plt.show()
# --8<-- [end:elbow]

# --8<-- [start:init]
# Data yang lebih menantang: lima gerombol yang cukup berdekatan
X5, _ = make_blobs(n_samples=500, centers=5, cluster_std=1.1, random_state=3)

rows = []
for init in ["random", "k-means++"]:
    inertias, iters = [], []
    for seed in range(20):
        model = KMeans(n_clusters=5, init=init, n_init=1, random_state=seed).fit(X5)
        inertias.append(model.inertia_)
        iters.append(model.n_iter_)
    rows.append(
        {"init": init, "WCSS terkecil": min(inertias), "WCSS terbesar": max(inertias),
         "rata-rata iterasi": np.mean(iters),
         "jumlah seed dengan WCSS terbaik": int(np.sum(np.isclose(inertias, min(inertias), rtol=1e-6)))}
    )
print(pd.DataFrame(rows).round(2).to_string(index=False))
# --8<-- [end:init]

# --8<-- [start:plusplus]
def kmeans_plus_plus_init(X, k, seed=0):
    """Memilih k centroid awal dengan k-means++ (versi sederhana)."""
    rng = np.random.default_rng(seed)
    centers = [X[rng.integers(len(X))]]  # centroid pertama: satu titik acak
    for _ in range(k - 1):
        # D(x)^2: kuadrat jarak tiap titik ke centroid terdekat yang sudah dipilih
        d2 = np.min([((X - c) ** 2).sum(axis=1) for c in centers], axis=0)
        probs = d2 / d2.sum()  # makin jauh, makin besar peluang terpilih
        centers.append(X[rng.choice(len(X), p=probs)])
    return np.array(centers)

centers_pp = kmeans_plus_plus_init(X5, k=5, seed=0)
print("Centroid awal dari k-means++ (buatan sendiri):\n", centers_pp.round(2))
_, _, hist_pp = kmeans_scratch(X5, centers_pp)
print("Iterasi sampai konvergen:", len(hist_pp), "| WCSS akhir:", round(hist_pp[-1]["wcss"], 2))
# --8<-- [end:plusplus]

# --8<-- [start:converge]
for max_iter in [1, 2, 3, 300]:
    model = KMeans(n_clusters=4, init="random", n_init=1, max_iter=max_iter, random_state=0).fit(X)
    print(f"max_iter = {max_iter:<3} -> n_iter_ = {model.n_iter_}, WCSS = {model.inertia_:.2f}")

wcss_history = [float(step["wcss"]) for step in hist_me]
print("\nWCSS tiap iterasi (versi buatan sendiri):", [round(w, 1) for w in wcss_history])
print("Tidak pernah naik?", all(a >= b - 1e-9 for a, b in zip(wcss_history, wcss_history[1:])))
# --8<-- [end:converge]

# --8<-- [start:plotconv]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([s["iteration"] for s in hist_me], wcss_history, marker="o", color="#0072B2")
ax.set_xlabel("Iterasi")
ax.set_ylabel("WCSS")
ax.set_title("WCSS turun lalu mendatar saat K-Means konvergen")
plt.tight_layout()
plt.show()
# --8<-- [end:plotconv]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]

scaler = StandardScaler()
X_mall = scaler.fit_transform(df[features])  # rata-rata 0, simpangan baku 1

km_mall = KMeans(n_clusters=5, n_init=10, random_state=42)
df["Cluster"] = km_mall.fit_predict(X_mall)

print("Jumlah pelanggan per kelompok:", np.bincount(df["Cluster"]).tolist())
# Kembalikan centroid ke satuan asli supaya mudah dibaca
centers_original = scaler.inverse_transform(km_mall.cluster_centers_)
print(pd.DataFrame(centers_original, columns=features).round(1))
# --8<-- [end:mall]

# --8<-- [start:newpoint]
new_customers = pd.DataFrame([[30, 80], [90, 15]], columns=features)
new_scaled = scaler.transform(new_customers)  # pakai scaler yang SAMA, jangan fit ulang
print("Label pelanggan baru:", km_mall.predict(new_scaled).tolist())
print("Jarak ke tiap centroid (pelanggan pertama):", km_mall.transform(new_scaled)[0].round(2).tolist())
# --8<-- [end:newpoint]

# --8<-- [start:mistake]
# Kesalahan umum: satu fitur berskala jauh lebih besar (pendapatan dalam dolar, bukan ribu dolar)
X_unscaled = df[features].copy()
X_unscaled["Annual Income (k$)"] = X_unscaled["Annual Income (k$)"] * 1000

km_unscaled = KMeans(n_clusters=5, n_init=10, random_state=42).fit(X_unscaled)
print("Ukuran kelompok TANPA penyamaan skala:", sorted(np.bincount(km_unscaled.labels_).tolist()))
print("Ukuran kelompok DENGAN penyamaan skala:", sorted(np.bincount(df["Cluster"]).tolist()))
# --8<-- [end:mistake]

# --8<-- [start:plotmall]
fig, ax = plt.subplots(figsize=(6.5, 5))
for j in range(5):
    members = df[df["Cluster"] == j]
    ax.scatter(members[features[0]], members[features[1]], s=22, color=palette[j % len(palette)],
               label=f"Kelompok {j}")
ax.scatter(centers_original[:, 0], centers_original[:, 1], s=200, marker="X",
           color="black", label="Centroid")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("K-Means (K = 5) pada Mall Customers")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
