"""Level 6, Bab 5: Seleksi fitur dan analisis dampak fitur (Eksperimen B).

Jalankan dari folder utama proyek:
    python examples/level-6/05_feature_selection_and_impact_analysis.py
"""
# NB: setup=Siapkan alat | wine=Dataset Wine dan fitur berkorelasi | baseline=Baseline dan pengaruh skala | randomsubsets=Subset fitur acak | loo=Melepas satu fitur | noisefeat=Menambah fitur tak relevan | grid=Subset fitur dan K bersama | mall=Mall Customers: dampak fitur tanpa label | save=Menyimpan catatan eksperimen | plotloo=Menggambar dampak tiap fitur | plotnoise=Menggambar fitur tak relevan | plotgrid=Menggambar peta subset dan K

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
from sklearn.datasets import load_wine
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.preprocessing import StandardScaler

import _experiment as ex

SEED = 42
records = []   # semua catatan eksperimen B dikumpulkan di sini


def kmeans_labels(X, k):
    """K-Means dengan konfigurasi terkontrol yang sama untuk semua eksperimen bab ini."""
    return KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(X)
# --8<-- [end:setup]

import _savefig

_savefig.install(["05-dampak-lepas-fitur", "05-fitur-tak-relevan", "05-peta-subset-k"])

# --8<-- [start:wine]
wine = load_wine(as_frame=True)
X_wine_df, y_wine = wine.data, wine.target
features = list(X_wine_df.columns)
print("Wine:", X_wine_df.shape, "| kelas acuan:", np.bincount(y_wine).tolist())

corr = X_wine_df.corr()
pairs = [(a, b, corr.loc[a, b]) for i, a in enumerate(features) for b in features[i + 1:] if abs(corr.loc[a, b]) > 0.7]
print("Pasangan fitur dengan |korelasi| > 0.7:")
for a, b, r in sorted(pairs, key=lambda item: -abs(item[2])):
    print(f"  {a:30s} {b:30s} r = {r:+.3f}")

# Penyaringan sederhana: simpan fitur hanya jika |korelasi| dengan semua fitur yang sudah disimpan <= 0.7
kept = []
for name in features:
    if all(abs(corr.loc[name, other]) <= 0.7 for other in kept):
        kept.append(name)
print("Fitur disimpan setelah penyaringan redundansi:", len(kept), "dari", len(features))
print("Fitur dibuang:", [name for name in features if name not in kept])
# --8<-- [end:wine]

# --8<-- [start:baseline]
X_all = StandardScaler().fit_transform(X_wine_df)
labels_all = kmeans_labels(X_all, 3)
print(f"Baseline (13 fitur, terskala, K = 3): Silhouette = {silhouette_score(X_all, labels_all):.3f}, ARI acuan = {adjusted_rand_score(y_wine, labels_all):.3f}")
records.append(ex.make_record("B-W-00", "wine", X_all, "StandardScaler", "13 fitur", "KMeans", {"n_clusters": 3}, SEED,
                              {"silhouette": silhouette_score(X_all, labels_all), "ari_reference": adjusted_rand_score(y_wine, labels_all)}, 0.0))

# Pengaruh skala: tanpa StandardScaler, satu fitur berskala besar mendominasi jarak
labels_unscaled = kmeans_labels(X_wine_df.to_numpy(float), 3)
variance_share = (X_wine_df.var() / X_wine_df.var().sum()).sort_values(ascending=False)
print(f"Tanpa penskalaan: ARI acuan = {adjusted_rand_score(y_wine, labels_unscaled):.3f}, ARI vs baseline = {adjusted_rand_score(labels_all, labels_unscaled):.3f}")
print(f"Fitur dengan varians terbesar tanpa penskalaan: {variance_share.index[0]} ({variance_share.iloc[0] * 100:.1f}% dari total varians)")
# --8<-- [end:baseline]

# --8<-- [start:randomsubsets]
rng = np.random.default_rng(SEED)
rows = []
for draw in range(30):
    chosen = sorted(rng.choice(len(features), size=4, replace=False).tolist())
    labels = kmeans_labels(X_all[:, chosen], 3)
    rows.append({"ARI acuan": adjusted_rand_score(y_wine, labels), "ARI vs baseline": adjusted_rand_score(labels_all, labels)})
subset_table = pd.DataFrame(rows)
print("30 subset acak berukuran 4 fitur, semuanya K-Means K = 3:")
print(subset_table.describe().loc[["min", "25%", "50%", "75%", "max"]].round(3).to_string())
# --8<-- [end:randomsubsets]

# --8<-- [start:loo]
rows = []
for dropped in features:
    keep = [i for i, name in enumerate(features) if name != dropped]
    labels = kmeans_labels(X_all[:, keep], 3)
    rows.append({"fitur dilepas": dropped, "ARI vs baseline": adjusted_rand_score(labels_all, labels),
                 "ARI acuan": adjusted_rand_score(y_wine, labels)})
loo = pd.DataFrame(rows).sort_values("ARI vs baseline").reset_index(drop=True)
print(loo.round(3).to_string(index=False))
# --8<-- [end:loo]

# --8<-- [start:noisefeat]
rng = np.random.default_rng(SEED)
rows = []
for m in [0, 2, 5, 10, 20, 50]:
    extra = rng.normal(size=(len(X_all), m))            # m fitur acak murni, sudah berskala standar
    X_aug = np.hstack([X_all, extra])
    labels = kmeans_labels(X_aug, 3)
    rows.append({"fitur acak ditambah": m, "ARI acuan": adjusted_rand_score(y_wine, labels),
                 "ARI vs baseline": adjusted_rand_score(labels_all, labels)})
noise_table = pd.DataFrame(rows)
print(noise_table.round(3).to_string(index=False))
# --8<-- [end:noisefeat]

# --8<-- [start:grid]
subsets = {
    "13 fitur": list(range(13)),
    f"Tanpa redundan ({len(kept)} fitur)": [features.index(name) for name in kept],
    "4 fitur pertama": [0, 1, 2, 3],
}
rows = []
for subset_name, columns in subsets.items():
    for k in [2, 3, 4, 5]:
        labels = kmeans_labels(X_all[:, columns], k)
        scores = {"silhouette": silhouette_score(X_all[:, columns], labels), "ari_reference": adjusted_rand_score(y_wine, labels)}
        records.append(ex.make_record(f"B-W-{subset_name[:6]}-K{k}", "wine", X_all[:, columns], "StandardScaler", subset_name,
                                      "KMeans", {"n_clusters": k}, SEED, scores, 0.0))
        rows.append({"subset": subset_name, "K": k, **scores})
grid_table = pd.DataFrame(rows)
print("ARI acuan (dinilai setelahnya):")
print(grid_table.pivot(index="subset", columns="K", values="ari_reference").round(3).to_string())
print("Silhouette di ruang masing-masing (TIDAK sebanding antar baris):")
print(grid_table.pivot(index="subset", columns="K", values="silhouette").round(3).to_string())
# --8<-- [end:grid]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
df["Gender"] = (df["Gender"] == "Male").astype(int)
income, score, age, gender = (df["Annual Income (k$)"].to_numpy(float), df["Spending Score (1-100)"].to_numpy(float),
                              df["Age"].to_numpy(float), df["Gender"].to_numpy(float))
z = lambda v: (v - v.mean()) / v.std()                      # standarisasi satu kolom

X_base = np.column_stack([z(income), z(score)])
base_labels = kmeans_labels(X_base, 5)
variants = {
    "Baseline: pendapatan + skor belanja": X_base,
    "+ umur": np.column_stack([z(income), z(score), z(age)]),
    "+ umur + gender": np.column_stack([z(income), z(score), z(age), z(gender)]),
    "umur + skor belanja": np.column_stack([z(age), z(score)]),
    "pendapatan x3 (digandakan) + skor belanja": np.column_stack([z(income), z(income), z(income), z(score)]),
}
rows = []
for name, X_variant in variants.items():
    labels = kmeans_labels(X_variant, 5)
    rows.append({"Variasi": name, "ARI vs baseline": adjusted_rand_score(base_labels, labels),
                 "Silhouette ruang baseline": silhouette_score(X_base, labels),
                 "ukuran kelompok": sorted(np.bincount(labels).tolist(), reverse=True)})
    records.append(ex.make_record(f"B-M-{len(rows):02d}", "mall_customers", X_variant, "z-score per kolom", name, "KMeans",
                                  {"n_clusters": 5}, SEED, {"silhouette": rows[-1]["Silhouette ruang baseline"], "ari_reference": np.nan}, 0.0))
print(pd.DataFrame(rows).round(3).to_string(index=False))
# --8<-- [end:mall]

# --8<-- [start:save]
results = ex.save_records(records, "05_feature_impact")
ex.save_json({"seed": SEED, "datasets": ["sklearn.datasets.load_wine", "data/mall_customers.csv"], "algorithm": "KMeans n_init=10",
              "note": "ari_reference hanya untuk menilai; pada Mall Customers tidak ada label acuan"}, "05_config")
print("Catatan eksperimen B tersimpan:", len(results))
# --8<-- [end:save]

# --8<-- [start:plotloo]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

order = loo.sort_values("ARI vs baseline", ascending=False)
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.barh(order["fitur dilepas"], order["ARI vs baseline"], color=palette[0])
ax.set_xlabel("ARI antara clustering tanpa fitur itu dan clustering 13 fitur")
ax.set_title("Dampak melepas satu fitur pada struktur kelompok (Wine)")
ax.set_xlim(0, 1.05)
plt.tight_layout()
plt.show()
# --8<-- [end:plotloo]

# --8<-- [start:plotnoise]
fig, ax = plt.subplots(figsize=(6.5, 4.3))
ax.plot(noise_table["fitur acak ditambah"], noise_table["ARI acuan"], marker="o", color=palette[0], label="ARI terhadap label acuan")
ax.plot(noise_table["fitur acak ditambah"], noise_table["ARI vs baseline"], marker="s", color=palette[1], label="ARI terhadap baseline (13 fitur)")
ax.set_xlabel("Jumlah fitur acak yang ditambahkan")
ax.set_ylabel("ARI")
ax.set_title("Fitur tak relevan mengencerkan struktur (Wine)")
ax.set_ylim(0, 1.05)
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotnoise]

# --8<-- [start:plotgrid]
pivot = grid_table.pivot(index="subset", columns="K", values="ari_reference").loc[list(subsets.keys())]
fig, ax = plt.subplots(figsize=(7, 3.6))
image = ax.imshow(pivot.to_numpy(float), cmap="viridis", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(pivot.shape[1]))
ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(pivot.shape[0]))
ax.set_yticklabels(pivot.index, fontsize=8)
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax.text(j, i, f"{pivot.to_numpy(float)[i, j]:.2f}", ha="center", va="center", color="white", fontsize=9)
ax.set_xlabel("Jumlah kelompok K")
ax.set_title("ARI acuan: subset fitur x K (Wine)")
fig.colorbar(image, ax=ax, label="ARI")
plt.tight_layout()
plt.show()
# --8<-- [end:plotgrid]
