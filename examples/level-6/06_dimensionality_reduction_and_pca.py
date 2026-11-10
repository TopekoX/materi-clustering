"""Level 6, Bab 6: Reduksi dimensi dan PCA untuk clustering.

Jalankan dari folder utama proyek:
    python examples/level-6/06_dimensionality_reduction_and_pca.py
"""
# NB: setup=Siapkan alat | manual=PCA dari matriks kovarians pada data kecil | sklearn=Mencocokkan dengan PCA scikit-learn | wine=PCA pada Wine | scaling=PCA tanpa dan dengan penskalaan | loadings=Fitur yang membentuk komponen | viz=Proyeksi kelompok ke ruang 2D | inpca=Clustering di ruang PCA | digits=Digits: 64 dimensi | projection=Batas visualisasi 2D | plotscree=Menggambar scree plot | plotwine=Menggambar proyeksi Wine | plotdigits=Menggambar Digits

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
from sklearn.datasets import load_digits, load_wine
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.preprocessing import StandardScaler

SEED = 42


def kmeans_labels(X, k):
    return KMeans(n_clusters=k, n_init=10, random_state=SEED).fit_predict(X)
# --8<-- [end:setup]

import _savefig

_savefig.install(["06-scree-wine", "06-proyeksi-wine", "06-digits-pca"])

# --8<-- [start:manual]
# Enam titik dua dimensi yang menyebar miring
X_small = np.array([[2.0, 1.0], [3.0, 2.0], [4.0, 2.5], [5.0, 4.0], [6.0, 4.5], [7.0, 6.0]])
centered = X_small - X_small.mean(axis=0)                  # 1) pusatkan data (kurangi rata-rata)
cov = centered.T @ centered / (len(X_small) - 1)           # 2) matriks kovarians (pembagi n - 1)
eigenvalues, eigenvectors = np.linalg.eigh(cov)            # 3) nilai eigen dan vektor eigen (urut naik)
order = np.argsort(eigenvalues)[::-1]                      # urutkan dari yang terbesar
eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
print("Matriks kovarians:\n", cov.round(4))
print("Nilai eigen          :", eigenvalues.round(4))
print("Rasio varians manual :", (eigenvalues / eigenvalues.sum()).round(4))
print("Vektor eigen pertama :", eigenvectors[:, 0].round(4))
# --8<-- [end:manual]

# --8<-- [start:sklearn]
pca_small = PCA(n_components=2).fit(X_small)
print("explained_variance_        :", pca_small.explained_variance_.round(4))
print("explained_variance_ratio_  :", pca_small.explained_variance_ratio_.round(4))
print("components_[0] (komponen 1):", pca_small.components_[0].round(4), "(tanda boleh terbalik)")
projected = pca_small.transform(X_small)
print("Varians skor komponen 1    :", projected[:, 0].var(ddof=1).round(4))
# --8<-- [end:sklearn]

# --8<-- [start:wine]
wine = load_wine(as_frame=True)
X_wine_df, y_wine = wine.data, wine.target
X_wine = StandardScaler().fit_transform(X_wine_df)

pca_full = PCA().fit(X_wine)
ratio = pca_full.explained_variance_ratio_
cumulative = np.cumsum(ratio)
print("Rasio varians 6 komponen pertama:", ratio[:6].round(3))
print("Kumulatif 6 komponen pertama    :", cumulative[:6].round(3))
for target in (0.80, 0.90, 0.95):
    print(f"Komponen minimum untuk >= {int(target * 100)}% varians: {int(np.argmax(cumulative >= target) + 1)} dari {X_wine.shape[1]}")
# --8<-- [end:wine]

# --8<-- [start:scaling]
pca_raw = PCA(n_components=2).fit(X_wine_df.to_numpy(float))
pca_scaled = PCA(n_components=2).fit(X_wine)
print("Tanpa penskalaan: rasio varians komponen 1 dan 2 =", pca_raw.explained_variance_ratio_.round(4))
print("Dengan penskalaan: rasio varians komponen 1 dan 2 =", pca_scaled.explained_variance_ratio_.round(4))
# --8<-- [end:scaling]

# --8<-- [start:loadings]
loadings = pd.DataFrame(pca_scaled.components_.T, index=X_wine_df.columns, columns=["PC1", "PC2"])
print("Lima fitur dengan |bobot| terbesar pada PC1:")
print(loadings["PC1"].reindex(loadings["PC1"].abs().sort_values(ascending=False).index).head(5).round(3).to_string())
print("Lima fitur dengan |bobot| terbesar pada PC2:")
print(loadings["PC2"].reindex(loadings["PC2"].abs().sort_values(ascending=False).index).head(5).round(3).to_string())
# --8<-- [end:loadings]

# --8<-- [start:viz]
# Cara A: cluster di ruang ASLI (13 dimensi), lalu PROYEKSIKAN hasilnya ke 2D hanya untuk digambar
labels_13d = kmeans_labels(X_wine, 3)
X_2d = pca_scaled.transform(X_wine)
print(f"Cluster di 13 dimensi: ARI acuan = {adjusted_rand_score(y_wine, labels_13d):.3f}, Silhouette (13D) = {silhouette_score(X_wine, labels_13d):.3f}")
print(f"Label yang sama, dihitung di ruang 2D proyeksi: Silhouette (2D) = {silhouette_score(X_2d, labels_13d):.3f}")
print(f"Varians yang dipertahankan oleh 2 komponen: {pca_scaled.explained_variance_ratio_.sum() * 100:.1f}%")
# --8<-- [end:viz]

# --8<-- [start:inpca]
# Cara B: cluster DI DALAM ruang PCA (fit_transform lalu K-Means), dengan jumlah komponen berbeda
rows = []
for n_components in [2, 3, 5, 8, 13]:
    X_pca = PCA(n_components=n_components).fit_transform(X_wine)
    labels = kmeans_labels(X_pca, 3)
    rows.append({"n_components": n_components, "varians dipertahankan (%)": PCA(n_components=n_components).fit(X_wine).explained_variance_ratio_.sum() * 100,
                 "ARI acuan": adjusted_rand_score(y_wine, labels), "ARI vs cluster 13D": adjusted_rand_score(labels_13d, labels)})
print(pd.DataFrame(rows).round(3).to_string(index=False))
# --8<-- [end:inpca]

# --8<-- [start:digits]
digits = load_digits()
X_digits, y_digits = digits.data / 16.0, digits.target       # piksel 0-16 diubah ke 0-1
print("Digits:", X_digits.shape, "| jumlah kelas:", len(set(y_digits)))

pca_digits = PCA().fit(X_digits)
cum_digits = np.cumsum(pca_digits.explained_variance_ratio_)
print("Varians dipertahankan: 2 komponen =", round(cum_digits[1] * 100, 1), "%, 10 =", round(cum_digits[9] * 100, 1),
      "%, 30 =", round(cum_digits[29] * 100, 1), "%")
print("Komponen minimum untuk >= 90% varians:", int(np.argmax(cum_digits >= 0.90) + 1), "dari 64")

labels_64d = kmeans_labels(X_digits, 10)
rows = [{"ruang": "64 dimensi asli", "ARI acuan": adjusted_rand_score(y_digits, labels_64d),
         "NMI acuan": normalized_mutual_info_score(y_digits, labels_64d), "ARI vs cluster 64D": 1.0}]
for n_components in [2, 10, 20, 30]:
    labels = kmeans_labels(PCA(n_components=n_components).fit_transform(X_digits), 10)
    rows.append({"ruang": f"PCA {n_components} komponen", "ARI acuan": adjusted_rand_score(y_digits, labels),
                 "NMI acuan": normalized_mutual_info_score(y_digits, labels), "ARI vs cluster 64D": adjusted_rand_score(labels_64d, labels)})
print(pd.DataFrame(rows).round(3).to_string(index=False))
# --8<-- [end:digits]

# --8<-- [start:projection]
X_digits_2d = PCA(n_components=2).fit_transform(X_digits)
print(f"Silhouette label digit asli di 64D : {silhouette_score(X_digits, y_digits):.3f}")
print(f"Silhouette label digit asli di 2D  : {silhouette_score(X_digits_2d, y_digits):.3f}")
print(f"Silhouette cluster 64D di 64D      : {silhouette_score(X_digits, labels_64d):.3f}")
print(f"Silhouette cluster 64D di 2D       : {silhouette_score(X_digits_2d, labels_64d):.3f}")
# --8<-- [end:projection]

# --8<-- [start:plotscree]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9", "#F0E442", "#999999", "#332288", "#882255"]

fig, ax = plt.subplots(figsize=(7, 4.3))
components = np.arange(1, len(ratio) + 1)
ax.bar(components, ratio * 100, color=palette[0], label="Per komponen")
ax.plot(components, cumulative * 100, marker="o", color=palette[1], label="Kumulatif")
ax.axhline(90, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Komponen utama")
ax.set_ylabel("Varians yang dijelaskan (%)")
ax.set_title("Scree plot Wine (data terskala)")
ax.set_xticks(components)
ax.legend(fontsize=8, loc="center right")
plt.tight_layout()
plt.show()
# --8<-- [end:plotscree]

# --8<-- [start:plotwine]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharex=True, sharey=True)
for ax, labels, title in zip(axes, [labels_13d, y_wine],
                             ["Kelompok K-Means (dihitung di 13D, diproyeksikan ke 2D)", "Kelas acuan (hanya untuk membandingkan)"]):
    for c in range(3):
        ax.scatter(X_2d[labels == c, 0], X_2d[labels == c, 1], s=22, color=palette[c], label=f"Kelompok {c}" if labels is labels_13d else f"Kelas {c}")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel(f"PC1 ({pca_scaled.explained_variance_ratio_[0] * 100:.1f}% varians)")
    ax.legend(fontsize=8)
axes[0].set_ylabel(f"PC2 ({pca_scaled.explained_variance_ratio_[1] * 100:.1f}% varians)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotwine]

# --8<-- [start:plotdigits]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
for digit in range(10):
    axes[0].scatter(X_digits_2d[y_digits == digit, 0], X_digits_2d[y_digits == digit, 1], s=6, color=palette[digit], label=str(digit))
axes[0].set_xlabel("PC1")
axes[0].set_ylabel("PC2")
axes[0].set_title(f"Digits di 2D PCA ({cum_digits[1] * 100:.1f}% varians dipertahankan)")
axes[0].legend(fontsize=7, ncol=2, markerscale=2)

n_list = [2, 5, 10, 15, 20, 30, 40, 64]
ari_list = [adjusted_rand_score(y_digits, kmeans_labels(PCA(n_components=n).fit_transform(X_digits), 10)) for n in n_list]
axes[1].plot(n_list, ari_list, marker="o", color=palette[0], label="Cluster di ruang PCA")
axes[1].axhline(adjusted_rand_score(y_digits, labels_64d), color=palette[1], linestyle="--", label="Cluster di 64D asli")
axes[1].set_xlabel("Jumlah komponen PCA")
axes[1].set_ylabel("ARI terhadap label digit")
axes[1].set_title("Kualitas clustering vs jumlah komponen")
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotdigits]
