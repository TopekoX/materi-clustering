"""Level 6, Bab 1: Pengantar eksperimen clustering.

Jalankan dari folder utama proyek:
    python examples/level-6/01_introduction_to_clustering_experiments.py
"""
# NB: setup=Siapkan alat | question=Merumuskan pertanyaan dan variabel | data=Dataset dan karakteristiknya | baseline=Baseline dan kebisingan antar-seed | conditions=Menjalankan empat kondisi | commonspace=Mengukur di ruang yang sama | plot=Menggambar empat kondisi | summary=Meringkas temuan

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
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-empat-kondisi-skala"])

# --8<-- [start:question]
# Rancangan eksperimen ditulis lebih dulu, sebelum menjalankan apa pun
experiment = {
    "pertanyaan": "Apakah cara menyamakan skala mengubah pengelompokan pelanggan Mall Customers?",
    "variabel_bebas": "perlakuan skala fitur (4 kondisi)",
    "variabel_terkontrol": "algoritma K-Means, K = 5, n_init = 10, seed = 42, dua fitur yang sama",
    "variabel_terikat": "kesamaan pengelompokan dengan baseline (ARI), ukuran kelompok, Silhouette di ruang bersama",
    "baseline": "StandardScaler",
}
for key, value in experiment.items():
    print(f"{key:20s}: {value}")
# --8<-- [end:question]

# --8<-- [start:data]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_raw = df[features].to_numpy(dtype=float)

print("Jumlah pelanggan :", len(df))
print("Fitur dipakai    :", features)
print(df[features].describe().loc[["min", "max", "mean", "std"]].round(2).to_string())
# --8<-- [end:data]

# --8<-- [start:baseline]
SEED = 42
X_standard = StandardScaler().fit_transform(X_raw)   # kondisi baseline
baseline = KMeans(n_clusters=5, n_init=10, random_state=SEED).fit_predict(X_standard)
print("Ukuran kelompok baseline:", sorted(np.bincount(baseline).tolist(), reverse=True))

# Kebisingan baseline: ulangi baseline dengan seed lain, lalu bandingkan dengan ARI
runs = [KMeans(n_clusters=5, n_init=10, random_state=seed).fit_predict(X_standard) for seed in range(10)]
ari_between_runs = [adjusted_rand_score(runs[0], run) for run in runs[1:]]
print("ARI baseline seed 0 vs seed 1..9, terkecil:", round(min(ari_between_runs), 4))
print("ARI baseline seed 0 vs seed 1..9, terbesar:", round(max(ari_between_runs), 4))
# --8<-- [end:baseline]

# --8<-- [start:conditions]
X_dollars = X_raw.copy()
X_dollars[:, 0] *= 1000            # pendapatan dalam dolar, bukan ribu dolar

conditions = {
    "A. StandardScaler (baseline)": X_standard,
    "B. MinMaxScaler": MinMaxScaler().fit_transform(X_raw),
    "C. Tanpa skala (k$)": X_raw,
    "D. Tanpa skala (pendapatan dalam dolar)": X_dollars,
}

labels_by_condition = {}
for name, X_condition in conditions.items():
    labels_by_condition[name] = KMeans(n_clusters=5, n_init=10, random_state=SEED).fit_predict(X_condition)
    sizes = sorted(np.bincount(labels_by_condition[name]).tolist(), reverse=True)
    print(f"{name:42s} ukuran kelompok: {sizes}")
# --8<-- [end:conditions]

# --8<-- [start:commonspace]
rows = []
for name, X_condition in conditions.items():
    labels = labels_by_condition[name]
    rows.append(
        {
            "Kondisi": name,
            "ARI vs baseline": adjusted_rand_score(baseline, labels),
            "Silhouette (ruang sendiri)": silhouette_score(X_condition, labels),
            "Silhouette (ruang bersama)": silhouette_score(X_standard, labels),
        }
    )
result_table = pd.DataFrame(rows).set_index("Kondisi")
print(result_table.round(3).to_string())
# --8<-- [end:commonspace]

# --8<-- [start:plot]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 4, figsize=(17, 4.2), sharex=True, sharey=True)
for ax, (name, labels) in zip(axes, labels_by_condition.items()):
    for c in range(5):
        ax.scatter(X_raw[labels == c, 0], X_raw[labels == c, 1], s=14, color=palette[c])
    ari = result_table.loc[name, "ARI vs baseline"]
    ax.set_title(f"{name}\nARI vs baseline = {ari:.3f}", fontsize=9)
    ax.set_xlabel("Pendapatan tahunan (k$)")
axes[0].set_ylabel("Skor belanja (1-100)")
plt.tight_layout()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:summary]
for name in conditions:
    ari = result_table.loc[name, "ARI vs baseline"]
    verdict = "praktis sama dengan baseline" if ari >= 0.95 else "berbeda dari baseline"
    print(f"{name:42s} ARI = {ari:.3f} -> {verdict}")
# --8<-- [end:summary]
