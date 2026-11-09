# Bab 5 — Missing Values Analysis

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan apa itu *missing value* dan mengapa ia menjadi masalah.
- [x] Membedakan tiga jenis penyebab data kosong: MCAR, MAR, dan MNAR.
- [x] Menghitung jumlah dan persentase nilai kosong dengan `isna()`.
- [x] Menangani nilai kosong dengan membuang baris (`dropna`) atau mengisinya (`fillna`, `SimpleImputer`).
- [x] Membandingkan dampak tiap strategi terhadap data.

## Introduction

Dalam data nyata, sering ada sel yang kosong: responden tidak mengisi usia, sensor gagal mencatat, atau data hilang saat dipindahkan. Di pandas, sel kosong ditulis sebagai **`NaN`** (*Not a Number*).

Masalahnya, **sebagian besar algoritma clustering tidak bisa memproses nilai kosong**. Scikit-learn akan langsung menolak data yang mengandung `NaN`. Jadi kita harus menanganinya sebelum clustering.

!!! warning "Dataset ini sebenarnya tidak punya nilai kosong"
    Di Bab 1 kita sudah melihat bahwa Mall Customers **tidak punya nilai kosong**. Supaya kita bisa berlatih, bab ini **sengaja mengosongkan sebagian nilai pada salinan data** (simulasi, dengan `random seed` tetap). Itu bukan temuan dari data asli. Data asli tetap tidak diubah.

## Fundamental Concepts

### Tiga penyebab data kosong

| Jenis | Singkatan | Arti | Contoh |
|---|---|---|---|
| **Missing Completely At Random** | MCAR | Kosong secara acak, tidak ada hubungannya dengan data lain | Sensor sesekali gagal tanpa pola |
| **Missing At Random** | MAR | Peluang kosong berhubungan dengan kolom **lain** yang kita punya | Pelanggan muda lebih sering tidak mengisi pendapatan |
| **Missing Not At Random** | MNAR | Peluang kosong berhubungan dengan **nilai kosong itu sendiri** | Orang berpendapatan sangat tinggi enggan mengisi pendapatan |

Mengapa ini penting? Pada MCAR, membuang atau mengisi data relatif aman. Pada MAR dan MNAR, cara penanganan bisa **menggeser** hasil analisis.

### Strategi penanganan

| Strategi | Cara | Kelebihan | Kekurangan |
|---|---|---|---|
| **Buang baris** | `dropna()` | Sederhana | Kehilangan data. Bisa bias jika kosongnya tidak acak |
| **Isi dengan mean** | `fillna(mean)` | Mudah | Terpengaruh nilai ekstrem |
| **Isi dengan median** | `fillna(median)` | Tahan nilai ekstrem | Mengurangi variasi data |
| **Isi dengan modus** | `fillna(modus)` | Cocok untuk kolom kategori | Mengurangi variasi data |
| **Buang kolom** | `drop(columns=...)` | Masuk akal jika hampir seluruh kolom kosong | Kehilangan seluruh informasi kolom itu |

## Detailed Explanation

### Langkah berpikir

1. **Ukur dulu.** Berapa persen yang kosong? Di kolom mana?
2. **Cari tahu penyebabnya.** Acak atau berpola? Pertanyaan ini sering hanya bisa dijawab dengan memahami asal datanya.
3. **Pilih strategi** sesuai jumlah dan penyebabnya.
4. **Bandingkan hasilnya** dengan data sebelum diubah.

!!! tip "Aturan praktis, bukan hukum"
    Jika yang kosong hanya sedikit (misalnya di bawah 5% baris) dan tampak acak, membuang baris sering cukup. Jika banyak baris terdampak, membuangnya berarti kehilangan banyak data, sehingga mengisi nilai lebih masuk akal. Jika sebuah kolom kosong sebagian besar, pertimbangkan membuang kolomnya. Angka ambang ini bukan standar baku, tetapi pegangan awal.

### Mengisi nilai tidak gratis

Setiap nilai yang kita isi adalah **tebakan**. Mengisi dengan median membuat banyak baris punya nilai yang sama persis, sehingga variasi data sedikit mengecil. Pada clustering, hal ini bisa menarik banyak titik ke arah tengah.

## Mathematical Foundation

Strategi isian paling sederhana memakai statistik dari nilai yang **tidak** kosong.

Untuk pengisian dengan **mean** dari \(m\) nilai yang tersedia \(x_1, \dots, x_m\):

$$
\hat{x} = \frac{1}{m} \sum_{i=1}^{m} x_i
$$

Untuk **median**, \(\hat{x}\) adalah nilai tengah dari \(m\) nilai itu setelah diurutkan.

## Python Implementation

Kita kerjakan dalam delapan langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/05_missing_values.py`, dan versi notebook-nya di `notebooks/level-2/05-missing-values-analysis.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/05_missing_values.py:setup"
```

**Penjelasan:**

- `numpy` (disingkat `np`) adalah pustaka angka yang dipakai pandas di baliknya. Di sini kita memakainya untuk membuat angka acak dan nilai `NaN`.
- `pandas` membaca file CSV menjadi tabel `df`.

### Langkah 2 — Periksa data asli

```python
--8<-- "level-2/05_missing_values.py:real"
```

**Penjelasan:**

- `df.isna()` menandai sel kosong dengan `True`. Pertama `.sum()` menjumlahkan per kolom, kedua `.sum()` menjumlahkan semua kolom menjadi satu angka.
- Hasil `0` berarti data asli bersih dari nilai kosong.

### Langkah 3 — Buat salinan dengan nilai kosong buatan

```python
--8<-- "level-2/05_missing_values.py:simulate"
```

**Penjelasan:**

- `np.random.default_rng(42)` membuat generator angka acak. Angka `42` adalah **seed**: dengan seed yang sama, hasil acaknya selalu sama, jadi hasilmu pasti sama dengan di buku ini.
- `df.copy()` membuat **salinan** tabel. Kita mengosongkan salinannya, supaya data asli aman.
- `rng.choice(df_kosong.index, size=10, replace=False)` memilih 10 nomor baris secara acak. `replace=False` artinya tidak ada baris yang terpilih dua kali.
- `df_kosong.loc[baris_terpilih, kolom] = np.nan` mengosongkan sel pada baris-baris itu. `loc` berarti "pilih berdasarkan label baris dan nama kolom".
- Kita lakukan ini pada `Age` dan `Annual Income (k$)`, masing-masing 10 sel (5% dari 200 baris).

### Langkah 4 — Temukan nilai kosong

```python
--8<-- "level-2/05_missing_values.py:detect"
```

**Penjelasan:**

- `df_kosong.isna().sum()` menghitung sel kosong per kolom.
- `df_kosong.isna().mean() * 100` menghitung **persentase**: rata-rata dari `True/False` sama dengan proporsi `True`.
- `df_kosong.isna().any(axis=1)` memeriksa **per baris** apakah ada minimal satu sel kosong. `axis=1` berarti "arah baris". Hasil `.sum()` adalah banyaknya baris bermasalah.
- `df_kosong[...]` dengan syarat `True/False` di dalamnya hanya menampilkan baris yang memenuhi syarat. `.head()` membatasi tampilan ke 5 baris.

### Langkah 5 — Strategi 1: buang baris yang kosong

```python
--8<-- "level-2/05_missing_values.py:dropna"
```

**Penjelasan:**

- `dropna()` membuang semua baris yang punya minimal satu sel kosong, dan mengembalikan tabel baru.
- Kita bandingkan ukuran sebelum dan sesudah untuk melihat berapa baris yang hilang.

### Langkah 6 — Strategi 2: isi dengan median

```python
--8<-- "level-2/05_missing_values.py:fillna"
```

**Penjelasan:**

- Kita ulangi untuk setiap kolom yang punya nilai kosong.
- `median()` menghitung nilai tengah dari sel yang **tidak** kosong (pandas otomatis mengabaikan `NaN`).
- `fillna(median)` mengganti semua `NaN` di kolom itu dengan nilai median.
- Setelah ini, sisa nilai kosong harus 0, dan jumlah baris tetap 200.

### Langkah 7 — Bandingkan hasilnya dengan data asli

```python
--8<-- "level-2/05_missing_values.py:compare"
```

**Penjelasan:**

- Kita membuat tabel kecil yang membandingkan **rata-rata** kolom pada tiga versi data: asli, hasil buang baris, dan hasil isi median.
- Tujuannya memeriksa apakah strategi kita menggeser data. Selisih kecil berarti penanganannya tidak merusak gambaran data.

### Langkah 8 — Mengisi dengan scikit-learn

```python
--8<-- "level-2/05_missing_values.py:imputer"
```

**Penjelasan:**

- `SimpleImputer(strategy="median")` adalah alat siap pakai dari scikit-learn untuk mengisi nilai kosong. Ia melakukan hal yang sama dengan Langkah 6.
- `fit_transform(...)` melakukan dua hal sekaligus: **belajar** median tiap kolom (`fit`), lalu **mengisi** nilai kosong (`transform`).
- `imputer.statistics_` menampilkan median yang ia pelajari.
- Keunggulan alat ini: ia bisa dipakai ulang pada data baru dengan median yang sama, dan mudah disambungkan ke alur kerja scikit-learn lainnya.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `df.isna()` | Menandai sel kosong |
| `.isna().sum()` | Jumlah kosong per kolom |
| `.isna().mean()` | Proporsi kosong per kolom |
| `.isna().any(axis=1)` | Baris mana yang punya sel kosong |
| `df.dropna()` | Membuang baris yang punya sel kosong |
| `kolom.fillna(nilai)` | Mengisi sel kosong |
| `df.copy()` | Membuat salinan tabel |
| `SimpleImputer(strategy=...)` | Alat scikit-learn untuk mengisi nilai kosong |
| `np.random.default_rng(seed)` | Generator angka acak dengan seed |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/05_missing_values.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/05-missing-values-analysis.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, scikit-learn 1.9.1, Python 3.14.7):

```text
--8<-- "level-2/outputs/05.txt"
```

**Cara membaca output:**

- Data asli: **0** nilai kosong. Salinan: 10 kosong pada `Age` dan 10 pada `Annual Income (k$)`, masing-masing **5,0%**.
- **19 baris** punya minimal satu sel kosong, bukan 20, karena satu baris kebetulan kosong di kedua kolom.
- Membuang baris: ukuran turun dari `(200, 5)` menjadi `(181, 5)`. **19 pelanggan hilang**.
- Mengisi median: ukuran tetap `(200, 5)`. Median yang dipakai: 36,0 untuk `Age` dan 61,5 untuk `Annual Income (k$)`.
- Rata-rata `Age`: asli 38,85, buang baris 38,71, isi median 38,78. Rata-rata `Annual Income (k$)`: asli 60,56, buang baris 60,88, isi median 60,42. Semuanya berdekatan.
- `SimpleImputer` memberi hasil yang sama dengan `fillna`: tidak ada nilai kosong tersisa, dengan median `[36., 61.5]`.

## Practical Examples

**Mengapa selisihnya kecil di sini?** Karena nilai kosongnya kita buat **acak** (MCAR) dan jumlahnya sedikit (5%). Pada data nyata, kekosongan jarang sebersih ini. Jika kekosongan berpola (MAR atau MNAR), membuang baris atau mengisi median bisa **menggeser** rata-rata cukup jauh. Maka pemeriksaan dengan membandingkan rata-rata, seperti Langkah 7, patut dibiasakan.

**Pilihan untuk clustering.** Karena clustering tidak punya label, setiap pelanggan yang dibuang adalah satu titik yang tidak akan pernah masuk kelompok mana pun. Untuk data kecil seperti ini (200 baris), mengisi nilai sering lebih baik daripada membuang 19 pelanggan. Untuk data besar dengan sedikit baris kosong, membuang bisa jadi cukup.

**Kolom kategori.** Untuk kolom seperti `Gender` yang kosong, median tidak berlaku. Gunakan **modus** (nilai paling sering): `df["Gender"].fillna(df["Gender"].mode()[0])`.

## Hands-on Exercises

1. Ubah `size=10` menjadi `size=40` pada Langkah 3. Berapa persen yang kosong? Berapa baris yang tersisa setelah `dropna()`?
2. Isi nilai kosong dengan **mean** (bukan median). Apakah rata-ratanya berubah dibanding isi median?
3. Mengapa `SimpleImputer(strategy="most_frequent")` cocok untuk kolom `Gender`?
4. Mengapa kita memakai `df.copy()` sebelum mengosongkan data?
5. Sebutkan satu situasi di mana membuang baris yang kosong adalah pilihan yang buruk.

??? question "Jawaban"
    1. 40 dari 200 sel kosong per kolom = **20%**. Jumlah baris tersisa dihitung dari output `dropna()`: pasti kurang dari 200 dan bisa jauh berkurang, karena baris yang terdampak di dua kolom hampir tidak tumpang tindih. Jalankan sendiri dan catat angkanya.
    2. Jalankan dan bandingkan. Mean cenderung lebih terpengaruh nilai ekstrem daripada median, jadi selisihnya bisa sedikit berbeda.
    3. `most_frequent` mengisi dengan modus (nilai paling sering), yang cocok untuk teks. Median hanya untuk angka.
    4. Supaya data asli tetap utuh. Tanpa `copy()`, perubahan pada variabel baru bisa ikut mengubah tabel asli.
    5. Misalnya ketika kekosongan berpola (MNAR): membuang baris itu menghapus justru kelompok tertentu, sehingga data yang tersisa tidak lagi mewakili kenyataan. Contoh lain: jika sebagian besar baris punya minimal satu sel kosong, membuangnya menghabiskan data.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ValueError: Input X contains NaN` saat clustering | Masih ada nilai kosong | Tangani dulu dengan `dropna`, `fillna`, atau `SimpleImputer` |
| `fillna` tidak mengubah tabel | Hasilnya tidak disimpan | Simpan hasilnya: `df["Age"] = df["Age"].fillna(...)` |
| Nilai kosong tertulis `"?"` atau `"-"`, bukan `NaN` | Pandas tidak mengenalinya sebagai kosong | Baca dengan `pd.read_csv(..., na_values=["?", "-"])` |
| `SettingWithCopyWarning` | Mengubah potongan tabel, bukan tabel utuh | Pakai `df.copy()` dan `loc` |
| `KeyError` pada `dropna(subset=[...])` | Nama kolom salah | Salin nama dari `df.columns` |

## Summary

- Nilai kosong (`NaN`) harus ditangani sebelum clustering.
- Tiga penyebab: MCAR, MAR, MNAR. Penyebabnya memengaruhi pilihan strategi.
- Strategi utama: buang baris (`dropna`), isi dengan median/mean/modus (`fillna`, `SimpleImputer`), atau buang kolom.
- Selalu **bandingkan** statistik sebelum dan sesudah penanganan.
- Di bab ini, nilai kosong dibuat **sengaja pada salinan data** untuk latihan. Data asli Mall Customers tidak punya nilai kosong.

## References

- Little, R. J. A., & Rubin, D. B. (2019). *Statistical Analysis with Missing Data* (3rd ed.). Wiley.
- pandas documentation: [*Working with missing data*](https://pandas.pydata.org/docs/user_guide/missing_data.html).
- scikit-learn documentation: [*Imputation of missing values*](https://scikit-learn.org/stable/modules/impute.html).
