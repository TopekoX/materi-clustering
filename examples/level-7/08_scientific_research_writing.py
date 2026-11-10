"""Level 7, Bab 8: Penulisan ilmiah.

Merakit kerangka naskah dari hasil proyek (judul, abstrak terstruktur, peta bagian IMRaD, tabel konfigurasi,
daftar tabel/gambar/persamaan, pernyataan ketersediaan data) lalu menjalankan daftar periksa penulisan yang
bisa diperiksa otomatis. Butir yang memerlukan penilaian manusia ditandai MANUAL.

Skrip TIDAK menulis prosa Pendahuluan, Kajian Pustaka, Pembahasan, atau Kesimpulan. Ia hanya merakit
kerangka dari fakta yang sudah terverifikasi; prosa tetap tugas penulis.

Jalankan dari folder utama proyek (setelah skrip Bab 2 sampai 7):
    python examples/level-7/08_scientific_research_writing.py
"""
# NB: setup=Siapkan alat dan baca hasil proyek | title=Judul | abstract=Abstrak terstruktur | sections=Peta bagian naskah | elements=Tabel konfigurasi, tabel, gambar, dan persamaan | statements=Pernyataan data dan kode | checklist=Daftar periksa penulisan | outline=Menyusun kerangka naskah

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:setup]
import json
import re

import pandas as pd

import _research as rs

RESULTS = rs.RESULTS_DIR
FIGURES = ROOT / "docs" / "assets" / "level-7"
problem = json.loads((RESULTS / "02_research_problem.json").read_text(encoding="utf-8"))
gap = json.loads((RESULTS / "03_gap_statement.json").read_text(encoding="utf-8"))
card = json.loads((RESULTS / "04_dataset_card.json").read_text(encoding="utf-8"))
protocol = json.loads((RESULTS / "05_protocol.json").read_text(encoding="utf-8"))
protocol_lock = (RESULTS / "05_protocol.sha256").read_text(encoding="utf-8").strip()
facts = json.loads((RESULTS / "07_facts.json").read_text(encoding="utf-8"))
ledger = pd.read_csv(RESULTS / "07_claim_ledger.csv").set_index("id")
literature = pd.read_csv(RESULTS / "03_literature_matrix.csv", index_col="id")


def fmt(value, digits=3):
    return f"{value:.{digits}f}".replace(".", ",")


def words(text):
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


pool = {fmt(float(v), d) for v in facts.values() for d in (1, 2, 3)}
OVERCLAIM = ["membuktikan", "terbukti", "pasti", "menyebabkan", "tidak diragukan", "selalu", "mengonfirmasi", "terbaik", "revolusioner", "sempurna"]


def overclaim_words(text):
    low = text.lower()
    found = []
    for word in OVERCLAIM:
        for match in re.finditer(r"\b" + word + r"\b", low):
            if "tidak " not in low[max(0, match.start() - 12):match.start()] and "bukan " not in low[max(0, match.start() - 12):match.start()]:
                found.append(word)
                break
    return found


def untraceable_numbers(text):
    return [x for x in re.findall(r"-?\d+,\d+", text) if x not in pool and x not in {"0,95", "0,9"}]


print("Sumber dibaca: buku bukti", len(ledger), "kalimat | matriks pustaka", len(literature), "makalah")
# --8<-- [end:setup]

# --8<-- [start:title]
def check_title(title):
    """True berarti ada MASALAH. Alat bantu berbasis kata kunci."""
    low = title.lower()
    n = words(title)
    return {
        "terlalu_pendek": n < 8,
        "terlalu_panjang": n > 25,
        "klaim_berlebihan": bool(overclaim_words(title)),
        "tanpa_objek_penelitian": not any(w in low for w in ("pengelompokan", "clustering", "klaster")),
        "tanpa_konteks_data": " pada " not in f" {low} ",
    }


titles = {
    "T1": "Clustering Terbaik untuk Semua Data Kanker",
    "T2": "Analisis Clustering",
    "T3": "Kestabilan dan Keselarasan Eksternal Pengelompokan pada Profil Morfologi Inti Sel: Studi Metodologis dengan Protokol Terkunci pada Satu Dataset Publik",
}
for code_, title in titles.items():
    flags = check_title(title)
    problems = [k for k, v in flags.items() if v]
    print(f"{code_} ({words(title)} kata): {'lolos' if not problems else 'perlu diperbaiki: ' + ', '.join(problems)}")
final_title = titles["T3"]
# --8<-- [end:title]

# --8<-- [start:abstract]
def pick(*ids):
    return " ".join(ledger.loc[i, "kalimat"] for i in ids)


goals = [g.rstrip(".")[0].lower() + g.rstrip(".")[1:] for g in problem["tujuan"]]
algorithms = ", ".join(protocol["algoritma"])
abstract_draft = {
    "Latar belakang": problem["masalah"],
    "Tujuan": "Penelitian ini bertujuan " + "; ".join(goals) + ".",
    "Metode": (
        f"Data: {card['nama']} ({protocol['dataset']['jumlah_sampel']} sampel, {protocol['dataset']['jumlah_fitur']} fitur; UCI, CC BY 4.0). "
        f"Algoritma: {algorithms}. Praproses StandardScaler. Protokol dikunci dengan hash sebelum eksperimen; label diagnosis hanya untuk validasi."
    ),
    "Hasil": pick("H1", "H3", "H5", "H7"),
    "Kesimpulan": pick("I1", "I5"),
    "Keterbatasan": pick("K1", "K2"),
}
ABSTRACT_LIMIT = 250   # contoh batas; sesuaikan dengan pedoman penerbit tujuan
draft_words = words(" ".join(abstract_draft.values()))
print("Draf pertama:", draft_words, "kata |", "melebihi batas" if draft_words > ABSTRACT_LIMIT else "dalam batas")

# Pemangkasan: H7 (bootstrap) dibuang dari bagian Hasil karena isinya sudah ada pada kalimat Kesimpulan (I5).
abstract = {**abstract_draft, "Hasil": pick("H1", "H3", "H5")}
abstract_text = " ".join(abstract.values())
for key, value in abstract.items():
    print(f"{key:15s}: {words(value):3d} kata")
print("Total kata abstrak:", words(abstract_text), "| contoh batas:", ABSTRACT_LIMIT)
print("Angka tak terlacak :", untraceable_numbers(abstract_text))
print("Kata berlebihan    :", overclaim_words(abstract_text))
# --8<-- [end:abstract]

# --8<-- [start:sections]
section_map = pd.DataFrame(
    [
        ["Pendahuluan", "02_research_problem.json; 03_gap_statement.json", "Masalah, konteks, celah yang dibatasi, tujuan, pertanyaan", "500-800"],
        ["Kajian pustaka", "03_literature_matrix.csv", "Dikelompokkan per tema, bukan per makalah", "600-1000"],
        ["Metode", "04_dataset_card.json; 05_protocol.json; 05_environment.json", "Data, praproses, algoritma, metrik, protokol, hash", "800-1200"],
        ["Hasil", "06_rq2_scaling.csv; 06_rq3_algorithms.csv; 07_tables.md", "Angka dan pengamatan, tanpa alasan", "700-1000"],
        ["Pembahasan", "07_claim_ledger.csv", "Interpretasi, hasil tak terduga, hubungan dengan pustaka", "700-1000"],
        ["Keterbatasan", "07_claim_ledger.csv", "Batas data, metode, protokol, bacaan pustaka", "200-400"],
        ["Kesimpulan", "07_claim_ledger.csv", "Jawaban terbatas untuk tiap pertanyaan", "150-300"],
        ["Ketersediaan data dan kode", "04_dataset_card.json; 05_protocol.sha256", "Sumber, lisensi, atribusi, tautan kode", "80-150"],
    ],
    columns=["bagian", "sumber_dari_proyek", "isi_utama", "saran_kata"],
)
exists = []
for sources in section_map["sumber_dari_proyek"]:
    names = [s.strip() for s in sources.split(";")]
    exists.append(all((RESULTS / n).exists() for n in names))
section_map["sumber_ada"] = exists
print(section_map[["bagian", "saran_kata", "sumber_ada"]].to_string(index=False))
print("Semua sumber ada:", bool(section_map["sumber_ada"].all()))
# --8<-- [end:sections]

# --8<-- [start:elements]
cfg_rows = []
for name, params in protocol["algoritma"].items():
    shown = {k: v for k, v in params.items() if k not in ("disetel", "aturan_seleksi", "jika_tak_ada_yang_valid")}
    cfg_rows.append([name, "; ".join(f"{k}={v}" for k, v in shown.items()), "ya" if params["disetel"] else "tidak"])
config_table = pd.DataFrame(cfg_rows, columns=["Algoritma", "Pengaturan", "Disetel"])
print(config_table.to_string(index=False))

assets = [
    {"id": "Tabel 1", "file": "07_tables.md", "dir": RESULTS, "caption": "Perbandingan empat algoritma pada K = 2 di ruang baseline terstandarisasi; arah metrik ditulis pada kepala kolom, dan DBSCAN tidak memiliki konfigurasi valid menurut protokol."},
    {"id": "Tabel 2", "file": "07_tables.md", "dir": RESULTS, "caption": "ARI terhadap baseline menurut perlakuan skala (20 seed per perlakuan); ambang praktis sama ditetapkan 0,95 sebelum eksperimen."},
    {"id": "Gambar 1", "file": "06-kestabilan-dan-skala.png", "dir": FIGURES, "caption": "Kestabilan K-Means (K = 2) antar-seed dan antar-subsampel, serta ARI terhadap baseline untuk tiga perlakuan skala; garis putus-putus menandai ambang 0,95."},
    {"id": "Gambar 2", "file": "06-empat-algoritma.png", "dir": FIGURES, "caption": "Proyeksi PCA dua komponen dengan pengelompokan K-Means, Agglomerative, dan GMM; proyeksi hanya untuk visualisasi dan DBSCAN tidak ditampilkan karena tidak ada konfigurasi valid."},
    {"id": "Gambar 3", "file": "07-ari-dan-ketidakpastian.png", "dir": FIGURES, "caption": "ARI terhadap diagnosis per algoritma dengan interval bootstrap 95 persen (eksploratori) dan ukuran inti sel yang paling berbeda antar dua kelompok K-Means."},
]
for item in assets:
    item["ada"] = (item["dir"] / item["file"]).exists()
    item["kata_keterangan"] = words(item["caption"])
assets_df = pd.DataFrame(assets)[["id", "file", "ada", "kata_keterangan"]]
print(assets_df.to_string(index=False))

equations = {
    "Persamaan 1 (ARI)": {"simbol": {"RI": "Rand Index", "E[RI]": "nilai harapan RI untuk pengelompokan acak"}, "dirujuk_di": "Metode"},
    "Persamaan 2 (Stab_seed)": {"simbol": {"S": "jumlah seed", "l_i": "pengelompokan pada seed ke-i"}, "dirujuk_di": "Metode"},
    "Persamaan 3 (Stab_sub)": {"simbol": {"B": "jumlah subsampel", "I_b": "indeks subsampel ke-b"}, "dirujuk_di": "Metode"},
    "Persamaan 4 (selisih ARI)": {"simbol": {"Delta_b": "selisih ARI dua algoritma pada ulangan ke-b", "B": "jumlah ulangan bootstrap"}, "dirujuk_di": "Metode"},
}
undefined = [name for name, e in equations.items() if not e["simbol"] or any(not d for d in e["simbol"].values())]
print("Persamaan:", len(equations), "| persamaan dengan simbol belum didefinisikan:", undefined if undefined else "tidak ada")
# --8<-- [end:elements]

# --8<-- [start:statements]
data_statement = (
    f"Data: {card['nama']}, {card['sumber_asli'].split(', ')[0]}, DOI {card['doi']}, lisensi CC BY 4.0 menurut halaman UCI; "
    f"salinan yang dipakai dimuat melalui scikit-learn. Pembuat: {card['pembuat'].split(' (')[0]}. "
    f"Sidik jari data final: {card['sidik_jari_data_final']}. "
    f"Protokol dikunci dengan hash SHA-256 {protocol_lock[:16]}...; seluruh kode dan berkas hasil tersedia di [TAUTAN REPOSITORI: diisi penulis]."
)
ethics_statement = "Data publik berlisensi CC BY 4.0. Persetujuan etik dan status de-identifikasi tidak dinyatakan pada sumber yang dibaca. Penelitian ini tidak membuat klaim klinis."
print(data_statement)
print(ethics_statement)
# --8<-- [end:statements]

# --8<-- [start:checklist]
checks = []


def check(name, ok, detail, kind="otomatis", warn_only=False):
    status = "LULUS" if ok else ("PERINGATAN" if warn_only else "GAGAL")
    checks.append({"butir": name, "jenis": kind, "status": status, "rincian": detail})


check("Judul: tidak ada masalah pada pemeriksa", not any(check_title(final_title).values()), f"{words(final_title)} kata")
check("Abstrak dalam batas kata", words(abstract_text) <= ABSTRACT_LIMIT, f"{words(abstract_text)} dari {ABSTRACT_LIMIT} kata")
check("Abstrak: angka terlacak ke berkas hasil", not untraceable_numbers(abstract_text), f"tak terlacak: {untraceable_numbers(abstract_text)}")
check("Abstrak: tanpa kata berlebihan", not overclaim_words(abstract_text), f"ditemukan: {overclaim_words(abstract_text)}")
check("Abstrak menyebut keterbatasan", "Keterbatasan" in abstract and words(abstract["Keterbatasan"]) > 0, f"{words(abstract['Keterbatasan'])} kata")
check("Semua sumber proyek untuk bagian naskah ada", bool(section_map["sumber_ada"].all()), f"{int(section_map['sumber_ada'].sum())} dari {len(section_map)} bagian")
check("Tabel dan gambar: berkas ada", bool(assets_df["ada"].all()), f"{int(assets_df['ada'].sum())} dari {len(assets_df)}")
check("Keterangan tabel dan gambar cukup mandiri (minimal 15 kata)", bool((assets_df["kata_keterangan"] >= 15).all()), f"terpendek {int(assets_df['kata_keterangan'].min())} kata")
check("Semua simbol persamaan didefinisikan", not undefined, f"{len(equations)} persamaan")
limitations = ledger[ledger["jenis"] == "keterbatasan"]
check("Keterbatasan minimal tiga butir", len(limitations) >= 3, f"{len(limitations)} butir")
exploratory = ledger[ledger["kalimat"].str.contains("Eksploratori", case=False)]
check("Analisis eksploratori diberi label", len(exploratory) >= 1, f"{len(exploratory)} kalimat berlabel")
check("Pernyataan data memuat DOI, lisensi, dan sidik jari", all(x in data_statement for x in (card["doi"], "CC BY 4.0", card["sidik_jari_data_final"])), "DOI, lisensi, sidik jari")
check("Pernyataan data: tautan repositori sudah final", "[TAUTAN REPOSITORI" not in data_statement, "masih placeholder, diisi penulis", warn_only=True)
check("Hash protokol dikutip pada pernyataan", protocol_lock[:16] in data_statement, protocol_lock[:16])
read_full = int((literature["dibaca"] == "teks lengkap").sum())
check("Kajian pustaka: sumber dibaca penuh", read_full == len(literature), f"{read_full} dari {len(literature)} dibaca penuh", warn_only=True)
check("Kajian pustaka: tiap pertanyaan punya pustaka", not gap["pertanyaan_tanpa_pustaka"], f"tanpa pustaka: {gap['pertanyaan_tanpa_pustaka']}", warn_only=True)
for manual in ["Tata bahasa dan gaya sesuai pedoman penerbit tujuan", "Format sitasi dan daftar pustaka konsisten", "Kebijakan etik, kepengarangan, dan penggunaan alat bantu penulisan penerbit dibaca dan dipenuhi", "Pemeriksaan kemiripan teks (plagiarisme) dilakukan", "Semua penulis menyetujui naskah"]:
    check(manual, False, "memerlukan penilaian manusia", kind="manual", warn_only=True)
    checks[-1]["status"] = "MANUAL"

report = pd.DataFrame(checks)
print(report[["butir", "jenis", "status", "rincian"]].to_string(index=False))
print("Ringkasan:", report["status"].value_counts().to_dict())
# --8<-- [end:checklist]

# --8<-- [start:outline]
def block(title, body):
    return f"## {title}\n\n{body}\n"


todo = "[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]"
lines = [f"# {final_title}\n", "## Abstrak\n"]
for key, value in abstract.items():
    lines.append(f"**{key}.** {value}\n")
lines.append(f"*Kata abstrak: {words(abstract_text)}.*\n")
for _, row in section_map.iterrows():
    if row["bagian"] == "Ketersediaan data dan kode":
        continue
    lines.append(block(row["bagian"], f"Sumber: {row['sumber_dari_proyek']}. Isi utama: {row['isi_utama']}. Saran panjang: {row['saran_kata']} kata.\n\n{todo}"))
lines.append(block("Tabel konfigurasi eksperimen (untuk bagian Metode)", "| Algoritma | Pengaturan | Disetel |\n|---|---|---|\n" + "\n".join(f"| {r.Algoritma} | {r.Pengaturan} | {r.Disetel} |" for r in config_table.itertuples())))
lines.append(block("Daftar tabel dan gambar", "\n".join(f"- **{a['id']}** ({a['file']}): {a['caption']}" for a in assets)))
lines.append(block("Ketersediaan data dan kode", data_statement))
lines.append(block("Pernyataan etik", ethics_statement))
lines.append(block("Referensi", "\n".join(f"- {r.referensi}. {r.tautan} (dibaca: {r.dibaca})" for r in literature.itertuples())))
outline = "\n".join(lines)
RESULTS.mkdir(exist_ok=True)
(RESULTS / "08_manuscript_outline.md").write_text(outline, encoding="utf-8")
report.to_csv(RESULTS / "08_writing_checklist.csv", index=False, encoding="utf-8")
section_map.to_csv(RESULTS / "08_section_map.csv", index=False, encoding="utf-8")
print("Kerangka naskah:", len(outline.split()), "kata |", outline.count("[TODO penulis"), "bagian menunggu prosa penulis")
print("Berkas hasil disimpan di examples/level-7/results/ (awalan 08_)")
# --8<-- [end:outline]
