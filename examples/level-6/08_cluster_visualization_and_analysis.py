"""Level 6, Bab 8: Visualisasi dan analisis kelompok (data sintetis dan Wine).

Jalankan dari folder utama proyek:
    python examples/level-6/08_cluster_visualization_and_analysis.py
"""
# NB: setup=Siapkan alat | synth=Data sintetis dengan noise | panels=Tiga panel dasar | overlap=Kelompok yang tumpang tindih | wine=Wine dan K-Means | pairs=Pair plot | heat=Peta panas dan koordinat paralel | slice=Batas irisan 2D | save=Menyimpan ringkasan | plotpanels=Gambar tiga panel | plotoverlap=Gambar tumpang tindih | plotpairs=Gambar pair plot | plotheat=Gambar peta panas dan koordinat paralel | plotslice=Gambar irisan 2D

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
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import load_wine, make_blobs
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler

import _experiment as ex

SEED = 42
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]   # aman bagi buta warna
NOISE_COLOR = "#7f7f7f"
# --8<-- [end:setup]

import _savefig

_savefig.install(["08-tiga-panel-dasar", "08-tumpang-tindih", "08-pair-plot-wine", "08-peta-panas-dan-paralel", "08-irisan-2d"])

# --8<-- [start:synth]
# Tiga kelompok dengan kepadatan berbeda, ditambah 30 titik noise yang tersebar acak
centers = [(-4.0, 0.0), (4.0, 0.0), (0.0, 6.0)]
blobs, blob_truth = make_blobs(n_samples=270, centers=centers, cluster_std=[0.7, 1.1, 0.6], random_state=SEED)
rng = np.random.default_rng(SEED)
noise = rng.uniform(low=[-8, -4], high=[8, 10], size=(30, 2))
X_synth = np.vstack([blobs, noise])
print("Data sintetis:", X_synth.shape, "| 270 titik kelompok + 30 titik noise")

kmeans_synth = KMeans(n_clusters=3, n_init=10, random_state=SEED).fit(X_synth)
dbscan_synth = DBSCAN(eps=0.6, min_samples=5).fit(X_synth)
n_db = len(set(dbscan_synth.labels_) - {-1})
print(f"K-Means: 3 kelompok, noise 0 | DBSCAN: {n_db} kelompok, noise {int((dbscan_synth.labels_ == -1).sum())} titik")
is_true_noise = np.arange(len(X_synth)) >= 270          # kita tahu mana noise karena data ini sintetis
print(f"Dari 30 noise sebenarnya, DBSCAN menandai {int((dbscan_synth.labels_[is_true_noise] == -1).sum())} sebagai noise")
print(f"Dari 270 titik kelompok, DBSCAN ikut menandai {int((dbscan_synth.labels_[~is_true_noise] == -1).sum())} sebagai noise")
edge = {f"gerombol {g} (std {sd})": int(((dbscan_synth.labels_ == -1) & (np.r_[blob_truth, np.full(30, -1)] == g)).sum())
        for g, sd in enumerate([0.7, 1.1, 0.6])}
print("Titik kelompok yang ditandai noise, per gerombol asal:", edge)
# --8<-- [end:synth]

# --8<-- [start:overlap]
# Dua kelompok yang sengaja dibuat bertumpuk. Silhouette per titik menunjukkan titik mana yang ambigu.
X_over, _ = make_blobs(n_samples=300, centers=[(-1.2, 0.0), (1.2, 0.0)], cluster_std=1.3, random_state=SEED)
over_labels = KMeans(n_clusters=2, n_init=10, random_state=SEED).fit_predict(X_over)
sample_sil = silhouette_samples(X_over, over_labels)
ambiguous = sample_sil < 0.1
print(f"Silhouette rata-rata (tumpang tindih): {sample_sil.mean():.3f}")
print(f"Titik dengan silhouette < 0,1: {int(ambiguous.sum())} dari {len(X_over)} ({ambiguous.mean() * 100:.1f}%)")
print(f"Titik dengan silhouette < 0: {int((sample_sil < 0).sum())}")
# --8<-- [end:overlap]

# --8<-- [start:wine]
wine = load_wine(as_frame=True)
features = list(wine.data.columns)
X_wine = StandardScaler().fit_transform(wine.data)
wine_model = KMeans(n_clusters=3, n_init=10, random_state=SEED).fit(X_wine)
# Beri huruf A-C menurut ukuran kelompok, seperti Bab 7
order = np.argsort(-np.bincount(wine_model.labels_), kind="stable")
letter = {int(old): "ABC"[new] for new, old in enumerate(order)}
wine_labels = np.array([letter[int(c)] for c in wine_model.labels_])
sizes = pd.Series(wine_labels).value_counts().sort_index()
print("Ukuran kelompok Wine:", sizes.to_dict())
print(f"Silhouette (13 fitur terstandar): {silhouette_score(X_wine, wine_labels):.3f}")
print(f"ARI terhadap label cultivar (hanya untuk evaluasi, bukan masukan): {adjusted_rand_score(wine.target, wine_labels):.3f}")
# --8<-- [end:wine]

# --8<-- [start:pairs]
pair_features = ["alcohol", "flavanoids", "color_intensity", "proline"]
pair_data = pd.DataFrame(X_wine, columns=features)[pair_features]
# Pisahan kelompok per fitur: selisih rata-rata kelompok terbesar dan terkecil (satuan simpangan baku)
spread = pair_data.groupby(wine_labels).mean().agg(lambda col: col.max() - col.min())
print("Pemisahan kelompok per fitur (z):", spread.round(2).to_dict())
# --8<-- [end:pairs]

# --8<-- [start:heat]
z_profile = pd.DataFrame(X_wine, columns=features).groupby(wine_labels).mean()
feature_order = z_profile.apply(lambda col: col.max() - col.min()).sort_values(ascending=False).index
z_profile = z_profile[feature_order]
print("Urutan fitur menurut pemisahan kelompok:", list(feature_order[:5]), "...", list(feature_order[-3:]))
print(z_profile.round(2).T.head(5).to_string())
# --8<-- [end:heat]

# --8<-- [start:slice]
# Apakah gambar 2D jujur? Bandingkan Silhouette di 13 dimensi dengan Silhouette di dua cara menggambar 2D.
pca2 = PCA(n_components=2).fit(X_wine)
X_pca2 = pca2.transform(X_wine)
raw_pair = ["alcohol", "ash"]
X_raw2 = pd.DataFrame(X_wine, columns=features)[raw_pair].to_numpy()
print(f"Varians yang ditangkap PC1 dan PC2: {pca2.explained_variance_ratio_.sum() * 100:.1f}%")
print(f"Silhouette di 13 fitur   : {silhouette_score(X_wine, wine_labels):.3f}")
print(f"Silhouette di bidang PCA : {silhouette_score(X_pca2, wine_labels):.3f}")
print(f"Silhouette di {raw_pair[0]} dan {raw_pair[1]}: {silhouette_score(X_raw2, wine_labels):.3f}")
# --8<-- [end:slice]

# --8<-- [start:save]
z_profile.T.to_csv(ex.RESULTS_DIR / "08_wine_z_profile.csv")
ex.save_json({"seed": SEED, "datasets": ["sintetis make_blobs + noise (270+30)", "sklearn load_wine (178 x 13)"],
              "preprocessing": "StandardScaler (Wine)", "algorithms": ["KMeans k=3", "DBSCAN eps=0.6 min_samples=5"],
              "palette": PALETTE, "noise_color": NOISE_COLOR,
              "silhouette_13d": float(silhouette_score(X_wine, wine_labels)),
              "silhouette_pca2d": float(silhouette_score(X_pca2, wine_labels)),
              "silhouette_alcohol_ash": float(silhouette_score(X_raw2, wine_labels))}, "08_config")
print("Hasil dan konfigurasi tersimpan.")
# --8<-- [end:save]

# --8<-- [start:plotpanels]
fig, axes = plt.subplots(1, 3, figsize=(14, 4.4), sharex=True, sharey=True)
axes[0].scatter(X_synth[:, 0], X_synth[:, 1], s=16, color=NOISE_COLOR)
axes[0].set_title("(a) Data mentah tanpa warna", fontsize=10)

for c in range(3):
    part = X_synth[kmeans_synth.labels_ == c]
    axes[1].scatter(part[:, 0], part[:, 1], s=16, color=PALETTE[c], label=f"kelompok {c}")
axes[1].scatter(*kmeans_synth.cluster_centers_.T, marker="X", s=170, color="black", edgecolor="white", linewidth=1.2, label="centroid")
axes[1].set_title("(b) K-Means (K = 3) dengan centroid", fontsize=10)
axes[1].legend(fontsize=8, loc="upper left")

for c in sorted(set(dbscan_synth.labels_) - {-1}):
    part = X_synth[dbscan_synth.labels_ == c]
    axes[2].scatter(part[:, 0], part[:, 1], s=16, color=PALETTE[c], label=f"kelompok {c}")
isolated = X_synth[dbscan_synth.labels_ == -1]
axes[2].scatter(isolated[:, 0], isolated[:, 1], s=34, marker="x", color=NOISE_COLOR, label=f"noise ({len(isolated)})")
axes[2].set_title("(c) DBSCAN (eps = 0,6) dengan noise", fontsize=10)
axes[2].legend(fontsize=8, loc="upper left")
for ax in axes:
    ax.set_xlabel("fitur 1")
axes[0].set_ylabel("fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotpanels]

# --8<-- [start:plotoverlap]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharex=True, sharey=True)
for c in range(2):
    part = X_over[over_labels == c]
    axes[0].scatter(part[:, 0], part[:, 1], s=18, color=PALETTE[c], alpha=0.75, label=f"kelompok {c}")
axes[0].set_title("(a) Warna menurut kelompok: batas tampak jelas", fontsize=10)
axes[0].legend(fontsize=8)

image = axes[1].scatter(X_over[:, 0], X_over[:, 1], c=sample_sil, cmap="RdYlBu", vmin=-0.2, vmax=0.8, s=18)
axes[1].scatter(X_over[ambiguous, 0], X_over[ambiguous, 1], s=60, facecolors="none", edgecolors="black", linewidth=0.8, label="silhouette < 0,1")
axes[1].set_title("(b) Warna menurut Silhouette tiap titik", fontsize=10)
axes[1].legend(fontsize=8)
fig.colorbar(image, ax=axes[1], label="Silhouette titik")
for ax in axes:
    ax.set_xlabel("fitur 1")
axes[0].set_ylabel("fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotoverlap]

# --8<-- [start:plotpairs]
fig, axes = plt.subplots(4, 4, figsize=(9.5, 9), sharex="col")
for i, row_f in enumerate(pair_features):
    for j, col_f in enumerate(pair_features):
        ax = axes[i, j]
        for k, c in enumerate("ABC"):
            mask = wine_labels == c
            if i == j:
                ax.hist(pair_data.loc[mask, col_f], bins=14, color=PALETTE[k], alpha=0.6)
            else:
                ax.scatter(pair_data.loc[mask, col_f], pair_data.loc[mask, row_f], s=9, color=PALETTE[k], alpha=0.8,
                           label=f"{c} (n={int(mask.sum())})" if (i, j) == (0, 1) else None)
        if j == 0:
            ax.set_ylabel(row_f, fontsize=8)
        if i == 3:
            ax.set_xlabel(col_f, fontsize=8)
        ax.tick_params(labelsize=7)
axes[0, 1].legend(fontsize=7, loc="upper right")
fig.suptitle("Pair plot Wine: empat fitur terstandar, warna menurut kelompok K-Means", fontsize=10)
plt.tight_layout()
plt.show()
# --8<-- [end:plotpairs]

# --8<-- [start:plotheat]
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw={"width_ratios": [1, 1.35]})
image = axes[0].imshow(z_profile.T.to_numpy(), cmap="RdBu_r", vmin=-1.6, vmax=1.6, aspect="auto")
axes[0].set_xticks(range(3), [f"{c}\n(n={sizes[c]})" for c in "ABC"])
axes[0].set_yticks(range(len(feature_order)), feature_order, fontsize=8)
for i in range(z_profile.shape[1]):
    for j in range(3):
        value = z_profile.iloc[j, i]
        axes[0].text(j, i, f"{value:+.1f}", ha="center", va="center", fontsize=7, color="white" if abs(value) > 1.0 else "black")
axes[0].set_title("(a) Peta panas: rata-rata z tiap kelompok", fontsize=10)
fig.colorbar(image, ax=axes[0], label="z")

# Koordinat paralel: satu garis tipis per anggota, satu garis tebal per rata-rata kelompok
scaled = pd.DataFrame(X_wine, columns=features)[feature_order]
for k, c in enumerate("ABC"):
    members = scaled[wine_labels == c]
    for _, row in members.iterrows():
        axes[1].plot(range(len(feature_order)), row.to_numpy(), color=PALETTE[k], alpha=0.07, linewidth=0.8)
    axes[1].plot(range(len(feature_order)), members.mean().to_numpy(), color=PALETTE[k], linewidth=2.6, marker="o", markersize=4,
                 label=f"{c} (n={int(sizes[c])})")
axes[1].set_xticks(range(len(feature_order)), feature_order, rotation=60, ha="right", fontsize=8)
axes[1].set_ylabel("nilai terstandar (z)")
axes[1].set_title("(b) Koordinat paralel: garis tipis = anggota, garis tebal = rata-rata", fontsize=10)
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotheat]

# --8<-- [start:plotslice]
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
views = [
    (axes[0], X_pca2, "PC1", "PC2", f"(a) Bidang PCA (varians {pca2.explained_variance_ratio_.sum() * 100:.1f}%)"),
    (axes[1], X_raw2, raw_pair[0], raw_pair[1], f"(b) Dua fitur mentah: {raw_pair[0]} dan {raw_pair[1]}"),
    (axes[2], X_pca2, "PC1", "PC2", "(c) Bidang PCA yang sama, sumbu y dipadatkan"),
]
for ax, data, xl, yl, title in views:
    for k, c in enumerate("ABC"):
        mask = wine_labels == c
        ax.scatter(data[mask, 0], data[mask, 1], s=16, color=PALETTE[k], label=c)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.set_title(title, fontsize=9)
axes[0].set_aspect("equal")
axes[2].set_aspect(0.25)          # sengaja menipu: sumbu y dipadatkan
axes[0].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotslice]
