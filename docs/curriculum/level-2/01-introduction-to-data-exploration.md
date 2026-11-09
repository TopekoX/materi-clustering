# Bab 1 — Introduction to Data Exploration

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan apa itu *data exploration* dan perbedaannya dengan *preprocessing*.
- [x] Menjelaskan mengapa clustering sangat bergantung pada kualitas data.
- [x] Membedakan *observation* (baris) dan *feature* (kolom) pada sebuah dataset.
- [x] Memuat file CSV dengan *pandas* dan memeriksanya dengan `head()`, `shape`, `dtypes`, dan `describe()`.
- [x] Melakukan pemeriksaan kualitas dasar: nilai kosong dan baris duplikat.
- [x] Membuat histogram dan *scatter plot* pertama untuk melihat bentuk data.

## Introduction

Pada **supervised learning**, kita punya label sebagai kunci jawaban. Model yang salah bisa langsung ketahuan karena prediksinya dibandingkan dengan label. Pada **clustering**, label itu tidak ada. Algoritma hanya mengelompokkan data berdasarkan kemiripan, dan hasil akhirnya hanya sebaik data yang masuk.

Karena itu, kebiasaan terpenting dalam clustering adalah **mengenal data sebelum memprosesnya**. Beberapa hal yang perlu dicek sebelum menjalankan algoritma apa pun:

- Berapa baris dan kolomnya?
- Apakah ada nilai yang kosong atau baris yang dobel?
- Apakah rentang nilai antar kolom sangat berbeda?
- Apakah datanya sudah tampak membentuk kelompok?

Bab ini membuka **Level 2** dengan latihan pertama: memuat dataset *Mall Customers* dan memeriksanya langkah demi langkah.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Dataset** | Kumpulan data dalam bentuk tabel |
| **Observation** (*record*, sampel) | Satu baris. Di sini: satu pelanggan |
| **Feature** (variabel, atribut) | Satu kolom. Di sini: usia, pendapatan, skor belanja |
| **Data exploration** | Memeriksa data untuk memahami isi, bentuk, dan masalahnya. **Belum mengubah** data |
| **Preprocessing** | Mengubah data agar siap dipakai algoritma: membersihkan, mengubah skala, mengubah kode |

Urutannya penting: **eksplorasi dulu, preprocessing sesudahnya.** Kita tidak bisa memperbaiki masalah yang belum kita lihat.

!!! note "Tentang dataset"
    **Mall Customers** berisi 200 pelanggan dengan lima kolom: `CustomerID`, `Gender`, `Age`, `Annual Income (k$)`, dan `Spending Score (1-100)`. Skor belanja diberikan oleh pihak mall (1–100, makin tinggi berarti makin sering dan banyak berbelanja). File ada di `data/mall_customers.csv`.

    Dataset ini populer sebagai contoh clustering, dan aslinya dipublikasikan di Kaggle. Salinan di repo ini diunduh dari mirror GitHub. Kalau kamu memakainya di luar belajar, periksa lisensi dataset di sumber aslinya.

## Detailed Explanation

### Alur eksplorasi dasar

```mermaid
flowchart LR
    A[Muat data] --> B[Lihat sekilas<br/>head, shape]
    B --> C[Periksa tipe data<br/>dtypes]
    C --> D[Ringkasan statistik<br/>describe]
    D --> E[Cek kualitas<br/>kosong, duplikat]
    E --> F[Visualisasi awal]
```

1. **Muat data.** Baca file CSV menjadi tabel *pandas* yang disebut `DataFrame`.
2. **Lihat sekilas.** `head()` menampilkan beberapa baris pertama, `shape` memberi jumlah baris dan kolom.
3. **Periksa tipe data.** Angka (`int64`) dan teks (`str`/`object`) diperlakukan berbeda oleh algoritma. Pembahasan lengkapnya ada di Bab 2.
4. **Ringkasan statistik.** `describe()` menunjukkan rata-rata, simpangan baku, minimum, dan maksimum. Mulai dari sini kita bisa melihat apakah rentang antar kolom berbeda jauh (dibahas lebih dalam di Bab 3).
5. **Cek kualitas.** Hitung nilai kosong dan baris duplikat (Bab 5 dan 6).
6. **Visualisasi awal.** Histogram untuk bentuk sebaran tiap kolom, *scatter plot* untuk hubungan dua kolom (Bab 4).

### Peta Level 2

Bab ini hanya memperkenalkan semua langkah itu sekilas. Setiap langkah dibahas mendalam di bab sesudahnya, dan Level 2 berakhir dengan dataset yang siap di-*cluster* (Bab 12).

## Mathematical Foundation

Bab pengantar ini belum memerlukan rumus. Statistik ringkasan seperti rata-rata dan simpangan baku dibahas dengan rumusnya di Bab 3.

## Python Implementation

Kita kerjakan dalam enam langkah kecil. **Setiap potongan kode diikuti penjelasannya**, jadi baca kode, lalu baca penjelasannya sebelum lanjut. Skrip lengkapnya ada di `examples/level-2/01_explore_mall_customers.py`, dan versi notebook-nya di `notebooks/level-2/01-introduction-to-data-exploration.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/01_explore_mall_customers.py:setup"
```

**Penjelasan:**

- `import pandas as pd` memanggil *pandas*, pustaka Python untuk mengolah tabel. Kita beri nama singkat `pd` supaya mengetiknya tidak panjang.
- `import matplotlib.pyplot as plt` memanggil *matplotlib*, pustaka untuk membuat grafik. Nama singkatnya `plt`.
- `DATA_PATH = "data/mall_customers.csv"` menyimpan lokasi file data dalam sebuah variabel. Artinya: file `mall_customers.csv` ada di folder `data`.
- `pd.read_csv(DATA_PATH)` membaca file CSV dan mengubahnya menjadi tabel pandas yang disebut **DataFrame**. Kita simpan di variabel `df`. Mulai sekarang, `df` adalah tabel data pelanggan kita.

### Langkah 2 — Lihat sekilas isi data

```python
--8<-- "level-2/01_explore_mall_customers.py:glance"
```

**Penjelasan:**

- `df.head()` menampilkan **5 baris pertama**. Ini seperti mengintip isi tabel tanpa membuka semuanya.
- `df.shape` memberi pasangan angka `(jumlah baris, jumlah kolom)`. Hasilnya nanti `(200, 5)`: 200 pelanggan dan 5 kolom.
- `df.dtypes` menunjukkan **tipe data** tiap kolom, misalnya `int64` (bilangan bulat) atau `str` (teks). Tipe data penting karena angka dan teks diperlakukan berbeda.
- `print("\n...")`: tanda `\n` hanya membuat baris kosong supaya output mudah dibaca.

### Langkah 3 — Ringkasan statistik

```python
--8<-- "level-2/01_explore_mall_customers.py:summary"
```

**Penjelasan:**

- `df.describe()` menghitung ringkasan untuk semua kolom angka sekaligus: jumlah data (`count`), rata-rata (`mean`), simpangan baku (`std`), nilai terkecil (`min`), nilai terbesar (`max`), dan kuartil (`25%`, `50%`, `75%`).
- `.round(2)` membulatkan angka menjadi dua angka di belakang koma, supaya tabelnya rapi.
- Dengan satu baris ini kita sudah bisa melihat rentang tiap kolom. Misalnya, usia berkisar 18 sampai 70 tahun.

### Langkah 4 — Pemeriksaan kualitas dasar

```python
--8<-- "level-2/01_explore_mall_customers.py:quality"
```

**Penjelasan:**

- `df.isna()` menandai sel yang **kosong** (`True`), lalu `.sum()` menjumlahkannya per kolom. Hasil `0` berarti tidak ada sel kosong.
- `df.duplicated()` menandai baris yang **sama persis** dengan baris sebelumnya, lalu `.sum()` menghitungnya. Hasil `0` berarti tidak ada baris ganda.
- `df["Gender"]` mengambil satu kolom. `.value_counts()` menghitung berapa kali tiap isi kolom muncul, di sini jumlah pelanggan `Female` dan `Male`.

### Langkah 5 — Histogram: bentuk sebaran tiap kolom

```python
--8<-- "level-2/01_explore_mall_customers.py:hist"
```

**Penjelasan:**

- `features = [...]` adalah daftar tiga kolom yang ingin kita gambar.
- `plt.subplots(1, 3, ...)` membuat satu bidang gambar berisi **1 baris dan 3 grafik** berdampingan. `fig` adalah gambar keseluruhan, `axes` adalah ketiga grafiknya.
- `for ax, col in zip(axes, features)` mengulang pekerjaan yang sama untuk tiap pasangan (grafik, kolom).
- `ax.hist(df[col], bins=15)` menggambar **histogram**: nilai dibagi ke 15 rentang, lalu tinggi batang menunjukkan berapa pelanggan di tiap rentang.
- `plt.show()` menampilkan gambar. (Di skrip ini, gambarnya disimpan ke file.)

### Langkah 6 — Scatter plot: hubungan dua kolom

```python
--8<-- "level-2/01_explore_mall_customers.py:scatter"
```

**Penjelasan:**

- `ax.scatter(x, y)` menggambar **satu titik untuk setiap pelanggan**. Posisi titik ditentukan oleh pendapatan (sumbu x) dan skor belanja (sumbu y).
- `s=18` mengatur ukuran titik.
- `set_xlabel`, `set_ylabel`, dan `set_title` memberi nama pada sumbu dan judul grafik. Grafik tanpa label sulit dibaca.

## Code Explanation

Ringkasan cara membaca kode di atas:

| Yang kamu lihat | Artinya |
|---|---|
| `df` | Tabel data (DataFrame). Hampir semua perintah dimulai dari sini |
| `df.sesuatu()` | **Metode**: perintah yang dijalankan pada tabel, misalnya `df.head()` |
| `df.sesuatu` (tanpa kurung) | **Atribut**: informasi yang sudah tersedia, misalnya `df.shape` |
| `df["Nama Kolom"]` | Mengambil satu kolom |
| `print(...)` | Menampilkan hasil di layar |

Pola umumnya: **muat data → lihat sekilas → ringkas → periksa kualitas → gambar**. Pola ini kita ulangi di bab-bab berikutnya.

## How to Run

Jalankan dari **folder utama proyek** (folder yang berisi `mkdocs.yml`):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-notebooks.txt
python examples/level-2/01_explore_mall_customers.py
```

Skrip membuat dua gambar di `docs/assets/level-2/`. Untuk menjalankan notebook:

```powershell
jupyter notebook notebooks/level-2/01-introduction-to-data-exploration.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, matplotlib 3.11.2, Python 3.14.7):

```text
--8<-- "level-2/outputs/01.txt"
```

Gambar yang dihasilkan:

![Histogram usia, pendapatan, dan skor belanja](../../assets/level-2/01-distribusi-fitur.png)

![Scatter plot pendapatan vs skor belanja](../../assets/level-2/01-scatter-income-spending.png)

## Practical Examples

Beberapa temuan dari output di atas, dan artinya untuk clustering:

**1. Tidak ada nilai kosong dan tidak ada duplikat.** Dataset ini sudah bersih untuk dua pemeriksaan itu. Data nyata biasanya tidak seramah ini. Teknik menanganinya dibahas di Bab 5, 6, dan 8.

**2. Rentang tiap kolom berbeda.** Usia berkisar 18–70, pendapatan 15–137, skor belanja 1–99. Banyak algoritma clustering (misalnya K-Means) menghitung **jarak**, sehingga kolom dengan rentang besar bisa lebih mendominasi. Cara mengatasinya, *feature scaling*, dibahas di Bab 10.

**3. `CustomerID` bukan fitur yang bermakna.** Kolom ini hanya nomor urut (rata-ratanya 100,50 karena isinya 1 sampai 200). Memasukkannya ke clustering akan menyesatkan. Memilih kolom yang tepat dibahas di Bab 11.

**4. `Gender` berupa teks.** Algoritma jarak butuh angka, jadi kolom ini perlu diubah dulu (*encoding*, Bab 9).

**5. *Scatter plot* menunjukkan pola.** Pada grafik pendapatan vs skor belanja, titik-titik tampak terkumpul dalam beberapa gerombol, dengan satu gerombol padat di tengah. Ini baru **kesan visual** dari dua kolom saja, bukan hasil clustering. Kita belum menjalankan algoritma apa pun, dan jumlah kelompok sebenarnya perlu diuji secara sistematis di level berikutnya.

## Hands-on Exercises

1. Berapa banyak pelanggan berusia di atas 50 tahun? *(petunjuk: `(df["Age"] > 50).sum()`)*
2. Berapa rata-rata `Spending Score (1-100)` untuk `Female` dan untuk `Male`? *(petunjuk: `df.groupby("Gender")[...].mean()`)*
3. Tampilkan 5 pelanggan dengan pendapatan tertinggi. *(petunjuk: `sort_values`)*
4. Buat *scatter plot* `Age` vs `Spending Score (1-100)`. Apakah kamu melihat pola?
5. Sebutkan dua alasan mengapa `CustomerID` sebaiknya tidak dipakai sebagai fitur clustering.

??? question "Jawaban"
    Hasil berikut dari eksekusi nyata pada data ini:

    1. **40** pelanggan berusia di atas 50 tahun.
    2. Rata-rata skor belanja: `Female` **51,53** dan `Male` **48,51**. Selisihnya kecil.
    3. Pendapatan tertinggi adalah 137 (CustomerID 200 dan 199), disusul 126 (CustomerID 198 dan 197), lalu 120 (CustomerID 196).
    4. Koefisien korelasi `Age` dan `Spending Score (1-100)` adalah **−0,33**: ada kecenderungan lemah bahwa pelanggan yang lebih muda punya skor belanja lebih tinggi, tetapi titik-titiknya tetap tersebar. Buat grafiknya sendiri dan bandingkan dengan kesanmu.

    5. (a) `CustomerID` hanya nomor urut, tidak menggambarkan sifat pelanggan. (b) Nilainya bertambah teratur dari 1 sampai 200, sehingga bisa memengaruhi perhitungan jarak tanpa makna apa pun.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `FileNotFoundError: ... mall_customers.csv` | File belum ada atau lokasi salah | Pastikan `data/mall_customers.csv` ada di folder utama repo |
| `ModuleNotFoundError: No module named 'pandas'` | Pustaka belum terpasang di lingkungan aktif | Aktifkan `.venv`, lalu `pip install -r requirements-notebooks.txt` |
| Kolom teks tampil sebagai `object`, bukan `str` | Perbedaan versi pandas. Pandas 3 menampilkan `str`, versi lebih lama `object` | Bukan kesalahan. Keduanya berarti kolom teks |
| Angka di tabel sedikit berbeda | Versi pandas lain atau pembulatan | Bandingkan nilai `describe()`, bukan tampilan persisnya |
| Jendela grafik tidak muncul | Skrip memakai backend `Agg` yang hanya menyimpan file | Buka file PNG di `docs/assets/level-2/` atau jalankan notebook |

## Summary

- Clustering tidak punya label, jadi **kualitas data** menentukan kualitas hasil.
- **Eksplorasi** (memeriksa data) mendahului **preprocessing** (mengubah data).
- Pemeriksaan dasar dengan pandas: `head()`, `shape`, `dtypes`, `describe()`, `isna().sum()`, `duplicated().sum()`.
- Pada Mall Customers: 200 baris, 5 kolom, tidak ada nilai kosong atau duplikat. Rentang kolom berbeda, `CustomerID` bukan fitur bermakna, dan `Gender` berupa teks.
- Visualisasi awal memberi **kesan** tentang bentuk data, belum membuktikan apa pun.

## References

- pandas documentation: [*Getting started tutorials*](https://pandas.pydata.org/docs/getting_started/index.html) dan [`DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html).
- Matplotlib documentation: [`hist`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html) dan [`scatter`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html).
- Dataset *Customer Segmentation Tutorial in Python* (Mall Customers), Kaggle.
