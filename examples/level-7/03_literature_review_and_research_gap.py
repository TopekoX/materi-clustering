"""Level 7, Bab 3: Tinjauan pustaka dan celah riset.

Membangun matriks tinjauan pustaka dari lima sumber yang diverifikasi (hanya dari abstrak atau
ringkasan sumber, bukan teks lengkap), memetakan cakupannya ke pertanyaan riset Bab 2, mencatat log
pencarian, dan memeriksa kata-kata klaim celah riset.

Tidak ada temuan yang diketik dari ingatan: setiap sel matriks berasal dari sumber yang dibaca saat
bab ini ditulis. Bagian yang tidak tercantum di sumber ditulis "—".

Jalankan dari folder utama proyek (setelah menjalankan skrip Bab 2):
    python examples/level-7/03_literature_review_and_research_gap.py
"""
# NB: setup=Siapkan alat dan baca rumusan Bab 2 | matrix=Matriks tinjauan pustaka | completeness=Kelengkapan dan tingkat verifikasi | coverage=Cakupan pustaka terhadap pertanyaan riset | searchlog=Log pencarian | gapcheck=Memeriksa kata-kata klaim celah | statement=Pernyataan celah yang dibatasi | save=Menyimpan hasil

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")  # tanda "—" aman dicetak/dialihkan di Windows

# --8<-- [start:setup]
import json
import re

import pandas as pd

import _research as rs

RESULTS = rs.RESULTS_DIR
problem = json.loads((RESULTS / "02_research_problem.json").read_text(encoding="utf-8"))
print("Pertanyaan dari Bab 2:", list(problem["pertanyaan"]))
# --8<-- [end:setup]

# --8<-- [start:matrix]
NA = "—"  # tidak tercantum pada sumber yang dibaca
rows = [
    {
        "id": "L1",
        "referensi": "von Luxburg, Williamson, & Guyon (2012)",
        "tujuan": "Menanyakan apakah algoritma clustering dapat dibandingkan dengan prosedur umum yang ilmiah",
        "dataset": NA,
        "praproses": NA,
        "algoritma": NA,
        "metrik": NA,
        "temuan": "Evaluasi clustering harus mempertimbangkan konteks dan tujuan pemakaian; diusulkan taksonomi masalah clustering",
        "keterbatasan": NA,
        "celah_potensial": "Inferensi penulis bab: evaluasi perlu dikaitkan dengan tujuan pemakaian hasil",
        "topik": "konteks-evaluasi",
        "dibaca": "abstrak",
        "tautan": "https://proceedings.mlr.press/v27/luxburg12a.html",
    },
    {
        "id": "L2",
        "referensi": "Hennig (2015)",
        "tujuan": "Membahas makna \"kelompok yang benar\" pada analisis klaster",
        "dataset": NA,
        "praproses": NA,
        "algoritma": NA,
        "metrik": NA,
        "temuan": "Kebenaran bergantung pada konteks dan tujuan; clustering menjadi ilmiah lewat komunikasi yang terbuka dan transparan",
        "keterbatasan": NA,
        "celah_potensial": "Inferensi penulis bab: laporan perlu menyatakan tujuan dan konteks secara eksplisit",
        "topik": "konteks-evaluasi",
        "dibaca": "ringkasan halaman arXiv",
        "tautan": "https://arxiv.org/abs/1502.02555",
    },
    {
        "id": "L3",
        "referensi": "Ben-Hur, Elisseeff, & Guyon (2002)",
        "tujuan": "Menilai apakah data punya struktur kelompok dan membantu memilih jumlah kelompok lewat kestabilan",
        "dataset": "Data buatan dan data microarray",
        "praproses": NA,
        "algoritma": "Hierarchical clustering (pada hasil yang dilaporkan)",
        "metrik": "Kemiripan antara pengelompokan acuan dan pengelompokan dari subsampel",
        "temuan": "Pengelompokan yang baik seharusnya stabil terhadap gangguan pada data; metode berlaku untuk algoritma apa pun",
        "keterbatasan": NA,
        "celah_potensial": "Inferensi penulis bab: kestabilan perlu dilaporkan, termasuk pada data tabular lain",
        "topik": "kestabilan",
        "dibaca": "ringkasan hasil pencarian",
        "tautan": "Pacific Symposium on Biocomputing 7:6-17 (2002)",
    },
    {
        "id": "L4",
        "referensi": "Vinh, Epps, & Bailey (2010)",
        "tujuan": "Mengkaji ukuran berbasis teori informasi untuk membandingkan dua pengelompokan",
        "dataset": NA,
        "praproses": NA,
        "algoritma": NA,
        "metrik": "Ukuran teori informasi (termasuk NMI dan NID) dengan koreksi kebetulan",
        "temuan": "Ukuran perlu dikoreksi untuk kebetulan, terutama saat data kecil dibanding jumlah kelompok; NID direkomendasikan",
        "keterbatasan": NA,
        "celah_potensial": "Inferensi penulis bab: pilihan ukuran perbandingan perlu dijustifikasi dalam laporan",
        "topik": "pembanding-partisi",
        "dibaca": "ringkasan halaman JMLR",
        "tautan": "https://jmlr.org/papers/v11/vinh10a.html",
    },
    {
        "id": "L5",
        "referensi": "Jain (2010)",
        "tujuan": "Tinjauan umum metode clustering, tantangan, dan arah penelitian",
        "dataset": NA,
        "praproses": NA,
        "algoritma": "Tinjauan metode clustering yang dikenal",
        "metrik": NA,
        "temuan": "Merangkum metode dan tantangan; menyebut arah baru seperti semi-supervised, ensemble, seleksi fitur bersamaan, dan data besar",
        "keterbatasan": NA,
        "celah_potensial": "Inferensi penulis bab: tidak ada pada ringkasan yang dibaca",
        "topik": "tinjauan-umum",
        "dibaca": "ringkasan hasil pencarian",
        "tautan": "https://doi.org/10.1016/j.patrec.2009.09.011",
    },
]
matrix = pd.DataFrame(rows).set_index("id")
show = ["referensi", "dataset", "algoritma", "metrik", "topik", "dibaca"]
print(matrix[show].to_string())
# --8<-- [end:matrix]

# --8<-- [start:completeness]
fields = ["tujuan", "dataset", "praproses", "algoritma", "metrik", "temuan", "keterbatasan"]
filled = (matrix[fields] != NA).sum(axis=1)
report = pd.DataFrame({"sel_terisi": filled, "dari": len(fields), "dibaca": matrix["dibaca"]})
print(report.to_string())
print("Makalah dibaca penuh :", int((matrix["dibaca"] == "teks lengkap").sum()), "dari", len(matrix))
print("Kolom 'keterbatasan' terisi:", int((matrix["keterbatasan"] != NA).sum()), "dari", len(matrix))
# --8<-- [end:completeness]

# --8<-- [start:coverage]
# Setiap pertanyaan riset memerlukan jenis pustaka tertentu.
needs = {"RQ1": "kestabilan", "RQ2": "sensitivitas-praproses", "RQ3": "pembanding-partisi"}
coverage = {}
for rq, topic in needs.items():
    ids = matrix.index[matrix["topik"] == topic].tolist()
    coverage[rq] = {"topik_dibutuhkan": topic, "jumlah_makalah": len(ids), "makalah": ids}
    print(f"{rq}: butuh '{topic}' -> {len(ids)} makalah {ids}")
uncovered = [rq for rq, info in coverage.items() if info["jumlah_makalah"] == 0]
print("Pertanyaan tanpa dukungan pustaka pada set ini:", uncovered)
# --8<-- [end:coverage]

# --8<-- [start:searchlog]
# Log pencarian yang benar-benar dilakukan saat bab ini disusun.
search_log = pd.DataFrame(
    [
        ["2026-11-10", "alat pencarian web", "Clustering: Science or Art? von Luxburg Williamson Guyon", "L1"],
        ["2026-11-10", "halaman arXiv", "arXiv:1502.02555 (Hennig)", "L2"],
        ["2026-11-10", "alat pencarian web", "Ben-Hur Elisseeff Guyon stability based method clustered data", "L3"],
        ["2026-11-10", "halaman JMLR", "jmlr.org/papers/v11/vinh10a.html", "L4"],
        ["2026-11-10", "alat pencarian web", "Jain Data clustering 50 years beyond K-means", "L5"],
    ],
    columns=["tanggal", "sumber", "kueri", "hasil_dipilih"],
)
print(search_log.to_string(index=False))
print("Jenis tinjauan: terarah (bukan sistematis); jumlah pencarian:", len(search_log))
# --8<-- [end:searchlog]

# --8<-- [start:gapcheck]
def check_gap_claim(text):
    """True berarti ada MASALAH. Alat bantu berbasis kata kunci, bukan penilai."""
    low = text.lower()
    return {
        "klaim_mutlak": any(w in low for w in ["belum pernah", "tidak ada penelitian", "tidak ada satu pun", "pertama kali", "satu-satunya"]),
        "tanpa_batas_pencarian": not re.search(r"\b(dari|di antara)\s+\d+\s+(makalah|sumber|studi)", low),
        "klaim_kebaruan": any(w in low for w in ["baru", "inovatif", "terobosan"]),
    }


claims = {
    "C1": "Belum pernah ada penelitian tentang kestabilan clustering pada data medis.",
    "C2": "Penelitian ini adalah yang pertama kali membandingkan kestabilan dan keselarasan eksternal.",
    "C3": "Dari 5 sumber yang ditelaah berdasarkan abstrak, tidak satu pun yang kami baca menyajikan protokol terpadu untuk kestabilan, kepekaan praproses, dan keselarasan eksternal pada satu dataset publik. Ini bukan klaim bahwa studi serupa tidak ada.",
}
for code_, text in claims.items():
    flags = check_gap_claim(text)
    problems = [name for name, is_problem in flags.items() if is_problem]
    print(f"{code_}: {'lolos' if not problems else 'perlu diperbaiki: ' + ', '.join(problems)}")
# --8<-- [end:gapcheck]

# --8<-- [start:statement]
n_sources = len(matrix)
gap_statement = (
    f"Dari {n_sources} sumber yang ditelaah berdasarkan abstrak atau ringkasan, tidak satu pun yang kami baca "
    "menyajikan protokol terpadu yang mengukur kestabilan, kepekaan terhadap praproses, dan keselarasan eksternal "
    "pada satu dataset publik dengan seluruh konfigurasi dibagikan. Ini bukan klaim bahwa studi serupa tidak ada; "
    "tinjauan ini terarah, bukan sistematis."
)
flags = check_gap_claim(gap_statement)
print("Pernyataan celah:", gap_statement)
print("Pemeriksa klaim :", "lolos" if not any(flags.values()) else flags)
# --8<-- [end:statement]

# --8<-- [start:save]
def to_markdown(frame):
    header = "| " + " | ".join(frame.columns) + " |"
    divider = "|" + "|".join("---" for _ in frame.columns) + "|"
    body = ["| " + " | ".join(str(v).replace("|", "/") for v in row) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, divider, *body])


view = matrix.reset_index()[["id", "referensi", "tujuan", "dataset", "algoritma", "metrik", "temuan", "dibaca"]]
RESULTS.mkdir(exist_ok=True)
matrix.to_csv(RESULTS / "03_literature_matrix.csv", encoding="utf-8")
search_log.to_csv(RESULTS / "03_search_log.csv", index=False, encoding="utf-8")
(RESULTS / "03_literature_matrix.md").write_text(to_markdown(view) + "\n", encoding="utf-8")
(RESULTS / "03_gap_statement.json").write_text(
    json.dumps(
        {
            "pernyataan_celah": gap_statement,
            "jumlah_sumber": n_sources,
            "jenis_tinjauan": "terarah",
            "cakupan": coverage,
            "pertanyaan_tanpa_pustaka": uncovered,
            "perubahan_pertanyaan_dari_bab_2": "tidak ada perubahan teks; RQ2 ditandai butuh pustaka tambahan",
            "sumber_rumusan": "02_research_problem.json",
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
for name in ["03_literature_matrix.csv", "03_literature_matrix.md", "03_search_log.csv", "03_gap_statement.json"]:
    print("Disimpan:", f"examples/level-7/results/{name}")
# --8<-- [end:save]
