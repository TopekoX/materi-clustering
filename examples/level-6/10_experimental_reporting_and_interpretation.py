"""Level 6, Bab 10: Pelaporan eksperimen clustering dan interpretasinya.

Skrip ini menyusun laporan eksperimen dari file hasil yang sudah tersimpan oleh Bab 4, 7, dan 9.
Tidak ada angka yang diketik tangan di laporan: semuanya dibaca dari file sumber.

Jalankan dari folder utama proyek (setelah menjalankan skrip Bab 7 dan Bab 9):
    python examples/level-6/10_experimental_reporting_and_interpretation.py
"""
# NB: setup=Siapkan alat | load=Membaca file hasil | dataset=Deskripsi data | permtest=Uji permutasi umur | tables=Tabel hasil | conflict=Metrik yang bertentangan | wording=Pemeriksa kata berlebihan | report=Menyusun laporan | save=Menyimpan laporan | plotreport=Gambar untuk laporan

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import json
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import _experiment as ex

SEED = 42
RESULTS = ex.RESULTS_DIR


def fmt(value, digits=3):
    """Angka dengan koma desimal, seperti penulisan bahasa Indonesia."""
    return f"{value:.{digits}f}".replace(".", ",")


def md_table(frame):
    """Mengubah DataFrame menjadi tabel Markdown (tanpa pustaka tambahan)."""
    header = "| " + " | ".join(map(str, frame.columns)) + " |"
    divider = "|" + "|".join("---" for _ in frame.columns) + "|"
    rows = ["| " + " | ".join(map(str, row)) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, divider, *rows])
# --8<-- [end:setup]

import _savefig

_savefig.install(["10-gambar-laporan"])

# --8<-- [start:load]
profile = pd.read_csv(RESULTS / "07_cluster_profile.csv", index_col="Cluster")
k_table = pd.read_csv(RESULTS / "09_stability_by_k.csv")
jaccard = pd.read_csv(RESULTS / "09_cluster_jaccard.csv", index_col=0)
benchmark = pd.read_csv(RESULTS / "04_benchmark.csv")
config = json.loads((RESULTS / "09_config.json").read_text(encoding="utf-8"))
for name, table in [("07_cluster_profile", profile), ("09_stability_by_k", k_table), ("09_cluster_jaccard", jaccard), ("04_benchmark", benchmark)]:
    print(f"{name}.csv: {len(table)} baris")
print("09_config.json:", sorted(config))
# --8<-- [end:load]

# --8<-- [start:dataset]
df = pd.read_csv("data/mall_customers.csv")
used = ["Annual Income (k$)", "Spending Score (1-100)"]
data_facts = {
    "n": len(df),
    "kolom": list(df.columns),
    "kosong": int(df.isna().sum().sum()),
    "perempuan": int((df["Gender"] == "Female").sum()),
    "laki": int((df["Gender"] == "Male").sum()),
    "pendapatan": (int(df[used[0]].min()), int(df[used[0]].max())),
    "skor": (int(df[used[1]].min()), int(df[used[1]].max())),
    "umur": (int(df["Age"].min()), int(df["Age"].max())),
}
print(data_facts)
print("Sidik jari data (cocok dengan konfigurasi Bab 9):", config["dataset_fingerprint"])
# --8<-- [end:dataset]

# --8<-- [start:permtest]
# Uji permutasi umur antar kelompok, sama dengan Bab 7 (label kelompok dibangun ulang dengan konfigurasi yang sama)
from sklearn.cluster import KMeans

z = ((df[used] - df[used].mean()) / df[used].std()).to_numpy()
raw_labels = KMeans(n_clusters=5, n_init=10, random_state=SEED).fit(z).labels_
order = np.argsort(-np.bincount(raw_labels), kind="stable")
letter = {int(old): "ABCDE"[new] for new, old in enumerate(order)}
cluster = np.array([letter[int(c)] for c in raw_labels])
assert [int((cluster == c).sum()) for c in "ABCDE"] == profile["n"].tolist(), "ukuran kelompok tidak cocok dengan 07_cluster_profile.csv"

def spread(values, labels):
    means = pd.Series(values).groupby(labels).mean()
    return means.max() - means.min()

rng = np.random.default_rng(SEED)
age = df["Age"].to_numpy(float)
observed = spread(age, cluster)
shuffled = [spread(age, rng.permutation(cluster)) for _ in range(2000)]
p_age = (sum(s >= observed for s in shuffled) + 1) / (len(shuffled) + 1)
print(f"Umur: selisih rata-rata antar kelompok {observed:.3f} tahun | batas acak 95% {np.percentile(shuffled, 95):.3f} | p = {p_age:.4f}")
# --8<-- [end:permtest]

# --8<-- [start:tables]
best_sil = k_table.loc[k_table["silhouette"].idxmax()]
best_stab = k_table.loc[k_table["stability_mean"].idxmax()]
k5 = k_table.loc[k_table["k"] == 5].iloc[0]

table_k = pd.DataFrame({
    "K": k_table["k"], "Silhouette": k_table["silhouette"].map(fmt),
    "Kestabilan (rata-rata)": k_table["stability_mean"].map(fmt), "Kestabilan (minimum)": k_table["stability_min"].map(fmt),
})
table_profile = pd.DataFrame({
    "Kelompok": profile.index, "Ukuran": profile["n"],
    "Pendapatan (k$), rata-rata": profile["pendapatan_rata"].map(lambda v: fmt(v, 1)),
    "Skor belanja, rata-rata": profile["skor_rata"].map(lambda v: fmt(v, 1)),
    "Umur, median": profile["umur_median"].map(lambda v: fmt(v, 1)),
    "Jaccard (kestabilan)": jaccard["jaccard_rata"].map(fmt).to_numpy(),
})
print(table_k.to_string(index=False))
print(table_profile.to_string(index=False))
# --8<-- [end:tables]

# --8<-- [start:conflict]
# Contoh metrik yang bertentangan: dataset "Bulan sabit" pada benchmark Bab 4
crescent = benchmark[(benchmark["dataset"] == "Bulan sabit") & benchmark["algorithm"].isin(["K-Means", "DBSCAN"])].set_index("algorithm")
by_sil = crescent["silhouette"].idxmax()
by_ari = crescent["ari_reference"].idxmax()
print(crescent[["silhouette", "davies_bouldin", "ari_reference"]].round(3).to_string())
print(f"Dipilih menurut Silhouette: {by_sil} | dipilih menurut ARI terhadap label acuan: {by_ari}")
# --8<-- [end:conflict]

# --8<-- [start:wording]
# Pemeriksa sederhana untuk kata yang cenderung melebih-lebihkan. Ini heuristik, bukan pengganti membaca.
RISKY = ["membuktikan", "pasti", "menyebabkan", "penyebab", "terbaik", "sempurna", "selalu", "benar-benar", "jelas bahwa"]
NEGATIONS = ("tidak", "bukan", "belum", "jangan")

def flag_overclaims(text):
    """Mengembalikan kalimat yang memuat kata berisiko tanpa kata penyangkal di kalimat yang sama."""
    flagged = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        lowered = sentence.lower()
        hits = [w for w in RISKY if w in lowered]
        if hits and not any(n in lowered.split() for n in NEGATIONS):
            flagged.append((hits, sentence.strip()))
    return flagged

draft = ("Hasil ini membuktikan bahwa lima segmen pelanggan benar-benar ada. Kelompok E pasti boros karena umurnya muda. "
         "K = 5 adalah pilihan terbaik. Kelompok C tidak berbelanja banyak.")
for hits, sentence in flag_overclaims(draft):
    print(f"DITANDAI {hits}: {sentence}")
# --8<-- [end:wording]

# --8<-- [start:report]
env = config["environment"]
facts = data_facts
sizes = ", ".join(f"{c} ({int(profile.loc[c, 'n'])})" for c in profile.index)
report = f"""# Laporan Eksperimen: Pengelompokan Pelanggan Mall Customers dengan K-Means

## 1. Pertanyaan dan tujuan

Apakah pelanggan dapat dikelompokkan berdasarkan pendapatan tahunan dan skor belanja, dan seberapa konsisten pengelompokan itu terhadap perubahan seed, sampel, dan jumlah kelompok (K)? Eksperimen ini bersifat **eksploratif**: tidak ada label acuan dan tidak ada hipotesis yang diuji secara statistik formal.

## 2. Data

Mall Customers, {facts['n']} pelanggan, kolom: {', '.join(facts['kolom'])}. Nilai kosong: {facts['kosong']}. Perempuan {facts['perempuan']}, laki-laki {facts['laki']}. Rentang pendapatan {facts['pendapatan'][0]} sampai {facts['pendapatan'][1]} k$, skor belanja {facts['skor'][0]} sampai {facts['skor'][1]}, umur {facts['umur'][0]} sampai {facts['umur'][1]} tahun. Sumber: Kaggle (salinan di `data/mall_customers.csv`). Sidik jari data: `{config['dataset_fingerprint']}`.

## 3. Praproses dan fitur

Fitur untuk clustering: {', '.join(config['features'])}. Praproses: {config['preprocessing']}. Umur dan gender **tidak** dipakai clustering dan hanya dipakai untuk menggambarkan kelompok.

## 4. Algoritma dan konfigurasi

{config['algorithm']}, seed {config['seed']}. Untuk memilih K, K = 2 sampai 8 dibandingkan memakai Silhouette dan kestabilan terhadap sampel ({int(config['subsample_fractions'][1] * 100)}% data, {config['subsample_repeats']} pengulangan). Kestabilan tiap kelompok dihitung dengan {config['bootstrap_repeats']} sampel bootstrap.

## 5. Hasil: memilih K

{md_table(table_k)}

Silhouette tertinggi pada K = {int(best_sil['k'])} ({fmt(best_sil['silhouette'])}). Kestabilan rata-rata tertinggi pada K = {int(best_stab['k'])} ({fmt(best_stab['stability_mean'])}). Untuk K = 5, Silhouette {fmt(k5['silhouette'])} dan kestabilan rata-rata {fmt(k5['stability_mean'])} (minimum {fmt(k5['stability_min'])}).

Kedua kriteria **tidak menunjuk K yang sama**. Silhouette menilai keterpisahan dan kekompakan kelompok. Kestabilan menilai konsistensi hasil terhadap sampel. K = {int(best_stab['k'])} konsisten tetapi lebih longgar dalam keterpisahan. Kami memilih K = 5 karena Silhouette tertinggi dan kestabilannya juga tinggi, bukan karena K = 5 terbukti benar.

## 6. Hasil: profil kelompok (K = 5)

{md_table(table_profile)}

Ukuran kelompok: {sizes}. Perbedaan umur antar kelompok lebih besar daripada yang diharapkan secara acak (selisih rata-rata terbesar dan terkecil {fmt(observed)} tahun, batas acak 95% {fmt(np.percentile(shuffled, 95))}, p = {fmt(p_age, 4)}, uji permutasi {len(shuffled)} kali). Ini asosiasi, bukan sebab: kami tidak menyimpulkan bahwa umur memengaruhi perilaku belanja.

## 7. Keterbatasan

- Hanya satu dataset kecil ({facts['n']} pelanggan), satu algoritma (K-Means), dan dua fitur.
- Kelompok terkecil hanya {int(profile['n'].min())} pelanggan, sehingga rata-rata kelompok itu bergantung pada sedikit data.
- Kestabilan menunjukkan konsistensi terhadap sampel dan seed, bukan bahwa kelompok itu nyata atau berguna.
- Nama kelompok pada profil adalah label deskriptif dan bergantung pada ambang yang dipilih.
- Hasil belum diuji pada pelanggan di luar data ini.

## 8. Kesimpulan yang didukung data

Pada data ini, K-Means dengan K = 5 pada pendapatan dan skor belanja menghasilkan lima kelompok yang konsisten terhadap seed (dengan n_init = 10) dan sampel, dengan Jaccard tiap kelompok antara {fmt(jaccard['jaccard_rata'].min())} dan {fmt(jaccard['jaccard_rata'].max())}. Pilihan K = 5 didukung oleh Silhouette tertinggi, tetapi K = {int(best_stab['k'])} lebih stabil.

## 9. Reproduksibilitas

Python {env['python']}, NumPy {env['numpy']}, pandas {env['pandas']}, scikit-learn {env['scikit-learn']}, SciPy {env['scipy']}, Matplotlib {env['matplotlib']}, {env['os']}. Seed {config['seed']}. File hasil: `07_cluster_profile.csv`, `09_stability_by_k.csv`, `09_cluster_jaccard.csv`, `09_config.json`.
"""
problems = flag_overclaims(report)
print(f"Laporan: {len(report.splitlines())} baris, {len(report.split())} kata. Kalimat berisiko ditandai: {len(problems)}")
for hits, sentence in problems:
    print("  ", hits, sentence)
# --8<-- [end:report]

# --8<-- [start:save]
(RESULTS / "10_report.md").write_text(report, encoding="utf-8")
ex.save_json({"seed": SEED, "sources": ["07_cluster_profile.csv", "09_stability_by_k.csv", "09_cluster_jaccard.csv", "04_benchmark.csv", "09_config.json"],
              "permutations": 2000, "wording_checked": True}, "10_config")
print("Laporan tersimpan: examples/level-6/results/10_report.md")
# --8<-- [end:save]

# --8<-- [start:plotreport]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
axes[0].plot(k_table["k"], k_table["silhouette"], marker="s", color="#D55E00", label="Silhouette")
axes[0].plot(k_table["k"], k_table["stability_mean"], marker="o", color="#0072B2", label="Kestabilan (rata-rata)")
axes[0].fill_between(k_table["k"], k_table["stability_min"], k_table["stability_mean"], color="#0072B2", alpha=0.15, label="rentang rata-rata sampai minimum")
axes[0].set_xlabel("K")
axes[0].set_ylabel("Nilai")
axes[0].set_title("(a) Memilih K: dua kriteria", fontsize=10)
axes[0].legend(fontsize=8, loc="lower right")

colors = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00"]
bars = axes[1].bar(profile.index, profile["n"], color=colors)
for bar, value in zip(bars, jaccard["jaccard_rata"]):
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5, f"J = {value:.2f}".replace(".", ","), ha="center", fontsize=8)
axes[1].set_ylim(0, profile["n"].max() * 1.15)
axes[1].set_xlabel("Kelompok")
axes[1].set_ylabel("Jumlah pelanggan")
axes[1].set_title("(b) Ukuran dan kestabilan (Jaccard) kelompok", fontsize=10)

width = 0.35
x = np.arange(2)
for i, (metric, label, color) in enumerate([("silhouette", "Silhouette (internal)", "#D55E00"), ("ari_reference", "ARI terhadap label acuan", "#0072B2")]):
    axes[2].bar(x + (i - 0.5) * width, [crescent.loc[a, metric] for a in ["K-Means", "DBSCAN"]], width, color=color, label=label)
axes[2].set_xticks(x, ["K-Means", "DBSCAN"])
axes[2].set_ylim(0, 1.05)
axes[2].set_ylabel("Nilai")
axes[2].set_title("(c) Metrik bertentangan: data bulan sabit (Bab 4)", fontsize=10)
axes[2].legend(fontsize=8, loc="upper left")
plt.tight_layout()
plt.show()
# --8<-- [end:plotreport]
