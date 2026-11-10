# QA Report — Level 4: Clustering Algorithms

Tanggal: 2026-11-10 · Lingkungan: Python 3.14, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, SciPy 1.18.1, matplotlib 3.11.1

## Bab selesai

7 dari 7 bab (`docs/clustering-algorithms/01`–`07`) plus `index.md`. Semua mengikuti 14 bagian standar `CLAUDE.md` (keputusan 2026-11-10, bukan 15 bagian dari prompt tugas). Pemetaan: *How the Algorithm Works* dan *Algorithm Steps* masuk *Detailed Explanation*; *Step-by-Step Code Explanation* masuk *Python Implementation*; *Output and Interpretation* dan *Visualization* masuk *Expected Output*; *Advantages and Limitations* masuk *Detailed Explanation*; *Common Mistakes* masuk *Troubleshooting*.

| Bab | File | Algoritma / isi | Kode dari nol |
|---|---|---|---|
| 1 | `01-introduction-to-clustering-algorithms.md` | Peta keluarga algoritma, API scikit-learn | — |
| 2 | `02-k-means-clustering.md` | K-Means, WCSS, k-means++, elbow | K-Means dan k-means++ (NumPy) |
| 3 | `03-hierarchical-clustering.md` | Agglomerative, dendrogram, 4 linkage | — (SciPy untuk dendrogram) |
| 4 | `04-dbscan-clustering.md` | DBSCAN, k-distance | Klasifikasi core/border/noise (NumPy) |
| 5 | `05-gaussian-mixture-models.md` | GMM, EM, 4 tipe kovarians | EM satu dimensi (NumPy) |
| 6 | `06-mean-shift-clustering.md` | Mean Shift, KDE, bandwidth | Mean Shift (NumPy) |
| 7 | `07-comparison-of-clustering-algorithms.md` | Perbandingan 5 algoritma x 6 dataset | Panduan keputusan (fungsi) |

## Validasi

| Pemeriksaan | Hasil |
|---|---|
| `mkdocs build --strict` | Lulus (tautan, anchor, gambar, snippet `check_paths`) |
| Skrip `examples/level-4/01`–`07` | Semua dijalankan. Output nyata disimpan di `examples/level-4/outputs/NN.txt` dan disertakan ke bab lewat snippet |
| Reproduksibilitas | Skrip 01–06 dijalankan ulang di akhir: output identik byte demi byte dengan `outputs/NN.txt`. Skrip 07 memuat pengukuran waktu sehingga angka waktunya berbeda tiap eksekusi (dinyatakan di bab) |
| Notebook `notebooks/level-4/01`–`07` | Semua dieksekusi dengan `jupyter nbconvert --execute`, 0 error. Hasil eksekusi hanya di folder sementara. Notebook di repo tidak berisi output (sama seperti Level 2 dan 3). Kode notebook dibangun dari potongan skrip yang sama, sehingga tidak menyimpang dari skrip |
| Rumus | 698 rumus pada halaman hasil build diurai dengan parser TeX MathJax 3.2.2 (paket `base`, `ams`, `newcommand`, `configmacros`): 0 galat. Pemeriksaan dilakukan setelah tiap bab. Pemeriksaan ini menangkap makro tak didukung seperti `\boldsymbol` (ditemukan dan diperbaiki di Bab 1) |
| Penanda `--8<--` tersisa di HTML | Tidak ada |
| Mermaid | Satu atau lebih diagram per bab ada di HTML hasil build. **Sintaks Mermaid belum dirender di browser** |
| Gambar | 30 gambar di `docs/assets/level-4/`. Gambar utama tiap bab dilihat langsung selama pengerjaan |
| Angka di bab | Semua output dan jawaban latihan berasal dari eksekusi nyata atau hitungan manual yang dicek dengan kode |
| Level 1, 2, 3 | Tidak diubah oleh tugas ini. Perubahan di `docs/data-exploration-and-preprocessing/01-introduction-to-data-exploration.md` berasal dari pengguna (tautan dataset), bukan dari tugas ini |
| Cakupan Level 5 | Tidak ada metrik evaluasi (silhouette, ARI, Davies-Bouldin, BIC/AIC) yang dihitung. Beberapa bab hanya menyebut namanya sebagai penunjuk ke Level 5 |

## File dibuat

- `docs/clustering-algorithms/index.md`, `01`–`07-*.md`
- `examples/level-4/01`–`07_*.py`, `_savefig.py`, `outputs/01`–`07.txt`
- `docs/assets/level-4/*.png`
- `notebooks/level-4/01`–`07-*.ipynb`
- `LEVEL4_QA_REPORT.md`

## File diubah

- `mkdocs.yml` (hanya `nav:`)
- `docs/curriculum/index.md`, `PRD.md`, `CLAUDE.md`, `IMPLEMENTATION_PLAN.md`
- `requirements-notebooks.txt` (tambah `scipy>=1.10`)

## Catatan temuan selama pengerjaan

- `\boldsymbol` tidak dirender (merah) di situs karena ekstensi MathJax tidak termuat; diganti `\mu` di Bab 1. Sejak itu semua bab diperiksa dengan pemeriksa rumus berbasis MathJax.
- Bab 5: notebook gagal pada eksekusi pertama (`import warnings` berada di luar potongan kode); diperbaiki dengan memindahkan impor ke potongan `setup`. Bab 7 mendapat perbaikan serupa (`import time`).
- Bab 2: scikit-learn tidak memberi peringatan bila `max_iter` terlalu kecil pada `KMeans` (diamati pada eksekusi); dicatat di bab.
- Bab 5: dataset 2D awal terlalu mudah (semua metode identik), diganti data yang dibangkitkan dari tiga Gaussian bertumpang tindih dengan parameter diketahui.

## Keterbatasan dan isu tersisa

- Render visual MathJax dan Mermaid belum diperiksa di browser (perlu jaringan untuk CDN). Parser MathJax lolos untuk semua rumus, tetapi tampilan visual belum dilihat.
- Gambar memakai latar putih; di tema gelap tampil sebagai kotak putih (sama dengan Level 2 dan 3).
- Pengukuran skalabilitas (Bab 7) hanya satu eksekusi pada satu mesin dengan data kecil. Untuk K-Means, GMM, dan DBSCAN waktunya terlalu kecil sehingga rasionya tidak bermakna (dinyatakan di bab).
- Perbandingan Bab 7 tidak setara sepenuhnya (K diberikan, `eps` disetel per dataset, Mean Shift satu aturan). Dinyatakan di bab.
- Referensi bibliografi ditulis dari pengetahuan umum dan belum diverifikasi satu per satu terhadap sumbernya (volume, halaman).
- `AgglomerativeClustering` hanya mendukung agglomerative; divisive hanya dijelaskan secara konseptual sesuai instruksi.
- Tidak ada deploy. Level 4 Bab 1–6 sudah dikomit (`9adb656`); Bab 7, laporan ini, dan pembaruan status belum dikomit.
