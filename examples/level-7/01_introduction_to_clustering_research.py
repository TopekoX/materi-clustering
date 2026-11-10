"""Level 7, Bab 1: Pengantar penelitian clustering.

Menunjukkan bahwa pada penelitian, pertanyaan riset menentukan fitur, algoritma, dan evaluasi.
Data yang sama dengan tiga pertanyaan berbeda menghasilkan tiga pengelompokan berbeda.

Jalankan dari folder utama proyek:
    python examples/level-7/01_introduction_to_clustering_research.py
"""
# NB: setup=Siapkan alat | data=Mengenal data penelitian | questions=Tiga pertanyaan riset | cluster=Menjalankan satu protokol untuk tiap pertanyaan | evaluate=Evaluasi internal dan validasi eksternal | compare=Membandingkan pengelompokan antar pertanyaan | plot=Menggambar | record=Catatan penelitian

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
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.preprocessing import StandardScaler

import _research as rs
# --8<-- [end:setup]

import _savefig

_savefig.install(["01-tiga-pertanyaan-tiga-pengelompokan"])

SEED = 42

# --8<-- [start:data]
X_all, diagnosis = rs.load_wdbc()

print("Jumlah baris (sampel) :", X_all.shape[0])
print("Jumlah fitur          :", X_all.shape[1])
print("Nilai hilang          :", int(X_all.isna().sum().sum()))
print("Diagnosis (hanya untuk validasi):", diagnosis.value_counts().to_dict())
print("Sidik jari data       :", rs.dataset_fingerprint(X_all))
print("Contoh nama fitur     :", list(X_all.columns[:5]))
# --8<-- [end:data]

# --8<-- [start:questions]
# Setiap pertanyaan riset menentukan fitur yang relevan.
questions = {
    "Q1 ukuran inti sel": ["mean radius", "mean perimeter", "mean area"],
    "Q2 tekstur dan kehalusan": ["mean texture", "mean smoothness", "mean symmetry", "mean fractal dimension"],
    "Q3 seluruh profil morfologi": list(X_all.columns),
}
for name, columns in questions.items():
    print(f"{name:30s}: {len(columns):2d} fitur")
# --8<-- [end:questions]

# --8<-- [start:cluster]
# Protokol yang sama untuk semua pertanyaan: StandardScaler, K-Means, K = 2, n_init = 10, seed 42.
labels = {}
spaces = {}
for name, columns in questions.items():
    X_scaled = StandardScaler().fit_transform(X_all[columns])
    spaces[name] = X_scaled
    labels[name] = KMeans(n_clusters=2, n_init=10, random_state=SEED).fit_predict(X_scaled)
    sizes = np.bincount(labels[name]).tolist()
    print(f"{name:30s} ukuran kelompok: {sizes}")
# --8<-- [end:cluster]

# --8<-- [start:evaluate]
rows = []
for name in questions:
    rows.append(
        {
            "Pertanyaan": name,
            "Silhouette (internal)": silhouette_score(spaces[name], labels[name]),
            "ARI vs diagnosis": adjusted_rand_score(diagnosis, labels[name]),
            "NMI vs diagnosis": normalized_mutual_info_score(diagnosis, labels[name]),
        }
    )
evaluation = pd.DataFrame(rows).set_index("Pertanyaan")
print(evaluation.round(3).to_string())
# --8<-- [end:evaluate]

# --8<-- [start:compare]
names = list(questions)
agreement = pd.DataFrame(
    [[adjusted_rand_score(labels[a], labels[b]) for b in names] for a in names], index=names, columns=names
)
print(agreement.round(3).to_string())
# --8<-- [end:compare]

# --8<-- [start:plot]
palette = ["#0072B2", "#E69F00"]          # kelompok (nomornya sembarang)
diag_palette = ["#009E73", "#CC79A7"]     # diagnosis: warna lain agar tidak tertukar dengan kelompok
markers = ["o", "s"]
pair = {
    "Q1 ukuran inti sel": ("mean radius", "mean area"),
    "Q2 tekstur dan kehalusan": ("mean texture", "mean smoothness"),
}

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for col, name in enumerate(names):
    if name in pair:
        x_name, y_name = pair[name]
        xy = X_all[[x_name, y_name]].to_numpy()
        xlabel, ylabel = x_name, y_name
    else:
        xy = PCA(n_components=2, random_state=SEED).fit_transform(spaces[name])
        xlabel, ylabel = "komponen utama 1 (PCA)", "komponen utama 2 (PCA)"
    for c in range(2):
        mask = labels[name] == c
        axes[0, col].scatter(xy[mask, 0], xy[mask, 1], s=12, color=palette[c], marker=markers[c], label=f"kelompok {c}")
    for c, diag in enumerate(["benign", "malignant"]):
        mask = (diagnosis == diag).to_numpy()
        axes[1, col].scatter(xy[mask, 0], xy[mask, 1], s=12, color=diag_palette[c], marker=markers[c], label=diag)
    axes[0, col].set_title(f"{name}\nwarna = kelompok K-Means", fontsize=10)
    axes[1, col].set_title("tata letak sama, warna = diagnosis (hanya validasi)", fontsize=10)
    axes[1, col].set_xlabel(xlabel)
    axes[0, col].set_ylabel(ylabel)
    axes[1, col].set_ylabel(ylabel)
axes[0, 0].legend(fontsize=8)
axes[1, 0].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:record]
record = {
    "dataset": "Breast Cancer Wisconsin (Diagnostic), UCI, CC BY 4.0",
    "sidik_jari_data": rs.dataset_fingerprint(X_all),
    "algoritma": "KMeans(n_clusters=2, n_init=10)",
    "praproses": "StandardScaler",
    "seed": SEED,
    "pertanyaan": list(questions),
    "label_diagnosis": "hanya untuk validasi eksternal, tidak dipakai melatih",
}
for key, value in record.items():
    print(f"{key:16s}: {value}")
# --8<-- [end:record]
