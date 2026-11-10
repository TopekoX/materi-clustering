"""Level 7, Bab 6: Implementasi penelitian dengan Python.

Menjalankan protokol yang sudah dikunci di Bab 5 (156 eksekusi), tanpa mengubahnya: memeriksa hash
protokol dan sidik jari data, EDA singkat, praproses, kestabilan (RQ1), kepekaan skala (RQ2),
perbandingan algoritma dan validasi eksternal (RQ3), sensitivitas K, profil kelompok, visualisasi,
dan penyimpanan hasil.

Hal yang belum ditetapkan protokol dicatat sebagai klarifikasi implementasi (06_clarifications.json).

Jalankan dari folder utama proyek (setelah skrip Bab 2, 4, dan 5):
    python examples/level-7/06_research_implementation.py
"""
# NB: setup=Siapkan alat dan periksa protokol terkunci | data=Memuat dataset penelitian | eda=Eksplorasi data singkat | prep=Praproses sesuai protokol | metrics=Fungsi metrik | rq1=RQ1 kestabilan | rq2=RQ2 kepekaan skala | rq3=RQ3 algoritma dan validasi eksternal | ksens=Sensitivitas K | profile=Profil kelompok | plot=Visualisasi | save=Menyimpan hasil dan memeriksa jumlah eksekusi

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:setup]
import hashlib
import json
from itertools import combinations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    normalized_mutual_info_score,
    silhouette_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import _research as rs

RESULTS = rs.RESULTS_DIR
SEED = 42


def protocol_hash(p):
    return hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


protocol = json.loads((RESULTS / "05_protocol.json").read_text(encoding="utf-8"))
locked = (RESULTS / "05_protocol.sha256").read_text(encoding="utf-8").strip()
if protocol_hash(protocol) != locked:
    raise SystemExit("Protokol berubah sejak dikunci. Eksperimen tidak dijalankan.")
print("Protokol terkunci terverifikasi:", locked[:16], "...")

fits = {"RQ1": 0, "RQ2": 0, "RQ3": 0, "K": 0}   # penghitung eksekusi, dicocokkan dengan protokol di akhir
clarifications = []                               # hal yang belum ditetapkan protokol dan diputuskan saat implementasi
# --8<-- [end:setup]

import _savefig

_savefig.install(["06-skala-fitur", "06-kestabilan-dan-skala", "06-empat-algoritma", "06-sensitivitas-k-dan-dbscan"])

# --8<-- [start:data]
frame = pd.read_csv(RESULTS / "04_research_dataset.csv")
y = frame.pop("diagnosis")
X = frame
fingerprint_ok = rs.dataset_fingerprint(X) == protocol["dataset"]["sidik_jari"]
print("Dataset:", X.shape, "| diagnosis:", y.value_counts().to_dict())
print("Sidik jari cocok dengan protokol:", fingerprint_ok)
if not fingerprint_ok:
    raise SystemExit("Sidik jari data berbeda dari protokol.")
# --8<-- [end:data]

# --8<-- [start:eda]
std = X.std().sort_values()
print("Simpangan baku terkecil :", std.index[0], round(float(std.iloc[0]), 5))
print("Simpangan baku terbesar :", std.index[-1], round(float(std.iloc[-1]), 2))
print("Rasio terbesar/terkecil :", f"{float(std.iloc[-1] / std.iloc[0]):.3g}")
print("Proporsi malignant      :", round(float((y == "malignant").mean()), 3))
print(X[["mean radius", "mean area", "mean smoothness"]].describe().loc[["min", "mean", "max"]].round(3).to_string())
# --8<-- [end:eda]

# --8<-- [start:prep]
X_raw = X.to_numpy(dtype=float)
X_base = StandardScaler().fit_transform(X_raw)       # baseline protokol
X_minmax = MinMaxScaler().fit_transform(X_raw)
n = X_base.shape[0]
print("Baseline: rata-rata kolom ~", round(float(X_base.mean()), 6), "| simpangan baku ~", round(float(X_base.std()), 3))
# --8<-- [end:prep]

# --8<-- [start:metrics]
def internal_metrics(Xs, labels):
    """Silhouette, Davies-Bouldin, Calinski-Harabasz di ruang Xs. Titik noise (-1) dikeluarkan."""
    mask = labels != -1
    if len(set(labels[mask])) < 2:
        return {"silhouette": np.nan, "davies_bouldin": np.nan, "calinski_harabasz": np.nan}
    return {
        "silhouette": silhouette_score(Xs[mask], labels[mask]),
        "davies_bouldin": davies_bouldin_score(Xs[mask], labels[mask]),
        "calinski_harabasz": calinski_harabasz_score(Xs[mask], labels[mask]),
    }


def external_metrics(truth, labels):
    """ARI dan NMI terhadap diagnosis. Titik noise diperlakukan sebagai satu kelompok tambahan."""
    return {"ari_vs_diagnosis": adjusted_rand_score(truth, labels), "nmi_vs_diagnosis": normalized_mutual_info_score(truth, labels)}


clarifications.append({"id": "C1", "hal": "metrik internal DBSCAN", "keputusan": "titik noise dikeluarkan saat menghitung Silhouette, Davies-Bouldin, dan Calinski-Harabasz", "alasan": "metrik internal membutuhkan kelompok; noise bukan kelompok"})
clarifications.append({"id": "C2", "hal": "noise pada validasi eksternal", "keputusan": "label noise (-1) diperlakukan sebagai satu kelompok tambahan pada ARI dan NMI", "alasan": "agar semua titik ikut dihitung dan hasil tidak tampak lebih baik karena noise dibuang"})
# --8<-- [end:metrics]

# --8<-- [start:rq1]
km = protocol["algoritma"]["KMeans"]
plan1 = protocol["analisis"]["RQ1"]["ulangan"]

seed_labels = []
for s in range(plan1["seed"]):
    seed_labels.append(KMeans(n_clusters=km["n_clusters"], n_init=km["n_init"], random_state=s).fit_predict(X_base))
    fits["RQ1"] += 1
pair_ari = np.array([adjusted_rand_score(a, b) for a, b in combinations(seed_labels, 2)])

# Pengelompokan acuan (data penuh, seed dasar) = juga baseline RQ3; dihitung di bagian RQ3.
reference = KMeans(n_clusters=km["n_clusters"], n_init=km["n_init"], random_state=SEED).fit_predict(X_base)

rng = np.random.default_rng(SEED)
size = int(round(plan1["fraksi_subsampel"] * n))
sub_ari = []
for _ in range(plan1["subsampel"]):
    idx = np.sort(rng.choice(n, size=size, replace=False))
    X_sub = StandardScaler().fit_transform(X_raw[idx])      # praproses diulang pada subsampel
    labels_sub = KMeans(n_clusters=km["n_clusters"], n_init=km["n_init"], random_state=SEED).fit_predict(X_sub)
    fits["RQ1"] += 1
    sub_ari.append(adjusted_rand_score(reference[idx], labels_sub))
sub_ari = np.array(sub_ari)

rq1 = {
    "stab_seed_mean": float(pair_ari.mean()), "stab_seed_min": float(pair_ari.min()), "pasangan": int(len(pair_ari)),
    "stab_sub_mean": float(sub_ari.mean()), "stab_sub_min": float(sub_ari.min()), "stab_sub_max": float(sub_ari.max()),
    "ukuran_subsampel": size,
}
for key, value in rq1.items():
    print(f"{key:16s}: {round(value, 4) if isinstance(value, float) else value}")
clarifications.append({"id": "C3", "hal": "subsampel pada RQ1", "keputusan": "StandardScaler dihitung ulang pada tiap subsampel; K-Means memakai seed 42; subsampel diambil tanpa pengembalian dengan generator seed 42", "alasan": "seluruh alur praproses diulang agar sesuai praktik nyata; protokol hanya menyebut fraksi 0,8"})
# --8<-- [end:rq1]

# --8<-- [start:rq2]
levels = {
    "StandardScaler (baseline)": X_base,
    "tanpa skala": X_raw,
    "MinMaxScaler": X_minmax,
}
assert list(levels) == protocol["analisis"]["RQ2"]["level"], "level skala harus sama dengan protokol"
threshold = protocol["aturan_keputusan"]["ambang_praktis_sama_ARI"]
rows = []
ari_by_level = {}
for name, Xs in levels.items():
    aris = []
    for s in range(protocol["analisis"]["RQ2"]["ulangan"]["seed"]):
        labels = KMeans(n_clusters=km["n_clusters"], n_init=km["n_init"], random_state=s).fit_predict(Xs)
        fits["RQ2"] += 1
        aris.append(adjusted_rand_score(reference, labels))
    aris = np.array(aris)
    ari_by_level[name] = aris
    rows.append({"perlakuan": name, "ari_mean": aris.mean(), "ari_min": aris.min(), "ari_max": aris.max(), f"proporsi_ari>={threshold}": float((aris >= threshold).mean())})
rq2 = pd.DataFrame(rows).set_index("perlakuan")
print(rq2.round(3).to_string())
# --8<-- [end:rq2]

# --8<-- [start:rq3]
cfg = protocol["algoritma"]
final = {}
final["KMeans"] = reference                                   # baseline, seed dasar (dihitung di RQ1)
fits["RQ3"] += 1
final["Agglomerative"] = AgglomerativeClustering(n_clusters=cfg["Agglomerative"]["n_clusters"], linkage=cfg["Agglomerative"]["linkage"]).fit_predict(X_base)
fits["RQ3"] += 1
final["GMM"] = GaussianMixture(n_components=cfg["GMM"]["n_components"], covariance_type=cfg["GMM"]["covariance_type"], n_init=cfg["GMM"]["n_init"], random_state=SEED).fit_predict(X_base)
fits["RQ3"] += 1

# DBSCAN: grid tanpa label, aturan seleksi dari protokol
db = cfg["DBSCAN"]
grid_rows = []
grid_labels = {}
for k in db["min_samples"]:
    kth = NearestNeighbors(n_neighbors=k).fit(X_base).kneighbors(X_base)[0][:, -1]
    for q in db["eps_kuantil_jarak_tetangga"]:
        eps = float(np.quantile(kth, q))
        labels = DBSCAN(eps=eps, min_samples=k).fit_predict(X_base)
        fits["RQ3"] += 1
        n_clusters = len(set(labels) - {-1})
        noise = float((labels == -1).mean())
        sil = internal_metrics(X_base, labels)["silhouette"]
        valid = bool(n_clusters >= 2 and noise <= 0.10)
        grid_rows.append({"min_samples": k, "kuantil": q, "eps": eps, "kelompok": n_clusters, "noise_persen": 100 * noise, "silhouette": sil, "valid": valid})
        grid_labels[(k, q)] = labels
dbscan_grid = pd.DataFrame(grid_rows)
print(dbscan_grid.round(3).to_string(index=False))

valid_grid = dbscan_grid[dbscan_grid["valid"]]
selected = None
if len(valid_grid):
    best = valid_grid.sort_values("silhouette", ascending=False).iloc[0]
    selected = (int(best["min_samples"]), float(best["kuantil"]))
    final["DBSCAN"] = grid_labels[selected]
    print("DBSCAN terpilih:", selected)
else:
    print("DBSCAN: tidak ada konfigurasi valid (minimal 2 kelompok dan noise paling banyak 10 persen). Aturan tidak dilonggarkan.")

rows = []
for name, labels in final.items():
    rows.append({"algoritma": name, "kelompok": len(set(labels) - {-1}), "noise": int((labels == -1).sum()),
                 **internal_metrics(X_base, labels), **external_metrics(y, labels)})
rq3 = pd.DataFrame(rows).set_index("algoritma")
print(rq3.round(3).to_string())
clarifications.append({"id": "C4", "hal": "baseline acuan", "keputusan": "baseline acuan RQ1 dan RQ2 adalah K-Means StandardScaler dengan seed 42, yang sama dengan K-Means pada RQ3 (dihitung sekali)", "alasan": "protokol menyebut random_state dasar 42 tetapi tidak menyebut dari mana acuan diambil"})
clarifications.append({"id": "C5", "hal": "jarak ke tetangga ke-k pada DBSCAN", "keputusan": "jarak ke tetangga ke-k dihitung termasuk titik itu sendiri sebagai tetangga pertama", "alasan": "konsisten dengan cara scikit-learn menghitung min_samples (titik itu sendiri ikut dihitung)"})
# --8<-- [end:rq3]

# --8<-- [start:ksens]
plan_k = protocol["analisis"]["sensitivitas_K"]
k_rows = []
for k in plan_k["level"]:
    models = {
        "KMeans": KMeans(n_clusters=k, n_init=km["n_init"], random_state=SEED),
        "Agglomerative": AgglomerativeClustering(n_clusters=k, linkage=cfg["Agglomerative"]["linkage"]),
        "GMM": GaussianMixture(n_components=k, covariance_type=cfg["GMM"]["covariance_type"], n_init=cfg["GMM"]["n_init"], random_state=SEED),
    }
    for name, model in models.items():
        labels = model.fit_predict(X_base)
        fits["K"] += 1
        k_rows.append({"k": k, "algoritma": name, "silhouette": silhouette_score(X_base, labels)})
k_table = pd.DataFrame(k_rows).pivot(index="k", columns="algoritma", values="silhouette")
print(k_table.round(3).to_string())
print("K dengan Silhouette tertinggi per algoritma:", {c: int(k_table[c].idxmax()) for c in k_table.columns})
# --8<-- [end:ksens]

# --8<-- [start:profile]
z = pd.DataFrame(X_base, columns=X.columns)
cluster = pd.Series(reference, name="kelompok")
profile = z.groupby(cluster).mean().T
profile.columns = [f"kelompok_{c}" for c in profile.columns]
profile["selisih"] = profile.iloc[:, 1] - profile.iloc[:, 0]
top = profile["selisih"].abs().sort_values(ascending=False).head(6).index
print("Ukuran kelompok:", cluster.value_counts().sort_index().to_dict())
print("Enam fitur dengan selisih z-score terbesar antar kelompok:")
print(profile.loc[top].round(2).to_string())
crosstab = pd.crosstab(cluster, y)
print("Tabulasi silang kelompok x diagnosis (jumlah):")
print(crosstab.to_string())
print("Proporsi malignant per kelompok:", (crosstab["malignant"] / crosstab.sum(axis=1)).round(3).to_dict())
# --8<-- [end:profile]

# --8<-- [start:plot]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7"]
markers = ["o", "s", "^", "D"]

# Gambar 1: skala fitur
fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(std.index, std.values, color="#0072B2")
ax.set_xscale("log")
ax.set_xlabel("simpangan baku (skala logaritmik)")
ax.set_title(f"Simpangan baku 30 fitur: rasio terbesar/terkecil = {float(std.iloc[-1] / std.iloc[0]):.3g}", fontsize=10)
ax.tick_params(axis="y", labelsize=7)
plt.tight_layout()
plt.show()

# Gambar 2: kestabilan (RQ1) dan kepekaan skala (RQ2)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
axes[0].boxplot([pair_ari, sub_ari], tick_labels=["antar-seed\n(190 pasangan)", "subsampel vs data penuh\n(50 ulangan)"], showmeans=True)
axes[0].set_ylabel("ARI")
axes[0].set_title("RQ1: kestabilan K-Means (K = 2)", fontsize=10)
axes[1].boxplot(list(ari_by_level.values()), tick_labels=[name.replace(" (baseline)", "\n(baseline)") for name in ari_by_level], showmeans=True)
axes[1].axhline(threshold, color="#D55E00", linestyle="--", label=f"ambang {threshold}")
axes[1].set_ylabel("ARI terhadap baseline")
axes[1].set_title("RQ2: perlakuan skala (20 seed per level)", fontsize=10)
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.show()

# Gambar 3: empat algoritma pada proyeksi PCA (hanya untuk gambar)
coords = PCA(n_components=2, random_state=SEED).fit_transform(X_base)
names = ["KMeans", "Agglomerative", "GMM", "DBSCAN"]
fig, axes = plt.subplots(1, 4, figsize=(17, 4.4), sharex=True, sharey=True)
for ax, name in zip(axes, names):
    if name not in final:
        ax.text(0.5, 0.5, "tidak ada konfigurasi valid", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(f"{name}", fontsize=10)
        continue
    labels = final[name]
    for c, label in enumerate(sorted(set(labels) - {-1})):
        ax.scatter(coords[labels == label, 0], coords[labels == label, 1], s=12, color=palette[c], marker=markers[c], label=f"kelompok {label}")
    if (labels == -1).any():
        ax.scatter(coords[labels == -1, 0], coords[labels == -1, 1], s=18, color="#555555", marker="x", label="noise")
    ax.set_title(f"{name}\nARI vs diagnosis = {rq3.loc[name, 'ari_vs_diagnosis']:.3f}", fontsize=10)
    ax.set_xlabel("komponen utama 1")
    ax.legend(fontsize=7)
axes[0].set_ylabel("komponen utama 2")
plt.tight_layout()
plt.show()

# Gambar 4: sensitivitas K dan grid DBSCAN
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
for i, name in enumerate(k_table.columns):
    axes[0].plot(k_table.index, k_table[name], marker=markers[i], color=palette[i], label=name)
axes[0].set_xlabel("K")
axes[0].set_xticks(list(k_table.index))
axes[0].set_ylabel("Silhouette (ruang baseline)")
axes[0].set_title("Sensitivitas K", fontsize=10)
axes[0].legend(fontsize=8)
labels_grid = [f"m={int(r.min_samples)}, q={r.kuantil:.2f}" for r in dbscan_grid.itertuples()]
colors = ["#009E73" if v else "#999999" for v in dbscan_grid["valid"]]
axes[1].bar(range(len(dbscan_grid)), dbscan_grid["noise_persen"], color=colors)
axes[1].axhline(10, color="#D55E00", linestyle="--", label="batas noise 10%")
axes[1].set_xticks(range(len(dbscan_grid)))
axes[1].set_xticklabels(labels_grid, rotation=60, ha="right", fontsize=8)
axes[1].set_ylabel("noise (%)")
axes[1].set_title("Grid DBSCAN: hijau = valid, abu-abu = tidak valid menurut protokol", fontsize=10)
axes[1].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:save]
planned = (
    plan1["seed"] + plan1["subsampel"]
    + len(protocol["analisis"]["RQ2"]["level"]) * protocol["analisis"]["RQ2"]["ulangan"]["seed"]
    + sum(not v["disetel"] for v in cfg.values()) + len(db["min_samples"]) * len(db["eps_kuantil_jarak_tetangga"])
    + len(plan_k["level"]) * len(plan_k["algoritma"])
)
executed = sum(fits.values())
print("Eksekusi direncanakan:", planned, "| dijalankan:", executed, "| rincian:", fits)
print("Sesuai protokol:", planned == executed)

pd.DataFrame({"ari_antar_seed": pd.Series(pair_ari)}).to_csv(RESULTS / "06_rq1_seed_pairs.csv", index=False)
pd.DataFrame({"ari_subsampel": sub_ari}).to_csv(RESULTS / "06_rq1_subsample.csv", index=False)
rq2.to_csv(RESULTS / "06_rq2_scaling.csv", encoding="utf-8")
rq3.to_csv(RESULTS / "06_rq3_algorithms.csv", encoding="utf-8")
dbscan_grid.to_csv(RESULTS / "06_dbscan_grid.csv", index=False)
k_table.to_csv(RESULTS / "06_k_sensitivity.csv")
profile.to_csv(RESULTS / "06_cluster_profile.csv", encoding="utf-8")
crosstab.to_csv(RESULTS / "06_crosstab_diagnosis.csv")
(RESULTS / "06_rq1_summary.json").write_text(json.dumps(rq1, indent=2), encoding="utf-8")
(RESULTS / "06_clarifications.json").write_text(json.dumps(clarifications, indent=2, ensure_ascii=False), encoding="utf-8")
manifest = {
    "protokol_hash": locked,
    "sidik_jari_data": protocol["dataset"]["sidik_jari"],
    "eksekusi_direncanakan": planned,
    "eksekusi_dijalankan": executed,
    "rincian": fits,
    "dbscan_terpilih": None if selected is None else {"min_samples": selected[0], "kuantil": selected[1]},
}
(RESULTS / "06_run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("Klarifikasi implementasi dicatat:", [c["id"] for c in clarifications])
print("Berkas hasil disimpan di examples/level-7/results/ (awalan 06_)")
# --8<-- [end:save]
