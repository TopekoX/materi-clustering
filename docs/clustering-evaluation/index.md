# Level 5 — Clustering Evaluation

Level ini mengajarkan cara **menilai hasil clustering**: apakah kelompok yang ditemukan rapat, terpisah, dan bermakna. Kamu akan mengenal metrik internal (Inertia, Silhouette, Davies-Bouldin, Calinski-Harabasz), Elbow Method untuk membandingkan jumlah kelompok, dan metrik eksternal (ARI, NMI, Homogeneity, Completeness, V-measure) bila ada label acuan.

Bab-bab memakai **data sintetis** (`make_blobs`, `make_moons`, `make_circles`) dengan `random_state=42` supaya hasil bisa dihitung ulang dan dibandingkan dengan bab. Beberapa bab juga memakai dataset **Mall Customers**. Setiap potongan kode diikuti penjelasannya.

!!! note "Batas dengan Level 4 dan Level 6"
    Level 4 mengajarkan **cara kerja** algoritma. Level 5 mengajarkan **cara menilai hasilnya**. Perancangan eksperimen yang sistematis (pencarian parameter, pengulangan, interpretasi mendalam) adalah materi Level 6.

## Daftar bab

| Bab | Judul | Status |
|---|---|---|
| 1 | [Introduction to Clustering Evaluation](01-introduction-to-clustering-evaluation.md) | Selesai |
| 2 | [Internal Clustering Evaluation](02-internal-clustering-evaluation.md) | Selesai |
| 3 | [Inertia and WCSS](03-inertia-and-wcss.md) | Selesai |
| 4 | [Elbow Method](04-elbow-method.md) | Selesai |
| 5 | [Silhouette Score](05-silhouette-score.md) | Selesai |
| 6 | [Davies-Bouldin Index](06-davies-bouldin-index.md) | Selesai |
| 7 | [Calinski-Harabasz Index](07-calinski-harabasz-index.md) | Selesai |
| 8 | [External Evaluation and Metric Comparison](08-external-evaluation-and-metric-comparison.md) | Selesai |

## Prasyarat

- Level 3 ([Fundamental Clustering](../fundamental-clustering/index.md)), terutama jarak dan centroid.
- Level 4 ([Clustering Algorithms](../clustering-algorithms/index.md)), terutama K-Means dan DBSCAN.
- Python dasar dan kemampuan menjalankan skrip atau notebook.
