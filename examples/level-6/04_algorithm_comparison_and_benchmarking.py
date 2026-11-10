"""Level 6, Bab 4: Perbandingan algoritma dan benchmarking (Eksperimen A).

Jalankan dari folder utama proyek:
    python examples/level-6/04_algorithm_comparison_and_benchmarking.py
"""
# NB: setup=Siapkan alat | datasets=Enam dataset dengan karakter berbeda | protocol=Protokol perbandingan yang adil | tuners=Pemilihan parameter DBSCAN dan Mean Shift tanpa label | runall=Menjalankan semua kombinasi | tables=Tabel hasil | rankings=Siapa yang terbaik menurut metrik berbeda | scaling=Waktu jalan dan memori terhadap jumlah data | save=Menyimpan hasil | plotgrid=Menggambar hasil semua kombinasi | plotheat=Peta panas metrik | plotscale=Menggambar waktu dan memori

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import json
import tracemalloc

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import StandardScaler

import _experiment as ex

SEED = 42
# --8<-- [end:setup]

import _savefig

_savefig.install(["04-hasil-semua-kombinasi", "04-peta-panas-metrik", "04-waktu-dan-memori"])

# --8<-- [start:datasets]
rng = np.random.default_rng(SEED)

def standardize(X):
    return StandardScaler().fit_transform(X)

raw = {}
raw["Jelas"] = make_blobs(n_samples=450, centers=3, cluster_std=0.7, random_state=SEED)
raw["Tumpang tindih"] = make_blobs(n_samples=450, centers=3, cluster_std=2.2, random_state=SEED)
raw["Bulan sabit"] = make_moons(n_samples=450, noise=0.07, random_state=SEED)
raw["Kepadatan berbeda"] = make_blobs(n_samples=[200, 150, 100], centers=[[0, 0], [7, 0], [3.5, 7]],
                                      cluster_std=[0.4, 1.0, 1.6], random_state=SEED)
# Tiga gerombol ditambah 50 titik noise. Titik noise diberi label acuan ke-4 ("noise").
X_core, y_core = make_blobs(n_samples=400, centers=3, cluster_std=0.6, random_state=SEED)
noise = rng.uniform(X_core.min(axis=0) - 2, X_core.max(axis=0) + 2, size=(50, 2))
raw["Dengan noise"] = (np.vstack([X_core, noise]), np.concatenate([y_core, np.full(50, 3)]))
# Gerombol miring (elips), bukan bulat
X_a, y_a = make_blobs(n_samples=450, centers=3, cluster_std=1.0, random_state=SEED)
raw["Miring (elips)"] = (X_a @ np.array([[0.6, -0.6], [-0.4, 0.8]]), y_a)

datasets = {name: (standardize(X), y) for name, (X, y) in raw.items()}
true_k = {"Jelas": 3, "Tumpang tindih": 3, "Bulan sabit": 2, "Kepadatan berbeda": 3, "Dengan noise": 3, "Miring (elips)": 3}
for name, (X, y) in datasets.items():
    print(f"{name:18s} bentuk {X.shape}, kelas acuan: {np.bincount(y).tolist()}, sidik jari {ex.dataset_fingerprint(X)}")
# --8<-- [end:datasets]

# --8<-- [start:protocol]
protocol = pd.DataFrame(
    [
        ["K-Means", "n_clusters = K acuan, n_init = 10, seed 42", "diberi K acuan"],
        ["Hierarchical", "n_clusters = K acuan, linkage = ward", "diberi K acuan"],
        ["GMM", "n_components = K acuan, covariance_type = full, n_init = 3, seed 42", "diberi K acuan"],
        ["DBSCAN", "eps dan min_samples dicari dengan grid", "dipilih TANPA label (batasan + Silhouette)"],
        ["Mean Shift", "bandwidth dicari dengan grid", "dipilih TANPA label (batasan + Silhouette)"],
    ],
    columns=["Algoritma", "Konfigurasi", "Cara menentukan"],
)
print(protocol.to_string(index=False))
print("Praproses sama untuk semua: StandardScaler. Seed = 42. Label acuan hanya untuk menilai.")
# --8<-- [end:protocol]

# --8<-- [start:tuners]
def pick_by_internal(X, make_model, grid, max_noise, min_k=2, max_k=10):
    """Memilih parameter dengan Silhouette tertinggi di antara kombinasi yang memenuhi batasan. Tanpa label."""
    best = None
    for params in grid:
        labels = make_model(params).fit_predict(X)
        scores = ex.internal_scores(X, labels)
        if np.isnan(scores["silhouette"]) or scores["noise_fraction"] > max_noise or not (min_k <= scores["n_clusters"] <= max_k):
            continue
        if best is None or scores["silhouette"] > best[1]:
            best = (params, scores["silhouette"])
    return best[0] if best else None


dbscan_grid = ParameterGrid({"eps": [round(v, 2) for v in np.arange(0.10, 0.61, 0.05)], "min_samples": [5, 10]})
meanshift_grid = ParameterGrid({"bandwidth": [0.2, 0.3, 0.5, 0.7, 1.0, 1.5]})
# --8<-- [end:tuners]

# --8<-- [start:runall]
algorithms = ["K-Means", "Hierarchical", "GMM", "DBSCAN", "Mean Shift"]
records, labels_store = [], {}
for d_index, (name, (X, y)) in enumerate(datasets.items(), start=1):
    k = true_k[name]
    chosen = {
        "K-Means": {"n_clusters": k},
        "Hierarchical": {"n_clusters": k, "linkage": "ward"},
        "GMM": {"n_components": k, "covariance_type": "full"},
        "DBSCAN": pick_by_internal(X, lambda p: DBSCAN(**p), dbscan_grid, max_noise=0.20),
        "Mean Shift": pick_by_internal(X, lambda p: MeanShift(**p), meanshift_grid, max_noise=0.0),
    }
    for algo in algorithms:
        params = chosen[algo]
        if params is None:                      # tidak ada kombinasi yang memenuhi batasan
            continue
        if algo == "K-Means":
            model = KMeans(n_init=10, random_state=SEED, **params)
        elif algo == "Hierarchical":
            model = AgglomerativeClustering(**params)
        elif algo == "GMM":
            model = GaussianMixture(n_init=3, random_state=SEED, **params)
        elif algo == "DBSCAN":
            model = DBSCAN(**params)
        else:
            model = MeanShift(**params)
        labels, seconds = ex.timed(model.fit_predict, X)
        scores = ex.internal_scores(X, labels)
        scores["ari_reference"] = adjusted_rand_score(y, labels)
        scores["nmi_reference"] = normalized_mutual_info_score(y, labels)
        records.append(ex.make_record(f"A-{d_index}-{algo}", name, X, "StandardScaler", "semua fitur", algo, params, SEED, scores, seconds))
        labels_store[(name, algo)] = labels
results = pd.DataFrame(records)
print("Jumlah catatan:", len(results), "(6 dataset x 5 algoritma)")
chosen_params = results[results["algorithm"].isin(["DBSCAN", "Mean Shift"])][["dataset", "algorithm", "params"]]
print(chosen_params.to_string(index=False))
# --8<-- [end:runall]

# --8<-- [start:tables]
order = list(datasets.keys())
def pivot(column):
    return results.pivot(index="dataset", columns="algorithm", values=column).loc[order, algorithms]

print("Jumlah kelompok yang ditemukan (kelas acuan: 3, 3, 2, 3, 3, 3):")
print(pivot("n_clusters").to_string())
print("\nProporsi noise (hanya DBSCAN yang punya noise):")
print(pivot("noise_fraction").round(3).to_string())
print("\nSilhouette (noise dikeluarkan):")
print(pivot("silhouette").round(3).to_string())
print("\nARI terhadap label acuan:")
print(pivot("ari_reference").round(3).to_string())
print("\nNMI terhadap label acuan:")
print(pivot("nmi_reference").round(3).to_string())
# --8<-- [end:tables]

# --8<-- [start:rankings]
def winners(series, highest=True, digits=3):
    """Nama algoritma dengan nilai terbaik. Bila ada seri (setelah dibulatkan), semuanya ditulis."""
    rounded = series.round(digits)
    best = rounded.max() if highest else rounded.min()
    return " / ".join(rounded[rounded == best].index)


rows = []
for name in order:
    part = results[results["dataset"] == name].set_index("algorithm")
    rows.append(
        {
            "Dataset": name,
            "Silhouette tertinggi": winners(part["silhouette"]),
            "DBI terendah": winners(part["davies_bouldin"], highest=False),
            "CHI tertinggi": winners(part["calinski_harabasz"], digits=1),
            "ARI tertinggi": winners(part["ari_reference"]),
        }
    )
print(pd.DataFrame(rows).set_index("Dataset").to_string())
# --8<-- [end:rankings]

# --8<-- [start:scaling]
def scaling_benchmark(sizes):
    """Waktu jalan dan puncak memori (MB) tiap algoritma pada data berukuran n. Parameter tetap."""
    rows = []
    for n in sizes:
        X, _ = make_blobs(n_samples=n, centers=4, cluster_std=1.0, random_state=SEED)
        X = standardize(X)
        models = {
            "K-Means": KMeans(n_clusters=4, n_init=10, random_state=SEED),
            "Hierarchical": AgglomerativeClustering(n_clusters=4, linkage="ward"),
            "GMM": GaussianMixture(n_components=4, random_state=SEED),
            "DBSCAN": DBSCAN(eps=0.3, min_samples=5),
            "Mean Shift": MeanShift(bandwidth=0.7),
        }
        for algo, model in models.items():
            tracemalloc.start()
            _, seconds = ex.timed(model.fit_predict, X)
            peak = tracemalloc.get_traced_memory()[1] / 1e6
            tracemalloc.stop()
            rows.append({"n": n, "algorithm": algo, "runtime_seconds": seconds, "peak_memory_mb": peak})
    return pd.DataFrame(rows)


scaling = scaling_benchmark([500, 1000, 2000, 4000])
print("Benchmark skala selesai:", len(scaling), "pengukuran (waktu dan memori disimpan di CSV, tidak dicetak karena berubah tiap eksekusi)")
# --8<-- [end:scaling]

# --8<-- [start:save]
results.to_csv(ex.RESULTS_DIR / "04_benchmark.csv", index=False)
scaling.to_csv(ex.RESULTS_DIR / "04_scaling.csv", index=False)
ex.save_json({"seed": SEED, "protocol": protocol.to_dict(orient="records"), "environment": ex.environment_info()}, "04_protocol")
print("Disimpan: 04_benchmark.csv, 04_scaling.csv, 04_protocol.json")
# --8<-- [end:save]

# --8<-- [start:plotgrid]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442", "#999999"]

fig, axes = plt.subplots(6, 5, figsize=(15, 17))
for r, name in enumerate(order):
    X, y = datasets[name]
    for c, algo in enumerate(algorithms):
        ax = axes[r, c]
        labels = labels_store.get((name, algo))
        if labels is None:
            ax.axis("off")
            continue
        for cluster in sorted(set(labels)):
            if cluster == -1:
                ax.scatter(X[labels == cluster, 0], X[labels == cluster, 1], s=18, marker="x", color="gray")
            else:
                ax.scatter(X[labels == cluster, 0], X[labels == cluster, 1], s=9, color=palette[cluster % len(palette)])
        ari = results[(results["dataset"] == name) & (results["algorithm"] == algo)]["ari_reference"].iloc[0]
        ax.set_title(f"{name} - {algo}\nARI = {ari:.2f}", fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
plt.tight_layout()
plt.show()
# --8<-- [end:plotgrid]

# --8<-- [start:plotheat]
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
for ax, (column, title, cmap) in zip(axes, [("ari_reference", "ARI terhadap label acuan", "viridis"),
                                            ("silhouette", "Silhouette (noise dikeluarkan)", "viridis"),
                                            ("n_clusters", "Jumlah kelompok ditemukan", "magma_r")]):
    table = pivot(column).to_numpy(float)
    image = ax.imshow(table, cmap=cmap, aspect="auto")
    ax.set_xticks(range(len(algorithms)))
    ax.set_xticklabels(algorithms, rotation=25, fontsize=8)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=8)
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            ax.text(j, i, f"{table[i, j]:.2f}" if column != "n_clusters" else f"{int(table[i, j])}",
                    ha="center", va="center", color="white", fontsize=8)
    ax.set_title(title, fontsize=10)
    fig.colorbar(image, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
# --8<-- [end:plotheat]

# --8<-- [start:plotscale]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))
for color, algo in zip(palette, algorithms):
    part = scaling[scaling["algorithm"] == algo]
    axes[0].plot(part["n"], part["runtime_seconds"], marker="o", color=color, label=algo)
    axes[1].plot(part["n"], part["peak_memory_mb"], marker="o", color=color, label=algo)
axes[0].set_ylabel("Waktu jalan (detik)")
axes[1].set_ylabel("Puncak memori (MB)")
for ax in axes:
    ax.set_xlabel("Jumlah titik (n)")
    ax.set_xscale("log")
    ax.set_yscale("log")
axes[0].legend(fontsize=8)
axes[0].set_title("Waktu jalan (skala log)")
axes[1].set_title("Puncak memori (skala log)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotscale]
