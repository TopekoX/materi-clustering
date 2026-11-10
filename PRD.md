# PRD — Materi Clustering (Clustering pada Machine Learning)

Status: Draft untuk persetujuan · Tanggal: 2026-11-09

> PRD template lama dipertahankan sebagai `PRD_TEMPLATE.md`.

## 1. Tujuan

Platform dokumentasi berbahasa Indonesia yang mengajarkan Clustering Machine Learning dari tingkat pemula sampai penerapan riset, di atas template MkDocs + Material yang sudah ada (tanpa membangun ulang).

Pendekatan belajar: Konsep → Fondasi Matematika → Implementasi Python → Latihan → Eksperimen → Evaluasi Model → Aplikasi Riset.

## 2. Pengguna

- **Pembelajar** (utama): pemula–menengah, membaca di desktop/ponsel, menjalankan kode sendiri.
- **Penulis/maintainer**: menulis Markdown, menambah bab dan notebook.

## 3. Kurikulum

| Level | Topik |
|---|---|
| 1 | Machine Learning Fundamentals |
| 2 | Data Exploration and Preprocessing **(lingkup awal)** |
| 3 | Fundamental Clustering |
| 4 | Clustering Algorithms |
| 5 | Clustering Evaluation |
| 6 | Experimentation and Interpretation |
| 7 | Research Project |

### Lingkup awal: Level 2 (12 bab)

1. Introduction to Data Exploration
2. Understanding Data Types
3. Descriptive Statistics
4. Exploratory Data Analysis
5. Missing Values Analysis
6. Duplicate Data Analysis
7. Outlier Detection and Handling
8. Data Cleaning
9. Data Transformation and Encoding
10. Feature Scaling
11. Feature Selection and Feature Engineering
12. Dataset Preparation for Clustering

### Level 3 (disetujui dikerjakan, 2026-11-09): Fundamental Clustering — 7 bab

1. Introduction to Clustering
2. Understanding Clusters
3. Centroid and Cluster Representation
4. Similarity and Dissimilarity
5. Distance Metrics
6. Feature Space and Dimensionality
7. Clustering Workflow

Folder: `docs/fundamental-clustering/`. Algoritma clustering tidak dibahas mendalam (itu Level 4); K-Means hanya disebut sebagai alat bantu.

### Level 4 (disetujui dikerjakan, 2026-11-10): Clustering Algorithms — 7 bab

1. Introduction to Clustering Algorithms
2. K-Means Clustering
3. Hierarchical Clustering
4. DBSCAN Clustering
5. Gaussian Mixture Models (GMM)
6. Mean Shift Clustering
7. Comparison of Clustering Algorithms

Folder: `docs/clustering-algorithms/`. Struktur bab tetap 14 bagian standar (keputusan 2026-11-10). Metrik evaluasi formal tidak dibahas (itu Level 5). `scipy` ditambahkan ke `requirements-notebooks.txt` untuk dendrogram.

Level 5–7 di luar lingkup sampai Level 4 disetujui.

## 4. Standar isi bab (wajib)

1. Learning Objectives · 2. Introduction · 3. Fundamental Concepts · 4. Detailed Explanation · 5. Mathematical Foundation (jika relevan) · 6. Python Implementation · 7. Code Explanation · 8. How to Run · 9. Expected Output · 10. Practical Examples · 11. Hands-on Exercises · 12. Troubleshooting · 13. Summary · 14. References

Judul bagian memakai istilah Inggris di atas atau padanan Indonesia yang konsisten (diputuskan di Phase 3 dan dikunci di `CLAUDE.md`). Isi dalam bahasa Indonesia; istilah teknis internasional tetap dalam bahasa Inggris.

## 5. Persyaratan fungsional

| ID | Persyaratan |
|---|---|
| F1 | Seluruh materi berbahasa Indonesia; `theme.language: id`; `site_name: Materi Clustering`; `site_description: Clustering pada Machine Learning` |
| F2 | Menggunakan template, tema, CSS, JS, dan navigasi yang ada; perubahan hanya aditif |
| F3 | Setiap level berada langsung di bawah `docs/` dalam folder bernama sesuai topik; Level 2 di `docs/data-exploration-and-preprocessing/` dengan halaman indeks dan 12 bab |
| F4 | Setiap bab mengikuti standar 14 bagian |
| F5 | Rumus matematika memakai arithmatex/MathJax yang ada |
| F6 | Setiap bab punya kode Python yang dapat dijalankan dan output yang diharapkan yang benar-benar dihasilkan dari kode tersebut |
| F7 | Notebook Jupyter yang dapat dieksekusi, dengan sel Markdown penjelas, memakai dataset Mall Customers |
| F8 | Dataset tersedia di repositori dengan lisensi/sumber yang tercatat |
| F9 | `mkdocs build --strict` lulus |

## 6. Persyaratan non-fungsional

- Akurasi teori: rumus dan klaim diverifikasi; referensi dapat ditelusuri (tidak mengarang kutipan).
- Ramah pemula: istilah dijelaskan saat pertama muncul; contoh bertahap.
- Reprodusibel: `random_state` tetap; versi pustaka dicatat.
- Aksesibel: mengikuti tema (terang/gelap), teks alternatif untuk gambar.
- Tidak ada commit, push, atau deploy tanpa instruksi eksplisit.

## 7. Arsitektur

```
mkdocs.yml                       (ubah hanya nav, identitas yang disetujui)
docs/curriculum/index.md         roadmap 7 level (hanya indeks; level tidak ditaruh di sini)
docs/data-exploration-and-preprocessing/         index.md + 01-…12-*.md
docs/assets/level-2/             gambar
data/mall_customers.csv          dataset
notebooks/level-2/NN-*.ipynb     notebook (diunduh dari situs / dijalankan lokal)
requirements-notebooks.txt       dependensi notebook (terpisah dari requirements.txt)
```

Notebook disediakan sebagai file unduhan di samping bab Markdown; plugin `mkdocs-jupyter` tidak ditambahkan kecuali disetujui.

## 8. Tumpukan teknologi

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Jupyter Notebook, Markdown, MkDocs (Material), MathJax/LaTeX.

## 9. Kriteria penerimaan Level 2

- 12 bab lengkap sesuai standar; 12 notebook dieksekusi tanpa error dari awal sampai akhir.
- Build strict bersih; tautan, anchor, gambar, dan rumus diperiksa.
- Navigasi menampilkan Level 2 tanpa merusak halaman yang ada.
- Daftar isu tersisa didokumentasikan.

## 10. Risiko dan pertanyaan terbuka

- Sumber dan lisensi dataset Mall Customers belum diputuskan (lihat `IMPLEMENTATION_PLAN.md`, Phase 0).
- Ketersediaan wheel pandas/scikit-learn/Jupyter untuk Python 3.14 belum diverifikasi.
- MathJax dari CDN memerlukan jaringan.
- `origin` git masih mengarah ke `mkdocs-template`.
