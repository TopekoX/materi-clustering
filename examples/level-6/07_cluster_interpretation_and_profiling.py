"""Level 6, Bab 7: Interpretasi dan profiling kelompok (Mall Customers).

Jalankan dari folder utama proyek:
    python examples/level-6/07_cluster_interpretation_and_profiling.py
"""
# NB: setup=Siapkan alat | data=Data dan clustering | sizes=Ukuran kelompok | profile=Profil dalam satuan asli | zprofile=Profil terstandar | names=Memberi nama berbasis aturan | represent=Pelanggan perwakilan | outside=Variabel di luar clustering dan uji permutasi | save=Menyimpan profil | plotheat=Menggambar profil terstandar | plotmap=Menggambar peta dan umur

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

import _experiment as ex

SEED = 42
# --8<-- [end:setup]

import _savefig

_savefig.install(["07-profil-kelompok", "07-peta-dan-umur"])

# --8<-- [start:data]
df = pd.read_csv("data/mall_customers.csv")
df["Male"] = (df["Gender"] == "Male").astype(int)           # 1 = laki-laki, 0 = perempuan
used = ["Annual Income (k$)", "Spending Score (1-100)"]     # fitur yang DIPAKAI clustering
unused = ["Age", "Male"]                                   # variabel yang TIDAK dipakai clustering

X = ((df[used] - df[used].mean()) / df[used].std()).to_numpy()   # z-score per kolom
model = KMeans(n_clusters=5, n_init=10, random_state=SEED).fit(X)

# Nomor kelompok K-Means bersifat acak. Kita beri huruf A sampai E menurut ukuran (terbesar dulu)
order = np.argsort(-np.bincount(model.labels_), kind="stable")
letter = {int(old): "ABCDE"[new] for new, old in enumerate(order)}
df["Cluster"] = [letter[int(c)] for c in model.labels_]
centers_z = pd.DataFrame(model.cluster_centers_[order], index=list("ABCDE"), columns=used)
# --8<-- [end:data]

# --8<-- [start:sizes]
sizes = df["Cluster"].value_counts().sort_index()
print("Ukuran kelompok:", sizes.to_dict())
print("Persentase:", (sizes / len(df) * 100).round(1).to_dict())
# --8<-- [end:sizes]

# --8<-- [start:profile]
profile = df.groupby("Cluster").agg(
    n=("Cluster", "size"),
    pendapatan_rata=("Annual Income (k$)", "mean"),
    pendapatan_sd=("Annual Income (k$)", "std"),
    skor_rata=("Spending Score (1-100)", "mean"),
    skor_sd=("Spending Score (1-100)", "std"),
    umur_median=("Age", "median"),
    umur_rata=("Age", "mean"),
    porsi_laki=("Male", "mean"),
)
print(profile.round(2).to_string())
print("\nSeluruh pelanggan: pendapatan", round(df[used[0]].mean(), 2), "| skor", round(df[used[1]].mean(), 2),
      "| umur", round(df["Age"].mean(), 2), "| porsi laki-laki", round(df["Male"].mean(), 3))
# --8<-- [end:profile]

# --8<-- [start:zprofile]
# Selisih rata-rata kelompok terhadap rata-rata seluruh data, dinyatakan dalam simpangan baku seluruh data
variables = used + unused
z_profile = (df.groupby("Cluster")[variables].mean() - df[variables].mean()) / df[variables].std()
z_profile.columns = ["pendapatan", "skor belanja", "umur", "laki-laki"]
print(z_profile.round(2).to_string())
# --8<-- [end:zprofile]

# --8<-- [start:names]
def describe(z_income, z_score):
    """Nama berbasis aturan: |z| < 0,5 disebut menengah. Ini label komunikasi, bukan kebenaran tentang orangnya."""
    level = lambda z, hi, lo: hi if z >= 0.5 else lo if z <= -0.5 else "menengah"
    return f"pendapatan {level(z_income, 'tinggi', 'rendah')}, belanja {level(z_score, 'tinggi', 'rendah')}"

names = {c: describe(z_profile.loc[c, "pendapatan"], z_profile.loc[c, "skor belanja"]) for c in z_profile.index}
for c, name in names.items():
    print(f"Kelompok {c} ({sizes[c]} pelanggan): {name}")
# --8<-- [end:names]

# --8<-- [start:represent]
# Pelanggan nyata yang paling dekat dengan pusat kelompok (di ruang terstandar yang dipakai clustering)
rows = []
for c in "ABCDE":
    members = df[df["Cluster"] == c]
    member_x = X[members.index]
    nearest = members.index[np.argmin(((member_x - centers_z.loc[c].to_numpy()) ** 2).sum(axis=1))]
    rows.append({"Kelompok": c, "CustomerID": int(df.loc[nearest, "CustomerID"]), "Gender": df.loc[nearest, "Gender"],
                 "Age": int(df.loc[nearest, "Age"]), "Income": int(df.loc[nearest, used[0]]), "Score": int(df.loc[nearest, used[1]])})
print(pd.DataFrame(rows).to_string(index=False))
# --8<-- [end:represent]

# --8<-- [start:outside]
# Apakah perbedaan umur antar kelompok lebih besar daripada yang wajar bila kelompok dibentuk acak?
rng = np.random.default_rng(SEED)

def spread(values, labels):
    """Selisih rata-rata terbesar dan terkecil antar kelompok."""
    means = pd.Series(values).groupby(labels).mean()
    return means.max() - means.min()

for variable in unused:
    values = df[variable].to_numpy(float)
    observed = spread(values, df["Cluster"].to_numpy())
    shuffled = [spread(values, rng.permutation(df["Cluster"].to_numpy())) for _ in range(2000)]
    p_value = (sum(s >= observed for s in shuffled) + 1) / (len(shuffled) + 1)
    print(f"{variable:5s}: selisih rata-rata antar kelompok = {observed:.3f} | "
          f"rentang acak 95% = {np.percentile(shuffled, 95):.3f} | p (permutasi, 2000 kali) = {p_value:.4f}")
# --8<-- [end:outside]

# --8<-- [start:save]
out = profile.copy()
out.insert(0, "nama", [names[c] for c in out.index])
out = out.join(z_profile.add_prefix("z_"))
out.to_csv(ex.RESULTS_DIR / "07_cluster_profile.csv")
ex.save_json({"seed": SEED, "dataset": "data/mall_customers.csv", "algorithm": "KMeans n_clusters=5 n_init=10",
              "features_used": used, "variables_not_used": unused, "preprocessing": "z-score per kolom",
              "naming_rule": "|z| < 0.5 = menengah", "permutations": 2000}, "07_config")
print("Profil dan konfigurasi tersimpan.")
# --8<-- [end:save]

# --8<-- [start:plotheat]
fig, ax = plt.subplots(figsize=(7.2, 4.2))
image = ax.imshow(z_profile.to_numpy(), cmap="RdBu_r", vmin=-1.5, vmax=1.5, aspect="auto")
ax.set_xticks(range(4), ["pendapatan\n(dipakai)", "skor belanja\n(dipakai)", "umur\n(tidak dipakai)", "laki-laki\n(tidak dipakai)"])
ax.set_yticks(range(5), [f"{c} (n={sizes[c]})" for c in z_profile.index])
for i in range(5):
    for j in range(4):
        value = z_profile.iloc[i, j]
        ax.text(j, i, f"{value:+.2f}", ha="center", va="center", fontsize=9, color="white" if abs(value) > 0.9 else "black")
ax.axvline(1.5, color="black", linewidth=1.5)
ax.set_title("Profil terstandar tiap kelompok (selisih dari rata-rata, dalam simpangan baku)", fontsize=9)
fig.colorbar(image, ax=ax, label="z")
plt.tight_layout()
plt.show()
# --8<-- [end:plotheat]

# --8<-- [start:plotmap]
palette = {"A": "#0072B2", "B": "#E69F00", "C": "#009E73", "D": "#CC79A7", "E": "#D55E00"}
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.3, 1]})
for c in "ABCDE":
    part = df[df["Cluster"] == c]
    axes[0].scatter(part[used[0]], part[used[1]], s=24, color=palette[c], label=f"{c}: {names[c]}")
    axes[0].text(part[used[0]].mean(), part[used[1]].mean(), c, fontsize=13, fontweight="bold", ha="center", va="center",
                 bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.85})
axes[0].set_xlabel("Pendapatan tahunan (k$)")
axes[0].set_ylabel("Skor belanja (1-100)")
axes[0].set_title("Peta kelompok (dua variabel yang dipakai clustering)", fontsize=10)
axes[0].legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)

groups = [df.loc[df["Cluster"] == c, "Age"] for c in "ABCDE"]
box = axes[1].boxplot(groups, tick_labels=list("ABCDE"), patch_artist=True, medianprops={"color": "black"})
for patch, c in zip(box["boxes"], "ABCDE"):
    patch.set_facecolor(palette[c])
axes[1].axhline(df["Age"].mean(), color="gray", linestyle="--", linewidth=1, label="rata-rata semua")
axes[1].set_xlabel("Kelompok")
axes[1].set_ylabel("Umur (tahun), tidak dipakai clustering")
axes[1].set_title("Sebaran umur tiap kelompok", fontsize=10)
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmap]
