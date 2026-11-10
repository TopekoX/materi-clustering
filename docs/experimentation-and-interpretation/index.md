# Level 6 — Experimentation and Interpretation

Level ini mengajarkan cara **bekerja secara sistematis** dengan clustering: merancang eksperimen, mengatur hyperparameter, membandingkan algoritma, memahami dampak fitur dan reduksi dimensi, membaca dan menafsirkan kelompok, menguji kestabilan, lalu melaporkan hasil dengan jujur. Semuanya dibangun di atas [Level 4](../clustering-algorithms/index.md) (algoritma) dan [Level 5](../clustering-evaluation/index.md) (metrik evaluasi).

Bab-bab memakai **data sintetis** (`make_blobs`, `make_moons`, dan sejenisnya) dengan seed tetap, serta dataset **Mall Customers**. Setiap potongan kode diikuti penjelasannya. Hasil eksperimen disimpan sebagai CSV dan JSON di `examples/level-6/results/`, bersama catatan konfigurasi, seed, dan versi pustaka.

!!! note "Batas dengan Level 5 dan Level 7"
    Level 5 mengajarkan **definisi dan makna metrik**. Level 6 **memakai** metrik itu sebagai alat dalam eksperimen. Proyek riset penuh (studi literatur, perumusan celah riset, dan penulisan makalah) adalah materi Level 7.

## Daftar bab

| Bab | Judul | Status |
|---|---|---|
| 1 | [Introduction to Clustering Experiments](01-introduction-to-clustering-experiments.md) | Selesai |
| 2 | [Experimental Design and Configuration](02-experimental-design-and-configuration.md) | Selesai |
| 3 | [Hyperparameter Tuning and Optimization](03-hyperparameter-tuning-and-optimization.md) | Selesai |
| 4 | [Algorithm Comparison and Benchmarking](04-algorithm-comparison-and-benchmarking.md) | Selesai |
| 5 | [Feature Selection and Impact Analysis](05-feature-selection-and-impact-analysis.md) | Selesai |
| 6 | [Dimensionality Reduction and PCA](06-dimensionality-reduction-and-pca.md) | Selesai |
| 7 | [Cluster Interpretation and Profiling](07-cluster-interpretation-and-profiling.md) | Selesai |
| 8 | [Cluster Visualization and Analysis](08-cluster-visualization-and-analysis.md) | Selesai |
| 9 | [Cluster Stability and Reproducibility](09-cluster-stability-and-reproducibility.md) | Selesai |
| 10 | [Experimental Reporting and Interpretation](10-experimental-reporting-and-interpretation.md) | Selesai |

## Prasyarat

- Level 3 ([Fundamental Clustering](../fundamental-clustering/index.md)), terutama alur kerja clustering.
- Level 4 ([Clustering Algorithms](../clustering-algorithms/index.md)).
- Level 5 ([Clustering Evaluation](../clustering-evaluation/index.md)).
- Python dasar dan kemampuan menjalankan skrip atau notebook.
