# Bab 7 — Clustering Workflow

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menyebut dan menjelaskan tahapan sebuah proyek clustering dari awal sampai laporan.
- [x] Merumuskan masalah clustering yang jelas sebelum menyentuh data.
- [x] Menghubungkan tiap tahap dengan konsep dari Bab 1 sampai 6 dan Level 2.
- [x] Menjalankan alur kerja lengkap pada dataset Mall Customers.
- [x] Memilih jumlah kelompok dengan bantuan *silhouette score* (pratinjau Level 5).
- [x] Memeriksa kestabilan hasil dan menafsirkan kelompok menjadi temuan yang bisa dilaporkan.
- [x] Mengenali kesalahan umum dalam proyek clustering.
- [x] Menjelaskan apa yang akan dipelajari di Level 4.

## Introduction

Kamu sudah mempelajari bagian-bagiannya: apa itu clustering (Bab 1), seperti apa kelompok yang baik (Bab 2), centroid (Bab 3), kemiripan dan jarak (Bab 4 dan 5), serta ruang fitur (Bab 6). Level 2 mengajarkan cara mengenal dan membersihkan data. Bab ini **merangkai semuanya** menjadi satu alur kerja yang bisa kamu pakai pada proyek apa pun.

Penting dipahami bahwa memilih algoritma hanya **satu langkah kecil** di tengah alur. Sebagian besar kualitas hasil ditentukan oleh langkah **sebelum** dan **sesudah** algoritma: merumuskan masalah, memahami data, memilih fitur, menyamakan skala, dan menafsirkan hasil.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Workflow** | Urutan langkah kerja dari masalah sampai laporan |
| **Problem definition** | Merumuskan apa yang ingin dijawab dan untuk apa hasilnya dipakai |
| **Model fitting** | Menjalankan algoritma pada data untuk membentuk kelompok |
| **Cluster assignment** | Memberi nomor kelompok pada tiap data |
| **Cluster evaluation** | Menilai kualitas kelompok dengan ukuran tertentu (Level 5) |
| **Cluster interpretation** | Memberi arti pada kelompok berdasarkan profilnya |
| **Silhouette score** | Ukuran kualitas kelompok dari −1 sampai 1. Makin tinggi, makin baik terpisah dan padat. Dibahas rinci di Level 5 |

## Detailed Explanation

### Gambaran alur

```mermaid
flowchart TD
    A[1. Definisi masalah] --> B[2. Memahami dataset]
    B --> C[3. Menyiapkan data]
    C --> D[4. Memilih fitur]
    D --> E[5. Menyamakan skala]
    E --> F[6. Memilih ukuran jarak]
    F --> G[7. Memilih algoritma]
    G --> H[8. Melatih model dan memberi kelompok]
    H --> I[9. Evaluasi kelompok]
    I --> J[10. Menafsirkan kelompok]
    J --> K[11. Visualisasi dan laporan]
    I -. tidak memuaskan .-> D
    I -. tidak memuaskan .-> G
```

Perhatikan panah putus-putus: alur ini **berulang**. Jika evaluasi atau tafsiran tidak memuaskan, kamu kembali memilih fitur atau algoritma.

### 1. Problem definition (definisi masalah)

Mulailah dengan pertanyaan, bukan dengan algoritma. Contoh yang baik: *"Adakah kelompok pelanggan berdasarkan pendapatan dan perilaku belanja, yang bisa kita beri promosi berbeda?"* Pertanyaan ini memberi tahu fitur apa yang relevan dan seperti apa hasil yang berguna. Pertanyaan yang buruk: "Mari clusteringkan data ini."

### 2. Dataset understanding (memahami dataset)

Periksa ukuran data, tipe kolom, rentang nilai, nilai kosong, dan duplikat (Level 2 Bab 1 sampai 6). Tujuannya menghindari kejutan di tengah proyek.

### 3. Data preparation (menyiapkan data)

Tangani nilai kosong, duplikat, dan outlier (Level 2 Bab 5 sampai 8). Ubah kolom kategori menjadi angka bila perlu (Bab 9).

### 4. Feature selection (memilih fitur)

Pilih kolom yang relevan dengan pertanyaanmu. Buang kolom ID. Ingat Bab 6: fitur tak relevan merusak jarak. Fitur yang tidak dipakai untuk clustering masih berguna untuk **menafsirkan** kelompok nanti (misalnya `Age`).

### 5. Feature scaling (menyamakan skala)

Standardisasi atau normalisasi agar tidak ada fitur yang mendominasi jarak (Bab 5 dan Level 2 Bab 10).

### 6. Distance measurement (ukuran jarak)

Pilih metrik yang cocok dengan makna datamu. Untuk fitur numerik berskala sama, Euclidean adalah pilihan umum (Bab 5).

### 7. Algorithm selection (memilih algoritma)

Pilih algoritma yang cocok dengan bentuk dan ukuran kelompok yang kamu perkirakan (Bab 2). Algoritma yang ada: *K-Means* (kelompok berbentuk bola), *hierarchical clustering* (hubungan bertingkat), *DBSCAN* (kelompok berdasarkan kepadatan, tahan outlier), dan lain-lain. Semuanya dibahas di Level 4. Pada bab ini kita memakai K-Means sebagai alat bantu.

### 8. Model fitting dan cluster assignment

Jalankan algoritma pada data. Hasilnya nomor kelompok untuk tiap data (Bab 1) dan, untuk algoritma berbasis pusat, centroid (Bab 3).

### 9. Cluster evaluation (evaluasi)

Nilai kualitas kelompok. Karena tidak ada label, kita memakai ukuran internal seperti *silhouette score* yang menggabungkan kekompakan dan keterpisahan (Bab 2). Level 5 membahas berbagai ukuran evaluasi.

### 10. Cluster interpretation (penafsiran)

Hitung profil tiap kelompok (rata-rata fitur), lihat ukurannya, dan beri arti dalam bahasa bisnis atau riset. Kelompok yang tidak bisa dijelaskan sering menandakan masalah pada fitur atau jumlah kelompok.

### 11. Visualization dan reporting

Gambarkan hasilnya dan susun laporan: pertanyaan, data, langkah penyiapan, jumlah kelompok dan alasannya, profil tiap kelompok, serta rekomendasi dan keterbatasan.

### Kesalahan umum dalam proyek clustering

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Langsung menjalankan algoritma tanpa merumuskan masalah | Hasil tidak berguna | Tulis pertanyaan dulu |
| Memakai semua kolom, termasuk ID | Jarak menyesatkan | Pilih fitur (Bab 6) |
| Lupa menyamakan skala | Satu fitur mendominasi | Standardisasi (Bab 5) |
| Memutuskan jumlah kelompok hanya dengan menebak | Kelompok dipaksakan | Uji beberapa nilai dan evaluasi |
| Menjalankan sekali dan percaya | Hasil bisa tidak stabil | Periksa kestabilan |
| Menganggap kelompok sebagai fakta mutlak | Kesimpulan berlebihan | Ingat bahwa hasil bergantung pada fitur dan metode |
| Tidak menafsirkan kelompok | Angka tanpa arti | Buat profil dan beri nama kelompok |

## Mathematical Foundation

Bab ini tidak memperkenalkan rumus baru, tetapi memakai satu ukuran evaluasi yang akan dibahas penuh di Level 5. Untuk sebuah titik \( i \):

- \( a(i) \) adalah **rata-rata jarak titik \( i \) ke anggota lain di kelompoknya sendiri** (makin kecil makin baik, cerminan kekompakan, Bab 2).
- \( b(i) \) adalah **rata-rata jarak titik \( i \) ke anggota kelompok terdekat lainnya** (makin besar makin baik, cerminan keterpisahan).

$$
s(i) = \frac{b(i) - a(i)}{\max\{a(i),\, b(i)\}}
$$

Nilai \( s(i) \) berada di antara −1 dan 1. Silhouette score sebuah pengelompokan adalah rata-rata \( s(i) \) semua titik.

### Contoh hitung manual

Misalkan titik \( i \) punya \( a(i) = 2 \) dan \( b(i) = 6 \).

1. Selisih: \( b - a = 6 - 2 = 4 \).
2. Penyebut: \( \max\{2, 6\} = 6 \).
3. \( s(i) = 4/6 \approx 0{,}667 \).

**Interpretasi.** Titik ini jauh lebih dekat ke kelompoknya sendiri (rata-rata jarak 2) daripada ke kelompok tetangga (6), jadi nilainya mendekati 1: ditempatkan dengan baik. Jika \( a(i) = 5 \) dan \( b(i) = 5 \), maka \( s(i) = 0 \): titik berada di batas. Jika \( a(i) > b(i) \), nilainya negatif: titik mungkin salah kelompok.

## Python Implementation

Kita kerjakan dalam sembilan langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-3/07_clustering_workflow.py`, dan versi notebook-nya di `notebooks/level-3/07-clustering-workflow.ipynb`.

**Langkah 1 (definisi masalah)** ditulis sebagai pertanyaan, bukan kode: *"Adakah kelompok pelanggan menurut pendapatan dan perilaku belanja, yang bisa diberi promosi berbeda?"*

**Input yang diharapkan:** `data/mall_customers.csv`, dijalankan dari folder utama proyek.

### Langkah 2 — Pahami dataset

```python
--8<-- "level-3/07_clustering_workflow.py:understand"
```

```text title="Output"
--8<-- "level-3/outputs/07/understand.txt"
```

**Penjelasan:**

- `df.shape` memberi ukuran data (baris, kolom).
- `df.isna().sum().sum()` menghitung total sel kosong: `isna()` menandai sel kosong, `.sum()` pertama menjumlahkan per kolom, `.sum()` kedua menjumlahkan semua kolom. `int(...)` merapikan tampilannya.
- `df.duplicated().sum()` menghitung baris ganda.
- `df.describe().round(1).loc[["min", "mean", "max"]]` menampilkan ringkasan statistik, lalu **memilih hanya baris** minimum, rata-rata, dan maksimum agar tampil ringkas.

### Langkah 3 — Pilih fitur

```python
--8<-- "level-3/07_clustering_workflow.py:prepare"
```

```text title="Output"
--8<-- "level-3/outputs/07/prepare.txt"
```

**Penjelasan:**

- `features` adalah daftar kolom yang dipakai: pendapatan dan skor belanja, sesuai pertanyaan masalah.
- `X = df[features]` membuat tabel hanya berisi kolom itu.
- Daftar `[c for c in df.columns if c not in features]` menampilkan kolom yang **tidak** dipakai: `CustomerID` (hanya nomor urut), `Gender` (kategori, perlu encoding), dan `Age` (kita simpan untuk menafsirkan kelompok).

### Langkah 4 — Samakan skala

```python
--8<-- "level-3/07_clustering_workflow.py:scale"
```

```text title="Output"
--8<-- "level-3/outputs/07/scale.txt"
```

**Penjelasan:**

- `StandardScaler()` membuat alat standardisasi. `.fit_transform(X)` mempelajari rata-rata dan simpangan baku tiap fitur, lalu mengubah data sehingga rata-rata 0 dan simpangan baku 1.
- Kita cetak rata-rata dan simpangan baku hasilnya untuk memastikan standardisasi berjalan. Tambahan `+ 0.0` hanya menghindari tampilan `-0.`.
- Hasil `X_scaled` adalah larik NumPy, dan itulah yang akan dikelompokkan.

### Langkah 5 — Pilih jumlah kelompok

```python
--8<-- "level-3/07_clustering_workflow.py:choose"
```

```text title="Output"
--8<-- "level-3/outputs/07/choose.txt"
```

![Grafik silhouette score terhadap jumlah kelompok 2 sampai 8, puncak di k=5](../assets/level-3/07-pemilihan-k.png)

**Penjelasan:**

- Kita mencoba `k` dari 2 sampai 8. Untuk tiap `k`, `KMeans(...).fit_predict(X_scaled)` membuat kelompok dan `silhouette_score(X_scaled, labels_k)` menghitung kualitasnya.
- `scores` adalah kamus (*dictionary*): kunci adalah `k`, nilai adalah skornya.
- `max(scores, key=scores.get)` mengambil **kunci** dengan nilai terbesar, yaitu `k` terbaik menurut silhouette.
- Bagian grafik memplot skor terhadap `k`.

!!! note "Silhouette hanya salah satu petunjuk"
    Jumlah kelompok sebaiknya dipilih dengan beberapa petunjuk: silhouette, pemahaman bisnis, dan kemudahan menafsirkan. Silhouette membantu, tetapi bukan keputusan akhir. Level 5 membahas ukuran lain.

### Langkah 6 — Latih model dan beri nomor kelompok

```python
--8<-- "level-3/07_clustering_workflow.py:fit"
```

```text title="Output"
--8<-- "level-3/outputs/07/fit.txt"
```

**Penjelasan:**

- `KMeans(n_clusters=best_k, ...)` membuat model dengan jumlah kelompok terpilih. `random_state=42` mengunci hasil.
- `fit_predict(X_scaled)` melatih model dan memberi nomor kelompok. Kita simpan di kolom baru `df["Cluster"]`.
- `value_counts().sort_index()` menghitung jumlah anggota tiap kelompok.

### Langkah 7 — Periksa kestabilan

```python
--8<-- "level-3/07_clustering_workflow.py:stability"
```

```text title="Output"
--8<-- "level-3/outputs/07/stability.txt"
```

**Penjelasan:**

- Kita menjalankan K-Means lagi dengan lima `random_state` berbeda (0 sampai 4).
- `adjusted_rand_score(a, b)` membandingkan dua pengelompokan **tanpa peduli nomor kelompoknya**. Nilai 1 berarti identik, nilai sekitar 0 berarti tidak lebih mirip daripada kebetulan.
- Jika hasil berubah-ubah menurut seed, kelompok tidak stabil dan harus dicurigai.

### Langkah 8 — Tafsirkan kelompok

```python
--8<-- "level-3/07_clustering_workflow.py:interpret"
```

```text title="Output"
--8<-- "level-3/outputs/07/interpret.txt"
```

**Penjelasan:**

- `df.groupby("Cluster")[features + ["Age"]].mean()` menghitung rata-rata tiap fitur **dalam satuan asli** per kelompok. Kita tambahkan `Age` meski tidak dipakai saat clustering, untuk memperkaya tafsiran.
- `.round(1)` membulatkan satu angka di belakang koma.
- `profile.insert(0, "Jumlah", ...)` menambahkan kolom jumlah anggota di posisi paling kiri.

### Langkah 9 — Visualisasi akhir dan laporan

```python
--8<-- "level-3/07_clustering_workflow.py:plot"
```

![Scatter plot pelanggan dalam lima warna dengan centroid hitam](../assets/level-3/07-segmentasi-akhir.png)

**Penjelasan:**

- `scaler.inverse_transform(model.cluster_centers_)` mengubah centroid dari skala standar **kembali ke satuan asli** (ribu dolar dan skor) agar pas digambar di atas data asli. Ini penting: centroid model berada di ruang terstandardisasi.
- Selebihnya sama seperti Bab 1: gambar titik per kelompok dengan warna berbeda, lalu centroid sebagai tanda `X`.

```python
--8<-- "level-3/07_clustering_workflow.py:report"
```

```text title="Output"
--8<-- "level-3/outputs/07/report.txt"
```

**Penjelasan:**

- `profile.iterrows()` mengulang baris tabel profil satu per satu: `k` adalah nomor kelompok, `row` datanya.
- Kita hitung persentase anggota (`jumlah / total * 100`) dan menyusun satu kalimat laporan per kelompok memakai f-string.

## Code Explanation

| Yang kamu lihat | Artinya |
|---|---|
| `StandardScaler().fit_transform(X)` | Menyamakan skala fitur |
| `KMeans(n_clusters=k, n_init=10, random_state=42)` | Model dengan k kelompok, hasil dapat diulang |
| `silhouette_score(X, labels)` | Kualitas kelompok (−1 sampai 1) |
| `adjusted_rand_score(a, b)` | Kesamaan dua pengelompokan, tidak peduli nomor |
| `groupby("Cluster").mean()` | Profil tiap kelompok |
| `scaler.inverse_transform(...)` | Kembali ke satuan asli |

Pola umumnya: **pahami → siapkan → skalakan → kelompokkan → evaluasi → periksa stabil → tafsirkan → laporkan.**

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
pip install -r requirements-notebooks.txt
python examples/level-3/07_clustering_workflow.py
```

Skrip membuat dua gambar di `docs/assets/level-3/`. Untuk notebook:

```powershell
jupyter notebook notebooks/level-3/07-clustering-workflow.ipynb
```

## Expected Output

Semua output berasal dari eksekusi nyata skrip (Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, matplotlib 3.11.1). Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).


![Grafik silhouette score terhadap jumlah kelompok 2 sampai 8, puncak di k=5](../assets/level-3/07-pemilihan-k.png)

![Scatter plot pelanggan dalam lima warna dengan centroid hitam](../assets/level-3/07-segmentasi-akhir.png)

### Interpretasi output

**Memahami dataset.** 200 baris, 5 kolom, tanpa nilai kosong dan tanpa duplikat. Data siap dipakai tanpa pembersihan tambahan.

**Pemilihan jumlah kelompok.** Silhouette tertinggi 0,555 pada `k = 5`, diikuti 0,540 pada `k = 6` dan 0,528 pada `k = 7`. Selisih antara 5 dan 6 kecil, jadi `k = 6` juga layak dipertimbangkan. Di sinilah pertimbangan lain (pemahaman bisnis dan kemudahan menafsirkan) ikut berperan. Kita memakai `k = 5` karena silhouette tertinggi dan hasilnya mudah ditafsirkan, sesuai dengan Bab 1.

**Kestabilan.** Kelima seed menghasilkan ARI = 1,000: pengelompokannya identik. Pada data ini struktur kelompoknya cukup jelas sehingga hasil stabil.

**Profil kelompok.**

| Kelompok | Jumlah (%) | Pendapatan | Skor belanja | Usia | Kemungkinan arti |
|---|---|---|---|---|---|
| 0 | 81 (40,5%) | 55,3 | 49,5 | 42,7 | Menengah di keduanya. Kelompok terbesar |
| 1 | 39 (19,5%) | 86,5 | 82,1 | 32,7 | Mampu dan aktif berbelanja |
| 2 | 22 (11,0%) | 25,7 | 79,4 | 25,3 | Pendapatan rendah tetapi aktif berbelanja, paling muda |
| 3 | 35 (17,5%) | 88,2 | 17,1 | 41,1 | Mampu tetapi jarang berbelanja |
| 4 | 23 (11,5%) | 26,3 | 20,9 | 45,2 | Pendapatan rendah dan jarang berbelanja |

Angka ini sama dengan hasil Bab 1 karena fitur dan jumlah kelompoknya sama. Yang berbeda di bab ini adalah **proses**: kita membuktikan data bersih, memilih jumlah kelompok dengan alasan, memeriksa kestabilan, dan menafsirkan dengan variabel tambahan (`Age`).

## Practical Examples

**Contoh laporan singkat (dari output di atas).**

> Dari 200 pelanggan, ditemukan lima segmen berdasarkan pendapatan tahunan dan skor belanja. Segmen terbesar (40,5%) berpendapatan dan berbelanja sedang. Segmen "mampu tetapi jarang berbelanja" (17,5%, pendapatan rata-rata 88,2 ribu dolar, skor belanja 17,1) adalah peluang promosi karena potensi belanjanya besar. Segmen "pendapatan rendah tetapi aktif berbelanja" (11,0%) paling muda (rata-rata 25,3 tahun). Hasil stabil pada lima seed berbeda. Keterbatasan: hanya dua fitur yang dipakai, dan nama segmen adalah tafsiran kami.

**Alur yang sama untuk bidang lain.** Ganti dataset: pasien dengan hasil laboratorium (kelompok pasien), artikel berita (topik), atau sensor (kondisi mesin). Tahapannya sama: rumuskan, pahami, siapkan, pilih fitur, skalakan, kelompokkan, evaluasi, tafsirkan, laporkan.

**Mengulang alur.** Jika `Age` ditambahkan sebagai fitur, silhouette dan kelompoknya berubah. Itu bukan kegagalan, melainkan eksperimen: alur ini memang berulang. Level 6 membahas eksperimen dan interpretasi lebih jauh.

### Persiapan untuk Level 4

Dengan fondasi Level 3, kamu siap mempelajari algoritma di Level 4:

| Konsep Level 3 | Dipakai di Level 4 |
|---|---|
| Centroid dan medoid (Bab 3) | K-Means dan K-Medoids |
| Jarak dan kemiripan (Bab 4 dan 5) | Hierarchical clustering dan semua algoritma |
| Kepadatan dan bentuk (Bab 2) | DBSCAN |
| Keanggotaan batas (Bab 2) | Soft clustering |
| Ruang fitur dan dimensi (Bab 6) | Memilih fitur dan mengurangi dimensi |

## Hands-on Exercises

1. Tambahkan `Age` ke daftar `features`. Berapa `k` terbaik menurut silhouette, dan berapa skornya?
2. Ubah rentang `k` menjadi 2 sampai 10. Apakah `k` terbaik berubah?
3. Hitung manual \( s(i) \) jika \( a(i) = 3 \) dan \( b(i) = 4 \).
4. Sebutkan tiga langkah alur kerja yang paling sering dilewati pemula, dan akibatnya.
5. Tulis tiga kalimat laporan untuk kelompok 3 menggunakan angka dari output.

??? question "Jawaban"
    1. Hasil eksekusi nyata dengan tiga fitur (`Age`, `Annual Income (k$)`, `Spending Score (1-100)`) yang distandardisasi: silhouette tertinggi **0,428 pada `k = 6`**, dengan `k = 5` mendapat 0,417. Skor lebih rendah daripada dua fitur (0,555), dan `k` terbaik bergeser dari 5 ke 6. Menambah fitur mengubah struktur data.
    2. Jalankan kodenya. Bandingkan skor `k` = 9 dan 10 dengan puncak di `k` = 5. Kamu akan melihat apakah ada `k` yang mengalahkan 0,555.
    3. \( s = (4 - 3)/\max\{3, 4\} = 1/4 = 0{,}25 \). Titik sedikit lebih dekat ke kelompoknya sendiri daripada ke kelompok tetangga, tetapi tidak jelas.
    4. Contoh: (a) merumuskan masalah, akibatnya hasil tidak relevan. (b) menyamakan skala, akibatnya satu fitur mendominasi jarak. (c) menafsirkan dan memeriksa kestabilan, akibatnya angka tanpa arti dan kesimpulan yang rapuh.
    5. Contoh jawaban: "Kelompok 3 berisi 35 pelanggan (17,5%) dengan pendapatan rata-rata 88,2 ribu dolar tetapi skor belanja hanya 17,1. Usia rata-rata 41,1 tahun. Segmen ini bernilai karena mampu membeli tetapi jarang berbelanja, sehingga cocok untuk survei dan promosi khusus."

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| Skor silhouette sangat rendah (di bawah 0,2) | Data tidak punya struktur kelompok jelas, atau fitur kurang tepat | Tinjau fitur, skala, dan jumlah kelompok. Mungkin data memang tidak berkelompok |
| Hasil berbeda tiap dijalankan | `random_state` tidak dikunci atau `n_init` kecil | Tetapkan `random_state` dan `n_init=10` |
| Centroid tergambar di tempat yang salah | Memakai centroid terstandardisasi pada grafik data asli | Pakai `scaler.inverse_transform(...)` |
| `ValueError: could not convert string to float` | Kolom teks ikut dikelompokkan | Pilih fitur numerik atau lakukan encoding dulu |
| `k` terbaik berubah drastis saat fitur ditambah | Struktur data berubah | Wajar. Bandingkan beberapa konfigurasi dan pilih yang paling bermakna |
| Kelompok tidak bisa dijelaskan | Fitur kurang relevan atau `k` terlalu besar | Kurangi `k` atau ganti fitur (Bab 6) |

## Summary

- Alur proyek clustering: **definisi masalah → pahami data → siapkan → pilih fitur → skalakan → ukuran jarak → algoritma → model dan kelompok → evaluasi → tafsir → laporan**, dan alur ini berulang.
- Memilih algoritma hanya satu langkah. Kualitas hasil sangat ditentukan langkah sebelum dan sesudahnya.
- Pada Mall Customers: data bersih (200 baris, 0 kosong, 0 duplikat), silhouette tertinggi 0,555 pada `k = 5`, hasil stabil (ARI = 1,000 pada lima seed), dan lima kelompok bisa ditafsirkan.
- Silhouette \( s(i) = \frac{b(i) - a(i)}{\max\{a(i), b(i)\}} \) menggabungkan kekompakan dan keterpisahan (Bab 2). Pembahasan lengkapnya di Level 5.
- Kamu kini siap mempelajari algoritma di **Level 4**: K-Means, hierarchical clustering, DBSCAN, dan lainnya.

## References

- Rousseeuw, P. J. (1987). Silhouettes: a graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53–65.
- Scikit-learn documentation: [`silhouette_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html) dan [`adjusted_rand_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html).
- Scikit-learn documentation: [*Clustering*](https://scikit-learn.org/stable/modules/clustering.html).
- Han, J., Kamber, M., & Pei, J. *Data Mining: Concepts and Techniques* (Morgan Kaufmann), bab tentang analisis klaster.
