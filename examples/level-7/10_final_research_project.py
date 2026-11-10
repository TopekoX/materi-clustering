"""Level 7, Bab 10: Proyek penelitian clustering akhir.

Menyatukan seluruh tahap (Bab 1-9) menjadi satu laporan proyek dengan 17 bagian. Setiap bagian diberi
label status isi (TEMUAN EKSPERIMEN, ILUSTRASI DIDAKTIK, EKSPLORATORI, dst.) dan dirakit dari berkas hasil,
bukan diketik ulang. Skrip juga:
  - melengkapi tinjauan pustaka untuk RQ2 (dua sumber baru, hanya dari ringkasan hasil pencarian),
  - menjalankan satu uji eksploratori lanjutan untuk dugaan "dominasi fitur berskala besar" dari Bab 7,
  - menjalankan QA akhir.

Skrip TIDAK menjalankan ulang eksperimen utama (Bab 6) dan TIDAK mengubah protokol terkunci.

Jalankan dari folder utama proyek (setelah skrip Bab 2 sampai 9):
    python examples/level-7/10_final_research_project.py
"""
# NB: setup=Siapkan alat dan periksa protokol terkunci | literature=Melengkapi tinjauan pustaka untuk RQ2 | followup=Uji eksploratori lanjutan | statusmap=Peta status isi | facts=Fakta yang boleh dikutip | report=Menyusun laporan proyek 17 bagian | qa=QA akhir | save=Menyimpan laporan dan hasil QA

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
import re

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import _research as rs

RESULTS = rs.RESULTS_DIR
FIGURES = ROOT / "docs" / "assets" / "level-7"
LEVEL_DIR = ROOT / "examples" / "level-7"
SEED = 42

protocol = json.loads((RESULTS / "05_protocol.json").read_text(encoding="utf-8"))
locked = (RESULTS / "05_protocol.sha256").read_text(encoding="utf-8").strip()
if hashlib.sha256(json.dumps(protocol, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest() != locked:
    raise SystemExit("Protokol berubah sejak dikunci. Laporan akhir tidak disusun.")
problem = json.loads((RESULTS / "02_research_problem.json").read_text(encoding="utf-8"))
card = json.loads((RESULTS / "04_dataset_card.json").read_text(encoding="utf-8"))
manifest = json.loads((RESULTS / "06_run_manifest.json").read_text(encoding="utf-8"))
clarifications = json.loads((RESULTS / "06_clarifications.json").read_text(encoding="utf-8"))
facts = json.loads((RESULTS / "07_facts.json").read_text(encoding="utf-8"))
ledger = pd.read_csv(RESULTS / "07_claim_ledger.csv").set_index("id")
literature = pd.read_csv(RESULTS / "03_literature_matrix.csv", index_col="id")
by_measure = pd.read_csv(RESULTS / "07_profile_by_measure.csv", index_col=0).iloc[:, 0]
package_check = pd.read_csv(RESULTS / "09_package_checklist.csv")
checksum_count = len(pd.read_csv(RESULTS / "09_checksums.csv"))
outline_title = (RESULTS / "08_manuscript_outline.md").read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()


def fmt(value, digits=3):
    return f"{value:.{digits}f}".replace(".", ",")


def words(text):
    return len(re.findall(r"\w+", text, flags=re.UNICODE))


print("Protokol terkunci terverifikasi:", locked[:16], "| eksekusi Bab 6:", manifest["eksekusi_dijalankan"], "dari", manifest["eksekusi_direncanakan"])
# --8<-- [end:setup]

# --8<-- [start:literature]
# Dua sumber baru untuk RQ2. Hanya informasi dari ringkasan hasil pencarian; teks lengkap TIDAK dibaca.
NA = "—"
new_rows = pd.DataFrame(
    [
        {
            "referensi": "Milligan & Cooper (1988)",
            "tujuan": "Mengkaji standardisasi variabel dalam analisis klaster lewat studi simulasi",
            "dataset": "Data simulasi dengan variasi jarak antar-klaster dan skala variabel",
            "praproses": "Beberapa cara standardisasi variabel",
            "algoritma": NA, "metrik": NA, "temuan": NA, "keterbatasan": NA,
            "celah_potensial": "Inferensi penulis bab: pengaruh standardisasi perlu diperiksa pada data nyata",
            "topik": "sensitivitas-praproses", "dibaca": "ringkasan hasil pencarian",
            "tautan": "https://doi.org/10.1007/BF01897163",
        },
        {
            "referensi": "Steinley (2004)",
            "tujuan": "Mengkaji beberapa cara standardisasi pada K-Means di berbagai kondisi",
            "dataset": NA,
            "praproses": "Beberapa cara standardisasi, termasuk z-score",
            "algoritma": "K-Means", "metrik": NA,
            "temuan": "Menurut ringkasan abstrak, z-score kurang baik dibanding cara standardisasi lain pada studi itu",
            "keterbatasan": NA,
            "celah_potensial": "Inferensi penulis bab: belum diketahui apakah pola itu muncul pada dataset ini",
            "topik": "sensitivitas-praproses", "dibaca": "ringkasan hasil pencarian",
            "tautan": "https://doi.org/10.1007/978-3-642-17103-1_6",
        },
    ],
    index=["L6", "L7"],
)
new_rows.index.name = "id"
final_literature = pd.concat([literature, new_rows])
needs = {"RQ1": "kestabilan", "RQ2": "sensitivitas-praproses", "RQ3": "pembanding-partisi"}
coverage = {rq: int((final_literature["topik"] == topic).sum()) for rq, topic in needs.items()}
read_full = int((final_literature["dibaca"] == "teks lengkap").sum())
print("Sumber pada matriks akhir:", len(final_literature), "| dibaca penuh:", read_full)
print("Cakupan pustaka per pertanyaan:", coverage)
final_gap = (
    f"Dari {len(final_literature)} sumber yang ditelaah berdasarkan abstrak atau ringkasan, tidak satu pun yang kami baca "
    "menyajikan protokol terpadu yang mengukur kestabilan, kepekaan terhadap praproses, dan keselarasan eksternal "
    "pada satu dataset publik dengan seluruh konfigurasi dibagikan. Ini bukan klaim bahwa studi serupa tidak ada; "
    "tinjauan ini terarah, bukan sistematis."
)
# --8<-- [end:literature]

# --8<-- [start:followup]
# EKSPLORATORI (tidak ada di protokol): menguji dugaan Bab 7 bahwa K-Means tanpa skala didominasi fitur berskala besar.
X_df, y = rs.load_wdbc()
Xr = X_df.to_numpy(dtype=float)
kmeans = lambda data: KMeans(n_clusters=2, n_init=10, random_state=SEED).fit_predict(data)
raw_all = kmeans(Xr)
by_worst_area = kmeans(X_df[["worst area"]].to_numpy())
by_two_areas = kmeans(X_df[["worst area", "mean area"]].to_numpy())
without_two = kmeans(X_df.drop(columns=["worst area", "mean area"]).to_numpy())
followup = {
    "ari_raw_vs_worst_area_saja": adjusted_rand_score(raw_all, by_worst_area),
    "ari_raw_vs_dua_fitur_area": adjusted_rand_score(raw_all, by_two_areas),
    "ari_raw_vs_tanpa_dua_fitur_area": adjusted_rand_score(raw_all, without_two),
}
for key, value in followup.items():
    print(f"{key:34s}: {fmt(value)}")
print("Ukuran kelompok K-Means tanpa skala:", np.bincount(raw_all).tolist(), "| tanpa dua fitur area:", np.bincount(without_two).tolist())
# --8<-- [end:followup]

# --8<-- [start:statusmap]
status_items = [
    ["Demonstrasi tiga pertanyaan riset pada data yang sama", "Bab 1", "ILUSTRASI DIDAKTIK", "outputs/01.txt"],
    ["Contoh pertanyaan baik dan buruk, pemeriksa kata kunci", "Bab 2", "ILUSTRASI DIDAKTIK", "outputs/02.txt"],
    ["Matriks pustaka (abstrak atau ringkasan)", "Bab 3 dan 10", "TINJAUAN PUSTAKA TERBATAS", "results/03_literature_matrix.csv"],
    ["Kartu data, kriteria, etika", "Bab 4", "DOKUMENTASI", "results/04_dataset_card.json"],
    ["Protokol terkunci (156 eksekusi)", "Bab 5", "RENCANA DAN PROTOKOL", "results/05_protocol.json"],
    ["RQ1 kestabilan", "Bab 6", "TEMUAN EKSPERIMEN", "results/06_rq1_summary.json"],
    ["RQ2 kepekaan skala", "Bab 6", "TEMUAN EKSPERIMEN", "results/06_rq2_scaling.csv"],
    ["RQ3 perbandingan algoritma dan validasi", "Bab 6", "TEMUAN EKSPERIMEN", "results/06_rq3_algorithms.csv"],
    ["Sensitivitas K dan grid DBSCAN", "Bab 6", "TEMUAN EKSPERIMEN", "results/06_k_sensitivity.csv"],
    ["Profil kelompok", "Bab 6", "TEMUAN EKSPERIMEN", "results/06_cluster_profile.csv"],
    ["Bootstrap ARI", "Bab 7", "EKSPLORATORI", "results/07_bootstrap_ari.csv"],
    ["Pangsa varians fitur", "Bab 7", "EKSPLORATORI", "results/07_facts.json"],
    ["Uji dominasi fitur berskala besar", "Bab 10", "EKSPLORATORI", "10_final_research_project.py"],
    ["Kerangka naskah dan daftar periksa penulisan", "Bab 8", "DOKUMENTASI", "results/08_manuscript_outline.md"],
    ["Paket reproduksi dan uji keterulangan", "Bab 9", "DOKUMENTASI", "results/09_package_checklist.csv"],
]
status_map = pd.DataFrame(status_items, columns=["isi", "bab", "label", "sumber"])
status_map["sumber_ada"] = [(LEVEL_DIR / s).exists() for s in status_map["sumber"]]
print(status_map["label"].value_counts().to_string())
print("Sumber yang belum ada:", status_map.loc[~status_map["sumber_ada"], "isi"].tolist() or "tidak ada")
# --8<-- [end:statusmap]

# --8<-- [start:facts]
facts_all = dict(facts)
facts_all.update({k: float(v) for k, v in followup.items()})
facts_all.update({"measure_1": float(by_measure.iloc[0]), "measure_2": float(by_measure.iloc[1]), "measure_3": float(by_measure.iloc[2]), "measure_last": float(by_measure.iloc[-1])})
pool = {fmt(float(v), d) for v in facts_all.values() for d in (1, 2, 3)}
F = lambda key, d=3: fmt(float(facts_all[key]), d)
OVERCLAIM = ["membuktikan", "terbukti", "pasti", "menyebabkan", "tidak diragukan", "selalu", "mengonfirmasi", "terbaik", "revolusioner", "sempurna"]


def overclaim_words(text):
    low = text.lower()
    found = []
    for word in OVERCLAIM:
        for match in re.finditer(r"\b" + word + r"\b", low):
            window = low[max(0, match.start() - 12):match.start()]
            if "tidak " not in window and "bukan " not in window:
                found.append(word)
                break
    return found


def untraceable_numbers(text):
    return [x for x in re.findall(r"-?\d+,\d+", text) if x not in pool and x not in {"0,95", "0,9"}]


print("Fakta yang boleh dikutip:", len(facts_all), "| bentuk angka sah:", len(pool))
# --8<-- [end:facts]

# --8<-- [start:report]
sections = []


def sec(title, label, sources, body):
    sections.append({"no": len(sections) + 1, "judul": title, "label": label, "sumber": sources, "isi": body.strip()})


def bullets(items):
    return "\n".join(f"- {x}" for x in items)


def md_table(frame):
    header = "| " + " | ".join(frame.columns) + " |"
    divider = "|" + "|".join("---" for _ in frame.columns) + "|"
    rows = ["| " + " | ".join(str(v).replace("|", "/") for v in row) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, divider, *rows])


led = lambda kind: [f"({i}) {r.kalimat}" for i, r in ledger.iterrows() if r.jenis == kind]

sec("Judul penelitian", "DOKUMENTASI", "08_manuscript_outline.md", outline_title)
sec("Latar belakang dan masalah penelitian", "RENCANA DAN PROTOKOL", "02_research_problem.json", f"{problem['masalah']}\n\nKontribusi yang dinyatakan: {problem['kontribusi']}")
sec("Tujuan dan pertanyaan penelitian", "RENCANA DAN PROTOKOL", "02_research_problem.json", "Tujuan:\n" + bullets(problem["tujuan"]) + "\n\nPertanyaan:\n" + bullets(f"{k}: {v}" for k, v in problem["pertanyaan"].items()))
sec("Matriks tinjauan pustaka", "TINJAUAN PUSTAKA TERBATAS", "03_literature_matrix.csv; Bab 10", md_table(final_literature.reset_index()[["id", "referensi", "topik", "dibaca"]]) + f"\n\nDibaca penuh: {read_full} dari {len(final_literature)}. Cakupan per pertanyaan: {coverage}.")
sec("Celah riset dan kontribusi", "TINJAUAN PUSTAKA TERBATAS", "Bab 3 dan 10", f"{final_gap}\n\nKontribusi: {problem['kontribusi']}")
sec("Pemilihan dan deskripsi dataset", "DOKUMENTASI", "04_dataset_card.json", bullets([f"Dataset: {card['nama']} ({card['jumlah_sampel_final']} sampel, 30 fitur)", f"Sumber: {card['sumber_asli'].split(', ')[0]}, DOI {card['doi']}, lisensi CC BY 4.0 menurut halaman UCI", f"Baris dikeluarkan oleh kriteria: {card['baris_dikeluarkan']}", f"Sidik jari data final: {card['sidik_jari_data_final']}", "Persetujuan etik dan de-identifikasi: tidak dinyatakan pada sumber yang dibaca; tidak ada klaim klinis"]))
sec("Metodologi penelitian", "RENCANA DAN PROTOKOL", "05_protocol.json", bullets([f"{k}: faktor {v['faktor']}" for k, v in protocol["analisis"].items()]) + f"\n\nProtokol dikunci sebelum eksperimen (SHA-256 {locked[:16]}...). Pengungkapan:\n" + bullets(protocol["pengungkapan"]))
sec("Praproses data", "RENCANA DAN PROTOKOL", "05_protocol.json; 06_clarifications.json", bullets(f"{k}: {v}" for k, v in protocol["praproses"].items()) + "\n- " + [c for c in clarifications if c["id"] == "C3"][0]["keputusan"])
cfg = pd.DataFrame([[n, "; ".join(f"{k}={v}" for k, v in p.items() if k not in ("disetel", "aturan_seleksi", "jika_tak_ada_yang_valid")), "ya" if p["disetel"] else "tidak"] for n, p in protocol["algoritma"].items()], columns=["Algoritma", "Pengaturan", "Disetel"])
sec("Implementasi clustering", "RENCANA DAN PROTOKOL", "05_protocol.json; 06_run_manifest.json", md_table(cfg) + f"\n\nEksekusi dijalankan: {manifest['eksekusi_dijalankan']} dari {manifest['eksekusi_direncanakan']} ({manifest['rincian']}). Klarifikasi implementasi: {len(clarifications)}.")
sec("Desain eksperimen", "RENCANA DAN PROTOKOL", "05_protocol.json", bullets(f"{k}: faktor {v['faktor']}; metrik {', '.join(v['metrik'])}" for k, v in protocol["analisis"].items()) + f"\n\nAmbang praktis sama (ARI): {fmt(protocol['aturan_keputusan']['ambang_praktis_sama_ARI'], 2)}, ditetapkan sebelum eksperimen.")
sec("Evaluasi", "RENCANA DAN PROTOKOL", "05_protocol.json", "Metrik internal (Silhouette naik lebih baik, Davies-Bouldin turun lebih baik, Calinski-Harabasz naik lebih baik) dihitung di ruang baseline. ARI dan NMI terhadap diagnosis dipakai hanya sebagai validasi eksternal, bukan target optimasi.")
figs = ["06-kestabilan-dan-skala.png", "06-empat-algoritma.png", "06-sensitivitas-k-dan-dbscan.png", "07-ari-dan-ketidakpastian.png"]
sec("Visualisasi hasil", "TEMUAN EKSPERIMEN", "docs/assets/level-7/", bullets(f"{n} (ada: {(FIGURES / n).exists()})" for n in figs))
sec("Profil kelompok", "TEMUAN EKSPERIMEN", "06_cluster_profile.csv; 07_profile_by_measure.csv", f"{ledger.loc['H6', 'kalimat']}\n\nUkuran inti sel yang paling berbeda antar kelompok: {by_measure.index[0]} ({F('measure_1', 2)}), {by_measure.index[1]} ({F('measure_2', 2)}), {by_measure.index[2]} ({F('measure_3', 2)}); paling mirip: {by_measure.index[-1]} ({F('measure_last', 2)}). Ini deskripsi, bukan penjelasan sebab.")
extra_discussion = (
    "(P5, Bab 10) Hasil RQ2 sejalan dengan gagasan bahwa pilihan cara standardisasi memengaruhi pengelompokan (Milligan & Cooper, 1988; Steinley, 2004; "
    "berdasarkan ringkasan hasil pencarian, bukan teks lengkap). Kami tidak menilai cara standardisasi mana yang lebih baik, karena tidak ada kebenaran dasar pada clustering."
)
followup_text = (
    f"(Eksploratori, Bab 10) Uji langsung dugaan I4. Pada K-Means tanpa skala, ARI terhadap pengelompokan yang hanya memakai worst area adalah {F('ari_raw_vs_worst_area_saja')}, "
    f"terhadap dua fitur area {F('ari_raw_vs_dua_fitur_area')}, dan terhadap pengelompokan tanpa kedua fitur area {F('ari_raw_vs_tanpa_dua_fitur_area')}. "
    "Pada dataset ini pengelompokan tanpa skala tampak ditentukan oleh worst area, sehingga dugaan I4 didukung; ini tidak menunjukkan hal yang sama pada data lain."
)
sec("Hasil dan pembahasan", "TEMUAN EKSPERIMEN", "07_claim_ledger.csv; Bab 10", "Hasil:\n" + bullets(led("hasil")) + "\n\nInterpretasi:\n" + bullets(led("interpretasi")) + "\n\nPembahasan terhadap penelitian terdahulu:\n" + bullets(led("pembahasan") + [extra_discussion]) + "\n\nUji lanjutan:\n- " + followup_text)
ari_values = [facts_all["km_ari"], facts_all["ag_ari"], facts_all["gm_ari"]]
conclusion = [
    f"RQ1: pada dataset ini K-Means (K = 2, data terstandarisasi) tampak konsisten terhadap seed (ARI rata-rata {F('seed_mean')}) dan subsampel ({F('sub_mean')}; minimum {F('sub_min')}).",
    f"RQ2: cara menyamakan skala mengubah pengelompokan; ARI terhadap baseline {F('std_none')} tanpa skala dan {F('std_minmax')} dengan MinMaxScaler, di bawah ambang {F('threshold', 2)}.",
    f"RQ3: pengelompokan cukup selaras dengan diagnosis (ARI {fmt(min(ari_values))} sampai {fmt(max(ari_values))}), peringkat algoritma berbeda antar jenis metrik, selisih ARI antar-algoritma tidak jelas melampaui ketidakpastian sampel (eksploratori), dan DBSCAN tidak memiliki konfigurasi valid.",
]
sec("Kesimpulan penelitian", "TEMUAN EKSPERIMEN", "Bab 6 dan 7", bullets(conclusion))
future = pd.DataFrame(
    [
        ["Uji dugaan kepadatan seragam pada DBSCAN", "Bandingkan sebaran jarak tetangga terdekat; coba kerangka grid yang ditetapkan lewat amendment"],
        ["Baca teks lengkap ketujuh sumber", "Isi kolom keterbatasan dan perbarui pembahasan pustaka"],
        ["Uji pada dataset lain (replicability)", "Terapkan protokol yang sama pada dataset berlisensi jelas"],
        ["Seleksi fitur untuk mengurangi redundansi", "Bandingkan dengan seluruh fitur memakai ARI antar-pengelompokan"],
        ["Tinjauan pustaka sistematis", "Tetapkan kueri dan kriteria inklusi lebih dulu, lalu laporkan alur seleksi"],
    ],
    columns=["Pekerjaan lanjutan", "Cara mengujinya"],
)
sec("Keterbatasan dan pekerjaan lanjutan", "KETERBATASAN DAN RENCANA LANJUTAN", "07_claim_ledger.csv", "Keterbatasan:\n" + bullets(led("keterbatasan")) + "\n\nPekerjaan lanjutan:\n" + md_table(future))
pk = package_check["status"].value_counts().to_dict()
sec("Dokumentasi reproduksibilitas", "DOKUMENTASI", "09_package_checklist.csv; 09_repro_package/", f"Paket reproduksi: 6 berkas di results/09_repro_package/. Daftar periksa Bab 9: {pk}. Uji keterulangan: skrip Bab 1 sampai 8 diulang dan {checksum_count} berkas dibandingkan (lihat output Bab 9). Peringatan yang tersisa: kode belum di-commit dan tautan repositori belum ditentukan.")
print("Bagian laporan:", len(sections))
for s in sections:
    print(f"{s['no']:2d}. {s['judul']:40s} [{s['label']}] {words(s['isi'])} kata")
# --8<-- [end:report]

# --8<-- [start:qa]
all_text = "\n".join(s["isi"] for s in sections)
qa = []


def check(name, ok, detail, warn_only=False):
    qa.append({"butir": name, "status": "LULUS" if ok else ("PERINGATAN" if warn_only else "GAGAL"), "rincian": detail})


required_titles = ["Judul", "Latar belakang", "Tujuan", "Matriks", "Celah", "dataset", "Metodologi", "Praproses", "Implementasi", "Desain", "Evaluasi", "Visualisasi", "Profil", "Hasil", "Kesimpulan", "Keterbatasan", "reproduksibilitas"]
check("Ketujuh belas bagian ada dan tidak kosong", len(sections) == 17 and all(words(s["isi"]) > 0 for s in sections), f"{len(sections)} bagian")
check("Setiap bagian punya label status isi", all(s["label"] for s in sections), "label lengkap")
check("Angka di laporan terlacak ke fakta", not untraceable_numbers(all_text), f"tak terlacak: {untraceable_numbers(all_text)}")
check("Tanpa kata berlebihan", not overclaim_words(all_text), f"ditemukan: {overclaim_words(all_text)}")
check("Hash protokol cocok dan tidak ada amendment", len(protocol["amendments"]) == 0, f"{len(protocol['amendments'])} amendment")
check("Eksekusi dijalankan sama dengan direncanakan", manifest["eksekusi_dijalankan"] == manifest["eksekusi_direncanakan"], f"{manifest['eksekusi_dijalankan']} dari {manifest['eksekusi_direncanakan']}")
check("Semua sumber pada peta status ada", bool(status_map["sumber_ada"].all()), f"{int(status_map['sumber_ada'].sum())} dari {len(status_map)}")
check("Semua gambar laporan ada", all((FIGURES / n).exists() for n in figs), f"{len(figs)} gambar")
check("Analisis eksploratori diberi label", "(Eksploratori" in all_text, "label terdeteksi di bagian hasil")
check("Setiap pertanyaan punya pustaka pendukung", all(v >= 1 for v in coverage.values()), f"cakupan {coverage}")
check("Ilustrasi didaktik terpisah dari temuan", set(status_map["label"]) >= {"ILUSTRASI DIDAKTIK", "TEMUAN EKSPERIMEN", "EKSPLORATORI"}, "tiga label hadir")
check("Sumber pustaka dibaca penuh", read_full == len(final_literature), f"{read_full} dari {len(final_literature)}", warn_only=True)
check("Paket reproduksi: tanpa peringatan", (package_check["status"] != "PERINGATAN").all(), f"status Bab 9: {pk}", warn_only=True)
qa_df = pd.DataFrame(qa)
print(qa_df.to_string(index=False))
print("Ringkasan QA:", qa_df["status"].value_counts().to_dict())
# --8<-- [end:qa]

# --8<-- [start:save]
parts = [f"# {outline_title}\n", "*Laporan proyek akhir Level 7 (17 bagian). Setiap bagian diberi label status isi.*\n"]
for s in sections:
    parts.append(f"## {s['no']}. {s['judul']}\n\n*Status isi: {s['label']}. Sumber: {s['sumber']}.*\n\n{s['isi']}\n")
parts.append("## Peta status isi\n\n" + md_table(status_map[["isi", "bab", "label"]]) + "\n")
report_text = "\n".join(parts)
RESULTS.mkdir(exist_ok=True)
(RESULTS / "10_final_report.md").write_text(report_text, encoding="utf-8")
final_literature.to_csv(RESULTS / "10_literature_matrix_final.csv", encoding="utf-8")
(RESULTS / "10_gap_statement_final.json").write_text(json.dumps({"pernyataan_celah": final_gap, "jumlah_sumber": len(final_literature), "cakupan": coverage, "dibaca_penuh": read_full}, indent=2, ensure_ascii=False), encoding="utf-8")
(RESULTS / "10_followup_variance.json").write_text(json.dumps({k: float(v) for k, v in followup.items()}, indent=2), encoding="utf-8")
pd.DataFrame(sections)[["no", "judul", "label", "sumber"]].to_csv(RESULTS / "10_section_status.csv", index=False, encoding="utf-8")
status_map.to_csv(RESULTS / "10_status_map.csv", index=False, encoding="utf-8")
qa_df.to_csv(RESULTS / "10_final_qa.csv", index=False, encoding="utf-8")
print("Laporan akhir:", words(report_text), "kata,", len(sections), "bagian")
print("Berkas hasil disimpan di examples/level-7/results/ (awalan 10_)")
# --8<-- [end:save]
