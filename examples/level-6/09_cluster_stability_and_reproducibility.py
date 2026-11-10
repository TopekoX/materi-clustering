"""Level 6, Bab 9: Kestabilan dan reproduksibilitas hasil clustering (Mall Customers).

Jalankan dari folder utama proyek:
    python examples/level-6/09_cluster_stability_and_reproducibility.py
"""
# NB: setup=Siapkan alat | data=Data | relabel=ID kelompok tidak boleh dibandingkan langsung | seed=Kestabilan terhadap seed | prep=Kepekaan terhadap praproses | hyper=Kepekaan terhadap hyperparameter | sample=Kestabilan terhadap sampel | kscan=Kestabilan terhadap K | jaccard=Kestabilan tiap kelompok | nostruct=Data tanpa struktur | repro=Reproduksibilitas | save=Menyimpan hasil | plotseed=Gambar seed | plotk=Gambar K dan kelompok | plotsample=Gambar sampel

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import hashlib
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import _experiment as ex

SEED = 42
# --8<-- [end:setup]

import _savefig

_savefig.install(["09-stabilitas-seed", "09-stabilitas-k-dan-kelompok", "09-stabilitas-sampel"])

# --8<-- [start:data]
df = pd.read_csv("data/mall_customers.csv")
used = ["Annual Income (k$)", "Spending Score (1-100)"]
X = ((df[used] - df[used].mean()) / df[used].std()).to_numpy()   # z-score per kolom
print("Data:", X.shape, "| fitur:", used)
# --8<-- [end:data]

# --8<-- [start:relabel]
# Dua eksekusi dengan seed berbeda: apakah hasilnya sama? Bandingkan cara naif dan cara yang benar.
run_a = KMeans(n_clusters=5, n_init=10, random_state=0).fit(X).labels_
run_b = KMeans(n_clusters=5, n_init=10, random_state=1).fit(X).labels_
print("ID kelompok identik (cara naif)   :", f"{(run_a == run_b).mean() * 100:.1f}% titik")
print("ARI (tidak bergantung pada ID)    :", round(adjusted_rand_score(run_a, run_b), 3))
print("Tabel silang ID eksekusi A (baris) vs B (kolom):")
print(pd.crosstab(run_a, run_b).to_string())
# --8<-- [end:relabel]

# --8<-- [start:seed]
def pairwise_ari(label_sets):
    """Rata-rata, minimum, dan maksimum ARI antar semua pasangan hasil."""
    values = [adjusted_rand_score(a, b) for a, b in combinations(label_sets, 2)]
    return float(np.mean(values)), float(np.min(values)), float(np.max(values))

seed_rows = []
seed_inertias = {}
for n_init in (1, 10):
    runs = [KMeans(n_clusters=5, n_init=n_init, random_state=s).fit(X) for s in range(30)]
    inertias = np.array([r.inertia_ for r in runs])
    seed_inertias[n_init] = inertias
    mean_ari, min_ari, max_ari = pairwise_ari([r.labels_ for r in runs])
    seed_rows.append({"n_init": n_init, "inertia_min": inertias.min(), "inertia_max": inertias.max(),
                      "ari_mean": mean_ari, "ari_min": min_ari, "ari_max": max_ari})
    print(f"n_init={n_init:2d}: inertia {inertias.min():.4f} sampai {inertias.max():.4f} | "
          f"ARI antar seed: rata-rata {mean_ari:.3f}, min {min_ari:.3f}, maks {max_ari:.3f}")
# --8<-- [end:seed]

# --8<-- [start:prep]
# Kepekaan terhadap praproses: tiga cara menyiapkan data, K-Means yang sama (K = 5, n_init = 10)
raw = df[used].to_numpy(float)
variants = {"z-score (baseline)": X, "min-max": MinMaxScaler().fit_transform(raw), "tanpa penskalaan": raw}
variant_labels = {name: KMeans(n_clusters=5, n_init=10, random_state=SEED).fit_predict(data) for name, data in variants.items()}
for name, labels in variant_labels.items():
    ari = adjusted_rand_score(variant_labels["z-score (baseline)"], labels)
    print(f"{name:20s}: ukuran kelompok {sorted(np.bincount(labels).tolist(), reverse=True)} | ARI terhadap baseline {ari:.3f}")

# Pembanding: Wine, 13 fitur dengan skala sangat berbeda (K = 3)
wine = load_wine(as_frame=True).data
wine_variants = {"z-score (baseline)": StandardScaler().fit_transform(wine), "min-max": MinMaxScaler().fit_transform(wine),
                 "tanpa penskalaan": wine.to_numpy(float)}
wine_labels = {name: KMeans(n_clusters=3, n_init=10, random_state=SEED).fit_predict(data) for name, data in wine_variants.items()}
for name, labels in wine_labels.items():
    ari = adjusted_rand_score(wine_labels["z-score (baseline)"], labels)
    print(f"Wine, {name:20s}: ukuran kelompok {sorted(np.bincount(labels).tolist(), reverse=True)} | ARI terhadap baseline {ari:.3f}")
# --8<-- [end:prep]

# --8<-- [start:hyper]
# Kepekaan terhadap hyperparameter inisialisasi: k-means++ atau acak, dengan n_init = 1, 30 seed
for init in ("k-means++", "random"):
    runs = [KMeans(n_clusters=5, init=init, n_init=1, random_state=s).fit(X) for s in range(30)]
    inertias = np.array([r.inertia_ for r in runs])
    mean_ari, min_ari, _ = pairwise_ari([r.labels_ for r in runs])
    best = int((inertias < inertias.min() + 1e-6).sum())
    print(f"init={init:9s}: {best} dari 30 seed mencapai inertia terbaik ({inertias.min():.4f}) | ARI antar seed: rata-rata {mean_ari:.3f}, min {min_ari:.3f}")
# --8<-- [end:hyper]

# --8<-- [start:sample]
def subsample_ari(X, k, fraction=0.8, repeats=50, seed=SEED):
    """ARI antara pengelompokan data penuh dan pengelompokan pada sampel acak (tanpa pengembalian).

    Hanya titik yang ada di sampel yang dibandingkan.
    """
    rng = np.random.default_rng(seed)
    full = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X).labels_
    scores = []
    for _ in range(repeats):
        idx = rng.choice(len(X), size=int(fraction * len(X)), replace=False)
        part = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X[idx]).labels_
        scores.append(adjusted_rand_score(full[idx], part))
    return np.array(scores)

fractions = (0.9, 0.8, 0.6, 0.4)
mall_curve = {}
for fraction in fractions:
    s = subsample_ari(X, k=5, fraction=fraction)
    mall_curve[fraction] = (s.mean(), s.min())
    print(f"K=5, sampel {int(fraction * 100)}%, 50 kali: ARI rata-rata {s.mean():.3f} | min {s.min():.3f} | maks {s.max():.3f}")
# --8<-- [end:sample]

# --8<-- [start:kscan]
k_rows = []
for k in range(2, 9):
    s = subsample_ari(X, k=k)
    full = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X)
    k_rows.append({"k": k, "silhouette": silhouette_score(X, full.labels_),
                   "stability_mean": s.mean(), "stability_min": s.min()})
k_table = pd.DataFrame(k_rows)
print(k_table.round(3).to_string(index=False))

# Mengapa K = 2 begitu tidak stabil? Pada tiap sampel 80%, periksa sumbu mana yang dipisahkan dua pusat.
rng_k2 = np.random.default_rng(SEED)
axis_counts = {"pendapatan": 0, "skor belanja": 0}
for _ in range(50):
    idx = rng_k2.choice(len(X), size=int(0.8 * len(X)), replace=False)
    c0, c1 = KMeans(n_clusters=2, n_init=10, random_state=SEED).fit(X[idx]).cluster_centers_
    axis_counts["pendapatan" if abs(c0[0] - c1[0]) > abs(c0[1] - c1[1]) else "skor belanja"] += 1
print("K = 2, 50 sampel 80%: dua kelompok memisah menurut", axis_counts)
# --8<-- [end:kscan]

# --8<-- [start:jaccard]
def clusterwise_jaccard(X, k=5, repeats=100, seed=SEED):
    """Kestabilan tiap kelompok: rata-rata Jaccard terbaik terhadap kelompok asli, pada sampel bootstrap.

    Jaccard dua himpunan = |irisan| / |gabungan|. Nilai di bawah 0,6 menandakan kelompok rapuh
    (Hennig, 2007).
    """
    rng = np.random.default_rng(seed)
    full = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X).labels_
    sizes = np.bincount(full)
    order = np.argsort(-sizes, kind="stable")        # A sampai E menurut ukuran, seperti Bab 7
    totals = np.zeros(k)
    for _ in range(repeats):
        idx = rng.choice(len(X), size=len(X), replace=True)      # bootstrap: dengan pengembalian
        part = KMeans(n_clusters=k, n_init=10, random_state=SEED).fit(X[idx]).labels_
        in_sample = np.unique(idx)
        for rank, c in enumerate(order):
            original = set(np.flatnonzero(full == c)) & set(in_sample)
            best = 0.0
            for d in range(k):
                found = set(idx[part == d])
                union = len(original | found)
                best = max(best, len(original & found) / union if union else 0.0)
            totals[rank] += best
    names = list("ABCDEFGH")[:k]
    return pd.Series(totals / repeats, index=names), pd.Series(sizes[order], index=names)

jaccard, cluster_sizes = clusterwise_jaccard(X)
print(pd.DataFrame({"ukuran": cluster_sizes, "jaccard_rata": jaccard.round(3)}).to_string())
# --8<-- [end:jaccard]

# --8<-- [start:nostruct]
# Data tanpa struktur: 200 titik acak seragam. K-Means tetap membuat 5 kelompok. Apakah mereka stabil?
rng_u = np.random.default_rng(SEED)
X_uniform = rng_u.uniform(size=(200, 2))
X_uniform = (X_uniform - X_uniform.mean(axis=0)) / X_uniform.std(axis=0, ddof=1)
uniform_curve = {}
for fraction in fractions:
    s = subsample_ari(X_uniform, k=5, fraction=fraction)
    uniform_curve[fraction] = (s.mean(), s.min())
uniform_full = KMeans(n_clusters=5, n_init=10, random_state=SEED).fit(X_uniform)
print(f"Data acak seragam, K=5: Silhouette {silhouette_score(X_uniform, uniform_full.labels_):.3f} (Mall Customers: {k_table.loc[k_table.k == 5, 'silhouette'].iloc[0]:.3f})")
for fraction in fractions:
    print(f"  sampel {int(fraction * 100)}%: ARI rata-rata {uniform_curve[fraction][0]:.3f} | min {uniform_curve[fraction][1]:.3f}  "
          f"(Mall: {mall_curve[fraction][0]:.3f} | {mall_curve[fraction][1]:.3f})")
# --8<-- [end:nostruct]

# --8<-- [start:repro]
def run_pipeline(seed):
    """Seluruh alur dari file data sampai label, supaya bisa diulang dari nol."""
    frame = pd.read_csv("data/mall_customers.csv")
    z = ((frame[used] - frame[used].mean()) / frame[used].std()).to_numpy()
    return z, KMeans(n_clusters=5, n_init=1, random_state=seed).fit(z).labels_

def label_hash(labels):
    return hashlib.sha256(np.ascontiguousarray(labels).tobytes()).hexdigest()[:12]

z1, first = run_pipeline(7)
z2, second = run_pipeline(7)
z3, third = run_pipeline(8)
print("Seed sama (7 dan 7): label identik =", np.array_equal(first, second), "| sidik jari label:", label_hash(first), label_hash(second))
print("Seed beda (7 dan 8): label identik =", np.array_equal(first, third), "| ARI =", round(adjusted_rand_score(first, third), 3))
print("Sidik jari data:", ex.dataset_fingerprint(z1), "=", ex.dataset_fingerprint(z2))
print("Lingkungan:", ex.environment_info())
# --8<-- [end:repro]

# --8<-- [start:save]
k_table.assign(dataset="Mall Customers").to_csv(ex.RESULTS_DIR / "09_stability_by_k.csv", index=False)
pd.DataFrame({"ukuran": cluster_sizes, "jaccard_rata": jaccard}).to_csv(ex.RESULTS_DIR / "09_cluster_jaccard.csv")
ex.save_json({"seed": SEED, "dataset": "data/mall_customers.csv", "dataset_fingerprint": ex.dataset_fingerprint(X),
              "features": used, "preprocessing": "z-score per kolom", "algorithm": "KMeans n_clusters=5 n_init=10",
              "seed_runs": 30, "subsample_fractions": list(fractions), "subsample_repeats": 50,
              "bootstrap_repeats": 100, "stability_measure": "ARI (sampel), Jaccard (kelompok)",
              "environment": ex.environment_info()}, "09_config")
print("Hasil dan konfigurasi tersimpan.")
# --8<-- [end:save]

# --8<-- [start:plotseed]
# Rentang histogram diambil dari data (bukan angka tetap) supaya tidak ada seed yang terpotong diam-diam
all_inertias = np.concatenate(list(seed_inertias.values()))
bins = np.linspace(np.floor(all_inertias.min()), np.ceil(all_inertias.max()), 15)
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True)
for ax, n_init in zip(axes, (1, 10)):
    ax.hist(seed_inertias[n_init], bins=bins, color="#0072B2")
    ax.set_title(f"Inertia dari 30 seed, n_init = {n_init}", fontsize=10)
    ax.set_xlabel("Inertia")
    ax.set_ylabel("Jumlah seed")
plt.tight_layout()
plt.show()
# --8<-- [end:plotseed]

# --8<-- [start:plotk]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].plot(k_table["k"], k_table["stability_mean"], marker="o", color="#0072B2", label="Kestabilan (ARI sampel 80%)")
axes[0].plot(k_table["k"], k_table["silhouette"], marker="s", color="#D55E00", label="Silhouette")
axes[0].set_xlabel("K")
axes[0].set_ylabel("Nilai")
axes[0].set_title("Kestabilan dan Silhouette menurut K", fontsize=10)
axes[0].legend(fontsize=8)
axes[1].bar(jaccard.index, jaccard.to_numpy(), color="#009E73")
axes[1].axhline(0.6, color="gray", linestyle="--", linewidth=1, label="ambang 0,6")
axes[1].set_ylim(0, 1.12)
axes[1].set_xlabel("Kelompok")
axes[1].set_ylabel("Jaccard rata-rata")
axes[1].set_title("Kestabilan tiap kelompok (K = 5, bootstrap)", fontsize=10)
axes[1].legend(fontsize=8, loc="upper right", ncol=1)
plt.tight_layout()
plt.show()
# --8<-- [end:plotk]

# --8<-- [start:plotsample]
fig, ax = plt.subplots(figsize=(6.4, 4.4))
percent = [int(f * 100) for f in fractions]
ax.plot(percent, [mall_curve[f][0] for f in fractions], marker="o", color="#0072B2", label="Mall Customers, rata-rata")
ax.plot(percent, [mall_curve[f][1] for f in fractions], marker="o", linestyle="--", color="#0072B2", label="Mall Customers, minimum")
ax.plot(percent, [uniform_curve[f][0] for f in fractions], marker="s", color="#D55E00", label="Data acak seragam, rata-rata")
ax.plot(percent, [uniform_curve[f][1] for f in fractions], marker="s", linestyle="--", color="#D55E00", label="Data acak seragam, minimum")
ax.set_xlabel("Ukuran sampel (% dari data)")
ax.set_ylabel("ARI terhadap hasil data penuh")
ax.set_ylim(0, 1.02)
ax.set_title("Kestabilan terhadap ukuran sampel (K = 5)", fontsize=10)
ax.legend(fontsize=8, loc="lower left")
plt.tight_layout()
plt.show()
# --8<-- [end:plotsample]
