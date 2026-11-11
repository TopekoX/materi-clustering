# Bab 3 — Descriptive Statistics

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menghitung dan menjelaskan ukuran pemusatan: *mean*, *median*, dan modus.
- [x] Menghitung dan menjelaskan ukuran sebaran: rentang, varians, simpangan baku, dan *IQR*.
- [x] Membaca *skewness* (kemiringan) dan korelasi.
- [x] Menghitung statistik per kelompok dengan `groupby`.
- [x] Menjelaskan mengapa statistik deskriptif membantu menyiapkan data clustering.

## Introduction

Statistik deskriptif adalah cara **meringkas ribuan angka menjadi beberapa angka yang mudah dibaca**. Alih-alih melihat 200 nilai usia satu per satu, kita cukup bertanya: "Rata-ratanya berapa? Seberapa menyebar?"

Dalam clustering, ringkasan ini sangat berguna karena ia menjawab pertanyaan seperti:

- Apakah rentang nilai antar kolom berbeda jauh? (penting untuk *feature scaling*, Bab 10)
- Apakah ada nilai yang tampak ekstrem? (penting untuk *outlier*, Bab 7)
- Apakah dua kolom saling berhubungan? (penting untuk memilih fitur, Bab 11)

## Fundamental Concepts

| Kelompok | Ukuran | Pertanyaan yang dijawab |
|---|---|---|
| **Pemusatan** | Mean, median, modus | "Nilai tipikalnya berapa?" |
| **Sebaran** | Rentang, varians, simpangan baku, IQR | "Seberapa menyebar nilainya?" |
| **Bentuk** | Skewness | "Apakah sebarannya miring?" |
| **Hubungan** | Korelasi | "Apakah dua kolom bergerak bersama?" |

**Pemusatan**

- **Mean** (rata-rata): jumlah semua nilai dibagi banyaknya nilai.
- **Median**: nilai tengah setelah data diurutkan. Setengah data ada di bawahnya, setengah di atasnya.
- **Modus**: nilai yang paling sering muncul.

**Sebaran**

- **Rentang**: nilai terbesar dikurangi nilai terkecil.
- **Simpangan baku** (*standard deviation*): seberapa jauh, rata-rata, nilai menyimpang dari mean.
- **Kuartil**: titik yang membagi data terurut menjadi empat bagian sama banyak. `Q1` = 25%, `Q2` = 50% (median), `Q3` = 75%.
- **IQR** (*interquartile range*): `Q3 − Q1`, lebar "bagian tengah" data.

## Detailed Explanation

### Mean atau median?

Keduanya mengukur "nilai tipikal", tetapi bereaksi berbeda terhadap nilai ekstrem.

!!! tip "Contoh sederhana"
    Gaji lima orang: 5, 5, 6, 6, 100 (juta). **Mean = 24,4.** **Median = 6.** Satu gaji yang sangat besar menarik mean ke atas, sedangkan median hampir tidak terpengaruh. Jadi kalau mean dan median **berjauhan**, curigai ada nilai ekstrem atau sebaran yang miring.

### Simpangan baku: ukuran "seberapa menyebar"

Dua kelompok bisa punya mean sama tetapi sebaran berbeda. Nilai 49, 50, 51 dan nilai 0, 50, 100 sama-sama bermean 50. Namun yang kedua jauh lebih menyebar, dan simpangan bakunya jauh lebih besar.

### Skewness: apakah sebarannya miring?

- **Skewness mendekati 0**: sebaran kira-kira simetris.
- **Skewness positif**: ekor panjang di sisi **kanan** (ada beberapa nilai besar).
- **Skewness negatif**: ekor panjang di sisi **kiri**.

### Korelasi: hubungan dua kolom

Koefisien korelasi (Pearson) bernilai antara **−1 dan +1**:

- Mendekati **+1**: kalau satu naik, yang lain cenderung naik.
- Mendekati **−1**: kalau satu naik, yang lain cenderung turun.
- Mendekati **0**: tidak ada hubungan **garis lurus**.

!!! warning "Korelasi nol bukan berarti tidak ada pola"
    Korelasi hanya mengukur hubungan garis lurus. Dua kolom bisa berkorelasi mendekati 0 tetapi tetap membentuk pola yang jelas, misalnya gerombol-gerombol. Kita akan melihat ini langsung pada data Mall Customers di bawah.

## Mathematical Foundation

Misalkan ada \(n\) nilai \(x_1, x_2, \dots, x_n\).

**Mean:**

$$
\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i
$$

**Varians sampel** dan **simpangan baku sampel**:

$$
s^2 = \frac{1}{n-1} \sum_{i=1}^{n} (x_i - \bar{x})^2
\qquad
s = \sqrt{s^2}
$$

Pembaginya \(n-1\), bukan \(n\), karena kita menghitung dari **sampel**. Pandas memakai \(n-1\) secara bawaan.

**IQR:**

$$
\text{IQR} = Q_3 - Q_1
$$

**Koefisien korelasi Pearson** antara \(x\) dan \(y\):

$$
r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2} \; \sqrt{\sum (y_i - \bar{y})^2}}
$$

## Python Implementation

Kita kerjakan dalam tujuh langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/03_descriptive_statistics.py`, dan versi notebook-nya di `notebooks/level-2/03-descriptive-statistics.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/03_descriptive_statistics.py:setup"
```

**Penjelasan:**

- Kita memanggil pandas dan membaca file CSV menjadi tabel `df`, seperti di bab sebelumnya.
- `fitur` adalah daftar tiga kolom angka yang bermakna. Kita sengaja **tidak memasukkan `CustomerID`**, karena itu hanya nomor urut (Bab 2).
- Dengan daftar ini, kita bisa menulis `df[fitur]` untuk mengambil ketiga kolom sekaligus.

### Langkah 2 — Ukuran pemusatan

```python
--8<-- "level-2/03_descriptive_statistics.py:center"
```

```text title="Output"
--8<-- "level-2/outputs/03/center.txt"
```

**Penjelasan:**

- `.mean()` menghitung rata-rata, `.median()` menghitung nilai tengah. Keduanya dihitung untuk setiap kolom sekaligus.
- `.mode()` menghitung modus. Hasilnya berupa daftar, karena bisa ada lebih dari satu nilai yang sama-sama paling sering muncul. `.tolist()` mengubahnya menjadi list biasa.
- `.round(2)` membulatkan hasil ke dua angka di belakang koma.

### Langkah 3 — Ukuran sebaran

```python
--8<-- "level-2/03_descriptive_statistics.py:spread"
```

```text title="Output"
--8<-- "level-2/outputs/03/spread.txt"
```

**Penjelasan:**

- `df[fitur].max() - df[fitur].min()` menghitung **rentang** untuk tiap kolom.
- `.std()` menghitung simpangan baku.
- `.quantile(0.25)` dan `.quantile(0.75)` mencari kuartil pertama (`Q1`) dan ketiga (`Q3`). Angka `0.25` artinya "titik di mana 25% data ada di bawahnya".
- `q3 - q1` adalah **IQR**.

### Langkah 4 — Menghitung dengan tangan

```python
--8<-- "level-2/03_descriptive_statistics.py:manual"
```

```text title="Output"
--8<-- "level-2/outputs/03/manual.txt"
```

**Penjelasan:**

- Langkah ini membuktikan bahwa pandas tidak "sihir". Kita hitung rumus di atas dengan Python biasa.
- `usia = df["Age"].tolist()` mengubah kolom menjadi list, dan `n = len(usia)` menghitung banyak datanya.
- `sum(usia) / n` adalah rumus mean.
- `sum((x - rata_rata) ** 2 for x in usia)` menjumlahkan kuadrat selisih tiap nilai dari mean. Tanda `**` berarti pangkat.
- Dibagi `n - 1`, lalu diakar dengan `** 0.5`, sehingga menjadi simpangan baku.
- Empat baris `print` terakhir membandingkan hasil manual dengan hasil pandas. Keduanya harus sama.

### Langkah 5 — Skewness

```python
--8<-- "level-2/03_descriptive_statistics.py:skew"
```

```text title="Output"
--8<-- "level-2/outputs/03/skew.txt"
```

**Penjelasan:**

- `.skew()` menghitung kemiringan sebaran tiap kolom.
- Nilai di dekat 0 berarti hampir simetris. Nilai positif berarti ekor memanjang ke kanan.

### Langkah 6 — Statistik per kelompok

```python
--8<-- "level-2/03_descriptive_statistics.py:group"
```

```text title="Output"
--8<-- "level-2/outputs/03/group.txt"
```

**Penjelasan:**

- `df.groupby("Gender")` membagi tabel menjadi kelompok berdasarkan isi kolom `Gender`.
- `[fitur].mean()` menghitung rata-rata ketiga kolom **di dalam masing-masing kelompok**.
- `.size()` menghitung jumlah baris per kelompok.
- `groupby` berguna untuk membandingkan kelompok yang sudah kita ketahui sebelum kita mencari kelompok baru lewat clustering.

### Langkah 7 — Korelasi

```python
--8<-- "level-2/03_descriptive_statistics.py:corr"
```

```text title="Output"
--8<-- "level-2/outputs/03/corr.txt"
```

**Penjelasan:**

- `.corr()` menghitung koefisien korelasi untuk **setiap pasangan** kolom, lalu menyusunnya menjadi tabel (matriks).
- Diagonal selalu `1.00`, karena sebuah kolom pasti berkorelasi sempurna dengan dirinya sendiri.
- Tabelnya simetris: korelasi A dengan B sama dengan B dengan A.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Menghasilkan |
|---|---|
| `.mean()`, `.median()`, `.mode()` | Rata-rata, nilai tengah, nilai paling sering |
| `.min()`, `.max()` | Nilai terkecil dan terbesar |
| `.std()` | Simpangan baku sampel |
| `.quantile(0.25)` | Kuartil pertama (`0.75` untuk kuartil ketiga) |
| `.skew()` | Kemiringan sebaran |
| `.corr()` | Matriks korelasi Pearson |
| `.groupby("kolom")` | Membagi tabel menjadi kelompok |
| `.size()` | Jumlah baris per kelompok |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/03_descriptive_statistics.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/03-descriptive-statistics.ipynb
```

## Expected Output

Semua output berasal dari eksekusi nyata skrip (pandas 3.1.1, Python 3.14.7). Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).


**Cara membaca output:**

- **Mean dan median hampir sama** pada ketiga kolom (misalnya `Age`: 38,85 vs 36,0). Tidak ada tanda nilai ekstrem yang kuat menarik rata-rata.
- **Rentang berbeda jauh**: `Age` 52, `Annual Income (k$)` 122, `Spending Score (1-100)` 98. Ini alasan *feature scaling* diperlukan (Bab 10).
- **Hasil manual = hasil pandas**: rata-rata `Age` 38,85 dan simpangan baku 13,97 pada keduanya.
- **Skewness kecil**: `Age` 0,49 (sedikit miring ke kanan), `Annual Income (k$)` 0,32, `Spending Score (1-100)` −0,05 (hampir simetris).
- **Per Gender**: rata-rata ketiga kolom hanya berbeda sedikit antara `Female` (112 orang) dan `Male` (88 orang).
- **Korelasi**: `Age` dan `Spending Score (1-100)` −0,33 (hubungan negatif lemah). `Annual Income (k$)` dan `Spending Score (1-100)` hanya 0,01.

## Practical Examples

**Korelasi mendekati nol, tetapi ada pola.** Pada Bab 1 kita melihat *scatter plot* pendapatan vs skor belanja yang tampak membentuk beberapa gerombol. Namun korelasi keduanya hanya **0,01**. Artinya: tidak ada hubungan garis lurus, tetapi **itu tidak berarti tidak ada struktur**. Inilah salah satu alasan clustering berguna: ia bisa menemukan pola yang tidak tertangkap oleh korelasi. Dan ini juga alasan kita **tidak boleh hanya mengandalkan angka ringkasan**. Selalu lihat grafiknya (Bab 4).

**Memilih kolom yang punya cukup variasi.** Simpangan baku menunjukkan seberapa bervariasi sebuah kolom. Kolom yang hampir tidak bervariasi tidak banyak membantu memisahkan pelanggan. Di dataset ini ketiganya cukup bervariasi.

**Membandingkan kelompok yang sudah diketahui.** Hasil `groupby("Gender")` menunjukkan `Female` dan `Male` hampir sama dalam rata-rata. Artinya, `Gender` kemungkinan bukan pembeda yang kuat antar pelanggan. Ini baru dugaan awal, bukan kesimpulan.

## Hands-on Exercises

1. Hitung median `Annual Income (k$)` untuk `Female` dan `Male` dengan `groupby`.
2. Hitung `IQR` kolom `Age` dengan tangan dari `Q1` dan `Q3` di output `describe()` Bab 1. Apakah cocok dengan hasil di output bab ini?
3. Mana yang lebih menyebar: `Age` atau `Annual Income (k$)`? Mengapa membandingkan simpangan baku langsung kurang adil?
4. Mean `Spending Score (1-100)` adalah 50,20 dan mediannya 50,0. Apa yang bisa kamu simpulkan?
5. Mengapa korelasi `Annual Income (k$)` dan `Spending Score (1-100)` yang hanya 0,01 tidak membuktikan bahwa kedua kolom tidak berhubungan sama sekali?

??? question "Jawaban"
    1. `df.groupby("Gender")["Annual Income (k$)"].median()`. Jalankan sendiri dan catat hasilnya.
    2. `Q3 − Q1 = 49,00 − 28,75 = 20,25`. Cocok dengan output (`Age` 20,25).
    3. Simpangan baku `Annual Income (k$)` (26,26) lebih besar dari `Age` (13,97). Namun kedua kolom punya **satuan dan rentang berbeda** (tahun vs ribu dolar), jadi perbandingan langsung kurang adil. Itu sebabnya nanti kita menyamakan skala (Bab 10).
    4. Mean dan median hampir sama, dan skewness hanya −0,05. Sebarannya kira-kira simetris, tanpa nilai ekstrem yang menarik rata-rata.
    5. Korelasi Pearson hanya mengukur hubungan **garis lurus**. Hubungan yang berbentuk gerombol atau lengkungan bisa menghasilkan korelasi mendekati 0.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `TypeError` saat `mean()` pada tabel yang ada kolom teks | Kolom `Gender` ikut terhitung | Pilih kolom angka saja: `df[fitur].mean()` atau `numeric_only=True` |
| Simpangan baku manual berbeda dengan pandas | Pembaginya `n`, bukan `n - 1` | Pandas memakai `n - 1` (sampel). Samakan dengan rumus di atas |
| `KeyError: 'Annual Income (k$)'` | Salah ketik nama kolom (spasi, huruf besar, tanda kurung) | Salin nama dari `df.columns` |
| Hasil `.mode()` berupa beberapa nilai | Ada lebih dari satu modus | Wajar. Ambil `.tolist()` untuk melihat semuanya |
| Korelasi tampil `NaN` | Salah satu kolom konstan atau ada nilai kosong | Periksa nilai kosong dan variasi kolom |

## Summary

- Statistik deskriptif **meringkas** data: pemusatan (mean, median, modus), sebaran (rentang, simpangan baku, IQR), bentuk (skewness), dan hubungan (korelasi).
- Mean yang jauh dari median adalah tanda nilai ekstrem atau sebaran miring.
- Pada Mall Customers, rentang tiga kolom sangat berbeda (52, 122, 98), sehingga perlu penyamaan skala.
- Korelasi `Annual Income (k$)` dan `Spending Score (1-100)` hanya 0,01, padahal grafik menunjukkan pola gerombol. **Angka ringkasan tidak cukup, selalu lihat grafik.**

## References

- pandas documentation: [*Computational tools*](https://pandas.pydata.org/docs/user_guide/computation.html) dan [`DataFrame.describe`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html).
- pandas documentation: [*Group by: split-apply-combine*](https://pandas.pydata.org/docs/user_guide/groupby.html).
- Montgomery, D. C., & Runger, G. C. *Applied Statistics and Probability for Engineers*. Wiley.
