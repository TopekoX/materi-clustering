# Laporan QA Level 6 — Experimentation and Interpretation

Tanggal: 2026-11-10. Cakupan: Bab 8, 9, dan 10 (Bab 1–7 sudah ada dan hanya diverifikasi ulang).

## Ringkasan

| Item | Status |
|---|---|
| Bab 1–10 tersedia | Ya (10 dari 10) |
| `mkdocs build --strict` | Lulus (tanpa peringatan dokumentasi) |
| Skrip Bab 1–10 dijalankan | Semua keluar tanpa galat |
| Output Bab 1, 3–7 cocok dengan `outputs/*.txt` | Ya, identik |
| Output Bab 2 cocok dengan `outputs/02.txt` | Ya, kecuali satu baris info lingkungan (versi pustaka berbeda) |
| Output Bab 8, 9 diulang dua kali | Identik (Bab 9 diuji dengan `diff`) |
| Notebook Bab 1–10 dieksekusi dari awal sampai akhir | Semua tanpa galat |
| Rumus MathJax dirender di peramban | **Belum diperiksa** (butuh jaringan dan peramban) |

## Dibuat

- `docs/experimentation-and-interpretation/08-cluster-visualization-and-analysis.md`, `09-cluster-stability-and-reproducibility.md`, `10-experimental-reporting-and-interpretation.md`
- `examples/level-6/08_cluster_visualization_and_analysis.py`, `09_cluster_stability_and_reproducibility.py`, `10_experimental_reporting_and_interpretation.py`
- `examples/level-6/outputs/08.txt`, `09.txt`, `10.txt`
- `examples/level-6/results/`: `08_config.json`, `08_wine_z_profile.csv`, `09_config.json`, `09_stability_by_k.csv`, `09_cluster_jaccard.csv`, `10_config.json`, `10_report.md`
- `docs/assets/level-6/`: 5 gambar Bab 8, 3 gambar Bab 9, 1 gambar Bab 10
- `notebooks/level-6/08-…ipynb`, `09-…ipynb`, `10-…ipynb`
- `LEVEL6_QA_REPORT.md`

## Diubah

- `mkdocs.yml`: hanya `nav:` (tiga baris Bab 8–10).
- `docs/experimentation-and-interpretation/index.md`: tiga baris tabel bab.
- `docs/experimentation-and-interpretation/07-cluster-interpretation-and-profiling.md`: satu kalimat "Bab berikutnya" (sebelumnya menyebut Bab 8 sebagai kestabilan).
- `docs/curriculum/index.md`: baris Level 6 pada tabel ringkasan, bagian daftar bab Level 6, dan judul "Level 6–7" menjadi "Level 7".
- `PRD.md` dan `IMPLEMENTATION_PLAN.md`: bagian Level 6.

Level 1–5 tidak diubah (`git status` hanya menampilkan berkas Level 6, rencana, dan kurikulum).

## Penyimpangan dari prompt Level 6

Prompt mengusulkan Bab 7 = Cluster Visualization and Analysis dan Bab 8 = Cluster Profiling and Interpretation. Bab 7 yang sudah ada adalah Cluster Interpretation and Profiling, sehingga urutan menjadi: Bab 7 profiling (tetap), Bab 8 visualisasi, Bab 9 kestabilan, Bab 10 pelaporan. Pembagian ini disetujui pengguna. Topik profiling pada prompt tercakup di Bab 7. Judul Bab 5 dan 6 sedikit berbeda dari prompt ("Feature Selection and Impact Analysis", "Dimensionality Reduction and PCA").

## Reproduksibilitas

Seed 42. Lingkungan eksekusi: Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, SciPy 1.18.1, Matplotlib 3.11.1, Windows. Bab 1–7 menyebut versi lain (Python 3.14.7, NumPy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1, Matplotlib 3.11.2). Angka metrik dan ukuran kelompok identik pada kedua lingkungan. Hanya waktu eksekusi dan info lingkungan yang berbeda. Bab 8–10 mencatat versi yang dipakai saat dijalankan.

## Pemeriksaan isi (yang ditemukan dan diperbaiki saat penulisan)

- Pair plot Bab 8: pasangan fitur yang memisahkan tiga kelompok paling baik ternyata `flavanoids` terhadap `color_intensity`, bukan `flavanoids` terhadap `proline` (diperiksa pada gambar). Teks diperbaiki.
- Silhouette 0,285 (Wine, 13 fitur) pada panduan Level 5 tergolong "lemah" (0,26–0,50). Teks diperbaiki.
- Pernyataan tentang asal noise DBSCAN (17 dari 20 dari satu gerombol) kini dicetak oleh skrip, bukan dihitung terpisah.
- `PALETTE[-1]` pada Python tidak menimbulkan `IndexError` (indeks negatif valid). Baris troubleshooting diperbaiki.
- Bab 9: hasil praproses pada Mall Customers tidak menunjukkan kepekaan (ARI 1,000). Ini dilaporkan apa adanya, dengan pembanding Wine (ARI 0,354 tanpa penskalaan).
- Bab 9: pada data acak seragam, rata-rata ARI sampel 80% sudah 0,958 (Mall Customers 0,987). Kesimpulan "stabil tidak membuktikan struktur" dirumuskan dengan angka ini, bukan dengan klaim bahwa data acak tidak stabil.

## Keterbatasan dan hal yang belum dikerjakan

- **MathJax belum dirender di peramban.** Rumus ditulis mengikuti konvensi proyek (`\( … \)`, `$$ … $$`) dan build strict lulus, tetapi tampilannya belum dilihat.
- Gambar Bab 8–10 sudah dilihat secara langsung, kecuali `08-pair-plot-wine.png` dan `08-tumpang-tindih.png` yang dilihat setelah revisi teks, bukan sebelum menulis.
- Skrip Bab 9 membutuhkan sekitar satu setengah menit (ratusan clustering ulang).
- Pemeriksa kata berlebihan di Bab 10 hanya heuristik; kelemahannya ditunjukkan di Latihan 1 bab itu.
- Daftar bab Level 5 pada `README.md` dan baris Level 5 di `docs/curriculum/index.md` masih tertulis "Direncanakan". Itu sudah demikian sebelum pekerjaan ini dan tidak diubah.
- Belum ada commit. `origin` masih `mkdocs-template`.
