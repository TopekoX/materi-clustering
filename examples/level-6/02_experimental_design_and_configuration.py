"""Level 6, Bab 2: Desain dan konfigurasi eksperimen.

Jalankan dari folder utama proyek:
    python examples/level-6/02_experimental_design_and_configuration.py
"""
# NB: setup=Siapkan alat | data=Dua dataset dan sidik jarinya | runner=Satu fungsi untuk menjalankan satu konfigurasi | kmeans=Desain K-Means: ubah K | dbscan=Desain DBSCAN: ubah satu variabel | hier=Desain Hierarchical: ubah linkage | factorial=Pengantar multi-faktor: eps x min_samples | save=Menyimpan hasil dan konfigurasi | repro=Memeriksa bahwa eksperimen bisa diulang | plot=Menggambar kondisi DBSCAN

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import StandardScaler

import _experiment as ex   # alat bantu pencatat (examples/level-6/_experiment.py)
# --8<-- [end:setup]

import _savefig

_savefig.install(["02-dbscan-eps", "02-faktorial-dbscan"])

# --8<-- [start:data]
SEED = 42
X_blobs_raw, y_blobs = make_blobs(n_samples=300, centers=3, cluster_std=1.2, random_state=SEED)
X_moons_raw, y_moons = make_moons(n_samples=300, noise=0.06, random_state=SEED)

# Praproses yang sama untuk semua eksperimen: StandardScaler
X_blobs = StandardScaler().fit_transform(X_blobs_raw)
X_moons = StandardScaler().fit_transform(X_moons_raw)

print("Blobs : bentuk", X_blobs.shape, "sidik jari data", ex.dataset_fingerprint(X_blobs))
print("Moons : bentuk", X_moons.shape, "sidik jari data", ex.dataset_fingerprint(X_moons))
# --8<-- [end:data]

# --8<-- [start:runner]
def build_estimator(algorithm, params, seed):
    """Membuat estimator dari nama algoritma dan dictionary parameter."""
    if algorithm == "KMeans":
        return KMeans(n_init=10, random_state=seed, **params)
    if algorithm == "DBSCAN":
        return DBSCAN(**params)
    if algorithm == "Hierarchical":
        return AgglomerativeClustering(**params)
    raise ValueError(f"Algoritma tidak dikenal: {algorithm}")


def run_config(exp_id, dataset, X, y_ref, algorithm, params, seed=SEED):
    """Menjalankan satu konfigurasi dan mengembalikan satu catatan lengkap."""
    estimator = build_estimator(algorithm, params, seed)
    labels, seconds = ex.timed(estimator.fit_predict, X)       # pelatihan: hanya X
    scores = ex.internal_scores(X, labels)                      # metrik internal
    scores["ari_reference"] = adjusted_rand_score(y_ref, labels)  # label acuan: hanya untuk menilai
    return ex.make_record(exp_id, dataset, X, "StandardScaler", "semua fitur", algorithm, params, seed, scores, seconds)


columns = ["experiment_id", "n_clusters", "noise_fraction", "silhouette", "davies_bouldin", "ari_reference"]
# --8<-- [end:runner]

# --8<-- [start:kmeans]
# Desain 1: K-Means pada blobs. Variabel bebas: K. Baseline: K = 3. Lainnya ditahan sama.
records = []
for i, k in enumerate([2, 3, 4, 5], start=1):
    records.append(run_config(f"KM-{i:02d}", "blobs", X_blobs, y_blobs, "KMeans", {"n_clusters": k}))
kmeans_table = pd.DataFrame(records)
print(kmeans_table[["experiment_id", "params"] + columns[1:]].round(3).to_string(index=False))
# --8<-- [end:kmeans]

# --8<-- [start:dbscan]
# Desain 2: DBSCAN pada moons, satu variabel per kali. Baseline: eps = 0.3, min_samples = 5.
dbscan_records = []
for i, eps in enumerate([0.15, 0.2, 0.3, 0.4], start=1):          # variabel bebas 1: eps
    dbscan_records.append(run_config(f"DB-E{i}", "moons", X_moons, y_moons, "DBSCAN", {"eps": eps, "min_samples": 5}))
for i, min_samples in enumerate([3, 10, 20], start=1):             # variabel bebas 2: min_samples (eps tetap 0.3)
    dbscan_records.append(run_config(f"DB-M{i}", "moons", X_moons, y_moons, "DBSCAN", {"eps": 0.3, "min_samples": min_samples}))
dbscan_table = pd.DataFrame(dbscan_records)
print(dbscan_table[["experiment_id", "params"] + columns[1:]].round(3).to_string(index=False))
# --8<-- [end:dbscan]

# --8<-- [start:hier]
# Desain 3: Hierarchical pada moons. Variabel bebas: linkage. Baseline: ward. n_clusters = 2 tetap.
hier_records = []
for i, linkage in enumerate(["ward", "complete", "average", "single"], start=1):
    hier_records.append(run_config(f"HC-{i:02d}", "moons", X_moons, y_moons, "Hierarchical", {"n_clusters": 2, "linkage": linkage}))
hier_table = pd.DataFrame(hier_records)
print(hier_table[["experiment_id", "params"] + columns[1:]].round(3).to_string(index=False))
# --8<-- [end:hier]

# --8<-- [start:factorial]
# Pengantar multi-faktor: dua variabel diubah bersama, semua kombinasinya dijalankan
grid = ParameterGrid({"eps": [0.2, 0.3, 0.4], "min_samples": [3, 5, 10]})
factorial_records = []
for i, params in enumerate(grid, start=1):
    factorial_records.append(run_config(f"DB-F{i:02d}", "moons", X_moons, y_moons, "DBSCAN", params))
factorial_table = pd.DataFrame(factorial_records)

# Kolom params berisi teks JSON. Kita urai supaya eps dan min_samples bisa dijadikan tabel silang
factorial_table["eps"] = [json.loads(text)["eps"] for text in factorial_table["params"]]
factorial_table["min_samples"] = [json.loads(text)["min_samples"] for text in factorial_table["params"]]
print("Jumlah kelompok (baris = eps, kolom = min_samples):")
print(factorial_table.pivot(index="eps", columns="min_samples", values="n_clusters").to_string())
print("Proporsi noise:")
print(factorial_table.pivot(index="eps", columns="min_samples", values="noise_fraction").round(3).to_string())
print("ARI terhadap label acuan (dinilai SETELAH clustering):")
print(factorial_table.pivot(index="eps", columns="min_samples", values="ari_reference").round(3).to_string())
# --8<-- [end:factorial]

# --8<-- [start:save]
all_records = records + dbscan_records + hier_records + factorial_records
results = ex.save_records(all_records, "02_experiments")
ex.save_json(ex.environment_info(), "02_environment")
ex.save_json(
    {
        "seed": SEED,
        "datasets": {"blobs": "make_blobs(n_samples=300, centers=3, cluster_std=1.2)", "moons": "make_moons(n_samples=300, noise=0.06)"},
        "preprocessing": "StandardScaler",
        "designs": {"KM": "ubah n_clusters", "DB-E": "ubah eps", "DB-M": "ubah min_samples", "HC": "ubah linkage", "DB-F": "grid eps x min_samples"},
    },
    "02_config",
)
print("Jumlah catatan eksperimen :", len(results))
print("Kolom catatan             :", list(results.columns))
print("Info lingkungan           :", ex.environment_info())
# --8<-- [end:save]

# --8<-- [start:repro]
# Jalankan ulang semua konfigurasi, lalu bandingkan dengan catatan tersimpan (waktu jalan tidak dibandingkan)
rerun = []
for rec in all_records:
    params = json.loads(rec["params"])
    dataset = X_blobs if rec["dataset"] == "blobs" else X_moons
    y_ref = y_blobs if rec["dataset"] == "blobs" else y_moons
    rerun.append(run_config(rec["experiment_id"], rec["dataset"], dataset, y_ref, rec["algorithm"], params, rec["seed"]))
rerun_table = pd.DataFrame(rerun).drop(columns="runtime_seconds")
saved_table = pd.read_csv(ex.RESULTS_DIR / "02_experiments.csv").drop(columns="runtime_seconds")
same = np.allclose(rerun_table[["n_clusters", "noise_fraction", "silhouette", "ari_reference"]].fillna(-9).to_numpy(float),
                   saved_table[["n_clusters", "noise_fraction", "silhouette", "ari_reference"]].fillna(-9).to_numpy(float))
print("Semua hasil identik dengan catatan tersimpan (tanpa waktu jalan):", bool(same))
# --8<-- [end:repro]

# --8<-- [start:plot]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, eps in zip(axes, [0.15, 0.2, 0.3, 0.4]):
    labels = DBSCAN(eps=eps, min_samples=5).fit_predict(X_moons)
    for c in sorted(set(labels)):
        if c == -1:
            ax.scatter(X_moons[labels == c, 0], X_moons[labels == c, 1], s=22, marker="x", color="gray")
        else:
            ax.scatter(X_moons[labels == c, 0], X_moons[labels == c, 1], s=12, color=palette[c % len(palette)])
    ax.set_title(f"eps = {eps}  ({len(set(labels) - {-1})} kelompok, {int((labels == -1).sum())} noise)", fontsize=9)
    ax.set_xlabel("Fitur 1 (terskala)")
axes[0].set_ylabel("Fitur 2 (terskala)")
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, (column, title) in zip(axes, [("n_clusters", "Jumlah kelompok"), ("noise_fraction", "Proporsi noise")]):
    pivot = factorial_table.pivot(index="eps", columns="min_samples", values=column)
    image = ax.imshow(pivot.to_numpy(float), cmap="viridis", aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for r in range(pivot.shape[0]):
        for c in range(pivot.shape[1]):
            ax.text(c, r, f"{pivot.to_numpy(float)[r, c]:.2f}".rstrip("0").rstrip("."), ha="center", va="center", color="white", fontsize=9)
    ax.set_xlabel("min_samples")
    ax.set_ylabel("eps")
    ax.set_title(title)
    fig.colorbar(image, ax=ax, fraction=0.046)
plt.tight_layout()
plt.show()
# --8<-- [end:plot]
