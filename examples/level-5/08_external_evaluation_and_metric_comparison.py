"""Level 5, Bab 8: Evaluasi eksternal dan perbandingan metrik.

Jalankan dari folder utama proyek:
    python examples/level-5/08_external_evaluation_and_metric_comparison.py
"""
# NB: setup=Siapkan alat | permutation=Nomor kelompok itu sembarang | contingency=Tabel kontingensi | arimanual=ARI dihitung manual | hcv=Homogeneity, completeness, dan V-measure | nmimanual=NMI dihitung manual | datasets=Tiga dataset dengan label acuan | algos=Empat algoritma Level 4 | tables=Tabel perbandingan metrik | epssweep=Kepekaan DBSCAN terhadap eps | plotgrid=Menggambar hasil tiap algoritma | plotbars=Metrik internal dan eksternal berdampingan | mall=Mall Customers tanpa label acuan | refgender=Label acuan harus bermakna

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
from math import comb
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.datasets import make_blobs, make_circles, make_moons
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    completeness_score,
    davies_bouldin_score,
    homogeneity_score,
    normalized_mutual_info_score,
    silhouette_score,
    v_measure_score,
)
from sklearn.metrics.cluster import contingency_matrix
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["08-hasil-algoritma", "08-metrik-berdampingan"])

# --8<-- [start:permutation]
# Label acuan (kelas sebenarnya) dan dua hasil clustering yang mengelompokkan data IDENTIK,
# hanya nomor kelompoknya yang berbeda
y_true = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
pred_same = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
pred_permuted = np.array([2, 2, 2, 0, 0, 0, 1, 1, 1])

print("Kecocokan langsung (pred == true), nomor sama    :", (pred_same == y_true).mean().round(3))
print("Kecocokan langsung (pred == true), nomor ditukar :", (pred_permuted == y_true).mean().round(3))
print("ARI nomor sama    :", adjusted_rand_score(y_true, pred_same))
print("ARI nomor ditukar :", adjusted_rand_score(y_true, pred_permuted))
print("NMI nomor ditukar :", normalized_mutual_info_score(y_true, pred_permuted))
# --8<-- [end:permutation]

# --8<-- [start:contingency]
# Hasil clustering yang tidak sempurna: dua titik salah kelompok
pred_mixed = np.array([0, 0, 1, 1, 1, 1, 2, 2, 0])
table = pd.crosstab(
    pd.Series(y_true, name="Kelas sebenarnya"),
    pd.Series(pred_mixed, name="Kelompok hasil clustering"),
)
print(table)
# --8<-- [end:contingency]

# --8<-- [start:arimanual]
def ari_manual(labels_true, labels_pred):
    """Adjusted Rand Index dari tabel kontingensi, dengan menghitung pasangan titik."""
    cont = contingency_matrix(labels_true, labels_pred)
    n = cont.sum()
    sum_cells = sum(comb(int(v), 2) for v in cont.ravel())          # pasangan yang bersama di kelas DAN kelompok
    sum_rows = sum(comb(int(v), 2) for v in cont.sum(axis=1))       # pasangan yang bersama di kelas
    sum_cols = sum(comb(int(v), 2) for v in cont.sum(axis=0))       # pasangan yang bersama di kelompok
    expected = sum_rows * sum_cols / comb(int(n), 2)                # nilai yang diharapkan secara kebetulan
    maximum = 0.5 * (sum_rows + sum_cols)
    print(f"Pasangan sel = {sum_cells}, baris = {sum_rows}, kolom = {sum_cols}, "
          f"total pasangan = {comb(int(n), 2)}, diharapkan = {expected:.3f}, maksimum = {maximum:.1f}")
    return (sum_cells - expected) / (maximum - expected)


print(f"ARI manual        = {ari_manual(y_true, pred_mixed):.4f}")
print(f"ARI scikit-learn  = {adjusted_rand_score(y_true, pred_mixed):.4f}")
# --8<-- [end:arimanual]

# --8<-- [start:hcv]
n_demo = len(y_true)
one_cluster = np.zeros(n_demo, dtype=int)                 # semua titik digabung jadi satu kelompok
each_alone = np.arange(n_demo)                            # setiap titik jadi kelompok sendiri

cases = {
    "Sempurna": pred_same,
    "Dua titik salah": pred_mixed,
    "Semua digabung (1 kelompok)": one_cluster,
    "Tiap titik sendiri (9 kelompok)": each_alone,
}
rows = []
for name, labels in cases.items():
    rows.append(
        {
            "Kasus": name,
            "Homogeneity": homogeneity_score(y_true, labels),
            "Completeness": completeness_score(y_true, labels),
            "V-measure": v_measure_score(y_true, labels),
            "NMI": normalized_mutual_info_score(y_true, labels),
            "ARI": adjusted_rand_score(y_true, labels),
        }
    )
print(pd.DataFrame(rows).set_index("Kasus").round(3).to_string())
# --8<-- [end:hcv]

# --8<-- [start:nmimanual]
def entropy(labels):
    """Entropi (dalam nat, logaritma natural) dari sebuah pelabelan."""
    _, counts = np.unique(labels, return_counts=True)
    p = counts / counts.sum()
    return -(p * np.log(p)).sum()


def nmi_manual(labels_true, labels_pred):
    """NMI = informasi bersama / rata-rata aritmetika dari dua entropi."""
    cont = contingency_matrix(labels_true, labels_pred).astype(float)
    n = cont.sum()
    pij = cont / n
    pi = pij.sum(axis=1, keepdims=True)
    pj = pij.sum(axis=0, keepdims=True)
    nonzero = pij > 0
    mutual_info = (pij[nonzero] * np.log(pij[nonzero] / (pi @ pj)[nonzero])).sum()
    h_true, h_pred = entropy(labels_true), entropy(labels_pred)
    print(f"H(kelas) = {h_true:.4f}, H(kelompok) = {h_pred:.4f}, informasi bersama = {mutual_info:.4f}")
    return mutual_info / (0.5 * (h_true + h_pred))


print(f"NMI manual        = {nmi_manual(y_true, pred_mixed):.4f}")
print(f"NMI scikit-learn  = {normalized_mutual_info_score(y_true, pred_mixed):.4f}")
# --8<-- [end:nmimanual]

# --8<-- [start:datasets]
# Label acuan (y) hanya dipakai untuk MENILAI, tidak pernah diberikan ke algoritma clustering
X_blobs, y_blobs = make_blobs(n_samples=300, centers=3, cluster_std=1.5, random_state=42)
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
X_circles, y_circles = make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)

datasets = {
    "Blobs": (StandardScaler().fit_transform(X_blobs), y_blobs, 3),
    "Moons": (StandardScaler().fit_transform(X_moons), y_moons, 2),
    "Circles": (StandardScaler().fit_transform(X_circles), y_circles, 2),
}
# eps DBSCAN dipilih setelah melihat data (belum pencarian parameter sistematis, itu materi Level 6)
dbscan_eps = {"Blobs": 0.30, "Moons": 0.30, "Circles": 0.30}
for name, (X, y, k) in datasets.items():
    print(f"{name:8s} bentuk data {X.shape}, jumlah kelas acuan = {k}, ukuran kelas = {np.bincount(y).tolist()}")
# --8<-- [end:datasets]

# --8<-- [start:algos]
def run_algorithms(name, X, k):
    """Empat algoritma Level 4. Hanya X yang diberikan, tanpa label acuan."""
    return {
        "K-Means": KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X),
        "Hierarchical (Ward)": AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(X),
        "DBSCAN": DBSCAN(eps=dbscan_eps[name], min_samples=5).fit_predict(X),
        "GMM": GaussianMixture(n_components=k, random_state=42).fit(X).predict(X),
    }


results = {name: run_algorithms(name, X, k) for name, (X, y, k) in datasets.items()}
for name, algos in results.items():
    dbscan_labels = algos["DBSCAN"]
    n_noise = int((dbscan_labels == -1).sum())
    n_found = len(set(dbscan_labels) - {-1})
    print(f"{name:8s} DBSCAN: {n_found} kelompok, {n_noise} titik noise dari {len(dbscan_labels)}")
# --8<-- [end:algos]

# --8<-- [start:tables]
def internal_scores(X, labels):
    """Metrik internal. Noise DBSCAN (-1) DIKELUARKAN dulu, dan butuh minimal 2 kelompok tersisa."""
    mask = labels != -1
    Xm, lm = X[mask], labels[mask]
    if len(set(lm)) < 2:
        return {"Silhouette": np.nan, "Davies-Bouldin": np.nan, "Calinski-Harabasz": np.nan}
    return {
        "Silhouette": silhouette_score(Xm, lm),
        "Davies-Bouldin": davies_bouldin_score(Xm, lm),
        "Calinski-Harabasz": calinski_harabasz_score(Xm, lm),
    }


def external_scores(y, labels):
    """Metrik eksternal. Di sini noise (-1) DIPERLAKUKAN sebagai satu kelompok tersendiri."""
    return {
        "ARI": adjusted_rand_score(y, labels),
        "NMI": normalized_mutual_info_score(y, labels),
        "Homogeneity": homogeneity_score(y, labels),
        "Completeness": completeness_score(y, labels),
        "V-measure": v_measure_score(y, labels),
    }


all_tables = {}
for name, (X, y, k) in datasets.items():
    rows = []
    for algo, labels in results[name].items():
        row = {"Algoritma": algo, **internal_scores(X, labels), **external_scores(y, labels)}
        if algo == "K-Means":   # Inertia hanya bermakna untuk objektif centroid
            row["Inertia"] = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X).inertia_
        rows.append(row)
    all_tables[name] = pd.DataFrame(rows).set_index("Algoritma")
    print(f"\n=== {name} ===")
    print("Metrik internal (butuh X dan label hasil clustering):")
    print(all_tables[name][["Silhouette", "Davies-Bouldin", "Calinski-Harabasz", "Inertia"]].round(3).to_string())
    print("Metrik eksternal (butuh label acuan):")
    print(all_tables[name][["ARI", "NMI", "Homogeneity", "Completeness", "V-measure"]].round(3).to_string())
# --8<-- [end:tables]

# --8<-- [start:epssweep]
# Kepekaan DBSCAN terhadap eps pada Circles. PERINGATAN: label acuan dipakai di sini hanya
# untuk MENUNJUKKAN kepekaan. Dalam praktik, memilih eps agar ARI tinggi berarti memakai label
# untuk menyetel model (kebocoran informasi), sehingga skor eksternal tidak lagi jujur.
X_c, y_c, _ = datasets["Circles"]
for eps in (0.20, 0.25, 0.30, 0.35, 0.40):
    labels = DBSCAN(eps=eps, min_samples=5).fit_predict(X_c)
    n_found = len(set(labels) - {-1})
    print(f"eps = {eps:.2f}: {n_found:2d} kelompok, {int((labels == -1).sum()):2d} noise, ARI = {adjusted_rand_score(y_c, labels):.3f}")
# --8<-- [end:epssweep]

# --8<-- [start:plotgrid]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]
algo_names = list(results["Blobs"].keys())

fig, axes = plt.subplots(3, 4, figsize=(15, 10.5))
for row, (name, (X, y, k)) in enumerate(datasets.items()):
    for col, algo in enumerate(algo_names):
        labels = results[name][algo]
        ax = axes[row, col]
        for c in sorted(set(labels)):
            if c == -1:
                ax.scatter(X[labels == c, 0], X[labels == c, 1], s=22, marker="x", color="gray")
            else:
                ax.scatter(X[labels == c, 0], X[labels == c, 1], s=12, color=palette[c % len(palette)])
        ari = all_tables[name].loc[algo, "ARI"]
        ax.set_title(f"{name} - {algo}\nARI = {ari:.3f}", fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
plt.tight_layout()
plt.show()
# --8<-- [end:plotgrid]

# --8<-- [start:plotbars]
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
width = 0.38
for ax, (name, table) in zip(axes, all_tables.items()):
    positions = np.arange(len(table))
    ax.bar(positions - width / 2, table["Silhouette"], width, color=palette[0], label="Silhouette (internal)")
    ax.bar(positions + width / 2, table["ARI"], width, color=palette[1], label="ARI (eksternal)")
    ax.set_xticks(positions)
    ax.set_xticklabels(table.index, rotation=20, fontsize=8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(name)
    ax.set_ylabel("Skor")
axes[1].legend(fontsize=8, loc="upper left")
plt.tight_layout()
plt.show()
# --8<-- [end:plotbars]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

mall_results = {
    "K-Means": KMeans(n_clusters=5, n_init=10, random_state=42).fit_predict(X_mall),
    "Hierarchical (Ward)": AgglomerativeClustering(n_clusters=5, linkage="ward").fit_predict(X_mall),
    "GMM": GaussianMixture(n_components=5, random_state=42).fit(X_mall).predict(X_mall),
}
mall_rows = [{"Algoritma": name, **internal_scores(X_mall, labels)} for name, labels in mall_results.items()]
print(pd.DataFrame(mall_rows).set_index("Algoritma").round(3).to_string())
print("Tidak ada label acuan pada Mall Customers, jadi metrik eksternal tidak bisa dihitung.")
# --8<-- [end:mall]

# --8<-- [start:refgender]
# Gender adalah label yang ADA di tabel, tetapi apakah ia 'jawaban benar' untuk pengelompokan ini?
gender = (df["Gender"] == "Male").astype(int).to_numpy()
km_mall = mall_results["K-Means"]
print(f"ARI antara K-Means dan Gender : {adjusted_rand_score(gender, km_mall):.4f}")
print(f"NMI antara K-Means dan Gender : {normalized_mutual_info_score(gender, km_mall):.4f}")
# --8<-- [end:refgender]
