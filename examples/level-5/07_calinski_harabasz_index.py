"""Level 5, Bab 7: Calinski-Harabasz Index (CHI).

Jalankan dari folder utama proyek:
    python examples/level-5/07_calinski_harabasz_index.py
"""
# NB: setup=Siapkan alat | tiny=Sembilan titik dan tiga kelompok | manual=CH dihitung manual | check=Mencocokkan dengan scikit-learn | blobs=CH untuk beberapa nilai K | invariance=Skala dan jumlah data | uniform=Data tanpa kelompok alami | moons=Keterbatasan pada moons | together=Tiga metrik internal bersama-sama | plotk=Menggambar CH terhadap K | plottogether=Menggambar tiga metrik pada Mall Customers

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
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["07-ch-vs-k", "07-tiga-metrik-mall"])

# --8<-- [start:tiny]
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2],   # kelompok 0
        [6, 5], [7, 5], [6, 6],   # kelompok 1
        [1, 8], [2, 8], [1, 9],   # kelompok 2
    ],
    dtype=float,
)
labels_tiny = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])
# --8<-- [end:tiny]

# --8<-- [start:manual]
def ch_manual(X, labels, verbose=False):
    """Calinski-Harabasz Index dihitung langkah demi langkah."""
    n = len(X)
    ks = np.unique(labels)
    k = len(ks)
    overall_centroid = X.mean(axis=0)

    B = 0.0   # dispersi ANTAR kelompok
    W = 0.0   # dispersi DALAM kelompok
    for c in ks:
        members = X[labels == c]
        centroid = members.mean(axis=0)
        B += len(members) * ((centroid - overall_centroid) ** 2).sum()
        W += ((members - centroid) ** 2).sum()

    ch = (B / (k - 1)) / (W / (n - k))
    if verbose:
        total = ((X - overall_centroid) ** 2).sum()
        print("Centroid keseluruhan :", overall_centroid.round(3).tolist())
        print(f"B (antar kelompok)   : {B:.3f}")
        print(f"W (dalam kelompok)   : {W:.3f}")
        print(f"B + W                : {B + W:.3f}   (jumlah kuadrat total = {total:.3f})")
        print(f"n = {n}, k = {k}  ->  (B / {k - 1}) / (W / {n - k})")
    return ch


ch_tiny = ch_manual(X_tiny, labels_tiny, verbose=True)
print(f"CH manual = {ch_tiny:.4f}")
# --8<-- [end:manual]

# --8<-- [start:check]
print(f"calinski_harabasz_score = {calinski_harabasz_score(X_tiny, labels_tiny):.4f}")
# --8<-- [end:check]

# --8<-- [start:blobs]
X_blobs, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=42)
rows = []
for k in range(2, 9):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_blobs)
    rows.append({"K": k, "Calinski-Harabasz": calinski_harabasz_score(X_blobs, labels)})
blob_table = pd.DataFrame(rows).set_index("K")
print(blob_table.round(1).to_string())
print("K dengan CH tertinggi:", int(blob_table["Calinski-Harabasz"].idxmax()))
# --8<-- [end:blobs]

# --8<-- [start:invariance]
labels4 = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X_blobs)
print(f"CH data asli          : {calinski_harabasz_score(X_blobs, labels4):.2f}")
print(f"CH data x 10          : {calinski_harabasz_score(X_blobs * 10, labels4):.2f}")

# Data digandakan: bentuk kelompok sama, jumlah titik dua kali lipat
X_double = np.vstack([X_blobs, X_blobs])
labels_double = np.concatenate([labels4, labels4])
print(f"CH data digandakan    : {calinski_harabasz_score(X_double, labels_double):.2f}   (400 -> 800 titik)")
# --8<-- [end:invariance]

# --8<-- [start:uniform]
X_uniform = np.random.default_rng(42).uniform(-10, 10, size=(400, 2))
uniform_ch = {}
for k in range(2, 11):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_uniform)
    uniform_ch[k] = calinski_harabasz_score(X_uniform, labels)
print({k: round(v, 1) for k, v in uniform_ch.items()})
print("K dengan CH tertinggi pada data acak:", max(uniform_ch, key=uniform_ch.get))
# --8<-- [end:uniform]

# --8<-- [start:moons]
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
km_moons = KMeans(n_clusters=2, n_init=10, random_state=42).fit_predict(X_moons)
print(f"CH K-Means (memotong bulan) : {calinski_harabasz_score(X_moons, km_moons):.1f}")
print(f"CH label benar              : {calinski_harabasz_score(X_moons, y_moons):.1f}")
# --8<-- [end:moons]

# --8<-- [start:together]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

rows = []
for k in range(2, 11):
    labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X_mall)
    rows.append(
        {
            "K": k,
            "Silhouette": silhouette_score(X_mall, labels),
            "Davies-Bouldin": davies_bouldin_score(X_mall, labels),
            "Calinski-Harabasz": calinski_harabasz_score(X_mall, labels),
        }
    )
mall_table = pd.DataFrame(rows).set_index("K")
print(mall_table.round(3).to_string())
print("K terbaik menurut Silhouette (tertinggi)        :", int(mall_table["Silhouette"].idxmax()))
print("K terbaik menurut Davies-Bouldin (terendah)     :", int(mall_table["Davies-Bouldin"].idxmin()))
print("K terbaik menurut Calinski-Harabasz (tertinggi) :", int(mall_table["Calinski-Harabasz"].idxmax()))
# --8<-- [end:together]

# --8<-- [start:plotk]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
axes[0].plot(blob_table.index, blob_table["Calinski-Harabasz"], marker="o", color=palette[0])
axes[0].set_title("Empat gerombol jelas")
axes[1].plot(list(uniform_ch.keys()), list(uniform_ch.values()), marker="o", color=palette[1])
axes[1].set_title("Tanpa kelompok alami")
axes[2].plot(mall_table.index, mall_table["Calinski-Harabasz"], marker="o", color=palette[2])
axes[2].set_title("Mall Customers")
for ax in axes:
    ax.set_xlabel("Jumlah kelompok (K)")
    ax.set_ylabel("Calinski-Harabasz Index (lebih tinggi lebih baik)")
plt.tight_layout()
plt.show()
# --8<-- [end:plotk]

# --8<-- [start:plottogether]
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, column, color in zip(axes, mall_table.columns, palette):
    ax.plot(mall_table.index, mall_table[column], marker="o", color=color)
    best = mall_table[column].idxmin() if column == "Davies-Bouldin" else mall_table[column].idxmax()
    ax.axvline(best, color="gray", linestyle="--")
    ax.set_title(f"{column}\n(terbaik: K = {best})")
    ax.set_xlabel("Jumlah kelompok (K)")
plt.tight_layout()
plt.show()
# --8<-- [end:plottogether]
