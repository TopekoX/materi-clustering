# Bab 8 — Data Cleaning

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan apa itu *data cleaning* dan mengapa urutan langkahnya penting.
- [x] Merapikan teks dengan `str.strip()`, `str.lower()`, dan `str.title()`.
- [x] Mengubah teks menjadi angka dengan `pd.to_numeric(errors="coerce")`.
- [x] Memeriksa dan memperbaiki nilai yang tidak masuk akal.
- [x] Merapikan nama kolom dengan `rename()`.
- [x] Membungkus langkah-langkah pembersihan dalam satu fungsi.

## Introduction

Bab 5 sampai 7 membahas masalah yang spesifik: nilai kosong, duplikat, dan outlier. **Data cleaning** adalah payung yang lebih luas: semua pekerjaan **memperbaiki data** agar konsisten dan benar sebelum dipakai.

Masalah yang umum ditemui pada data nyata:

- Teks tidak konsisten: `"male"`, `"Male"`, `" MALE "` padahal artinya sama.
- Angka tersimpan sebagai teks: `"25"`, atau tercampur tulisan `"tidak diketahui"`.
- Nilai mustahil: usia 250 tahun.
- Nama kolom berantakan: spasi, tanda kurung, huruf besar-kecil acak.

!!! warning "Data asli sudah cukup bersih, jadi ada tabel latihan buatan"
    Mall Customers **tidak punya masalah-masalah di atas** (kita buktikan di Langkah 2). Supaya kamu bisa berlatih, bab ini membuat **tabel kecil berisi 5 baris yang sengaja dikotori** di dalam kode. Isi tabel itu **artifisial**, bukan bagian dari data asli.

## Fundamental Concepts

| Masalah | Contoh | Alat pandas |
|---|---|---|
| Spasi berlebih | `"Female "` | `str.strip()` |
| Huruf besar-kecil tidak konsisten | `"FEMALE"`, `"female"` | `str.lower()`, `str.title()` |
| Angka bertipe teks | `"19"` | `pd.to_numeric()` |
| Teks pengganti nilai | `"tidak diketahui"` | `pd.to_numeric(errors="coerce")` |
| Nilai mustahil | `Age = 250` | Pemeriksaan rentang, `between()` |
| Nama kolom berantakan | `"Annual Income (k$)"` | `rename()` |

### Urutan yang disarankan

1. **Rapikan teks** dulu, karena banyak masalah lain bergantung pada teks yang konsisten.
2. **Ubah tipe** kolom ke tipe yang benar (angka, kategori).
3. **Periksa rentang** nilai yang masuk akal.
4. **Tangani** nilai kosong yang timbul dari langkah-langkah di atas (Bab 5), dan duplikat (Bab 6).
5. **Rapikan nama kolom** bila perlu.

## Detailed Explanation

### `errors="coerce"`: mengubah yang tidak bisa menjadi `NaN`

Saat mengubah teks menjadi angka, nilai seperti `"tidak diketahui"` tidak bisa diubah. Ada dua sikap:

- **Bawaan (`errors="raise"`)**: berhenti dan menampilkan galat. Aman, tetapi menghentikan program.
- **`errors="coerce"`**: nilai yang gagal diubah menjadi **`NaN`** (kosong). Program lanjut, dan kita menangani kosongnya kemudian dengan teknik Bab 5.

### Nilai mustahil: perbaiki, kosongkan, atau buang?

- Jika kesalahannya **jelas dan bisa ditebak** (misalnya 250 seharusnya 25), perbaiki.
- Jika **tidak bisa ditebak**, jadikan `NaN`, lalu tangani seperti nilai kosong lain.
- Hindari menebak tanpa dasar. Mengarang nilai pengganti sama saja dengan mengarang data.

### Fungsi pembersih

Setelah langkahnya jelas, bungkus dalam satu fungsi. Keuntungannya: bisa dipakai ulang pada data baru dan hasilnya selalu konsisten.

## Mathematical Foundation

Bab ini tidak memerlukan rumus. Pembersihan data bersifat prosedural.

## Python Implementation

Kita kerjakan dalam delapan langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/08_data_cleaning.py`, dan versi notebook-nya di `notebooks/level-2/08-data-cleaning.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/08_data_cleaning.py:setup"
```

**Penjelasan:**

- `pd.set_option("display.width", 120)` dan `display.max_columns` hanya mengatur **tampilan**: tabel lebar tidak dipotong dengan tanda `...`. Data tidak berubah.
- Setelah itu kita membaca file CSV menjadi `df`.

### Langkah 2 — Periksa konsistensi data asli

```python
--8<-- "level-2/08_data_cleaning.py:check"
```

**Penjelasan:**

- `sorted(df["Gender"].unique())` menampilkan nilai berbeda pada `Gender`, diurutkan. Jika ada `"male"` dan `"Male"`, keduanya akan muncul terpisah.
- `df["Gender"] != df["Gender"].str.strip()` membandingkan teks asli dengan teks yang sudah dibuang spasi di ujungnya. Jika berbeda, berarti ada spasi berlebih. `.sum()` menghitungnya.
- `between(18, 100)` bernilai `True` jika nilainya berada di antara 18 dan 100. Tanda `~` membaliknya, sehingga yang dihitung adalah nilai **di luar** rentang.
- Pendapatan `<= 0` kita anggap tidak masuk akal.

### Langkah 3 — Buat tabel kecil yang sengaja kotor

```python
--8<-- "level-2/08_data_cleaning.py:messy"
```

**Penjelasan:**

- `pd.DataFrame({...})` membuat tabel dari kamus Python: nama kolom di kiri, daftar isinya di kanan.
- Tabel ini sengaja berisi masalah: `Gender` dengan spasi dan huruf besar-kecil campur aduk, serta `Age` berisi teks `"tidak diketahui"` dan angka mustahil `"250"`.
- Perhatikan `dtypes`: `Age` bertipe `str` (teks), padahal seharusnya angka.

### Langkah 4 — Merapikan teks

```python
--8<-- "level-2/08_data_cleaning.py:text"
```

**Penjelasan:**

- `kotor.copy()` membuat salinan supaya tabel kotor asli tetap ada untuk dibandingkan.
- `str.strip()` membuang spasi di awal dan akhir teks.
- `str.title()` mengubah huruf pertama menjadi kapital, sisanya kecil: `"FEMALE"` menjadi `"Female"`.
- Kedua perintah dirangkai: `.str.strip().str.title()`. Setelahnya, kelima nilai hanya terdiri dari `"Male"` dan `"Female"`.

### Langkah 5 — Mengubah teks menjadi angka

```python
--8<-- "level-2/08_data_cleaning.py:numeric"
```

**Penjelasan:**

- `pd.to_numeric(..., errors="coerce")` mengubah tiap teks menjadi angka. `"19"` menjadi `19.0`.
- `"tidak diketahui"` tidak bisa diubah, jadi menjadi `NaN`.
- Angka yang terbentuk bertipe `float64` (desimal), karena kolom yang berisi `NaN` tidak bisa bertipe bilangan bulat biasa.
- `isna().sum()` memastikan ada 1 nilai kosong.

### Langkah 6 — Memeriksa rentang yang masuk akal

```python
--8<-- "level-2/08_data_cleaning.py:ranges"
```

**Penjelasan:**

- `~bersih["Age"].between(18, 100)` menandai usia di luar 18–100. Tapi `NaN` juga akan ikut ditandai, sehingga kita tambahkan `& bersih["Age"].notna()` ("dan nilainya tidak kosong").
- Hasilnya hanya baris dengan usia 250.
- `bersih.loc[kondisi, "Age"] = float("nan")` mengosongkan usia yang tidak masuk akal. Kita tidak menebak nilai gantinya.

### Langkah 7 — Merapikan nama kolom

```python
--8<-- "level-2/08_data_cleaning.py:rename"
```

**Penjelasan:**

- `rename(columns={lama: baru})` mengganti nama kolom.
- Nama baru memakai huruf kecil dan garis bawah, tanpa spasi atau tanda kurung. Ini lebih mudah diketik dan lebih aman dipakai di kode.
- Pada bab-bab lain kita tetap memakai nama asli kolom, supaya sesuai dengan file CSV.

### Langkah 8 — Membungkus semuanya dalam satu fungsi

```python
--8<-- "level-2/08_data_cleaning.py:pipeline"
```

**Penjelasan:**

- `def bersihkan(data):` mendefinisikan **fungsi**: sekumpulan langkah yang diberi nama, sehingga bisa dipanggil berkali-kali.
- Di dalamnya, kita menyalin tabel lalu menerapkan langkah-langkah pembersihan yang sama seperti di atas.
- `return hasil` mengembalikan tabel yang sudah bersih.
- Kita memanggil fungsi itu pada tabel kotor, lalu pada data asli. Pada data asli, **isi** kolom `Age` tetap sama. Namun tipenya berubah dari `int64` menjadi `float64`. Itu terjadi karena perintah `= float("nan")` membuat kolom bisa menampung nilai kosong, dan kolom bilangan bulat tidak bisa. Ini perilaku normal pandas.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `kolom.str.strip()` | Membuang spasi di ujung teks |
| `kolom.str.title()` / `.str.lower()` | Mengubah huruf besar-kecil |
| `pd.to_numeric(kolom, errors="coerce")` | Mengubah ke angka, yang gagal jadi `NaN` |
| `kolom.between(a, b)` | `True` jika nilai ada di antara `a` dan `b` |
| `kolom.notna()` | Kebalikan dari `isna()` |
| `df.loc[kondisi, kolom] = nilai` | Mengubah nilai pada baris tertentu |
| `df.rename(columns={...})` | Mengganti nama kolom |
| `def nama(parameter): ... return hasil` | Membuat fungsi |
| `pd.DataFrame({...})` | Membuat tabel dari kamus |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/08_data_cleaning.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/08-data-cleaning.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, Python 3.14.7):

```text
--8<-- "level-2/outputs/08.txt"
```

**Cara membaca output:**

- **Data asli konsisten**: `Gender` hanya berisi `Female` dan `Male`, tanpa spasi berlebih. Usia, skor, dan pendapatan semuanya dalam rentang yang masuk akal (hitungannya 0 semua).
- **Tabel kotor** (artifisial): `Gender` tampil sebagai `male`, `FEMALE`, `Female `, `Male`, `female`, dan `Age` bertipe teks.
- **Setelah merapikan teks**: nilai `Gender` menjadi `Male`, `Female`, `Female`, `Male`, `Female`.
- **Setelah `to_numeric`**: `Age` menjadi `[19.0, 21.0, nan, 23.0, 250.0]` dengan 1 nilai kosong.
- **Setelah pemeriksaan rentang**: 250 dikosongkan, sehingga `Age` menjadi `[19.0, 21.0, nan, 23.0, nan]`.
- **Fungsi `bersihkan`**: tabel kotor menjadi bersih (dua usia kosong tersisa untuk ditangani dengan Bab 5). Pada data asli, isi `Age` tetap sama, hanya tipenya yang berubah dari `int64` ke `float64`.

## Practical Examples

**Mengapa urutan penting.** Seandainya kita memeriksa rentang usia **sebelum** mengubah `Age` menjadi angka, perbandingan `between(18, 100)` pada teks akan gagal atau memberi hasil keliru. Karena itu: ubah tipe dulu, baru periksa rentang.

**Cleaning menghasilkan nilai kosong baru.** Dari lima baris tabel kotor, `"tidak diketahui"` dan `250` berakhir sebagai `NaN`. Itu wajar: kita **mengakui** bahwa nilainya tidak diketahui, bukan mengarang. Nilai kosong ini lalu ditangani dengan teknik Bab 5.

**Fungsi untuk konsistensi.** Bayangkan kamu menerima data pelanggan baru setiap bulan. Dengan fungsi `bersihkan`, kamu cukup memanggilnya lagi, dan semua data dibersihkan dengan cara yang sama.

!!! tip "Jangan menimpa data mentah"
    Selalu kerjakan pembersihan pada **salinan** (`copy()`), dan simpan data mentah apa adanya. Dengan begitu kamu selalu bisa kembali bila ada langkah yang keliru.

## Hands-on Exercises

1. Tambahkan satu baris ke tabel kotor dengan `Gender = "  MALE  "`. Apakah `str.strip().str.title()` merapikannya?
2. Ubah `errors="coerce"` menjadi `errors="raise"`. Apa yang terjadi?
3. Tambahkan pemeriksaan: skor belanja yang tidak berada di 1–100 dijadikan `NaN` pada fungsi `bersihkan`.
4. Mengapa kita mengosongkan usia 250, bukan menggantinya dengan 25?
5. Apa arti `~` pada `~bersih["Age"].between(18, 100)`?

??? question "Jawaban"
    1. Ya. `strip()` membuang spasi di kedua ujung dan `title()` menjadikannya `"Male"`.
    2. Pandas menampilkan galat `ValueError` karena `"tidak diketahui"` tidak bisa diubah menjadi angka, dan program berhenti.
    3. Tambahkan di dalam fungsi: `hasil.loc[~hasil["Spending Score (1-100)"].between(1, 100), "Spending Score (1-100)"] = float("nan")`.
    4. Kita tidak punya dasar untuk menebak bahwa 250 maksudnya 25. Bisa saja 52 atau 20. Menebak berarti mengarang data, jadi lebih jujur menandainya sebagai kosong.
    5. `~` berarti **kebalikan** (`True` menjadi `False` dan sebaliknya). Jadi yang dipilih adalah nilai yang **tidak** berada di antara 18 dan 100.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `AttributeError: Can only use .str accessor with string values` | Kolom bukan teks, atau berisi campuran | Pastikan kolomnya bertipe teks, atau ubah dulu dengan `astype(str)` |
| `ValueError: Unable to parse string "..."` | `to_numeric` bertemu teks yang tidak bisa diubah | Tambahkan `errors="coerce"` |
| Kolom `int64` berubah jadi `float64` | Ada `NaN` di dalamnya | Normal. Setelah `NaN` ditangani, ubah kembali dengan `astype("int64")` bila perlu |
| `title()` mengubah `"McDonald"` jadi `"Mcdonald"` | `title()` mengecilkan huruf sisanya | Pakai `str.capitalize()` atau aturan sendiri untuk teks khusus |
| Perubahan tidak tersimpan | Hasil tidak ditugaskan ulang ke kolom | Simpan: `df["kolom"] = df["kolom"].str.strip()` |

## Summary

- **Data cleaning** memperbaiki teks tidak konsisten, tipe yang salah, nilai mustahil, dan nama kolom.
- Alat utama: `str.strip()`, `str.title()`, `pd.to_numeric(errors="coerce")`, `between()`, `loc`, `rename()`.
- Nilai yang mustahil dan tidak bisa diperbaiki dijadikan `NaN`, **bukan ditebak**. Lalu ditangani dengan teknik Bab 5.
- Bungkus langkah-langkah dalam **fungsi** supaya konsisten dan bisa dipakai ulang.
- Mall Customers sudah konsisten. Tabel kotor 5 baris di bab ini **dibuat sengaja** untuk latihan.

## References

- pandas documentation: [*Working with text data*](https://pandas.pydata.org/docs/user_guide/text.html).
- pandas documentation: [`pandas.to_numeric`](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html).
- Wickham, H. (2014). *Tidy Data*. Journal of Statistical Software, 59(10).
