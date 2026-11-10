"""Level 7, Bab 5: Metodologi penelitian dan protokol eksperimen.

Menulis protokol eksperimen SEBELUM eksperimen dijalankan: variabel, algoritma, praproses, metrik,
aturan keputusan, dan prosedur pembanding yang adil. Protokol divalidasi, diuji dengan smoke test
(tanpa metrik berbasis label), lalu dikunci dengan hash SHA-256.

Metrik hasil eksperimen TIDAK dihitung di bab ini. Pelaksanaannya ada di Bab 6.

Jalankan dari folder utama proyek (setelah skrip Bab 2 dan Bab 4):
    python examples/level-7/05_research_methodology_and_protocol.py
"""
# NB: setup=Siapkan alat dan baca bab sebelumnya | protocol=Menulis protokol | validate=Memvalidasi protokol | grid=Menghitung jumlah eksekusi | smoke=Smoke test tanpa metrik berbasis label | lock=Mengunci protokol dengan hash | amend=Mencatat perubahan protokol

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:setup]
import copy
import hashlib
import json
import platform
import time
from importlib import metadata

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

import _research as rs

RESULTS = rs.RESULTS_DIR
problem = json.loads((RESULTS / "02_research_problem.json").read_text(encoding="utf-8"))
card = json.loads((RESULTS / "04_dataset_card.json").read_text(encoding="utf-8"))
X_all, diagnosis = rs.load_wdbc()
print("Pertanyaan:", list(problem["pertanyaan"]), "| sidik jari data final:", card["sidik_jari_data_final"])
# --8<-- [end:setup]

# --8<-- [start:protocol]
protocol = {
    "versi": "1.0",
    "judul_kerja": problem["judul_kerja"],
    "dataset": {
        "nama": card["nama"],
        "sidik_jari": card["sidik_jari_data_final"],
        "jumlah_sampel": card["jumlah_sampel_final"],
        "jumlah_fitur": 30,
        "label": "diagnosis: hanya untuk validasi eksternal, tidak dipakai melatih atau menyetel",
    },
    "pertanyaan": problem["pertanyaan"],
    "analisis": {
        "RQ1": {
            "faktor": "seed dan sampel data",
            "algoritma": ["KMeans"],
            "ulangan": {"seed": 20, "subsampel": 50, "fraksi_subsampel": 0.8},
            "metrik": ["ARI antar-seed", "ARI pengelompokan subsampel vs data penuh"],
        },
        "RQ2": {
            "faktor": "perlakuan skala fitur",
            "level": ["StandardScaler (baseline)", "tanpa skala", "MinMaxScaler"],
            "algoritma": ["KMeans"],
            "ulangan": {"seed": 20},
            "metrik": ["ARI vs baseline"],
        },
        "RQ3": {
            "faktor": "algoritma",
            "algoritma": ["KMeans", "Agglomerative", "GMM", "DBSCAN"],
            "metrik": ["ARI vs diagnosis", "NMI vs diagnosis"],
            "metrik_internal": ["Silhouette", "Davies-Bouldin", "Calinski-Harabasz"],
        },
        "sensitivitas_K": {
            "faktor": "jumlah kelompok K",
            "level": [2, 3, 4, 5, 6],
            "algoritma": ["KMeans", "Agglomerative", "GMM"],
            "metrik": ["Silhouette"],
        },
    },
    "algoritma": {
        "KMeans": {"n_clusters": 2, "n_init": 10, "disetel": False},
        "Agglomerative": {"n_clusters": 2, "linkage": "ward", "disetel": False},
        "GMM": {"n_components": 2, "covariance_type": "full", "n_init": 5, "disetel": False},
        "DBSCAN": {
            "min_samples": [5, 10],
            "eps_kuantil_jarak_tetangga": [0.80, 0.85, 0.90, 0.95],
            "disetel": True,
            "aturan_seleksi": "Silhouette tertinggi di antara konfigurasi dengan minimal 2 kelompok dan noise paling banyak 10 persen",
            "jika_tak_ada_yang_valid": "dilaporkan 'tidak ada konfigurasi valid'; aturan tidak dilonggarkan",
        },
    },
    "praproses": {
        "baseline": "StandardScaler pada ke-30 fitur",
        "outlier": "tidak dibuang (keputusan Bab 4)",
        "seleksi_fitur": "tidak ada pada analisis utama",
    },
    "kebijakan_hyperparameter": {
        "K_analisis_utama": 2,
        "justifikasi_K": "RQ3 membandingkan dengan diagnosis dua kelas; K = 2 adalah asumsi desain, bukan hasil pemilihan; sensitivitas K dilaporkan terpisah",
        "label_untuk_tuning": False,
    },
    "pembanding_adil": [
        "data dan praproses sama untuk semua algoritma",
        "metrik internal dihitung di ruang baseline yang sama",
        "label tidak dipakai untuk memilih konfigurasi",
        "keterbatasan: hanya DBSCAN yang disetel, jadi upaya penyetelan tidak setara",
    ],
    "kondisi_terkontrol": {"random_state_dasar": 42, "catatan": "versi pustaka dicatat terpisah di 05_environment.json"},
    "aturan_keputusan": {
        "ambang_praktis_sama_ARI": 0.95,
        "catatan": "ambang ditetapkan sebelum eksperimen dan tidak digeser setelah melihat hasil",
    },
    "pengungkapan": [
        "Bab 1 menjalankan demonstrasi K-Means pada data yang sama dan menampilkan ARI terhadap diagnosis sebelum protokol ini ditulis",
        "protokol ini karena itu tidak sepenuhnya buta terhadap data; K = 2 dipengaruhi jumlah kelas diagnosis",
    ],
    "amendments": [],
}
print("Bagian protokol:", list(protocol))
print("Algoritma:", list(protocol["algoritma"]))
# --8<-- [end:protocol]

# --8<-- [start:validate]
def validate(p):
    """Mengembalikan daftar masalah. Daftar kosong berarti protokol lolos pemeriksaan bentuk (bukan kebenaran ilmiah)."""
    issues = []
    for key in ["versi", "dataset", "pertanyaan", "analisis", "algoritma", "praproses", "kebijakan_hyperparameter", "pembanding_adil"]:
        if key not in p:
            issues.append(f"bagian '{key}' tidak ada")
    for rq in p.get("pertanyaan", {}):
        if rq not in p.get("analisis", {}):
            issues.append(f"{rq} tidak punya rencana analisis")
        elif not p["analisis"][rq].get("metrik"):
            issues.append(f"{rq} tidak punya metrik")
    if p.get("kebijakan_hyperparameter", {}).get("label_untuk_tuning") is not False:
        issues.append("label tidak boleh dipakai untuk menyetel")
    if not p.get("dataset", {}).get("sidik_jari"):
        issues.append("sidik jari data tidak tercatat")
    if p.get("analisis", {}).get("RQ1", {}).get("ulangan", {}).get("seed", 0) < 10:
        issues.append("RQ1 butuh minimal 10 seed")
    defined = set(p.get("algoritma", {}))
    for name, plan in p.get("analisis", {}).items():
        for algo in plan.get("algoritma", []):
            if algo not in defined:
                issues.append(f"{name} memakai algoritma '{algo}' yang tidak didefinisikan")
    for item in p.get("amendments", []):
        if not item.get("alasan"):
            issues.append("ada amendment tanpa alasan")
    return issues


print("Protokol asli, masalah:", validate(protocol))

broken = copy.deepcopy(protocol)
del broken["analisis"]["RQ2"]
broken["kebijakan_hyperparameter"]["label_untuk_tuning"] = True
broken["dataset"]["sidik_jari"] = ""
broken["analisis"]["RQ3"]["algoritma"].append("SpectralClustering")
for issue in validate(broken):
    print("  - protokol rusak:", issue)
# --8<-- [end:validate]

# --8<-- [start:grid]
a = protocol["analisis"]
dbscan = protocol["algoritma"]["DBSCAN"]
runs = {
    "RQ1 seed": a["RQ1"]["ulangan"]["seed"],
    "RQ1 subsampel": a["RQ1"]["ulangan"]["subsampel"],
    "RQ2 level x seed": len(a["RQ2"]["level"]) * a["RQ2"]["ulangan"]["seed"],
    "RQ3 algoritma tak disetel": sum(not v["disetel"] for v in protocol["algoritma"].values()),
    "RQ3 grid DBSCAN": len(dbscan["min_samples"]) * len(dbscan["eps_kuantil_jarak_tetangga"]),
    "Sensitivitas K": len(a["sensitivitas_K"]["level"]) * len(a["sensitivitas_K"]["algoritma"]),
}
grid = pd.DataFrame({"jumlah_eksekusi": runs})
grid.loc["TOTAL"] = grid["jumlah_eksekusi"].sum()
print(grid.to_string())
# --8<-- [end:grid]

# --8<-- [start:smoke]
# Smoke test: apakah setiap konfigurasi bisa dijalankan? TIDAK memakai label dan TIDAK menghitung metrik hasil.
X_scaled = StandardScaler().fit_transform(X_all)
cfg = protocol["algoritma"]
models = {
    "KMeans": KMeans(n_clusters=cfg["KMeans"]["n_clusters"], n_init=cfg["KMeans"]["n_init"], random_state=42),
    "Agglomerative": AgglomerativeClustering(n_clusters=cfg["Agglomerative"]["n_clusters"], linkage=cfg["Agglomerative"]["linkage"]),
    "GMM": GaussianMixture(n_components=cfg["GMM"]["n_components"], covariance_type=cfg["GMM"]["covariance_type"], n_init=cfg["GMM"]["n_init"], random_state=42),
}
k = dbscan["min_samples"][0]
distances = NearestNeighbors(n_neighbors=k).fit(X_scaled).kneighbors(X_scaled)[0][:, -1]
eps = float(np.quantile(distances, dbscan["eps_kuantil_jarak_tetangga"][0]))
models["DBSCAN"] = DBSCAN(eps=eps, min_samples=k)

smoke_rows = []
for name, model in models.items():
    start = time.perf_counter()
    labels = model.fit_predict(X_scaled)
    elapsed = time.perf_counter() - start
    n_clusters = len(set(labels) - {-1})
    smoke_rows.append({"algoritma": name, "berjalan": True, "kelompok": n_clusters, "noise": int((labels == -1).sum()), "detik": round(elapsed, 3)})
smoke = pd.DataFrame(smoke_rows).set_index("algoritma")
print(smoke.to_string())
print("Smoke test tidak menghitung ARI/NMI; hasilnya tidak dilaporkan sebagai temuan.")
# --8<-- [end:smoke]

# --8<-- [start:lock]
def protocol_hash(p):
    text = json.dumps(p, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


locked = protocol_hash(protocol)
RESULTS.mkdir(exist_ok=True)
(RESULTS / "05_protocol.json").write_text(json.dumps(protocol, indent=2, ensure_ascii=False), encoding="utf-8")
(RESULTS / "05_protocol.sha256").write_text(locked + "\n", encoding="utf-8")
environment = {"python": platform.python_version(), "os": platform.system()}
for package in ("numpy", "pandas", "scikit-learn"):
    environment[package] = metadata.version(package)
(RESULTS / "05_environment.json").write_text(json.dumps(environment, indent=2), encoding="utf-8")

reloaded = json.loads((RESULTS / "05_protocol.json").read_text(encoding="utf-8"))
print("Hash protokol    :", locked[:16], "...")
print("Hash setelah baca:", "sama" if protocol_hash(reloaded) == locked else "BERBEDA")
tampered = copy.deepcopy(protocol)
tampered["kebijakan_hyperparameter"]["K_analisis_utama"] = 3
print("Hash setelah K diubah menjadi 3:", "sama" if protocol_hash(tampered) == locked else "BERBEDA")
# --8<-- [end:lock]

# --8<-- [start:amend]
def amend(p, perubahan, alasan, tanggal):
    """Perubahan setelah protokol dikunci TIDAK menimpa isi lama: dicatat sebagai amendment berbalas alasan."""
    updated = copy.deepcopy(p)
    updated["amendments"].append({"tanggal": tanggal, "perubahan": perubahan, "alasan": alasan})
    return updated


example = amend(protocol, "contoh: menambah 10 seed pada RQ1", "contoh latihan saja, tidak dipakai", "2026-11-10")
print("Amendment pada protokol asli:", len(protocol["amendments"]))
print("Amendment pada salinan contoh:", len(example["amendments"]))
print("Hash salinan contoh berbeda dari protokol terkunci:", protocol_hash(example) != locked)
print("Masalah pada salinan contoh:", validate(example))
# --8<-- [end:amend]
