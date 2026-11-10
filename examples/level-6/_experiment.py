"""Alat bantu eksperimen untuk Level 6: pencatatan sederhana ke CSV dan JSON.

Modul ini hanya memakai pustaka standar, NumPy, pandas, dan scikit-learn. Tidak ada
platform pelacakan eksperimen. Hasil disimpan di examples/level-6/results/.
"""

# --8<-- [start:helpers]
import hashlib
import json
import platform
import time
from importlib import metadata
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def dataset_fingerprint(X):
    """Sidik jari data: 12 karakter pertama dari hash SHA-256 isi array. Data berbeda, sidik jari berbeda."""
    return hashlib.sha256(np.ascontiguousarray(X).tobytes()).hexdigest()[:12]


def environment_info():
    """Versi Python dan pustaka yang dipakai, supaya hasil bisa diulang di lingkungan yang sama."""
    info = {"python": platform.python_version(), "os": platform.system()}
    for package in ("numpy", "pandas", "scikit-learn", "scipy", "matplotlib"):
        info[package] = metadata.version(package)
    return info


def timed(function, *args, **kwargs):
    """Menjalankan function dan mengembalikan (hasil, waktu_detik)."""
    start = time.perf_counter()
    result = function(*args, **kwargs)
    return result, time.perf_counter() - start


def internal_scores(X, labels):
    """Ringkasan hasil clustering. Noise (label -1) dikeluarkan sebelum menghitung metrik internal.

    Mengembalikan jumlah kelompok, proporsi noise, dan tiga metrik internal Level 5.
    Bila kurang dari dua kelompok tersisa, ketiga metrik bernilai NaN.
    """
    labels = np.asarray(labels)
    mask = labels != -1
    n_clusters = len(set(labels[mask].tolist()))
    result = {
        "n_clusters": n_clusters,
        "noise_fraction": float(1 - mask.mean()),
        "silhouette": np.nan,
        "davies_bouldin": np.nan,
        "calinski_harabasz": np.nan,
    }
    if n_clusters >= 2 and mask.sum() > n_clusters:
        result["silhouette"] = silhouette_score(X[mask], labels[mask])
        result["davies_bouldin"] = davies_bouldin_score(X[mask], labels[mask])
        result["calinski_harabasz"] = calinski_harabasz_score(X[mask], labels[mask])
    return result


def make_record(experiment_id, dataset, X, preprocessing, features, algorithm, params, seed, scores, runtime):
    """Satu baris catatan eksperimen. `params` disimpan sebagai teks JSON."""
    return {
        "experiment_id": experiment_id,
        "dataset": dataset,
        "dataset_fingerprint": dataset_fingerprint(X),
        "preprocessing": preprocessing,
        "features": features,
        "algorithm": algorithm,
        "params": json.dumps(params, sort_keys=True),
        "seed": seed,
        **scores,
        "runtime_seconds": runtime,
    }


def save_records(records, name):
    """Menyimpan daftar catatan ke results/<name>.csv dan mengembalikan DataFrame-nya."""
    RESULTS_DIR.mkdir(exist_ok=True)
    table = pd.DataFrame(records)
    table.to_csv(RESULTS_DIR / f"{name}.csv", index=False)
    return table


def save_json(obj, name):
    """Menyimpan objek (misalnya konfigurasi atau info lingkungan) ke results/<name>.json."""
    RESULTS_DIR.mkdir(exist_ok=True)
    with open(RESULTS_DIR / f"{name}.json", "w", encoding="utf-8") as handle:
        json.dump(obj, handle, indent=2, ensure_ascii=False, default=str)
# --8<-- [end:helpers]
