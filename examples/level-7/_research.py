"""Alat bantu bersama untuk Level 7 (Research Project).

Hanya memakai NumPy, pandas, dan scikit-learn. Dataset proyek: Breast Cancer Wisconsin
(Diagnostic), UCI Machine Learning Repository, CC BY 4.0, DOI 10.24432/C5DW2B.
Lihat Bab 4 untuk dokumentasi sumber dan lisensi.
"""

# --8<-- [start:helpers]
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def load_wdbc():
    """Mengembalikan (fitur, diagnosis). Diagnosis hanya untuk validasi, bukan untuk melatih."""
    bunch = load_breast_cancer(as_frame=True)
    diagnosis = bunch.target.map({0: "malignant", 1: "benign"}).rename("diagnosis")
    return bunch.data, diagnosis


def dataset_fingerprint(X):
    """Sidik jari data: 12 karakter pertama hash SHA-256 isi array."""
    return hashlib.sha256(np.ascontiguousarray(np.asarray(X, dtype=float)).tobytes()).hexdigest()[:12]
# --8<-- [end:helpers]
