"""Level 7, Bab 9: Reproduksibilitas dan dokumentasi penelitian.

Membangun dan MEMERIKSA paket reproduksi untuk proyek Level 7: struktur proyek, audit seed (AST),
dependensi yang benar-benar dipakai, urutan eksekusi dari ketergantungan berkas, log keputusan, checksum,
uji keterulangan (menjalankan ulang skrip Bab 1-8 dan membandingkan hasil), status Git (hanya dibaca),
dan penulisan berkas paket.

Uji keterulangan menjalankan ulang skrip Bab 1 sampai 8 (sekitar dua menit). Matikan dengan
variabel lingkungan RERUN=0.

Jalankan dari folder utama proyek (setelah skrip Bab 2 sampai 8):
    python examples/level-7/09_reproducibility_and_documentation.py
"""
# NB: setup=Siapkan alat dan daftar skrip | layout=Struktur proyek yang disarankan | seeds=Audit seed dengan AST | deps=Dependensi yang benar-benar dipakai | order=Urutan eksekusi dari ketergantungan berkas | decisions=Log keputusan | checksums=Checksum berkas | rerun=Uji keterulangan | git=Status versi kode | package=Menulis paket reproduksi | checklist=Daftar periksa paket

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

# --8<-- [start:setup]
import ast
import hashlib
import json
import re
import subprocess
import time
from importlib import metadata

import pandas as pd

import _research as rs

LEVEL_DIR = ROOT / "examples" / "level-7"
RESULTS = rs.RESULTS_DIR
FIGURES = ROOT / "docs" / "assets" / "level-7"
PACKAGE = RESULTS / "09_repro_package"
scripts = sorted(p for p in LEVEL_DIR.glob("[0-9][0-9]_*.py") if not p.name.startswith("09_"))
print("Skrip bab yang diperiksa:", [p.name[:2] for p in scripts])


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
# --8<-- [end:setup]

# --8<-- [start:layout]
layout = pd.DataFrame(
    [
        ["README.md", "Pintu masuk: tujuan, cara menjalankan, status", "docs/research-project/index.md", ROOT / "docs" / "research-project" / "index.md"],
        ["requirements.txt (+ kunci versi)", "Versi pustaka yang dipakai", "requirements-notebooks.txt (kunci versi ditulis di paket)", ROOT / "requirements-notebooks.txt"],
        ["data/ (+ kartu data)", "Data beku dan dokumentasinya", "results/04_research_dataset.csv, 04_dataset_card.json", RESULTS / "04_dataset_card.json"],
        ["protocol/", "Protokol terkunci dan hash", "results/05_protocol.json, 05_protocol.sha256", RESULTS / "05_protocol.sha256"],
        ["src/ (modul bersama)", "Kode yang dipakai ulang", "examples/level-7/_research.py", LEVEL_DIR / "_research.py"],
        ["scripts/", "Alur yang bisa dijalankan berurutan", "examples/level-7/NN_*.py", LEVEL_DIR / "01_introduction_to_clustering_research.py"],
        ["notebooks/", "Eksplorasi dan penjelasan interaktif", "notebooks/level-7/", ROOT / "notebooks" / "level-7"],
        ["results/", "Tabel dan ringkasan hasil", "examples/level-7/results/", RESULTS],
        ["figures/", "Gambar yang dihasilkan skrip", "docs/assets/level-7/", FIGURES],
        ["logs/ (keputusan, pencarian)", "Catatan proses", "results/03_search_log.csv, 06_clarifications.json", RESULTS / "06_clarifications.json"],
    ],
    columns=["direktori_berkas", "fungsi", "di_proyek_ini", "path"],
)
layout["ada"] = [Path(p).exists() for p in layout["path"]]
print(layout[["direktori_berkas", "di_proyek_ini", "ada"]].to_string(index=False))
# --8<-- [end:layout]

# --8<-- [start:seeds]
STOCHASTIC = {"KMeans", "GaussianMixture", "PCA"}


def audit_seeds(source, filename="<kode>"):
    """Setiap pemanggilan yang acak harus menyebut seed. Mengembalikan (jumlah diperiksa, daftar pelanggaran)."""
    tree = ast.parse(source)
    checked, issues = 0, []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else None
        if name in STOCHASTIC:
            checked += 1
            if "random_state" not in {k.arg for k in node.keywords}:
                issues.append((filename, node.lineno, name))
        elif name == "default_rng":
            checked += 1
            if not node.args and not node.keywords:
                issues.append((filename, node.lineno, name))
    return checked, issues


total_checked, all_issues = 0, []
for path in scripts + [LEVEL_DIR / "09_reproducibility_and_documentation.py"]:
    checked, issues = audit_seeds(path.read_text(encoding="utf-8"), path.name)
    total_checked += checked
    all_issues += issues
print("Pemanggilan acak diperiksa:", total_checked, "| tanpa seed:", all_issues if all_issues else "tidak ada")

demo_source = "from sklearn.cluster import KMeans\nmodel = KMeans(n_clusters=2, n_init=10)\n"
print("Demo kode tanpa seed:", audit_seeds(demo_source, "demo.py"))
# --8<-- [end:seeds]

# --8<-- [start:deps]
STANDARD = set(sys.stdlib_module_names)
DISTRIBUTION = {"numpy": "numpy", "pandas": "pandas", "sklearn": "scikit-learn", "matplotlib": "matplotlib", "scipy": "scipy"}
local_modules = {p.stem for p in LEVEL_DIR.glob("_*.py")}
imported = set()
for path in scripts + [LEVEL_DIR / "09_reproducibility_and_documentation.py"] + sorted(LEVEL_DIR.glob("_*.py")):
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module.split(".")[0])
third_party = sorted(m for m in imported if m not in STANDARD and m not in local_modules)
unknown = [m for m in third_party if m not in DISTRIBUTION]
lock_lines = [f"{DISTRIBUTION[m]}=={metadata.version(DISTRIBUTION[m])}" for m in third_party if m in DISTRIBUTION]
print("Modul pihak ketiga yang diimpor:", third_party)
print("Tidak dikenali (perlu dipetakan):", unknown if unknown else "tidak ada")
print("Kunci versi:", lock_lines)
# --8<-- [end:deps]

# --8<-- [start:order]
pattern = re.compile(r"\b(\d\d)_[A-Za-z0-9_]+\.(?:json|csv|md|sha256|txt)")
rows = []
for path in scripts + [LEVEL_DIR / "09_reproducibility_and_documentation.py"]:
    own = path.name[:2]
    prefixes = sorted({m for m in pattern.findall(path.read_text(encoding="utf-8")) if m != own})
    forward = [m for m in prefixes if int(m) > int(own)]
    rows.append({"skrip": path.name[:2], "membaca_hasil_bab": ", ".join(prefixes) if prefixes else "-", "ketergantungan_ke_depan": forward})
order = pd.DataFrame(rows)
print(order.to_string(index=False))
print("Urutan eksekusi:", " -> ".join(order["skrip"]), "| ada ketergantungan ke depan:", bool(order["ketergantungan_ke_depan"].map(bool).any()))
# --8<-- [end:order]

# --8<-- [start:decisions]
problem = json.loads((RESULTS / "02_research_problem.json").read_text(encoding="utf-8"))
card = json.loads((RESULTS / "04_dataset_card.json").read_text(encoding="utf-8"))
protocol = json.loads((RESULTS / "05_protocol.json").read_text(encoding="utf-8"))
clar = json.loads((RESULTS / "06_clarifications.json").read_text(encoding="utf-8"))
entries = []
for criterion in card["kriteria"]:
    entries.append(["Bab 4", f"Kriteria data: {criterion}", "ditulis sebelum diterapkan", "dikunci", "04_dataset_card.json"])
for key, value in protocol["praproses"].items():
    entries.append(["Bab 5", f"Praproses {key}: {value}", "ditetapkan di protokol", "dikunci", "05_protocol.json"])
for key, value in protocol["kebijakan_hyperparameter"].items():
    entries.append(["Bab 5", f"Kebijakan {key}: {value}", "ditetapkan di protokol", "dikunci", "05_protocol.json"])
for item in protocol["pengungkapan"]:
    entries.append(["Bab 5", item, "pengungkapan hal yang sudah dilihat", "pengungkapan", "05_protocol.json"])
for c in clar:
    entries.append(["Bab 6", f"{c['id']}: {c['keputusan']}", c["alasan"], "klarifikasi", "06_clarifications.json"])
entries.append(["Bab 8", "Kalimat masalah di Bab 2 diubah dari 'selalu menghasilkan kelompok' menjadi 'berbasis partisi menghasilkan kelompok pada data apa pun'", "pemeriksa kata berlebihan menandainya dan DBSCAN tidak menghasilkan kelompok (Bab 6); hash protokol tidak berubah", "revisi", "02_research_problem.json"])
decisions = pd.DataFrame(entries, columns=["tahap", "keputusan", "alasan", "jenis", "sumber"])
decisions.insert(0, "id", [f"D{i + 1}" for i in range(len(decisions))])
print("Jumlah keputusan tercatat:", len(decisions))
print(decisions["jenis"].value_counts().to_string())
print("Amendment pada protokol:", len(protocol["amendments"]))
# --8<-- [end:decisions]

# --8<-- [start:checksums]
tracked = (
    scripts
    + sorted(LEVEL_DIR.glob("_*.py"))
    + sorted(p for p in RESULTS.glob("*") if p.is_file() and not p.name.startswith("09_"))
    + sorted(p for p in (LEVEL_DIR / "outputs").glob("*.txt") if not p.name.startswith("09"))   # keluaran skrip ini sendiri sedang ditulis
    + sorted(FIGURES.glob("*.png"))
)
checksums = pd.DataFrame(
    [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256_of(p)} for p in tracked]
)
print("Berkas dengan checksum:", len(checksums), "| total byte:", int(checksums["bytes"].sum()))
print(checksums.head(3).to_string(index=False))
# --8<-- [end:checksums]

# --8<-- [start:rerun]
RERUN = os.environ.get("RERUN", "1") == "1"
rerun_rows = []
changed_files = []
if RERUN:
    before = {c.path: c.sha256 for c in checksums.itertuples()}
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    for path in scripts:
        start = time.perf_counter()
        done = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, encoding="utf-8", env=env, cwd=ROOT)
        seconds = time.perf_counter() - start
        saved = (LEVEL_DIR / "outputs" / f"{path.name[:2]}.txt").read_text(encoding="utf-8").splitlines()
        now = done.stdout.splitlines()
        differing = [i for i in range(max(len(saved), len(now))) if (saved[i] if i < len(saved) else None) != (now[i] if i < len(now) else None)]
        rerun_rows.append({"skrip": path.name[:2], "kode_keluar": done.returncode, "detik": round(seconds, 1), "baris_output_berbeda": len(differing)})
    for c in checksums.itertuples():
        if sha256_of(ROOT / c.path) != before[c.path]:
            changed_files.append(c.path)
    print(pd.DataFrame(rerun_rows).to_string(index=False))
    print("Berkas dibandingkan:", len(before), "| berkas yang berubah setelah dijalankan ulang:", changed_files if changed_files else "tidak ada")
else:
    print("Uji keterulangan dilewati (RERUN=0)")
# --8<-- [end:rerun]

# --8<-- [start:git]
def git(*args):
    """Hanya perintah BACA. Mengembalikan None bila Git tidak terpasang atau perintah gagal."""
    try:
        done = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
    except FileNotFoundError:
        return None
    return done.stdout.strip() if done.returncode == 0 else None


head = git("rev-parse", "--short", "HEAD")
level_paths = ["examples/level-7", "docs/research-project", "notebooks/level-7", "docs/assets/level-7"]
status = git("status", "--porcelain", "--untracked-files=all", "--", *level_paths)
uncommitted = len(status.splitlines()) if status else 0
print("Commit HEAD       :", head)
print("Berkas Level 7 yang belum di-commit:", uncommitted)
print("Paket reproduksi dapat menunjuk satu commit:", uncommitted == 0 and head is not None)
# --8<-- [end:git]

# --8<-- [start:package]
PACKAGE.mkdir(parents=True, exist_ok=True)
lock_text = "# Versi pustaka yang dipakai skrip Level 7 (lingkungan penulisan bab)\n" + "\n".join(lock_lines) + "\n"
(PACKAGE / "requirements-lock.txt").write_text(lock_text, encoding="utf-8")

order_text = "# Urutan eksekusi\n\nJalankan dari folder utama proyek, berurutan:\n\n" + "\n".join(f"{i + 1}. `python examples/level-7/{p.name}`" for i, p in enumerate(scripts)) + "\n"
(PACKAGE / "RUN_ORDER.md").write_text(order_text, encoding="utf-8")

decision_text = "# Log keputusan\n\n| id | tahap | jenis | keputusan | alasan |\n|---|---|---|---|---|\n" + "\n".join(
    f"| {r.id} | {r.tahap} | {r.jenis} | {str(r.keputusan).replace('|', '/')} | {str(r.alasan).replace('|', '/')} |" for r in decisions.itertuples()
) + "\n"
(PACKAGE / "DECISIONS.md").write_text(decision_text, encoding="utf-8")

(PACKAGE / "DATA_ATTRIBUTION.md").write_text(
    "# Atribusi data\n\n"
    f"- Dataset: {card['nama']}\n- Sumber: UCI Machine Learning Repository, DOI {card['doi']}\n"
    f"- Pembuat: {card['pembuat'].split(' (')[0]}\n- Lisensi: CC BY 4.0 menurut halaman UCI\n"
    "- Salinan yang dipakai: scikit-learn; disimpan ulang sebagai CSV (04_research_dataset.csv) tanpa perubahan nilai, dengan kolom diagnosis ditambahkan.\n"
    f"- Sidik jari data final: {card['sidik_jari_data_final']}\n",
    encoding="utf-8",
)

manifest_text = "\n".join(f"{c.sha256}  {c.path}" for c in checksums.itertuples()) + "\n"
(PACKAGE / "MANIFEST.sha256").write_text(manifest_text, encoding="utf-8")
checksums.to_csv(RESULTS / "09_checksums.csv", index=False, encoding="utf-8")
decisions.to_csv(RESULTS / "09_decision_log.csv", index=False, encoding="utf-8")

if head is None:
    state = "status Git tidak tersedia (Git tidak terpasang atau folder bukan repositori)"
elif uncommitted == 0:
    state = f"semua berkas Level 7 sudah di-commit (HEAD {head})"
else:
    state = f"{uncommitted} berkas Level 7 belum di-commit; belum ada commit yang bisa dirujuk"
(PACKAGE / "README.md").write_text(
    "# Paket reproduksi: Level 7 (Research Project)\n\n"
    "Tujuan: menjalankan ulang penelitian clustering pada Breast Cancer Wisconsin (Diagnostic) dan memeriksa bahwa hasilnya sama.\n\n"
    f"- Protokol terkunci: SHA-256 {(RESULTS / '05_protocol.sha256').read_text(encoding='utf-8').strip()[:16]}...\n"
    f"- Sidik jari data: {card['sidik_jari_data_final']}\n"
    f"- Status versi kode: {state}\n"
    "- Cara menjalankan: lihat RUN_ORDER.md\n- Dependensi: requirements-lock.txt\n- Keputusan: DECISIONS.md\n"
    "- Integritas berkas: MANIFEST.sha256 (sha256sum -c atau Get-FileHash)\n- Data dan lisensi: DATA_ATTRIBUTION.md\n\n"
    "Batas: hasil terjamin sama hanya pada lingkungan dengan versi pustaka serupa. Tidak ada klaim klinis.\n",
    encoding="utf-8",
)
print("Berkas paket:", sorted(p.name for p in PACKAGE.iterdir()))
# --8<-- [end:package]

# --8<-- [start:checklist]
rows = []


def check(name, ok, detail, warn_only=False):
    rows.append({"butir": name, "status": "LULUS" if ok else ("PERINGATAN" if warn_only else "GAGAL"), "rincian": detail})


required = ["README.md", "requirements-lock.txt", "RUN_ORDER.md", "DECISIONS.md", "MANIFEST.sha256", "DATA_ATTRIBUTION.md"]
check("Berkas paket lengkap", all((PACKAGE / n).exists() for n in required), f"{sum((PACKAGE / n).exists() for n in required)} dari {len(required)}")
check("Semua pemanggilan acak memakai seed", not all_issues, f"{total_checked} pemanggilan diperiksa")
check("Semua modul pihak ketiga terpetakan ke versi", not unknown, f"{len(lock_lines)} pustaka dikunci")
check("Tidak ada ketergantungan ke depan antar skrip", not order["ketergantungan_ke_depan"].map(bool).any(), "urutan numerik valid")
protocol_ok = hashlib.sha256(json.dumps(protocol, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest() == (RESULTS / "05_protocol.sha256").read_text(encoding="utf-8").strip()
check("Hash protokol cocok", protocol_ok, "protokol belum berubah")
check("Log keputusan mencakup klarifikasi Bab 6", int((decisions["jenis"] == "klarifikasi").sum()) == len(clar), f"{len(clar)} klarifikasi")
if RERUN:
    check("Semua skrip berjalan tanpa error saat diulang", all(r["kode_keluar"] == 0 for r in rerun_rows), f"{len(rerun_rows)} skrip")
    check("Berkas hasil tidak berubah setelah diulang", not changed_files, f"{len(changed_files)} berkas berubah")
else:
    check("Uji keterulangan dijalankan", False, "dilewati (RERUN=0)", warn_only=True)
check("Kode sudah di-commit sehingga paket bisa menunjuk satu commit", uncommitted == 0, f"{uncommitted} berkas belum di-commit", warn_only=True)
report = pd.DataFrame(rows)
print(report.to_string(index=False))
print("Ringkasan:", report["status"].value_counts().to_dict())
report.to_csv(RESULTS / "09_package_checklist.csv", index=False, encoding="utf-8")
# --8<-- [end:checklist]
