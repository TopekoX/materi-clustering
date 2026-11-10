"""Level 5, Bab 3: Inertia dan Within-Cluster Sum of Squares (WCSS).

Jalankan dari folder utama proyek:
    python examples/level-5/03_inertia_and_wcss.py
"""
# NB: setup=Siapkan alat | tiny=Enam titik dan dua kelompoknya | manual=WCSS dihitung titik demi titik | sklearn=Mencocokkan dengan inertia_ scikit-learn | wcssfunc=WCSS sebagai fungsi | blobs=Inertia untuk K = 1 sampai 10 | kequalsn=Ketika K sama dengan jumlah titik | plotk=Menggambar Inertia terhadap K | scale=Inertia dipengaruhi skala dan jumlah data | notuniversal=Inertia hanya untuk objektif centroid | moons=Inertia lebih rendah belum tentu lebih baik | plotmoons=Menggambar moons | mall=Inertia pada Mall Customers

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
from sklearn.datasets import make_blobs, make_moons
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(["03-inertia-vs-k", "03-moons-inertia"])

# --8<-- [start:tiny]
X_tiny = np.array(
    [
        [1, 1], [2, 1], [1, 2],   # kelompok 0
        [6, 5], [7, 5], [6, 6],   # kelompok 1
    ],
    dtype=float,
)
labels_tiny = np.array([0, 0, 0, 1, 1, 1])
# --8<-- [end:tiny]

# --8<-- [start:manual]
total = 0.0
for k in (0, 1):
    members = X_tiny[labels_tiny == k]
    centroid = members.mean(axis=0)
    print(f"Kelompok {k}, centroid = {centroid.round(3).tolist()}")
    for point in members:
        sq_dist = ((point - centroid) ** 2).sum()   # jarak kuadrat titik ke centroid
        total += sq_dist
        print(f"  titik {point.tolist()} -> jarak kuadrat = {sq_dist:.3f}")
print(f"WCSS manual = {total:.3f}")
# --8<-- [end:manual]

# --8<-- [start:sklearn]
km_tiny = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X_tiny)
print("Label K-Means      :", km_tiny.labels_.tolist())
print(f"inertia_ scikit-learn = {km_tiny.inertia_:.3f}")
# --8<-- [end:sklearn]

# --8<-- [start:wcssfunc]
def wcss(X, labels):
    """WCSS: jumlah kuadrat jarak setiap titik ke centroid kelompoknya."""
    total = 0.0
    for k in np.unique(labels):
        members = X[labels == k]
        centroid = members.mean(axis=0)
        total += ((members - centroid) ** 2).sum()
    return total


print(f"wcss(X_tiny, labels_tiny) = {wcss(X_tiny, labels_tiny):.3f}")
# --8<-- [end:wcssfunc]

# --8<-- [start:blobs]
X_blobs, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=42)

k_values = list(range(1, 11))
inertias = []
for k in k_values:
    model = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_blobs)
    inertias.append(model.inertia_)

table = pd.DataFrame({"K": k_values, "Inertia": inertias})
table["Penurunan"] = -table["Inertia"].diff()
print(table.round(2).to_string(index=False))
print("Inertia tidak pernah naik saat K naik?", bool(np.all(np.diff(inertias) <= 1e-9)))
# --8<-- [end:blobs]

# --8<-- [start:kequalsn]
# K sama dengan jumlah titik: tiap titik menjadi kelompoknya sendiri
km_all = KMeans(n_clusters=len(X_tiny), n_init=10, random_state=42).fit(X_tiny)
print(f"K = {len(X_tiny)} pada {len(X_tiny)} titik -> Inertia = {km_all.inertia_:.3f}")
# --8<-- [end:kequalsn]

# --8<-- [start:plotk]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.plot(k_values, inertias, marker="o", color=palette[0])
ax.set_xlabel("Jumlah kelompok (K)")
ax.set_ylabel("Inertia (WCSS)")
ax.set_title("Inertia selalu turun saat K naik")
ax.set_xticks(k_values)
plt.tight_layout()
plt.show()
# --8<-- [end:plotk]

# --8<-- [start:scale]
inertia_base = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_blobs).inertia_

# 1) Skala data dikali 10: semua jarak ikut dikali 10, jarak kuadrat dikali 100
inertia_x10 = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_blobs * 10).inertia_

# 2) Jumlah data digandakan (data yang sama dua kali): Inertia ikut naik
X_double = np.vstack([X_blobs, X_blobs])
inertia_double = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X_double).inertia_

print(f"Inertia data asli          : {inertia_base:.2f}")
print(f"Inertia data x 10          : {inertia_x10:.2f}  (rasio {inertia_x10 / inertia_base:.1f})")
print(f"Inertia data digandakan    : {inertia_double:.2f}  (rasio {inertia_double / inertia_base:.2f})")
print(f"Inertia per titik (asli)   : {inertia_base / len(X_blobs):.3f}")
print(f"Inertia per titik (ganda)  : {inertia_double / len(X_double):.3f}")
# --8<-- [end:scale]

# --8<-- [start:notuniversal]
dbscan = DBSCAN(eps=0.7, min_samples=5).fit(X_blobs)
print("KMeans punya inertia_ :", hasattr(KMeans(n_clusters=2).fit(X_blobs), "inertia_"))
print("DBSCAN punya inertia_ :", hasattr(dbscan, "inertia_"))
# --8<-- [end:notuniversal]

# --8<-- [start:moons]
X_moons, y_moons = make_moons(n_samples=300, noise=0.06, random_state=42)
km_moons = KMeans(n_clusters=2, n_init=10, random_state=42).fit(X_moons)

print(f"Inertia K-Means (label salah bentuk) : {km_moons.inertia_:.2f}")
print(f"WCSS label benar (dua bulan utuh)    : {wcss(X_moons, y_moons):.2f}")
# --8<-- [end:moons]

# --8<-- [start:plotmoons]
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
panels = [
    (km_moons.labels_, f"Hasil K-Means\nInertia = {km_moons.inertia_:.1f}"),
    (y_moons, f"Label benar\nWCSS = {wcss(X_moons, y_moons):.1f}"),
]
for ax, (labels, title) in zip(axes, panels):
    for k in range(2):
        ax.scatter(X_moons[labels == k, 0], X_moons[labels == k, 1], s=14, color=palette[k])
    ax.set_title(title)
    ax.set_xlabel("Fitur 1")
axes[0].set_ylabel("Fitur 2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotmoons]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
X_mall = StandardScaler().fit_transform(df[features])

mall_inertia = [KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_mall).inertia_ for k in range(1, 11)]
mall_table = pd.DataFrame({"K": range(1, 11), "Inertia": mall_inertia})
mall_table["Penurunan"] = -mall_table["Inertia"].diff()
print(mall_table.round(2).to_string(index=False))
# --8<-- [end:mall]
