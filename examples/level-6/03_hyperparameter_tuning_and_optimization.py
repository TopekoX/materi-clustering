"""Level 6, Bab 3: Hyperparameter tuning dan optimasi.

Jalankan dari folder utama proyek:
    python examples/level-6/03_hyperparameter_tuning_and_optimization.py
"""
# NB: setup=Siapkan alat | paramtypes=Parameter dan hyperparameter | kmeans=Hyperparameter K-Means | hier=Hyperparameter Hierarchical | gmm=Hyperparameter GMM | meanshift=Hyperparameter Mean Shift | grid=Pencarian grid DBSCAN | naive=Memilih dengan satu metrik | constrained=Memilih dengan batasan | random=Pencarian acak | multimetric=Satu metrik tidak cukup untuk memilih K | nopredict=Mengapa GridSearchCV tidak dipakai buta | save=Menyimpan hasil pencarian | plotsens=Menggambar sensitivitas eps | plotsel=Menggambar peta pemilihan

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
from scipy.stats import randint, uniform
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans, MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import ParameterGrid, ParameterSampler
from sklearn.preprocessing import StandardScaler

import _experiment as ex

SEED = 42
# --8<-- [end:setup]

import _savefig

_savefig.install(["03-sensitivitas-eps", "03-peta-pemilihan"])

# --8<-- [start:paramtypes]
model = KMeans(n_clusters=3, n_init=10, random_state=SEED)
print("Hyperparameter (kamu yang menentukan, sebelum fit):")
params = model.get_params()
print({name: params[name] for name in ["n_clusters", "init", "n_init", "max_iter", "tol", "random_state"]})

X_demo, _ = make_blobs(n_samples=200, centers=3, random_state=SEED)
model.fit(X_demo)
print("Parameter yang DIPELAJARI (hasil fit, berakhiran _):")
print("  cluster_centers_ bentuk :", model.cluster_centers_.shape)
print(f"  inertia_                : {model.inertia_:.2f}")
print("  n_iter_                 :", model.n_iter_)
# --8<-- [end:paramtypes]

# --8<-- [start:kmeans]
# Data dengan enam gerombol yang sebagian bertumpuk, supaya pengaruh inisialisasi terlihat
X_six, y_six = make_blobs(n_samples=600, centers=6, cluster_std=1.6, random_state=SEED)

rows = []
for init in ["random", "k-means++"]:
    for n_init in [1, 10]:
        inertias = [KMeans(n_clusters=6, init=init, n_init=n_init, random_state=seed).fit(X_six).inertia_ for seed in range(20)]
        rows.append({"init": init, "n_init": n_init, "inertia terkecil": min(inertias), "inertia terbesar": max(inertias),
                     "seed yang mencapai terkecil": sum(abs(v - min(inertias)) < 1e-6 for v in inertias)})
print(pd.DataFrame(rows).round(2).to_string(index=False))

for max_iter in [1, 2, 5, 300]:
    model = KMeans(n_clusters=6, init="random", n_init=1, max_iter=max_iter, random_state=SEED).fit(X_six)
    print(f"max_iter = {max_iter:3d}: n_iter_ = {model.n_iter_}, inertia = {model.inertia_:.2f}")
# --8<-- [end:kmeans]

# --8<-- [start:hier]
X_moons_raw, y_moons = make_moons(n_samples=300, noise=0.06, random_state=SEED)
X_moons = StandardScaler().fit_transform(X_moons_raw)

rows = []
for linkage, metric in [("ward", "euclidean"), ("complete", "euclidean"), ("complete", "manhattan"),
                        ("average", "euclidean"), ("average", "cosine"), ("single", "euclidean")]:
    labels = AgglomerativeClustering(n_clusters=2, linkage=linkage, metric=metric).fit_predict(X_moons)
    rows.append({"linkage": linkage, "metric": metric, "ARI acuan": adjusted_rand_score(y_moons, labels),
                 "ukuran kelompok": sorted(np.bincount(labels).tolist())})
print(pd.DataFrame(rows).round(3).to_string(index=False))
# --8<-- [end:hier]

# --8<-- [start:gmm]
# Gerombol miring (anisotropik): bentuknya elips, bukan bulat
X_a, y_a = make_blobs(n_samples=500, centers=3, cluster_std=1.0, random_state=SEED)
X_aniso = X_a @ np.array([[0.6, -0.6], [-0.4, 0.8]])

rows = []
for covariance_type in ["spherical", "diag", "tied", "full"]:
    labels = GaussianMixture(n_components=3, covariance_type=covariance_type, random_state=SEED).fit_predict(X_aniso)
    rows.append({"covariance_type": covariance_type, "ARI acuan": adjusted_rand_score(y_a, labels)})
print(pd.DataFrame(rows).round(3).to_string(index=False))

for reg_covar in [1e-6, 1e-3, 1e-1, 1.0]:
    labels = GaussianMixture(n_components=3, covariance_type="full", reg_covar=reg_covar, random_state=SEED).fit_predict(X_aniso)
    print(f"reg_covar = {reg_covar:g}: ARI acuan = {adjusted_rand_score(y_a, labels):.3f}")
for n_components in [2, 3, 4, 6]:
    labels = GaussianMixture(n_components=n_components, covariance_type="full", random_state=SEED).fit_predict(X_aniso)
    print(f"n_components = {n_components}: ARI acuan = {adjusted_rand_score(y_a, labels):.3f}")
# --8<-- [end:gmm]

# --8<-- [start:meanshift]
X_b3, y_b3 = make_blobs(n_samples=400, centers=3, cluster_std=1.0, random_state=SEED)
print("estimate_bandwidth(quantile=0.2):", round(estimate_bandwidth(X_b3, quantile=0.2, random_state=SEED), 3))

rows = []
for bandwidth in [0.5, 1.0, 2.0, 4.0, 8.0]:
    labels = MeanShift(bandwidth=bandwidth).fit_predict(X_b3)
    rows.append({"bandwidth": bandwidth, "jumlah kelompok": len(set(labels)), "ARI acuan": adjusted_rand_score(y_b3, labels)})
print(pd.DataFrame(rows).round(3).to_string(index=False))

for bin_seeding, min_bin_freq in [(False, 1), (True, 1), (True, 5), (True, 20)]:
    labels = MeanShift(bandwidth=2.0, bin_seeding=bin_seeding, min_bin_freq=min_bin_freq).fit_predict(X_b3)
    print(f"bin_seeding = {bin_seeding!s:5}, min_bin_freq = {min_bin_freq:2d}: {len(set(labels))} kelompok, ARI acuan = {adjusted_rand_score(y_b3, labels):.3f}")
# --8<-- [end:meanshift]

# --8<-- [start:grid]
# Pencarian grid DBSCAN pada moons. Metrik internal untuk memilih, ARI hanya untuk menilai kemudian.
grid = ParameterGrid({"eps": [round(v, 2) for v in np.arange(0.10, 0.61, 0.05)], "min_samples": [3, 5, 10, 15, 20, 30]})
print("Jumlah kombinasi:", len(grid))


def evaluate_dbscan(params):
    labels = DBSCAN(**params).fit_predict(X_moons)
    scores = ex.internal_scores(X_moons, labels)
    scores["ari_reference"] = adjusted_rand_score(y_moons, labels)
    return {**params, **scores}


grid_table = pd.DataFrame([evaluate_dbscan(p) for p in grid])
print("Kombinasi dengan Silhouette bisa dihitung:", int(grid_table["silhouette"].notna().sum()), "dari", len(grid_table))
# --8<-- [end:grid]

# --8<-- [start:naive]
valid = grid_table.dropna(subset=["silhouette"])
cols = ["eps", "min_samples", "n_clusters", "noise_fraction", "silhouette", "davies_bouldin", "ari_reference"]
print("Dipilih dengan Silhouette tertinggi (tanpa batasan):")
print(valid.sort_values("silhouette", ascending=False).head(3)[cols].round(3).to_string(index=False))
print("Dipilih dengan Davies-Bouldin terendah (tanpa batasan):")
print(valid.sort_values("davies_bouldin").head(3)[cols].round(3).to_string(index=False))
# --8<-- [end:naive]

# --8<-- [start:constrained]
# Batasan yang masuk akal, ditetapkan SEBELUM melihat hasil: noise paling banyak 5%, 2 sampai 10 kelompok
allowed = valid[(valid["noise_fraction"] <= 0.05) & valid["n_clusters"].between(2, 10)]
print("Kombinasi yang memenuhi batasan:", len(allowed), "dari", len(valid))
print("Dipilih dengan Silhouette tertinggi di antara yang memenuhi batasan:")
print(allowed.sort_values("silhouette", ascending=False).head(3)[cols].round(3).to_string(index=False))
print("Dari kombinasi yang memenuhi batasan, ARI acuan terbesar adalah:", round(allowed["ari_reference"].max(), 3))
# --8<-- [end:constrained]

# --8<-- [start:random]
# Pencarian acak: 20 kombinasi dari distribusi, diulang dengan seed pengambil sampel berbeda
space = {"eps": uniform(0.10, 0.50), "min_samples": randint(3, 31)}
rows = []
for sampler_seed in range(5):
    sampled = list(ParameterSampler(space, n_iter=20, random_state=sampler_seed))
    table = pd.DataFrame([evaluate_dbscan({"eps": round(p["eps"], 3), "min_samples": int(p["min_samples"])}) for p in sampled])
    table = table.dropna(subset=["silhouette"])
    table = table[(table["noise_fraction"] <= 0.05) & table["n_clusters"].between(2, 10)]
    best = table.sort_values("silhouette", ascending=False).iloc[0]
    rows.append({"seed sampler": sampler_seed, "eps": best["eps"], "min_samples": int(best["min_samples"]),
                 "silhouette": best["silhouette"], "ARI acuan": best["ari_reference"]})
print(pd.DataFrame(rows).round(3).to_string(index=False))
# --8<-- [end:random]

# --8<-- [start:multimetric]
rows = []
for k in range(2, 11):
    labels = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(X_six)
    scores = ex.internal_scores(X_six, labels)
    rows.append({"K": k, "Silhouette": scores["silhouette"], "Davies-Bouldin": scores["davies_bouldin"],
                 "Calinski-Harabasz": scores["calinski_harabasz"], "ARI acuan": adjusted_rand_score(y_six, labels)})
k_table = pd.DataFrame(rows).set_index("K")
print(k_table.round(3).to_string())
print("K terbaik menurut Silhouette        :", int(k_table["Silhouette"].idxmax()))
print("K terbaik menurut Davies-Bouldin    :", int(k_table["Davies-Bouldin"].idxmin()))
print("K terbaik menurut Calinski-Harabasz :", int(k_table["Calinski-Harabasz"].idxmax()))
# --8<-- [end:multimetric]

# --8<-- [start:nopredict]
for name, estimator in [("KMeans", KMeans()), ("GaussianMixture", GaussianMixture()), ("MeanShift", MeanShift()),
                        ("DBSCAN", DBSCAN()), ("AgglomerativeClustering", AgglomerativeClustering())]:
    print(f"{name:24s} punya predict(): {hasattr(estimator, 'predict')}")
# --8<-- [end:nopredict]

# --8<-- [start:save]
grid_table.insert(0, "experiment_id", [f"GRID-{i:02d}" for i in range(1, len(grid_table) + 1)])
grid_table.to_csv(ex.RESULTS_DIR / "03_dbscan_grid.csv", index=False)
ex.save_json({"seed": SEED, "dataset": "make_moons(n_samples=300, noise=0.06) + StandardScaler",
              "space": "eps 0.10..0.60 langkah 0.05, min_samples [3,5,10,15,20,30]",
              "constraint": "noise <= 5% dan 2..10 kelompok", "fingerprint": ex.dataset_fingerprint(X_moons)}, "03_search_config")
print("Hasil pencarian grid disimpan:", len(grid_table), "baris")
# --8<-- [end:save]

# --8<-- [start:plotsens]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for color, min_samples in zip(palette, [3, 10, 30]):
    part = grid_table[grid_table["min_samples"] == min_samples].sort_values("eps")
    axes[0].plot(part["eps"], part["n_clusters"], marker="o", color=color, label=f"min_samples = {min_samples}")
    axes[1].plot(part["eps"], part["noise_fraction"] * 100, marker="o", color=color)
    axes[2].plot(part["eps"], part["ari_reference"], marker="o", color=color)
axes[0].set_ylabel("Jumlah kelompok")
axes[1].set_ylabel("Noise (%)")
axes[2].set_ylabel("ARI terhadap label acuan")
for ax in axes:
    ax.set_xlabel("eps")
axes[0].legend(fontsize=8)
fig.suptitle("Sensitivitas DBSCAN terhadap eps pada moons", y=1.02)
plt.tight_layout()
plt.show()
# --8<-- [end:plotsens]

# --8<-- [start:plotsel]
fig, ax = plt.subplots(figsize=(7, 5))
points = ax.scatter(valid["noise_fraction"] * 100, valid["silhouette"], c=valid["ari_reference"], cmap="viridis", s=45, edgecolor="black", linewidth=0.4)
top = valid.sort_values("silhouette", ascending=False).iloc[0]
ax.scatter([top["noise_fraction"] * 100], [top["silhouette"]], s=220, facecolors="none", edgecolors="#D55E00", linewidths=2, label="Silhouette tertinggi")
ax.axvline(5, color="gray", linestyle="--", label="Batas noise 5%")
ax.set_xlabel("Proporsi noise (%)")
ax.set_ylabel("Silhouette (noise dikeluarkan)")
ax.set_title("Setiap titik = satu kombinasi (eps, min_samples)")
ax.legend(fontsize=8, loc="lower right")
fig.colorbar(points, label="ARI terhadap label acuan")
plt.tight_layout()
plt.show()
# --8<-- [end:plotsel]
