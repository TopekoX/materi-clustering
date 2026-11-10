# Laporan Eksperimen: Pengelompokan Pelanggan Mall Customers dengan K-Means

## 1. Pertanyaan dan tujuan

Apakah pelanggan dapat dikelompokkan berdasarkan pendapatan tahunan dan skor belanja, dan seberapa konsisten pengelompokan itu terhadap perubahan seed, sampel, dan jumlah kelompok (K)? Eksperimen ini bersifat **eksploratif**: tidak ada label acuan dan tidak ada hipotesis yang diuji secara statistik formal.

## 2. Data

Mall Customers, 200 pelanggan, kolom: CustomerID, Gender, Age, Annual Income (k$), Spending Score (1-100). Nilai kosong: 0. Perempuan 112, laki-laki 88. Rentang pendapatan 15 sampai 137 k$, skor belanja 1 sampai 99, umur 18 sampai 70 tahun. Sumber: Kaggle (salinan di `data/mall_customers.csv`). Sidik jari data: `edb2a3858344`.

## 3. Praproses dan fitur

Fitur untuk clustering: Annual Income (k$), Spending Score (1-100). Praproses: z-score per kolom. Umur dan gender **tidak** dipakai clustering dan hanya dipakai untuk menggambarkan kelompok.

## 4. Algoritma dan konfigurasi

KMeans n_clusters=5 n_init=10, seed 42. Untuk memilih K, K = 2 sampai 8 dibandingkan memakai Silhouette dan kestabilan terhadap sampel (80% data, 50 pengulangan). Kestabilan tiap kelompok dihitung dengan 100 sampel bootstrap.

## 5. Hasil: memilih K

| K | Silhouette | Kestabilan (rata-rata) | Kestabilan (minimum) |
|---|---|---|---|
| 2 | 0,321 | 0,313 | -0,013 |
| 3 | 0,467 | 1,000 | 1,000 |
| 4 | 0,494 | 0,776 | 0,547 |
| 5 | 0,555 | 0,987 | 0,927 |
| 6 | 0,540 | 0,947 | 0,840 |
| 7 | 0,528 | 0,895 | 0,612 |
| 8 | 0,455 | 0,895 | 0,697 |

Silhouette tertinggi pada K = 5 (0,555). Kestabilan rata-rata tertinggi pada K = 3 (1,000). Untuk K = 5, Silhouette 0,555 dan kestabilan rata-rata 0,987 (minimum 0,927).

Kedua kriteria **tidak menunjuk K yang sama**. Silhouette menilai keterpisahan dan kekompakan kelompok. Kestabilan menilai konsistensi hasil terhadap sampel. K = 3 konsisten tetapi lebih longgar dalam keterpisahan. Kami memilih K = 5 karena Silhouette tertinggi dan kestabilannya juga tinggi, bukan karena K = 5 terbukti benar.

## 6. Hasil: profil kelompok (K = 5)

| Kelompok | Ukuran | Pendapatan (k$), rata-rata | Skor belanja, rata-rata | Umur, median | Jaccard (kestabilan) |
|---|---|---|---|---|---|
| A | 81 | 55,3 | 49,5 | 46,0 | 0,979 |
| B | 39 | 86,5 | 82,1 | 32,0 | 1,000 |
| C | 35 | 88,2 | 17,1 | 42,0 | 0,970 |
| D | 23 | 26,3 | 20,9 | 46,0 | 0,980 |
| E | 22 | 25,7 | 79,4 | 23,5 | 0,990 |

Ukuran kelompok: A (81), B (39), C (35), D (23), E (22). Perbedaan umur antar kelompok lebih besar daripada yang diharapkan secara acak (selisih rata-rata terbesar dan terkecil 19,945 tahun, batas acak 95% 9,890, p = 0,0005, uji permutasi 2000 kali). Ini asosiasi, bukan sebab: kami tidak menyimpulkan bahwa umur memengaruhi perilaku belanja.

## 7. Keterbatasan

- Hanya satu dataset kecil (200 pelanggan), satu algoritma (K-Means), dan dua fitur.
- Kelompok terkecil hanya 22 pelanggan, sehingga rata-rata kelompok itu bergantung pada sedikit data.
- Kestabilan menunjukkan konsistensi terhadap sampel dan seed, bukan bahwa kelompok itu nyata atau berguna.
- Nama kelompok pada profil adalah label deskriptif dan bergantung pada ambang yang dipilih.
- Hasil belum diuji pada pelanggan di luar data ini.

## 8. Kesimpulan yang didukung data

Pada data ini, K-Means dengan K = 5 pada pendapatan dan skor belanja menghasilkan lima kelompok yang konsisten terhadap seed (dengan n_init = 10) dan sampel, dengan Jaccard tiap kelompok antara 0,970 dan 1,000. Pilihan K = 5 didukung oleh Silhouette tertinggi, tetapi K = 3 lebih stabil.

## 9. Reproduksibilitas

Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, SciPy 1.18.1, Matplotlib 3.11.1, Windows. Seed 42. File hasil: `07_cluster_profile.csv`, `09_stability_by_k.csv`, `09_cluster_jaccard.csv`, `09_config.json`.
