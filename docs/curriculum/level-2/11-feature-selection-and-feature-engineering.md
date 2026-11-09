# Bab 11 — Feature Selection and Feature Engineering

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Membedakan ***feature selection*** (memilih fitur) dan ***feature engineering*** (membuat fitur).
- [x] Menjelaskan mengapa memilih fitur pada clustering berbeda dari pada supervised learning.
- [x] Membuang kolom yang bukan fitur, seperti kolom identitas.
- [x] Mendeteksi fitur yang redundan dengan korelasi.
- [x] Membuat fitur baru dari fitur yang ada, lalu menilai apakah layak dipakai.
- [x] Menyusun beberapa kandidat himpunan fitur.

## Introduction

Tidak semua kolom di dataset layak dipakai untuk clustering. Dan kadang, kolom yang ada belum cukup, sehingga kita perlu membuat kolom baru dari yang sudah ada.

- **Feature selection**: memilih **kolom mana** yang dipakai.
- **Feature engineering**: **membuat kolom baru** dari kolom yang ada.

Keduanya penting karena **fitur menentukan seperti apa "kemiripan" didefinisikan**. Dua pelanggan dianggap mirip jika fitur yang kita pilih mirip. Fitur yang berbeda menghasilkan kelompok yang berbeda.

## Fundamental Concepts

### Berbeda dari supervised learning

Pada supervised learning, kita punya label, sehingga bisa menguji fitur mana yang paling membantu memprediksi label. **Pada clustering tidak ada label**, jadi kita mengandalkan:

| Pegangan | Pertanyaannya |
|---|---|
| **Pengetahuan domain** | Fitur apa yang bermakna untuk tujuan kita? |
| **Variasi** | Apakah kolom ini cukup bervariasi untuk membedakan pelanggan? |
| **Redundansi** (korelasi) | Apakah dua kolom hampir sama informasinya? |
| **Ketersediaan** | Apakah kolom ini sudah bersih dan bisa dipakai algoritma? |

### Masalah yang ingin dihindari

| Masalah | Penyebab |
|---|---|
| **Kolom identitas ikut dihitung** | `CustomerID` hanya nomor urut |
| **Fitur redundan** | Dua kolom hampir identik membuat satu aspek dihitung dua kali |
| **Terlalu banyak fitur** | Pada banyak dimensi, jarak antar titik cenderung makin mirip, sehingga sulit dibedakan (dikenal sebagai *curse of dimensionality*) |
| **Fitur yang tidak relevan** | Menambah "bising" pada jarak |

## Detailed Explanation

### Feature selection: tiga pertanyaan

1. **Apakah kolom ini fitur sungguhan?** `CustomerID` bukan. Buang.
2. **Apakah ia bermakna untuk tujuan kita?** Jika tujuannya mengelompokkan pelanggan menurut perilaku belanja, `Annual Income (k$)` dan `Spending Score (1-100)` jelas relevan. `Age` mungkin. `Gender` perlu dipertimbangkan.
3. **Apakah ia redundan?** Korelasi tinggi (misalnya \(\lvert r \rvert \ge 0{,}8\)) antar dua kolom adalah tanda. Angka 0,8 hanya pegangan awal, bukan aturan baku.

### Feature engineering: membuat fitur baru

Contoh yang umum:

- **Rasio**: pembagian dua kolom (pengeluaran per pendapatan).
- **Selisih atau jumlah**: gabungan dua kolom.
- **Pengelompokan**: usia menjadi kelompok (Bab 9).
- **Fitur turunan tanggal**: bulan, hari dalam minggu.

!!! warning "Fitur baru tidak otomatis lebih baik"
    Setiap fitur baru perlu **dinilai**: apakah sebarannya wajar? Apakah ia hanya mengulang fitur lain? Kita akan membuat satu fitur baru dan menilainya secara jujur.

## Mathematical Foundation

Bab ini tidak memerlukan rumus baru. Korelasi mengacu ke koefisien Pearson di Bab 3. Fitur rasio yang kita buat:

$$
\text{Spend\_Income\_Ratio} = \frac{\text{Spending Score}}{\text{Annual Income}}
$$

## Python Implementation

Kita kerjakan dalam enam langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/11_feature_selection_engineering.py`, dan versi notebook-nya di `notebooks/level-2/11-feature-selection-and-feature-engineering.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/11_feature_selection_engineering.py:setup"
```

**Penjelasan:**

- Kita memanggil pandas dan membaca data ke `df`.
- Dua baris `pd.set_option` hanya mengatur tampilan supaya tabel lebar tidak terpotong.

### Langkah 2 — Membuang kolom yang bukan fitur

```python
--8<-- "level-2/11_feature_selection_engineering.py:drop_id"
```

**Penjelasan:**

- `df.columns.tolist()` menampilkan nama semua kolom sebagai daftar.
- `df.drop(columns=["CustomerID"])` membuat tabel baru **tanpa** kolom `CustomerID`. Tabel `df` yang asli tidak berubah.
- `CustomerID` dibuang karena hanya nomor urut (Bab 2). Kalau ikut dihitung, ia akan memengaruhi jarak tanpa makna apa pun.

### Langkah 3 — Mencari fitur yang redundan

```python
--8<-- "level-2/11_feature_selection_engineering.py:redundancy"
```

**Penjelasan:**

- `angka` adalah daftar tiga kolom angka. `df[angka].corr()` menghitung korelasi tiap pasangan.
- Loop bersarang `for i, a in enumerate(angka)` lalu `for b in angka[i + 1:]` memeriksa **setiap pasangan sekali saja**. `enumerate` memberi nomor urut `i`, dan `angka[i + 1:]` berarti "semua kolom setelah kolom ke-`i`".
- `abs(korelasi.loc[a, b]) >= 0.8` memeriksa apakah korelasinya kuat. `abs` mengambil nilai mutlak, karena korelasi −0,9 sama kuatnya dengan +0,9.
- Pasangan yang kuat dimasukkan ke daftar `pasangan_kuat`. Jika daftarnya kosong, tidak ada pasangan redundan.

### Langkah 4 — Membuat fitur baru

```python
--8<-- "level-2/11_feature_selection_engineering.py:engineer"
```

**Penjelasan:**

- `df_fitur.copy()` membuat salinan agar tabel sebelumnya aman.
- `df_baru["Spend_Income_Ratio"] = ... / ...` membuat **kolom baru**: skor belanja dibagi pendapatan. Ide-nya: seberapa besar belanja pelanggan relatif terhadap kemampuannya.
- Tanda kurung `( ... )` pada rumus yang panjang hanya agar kodenya bisa dipecah ke dua baris.

### Langkah 5 — Menilai fitur baru

```python
--8<-- "level-2/11_feature_selection_engineering.py:judge"
```

**Penjelasan:**

- `describe()` meringkas fitur baru: nilai terkecil, terbesar, rata-rata, dan kuartil.
- `skew()` mengukur kemiringan sebaran (Bab 3).
- `corr().loc["Spend_Income_Ratio"]` mengambil **satu baris** dari matriks korelasi: korelasi fitur baru dengan tiga fitur asalnya.
- Tujuannya menilai: apakah sebarannya wajar, dan apakah ia hanya menyalin fitur lain?

### Langkah 6 — Menyusun kandidat himpunan fitur

```python
--8<-- "level-2/11_feature_selection_engineering.py:sets"
```

**Penjelasan:**

- `X_dua`, `X_tiga`, dan `X_empat` adalah tiga **kandidat himpunan fitur** yang berbeda.
- `X_empat` memakai `pd.get_dummies` (Bab 9) untuk mengubah `Gender` menjadi dua kolom 0/1.
- Loop terakhir mencetak nama dan bentuk tiap himpunan. `f"{nama:18s}"` menata teks agar rata kiri selebar 18 karakter, supaya hasilnya rapi.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `df.drop(columns=[...])` | Membuang kolom |
| `df["baru"] = df["a"] / df["b"]` | Membuat kolom baru dari rumus |
| `enumerate(daftar)` | Mengulang sambil mencatat nomor urut |
| `daftar[i + 1:]` | Semua elemen setelah posisi `i` |
| `korelasi.loc[a, b]` | Nilai korelasi pasangan `a` dan `b` |
| `kolom.describe()` | Ringkasan satu kolom |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/11_feature_selection_engineering.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/11-feature-selection-and-feature-engineering.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, Python 3.14.7):

```text
--8<-- "level-2/outputs/11.txt"
```

**Cara membaca output:**

- **`CustomerID` dibuang**: kolom turun dari lima menjadi empat.
- **Tidak ada fitur redundan**: korelasi terbesar hanya −0,33 (usia dan skor belanja). Daftar `pasangan_kuat` kosong.
- **Fitur baru `Spend_Income_Ratio`**: nilainya dari 0,01 sampai 5,40 dengan median 0,89, tetapi **skewness 2,43** (miring ke kanan dengan kuat). Pelanggan berpendapatan rendah tetapi skor tinggi menghasilkan rasio besar.
- **Korelasi fitur baru**: −0,57 dengan pendapatan dan 0,59 dengan skor belanja. Ia **cukup bergantung** pada dua kolom asalnya.
- **Tiga kandidat himpunan fitur**: 2 fitur (200×2), 3 fitur (200×3), dan 3 fitur + `Gender` (200×5, karena `Gender` menjadi dua kolom).

## Practical Examples

**Menilai fitur rasio.** Dari hasil di atas, `Spend_Income_Ratio`:

- **Sebarannya sangat miring** (skewness 2,43), dengan beberapa nilai ekstrem karena pembaginya (pendapatan) kecil pada pelanggan berpendapatan rendah.
- **Banyak mengulang** informasi dari dua kolom asalnya (korelasi −0,57 dan 0,59).

Kesimpulan yang wajar: **tidak kita pakai** di sini. Fitur baru bukan keharusan. Menolak fitur yang tidak membantu adalah bagian dari pekerjaannya.

**Memilih himpunan fitur.** Ketiga kandidat punya kegunaan masing-masing:

| Himpunan | Kegunaan |
|---|---|
| 2 fitur (`Annual Income`, `Spending Score`) | Mudah divisualisasikan pada grafik dua dimensi. Pola gerombol di Bab 1 dan 4 terlihat pada pasangan ini |
| 3 fitur (+ `Age`) | Lebih lengkap. Usia berhubungan lemah dengan skor belanja (−0,33) |
| 3 fitur + `Gender` | Menambah informasi kategori. Di Bab 4, `Gender` bercampur di semua gerombol, sehingga kontribusinya diragukan |

Untuk Bab 12, kita akan menyusun dataset akhir dengan **tiga fitur angka** (`Age`, `Annual Income (k$)`, `Spending Score (1-100)`). Ini **pilihan didaktis**: ketiganya angka murni, tidak butuh *encoding*, dan semuanya bermakna. Pilihan ini bukan satu-satunya yang benar, dan evaluasi di level berikutnya dapat membuat kita meninjaunya lagi.

!!! tip "Libatkan pengetahuan domain"
    Pada proyek nyata, tanyakan pada pihak yang memahami bisnisnya: fitur apa yang menurut mereka membedakan pelanggan? Pengetahuan itu sering lebih berharga daripada statistik.

## Hands-on Exercises

1. Buat fitur `Income_per_Age` (pendapatan dibagi usia). Bagaimana sebarannya (`skew()`)?
2. Hitung korelasi `Income_per_Age` dengan `Annual Income (k$)`. Apakah redundan?
3. Mengapa `CustomerID` harus dibuang, walaupun bertipe angka?
4. Ubah ambang redundansi pada Langkah 3 dari 0,8 menjadi 0,3. Pasangan mana yang muncul?
5. Mengapa memilih fitur pada clustering lebih sulit dibanding pada supervised learning?

??? question "Jawaban"
    1. `df["Annual Income (k$)"] / df["Age"]`, lalu `.skew()`. Hasil nyata: skewness **0,59**, jauh lebih landai daripada 2,43 pada rasio di bab ini.
    2. Hitung `df["Annual Income (k$)"].corr(rasio_baru)`. Hasil nyata: korelasinya **0,77**, cukup tinggi, sehingga fitur ini banyak mengulang informasi pendapatan. Masih di bawah ambang 0,8, tetapi sudah mendekati.
    3. `CustomerID` hanya nomor urut, bukan ukuran sifat pelanggan. Kalau ikut dihitung, ia memengaruhi jarak tanpa makna.
    4. Hanya pasangan `Age` dan `Spending Score (1-100)` (korelasi −0,33), karena nilai mutlaknya 0,33 ≥ 0,3.
    5. Karena tidak ada label sebagai tolok ukur. Kita tidak bisa mengukur "fitur mana yang membuat prediksi paling tepat", sehingga harus mengandalkan pengetahuan domain, variasi, dan redundansi.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ZeroDivisionError` atau nilai `inf` pada rasio | Pembaginya nol | Periksa pembagi sebelum membagi, atau tambahkan angka kecil pada pembagi |
| `KeyError` pada `df.drop(columns=...)` | Nama kolom salah atau sudah dibuang | Salin nama dari `df.columns` |
| Fitur baru punya `NaN` | Ada `NaN` pada kolom asalnya | Tangani nilai kosong dulu (Bab 5) |
| Terlalu banyak kolom setelah one-hot | Kategori terlalu banyak | Gabungkan kategori jarang, atau pilih fitur lain |
| Ragu fitur mana yang dipilih | Tidak ada label sebagai tolok ukur | Mulai dari pengetahuan domain, uji beberapa himpunan fitur, bandingkan hasilnya di level evaluasi |

## Summary

- *Feature selection* memilih kolom, *feature engineering* membuat kolom baru.
- Pada clustering tidak ada label, jadi pegangannya: pengetahuan domain, variasi, dan redundansi.
- `CustomerID` dibuang. Tidak ada pasangan fitur yang redundan pada data ini (korelasi terbesar −0,33).
- Fitur baru `Spend_Income_Ratio` bersebaran sangat miring (skewness 2,43) dan banyak mengulang kolom asalnya, sehingga tidak dipakai.
- Untuk Bab 12 kita pakai tiga fitur angka: `Age`, `Annual Income (k$)`, `Spending Score (1-100)`.

## References

- Guyon, I., & Elisseeff, A. (2003). *An Introduction to Variable and Feature Selection*. Journal of Machine Learning Research, 3, 1157–1182.
- Zheng, A., & Casari, A. (2018). *Feature Engineering for Machine Learning*. O'Reilly.
- Bellman, R. (1961). *Adaptive Control Processes: A Guided Tour*. Princeton University Press. (asal istilah *curse of dimensionality*)
