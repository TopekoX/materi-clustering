# IMPLEMENTATION PLAN — Materi Clustering (Level 2)

Aturan: kerjakan bertahap, validasi tiap fase sebelum lanjut, laporkan file yang berubah dan hasil validasi. Tidak ada commit/push/deploy tanpa instruksi.

| Fase | Isi | Keluaran | Gerbang validasi |
|---|---|---|---|
| 1 | Audit repositori | `PROJECT_AUDIT.md` | Disetujui ✅ |
| 2 | Perencanaan | `PRD.md`, `IMPLEMENTATION_PLAN.md`, `CLAUDE.md`; identitas situs (`site_name`, `site_description`, `language: id`); PRD lama → `PRD_TEMPLATE.md` | Review pengguna |
| 0* | Prasyarat lingkungan | `.venv` (docs) dan venv notebook; baseline `mkdocs build --strict` | Build baseline lulus; paket sains terpasang |
| 3 | Arsitektur konten | Struktur `docs/data-exploration-and-preprocessing/`, nav, `_chapter-template` (satu format bab) | Build strict lulus dengan bab contoh |
| 4 | Pengembangan bab | Satu bab per iterasi (01 → 12) | Per bab: kode dijalankan, output cocok, build strict, review |
| 5 | Notebook | `notebooks/level-2/NN-*.ipynb` + `data/mall_customers.csv` | `jupyter nbconvert --execute` tanpa error |
| 6 | Integrasi MkDocs | Nav final, tautan unduh notebook, roadmap `curriculum/index.md` | Semua fitur lama tetap berfungsi |
| 7 | QA | Konsistensi, eksekusi kode, dataset, tautan, gambar, rumus, nav, build | Daftar periksa lulus |
| 8 | Rilis | Catatan rilis, isu tersisa | Persetujuan pengguna |

\*Fase 0 dijalankan segera setelah Fase 2 disetujui; ia prasyarat Fase 3 dan seterusnya.

## Keputusan yang masih terbuka

1. **Dataset Mall Customers**: CSV milik pengguna, unduhan Kaggle (cek lisensi), atau replika sintetis yang diberi label jelas. Dibutuhkan sebelum Fase 5; bab Fase 4 yang memakai data menunggu keputusan ini.
2. **Git `origin`**: arahkan ulang ke `materi-clustering`? (default: tidak diubah).
3. **Notebook**: default file unduhan; `mkdocs-jupyter` hanya jika disetujui.
4. **Bahasa judul bagian bab**: Inggris persis seperti standar (default) atau padanan Indonesia.

## Rencana per bab (Fase 4)

Urutan sama dengan daftar di `PRD.md`. Setiap iterasi: tulis bab → tulis kode → jalankan → tempel output nyata → build strict → laporkan → tunggu persetujuan sebelum bab berikutnya.

## Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Wheel Python 3.14 untuk paket sains | Verifikasi di Fase 0; bila gagal, gunakan Python 3.12/3.13 untuk venv notebook |
| MathJax butuh jaringan | Diterima dan didokumentasikan |
| Output yang ditulis tidak cocok dengan eksekusi | Output hanya disalin dari eksekusi nyata |
| Dataset tak tersedia/lisensi | Keputusan pengguna sebelum Fase 5 |

## Status Level 3 — Fundamental Clustering (2026-11-09)

| Bab | Bab (file) | Skrip | Notebook | Status |
|---|---|---|---|---|
| 1 | `01-introduction-to-clustering.md` | `01_introduction_to_clustering.py` | ✅ dieksekusi | Siap ditinjau |
| 2 | `02-understanding-clusters.md` | `02_understanding_clusters.py` | ✅ dieksekusi | Siap ditinjau |
| 3 | `03-centroid-and-cluster-representation.md` | `03_centroid_and_representation.py` | ✅ dieksekusi | Siap ditinjau |
| 4 | `04-similarity-and-dissimilarity.md` | `04_similarity_and_dissimilarity.py` | ✅ dieksekusi | Siap ditinjau |
| 5 | `05-distance-metrics.md` | `05_distance_metrics.py` | ✅ dieksekusi | Siap ditinjau |
| 6 | `06-feature-space-and-dimensionality.md` | `06_feature_space_and_dimensionality.py` | ✅ dieksekusi | Siap ditinjau |
| 7 | `07-clustering-workflow.md` | `07_clustering_workflow.py` | ✅ dieksekusi | Siap ditinjau |

Laporan QA: `LEVEL3_QA_REPORT.md`.

## Status Level 4 — Clustering Algorithms (2026-11-10)

| Bab | Bab (file) | Skrip | Notebook | Status |
|---|---|---|---|---|
| 1 | `01-introduction-to-clustering-algorithms.md` | `01_introduction_to_clustering_algorithms.py` | ✅ dieksekusi | Siap ditinjau |
| 2 | `02-k-means-clustering.md` | `02_k_means_clustering.py` | ✅ dieksekusi | Siap ditinjau |
| 3 | `03-hierarchical-clustering.md` | `03_hierarchical_clustering.py` | ✅ dieksekusi | Siap ditinjau |
| 4 | `04-dbscan-clustering.md` | `04_dbscan_clustering.py` | ✅ dieksekusi | Siap ditinjau |
| 5 | `05-gaussian-mixture-models.md` | `05_gaussian_mixture_models.py` | ✅ dieksekusi | Siap ditinjau |
| 6 | `06-mean-shift-clustering.md` | `06_mean_shift_clustering.py` | ✅ dieksekusi | Siap ditinjau |
| 7 | `07-comparison-of-clustering-algorithms.md` | — | — | Direncanakan |

Satu bab per iterasi; QA report (`LEVEL4_QA_REPORT.md`) dibuat setelah Bab 7.
