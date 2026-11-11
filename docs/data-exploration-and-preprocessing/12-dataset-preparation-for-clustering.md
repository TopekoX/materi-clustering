# Bab 12 — Dataset Preparation for Clustering

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Merangkai semua langkah Level 2 menjadi satu alur persiapan data yang berurutan.
- [x] Menulis alur itu sebagai satu fungsi yang bisa dipakai ulang.
- [x] Memeriksa bahwa dataset akhir memenuhi syarat untuk clustering.
- [x] Mengembalikan data terskala ke satuan asli dan ke pelanggan asalnya.
- [x] Melakukan uji coba singkat bahwa algoritma bisa menerima dataset itu.
- [x] Mendokumentasikan keputusan persiapan data.

## Introduction

Selama Level 2, kita mengerjakan langkah demi langkah: mengenal data (Bab 1–4), memeriksa kualitas (Bab 5–8), lalu mengubah dan memilih fitur (Bab 9–11). Bab penutup ini **merangkai semuanya** menjadi satu alur dan menghasilkan **dataset akhir** yang siap dipakai di Level 3.

Alur yang rapi punya keuntungan penting: **hasilnya bisa diulang**. Siapa pun yang menjalankan kode kita pada data yang sama akan mendapatkan dataset akhir yang sama.

## Fundamental Concepts

### Syarat dataset siap untuk clustering

| Syarat | Alasan | Bab |
|---|---|---|
| Hanya kolom **angka** | Algoritma jarak butuh angka | 2, 9 |
| Tidak ada **nilai kosong** | Scikit-learn menolak `NaN` | 5 |
| Tidak ada **baris ganda** | Duplikat memberi bobot ekstra | 6 |
| **Outlier** sudah dinilai | Titik jauh memengaruhi pusat kelompok | 7 |
| Tidak ada kolom **identitas** | Nomor urut tidak bermakna | 2, 11 |
| **Skala** sudah sama | Agar tiap fitur berperan adil | 10 |

### Keputusan yang kita ambil di Level 2

| Pertanyaan | Keputusan | Dasar |
|---|---|---|
| Nilai kosong? | Tidak ada, tetapi fungsi memeriksanya | Bab 1 dan 5 |
| Duplikat? | Tidak ada, tetapi dibuang bila ada | Bab 6 |
| Outlier? | **Dipertahankan** (2 baris, nilai masuk akal) | Bab 7 |
| Fitur? | `Age`, `Annual Income (k$)`, `Spending Score (1-100)`. `CustomerID` dibuang. `Gender` tidak dipakai | Bab 4 dan 11 |
| Skala? | *Standardization* | Bab 10 |
| Fitur baru? | Tidak ada | Bab 11 |

!!! note "Ini keputusan didaktis, bukan kebenaran mutlak"
    Pilihan di atas masuk akal untuk dataset ini dan untuk belajar. Dengan tujuan atau data berbeda, kamu bisa memilih lain. Yang penting: **setiap keputusan punya alasan dan tercatat**.

## Detailed Explanation

### Mengapa dibungkus dalam fungsi

Kalau langkah-langkahnya tersebar di banyak sel, mudah ada yang terlewat atau terjalankan dengan urutan salah. Fungsi `siapkan_dataset()`:

- menjalankan langkah **selalu dengan urutan yang sama**,
- bisa dipanggil ulang pada data baru,
- memudahkan orang lain memahami alurnya.

### Menyimpan `scaler`

Fungsi kita mengembalikan **tiga hal**: tabel bersih, dataset terskala, dan objek `scaler`. `scaler` menyimpan rata-rata dan simpangan baku yang dipakai, sehingga kita bisa **mengembalikan** angka terskala ke satuan asli. Ini penting saat menjelaskan hasil clustering kepada orang lain.

### Menjaga hubungan dengan pelanggan

Dataset akhir tidak punya `CustomerID`. Karena `index` barisnya kita jaga **sama** dengan tabel bersih, baris ke-0 di dataset akhir selalu milik pelanggan yang sama dengan baris ke-0 di tabel bersih. Dengan begitu, hasil clustering nanti bisa dikaitkan kembali ke pelanggan.

## Mathematical Foundation

Bab ini tidak memerlukan rumus baru. Penskalaan memakai z-score dari Bab 10:

$$
z = \frac{x - \mu}{\sigma}
$$

Mengembalikan ke satuan asli memakai kebalikannya:

$$
x = z \cdot \sigma + \mu
$$

## Python Implementation

Kita kerjakan dalam lima langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/12_dataset_preparation.py`, dan versi notebook-nya di `notebooks/level-2/12-dataset-preparation-for-clustering.ipynb`.

### Langkah 1 — Siapkan alat

```python
--8<-- "level-2/12_dataset_preparation.py:setup"
```

**Penjelasan:**

- Kita memanggil `pandas` untuk tabel dan `StandardScaler` dari scikit-learn untuk menskalakan.
- `FITUR` adalah daftar kolom yang akan dipakai. Dengan menaruhnya di satu tempat, kalau suatu hari kita mau mengganti fitur, cukup ubah di sini.

### Langkah 2 — Menyusun alur persiapan dalam satu fungsi

```python
--8<-- "level-2/12_dataset_preparation.py:pipeline"
```

**Penjelasan:**

- `def siapkan_dataset(path, fitur=FITUR):` mendefinisikan fungsi yang menerima lokasi file dan (opsional) daftar fitur.
- Teks di antara tanda `"""..."""` adalah **docstring**: penjelasan singkat tentang fungsi.
- **Langkah 1** merapikan teks `Gender` (Bab 8) dan membuang duplikat (Bab 6). `reset_index(drop=True)` menomori ulang baris dari 0 agar rapi.
- **Langkah 2** memeriksa nilai kosong. `isna().any().any()` bernilai `True` jika **ada satu pun** sel kosong (`any` pertama per kolom, `any` kedua dari semua kolom). Jika ada, fungsi **berhenti dengan pesan galat** (`raise ValueError`) daripada diam-diam meneruskan data bermasalah.
- **Langkah 3** hanya komentar: kita sengaja tidak melakukan apa-apa pada outlier, dan alasannya dicatat di situ.
- **Langkah 4** memilih tiga kolom fitur. `CustomerID` dan `Gender` tidak ikut.
- **Langkah 5** menskalakan dengan `StandardScaler`. `pd.DataFrame(..., columns=fitur, index=df.index)` membungkus hasilnya kembali menjadi tabel dengan nama kolom dan nomor baris yang sama.
- `return df, X_terskala, scaler` mengembalikan tiga hasil sekaligus.

### Langkah 3 — Menjalankan alur pada data asli

```python
--8<-- "level-2/12_dataset_preparation.py:run"
```

```text title="Output"
--8<-- "level-2/outputs/12/run.txt"
```

**Penjelasan:**

- `df_bersih, X, scaler = siapkan_dataset(DATA_PATH)` memanggil fungsi, lalu menerima tiga hasilnya ke tiga variabel.
- `X` adalah **dataset akhir** kita.
- Kita cetak ukuran tabel bersih (lima kolom) dan dataset akhir (tiga kolom), lalu lima baris pertamanya.

### Langkah 4 — Memeriksa dataset akhir

```python
--8<-- "level-2/12_dataset_preparation.py:sanity"
```

```text title="Output"
--8<-- "level-2/outputs/12/sanity.txt"
```

**Penjelasan:**

- Ini **uji kelayakan** (*sanity check*): kita memastikan syarat-syarat di tabel tadi benar-benar terpenuhi, bukan hanya berharap.
- `X.isna().sum().sum()` menghitung nilai kosong, dan `X.duplicated().sum()` menghitung baris ganda.
- `all(X.dtypes == "float64")` memeriksa bahwa semua kolom bertipe angka desimal.
- `X.mean()` harus mendekati 0 dan `X.std(ddof=0)` harus mendekati 1, sesuai sifat *standardization*.
- Terakhir kita pastikan jumlah baris sama dengan tabel bersih.

### Langkah 5 — Mengembalikan ke satuan asli dan ke pelanggan

```python
--8<-- "level-2/12_dataset_preparation.py:back"
```

```text title="Output"
--8<-- "level-2/outputs/12/back.txt"
```

**Penjelasan:**

- `scaler.inverse_transform(X)` membalik penskalaan: angka z-score diubah kembali ke usia, pendapatan, dan skor aslinya.
- Kita bandingkan hasilnya dengan tabel bersih. Jika `True`, penskalaan kita **dapat dibalik tanpa kehilangan informasi**.
- `df_bersih.loc[0, "CustomerID"]` mencari pelanggan pemilik baris ke-0. Karena nomor baris dijaga sama, hubungan itu tetap terjaga.

### Langkah 6 — Uji coba: apakah algoritma menerima dataset ini?

```python
--8<-- "level-2/12_dataset_preparation.py:smoke"
```

```text title="Output"
--8<-- "level-2/outputs/12/smoke.txt"
```

**Penjelasan:**

- Ini **uji coba singkat**, hanya untuk memastikan dataset kita diterima oleh algoritma clustering tanpa galat. **Bukan** clustering yang sesungguhnya.
- `KMeans(n_clusters=5, n_init=10, random_state=42)` membuat model K-Means. `random_state=42` membuat hasil selalu sama, dan `n_init=10` berarti algoritma dicoba dari 10 titik awal lalu diambil yang terbaik.
- `fit_predict(X)` menjalankan algoritma dan menghasilkan nomor kelompok untuk tiap pelanggan.
- `value_counts().sort_index()` menghitung berapa pelanggan di tiap kelompok.
- Jumlah kelompok `5` kita pilih **hanya untuk uji coba**. Cara memilih jumlah kelompok yang tepat, dan menilai apakah hasilnya bagus, dibahas di level berikutnya.

## Code Explanation

Ringkasan hal baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `def nama(...): ... return a, b, c` | Fungsi yang mengembalikan beberapa hasil |
| `raise ValueError("pesan")` | Menghentikan program dengan pesan galat |
| `df.drop_duplicates().reset_index(drop=True)` | Buang duplikat, lalu nomori baris ulang |
| `scaler.inverse_transform(X)` | Mengembalikan data terskala ke satuan asli |
| `KMeans(n_clusters, n_init, random_state)` | Model K-Means |
| `model.fit_predict(X)` | Menjalankan clustering dan memberi nomor kelompok |
| `a, b, c = fungsi()` | Menerima beberapa hasil sekaligus |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/12_dataset_preparation.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/12-dataset-preparation-for-clustering.ipynb
```

## Expected Output

Semua output berasal dari eksekusi nyata skrip (pandas 3.1.1, scikit-learn 1.9.1, Python 3.14.7). Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).


**Cara membaca output:**

- **Ukuran**: tabel bersih `(200, 5)` dan dataset akhir `(200, 3)`: lima kolom menjadi tiga fitur, 200 pelanggan tetap utuh.
- **Pemeriksaan kelayakan**: nol nilai kosong, nol baris ganda, semua kolom angka.
- **Rata-rata `-0.0`**: itu pembulatan angka yang sangat kecil ke nol, bukan nilai negatif sungguhan. Simpangan baku 1,0.
- **Dapat dibalik**: tiga baris pertama kembali menjadi usia 19, 21, 20, pendapatan 15, 15, 16, dan skor 39, 81, 6, persis seperti di data asli. Baris 0 milik `CustomerID` 1.
- **Uji coba K-Means**: berhasil tanpa galat, dengan anggota tiap kelompok 20, 54, 40, 39, dan 47 (total 200). Ini hanya bukti bahwa dataset diterima. Kita belum tahu apakah lima kelompok itu "benar".

## Practical Examples

**Menerapkan alur yang sama pada data baru.** Misalkan bulan depan kamu mendapat file pelanggan baru dengan kolom yang sama. Cukup panggil:

```python
df_baru, X_baru, scaler_baru = siapkan_dataset("data/pelanggan_bulan_depan.csv")
```

Semua langkah akan dijalankan dengan cara yang sama. (File itu hanya contoh nama. Kamu perlu menyiapkannya sendiri.)

**Menjelaskan hasil kepada orang lain.** Setelah clustering nanti, kamu ingin melaporkan "kelompok ini rata-rata berpendapatan berapa?". Caranya: tambahkan nomor kelompok ke `df_bersih` (satuan asli), lalu hitung rata-rata per kelompok. Angka terskala seperti −1,739 tidak bermakna bagi pembaca, tetapi 15 ribu dolar bermakna.

**Mendokumentasikan keputusan.** Tabel keputusan di bagian *Fundamental Concepts* adalah dokumentasi minimal. Kebiasaan ini membantu dirimu sendiri di masa depan, dan orang lain yang ingin mereproduksi pekerjaanmu.

!!! tip "Sebelum lanjut ke Level 3"
    Pastikan kamu bisa menjawab: *Apa yang diubah dari data mentah? Mengapa? Dan bagaimana mengembalikannya?* Jika ya, Level 2 sudah kamu kuasai.

## Hands-on Exercises

1. Ubah `FITUR` menjadi hanya `["Annual Income (k$)", "Spending Score (1-100)"]`. Berapa bentuk dataset akhirnya?
2. Ganti `StandardScaler` dengan `MinMaxScaler`. Periksa nilai minimum dan maksimum tiap kolom pada dataset akhir.
3. Tambahkan pemeriksaan ke fungsi: jika ada skor belanja di luar 1–100, hentikan dengan `raise ValueError`.
4. Jalankan uji coba K-Means dengan `n_clusters=3`. Berapa anggota tiap kelompok?
5. Mengapa kita menyimpan `scaler`, bukan hanya dataset terskalanya?

??? question "Jawaban"
    1. `(200, 2)`: 200 baris dan 2 kolom.
    2. Minimum tiap kolom 0 dan maksimum 1 (Bab 10). Jalankan `X.agg(["min", "max"])` untuk membuktikannya.
    3. Contoh: `if not df["Spending Score (1-100)"].between(1, 100).all(): raise ValueError("Skor di luar 1-100")`.
    4. Hasilnya berupa angka dari eksekusi nyata, jadi jalankan sendiri. Jumlah seluruh anggota harus tetap 200.
    5. `scaler` menyimpan rata-rata dan simpangan baku yang dipakai. Tanpa itu kita tidak bisa mengembalikan angka terskala ke satuan asli, dan tidak bisa menskalakan data baru dengan cara yang sama.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ValueError: Masih ada nilai kosong pada fitur` | Data berisi `NaN` | Tangani dengan teknik Bab 5 sebelum `siapkan_dataset` |
| `KeyError` pada nama fitur | Nama kolom pada `FITUR` berbeda dengan di CSV | Salin nama dari `df.columns` |
| `ModuleNotFoundError: sklearn` | scikit-learn belum terpasang | `pip install -r requirements-notebooks.txt` |
| Hasil K-Means berbeda tiap dijalankan | `random_state` tidak ditetapkan | Tambahkan `random_state=42` |
| Pesan `ConvergenceWarning` pada K-Means | Algoritma tidak konvergen dalam batas iterasi | Naikkan `max_iter`, atau periksa ulang datanya |

## Summary

- Persiapan data = merangkai langkah Level 2 dengan **urutan tetap**: bersihkan, periksa kosong dan duplikat, nilai outlier, pilih fitur, skalakan.
- Bungkus dalam **fungsi** supaya bisa diulang dan mudah dipahami.
- Simpan `scaler` agar angka terskala bisa **dikembalikan** ke satuan asli.
- Lakukan **uji kelayakan** pada dataset akhir: tidak ada nilai kosong atau ganda, semua angka, rata-rata ~0, simpangan baku ~1.
- Dataset akhir kita: **200 pelanggan × 3 fitur** terstandardisasi. Uji coba K-Means menerimanya tanpa galat, dan evaluasinya dibahas di level berikutnya.
- **Catat setiap keputusan** beserta alasannya.

## References

- scikit-learn documentation: [*Pipeline and composite estimators*](https://scikit-learn.org/stable/modules/compose.html) dan [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).
- scikit-learn documentation: [*Clustering*](https://scikit-learn.org/stable/modules/clustering.html#k-means).
- Lloyd, S. (1982). *Least squares quantization in PCM*. IEEE Transactions on Information Theory, 28(2), 129–137.
