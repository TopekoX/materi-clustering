# Bab 4 — Similarity and Dissimilarity

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan *similarity* (kemiripan) dan *dissimilarity* (ketidakmiripan).
- [x] Menjelaskan hubungan antara *similarity* dan *distance* (jarak).
- [x] Menjelaskan mengapa ukuran kemiripan menentukan hasil clustering.
- [x] Menghitung *pairwise distance* dan menyusunnya menjadi *distance matrix* serta *similarity matrix*.
- [x] Membaca matriks jarak dan menemukan pasangan data paling mirip.
- [x] Mengenali perbedaan penanganan data numerik dan data kategori.
- [x] Menghindari kesalahan umum saat mengukur kemiripan.

## Introduction

Bab 1 mengatakan clustering mengelompokkan data yang **mirip**. Tetapi komputer tidak punya rasa "mirip". Ia hanya bisa menghitung angka. Jadi sebelum algoritma apa pun bisa bekerja, kita harus **menerjemahkan "mirip" menjadi angka**.

Bayangkan dua pelanggan: yang satu berusia 19 tahun dengan skor belanja 39, yang lain berusia 21 tahun dengan skor belanja 81. Mirip atau tidak? Jawabannya bergantung pada cara kita mengukur, dan cara mengukur itu **menentukan kelompok yang terbentuk**. Mengubah cara mengukur berarti mengubah hasil clustering, walaupun datanya sama.

Bab ini membahas konsepnya secara umum. Bab 5 melanjutkannya dengan rumus jarak yang spesifik (Euclidean, Manhattan, Minkowski, cosine).

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Similarity** | Ukuran seberapa **mirip** dua data. Makin besar, makin mirip |
| **Dissimilarity** | Ukuran seberapa **berbeda** dua data. Makin besar, makin berbeda |
| **Distance** (jarak) | Bentuk dissimilarity yang memenuhi aturan tertentu (lihat di bawah). Jarak 0 berarti identik |
| **Pairwise distance** | Jarak antara **sepasang** data. Dihitung untuk semua pasangan |
| **Distance matrix** | Tabel \( n \times n \) berisi jarak setiap data ke setiap data lain |
| **Similarity matrix** | Tabel \( n \times n \) berisi kemiripan setiap pasangan data |

### Similarity vs distance

Keduanya dua sisi dari hal yang sama:

- **Jarak kecil = mirip.** Dua data yang jaraknya 0 identik.
- **Similarity besar = mirip.** Dua data identik punya similarity maksimum (biasanya 1).

Karena itu, similarity dan distance sering diubah satu sama lain. Salah satu cara sederhana:

$$
s = \frac{1}{1 + d}
$$

dengan \( d \) jarak dan \( s \) kemiripan. Jika \( d = 0 \) maka \( s = 1 \) (identik), dan makin besar \( d \) makin kecil \( s \), mendekati 0. Cara lain untuk similarity yang bernilai antara 0 dan 1 adalah \( d = 1 - s \).

## Detailed Explanation

### Mengapa pengukuran kemiripan begitu penting?

Algoritma clustering hampir selalu bekerja dengan pola: "gabungkan data yang jaraknya kecil, pisahkan yang jaraknya besar". Artinya hasilnya **sepenuhnya bergantung pada jarak yang kamu hitung**. Jika jaraknya menyesatkan (misalnya satu fitur terlalu mendominasi), kelompoknya ikut menyesatkan, seberapa pun canggih algoritmanya.

```mermaid
flowchart LR
    A[Data] --> B[Pilih ukuran<br/>kemiripan atau jarak]
    B --> C[Matriks jarak]
    C --> D[Algoritma clustering]
    D --> E[Kelompok]
    B -. mengubah ukuran<br/>mengubah hasil .-> E
```

### Aturan sebuah jarak

Agar disebut **jarak (metrik)** secara matematis, ukuran harus memenuhi empat sifat:

| Sifat | Arti | Contoh |
|---|---|---|
| **Tidak negatif** | \( d(a,b) \ge 0 \) | Jarak tidak bisa minus |
| **Identitas** | \( d(a,b) = 0 \) hanya jika \( a = b \) | Jarak nol berarti titik yang sama |
| **Simetri** | \( d(a,b) = d(b,a) \) | Jarak dari A ke B sama dengan dari B ke A |
| **Ketaksamaan segitiga** | \( d(a,c) \le d(a,b) + d(b,c) \) | Jalan langsung tidak lebih panjang dari jalan memutar |

Dua sifat pertama dan simetri langsung terlihat pada matriks jarak: tidak ada angka negatif, diagonalnya nol, dan matriksnya cermin terhadap diagonal.

### Pairwise distance dan distance matrix

Jika ada \( n \) data, jarak dihitung untuk **setiap pasangan**. Hasilnya disusun menjadi matriks \( n \times n \): sel baris \( i \) kolom \( j \) berisi jarak data ke-\( i \) dan data ke-\( j \). Karena simetris dan diagonalnya nol, hanya separuh matriks yang berisi informasi baru.

Untuk \( n = 5 \) data ada \( \frac{5 \times 4}{2} = 10 \) pasangan unik. Untuk \( n = 200 \) pelanggan ada \( \frac{200 \times 199}{2} = 19.900 \) pasangan. Jumlah pasangan tumbuh kira-kira **kuadrat** terhadap jumlah data, itulah mengapa matriks jarak berat untuk data yang sangat besar.

### Data numerik dan data kategori

| Jenis data | Contoh | Cara mengukur kemiripan |
|---|---|---|
| **Numerik** | Usia, pendapatan, skor | Selisih angka, lalu digabung menjadi jarak (Euclidean, Manhattan; Bab 5) |
| **Kategori biner** | Membeli produk X atau tidak (1 atau 0) | *Simple matching*, *Jaccard* |
| **Kategori umum** | Kota, jenis produk | Cocok atau tidak cocok. Ukuran khusus seperti Gower distance untuk data campuran |

Untuk data **biner**, dua ukuran yang sering dipakai:

- **Simple matching similarity** = banyak posisi yang sama dibagi banyak posisi:

$$
\text{SMC} = \frac{\text{jumlah posisi yang nilainya sama}}{\text{jumlah seluruh posisi}}
$$

- **Jaccard similarity** = hanya melihat posisi di mana **setidaknya satu** bernilai 1:

$$
J(a,b) = \frac{|a \cap b|}{|a \cup b|} = \frac{\text{posisi bernilai 1 pada keduanya}}{\text{posisi bernilai 1 pada salah satunya}}
$$

Jaccard cocok ketika "sama-sama tidak membeli" bukan bukti kemiripan. Dua orang yang sama-sama tidak membeli ribuan produk lain tidak otomatis mirip.

!!! warning "Jangan menganggap kode angka sebagai jarak"
    Jika `Gender` ditulis Female = 0 dan Male = 1, memasukkannya ke rumus jarak numerik menganggap "Male" lebih besar dari "Female" dan jaraknya 1. Itu bisa berguna sebagai kasus biner, tetapi untuk kategori dengan banyak nilai (misalnya kota = 1, 2, 3) **angka itu tidak punya urutan atau jarak**. Gunakan *encoding* yang tepat (Level 2 Bab 9).

## Mathematical Foundation

Untuk dua data numerik \( \mathbf{x} = (x_1, \dots, x_d) \) dan \( \mathbf{y} = (y_1, \dots, y_d) \), bentuk jarak yang paling umum adalah **jarak Euclidean**:

$$
d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{j=1}^{d} (x_j - y_j)^2}
$$

Penjelasan simbol:

- \( d \) di ruas kiri adalah **jarak**, sedangkan \( d \) pada batas penjumlahan adalah **jumlah fitur** (dimensi). Dua hal berbeda yang kebetulan memakai huruf sama.
- \( x_j \) dan \( y_j \) adalah nilai fitur ke-\( j \) dari kedua data.
- \( (x_j - y_j)^2 \) adalah kuadrat selisih fitur ke-\( j \). Kuadrat membuat selisih selalu positif dan menekankan selisih yang besar.
- \( \sum \) menjumlahkan semua fitur, dan akar kuadrat mengembalikan satuan ke satuan semula.

Rumus ini diuraikan penuh di Bab 5. Di sini kita memakainya untuk menghitung matriks jarak.

### Contoh hitung manual

Pelanggan 2 berusia 21, berpendapatan 15, dan bernilai belanja 81. Pelanggan 4 berusia 23, berpendapatan 16, dan bernilai belanja 77.

1. Selisih tiap fitur: usia \( 21 - 23 = -2 \), pendapatan \( 15 - 16 = -1 \), skor \( 81 - 77 = 4 \).
2. Kuadratkan: \( 4 \), \( 1 \), \( 16 \).
3. Jumlahkan: \( 4 + 1 + 16 = 21 \).
4. Akar: \( \sqrt{21} \approx 4{,}58 \).

Jarak 4,58 termasuk kecil. Kemiripannya \( s = \frac{1}{1 + 4{,}58} \approx 0{,}179 \).

**Interpretasi.** Pelanggan 2 dan 4 hanya berbeda sedikit di semua fitur, jadi jaraknya kecil dan kemiripannya relatif tinggi. Nilai 0,179 tampak kecil karena rumus \( 1/(1+d) \) menyusut cepat. Yang penting adalah **urutannya**: pasangan dengan jarak lebih kecil punya similarity lebih besar.

## Python Implementation

Kita kerjakan dalam tujuh langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-3/04_similarity_and_dissimilarity.py`, dan versi notebook-nya di `notebooks/level-3/04-similarity-and-dissimilarity.ipynb`.

**Konteks masalah:** dari 200 pelanggan Mall Customers, kita ambil lima pelanggan pertama, menghitung seberapa mirip mereka satu sama lain, lalu melihat bagaimana skala fitur mengubah gambaran.

**Input yang diharapkan:** `data/mall_customers.csv`, dijalankan dari folder utama proyek.

### Langkah 1 — Ambil lima pelanggan

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:setup"
```

**Penjelasan:**

- `pairwise_distances` dari scikit-learn menghitung jarak semua pasangan data. `StandardScaler` dipakai di Langkah 6.
- `cols` adalah tiga fitur numerik yang kita pakai: `Age`, `Annual Income (k$)`, dan `Spending Score (1-100)`.
- `df.loc[:4, [...]]` mengambil baris dari indeks 0 sampai **4 (termasuk 4)**, yaitu lima pelanggan pertama, dengan kolom yang kita pilih. Berbeda dengan potongan Python biasa, `.loc` **menyertakan** batas akhir.
- `.set_index("CustomerID")` menjadikan `CustomerID` sebagai label baris agar tabel jarak mudah dibaca.

### Langkah 2 — Hitung matriks jarak

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:matrix"
```

**Penjelasan:**

- `five.to_numpy()` mengubah tabel menjadi larik NumPy.
- `pairwise_distances(..., metric="euclidean")` mengembalikan matriks 5 × 5: jarak Euclidean setiap pelanggan ke setiap pelanggan lain.
- `pd.DataFrame(D, index=..., columns=...)` memberi label `CustomerID` pada baris dan kolom, dan `.round(2)` membulatkan dua angka di belakang koma.

### Langkah 3 — Ubah jarak menjadi kemiripan

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:similarity"
```

**Penjelasan:**

- `S = 1 / (1 + D)` menerapkan rumus \( s = 1/(1+d) \) pada **seluruh matriks sekaligus**. NumPy mengerjakannya untuk setiap sel.
- Hasilnya matriks kemiripan: diagonalnya 1 (tiap pelanggan identik dengan dirinya sendiri) dan angka lain di antara 0 dan 1.

### Langkah 4 — Periksa sifat matriks jarak

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:check"
```

**Penjelasan:**

- `np.allclose(D, D.T)` memeriksa **simetri**: `D.T` adalah transpos (baris dan kolom ditukar). Jika sama, maka \( d(a,b) = d(b,a) \).
- `np.diag(D)` mengambil diagonal, dan kita periksa semuanya nol.
- `(D >= 0).all()` memeriksa tidak ada jarak negatif. `bool(...)` mengubah hasilnya menjadi `True` atau `False` biasa.
- `D + np.diag([np.inf] * len(D))` menambahkan tak hingga pada diagonal supaya jarak nol ke diri sendiri **tidak terpilih** sebagai yang terkecil.
- `masked.argmin()` memberi posisi terkecil dalam bentuk satu angka, dan `np.unravel_index(..., masked.shape)` mengubahnya kembali menjadi (baris, kolom). Itulah pasangan paling mirip.

### Langkah 5 — Data kategori biner

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:categorical"
```

**Penjelasan:**

- `a` dan `b` adalah dua pelanggan dan lima produk: 1 berarti membeli, 0 berarti tidak.
- `(a == b).sum()` menghitung posisi yang sama (di sini 3). Bagi dengan 5 menghasilkan *simple matching similarity*.
- `(a == 1) & (b == 1)` bernilai benar hanya jika **keduanya** membeli. `(a == 1) | (b == 1)` bernilai benar jika **salah satunya** membeli. `.sum()` menghitung masing-masing.
- Rasio keduanya adalah *Jaccard similarity*, dan `1 - ...` menghasilkan *Jaccard distance*.

### Langkah 6 — Kesalahan umum: skala fitur

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:scale"
```

**Penjelasan:**

- `raw[0] - raw[1]` adalah selisih tiap fitur antara pelanggan 1 dan 2. Kita cetak selisih dan **kuadrat selisih** (kontribusi tiap fitur pada jarak).
- `StandardScaler().fit(df[cols])` mempelajari rata-rata dan simpangan baku tiap fitur dari **seluruh 200 pelanggan**. `.transform(five)` lalu mengubah lima pelanggan menjadi skala yang sebanding (rata-rata 0, simpangan baku 1). Standardisasi dibahas di Level 2 Bab 10.
- Kita hitung ulang matriks jarak pada data terstandardisasi untuk membandingkannya.

### Langkah 7 — Visualisasi matriks jarak

```python
--8<-- "level-3/04_similarity_and_dissimilarity.py:plot"
```

**Penjelasan:**

- `ax.imshow(M, cmap="viridis_r")` menggambar matriks sebagai **peta warna**. Dengan `viridis_r`, jarak kecil berwarna terang (kuning) dan jarak besar berwarna gelap.
- `ax.set_xticks(range(5), labels=...)` menuliskan `CustomerID` di sumbu.
- Dua `for` bertingkat menulis angka jarak di tiap sel dengan `ax.text(...)`. Warna teksnya diganti (hitam pada latar terang, putih pada latar gelap) agar tetap terbaca.

## Code Explanation

| Yang kamu lihat | Artinya |
|---|---|
| `pairwise_distances(X)` | Matriks jarak semua pasangan baris `X` |
| `D.T` | Transpos matriks (baris dan kolom ditukar) |
| `1 / (1 + D)` | Mengubah jarak menjadi kemiripan di seluruh matriks |
| `np.diag(D)` | Mengambil diagonal matriks |
| `(a == b).sum()` | Menghitung posisi yang sama |
| `StandardScaler().fit(...).transform(...)` | Menyamakan skala fitur |

Pola umumnya: **data → matriks jarak → periksa sifat → baca pasangan paling mirip.**

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
pip install -r requirements-notebooks.txt
python examples/level-3/04_similarity_and_dissimilarity.py
```

Skrip membuat satu gambar di `docs/assets/level-3/`. Untuk notebook:

```powershell
jupyter notebook notebooks/level-3/04-similarity-and-dissimilarity.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, matplotlib 3.11.1):

```text
--8<-- "level-3/outputs/04.txt"
```

![Dua peta warna matriks jarak lima pelanggan: kiri data mentah, kanan setelah standardisasi](../assets/level-3/04-matriks-jarak.png)

### Interpretasi output

**Matriks jarak.** Jarak pelanggan 2 dan 4 hanya 4,58, yang terkecil di tabel, jadi keduanya pasangan paling mirip. Jarak pelanggan 2 dan 3 adalah 75,01, yang terbesar. Pelanggan 3 punya skor belanja 6 sedangkan pelanggan 2 punya 81, selisih 75 pada skor belanja.

**Sifat matriks.** Ketiga pemeriksaan menghasilkan `True`: matriks simetris, diagonal nol, dan tidak ada jarak negatif.

**Matriks kemiripan.** Pasangan (2, 4) punya similarity tertinggi di luar diagonal (0,179). Urutannya sejalan dengan jarak, hanya terbalik arah.

**Data biner.** Kedua pelanggan sama pada 3 dari 5 produk, sehingga simple matching = 0,6. Jaccard hanya memperhatikan produk yang dibeli salah satunya: 2 dibeli keduanya dari 4 yang dibeli salah satunya, jadi Jaccard = 0,5 dan jarak Jaccard = 0,5. Nilainya berbeda karena Jaccard tidak menghitung posisi "sama-sama 0".

**Skala fitur.** Antara pelanggan 1 dan 2, selisih usia −2, selisih pendapatan 0, dan selisih skor belanja −42. Kuadratnya 4, 0, dan 1764. Dari jumlah 1768 itu, sekitar **99,8%** datang dari skor belanja. Jarak 42,05 antara pelanggan 1 dan 2 sebenarnya hampir seluruhnya hanya soal skor belanja. Setelah standardisasi, tiap fitur punya bobot sebanding, dan angka jaraknya berubah ke skala sekitar 0 sampai 3 (misalnya 1,64 untuk pelanggan 1 dan 2). Perhatikan juga bahwa **urutan pasangan bisa berubah**: sebelum standardisasi, jarak pelanggan 1 ke 4 (38,22) lebih kecil daripada jarak ke 2 (42,05), dan sesudahnya 1,50 melawan 1,64. Pada lima pelanggan ini urutannya kebetulan sama, tetapi pada Bab 5 kita akan melihat bahwa pada seluruh 200 pelanggan tetangga terdekat banyak yang berubah.

## Practical Examples

**Rekomendasi produk.** Pelanggan dengan pola pembelian mirip (Jaccard tinggi) bisa direkomendasikan produk yang sama. Di sini Jaccard lebih masuk akal daripada simple matching, karena ribuan produk yang sama-sama tidak dibeli bukan bukti kemiripan.

**Segmentasi pelanggan.** Jika kamu memasukkan pendapatan dalam rupiah (jutaan) dan skor belanja (1 sampai 100) tanpa penyamaan skala, hasil clustering hanya akan membagi pelanggan menurut pendapatan. Itu kesalahan umum yang bisa kamu hindari dengan memeriksa kontribusi tiap fitur seperti di Langkah 6.

**Deteksi kemiripan dokumen.** Dokumen dapat dibuat menjadi vektor jumlah kata. Pada kasus itu *cosine similarity* (Bab 5) lebih cocok daripada Euclidean, karena panjang dokumen tidak boleh mendominasi.

### Kesalahan umum

| Kesalahan | Akibat | Cara menghindari |
|---|---|---|
| Memakai fitur dengan skala berbeda tanpa menyamakan | Fitur ber-skala besar mendominasi jarak | Standardisasi atau normalisasi sebelum menghitung jarak |
| Memperlakukan kode kategori sebagai angka | Jarak mengada-ada (kota 1 "lebih dekat" ke 2 daripada 3) | Pakai *one-hot encoding* atau ukuran khusus kategori |
| Mengira similarity dan distance bisa dicampur | Algoritma memilih pasangan yang paling **berbeda** | Pastikan arahnya: jarak kecil = mirip, similarity besar = mirip |
| Memasukkan kolom ID sebagai fitur | Jarak dipengaruhi nomor urut | Buang kolom ID (Level 2 Bab 11) |
| Memakai Euclidean untuk data biner jarang | Kesamaan "sama-sama 0" mengaburkan | Pakai Jaccard |

## Hands-on Exercises

1. Hitung manual jarak Euclidean antara pelanggan 1 (19, 15, 39) dan pelanggan 5 (31, 17, 40). Samakah dengan angka di matriks?
2. Ubah `five` menjadi sepuluh pelanggan pertama (`df.loc[:9, ...]`). Siapa pasangan paling mirip?
3. Berapa banyak pasangan unik pada 200 data?
4. Hitung Jaccard similarity untuk \( a = [1,0,1,0,0,1] \) dan \( b = [1,1,1,0,0,0] \). Bandingkan dengan simple matching.
5. Mengapa `Spending Score` mendominasi jarak pelanggan 1 dan 2 pada data mentah?

??? question "Jawaban"
    1. Selisih: \( 19-31 = -12 \), \( 15-17 = -2 \), \( 39-40 = -1 \). Kuadrat: 144, 4, 1. Jumlah: 149. Akar: \( \sqrt{149} \approx 12{,}21 \). Sama dengan sel (1, 5) pada matriks, yaitu 12,21.
    2. Jalankan kodenya. Pasangan (2, 4) tetap kandidat kuat karena jaraknya hanya 4,58, tetapi ada pelanggan baru yang bisa lebih dekat. Periksa matriksnya.
    3. \( \frac{200 \times 199}{2} = 19.900 \) pasangan.
    4. Posisi yang sama: posisi 1 (1,1), 3 (1,1), 4 (0,0), 5 (0,0) = 4 dari 6, jadi simple matching \( 4/6 \approx 0{,}667 \). Jaccard: keduanya 1 di posisi 1 dan 3 (2 posisi). Salah satunya 1 di posisi 1, 2, 3, 6 (4 posisi). Jaccard = \( 2/4 = 0{,}5 \). Simple matching lebih tinggi karena menghitung posisi "sama-sama 0".
    5. Skor belanja berkisar 1 sampai 99 dan selisihnya antara kedua pelanggan 42, sedangkan usia hanya selisih 2 dan pendapatan 0. Karena jarak mengkuadratkan selisih, perbedaan besar menjadi jauh lebih berpengaruh (1764 melawan 4).

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ValueError: could not convert string to float` | Ada kolom teks (misalnya `Gender`) di data yang dihitung jaraknya | Pilih hanya kolom numerik atau lakukan encoding dulu |
| Diagonal bukan nol | Memakai ukuran similarity, bukan jarak | Periksa apakah ukurannya jarak (diagonal 0) atau similarity (diagonal 1) |
| Pasangan paling mirip adalah titik dengan dirinya sendiri | Diagonal nol ikut terpilih saat mencari minimum | Isi diagonal dengan `np.inf` seperti di Langkah 4 |
| `MemoryError` untuk data besar | Matriks \( n \times n \) terlalu besar | Hitung per bagian atau pakai sampel |
| Jarak tidak berubah setelah standardisasi | Menggunakan variabel data lama | Pastikan memakai hasil `transform`, bukan data awal |

## Summary

- **Similarity** mengukur kemiripan dan **dissimilarity** (jarak) mengukur perbedaan. Keduanya saling berbalik: jarak kecil berarti mirip, similarity besar berarti mirip.
- Hasil clustering bergantung pada cara kita mengukur kemiripan, jadi pemilihan ukuran harus disadari.
- **Distance matrix** berisi jarak semua pasangan. Ia tidak negatif, simetris, dan berdiagonal nol.
- Data numerik memakai jarak Euclidean atau sejenisnya. Data biner memakai *simple matching* atau *Jaccard*.
- Pada data mentah Mall Customers, 99,8% jarak antara pelanggan 1 dan 2 berasal dari satu fitur (skor belanja). Karena itu **skala fitur** harus disamakan dulu.

**Bab berikutnya:** Bab 5 membahas rumus jarak secara rinci: Euclidean, Manhattan, Minkowski, dan cosine.

## References

- Tan, P.-N., Steinbach, M., Karpatne, A., & Kumar, V. *Introduction to Data Mining* (Pearson), bab tentang ukuran kemiripan dan ketidakmiripan.
- Scikit-learn documentation: [`pairwise_distances`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html) dan [*Pairwise metrics*](https://scikit-learn.org/stable/modules/metrics.html).
- Scikit-learn documentation: [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).
- Gower, J. C. (1971). A general coefficient of similarity and some of its properties. *Biometrics*, 27(4), 857–871.
