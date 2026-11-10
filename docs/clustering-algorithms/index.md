# Level 4 — Clustering Algorithms

Level ini mempelajari lima algoritma clustering inti: cara kerjanya, dasar matematikanya, cara memakainya dengan scikit-learn, dan cara membaca hasilnya. Semuanya dibangun di atas fondasi [Level 3](../fundamental-clustering/index.md): centroid, jarak, ruang fitur, dan alur kerja clustering.

Bab-bab memakai **data sintetis kecil** (`make_blobs`, `make_moons`, dan sejenisnya) dengan `random_state=42`, supaya bentuk kelompok bisa digambar dan perilaku tiap algoritma terlihat jelas. Beberapa bab juga memakai dataset **Mall Customers** seperti Level 2 dan 3.

!!! note "Batas dengan Level 5"
    Level 4 fokus pada **cara kerja dan cara memakai** algoritma. Penilaian formal hasil clustering (metrik evaluasi, interpretasi skor, validasi) adalah materi [Level 5](../curriculum/index.md).

## Daftar bab

| Bab | Judul | Status |
|---|---|---|
| 1 | [Introduction to Clustering Algorithms](01-introduction-to-clustering-algorithms.md) | Siap ditinjau |
| 2 | [K-Means Clustering](02-k-means-clustering.md) | Siap ditinjau |
| 3 | [Hierarchical Clustering](03-hierarchical-clustering.md) | Siap ditinjau |
| 4 | [DBSCAN Clustering](04-dbscan-clustering.md) | Siap ditinjau |
| 5 | [Gaussian Mixture Models (GMM)](05-gaussian-mixture-models.md) | Siap ditinjau |
| 6 | [Mean Shift Clustering](06-mean-shift-clustering.md) | Siap ditinjau |
| 7 | [Comparison of Clustering Algorithms](07-comparison-of-clustering-algorithms.md) | Siap ditinjau |

## Prasyarat

- Level 3 ([Fundamental Clustering](../fundamental-clustering/index.md)), terutama Bab 3 (centroid), Bab 5 (jarak), dan Bab 7 (alur kerja).
- Python dasar dan kemampuan menjalankan skrip atau notebook.
