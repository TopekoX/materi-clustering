# Bab 2 — Understanding Data Types

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan perbedaan data **numerik** dan **kategorik**.
- [x] Membedakan skala **nominal**, **ordinal**, **interval**, dan **rasio**.
- [x] Membedakan data **diskrit** dan **kontinu**.
- [x] Memeriksa tipe data kolom dengan `dtypes`, `info()`, dan `select_dtypes()`.
- [x] Mengubah kolom teks menjadi tipe `category` dengan `astype()`.
- [x] Menjelaskan mengapa tipe data memengaruhi clustering.

## Introduction

Di Bab 1 kita sudah mengintip isi dataset. Sekarang kita perlu bertanya satu hal penting pada setiap kolom: **"Ini data jenis apa?"**

Pertanyaan ini penting karena **komputer dan algoritma memperlakukan tiap jenis data dengan cara berbeda**. Angka bisa dijumlahkan dan dihitung jaraknya. Teks tidak bisa. Dan ada angka yang sebenarnya bukan "angka sungguhan", misalnya nomor urut pelanggan. Kalau salah mengenali jenis data, hasil clustering bisa menyesatkan tanpa kita sadari.

## Fundamental Concepts

### Dua kelompok besar

| Kelompok | Arti | Contoh pada dataset |
|---|---|---|
| **Numerik** | Berisi angka yang punya makna hitung | `Age`, `Annual Income (k$)`, `Spending Score (1-100)` |
| **Kategorik** | Berisi kelompok atau label | `Gender` |

### Empat skala pengukuran

Para ahli statistik membagi data ke dalam empat skala. Kamu tidak perlu menghafal, cukup pahami perbedaan dasarnya:

| Skala | Ciri | Contoh |
|---|---|---|
| **Nominal** | Hanya nama kelompok. Tidak ada urutan | `Gender` (Female, Male) |
| **Ordinal** | Ada urutan, tetapi jarak antar tingkat tidak pasti sama | Tingkat kepuasan: buruk, cukup, baik |
| **Interval** | Ada urutan dan jarak sama, tetapi nol bukan "kosong sungguhan" | Suhu dalam derajat Celsius |
| **Rasio** | Ada urutan, jarak sama, dan nol berarti "tidak ada" | `Age`, `Annual Income (k$)` |

### Diskrit dan kontinu

- **Diskrit**: hanya bisa bernilai bilangan tertentu, biasanya hasil menghitung. Contoh: usia dalam tahun penuh.
- **Kontinu**: bisa bernilai apa saja dalam rentang tertentu, biasanya hasil mengukur. Contoh: berat badan 60,35 kg.

### Tipe data di pandas

| Tipe pandas | Arti | Contoh |
|---|---|---|
| `int64` | Bilangan bulat | `Age` |
| `float64` | Bilangan desimal | 3,14 |
| `str` / `object` | Teks | `Gender` |
| `category` | Teks dengan sedikit pilihan nilai | `Gender` setelah diubah |
| `bool` | Benar atau salah | `True` |

!!! note "`str` atau `object`?"
    Pandas versi 3 menampilkan kolom teks sebagai `str`. Versi yang lebih lama menampilkannya sebagai `object`. Keduanya berarti sama: kolom berisi teks.

## Detailed Explanation

### Mengenali jenis tiap kolom

Berikut hasil analisis untuk kelima kolom dataset Mall Customers:

| Kolom | Tipe pandas | Jenis | Skala | Catatan |
|---|---|---|---|---|
| `CustomerID` | `int64` | Identitas | — | Hanya nomor urut. Bukan ukuran apa pun |
| `Gender` | `str` | Kategorik | Nominal | Dua nilai: `Female` dan `Male` |
| `Age` | `int64` | Numerik, diskrit | Rasio | Usia dalam tahun penuh |
| `Annual Income (k$)` | `int64` | Numerik | Rasio | Pendapatan tahunan, dalam ribu dolar |
| `Spending Score (1-100)` | `int64` | Numerik | Skor | Skor dari pihak mall. Kita perlakukan sebagai angka |

!!! warning "Angka belum tentu numerik"
    `CustomerID` bertipe `int64` sehingga *terlihat* seperti angka. Padahal ia hanya **label** untuk membedakan satu pelanggan dari yang lain. Menghitung rata-rata nomor pelanggan tidak ada artinya. Pandas tidak tahu hal ini, jadi **kita** yang harus menyadarinya.

### Mengapa tipe data penting untuk clustering

1. **Algoritma berbasis jarak butuh angka.** K-Means, misalnya, menghitung jarak antar pelanggan. Kolom teks seperti `Gender` harus diubah menjadi angka dulu (*encoding*, Bab 9).
2. **Kolom identitas harus dibuang.** `CustomerID` tidak boleh ikut dihitung jaraknya (Bab 11).
3. **Skala menentukan perlakuan.** Kolom nominal tidak boleh diperlakukan seolah punya urutan. Misalnya, memberi kode `Female = 0` dan `Male = 1` lalu menghitung jaraknya perlu kehati-hatian.

## Mathematical Foundation

Bab ini tidak memerlukan rumus. Konsep tipe data dan skala pengukuran bersifat definisi, bukan perhitungan.

## Python Implementation

Kita kerjakan dalam enam langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/02_data_types.py`, dan versi notebook-nya di `notebooks/level-2/02-understanding-data-types.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/02_data_types.py:setup"
```

**Penjelasan:**

- `import pandas as pd` memanggil pustaka *pandas* dan menamainya `pd`.
- `DATA_PATH` menyimpan lokasi file data.
- `pd.read_csv(DATA_PATH)` membaca file CSV menjadi tabel (DataFrame) bernama `df`.

### Langkah 2 — Lihat tipe data tiap kolom

```python
--8<-- "level-2/02_data_types.py:dtypes"
```

**Penjelasan:**

- `df.dtypes` menampilkan tipe data setiap kolom, satu baris per kolom.
- `df.info()` memberi gambaran yang lebih lengkap: jumlah baris, jumlah data **yang tidak kosong** (`Non-Null Count`) per kolom, tipe data, dan penggunaan memori.
- Perhatikan bahwa `info()` langsung **menampilkan** hasilnya, jadi kita tidak perlu membungkusnya dengan `print()`.

### Langkah 3 — Pisahkan kolom angka dan kolom teks

```python
--8<-- "level-2/02_data_types.py:split"
```

**Penjelasan:**

- `df.select_dtypes(include="number")` memilih **hanya kolom bertipe angka**. Kebalikannya, `exclude="number"` memilih semua kolom **selain** angka.
- `.columns` mengambil nama-nama kolom yang terpilih.
- `.tolist()` mengubah nama-nama itu menjadi daftar (list) Python biasa, supaya mudah dibaca dan dipakai lagi.
- Pemisahan seperti ini berguna nanti, karena kolom angka dan kolom teks diproses dengan cara berbeda.

### Langkah 4 — Hitung nilai unik

```python
--8<-- "level-2/02_data_types.py:unique"
```

**Penjelasan:**

- `df.nunique()` menghitung **ada berapa nilai berbeda** di setiap kolom.
- Ini petunjuk cepat untuk mengenali jenis kolom. Kolom dengan **sedikit nilai unik** (seperti `Gender`: hanya 2) biasanya kategorik. Kolom dengan **nilai unik sama dengan jumlah baris** (seperti `CustomerID`: 200 dari 200) biasanya hanya identitas.
- `df["Gender"].unique()` menampilkan nilai-nilai berbeda itu sendiri.

### Langkah 5 — Ubah teks menjadi tipe `category`

```python
--8<-- "level-2/02_data_types.py:category"
```

**Penjelasan:**

- `memory_usage(deep=True)` menghitung berapa byte memori yang dipakai kolom `Gender`.
- `astype("category")` **mengubah tipe** kolom menjadi `category`. Pandas lalu menyimpan setiap pilihan nilai (`Female`, `Male`) sekali saja, dan tiap baris hanya mencatat nomor pilihannya.
- Hasilnya, memori turun drastis, dan pandas jadi tahu bahwa kolom ini **kategorik** dengan pilihan yang terbatas.
- `.cat.categories` menampilkan daftar pilihan yang ada.

### Langkah 6 — Cek rentang nilai

```python
--8<-- "level-2/02_data_types.py:scale"
```

**Penjelasan:**

- Loop `for kolom in [...]` mengulang pekerjaan yang sama untuk tiap kolom angka.
- `df[kolom].min()` dan `.max()` mencari nilai terkecil dan terbesar.
- `f"{kolom}: min=..."` adalah *f-string*: cara menyisipkan nilai variabel ke dalam teks.
- Baris terakhir memeriksa apakah `CustomerID` hanya berupa urutan 1 sampai 200. Jika `True`, itu bukti bahwa kolom ini hanya penomoran.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `df.dtypes` | Tipe data tiap kolom |
| `df.info()` | Ringkasan: jumlah baris, data tidak kosong, tipe, memori |
| `df.select_dtypes(include=..., exclude=...)` | Memilih kolom berdasarkan tipe |
| `df.nunique()` | Jumlah nilai unik per kolom |
| `kolom.unique()` | Daftar nilai unik |
| `kolom.astype("category")` | Mengubah tipe kolom |
| `kolom.memory_usage(deep=True)` | Memori yang dipakai kolom |

## How to Run

Jalankan dari **folder utama proyek** (folder yang berisi `mkdocs.yml`), dengan lingkungan Python yang sudah menginstal `requirements-notebooks.txt`:

```powershell
python examples/level-2/02_data_types.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/02-understanding-data-types.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, Python 3.14.7):

```text
--8<-- "level-2/outputs/02.txt"
```

**Cara membaca output:**

- `info()` menunjukkan `200 non-null` pada semua kolom, artinya tidak ada data kosong.
- `Gender` punya 2 nilai unik, sedangkan `CustomerID` punya 200 (sama dengan jumlah baris).
- Setelah diubah ke `category`, memori kolom `Gender` turun dari 10.956 byte menjadi 440 byte.
- Pada contoh kecil seperti ini, penghematan memori tidak penting. Pada dataset jutaan baris, hemat memori terasa.

## Practical Examples

**1. Menemukan kolom yang tidak boleh dipakai.** `nunique()` menunjukkan `CustomerID` punya 200 nilai unik dari 200 baris, dan `df["CustomerID"].tolist() == list(range(1, 201))` bernilai `True`. Kesimpulannya jelas: ini penomoran, bukan karakteristik pelanggan.

**2. Memutuskan kolom mana yang perlu diubah.** `Gender` adalah kolom teks nominal. Sebelum dipakai algoritma berbasis jarak, kolom ini perlu di-*encode* (Bab 9).

**3. Mencurigai tipe yang salah.** Bayangkan kolom `Age` terbaca sebagai teks (`str`) karena ada satu sel berisi tulisan "tidak diketahui". Itu pertanda ada data kotor. Di dataset ini hal itu **tidak terjadi**: keempat kolom angka terbaca sebagai `int64`. Pada data nyata, pemeriksaan tipe adalah cara cepat menemukan masalah seperti itu.

## Hands-on Exercises

1. Kolom mana saja yang bertipe angka? Tulis jawabanmu, lalu cocokkan dengan output `select_dtypes`.
2. Skala pengukuran apa yang paling tepat untuk `Gender`? Mengapa?
3. Mengapa `CustomerID` tidak cocok dipakai sebagai fitur clustering, walaupun bertipe `int64`?
4. Ubah kolom `Age` menjadi `float64` dengan `astype("float64")`, lalu periksa `dtypes`.
5. Berapa nilai unik pada kolom `Spending Score (1-100)`? Apakah angka itu berarti tiap pelanggan punya skor berbeda?

??? question "Jawaban"
    1. `CustomerID`, `Age`, `Annual Income (k$)`, dan `Spending Score (1-100)`. Hanya `Gender` yang berupa teks.
    2. **Nominal.** `Female` dan `Male` hanya nama kelompok. Tidak ada urutan dan tidak ada jarak di antara keduanya.
    3. `CustomerID` hanya nomor urut untuk membedakan pelanggan. Nilainya tidak menggambarkan sifat pelanggan, tetapi bisa memengaruhi perhitungan jarak tanpa makna apa pun.
    4. `df["Age"] = df["Age"].astype("float64")`, lalu `df.dtypes`. Kolom `Age` akan tampil sebagai `float64`.
    5. Ada **84** nilai unik (lihat output `nunique()`). Karena ada 200 pelanggan, artinya banyak pelanggan berbagi skor yang sama.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| Kolom angka terbaca sebagai teks (`str` atau `object`) | Ada sel berisi tulisan atau simbol, misalnya `"-"` atau `"N/A"` | Periksa nilai uniknya dengan `unique()`, bersihkan, lalu ubah dengan `pd.to_numeric()` (Bab 8) |
| `select_dtypes` mengembalikan daftar kosong | Tidak ada kolom dengan tipe tersebut | Periksa penulisan: `"number"`, bukan `"numeric"` |
| Setelah `astype("category")`, perhitungan aneh | Kolom `category` tidak bisa langsung dihitung rata-ratanya | Gunakan `category` hanya untuk kolom label, bukan angka |
| Tampilan `str` berbeda dengan teman yang memakai `object` | Beda versi pandas | Bukan kesalahan. Keduanya berarti teks |
| `AttributeError: Can only use .cat accessor with a 'category' dtype` | Memanggil `.cat` sebelum kolom diubah | Jalankan `astype("category")` terlebih dulu |

## Summary

- Data dibagi menjadi **numerik** dan **kategorik**. Skalanya: nominal, ordinal, interval, rasio.
- Angka belum tentu numerik sungguhan. `CustomerID` hanya identitas.
- Pada Mall Customers: empat kolom bertipe angka, satu kolom teks (`Gender`, nominal).
- Alat utama: `dtypes`, `info()`, `select_dtypes()`, `nunique()`, `astype()`.
- Tipe data menentukan perlakuan: teks perlu di-*encode*, identitas perlu dibuang, dan angka perlu diperiksa skalanya.

## References

- pandas documentation: [*Essential basic functionality*](https://pandas.pydata.org/docs/user_guide/basics.html) dan [*Categorical data*](https://pandas.pydata.org/docs/user_guide/categorical.html).
- pandas documentation: [`DataFrame.select_dtypes`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.select_dtypes.html).
- Stevens, S. S. (1946). *On the Theory of Scales of Measurement*. Science, 103(2684), 677–680.
