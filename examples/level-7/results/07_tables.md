**Tabel 1. RQ3, perbandingan algoritma (K = 2, ruang baseline)**

| Algoritma | Kelompok | Silhouette (naik lebih baik) | Davies-Bouldin (turun lebih baik) | Calinski-Harabasz (naik lebih baik) | ARI vs diagnosis | NMI vs diagnosis |
|---|---|---|---|---|---|---|
| KMeans | 2 | 0,343 | 1,321 | 267,692 | 0,654 | 0,532 |
| Agglomerative | 2 | 0,339 | 1,370 | 248,629 | 0,575 | 0,457 |
| GMM | 2 | 0,314 | 1,377 | 247,284 | 0,774 | 0,661 |
| DBSCAN | tidak ada konfigurasi valid | - | - | - | - | - |

**Tabel 2. RQ2, ARI terhadap baseline menurut perlakuan skala**

| Perlakuan skala | ARI rata-rata | ARI minimum | ARI maksimum | proporsi_ari>=0.95 |
|---|---|---|---|---|
| StandardScaler (baseline) | 0,982 | 0,965 | 1,000 | 1,000 |
| tanpa skala | 0,496 | 0,496 | 0,496 | 0,000 |
| MinMaxScaler | 0,896 | 0,896 | 0,896 | 0,000 |
