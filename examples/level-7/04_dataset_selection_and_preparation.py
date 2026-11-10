"""Level 7, Bab 4: Pemilihan dataset dan persiapan data penelitian.

Menyusun kartu dokumentasi dataset dari sumber yang diverifikasi, mencocokkan dokumentasi dengan data
yang benar-benar dimuat, memeriksa kualitas, menerapkan kriteria inklusi dan eksklusi, membuat daftar
periksa etika yang jujur tentang hal yang tidak diketahui, lalu menyimpan dataset penelitian final.

Jalankan dari folder utama proyek:
    python examples/level-7/04_dataset_selection_and_preparation.py
"""
# NB: setup=Siapkan alat | datacard=Kartu dokumentasi dataset | verify=Mencocokkan dokumentasi dengan data | quality=Pemeriksaan kualitas | criteria=Kriteria inklusi dan eksklusi | ethics=Daftar periksa etika dan privasi | prepare=Dataset penelitian final | save=Menyimpan kartu, laporan, dan dataset

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:setup]
import json

import numpy as np
import pandas as pd

import _research as rs

X_all, diagnosis = rs.load_wdbc()
RESULTS = rs.RESULTS_DIR
print("Dimuat:", X_all.shape, "| label:", len(diagnosis))
# --8<-- [end:setup]

# --8<-- [start:datacard]
UNKNOWN = "tidak dinyatakan pada sumber yang dibaca"
card = {
    "nama": "Breast Cancer Wisconsin (Diagnostic)",
    "sumber_asli": "UCI Machine Learning Repository, https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic",
    "doi": "10.24432/C5DW2B",
    "pembuat": "William Wolberg, Olvi Mangasarian, Nick Street, W. Street (menurut halaman UCI)",
    "tanggal_donasi": "1995-10-31 (menurut halaman UCI)",
    "lisensi": "CC BY 4.0 (menurut halaman UCI); pemakaian wajib mencantumkan atribusi",
    "salinan_yang_dipakai": "sklearn.datasets.load_breast_cancer (salinan UCI yang disertakan scikit-learn)",
    "cara_pengumpulan": "Fitur dihitung dari citra digital aspirasi jarum halus (FNA) massa payudara; menggambarkan inti sel (menurut UCI dan scikit-learn)",
    "fitur": "10 ukuran inti sel, masing-masing dalam bentuk mean, standard error, dan worst = 30 fitur (menurut scikit-learn)",
    "label": "Diagnosis malignant atau benign (menurut UCI dan scikit-learn)",
    "tugas_asli": "Classification (menurut halaman UCI)",
    "persetujuan_etika_deidentifikasi": UNKNOWN,
    "demografi_pasien": UNKNOWN,
    "satuan_fitur": UNKNOWN,
    "makalah_pengantar": "Street, Wolberg, & Mangasarian (1993), Nuclear feature extraction for breast tumor diagnosis",
}
for key, value in card.items():
    print(f"{key:34s}: {value}")
# --8<-- [end:datacard]

# --8<-- [start:verify]
# Angka dokumentasi (dari deskripsi scikit-learn dan halaman UCI) dibandingkan dengan data yang dimuat.
documented = {
    "jumlah_sampel": 569,
    "jumlah_fitur": 30,
    "nilai_hilang": 0,
    "malignant": 212,
    "benign": 357,
    "mean radius min": 6.981,
    "mean radius max": 28.11,
    "mean area min": 143.5,
    "mean area max": 2501.0,
}
counts = diagnosis.value_counts()
observed = {
    "jumlah_sampel": X_all.shape[0],
    "jumlah_fitur": X_all.shape[1],
    "nilai_hilang": int(X_all.isna().sum().sum()),
    "malignant": int(counts["malignant"]),
    "benign": int(counts["benign"]),
    "mean radius min": round(float(X_all["mean radius"].min()), 3),
    "mean radius max": round(float(X_all["mean radius"].max()), 3),
    "mean area min": round(float(X_all["mean area"].min()), 1),
    "mean area max": round(float(X_all["mean area"].max()), 1),
}
check = pd.DataFrame({"dokumentasi": documented, "data": observed}, dtype=object)
check["status"] = np.where(check["dokumentasi"] == check["data"], "cocok", "BERBEDA")
print(check.to_string())
print("Semua cocok:", bool((check["status"] == "cocok").all()))
# --8<-- [end:verify]

# --8<-- [start:quality]
corr = X_all.corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1))
pairs = upper.stack().sort_values(ascending=False)
q1, q3 = X_all.quantile(0.25), X_all.quantile(0.75)
iqr = q3 - q1
outlier_count = ((X_all < q1 - 1.5 * iqr) | (X_all > q3 + 1.5 * iqr)).sum().sort_values(ascending=False)
quality = {
    "baris_duplikat": int(X_all.duplicated().sum()),
    "kolom_konstan": int((X_all.nunique() <= 1).sum()),
    "nilai_negatif": int((X_all < 0).sum().sum()),
    "pasangan_fitur_korelasi_di_atas_0.95": int((pairs > 0.95).sum()),
    "fitur_miring_kuat_(|skew|>1)": int((X_all.skew().abs() > 1).sum()),
    "total_nilai_di_luar_pagar_IQR": int(outlier_count.sum()),
}
for key, value in quality.items():
    print(f"{key:40s}: {value}")
print("Lima pasangan fitur paling berkorelasi:")
print(pairs.head(5).round(3).to_string())
print("Lima fitur dengan nilai luar pagar IQR terbanyak:")
print(outlier_count.head(5).to_string())
# --8<-- [end:quality]

# --8<-- [start:criteria]
# Kriteria ditulis sebelum menerapkannya. Setiap aturan mengembalikan baris yang LOLOS.
positive_by_definition = [c for c in X_all.columns if any(k in c for k in ("radius", "texture", "perimeter", "area"))]
rules = [
    ("I1 tidak ada nilai hilang pada 30 fitur", lambda f, d: ~f.isna().any(axis=1)),
    ("I2 punya label diagnosis (hanya validasi)", lambda f, d: d.notna()),
    ("E1 bukan baris duplikat persis", lambda f, d: ~f.duplicated(keep="first")),
    ("E2 fitur yang harus positif bernilai > 0", lambda f, d: (f[positive_by_definition] > 0).all(axis=1)),
]
keep = pd.Series(True, index=X_all.index)
funnel = [("Data awal", int(keep.sum()), 0)]
for name, rule in rules:
    passed = rule(X_all, diagnosis)
    removed = int((keep & ~passed).sum())
    keep &= passed
    funnel.append((name, int(keep.sum()), removed))
funnel_table = pd.DataFrame(funnel, columns=["langkah", "sisa_baris", "dikeluarkan"])
print(funnel_table.to_string(index=False))
# --8<-- [end:criteria]

# --8<-- [start:ethics]
ethics = pd.DataFrame(
    [
        ["Kategori data sensitif (kesehatan)", "Ya", "Subjek halaman UCI: Health and Medicine"],
        ["Kolom identitas pada salinan yang dipakai", "Tidak ada" if not any(c.lower() in ("id", "patient_id") for c in X_all.columns) else "ADA", "Diperiksa dengan kode pada nama kolom"],
        ["Persetujuan pasien dan tinjauan etik", "Tidak diketahui", "Halaman UCI tidak membahasnya"],
        ["Status de-identifikasi", "Tidak diketahui", "Halaman UCI tidak membahasnya"],
        ["Lisensi mengizinkan pemakaian ulang", "Ya, dengan atribusi", "CC BY 4.0 menurut halaman UCI"],
        ["Tujuan asli sama dengan tujuan kita", "Tidak sama", "Asli: classification; kita: metodologi clustering"],
        ["Klaim klinis dilakukan", "Tidak", "Dinyatakan di luar lingkup (Bab 2)"],
    ],
    columns=["pemeriksaan", "status", "dasar"],
)
print(ethics.to_string(index=False))
print("Butir 'Tidak diketahui':", int((ethics["status"] == "Tidak diketahui").sum()), "dari", len(ethics))
# --8<-- [end:ethics]

# --8<-- [start:prepare]
final_features = X_all.loc[keep].reset_index(drop=True)
final_diagnosis = diagnosis.loc[keep].reset_index(drop=True)
print("Fitur final   :", final_features.shape)
print("Label final   :", final_diagnosis.value_counts().to_dict())
print("Sidik jari awal :", rs.dataset_fingerprint(X_all))
print("Sidik jari final:", rs.dataset_fingerprint(final_features))
print("Data berubah    :", rs.dataset_fingerprint(X_all) != rs.dataset_fingerprint(final_features))
# --8<-- [end:prepare]

# --8<-- [start:save]
RESULTS.mkdir(exist_ok=True)
card["sidik_jari_data_final"] = rs.dataset_fingerprint(final_features)
card["jumlah_sampel_final"] = int(final_features.shape[0])
card["baris_dikeluarkan"] = int(X_all.shape[0] - final_features.shape[0])
card["kriteria"] = [name for name, _ in rules]
(RESULTS / "04_dataset_card.json").write_text(json.dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
check.reset_index(names="item").to_csv(RESULTS / "04_documentation_check.csv", index=False, encoding="utf-8")
funnel_table.to_csv(RESULTS / "04_inclusion_funnel.csv", index=False, encoding="utf-8")
ethics.to_csv(RESULTS / "04_ethics_checklist.csv", index=False, encoding="utf-8")
research_dataset = final_features.assign(diagnosis=final_diagnosis)
research_dataset.to_csv(RESULTS / "04_research_dataset.csv", index=False, encoding="utf-8")
for name in ["04_dataset_card.json", "04_documentation_check.csv", "04_inclusion_funnel.csv", "04_ethics_checklist.csv", "04_research_dataset.csv"]:
    print("Disimpan:", f"examples/level-7/results/{name}")
# --8<-- [end:save]
