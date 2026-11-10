"""Level 4, Bab 7: membandingkan K-Means, Hierarchical, DBSCAN, GMM, dan Mean Shift.

Jalankan dari folder utama proyek:
    python examples/level-4/07_comparison_of_clustering_algorithms.py

Catatan: bagian skalabilitas memakai waktu nyata, jadi angkanya berbeda di tiap mesin dan tiap eksekusi.
"""
# NB: setup=Siapkan alat | datasets=Enam dataset sintetis | recipe=Pengaturan tiap algoritma | run=Menjalankan semua kombinasi | summary=Ringkasan jumlah kelompok dan noise | plotgrid=Grid perbandingan visual | capabilities=Kemampuan tiap objek | soft=Soft clustering pada GMM | scalability=Waktu jalan terhadap jumlah data | plotscal=Menggambar skalabilitas | mall=Perbandingan pada Mall Customers | crosstab=Tabel silang K-Means dan GMM | plotmall=Menggambar hasil Mall | guide=Fungsi panduan pemilihan algoritma | guidetest=Mencoba panduan pada beberapa profil data

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MeanShift, estimate_bandwidth
from sklearn.datasets import make_blobs, make_moons, make_circles
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["07-perbandingan-algoritma", "07-skalabilitas", "07-mall-perbandingan"])

# --8<-- [start:datasets]
rng = np.random.default_rng(42)

blobs_core, _ = make_blobs(n_samples=270, centers=3, cluster_std=0.8, random_state=42)
noise_points = rng.uniform(blobs_core.min(axis=0) - 1, blobs_core.max(axis=0) + 1, size=(30, 2))
overlap_raw, _ = make_blobs(n_samples=300, centers=[[0, 0], [3, 2], [1, 4]], cluster_std=1.1, random_state=42)

datasets = {
    "blobs": make_blobs(n_samples=300, centers=3, cluster_std=0.8, random_state=42)[0],
    "moons": make_moons(n_samples=300, noise=0.06, random_state=42)[0],
    "circles": make_circles(n_samples=300, noise=0.05, factor=0.5, random_state=42)[0],
    "noisy": np.vstack([blobs_core, noise_points]),   # tiga gerombol + 30 titik acak
    "density": make_blobs(n_samples=[150, 100, 50], centers=[[0, 0], [4, 0], [2, 5]],
                          cluster_std=[0.3, 1.0, 0.5], random_state=42)[0],
    "overlap": overlap_raw @ np.array([[1.0, 0.6], [0.0, 0.8]]),  # elips tumpang tindih
}
# Semua dataset diskalakan dulu (rata-rata 0, simpangan baku 1)
datasets = {name: StandardScaler().fit_transform(X) for name, X in datasets.items()}
print({name: X.shape for name, X in datasets.items()})
# --8<-- [end:datasets]

# --8<-- [start:recipe]
# Jumlah kelompok untuk K-Means, Ward, dan GMM (kita tahu strukturnya karena data buatan)
n_clusters = {"blobs": 3, "moons": 2, "circles": 2, "noisy": 3, "density": 3, "overlap": 3}
# eps DBSCAN dipilih per dataset setelah melihat datanya (min_samples = 5 untuk semua)
eps_values = {"blobs": 0.3, "moons": 0.3, "circles": 0.4, "noisy": 0.3, "density": 0.4, "overlap": 0.2}

def build_models(name, X):
    k = n_clusters[name]
    bandwidth = estimate_bandwidth(X, quantile=0.2, random_state=42)   # sama untuk semua dataset
    return {
        "K-Means": KMeans(n_clusters=k, n_init=10, random_state=42),
        "Hierarchical (Ward)": AgglomerativeClustering(n_clusters=k, linkage="ward"),
        "DBSCAN": DBSCAN(eps=eps_values[name], min_samples=5),
        "GMM": GaussianMixture(n_components=k, covariance_type="full", n_init=5, random_state=42),
        "Mean Shift": MeanShift(bandwidth=bandwidth),
    }

settings = pd.DataFrame(
    {"K (K-Means/Ward/GMM)": n_clusters, "eps DBSCAN": eps_values,
     "bandwidth Mean Shift": {name: round(estimate_bandwidth(X, quantile=0.2, random_state=42), 3)
                              for name, X in datasets.items()}}
)
print(settings.to_string())
# --8<-- [end:recipe]

# --8<-- [start:run]
results = {}  # (nama dataset, nama algoritma) -> label
for name, X in datasets.items():
    for algo_name, model in build_models(name, X).items():
        results[(name, algo_name)] = model.fit_predict(X)
# --8<-- [end:run]

# --8<-- [start:summary]
algo_names = list(build_models("blobs", datasets["blobs"]).keys())
rows = []
for name in datasets:
    row = {"dataset": name}
    for algo in algo_names:
        labels = results[(name, algo)]
        n_found = len(set(labels) - {-1})
        n_noise = int(np.sum(labels == -1))
        row[algo] = f"{n_found} kel" + (f", {n_noise} noise" if n_noise else "")
    rows.append(row)
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:summary]

# --8<-- [start:plotgrid]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442"]

fig, axes = plt.subplots(len(datasets), len(algo_names), figsize=(15, 17))
for row, (name, X) in enumerate(datasets.items()):
    for col, algo in enumerate(algo_names):
        ax = axes[row, col]
        labels = results[(name, algo)]
        for k in sorted(set(labels)):
            mask = labels == k
            if k == -1:   # noise DBSCAN
                ax.scatter(X[mask, 0], X[mask, 1], s=14, color="#777777", marker="x")
            else:
                ax.scatter(X[mask, 0], X[mask, 1], s=10, color=palette[k % len(palette)])
        if row == 0:
            ax.set_title(algo)
        ax.set_xticks([])
        ax.set_yticks([])
    axes[row, 0].set_ylabel(name)
plt.tight_layout()
plt.show()
# --8<-- [end:plotgrid]

# --8<-- [start:capabilities]
X_demo = datasets["blobs"]
fitted = {algo: model.fit(X_demo) for algo, model in build_models("blobs", X_demo).items()}

rows = []
for algo, model in fitted.items():
    rows.append(
        {
            "Algoritma": algo,
            "labels_": hasattr(model, "labels_"),
            "predict": hasattr(model, "predict"),
            "predict_proba": hasattr(model, "predict_proba"),
            "pusat kelompok": hasattr(model, "cluster_centers_") or hasattr(model, "means_"),
        }
    )
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:capabilities]

# --8<-- [start:soft]
X_ov = datasets["overlap"]
gmm_ov = GaussianMixture(n_components=3, covariance_type="full", n_init=5, random_state=42).fit(X_ov)
proba_ov = gmm_ov.predict_proba(X_ov)
confidence = proba_ov.max(axis=1)

print("Peluang tiga titik pertama dataset overlap (GMM):")
print(pd.DataFrame(proba_ov[:3], columns=["p_0", "p_1", "p_2"]).round(3).to_string())
print(f"\nTitik dengan peluang tertinggi < 0.9 : {int((confidence < 0.9).sum())} dari {len(X_ov)}")
print(f"Titik dengan peluang tertinggi < 0.6 : {int((confidence < 0.6).sum())} dari {len(X_ov)}")
print("Pada K-Means, Ward, DBSCAN, dan Mean Shift: tidak ada predict_proba (hanya satu label per titik).")
# --8<-- [end:soft]

# --8<-- [start:scalability]
def best_time(make_model, X, repeats):
    """Waktu tercepat dari beberapa kali jalan (detik)."""
    times = []
    for _ in range(repeats):
        model = make_model()
        start = time.perf_counter()
        model.fit(X)
        times.append(time.perf_counter() - start)
    return min(times)

factories = {
    "K-Means": (lambda: KMeans(n_clusters=3, n_init=10, random_state=42), 3),
    "Hierarchical (Ward)": (lambda: AgglomerativeClustering(n_clusters=3), 3),
    "DBSCAN": (lambda: DBSCAN(eps=0.5), 3),
    "GMM": (lambda: GaussianMixture(n_components=3, random_state=42), 3),
    "Mean Shift": (lambda: MeanShift(bandwidth=2.0), 1),   # lambat, cukup satu kali
}

# Pemanasan: jalankan sekali pada data kecil agar waktu pemuatan awal tidak ikut terhitung
X_warm, _ = make_blobs(n_samples=200, centers=3, random_state=0)
for make_model, _ in factories.values():
    make_model().fit(X_warm)

sizes = [500, 1000, 2000, 4000]
timing = {algo: [] for algo in factories}
for n in sizes:
    X_n, _ = make_blobs(n_samples=n, centers=3, cluster_std=1.0, random_state=42)
    for algo, (make_model, repeats) in factories.items():
        timing[algo].append(best_time(make_model, X_n, repeats))

table = pd.DataFrame(timing, index=sizes).round(3)
table.index.name = "n (jumlah data)"
print("Waktu fit (detik); angka bergantung mesin dan bisa berbeda tiap eksekusi:")
print(table.to_string())
print("\nRasio waktu saat n naik 4000/1000 (4 kali lipat data):")
print((table.loc[4000] / table.loc[1000]).round(1).to_string())
# --8<-- [end:scalability]

# --8<-- [start:plotscal]
fig, ax = plt.subplots(figsize=(7, 4.5))
for algo, color in zip(timing, palette):
    ax.plot(sizes, timing[algo], marker="o", color=color, label=algo)
ax.set_xlabel("Jumlah data (n)")
ax.set_ylabel("Waktu fit (detik)")
ax.set_yscale("log")
ax.set_title("Waktu komputasi terhadap jumlah data (sumbu y logaritmik)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotscal]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

bw_mall = estimate_bandwidth(X_mall, quantile=0.15, random_state=42)
mall_models = {
    "K-Means": KMeans(n_clusters=5, n_init=10, random_state=42),
    "Hierarchical (Ward)": AgglomerativeClustering(n_clusters=5, linkage="ward"),
    "DBSCAN": DBSCAN(eps=0.4, min_samples=8),
    "GMM": GaussianMixture(n_components=5, covariance_type="full", n_init=5, random_state=42),
    "Mean Shift": MeanShift(bandwidth=bw_mall),
}
mall_labels = {algo: model.fit_predict(X_mall) for algo, model in mall_models.items()}

for algo, labels in mall_labels.items():
    n_noise = int(np.sum(labels == -1))
    sizes_found = sorted(np.bincount(labels[labels >= 0]).tolist(), reverse=True)
    print(f"{algo:<20} {len(set(labels) - {-1})} kelompok, ukuran {sizes_found}, noise {n_noise}")
# --8<-- [end:mall]

# --8<-- [start:crosstab]
# Tabel silang: baris = label K-Means, kolom = label GMM (jumlah pelanggan di tiap sel)
print(pd.crosstab(mall_labels["K-Means"], mall_labels["GMM"], rownames=["K-Means"], colnames=["GMM"]))
# --8<-- [end:crosstab]

# --8<-- [start:plotmall]
fig, axes = plt.subplots(1, 5, figsize=(18, 4), sharex=True, sharey=True)
for ax, (algo, labels) in zip(axes, mall_labels.items()):
    for k in sorted(set(labels)):
        mask = labels == k
        if k == -1:
            ax.scatter(df.loc[mask, features[0]], df.loc[mask, features[1]], s=22, color="#777777", marker="x")
        else:
            ax.scatter(df.loc[mask, features[0]], df.loc[mask, features[1]], s=14, color=palette[k % len(palette)])
    ax.set_title(algo)
    ax.set_xlabel(features[0])
axes[0].set_ylabel(features[1])
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]

# --8<-- [start:guide]
def suggest_algorithms(n_samples, know_k, shape, has_noise, need_probability, density_varies):
    """Panduan sederhana memilih algoritma. shape: 'bulat', 'elips', atau 'bebas'.

    Ini aturan praktis untuk memulai percobaan, bukan hukum. Selalu coba lebih dari satu algoritma.
    """
    suggestions = []
    large = n_samples > 10_000

    if need_probability:
        suggestions.append(("GMM", "satu-satunya yang memberi peluang keanggotaan (soft clustering)"))
    if shape == "bebas" or has_noise:
        if density_varies:
            suggestions.append(("DBSCAN (hati-hati)", "mengikuti bentuk bebas dan mengenal noise, tetapi satu eps sulit untuk kepadatan beragam"))
        else:
            suggestions.append(("DBSCAN", "mengikuti bentuk bebas dan menandai noise"))
    if shape in ("bulat", "elips") and not has_noise:
        if shape == "elips":
            suggestions.append(("GMM (covariance_type='full')", "memodelkan elips berbagai ukuran dan kemiringan"))
        if know_k:
            suggestions.append(("K-Means", "cepat, mudah dijelaskan, cocok untuk kelompok bulat"))
        if not large:
            suggestions.append(("Hierarchical (Ward)", "dendrogram membantu memilih jumlah kelompok"))
    if not know_k and not large and shape != "bebas":
        suggestions.append(("Mean Shift", "jumlah kelompok mengikuti puncak kepadatan (pilih bandwidth dengan hati-hati)"))
    if large:
        suggestions.append(("(catatan)", "data besar: hindari Hierarchical dan Mean Shift tanpa bin_seeding; K-Means dan DBSCAN lebih skalabel"))
    return suggestions
# --8<-- [end:guide]

# --8<-- [start:guidetest]
profiles = {
    "Segmentasi pelanggan, 200 baris, kelompok bulat, K kira-kira 5": dict(
        n_samples=200, know_k=True, shape="bulat", has_noise=False, need_probability=False, density_varies=False),
    "Titik GPS 50.000 baris, bentuk bebas, ada titik tersesat": dict(
        n_samples=50_000, know_k=False, shape="bebas", has_noise=True, need_probability=False, density_varies=False),
    "Data pengukuran, elips tumpang tindih, butuh peluang": dict(
        n_samples=1_000, know_k=True, shape="elips", has_noise=False, need_probability=True, density_varies=False),
    "Data eksplorasi 800 baris, K tidak diketahui, kelompok bulat": dict(
        n_samples=800, know_k=False, shape="bulat", has_noise=False, need_probability=False, density_varies=False),
}
for description, profile in profiles.items():
    print(description)
    for algo, reason in suggest_algorithms(**profile):
        print(f"   - {algo}: {reason}")
# --8<-- [end:guidetest]
