# Bab 10 — Feature Scaling

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan mengapa kolom dengan rentang besar bisa mendominasi perhitungan jarak.
- [x] Menerapkan ***Min-Max scaling*** dan ***Standardization*** (z-score), baik dengan rumus maupun dengan scikit-learn.
- [x] Membedakan kapan memakai masing-masing.
- [x] Memeriksa bahwa hasil penskalaan benar.
- [x] Menjelaskan hubungan penskalaan dengan clustering berbasis jarak.

## Introduction

Dari Bab 3, kita tahu rentang tiga kolom kita sangat berbeda: usia 18–70, pendapatan 15–137, skor belanja 1–99. Algoritma seperti K-Means mengukur **jarak** antar pelanggan. Kolom dengan angka besar menyumbang lebih banyak pada jarak, **bukan karena lebih penting, tetapi karena satuannya lebih besar**.

Bayangkan menghitung jarak dengan mencampur meter dan milimeter. Selisih 1 meter dan selisih 1 milimeter dihitung sebagai "1", padahal 1.000 kali berbeda. ***Feature scaling*** menyamakan "satuan" semua kolom agar adil.

## Fundamental Concepts

| Teknik | Hasil | Cocok untuk |
|---|---|---|
| **Min-Max scaling** | Semua nilai masuk rentang **0 sampai 1** | Saat ingin rentang tetap dan terbatas |
| **Standardization** (z-score) | Rata-rata **0**, simpangan baku **1** | Pilihan umum untuk clustering berbasis jarak |
| **Robust scaling** | Memakai median dan IQR | Saat ada banyak outlier. (Hanya disebut di sini, tidak dipraktikkan) |

### Mengapa penting untuk clustering

Jarak Euclidean antara dua titik \(a\) dan \(b\) dengan tiga fitur:

$$
d(a, b) = \sqrt{(a_1 - b_1)^2 + (a_2 - b_2)^2 + (a_3 - b_3)^2}
$$

Selisih yang besar (karena satuannya besar) **membesarkan kuadratnya**, sehingga fitur itu menguasai \(d\).

## Detailed Explanation

### Min-Max: menekan ke rentang 0–1

Nilai terkecil menjadi 0, terbesar menjadi 1, dan nilai lain berada di antaranya secara proporsional.

- **Kelebihan:** hasilnya mudah dibayangkan, dan rentangnya pasti.
- **Kekurangan:** sangat dipengaruhi **outlier**. Satu nilai ekstrem menentukan batas atas dan menekan semua nilai lain mendekati 0.

### Standardization: berpusat di 0

Nilai dinyatakan sebagai **berapa simpangan baku dari rata-rata**. Nilai 0 berarti tepat di rata-rata, +1 berarti satu simpangan baku di atas.

- **Kelebihan:** tidak membatasi rentang, dan lebih tahan pada outlier dibanding Min-Max.
- **Kekurangan:** nilainya tidak berada di rentang tetap.

### Mana yang dipakai?

Tidak ada jawaban tunggal. Untuk clustering berbasis jarak seperti K-Means, **standardization** adalah titik awal yang umum. Min-Max juga wajar. Yang penting: **semua kolom diskalakan dengan cara yang sama**, dan kamu tahu alasannya.

!!! tip "Kolom hasil one-hot"
    Kolom 0/1 hasil *one-hot encoding* (Bab 9) sudah berada di rentang 0–1. Apakah perlu diskalakan lagi tergantung strategi. Dibahas saat menyusun dataset final (Bab 12).

## Mathematical Foundation

**Min-Max scaling:**

$$
x' = \frac{x - x_{\min}}{x_{\max} - x_{\min}}
$$

**Standardization (z-score):**

$$
z = \frac{x - \mu}{\sigma}
$$

dengan \(\mu\) rata-rata dan \(\sigma\) simpangan baku kolom.

!!! note "Dua versi simpangan baku"
    Scikit-learn (`StandardScaler`) memakai pembagi \(n\) (populasi), sedangkan `df.std()` pandas memakai \(n-1\) (sampel). Itu sebabnya, pada hitungan manual kita menulis `std(ddof=0)` supaya sama dengan scikit-learn. Selisihnya sangat kecil untuk data sebesar ini.

## Python Implementation

Kita kerjakan dalam enam langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/10_feature_scaling.py`, dan versi notebook-nya di `notebooks/level-2/10-feature-scaling.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/10_feature_scaling.py:setup"
```

**Penjelasan:**

- Kita memanggil pandas dan matplotlib, lalu membaca data ke `df`.
- `pd.set_option("display.width", 120)` mengatur lebar baris cetakan tabel menjadi 120 karakter, supaya tabel pandas tidak dipotong dan dilipat ke baris berikutnya di terminal.
- `pd.set_option("display.max_columns", None)` menampilkan **semua** kolom. Tanpa ini, pandas menyingkat tabel yang kolomnya banyak dengan `...`. Kedua pengaturan hanya memengaruhi tampilan, bukan data.
- `fitur` adalah tiga kolom yang akan diskalakan. `CustomerID` tidak ikut karena hanya nomor urut.
- `X = df[fitur]` adalah tabel yang berisi **hanya tiga kolom itu**. Mulai sekarang, kita bekerja dengan `X`.

### Langkah 2 — Masalah: rentang dan varians berbeda

```python
--8<-- "level-2/10_feature_scaling.py:raw"
```

```text title="Output"
--8<-- "level-2/outputs/10/raw.txt"
```

**Penjelasan:**

- `X.agg(["min", "max"])` menampilkan nilai terkecil dan terbesar tiap kolom.
- `X.var()` menghitung **varians** (kuadrat simpangan baku). Varians mengukur seberapa menyebar sebuah kolom, dan sangat menentukan sumbangan kolom itu pada jarak antar titik.
- `varians / varians.sum() * 100` menghitung **porsi** tiap kolom dari total varians, dalam persen.
- Kalau porsi tiap kolom jauh berbeda, jarak akan didominasi kolom dengan porsi terbesar.

**Cara membaca output:**

- **Rentang.** `Age` hanya bergerak dari 18 sampai 70 (selisih 52). `Annual Income (k$)` dari 15 sampai 137 (selisih 122), dan `Spending Score (1-100)` dari 1 sampai 99 (selisih 98). Satuan dan rentang ketiganya memang berbeda.
- **Varians.** `Age` hanya 195,1, sedangkan `Annual Income (k$)` 689,8 dan `Spending Score (1-100)` 666,9. Varians `Age` kira-kira sepertiga dari dua kolom lainnya.
- **Porsi varians.** Dari total varians, `Age` hanya menyumbang 12,6%, sedangkan `Annual Income (k$)` 44,5% dan `Spending Score (1-100)` 43,0%. Ketiga angka ini berjumlah 100%.
- **Artinya untuk clustering.** Pada skala asli, jarak antar pelanggan hampir seluruhnya (sekitar 87%) ditentukan oleh pendapatan dan skor belanja. `Age` nyaris tidak berpengaruh, padahal kita belum memutuskan bahwa usia kurang penting. Ketimpangan inilah yang ingin diperbaiki oleh *feature scaling* di langkah-langkah berikutnya.
- Pada data ini, tidak ada satu kolom yang mendominasi sendirian. Yang tertinggal jauh adalah `Age`. Pada data lain dengan satuan yang lebih ekstrem (misalnya gaji dalam rupiah dengan usia dalam tahun), satu kolom bisa menguasai hampir seluruh jarak.
- `dtype: float64` di akhir tiap deret hanya menunjukkan tipe angka hasil hitungan, bukan bagian dari hasil.

??? question "Belum paham rentang, varians, dan porsi varians? Ikuti contoh sederhana ini"

    Bayangkan kita punya dua kolom angka untuk tiga pelanggan:

    | Pelanggan | Kolom A | Kolom B |
    |---|---|---|
    | 1 | 20 | 20 |
    | 2 | 30 | 60 |
    | 3 | 40 | 100 |

    **1. Rentang: "dari berapa sampai berapa?"**

    Rentang hanya melihat angka terkecil dan terbesar, lalu mengurangkannya.

    - Kolom A: dari 20 sampai 40, selisihnya \( 40 - 20 = 20 \).
    - Kolom B: dari 20 sampai 100, selisihnya \( 100 - 20 = 80 \).

    Kolom B "lebih lebar" daripada kolom A. Baris `min` dan `max` pada output Langkah 2 adalah hal yang sama.

    **2. Varians: "seberapa berserakan angkanya?"**

    Varians adalah satu angka yang menggambarkan **seberapa jauh angka-angka menyebar dari titik tengahnya**.

    - Kalau angkanya **rapat** (misalnya 29, 30, 31), variansnya **kecil**.
    - Kalau angkanya **berserakan** (misalnya 0, 30, 60), variansnya **besar**.

    Pada contoh kita, komputer menghitung varians kolom A = **100** dan kolom B = **1600**. Anda tidak perlu menghitungnya sendiri, cukup ingat artinya: *makin besar angkanya, makin berserakan datanya*.

    **3. Porsi varians: "siapa yang paling berpengaruh?"**

    Bayangkan varians sebagai "suara" tiap kolom saat menentukan siapa mirip dengan siapa. Porsi varians adalah **persentase suara** tiap kolom dari seluruh suara.

    Total suara pada contoh: \( 100 + 1600 = 1700 \).

    - Kolom A: \( 100 / 1700 \approx 6\% \)
    - Kolom B: \( 1600 / 1700 \approx 94\% \)

    Artinya kolom B menguasai hampir seluruh suara, sedangkan kolom A nyaris tidak didengar. Kalau kita memakai kedua kolom ini untuk mengelompokkan pelanggan, hasilnya hampir hanya ditentukan kolom B.

    **Kaitannya dengan output di atas**

    Pada data Mall Customers, `Age` hanya mendapat "suara" 12,6%, sedangkan pendapatan dan skor belanja masing-masing sekitar 44% dan 43%. Jadi usia kurang didengar, bukan karena tidak penting, tetapi karena angkanya kebetulan lebih sempit. *Feature scaling* dipakai supaya semua kolom mendapat suara yang lebih adil.

### Langkah 3 — Min-Max scaling

```python
--8<-- "level-2/10_feature_scaling.py:minmax"
```

```text title="Output"
--8<-- "level-2/outputs/10/minmax.txt"
```

**Penjelasan:**

- `(X - X.min()) / (X.max() - X.min())` adalah rumus Min-Max, diterapkan pada semua kolom sekaligus.
- `X.min()` menghasilkan nilai terkecil **per kolom**, jadi pandas otomatis mengurangi tiap kolom dengan nilai minimumnya sendiri.
- `head().round(3)` menampilkan 5 baris pertama dengan tiga angka di belakang koma.
- `agg(["min", "max"])` membuktikan bahwa setiap kolom sekarang berada tepat di antara 0 dan 1.

**Cara membaca output:**

- **Tabel 5 baris pertama.** Bentuknya sama dengan tabel asli, tetapi semua angka kini berada di antara 0 dan 1. Pelanggan pertama punya `Age` 19, `Annual Income (k$)` 15, dan `Spending Score (1-100)` 39. Kita bisa mencocokkannya dengan rumus Min-Max menggunakan min dan max dari Langkah 2:
    - `Age`: \( (19 - 18) / (70 - 18) = 1/52 \approx 0{,}019 \)
    - `Annual Income (k$)`: \( (15 - 15) / (137 - 15) = 0 \), jadi 0,000
    - `Spending Score (1-100)`: \( (39 - 1) / (99 - 1) = 38/98 \approx 0{,}388 \)
- **Nilai 0,000 pada pendapatan.** Pelanggan 1 dan 2 punya pendapatan 15, yaitu yang terkecil di seluruh data, sehingga hasilnya tepat 0. Pelanggan 3 dan 4 punya pendapatan 16, sehingga hasilnya \( 1/122 \approx 0{,}008 \), dan pelanggan 5 dengan pendapatan 17 menjadi \( 2/122 \approx 0{,}016 \).
- **Urutan tetap terjaga.** Pelanggan 2 punya skor belanja 81 (hasil 0,816), jauh lebih tinggi daripada pelanggan 3 dengan skor 6 (hasil 0,051). Min-Max hanya menggeser dan meregangkan skala, sehingga urutan dan perbandingan relatif antar pelanggan tidak berubah.
- **Tabel min dan max.** Semua kolom kini bernilai min 0,0 dan max 1,0. Rentang `Age` (52), pendapatan (122), dan skor belanja (98) yang tadinya berbeda sekarang sama-sama 1, sehingga ketiganya punya skala yang sebanding dalam menghitung jarak.
- **Yang belum selesai.** Rentang sudah sama, tetapi varians belum tentu sama. Kolom yang sebagian besar datanya mengumpul di satu sisi tetap punya sebaran yang lebih sempit. Hal ini diperiksa di Langkah 6.

### Langkah 4 — Standardization

```python
--8<-- "level-2/10_feature_scaling.py:standard"
```

```text title="Output"
--8<-- "level-2/outputs/10/standard.txt"
```

**Penjelasan:**

- `(X - X.mean()) / X.std(ddof=0)` adalah rumus z-score. `ddof=0` memakai pembagi \(n\), sama dengan scikit-learn.

    **Bagian pertama: `X - X.mean()` dan `/ X.std(...)`.** Rumus ini sama dengan \( z = (x - \mu)/\sigma \) di bagian Mathematical Foundation. Ada dua langkah:

    1. **Kurangi dengan rata-rata** (`X - X.mean()`). Ini menggeser data sehingga titik tengahnya menjadi 0. Nilai di atas rata-rata menjadi positif, dan nilai di bawah rata-rata menjadi negatif.
    2. **Bagi dengan simpangan baku** (`/ X.std(...)`). Simpangan baku adalah ukuran "seberapa lebar sebaran" data (akar dari varians pada Langkah 2). Pembagian ini mengubah satuan asli (tahun, k\$, skor) menjadi satuan baru: **berapa simpangan baku nilai ini dari rata-rata**.

    Jadi z-score `-1,425` berarti "1,425 simpangan baku di bawah rata-rata", dan z-score `1,196` berarti "1,196 simpangan baku di atas rata-rata". Karena semua kolom kini memakai satuan yang sama, ketiganya bisa dibandingkan secara adil.

    **Contoh dari data kita (`Age` pelanggan pertama).** Usianya 19, rata-rata `Age` 38,85, dan simpangan baku (pembagi \(n\)) ≈ 13,934:

    $$
    z = \frac{19 - 38{,}85}{13{,}934} \approx -1{,}425
    $$

    Hasilnya sama dengan baris pertama kolom `Age` pada output.

    **Bagian kedua: apa itu `ddof=0`?** Ada dua cara menghitung simpangan baku yang sedikit berbeda. Bedanya hanya pada **angka pembagi** saat menghitung varians (setelah selisih tiap nilai dikuadratkan dan dijumlahkan):

    | Pengaturan | Pembagi | Nama | Dipakai oleh |
    |---|---|---|---|
    | `ddof=0` | \(n\) (jumlah data) | simpangan baku populasi | `StandardScaler` scikit-learn |
    | `ddof=1` | \(n-1\) | simpangan baku sampel | `.std()` pandas (bawaan) |

    `ddof` singkatan dari *delta degrees of freedom*, yaitu "berapa yang dikurangkan dari \(n\) pada pembagi". Pada `ddof=0` tidak ada yang dikurangkan, pada `ddof=1` dikurangi 1.

    **Contoh kecil.** Ambil tiga angka: 10, 20, 30. Rata-ratanya 20, selisihnya \( -10, 0, 10 \), kuadratnya \( 100, 0, 100 \), jumlahnya 200.

    | | Pembagi | Varians | Simpangan baku | z-score untuk angka 10 |
    |---|---|---|---|---|
    | `ddof=0` | \(3\) | \(200/3 \approx 66{,}7\) | \(\approx 8{,}165\) | \(\approx -1{,}225\) |
    | `ddof=1` | \(2\) | \(200/2 = 100\) | \(10\) | \(-1\) |

    Pada 3 data, bedanya terlihat jelas. Pada data kita \(n = 200\), pembaginya 200 lawan 199, sehingga bedanya sangat kecil: simpangan baku `Age` 13,934 (`ddof=0`) lawan 13,969 (`ddof=1`), dan z-score pelanggan pertama -1,425 lawan -1,421.

    **Mengapa kita memilih `ddof=0`?** Karena kita ingin hasil hitungan manual **persis sama** dengan `StandardScaler`. Itu dibuktikan di Langkah 5. Jika Anda memakai `.std()` tanpa `ddof=0`, angkanya sedikit berbeda dan `StandardScaler` tidak akan cocok dengan hitungan manual Anda.
- Kita memeriksa **rata-rata** dan **simpangan baku** hasilnya. Rata-ratanya hampir 0 (`-0.000` karena pembulatan, bukan negatif sungguhan), dan simpangan baku 1,003.
- Angka 1,003, bukan tepat 1, muncul karena `agg(["std"])` memakai pembagi \(n-1\), sedangkan kita menskalakan dengan pembagi \(n\). Itu hanya beda definisi, bukan kesalahan.

### Langkah 5 — Hasil yang sama dengan scikit-learn

```python
--8<-- "level-2/10_feature_scaling.py:sklearn"
```

```text title="Output"
--8<-- "level-2/outputs/10/sklearn.txt"
```

**Penjelasan:**

- `MinMaxScaler()` dan `StandardScaler()` adalah alat siap pakai dari scikit-learn untuk dua rumus tadi.
- `fit_transform(X)` melakukan dua hal sekaligus: **belajar** parameter (min/max atau mean/std) lalu **menerapkannya**.
- Hasilnya berupa larik NumPy, bukan tabel pandas. Karena itu kita bandingkan dengan `.to_numpy()`.
- `abs(a - b).max() < 1e-9` memeriksa bahwa selisih terbesarnya **hampir nol** (lebih kecil dari satu per miliar). Jika `True`, hitungan manual kita sama dengan scikit-learn.

### Langkah 6 — Porsi varians setelah penskalaan, dan grafiknya

```python
--8<-- "level-2/10_feature_scaling.py:after"
```

```text title="Output"
--8<-- "level-2/outputs/10/after.txt"
```

**Penjelasan:**

- Kita ulangi perhitungan porsi varians pada data yang sudah diskalakan, untuk kedua metode.
- Loop `for nama, data in [...]` mengulang pekerjaan yang sama untuk dua tabel.
- `print()` kosong hanya membuat baris kosong.

```python
--8<-- "level-2/10_feature_scaling.py:plot"
```

![Scatter plot usia vs pendapatan, sebelum dan sesudah standardization](../assets/level-2/10-scaling-scatter.png)

**Penjelasan:**

- Dua *scatter plot* berdampingan: usia vs pendapatan pada skala asli (kiri) dan setelah *standardization* (kanan).
- `set_aspect("equal")` membuat satu satuan di sumbu x sama panjang dengan satu satuan di sumbu y, sehingga kita melihat jarak yang **sesungguhnya** dihitung algoritma.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `pd.set_option(nama, nilai)` | Mengatur tampilan pandas (lebar cetak, jumlah kolom) tanpa mengubah data |
| `X.var()` | Varians tiap kolom |
| `X.std(ddof=0)` | Simpangan baku dengan pembagi \(n\) |
| `MinMaxScaler().fit_transform(X)` | Min-Max scaling dengan scikit-learn |
| `StandardScaler().fit_transform(X)` | Standardization dengan scikit-learn |
| `.to_numpy()` | Mengubah tabel pandas menjadi larik NumPy |
| `ax.set_aspect("equal")` | Skala sumbu x dan y sama |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/10_feature_scaling.py
```

Skrip menyimpan satu gambar di `docs/assets/level-2/`. Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/10-feature-scaling.ipynb
```

## Expected Output

Semua output berasal dari eksekusi nyata skrip (pandas 3.1.1, scikit-learn 1.9.1, Python 3.14.7). Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).


![Scatter plot usia vs pendapatan, sebelum dan sesudah standardization](../assets/level-2/10-scaling-scatter.png)

**Cara membaca output:**

- **Sebelum penskalaan**, porsi varians: `Age` 12,6%, `Annual Income (k$)` 44,5%, `Spending Score (1-100)` 43,0%. Usia hanya berperan seperempat dari pendapatan atau skor belanja dalam jarak.
- **Min-Max**: semua kolom tepat 0 sampai 1. Porsi varians menjadi 38,4%, 24,7%, dan 36,9%.
- **Standardization**: rata-rata 0 dan porsi varians **33,3% untuk ketiga kolom**: perlakuannya adil.
- **Scikit-learn** memberi hasil yang sama dengan hitungan manual (`True` untuk keduanya).
- **Grafik kiri** (skala asli, sumbu sama panjang): titik-titik tersebar sangat lebar secara horizontal, tetapi tampak "gepeng" secara vertikal. Pada grafik kanan setelah standardization, sebarannya setara di kedua arah.

## Practical Examples

**Mengapa Min-Max tidak menghasilkan porsi yang sama?** Porsi varians setelah Min-Max (38,4%, 24,7%, 36,9%) tidak merata karena Min-Max hanya menyamakan **rentang**, bukan **sebaran**. Rentang pendapatan (15–137) diperlebar oleh nilai-nilai terbesar di ujung atas, sedangkan sebagian besar nilainya tidak menyebar selebar itu. Akibatnya variansnya setelah di-Min-Max menjadi yang terkecil. Standardization menyamakan sebaran, sehingga porsinya persis sama.

**Pilihan untuk dataset ini.** Karena kita ingin ketiga fitur berperan setara dan data hanya punya 2 titik yang melewati batas outlier IQR (Bab 7), *standardization* adalah pilihan yang wajar dan akan dipakai di Bab 12.

**Skala dan interpretasi.** Setelah penskalaan, nilai tidak lagi dalam satuan asli. Untuk menjelaskan hasil clustering kepada orang lain ("kelompok ini berpendapatan rata-rata berapa?"), kita **kembalikan** ke satuan asli, misalnya dengan menghitung statistik pada data asli per kelompok.

!!! warning "Skala memengaruhi hasil clustering"
    Hasil K-Means pada data yang diskalakan dan yang tidak diskalakan bisa berbeda. Itu bukan kesalahan, melainkan akibat dari definisi jarak yang berbeda. Karena itu, keputusan penskalaan harus **disadari dan dicatat**.

## Hands-on Exercises

1. Terapkan `RobustScaler` dari `sklearn.preprocessing` pada `X`. Apa bedanya dengan `StandardScaler`? (petunjuk: baca dokumentasinya)
2. Tambahkan kolom `Gender_Male` (0/1) ke `X`, lalu hitung porsi variansnya sebelum penskalaan. Berapa persen?
3. Mengapa Min-Max sensitif terhadap outlier?
4. Setelah *standardization*, berapa nilai rata-rata tiap kolom? Mengapa tampil `-0.000`?
5. Hitung z-score untuk usia 40 dengan rata-rata 38,85 dan simpangan baku 13,97 (dari Bab 3).

??? question "Jawaban"
    1. `RobustScaler` memakai **median** dan **IQR**, bukan mean dan simpangan baku, sehingga lebih tahan terhadap outlier.
    2. Jalankan `X.assign(Gender_Male=(df["Gender"] == "Male").astype(int)).var()` lalu hitung porsinya. Karena kolom 0/1 hanya punya selisih maksimum 1, variansnya sangat kecil dibanding tiga kolom lain, sehingga porsinya mendekati nol pada skala asli.
    3. Karena Min-Max menentukan batas dari nilai **minimum dan maksimum**. Satu nilai ekstrem menggeser batas itu, dan semua nilai lain tertekan ke bagian kecil dari rentang 0–1.
    4. Rata-ratanya hampir 0 (jauh lebih kecil dari 0,001). Tanda minus muncul karena sisa pembulatan angka desimal komputer, bukan karena nilainya benar-benar negatif.
    5. \(z = (40 - 38{,}85) / 13{,}97 \approx 0{,}08\). Usia 40 hanya sedikit di atas rata-rata.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| Hasil scikit-learn berupa larik tanpa nama kolom | Scikit-learn mengembalikan NumPy | Bungkus kembali: `pd.DataFrame(hasil, columns=fitur)` |
| `ValueError: could not convert string to float` | Ada kolom teks di data yang diskalakan | Pilih hanya kolom angka, atau *encode* dulu (Bab 9) |
| `ValueError: Input contains NaN` | Masih ada nilai kosong | Tangani dulu (Bab 5) |
| Kolom hasil semuanya `NaN` | Kolom konstan, sehingga pembagi 0 | Buang kolom yang nilainya sama semua |
| Hitungan manual sedikit berbeda dari scikit-learn | Beda pembagi (\(n\) vs \(n-1\)) | Pakai `std(ddof=0)` |

## Summary

- Algoritma berbasis jarak sensitif terhadap satuan. Kolom dengan rentang atau sebaran besar bisa mendominasi.
- **Min-Max** menekan nilai ke 0–1. **Standardization** membuat rata-rata 0 dan simpangan baku 1.
- Pada Mall Customers, sebelum penskalaan porsi varians `Age` hanya 12,6%. Setelah *standardization*, ketiga kolom 33,3%.
- Min-Max sensitif terhadap outlier. Standardization lebih tahan, dan menjadi pilihan umum untuk clustering.
- Scikit-learn memberi hasil yang sama dengan rumus manual. Catat metode penskalaan yang kamu pakai.

## References

- scikit-learn documentation: [*Preprocessing data*](https://scikit-learn.org/stable/modules/preprocessing.html), termasuk `MinMaxScaler`, `StandardScaler`, dan `RobustScaler`.
- Han, J., Kamber, M., & Pei, J. (2011). *Data Mining: Concepts and Techniques* (3rd ed.), bab tentang normalisasi data. Morgan Kaufmann.
- Jain, A. K. (2010). *Data clustering: 50 years beyond K-means*. Pattern Recognition Letters, 31(8).
