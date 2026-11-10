"""Level 7, Bab 2: Perumusan masalah penelitian clustering.

Menunjukkan cara menulis pertanyaan riset yang terstruktur, memeriksanya dengan daftar periksa
sederhana, mengecek apakah data bisa menjawabnya, lalu menyimpan rumusan masalah proyek.

Jalankan dari folder utama proyek:
    python examples/level-7/02_research_problem_formulation.py
"""
# NB: setup=Siapkan alat | feasibility=Apakah data bisa menjawab? | checker=Pemeriksa pertanyaan riset | examples=Menguji pertanyaan baik dan buruk | matching=Mencocokkan pertanyaan dengan pendekatan | project=Rumusan masalah proyek | save=Menyimpan rumusan masalah

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import json
import re

import pandas as pd

import _research as rs

X_all, diagnosis = rs.load_wdbc()
# --8<-- [end:setup]

# --8<-- [start:feasibility]
# Sebelum merumuskan pertanyaan, periksa apa yang sebenarnya dimiliki data.
facts = {
    "jumlah_sampel": X_all.shape[0],
    "jumlah_fitur": X_all.shape[1],
    "nilai_hilang": int(X_all.isna().sum().sum()),
    "ada_label_eksternal": diagnosis is not None,
    "kelas_label": diagnosis.value_counts().to_dict(),
    "ada_kolom_waktu": any("time" in c or "date" in c for c in X_all.columns),
    "ada_kolom_pasien": any("id" == c.lower() or "patient" in c.lower() for c in X_all.columns),
}
for key, value in facts.items():
    print(f"{key:22s}: {value}")
# --8<-- [end:feasibility]

# --8<-- [start:checker]
def check_question(text):
    """Daftar periksa sederhana. True berarti ada MASALAH pada aspek tersebut.

    Ini alat bantu berpikir berbasis kata kunci, bukan penilai. Ia bisa salah (lihat contoh)."""
    low = text.lower()
    words = set(re.findall(r"[a-z]+", low))
    return {
        "bukan_pertanyaan": not text.strip().endswith("?"),
        "mulai_dari_algoritma": low.startswith(("menggunakan", "menerapkan", "memakai")),
        "klaim_sebab_akibat": any(w in low for w in ["menyebabkan", "penyebab", "akibat", "mengapa"]),
        "klaim_klinis": any(w in low for w in ["mendiagnosis", "mendeteksi", "memprediksi", "mengobati"]),
        "klaim_universal": any(w in low for w in ["selalu", "semua data", "pasti", "tidak pernah"]),
        "tidak_terukur": not (words & {"stabil", "seberapa", "ari", "nmi", "silhouette", "berubah", "selaras", "berbeda"}),
    }


def verdict(flags):
    problems = [name for name, is_problem in flags.items() if is_problem]
    return "lolos" if not problems else "perlu diperbaiki: " + ", ".join(problems)
# --8<-- [end:checker]

# --8<-- [start:examples]
examples = {
    "B1": "Menggunakan K-Means untuk mengelompokkan data kanker.",
    "B2": "Apakah clustering bisa mendiagnosis kanker payudara?",
    "B3": "Mengapa ukuran inti sel menyebabkan kelompok ganas?",
    "B4": "Algoritma clustering mana yang selalu terbaik untuk semua data?",
    "B5": "Bagaimana data ini?",
    "G1": "Seberapa stabil pengelompokan K-Means pada 30 fitur morfologi bila seed dan sampel data diubah?",
    "G2": "Apakah pengelompokan pada 30 fitur morfologi berubah bila fitur tidak distandarkan, dan seberapa besar perubahannya (ARI)?",
    "G3": "Seberapa selaras pengelompokan tak terawasi pada profil morfologi dengan diagnosis yang tercatat (ARI dan NMI)?",
    "T1": "Apakah hasil clustering stabil dan selaras dengan diagnosis serta berbeda antar algoritma pada semua aspek?",
}
for code, text in examples.items():
    print(f"{code}: {text}")
    print(f"    -> {verdict(check_question(text))}")
# --8<-- [end:examples]

# --8<-- [start:matching]
matching = pd.DataFrame(
    [
        ["Eksploratif", "Adakah struktur kelompok?", "K-Means, Hierarchical", "Silhouette, visualisasi", "Level 4 B2-B3, Level 6 B8"],
        ["Komparatif", "Algoritma mana yang cocok untuk data ini?", "K-Means, GMM, DBSCAN, Hierarchical", "Metrik di ruang yang sama", "Level 4 B7, Level 6 B4"],
        ["Sensitivitas", "Seberapa peka hasil terhadap praproses atau parameter?", "Satu algoritma, satu faktor diubah", "ARI terhadap baseline", "Level 6 B2, B3, B5"],
        ["Kestabilan", "Apakah hasil tahan terhadap seed dan sampel?", "Satu algoritma, ulang berkali-kali", "ARI antar-ulangan, Jaccard", "Level 6 B9"],
        ["Validasi eksternal", "Seberapa selaras dengan pengetahuan di luar data?", "Clustering dulu, label sesudahnya", "ARI, NMI terhadap label", "Level 5 B8"],
    ],
    columns=["Tipe pertanyaan", "Contoh", "Pendekatan", "Evaluasi", "Rujukan"],
)
print(matching.to_string(index=False))
# --8<-- [end:matching]

# --8<-- [start:project]
# Rumusan masalah untuk proyek akhir (Bab 10). Ini DRAF: dirumuskan ulang di Bab 3 setelah tinjauan pustaka.
project = {
    "judul_kerja": "Stabilitas dan keselarasan struktur kelompok pada profil morfologi inti sel",
    "masalah": "Algoritma clustering berbasis partisi menghasilkan kelompok pada data apa pun, tetapi belum tentu kelompok itu stabil atau bermakna.",
    "tujuan": [
        "Mengukur kestabilan pengelompokan terhadap seed dan sampel data.",
        "Mengukur kepekaan pengelompokan terhadap penyamaan skala dan pilihan algoritma.",
        "Mengukur keselarasan kelompok dengan diagnosis yang tercatat sebagai validasi eksternal.",
    ],
    "pertanyaan": {
        "RQ1": "Seberapa stabil pengelompokan K-Means pada 30 fitur morfologi bila seed dan sampel data diubah?",
        "RQ2": "Apakah pengelompokan pada 30 fitur morfologi berubah bila fitur tidak distandarkan, dan seberapa besar perubahannya (ARI)?",
        "RQ3": "Seberapa selaras pengelompokan tak terawasi pada profil morfologi dengan diagnosis yang tercatat (ARI dan NMI)?",
    },
    "dalam_lingkup": ["satu dataset publik", "empat algoritma dari Level 4", "metrik dari Level 5", "30 fitur numerik"],
    "di_luar_lingkup": ["klaim klinis atau diagnosis", "klaim sebab-akibat", "data pasien baru", "generalisasi ke dataset lain"],
    "keterbatasan": [
        "satu dataset dengan 569 sampel",
        "label diagnosis hanya dua kelas dan bukan satu-satunya struktur yang mungkin ada",
        "hasil berlaku untuk pengaturan yang diuji",
    ],
    "kontribusi": "didaktik dan metodologis: mendemonstrasikan protokol penelitian clustering yang bisa diulang. Tidak mengklaim kebaruan ilmiah.",
}
for rq_id, text in project["pertanyaan"].items():
    print(f"{rq_id}: {verdict(check_question(text))}")
# --8<-- [end:project]

# --8<-- [start:save]
project["data"] = {"sumber": "UCI, Breast Cancer Wisconsin (Diagnostic), CC BY 4.0", "sidik_jari": rs.dataset_fingerprint(X_all)}
project["status"] = "draf Bab 2, dirumuskan ulang di Bab 3"
rs.RESULTS_DIR.mkdir(exist_ok=True)
out = rs.RESULTS_DIR / "02_research_problem.json"
out.write_text(json.dumps(project, indent=2, ensure_ascii=False), encoding="utf-8")
print("Disimpan:", out.relative_to(ROOT).as_posix())
print("Jumlah pertanyaan:", len(project["pertanyaan"]), "| jumlah tujuan:", len(project["tujuan"]))
# --8<-- [end:save]
