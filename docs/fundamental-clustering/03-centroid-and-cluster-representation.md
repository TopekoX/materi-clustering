# Bab 3 — Centroid and Cluster Representation

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan apa itu *centroid* dan mengapa ia dipakai untuk mewakili sebuah kelompok.
- [x] Menghitung centroid data numerik secara manual dan dengan NumPy.
- [x] Menjelaskan perbedaan *centroid* dan *medoid*.
- [x] Menjelaskan mengapa centroid sensitif terhadap *outlier* sedangkan medoid lebih tahan.
- [x] Menjelaskan bagaimana posisi centroid berubah ketika anggota kelompok berubah.
- [x] Memvisualisasikan centroid dengan Matplotlib dan menafsirkannya sebagai profil kelompok.

## Introduction

Di Bab 1 dan 2 kita sudah beberapa kali menyebut "pusat kelompok" (tanda `X` pada grafik). Sekarang kita membahasnya dengan teliti.

Bayangkan sebuah kelompok berisi 81 pelanggan. Kamu tidak mungkin membacakan 81 baris data kepada manajer. Kamu butuh **satu titik yang mewakili** kelompok itu: "pelanggan tipikal di kelompok ini berpendapatan 55 dan bernilai belanja 49". Titik wakil inilah yang dipelajari di bab ini.

Wakil kelompok punya dua kegunaan utama:

1. **Menafsirkan.** Ia meringkas ciri kelompok dalam satu baris angka.
2. **Menentukan keanggotaan.** Banyak algoritma memasukkan titik baru ke kelompok yang wakilnya paling dekat (Bab 2). Level 4 membahasnya mendalam.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Centroid** | Titik **rata-rata** semua anggota kelompok. Belum tentu berimpit dengan data asli |
| **Medoid** | Anggota kelompok yang **paling sentral**: jumlah jaraknya ke anggota lain paling kecil. Selalu merupakan data asli |
| **Representative point** | Istilah umum untuk titik wakil kelompok: bisa centroid, medoid, atau titik lain |
| **Mean** | Rata-rata hitung. Centroid adalah *mean* yang dihitung per fitur |
| **Outlier** | Data yang jauh berbeda dari kebanyakan data lain (Level 2 Bab 7) |

!!! note "Mengapa disebut "pusat massa""
    Bayangkan tiap titik data sebagai kelereng berbobot sama di atas papan tipis. Titik tempat papan seimbang di ujung jari adalah centroid, sama seperti **pusat massa** dalam fisika.

## Detailed Explanation

### Centroid: rata-rata per fitur

Cara mencari centroid sederhana: **rata-ratakan setiap fitur secara terpisah**. Jika tiap titik punya dua fitur (pendapatan dan skor belanja), centroid juga punya dua angka: rata-rata pendapatan dan rata-rata skor belanja.

Contoh: tiga pelanggan dengan (pendapatan, skor) = (2, 3), (4, 4), dan (6, 5). Rata-rata pendapatan: \( (2+4+6)/3 = 4 \). Rata-rata skor: \( (3+4+5)/3 = 4 \). Centroid-nya \( (4, 4) \).

Perhatikan bahwa centroid **boleh jatuh di tempat yang tidak ada datanya**. Kalau data kita (1, 1) dan (3, 3), centroid-nya (2, 2) walau tidak ada pelanggan di sana. Itu wajar: ia adalah titik wakil, bukan anggota.

### Medoid: anggota yang paling sentral

**Medoid** adalah anggota kelompok yang jumlah jaraknya ke semua anggota lain paling kecil. Ia selalu berupa **data nyata**. Ini bermanfaat ketika:

- Rata-rata tidak bermakna (misalnya data kategori: "rata-rata" dari Female dan Male tidak ada artinya).
- Kamu ingin mencontohkan kelompok dengan satu **kasus nyata** ("pelanggan nomor 57 mewakili kelompok ini").
- Data punya *outlier* yang tidak ingin kamu biarkan menarik wakil kelompok.

### Centroid vs medoid

| | Centroid | Medoid |
|---|---|---|
| Cara hitung | Rata-rata tiap fitur | Anggota dengan jumlah jarak terkecil |
| Berupa data asli? | Belum tentu | **Selalu** |
| Tahan outlier? | **Tidak**, tertarik ke outlier | **Ya**, lebih stabil |
| Biaya hitung | Murah | Lebih mahal (butuh semua pasangan jarak) |
| Data kategori | Tidak cocok | Bisa, selama ada ukuran jarak |
| Dipakai oleh | K-Means (Level 4) | K-Medoids (Level 4) |

```mermaid
flowchart TD
    A[Kelompok titik data] --> B{Cara memilih wakil}
    B -->|Rata-rata tiap fitur| C[Centroid<br/>bisa di luar data]
    B -->|Anggota paling sentral| D[Medoid<br/>selalu data asli]
```

### Centroid berpindah ketika anggota berubah

Centroid ditentukan oleh anggotanya. Jika anggota bertambah, berkurang, atau berpindah kelompok, centroid ikut bergeser. Banyak algoritma memanfaatkan ini: **tebak pusat → tentukan anggota → hitung ulang pusat → ulangi.** Pada Python Implementation kita menjalankan **satu putaran** saja agar kamu melihat pergeseran pusatnya. Algoritma lengkapnya (K-Means) dibahas di Level 4.

### Pusat sebagai profil kelompok

Centroid pada data bisa dibaca sebagai **profil**: "pelanggan tipikal kelompok ini". Pada Bab 1 kita menafsirkan rata-rata tiap kelompok sebagai profil, dan ternyata itu persis centroid-nya. Kita membuktikannya dengan kode di bawah.

## Mathematical Foundation

Misalkan kelompok \( C \) berisi \( n \) titik \( \mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_n \), dengan tiap \( \mathbf{x}_i \) berisi \( d \) angka (satu per fitur). **Centroid** \( \mu \) adalah:

$$
\mu = \frac{1}{n} \sum_{i=1}^{n} \mathbf{x}_i
$$

Penjelasan simbol:

- \( n \) adalah jumlah anggota kelompok.
- \( \mathbf{x}_i \) adalah anggota ke-\( i \). Huruf tebal berarti ia berisi **beberapa angka** (satu per fitur).
- \( \sum_{i=1}^{n} \) berarti "jumlahkan dari \( i = 1 \) sampai \( i = n \)". Penjumlahan titik dilakukan **per fitur**.
- \( \frac{1}{n} \) membagi hasil jumlah dengan banyaknya anggota. Hasilnya rata-rata.
- Untuk fitur ke-\( j \), rumusnya menjadi \( \mu_j = \frac{1}{n} \sum_{i=1}^{n} x_{ij} \).

**Medoid** \( \mathbf{m} \) adalah anggota yang meminimalkan jumlah jarak ke semua anggota lain:

$$
\mathbf{m} = \underset{\mathbf{x}_a \in C}{\arg\min} \sum_{b=1}^{n} \lVert \mathbf{x}_a - \mathbf{x}_b \rVert
$$

- \( \arg\min \) berarti "ambil argumen yang menghasilkan nilai terkecil", yaitu **titik** \( \mathbf{x}_a \), bukan nilainya.
- \( \lVert \mathbf{x}_a - \mathbf{x}_b \rVert \) adalah jarak Euclidean (Bab 5). Untuk dua dimensi: \( \sqrt{(x_{a1}-x_{b1})^2 + (x_{a2}-x_{b2})^2} \).

### Contoh hitung manual: centroid

Lima pelanggan: \( P_1 = (2,3) \), \( P_2 = (3,5) \), \( P_3 = (4,4) \), \( P_4 = (3,2) \), \( P_5 = (8,8) \).

1. Jumlah fitur pertama: \( 2 + 3 + 4 + 3 + 8 = 20 \).
2. Jumlah fitur kedua: \( 3 + 5 + 4 + 2 + 8 = 22 \).
3. Bagi dengan \( n = 5 \): \( \mu_1 = 20/5 = 4 \) dan \( \mu_2 = 22/5 = 4{,}4 \).

Centroid-nya \( (4;\ 4{,}4) \). Perhatikan bahwa tidak ada pelanggan di titik itu.

### Contoh hitung manual: medoid

Jumlah jarak sebuah titik ke keempat titik lain. Untuk \( P_3 = (4,4) \):

- Ke \( P_1 \): \( \sqrt{(4-2)^2 + (4-3)^2} = \sqrt{5} \approx 2{,}236 \)
- Ke \( P_2 \): \( \sqrt{(4-3)^2 + (4-5)^2} = \sqrt{2} \approx 1{,}414 \)
- Ke \( P_4 \): \( \sqrt{(4-3)^2 + (4-2)^2} = \sqrt{5} \approx 2{,}236 \)
- Ke \( P_5 \): \( \sqrt{(4-8)^2 + (4-8)^2} = \sqrt{32} \approx 5{,}657 \)

Jumlahnya \( 2{,}236 + 1{,}414 + 2{,}236 + 5{,}657 \approx 11{,}54 \). Dengan cara yang sama, jumlah jarak \( P_1 \) kira-kira 13,70 (\( \sqrt{5} + \sqrt{5} + \sqrt{2} + \sqrt{61} \)). Titik dengan jumlah **terkecil** adalah medoid. Kita lihat hasil lengkapnya di bagian Python.

**Interpretasi.** Centroid (4; 4,4) agak tertarik ke arah \( P_5 = (8,8) \) yang jauh. Medoid adalah salah satu anggota nyata, yang paling "di tengah" dalam arti jarak.

## Python Implementation

Kita kerjakan dalam tujuh langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-3/03_centroid_and_representation.py`, dan versi notebook-nya di `notebooks/level-3/03-centroid-and-cluster-representation.ipynb`.

**Konteks masalah:** kita menghitung centroid dan medoid lima titik, melihat pengaruh outlier, melihat pergeseran pusat, lalu membuktikan bahwa centroid kelompok Mall Customers sama dengan rata-rata anggotanya.

**Input yang diharapkan:** data kecil dibuat di kode. Langkah 6 memakai `data/mall_customers.csv`.

### Langkah 1 — Siapkan data kecil

```python
--8<-- "level-3/03_centroid_and_representation.py:setup"
```

```text title="Output"
--8<-- "level-3/outputs/03/setup.txt"
```

**Penjelasan:**

- `import numpy as np`, `pandas as pd`, dan `matplotlib.pyplot as plt` memanggil tiga pustaka dengan nama singkat. `KMeans` kita pakai di Langkah 6.
- `np.array([[2, 3], [3, 5], ...], dtype=float)` membuat larik dua dimensi: tiap baris satu pelanggan, tiap kolom satu fitur. `dtype=float` membuat angkanya desimal agar hasil rata-rata tidak terpotong.
- `names` adalah daftar nama titik agar output mudah dibaca.
- `pd.DataFrame(points, index=names, columns=[...])` menampilkan larik sebagai tabel berlabel.

### Langkah 2 — Hitung centroid

Setelah data siap di Langkah 1, kita mulai dari cara paling umum untuk mewakili sebuah kelompok: **centroid**, yaitu rata-rata tiap fitur dari semua anggotanya. Kita menghitungnya dulu **dengan tangan** (jumlahkan, lalu bagi dengan banyaknya titik) sebelum memakai jalan pintas `mean`. Tujuannya agar jelas bahwa centroid bukan hasil ajaib dari sebuah fungsi, melainkan rumus rata-rata biasa yang sudah kamu lihat di Mathematical Foundation.

Hasilnya kita bandingkan dengan `points.mean(axis=0)` sebagai **pemeriksaan**. Bila keduanya sama, berarti pemahaman kita atas rumus benar dan kita bisa memakai `mean` dengan tenang di langkah-langkah berikutnya, termasuk pada data Mall Customers.

```python
--8<-- "level-3/03_centroid_and_representation.py:centroid"
```

```text title="Output"
--8<-- "level-3/outputs/03/centroid.txt"
```

**Cara membaca output:**

- `Jumlah per kolom: [20. 22.]` adalah jumlah semua nilai fitur pertama (2 + 3 + 4 + 3 + 8 = 20) dan fitur kedua (3 + 5 + 4 + 2 + 8 = 22) dari lima titik di Langkah 1.
- `Jumlah titik n  : 5` adalah pembaginya.
- `Centroid        : [4.  4.4]` adalah hasil bagi: 20 / 5 = 4 dan 22 / 5 = 4,4. Jadi pusat kelompok ini berada di koordinat (4; 4,4).
- Centroid ini **bukan salah satu titik data**. Titik yang paling mendekatinya adalah P3 di (4, 4), tetapi tidak persis sama. Perbedaan ini yang nanti membedakan centroid dari medoid (Langkah 3).
- `Sama dengan points.mean(axis=0)? True` berarti hitungan manual kita cocok dengan fungsi bawaan NumPy.
- Perhatikan bahwa P5 di (8, 8) menarik centroid ke arah kanan atas. Tanpa P5, centroid empat titik lainnya adalah (3; 3,5). Pengaruh titik yang jauh ini akan kita lihat lebih jelas di Langkah 4.

**Penjelasan:**

- `n = len(points)` memberi jumlah baris (jumlah titik), yaitu 5.
- `points.sum(axis=0)` menjumlahkan **turun per kolom**. `axis=0` berarti "sepanjang baris", sehingga hasilnya satu jumlah per fitur: `[20, 22]`.
- Membaginya dengan `n` memberi rata-rata tiap fitur, yaitu centroid. Ini sama persis dengan rumus \( \mu = \frac{1}{n}\sum \mathbf{x}_i \).
- `np.allclose(a, b)` memeriksa apakah dua larik sama (dengan toleransi pembulatan). Kita membandingkan dengan `points.mean(axis=0)`, cara singkat NumPy untuk hal yang sama.

### Langkah 3 — Hitung medoid

Centroid di Langkah 2 punya satu kelemahan: ia hanya angka rata-rata dan bisa jatuh di tempat yang tidak ditempati titik mana pun. Kadang kita butuh wakil yang **benar-benar ada** di data, misalnya satu pelanggan nyata yang bisa dilihat dan dijelaskan. Wakil seperti itu disebut **medoid**: anggota kelompok yang paling "sentral".

Ukuran sentral yang dipakai adalah **jumlah jarak** sebuah titik ke semua titik lain. Titik dengan jumlah terkecil adalah yang paling dekat dengan semua anggota secara keseluruhan, sehingga cocok menjadi wakil. Untuk itu kita perlu tahu jarak setiap pasangan titik, dan itu dikerjakan oleh `distance_matrix`. Cara ini lebih mahal daripada centroid karena harus menghitung semua pasangan, tetapi hasilnya selalu titik asli.

```python
--8<-- "level-3/03_centroid_and_representation.py:medoid"
```

```text title="Output"
--8<-- "level-3/outputs/03/medoid.txt"
```

**Cara membaca output:**

- Tiap baris `P1: 13.7` dan seterusnya adalah **jumlah jarak** titik itu ke empat titik lainnya. Makin kecil, makin sentral.
- P3 punya jumlah terkecil (11,54), diikuti P2 (12,48), P1 (13,7), dan P4 (14,46). Keempatnya berada di kumpulan titik yang berdekatan, jadi jumlahnya tidak jauh berbeda.
- P5 melonjak ke 27,11, sekitar 2,3 kali jumlah P3 (27,11 / 11,54). Karena P5 jauh dari semua titik lain, ia paling tidak cocok menjadi wakil.
- `Medoid: P3 [4. 4.]` menyatakan medoidnya adalah P3 di koordinat (4, 4). Ini **titik data asli**.
- Bandingkan dengan centroid dari Langkah 2, yaitu (4; 4,4). Keduanya berdekatan pada data ini, tetapi centroid berupa titik hasil hitungan sedangkan medoid adalah anggota nyata. Perbedaan keduanya akan terasa ketika ada outlier, yang kita lihat di Langkah 4.

**Penjelasan:**

- `distance_matrix(X)` adalah fungsi yang menghitung jarak **setiap titik ke setiap titik lain**. Hasilnya tabel \( n \times n \) (disebut *matriks jarak*, dibahas di Bab 4).
- `X[:, None, :] - X[None, :, :]` menghitung selisih semua pasangan sekaligus lewat *broadcasting*. `** 2`, `.sum(axis=2)`, dan `np.sqrt` mengubah selisih itu menjadi jarak Euclidean.
- `D.sum(axis=1)` menjumlahkan jarak **per baris**: untuk tiap titik, berapa jumlah jaraknya ke semua titik lain.
- `total.argmin()` memberi **nomor baris** dengan jumlah terkecil. Itulah medoid.
- `zip(names, total.round(2))` memasangkan nama dan nilai agar bisa dicetak berdampingan.

### Langkah 4 — Efek outlier

Kita sudah punya dua wakil kelompok: centroid (Langkah 2) dan medoid (Langkah 3). Pada data bersih, keduanya hampir sama, jadi sulit menilai mana yang lebih baik. Perbedaan baru terlihat saat data **tidak bersih**. Data nyata sering memuat *outlier*, yaitu titik yang jauh dari kebanyakan, misalnya pelanggan dengan pendapatan atau belanja yang tidak biasa.

Karena itu kita sengaja menambahkan satu outlier ekstrem di (30, 30), lalu menghitung ulang centroid dan medoid pada data baru. Dengan membandingkan posisi sebelum dan sesudah, kita bisa melihat wakil mana yang **tahan** terhadap titik aneh dan mana yang ikut terseret. Ini penting karena wakil yang bergeser jauh tidak lagi menggambarkan kelompoknya.

```python
--8<-- "level-3/03_centroid_and_representation.py:outlier"
```

```text title="Output"
--8<-- "level-3/outputs/03/outlier.txt"
```

**Cara membaca output:**

- **Centroid** bergeser dari `[4. 4.4]` ke `[8.33 8.67]`, yaitu sekitar 6,1 satuan hanya karena satu titik tambahan. Rumusnya: (20 + 30) / 6 = 8,33 dan (22 + 30) / 6 = 8,67.
- Centroid baru berada di (8,33; 8,67), **lebih jauh dari kelima titik asli**, bahkan melewati P5 di (8, 8). Artinya ia tidak lagi mewakili kumpulan titik yang awalnya berdekatan. Ia berada di antara kelompok kecil itu dan outlier, tempat tidak ada titik sama sekali.
- **Medoid** tetap `[4. 4.]` sebelum dan sesudah, yaitu P3. Medoid ditentukan oleh jumlah jarak, dan P3 masih paling sentral di antara kumpulan titik, sedangkan outlier hanya menambah jarak ke semua titik hampir sama besar.
- Kesimpulannya: centroid **peka** terhadap outlier, medoid **lebih kokoh**. Karena itu medoid dipilih bila data banyak mengandung outlier, sedangkan centroid tetap umum dipakai karena murah dihitung dan mudah diturunkan secara matematis.

**Penjelasan:**

- `np.vstack([points, [[30, 30]]])` menumpuk satu baris baru (titik (30, 30)) di bawah data lama. Titik ini sengaja jauh: sebuah *outlier*.
- Kita hitung ulang centroid dan medoid pada data baru, lalu membandingkannya dengan hasil sebelum outlier ditambahkan.

### Langkah 5 — Centroid berpindah

Di Langkah 2 sampai 4 centroid dihitung dari kelompok yang sudah **diketahui** anggotanya. Pada clustering sungguhan, anggota kelompok justru belum diketahui: yang ada hanya tebakan pusat, lalu titik dikelompokkan ke pusat terdekat, dan pusat dihitung ulang dari anggotanya. Langkah ini memperlihatkan satu putaran proses itu.

Tujuannya menunjukkan bahwa **centroid bukan nilai tetap**: ia berubah setiap kali keanggotaan berubah. Perilaku inilah yang nanti dimanfaatkan K-Means di Level 4, yang mengulang putaran ini sampai pusat berhenti bergeser.

```python
--8<-- "level-3/03_centroid_and_representation.py:move"
```

```text title="Output"
--8<-- "level-3/outputs/03/move.txt"
```

**Cara membaca output:**

- `Pusat awal` adalah dua tebakan kita: (2, 2) dan (7, 7). Keduanya bukan hasil perhitungan, hanya titik awal.
- `Kelompok tiap titik: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 1}` menunjukkan bahwa P1 sampai P4 lebih dekat ke pusat 0, sedangkan P5 yang jauh sendirian ke pusat 1. Jadi kelompok 0 punya empat anggota dan kelompok 1 hanya satu.
- `Pusat baru` adalah rata-rata anggota masing-masing. Pusat 0 menjadi (3; 3,5), yaitu rata-rata P1 sampai P4. Pusat 1 menjadi (8, 8), tepat di P5, karena rata-rata satu titik adalah titik itu sendiri.
- `Pergeseran pusat: [1.8  1.41]` adalah jarak perpindahan tiap pusat dari tebakan awalnya: pusat 0 bergeser sekitar 1,80 (dari (2, 2) ke (3; 3,5)) dan pusat 1 sekitar 1,41 (dari (7, 7) ke (8, 8)).
- Pusat yang bergeser berarti tebakan awal belum pas. Bila putarannya diulang dengan pusat baru, keanggotaan kelima titik di sini tidak berubah (P1 sampai P4 tetap lebih dekat ke (3; 3,5), P5 ke (8, 8)), sehingga pusat langsung stabil. Pada data yang lebih rumit, butuh beberapa putaran sampai keanggotaan berhenti berubah.

**Penjelasan:**

- `start` adalah dua **tebakan** pusat awal: (2, 2) dan (7, 7).
- `points[:, None, :] - start[None, :, :]` menghitung jarak setiap titik ke kedua tebakan pusat. Hasil `d` berukuran (5 titik) × (2 pusat).
- `d.argmin(axis=1)` memilih, untuk tiap titik, **nomor pusat terdekat**. Itulah keanggotaan.
- `points[assign == k].mean(axis=0)` menghitung **rata-rata anggota** kelompok `k`, yaitu centroid baru.
- Baris terakhir menghitung seberapa jauh tiap pusat bergeser dari tebakan awalnya.

!!! note "Ini hanya satu putaran"
    Kita memakai langkah "tentukan anggota lalu hitung ulang pusat" **sekali** untuk memperlihatkan pergeseran. Pada algoritma K-Means di Level 4, langkah ini diulang sampai pusat tidak banyak berubah.

### Langkah 6 — Centroid pada Mall Customers

Langkah 2 sampai 5 memakai lima titik kecil agar bisa dihitung dengan tangan. Sekarang kita pindahkan ide yang sama ke **data nyata**: 200 pelanggan Mall Customers. Ada dua tujuan. Pertama, membuktikan bahwa centroid yang dihasilkan K-Means memang **rata-rata anggota kelompoknya**, persis seperti yang kita hitung manual di Langkah 2, bukan sesuatu yang berbeda atau rumit. Kedua, melihat bahwa centroid berguna sebagai **profil**: lima baris angka yang meringkas karakter tiap kelompok.

Pembuktiannya dengan dua jalan: menghitung rata-rata per kelompok memakai pandas (`groupby`), lalu membandingkannya dengan `cluster_centers_` dari K-Means. Bila keduanya sama, ide "pusat = rata-rata anggota" terbukti berlaku pada data sungguhan.

```python
--8<-- "level-3/03_centroid_and_representation.py:mall"
```

```text title="Output"
--8<-- "level-3/outputs/03/mall.txt"
```

**Cara membaca output:**

- Ada dua tabel. Tabel pertama (`groupby`) adalah rata-rata yang kita hitung sendiri, tabel kedua adalah centroid dari K-Means. Baris dan kolomnya sama: lima kelompok (0 sampai 4), dua fitur.
- Isi kedua tabel **identik** pada semua sel, dan baris terakhir `Sama? True` memastikannya. Jadi centroid K-Means tidak lebih dari rata-rata anggota kelompok.
- Setiap baris centroid bisa dibaca sebagai **profil kelompok** (pendapatan dalam k\$, skor belanja 1-100):
    - Kelompok 0: pendapatan 55,30 dan skor 49,52, yaitu menengah di kedua fitur.
    - Kelompok 1: pendapatan 86,54 dan skor 82,13, yaitu pendapatan tinggi dan belanja tinggi.
    - Kelompok 2: pendapatan 25,73 dan skor 79,36, yaitu pendapatan rendah tetapi belanja tinggi.
    - Kelompok 3: pendapatan 88,20 dan skor 17,11, yaitu pendapatan tinggi tetapi belanja rendah.
    - Kelompok 4: pendapatan 26,30 dan skor 20,91, yaitu pendapatan rendah dan belanja rendah.
- Label seperti "tinggi" dan "rendah" di atas hanya pembacaan dari angka centroid. Centroid adalah rata-rata, jadi tidak semua anggota kelompok persis seperti itu.

**Penjelasan:**

- Kita memuat data dan melakukan clustering seperti Bab 1.
- `df.groupby("Cluster")[cols].mean()` menghitung rata-rata tiap kelompok dengan pandas.
- `model.cluster_centers_` adalah centroid yang dihitung K-Means.
- `np.allclose(...)` membuktikan keduanya sama. Jadi "rata-rata anggota" dan "centroid" adalah hal yang sama.
- `pd.DataFrame(model.cluster_centers_, columns=cols)` membungkus larik menjadi tabel berlabel.

### Langkah 7 — Visualisasi

Langkah 2 sampai 6 menghasilkan angka. Angka tepat, tetapi sulit dirasakan: "centroid bergeser 6,1 satuan" belum memberi gambaran sejauh apa itu dibanding sebaran datanya. Karena itu kita menggambar tiga hal yang sudah dihitung: perbandingan centroid dan medoid dengan serta tanpa outlier, perpindahan pusat, dan centroid pada data Mall Customers.

Semua gambar memakai data dan hasil dari langkah sebelumnya, tanpa perhitungan baru, jadi gambar ini hanya **memperlihatkan** apa yang sudah kita buktikan dengan angka.

```python
--8<-- "level-3/03_centroid_and_representation.py:plot"
```

![Dua panel: kiri lima titik dengan centroid dan medoid berdekatan, kanan setelah ditambah outlier di (30, 30) sehingga centroid tertarik jauh sedangkan medoid tetap](../assets/level-3/03-centroid-vs-medoid.png)

**Cara membaca gambar 1 (centroid vs medoid):**

- **Panel kiri (tanpa outlier):** `X` oranye (centroid, di (4; 4,4)) dan berlian biru (medoid, di (4, 4)) letaknya berdekatan, di tengah kumpulan empat titik dan P5 di pojok kanan atas.
- **Panel kanan (dengan outlier di (30, 30)):** sumbu melebar, dan kelima titik asli mengumpul di pojok kiri bawah. Centroid terseret ke sekitar (8,33; 8,67), jauh dari kumpulan itu dan hampir menempel pada P5. Medoid tetap di (4, 4), di tengah kumpulan empat titik.
- Inilah arti peka dan kokoh dari Langkah 4: satu titik jauh cukup memindahkan centroid, tetapi tidak medoid.

![Dua pusat awal berpindah ke pusat baru dengan panah, di atas lima titik data](../assets/level-3/03-centroid-berpindah.png)

**Cara membaca gambar 2 (centroid berpindah):**

- Kotak oranye adalah tebakan pusat awal, (2, 2) dan (7, 7). Tanda `X` oranye adalah pusat baru, dan panah menunjukkan arah perpindahannya.
- Pusat kiri bergerak naik ke kanan ke (3; 3,5), ke tengah empat titik anggotanya (P1 sampai P4). Pusat kanan bergerak ke (8, 8), tepat menimpa P5 karena kelompoknya hanya satu titik.
- Panah menunjukkan bahwa pusat **mengejar anggotanya**: ia pindah ke tempat rata-rata anggota berada. Panjang panah sesuai `[1.8  1.41]` dari Langkah 5.

![Scatter plot Mall Customers lima warna dengan label centroid di tengah tiap kelompok](../assets/level-3/03-centroid-mall.png)

**Cara membaca gambar 3 (centroid Mall Customers):**

- Tiap warna adalah satu kelompok, dan kotak putih bertanda \( \mu_0 \) sampai \( \mu_4 \) menandai centroidnya. Letaknya cocok dengan tabel di Langkah 6.
- Lima kelompok tersebar di lima daerah: \( \mu_0 \) di tengah (pendapatan dan belanja menengah), \( \mu_1 \) di kanan atas, \( \mu_2 \) di kiri atas, \( \mu_3 \) di kanan bawah, dan \( \mu_4 \) di kiri bawah.
- Tiap centroid berada di tengah awan titik warnanya, sehingga memang menjadi wakil kelompok. Kelompok 0 terlihat paling padat di sekitar \( \mu_0 \), sedangkan kelompok di pojok-pojok lebih tersebar.

**Penjelasan:**

- Grafik pertama membandingkan data **tanpa** outlier dan **dengan** outlier. Centroid digambar sebagai `X` oranye dan medoid sebagai berlian biru.
- Grafik kedua menggambar tebakan pusat awal (kotak), pusat baru (tanda `X`), dan panah pergeseran memakai `ax.annotate("", xy=..., xytext=..., arrowprops=...)`.
- Grafik ketiga menandai centroid tiap kelompok Mall Customers dengan label \( \mu_0 \) sampai \( \mu_4 \) di dalam kotak putih (`bbox=...`) agar terbaca di atas titik.
- `marker="X"` dan `marker="D"` memilih bentuk tanda, `s=` ukuran, dan `alpha=` transparansi.

## Code Explanation

| Yang kamu lihat | Artinya |
|---|---|
| `points.sum(axis=0) / n` | Rumus centroid: jumlah per fitur dibagi jumlah titik |
| `points.mean(axis=0)` | Cara singkat menghitung hal yang sama |
| `D.sum(axis=1).argmin()` | Mencari medoid: baris dengan jumlah jarak terkecil |
| `.argmin(axis=1)` pada jarak ke pusat | Keanggotaan: pusat terdekat |
| `points[assign == k].mean(axis=0)` | Centroid baru untuk kelompok `k` |

Pola umumnya: **jarak → pilih yang terdekat → rata-ratakan anggota.** Ini fondasi hampir semua algoritma berbasis pusat.

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
pip install -r requirements-notebooks.txt
python examples/level-3/03_centroid_and_representation.py
```

Skrip membuat tiga gambar di `docs/assets/level-3/`. Untuk notebook:

```powershell
jupyter notebook notebooks/level-3/03-centroid-and-cluster-representation.ipynb
```

## Expected Output

Semua output berasal dari eksekusi nyata skrip (Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, matplotlib 3.11.1). Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).


Gambar yang dihasilkan:

![Dua panel: kiri lima titik dengan centroid dan medoid berdekatan, kanan setelah ditambah outlier di (30, 30) sehingga centroid tertarik jauh sedangkan medoid tetap](../assets/level-3/03-centroid-vs-medoid.png)

![Dua pusat awal berpindah ke pusat baru dengan panah, di atas lima titik data](../assets/level-3/03-centroid-berpindah.png)

![Scatter plot Mall Customers lima warna dengan label centroid di tengah tiap kelompok](../assets/level-3/03-centroid-mall.png)

### Interpretasi output

**Centroid dan medoid.** Centroid kelima titik adalah \( (4;\ 4{,}4) \), sama dengan hitungan manual. Jumlah jarak terkecil dimiliki \( P_3 \) (11,54), jadi medoid adalah \( P_3 = (4, 4) \). Kedua wakil ini berdekatan karena data tidak punya outlier berat.

**Efek outlier.** Setelah titik (30, 30) ditambahkan, centroid melonjak dari \( (4;\ 4{,}4) \) menjadi \( (8{,}33;\ 8{,}67) \): bergeser sekitar dua kali lipat hanya karena **satu titik**. Medoid tetap di \( (4, 4) \). Inilah alasan medoid disebut lebih tahan *outlier*. Itu juga alasan Level 2 Bab 7 menekankan penanganan outlier sebelum clustering berbasis rata-rata.

**Pusat berpindah.** Dari tebakan awal (2, 2) dan (7, 7), empat titik pertama jatuh ke pusat pertama dan \( P_5 \) ke pusat kedua. Pusat baru adalah rata-rata anggotanya: \( (3;\ 3{,}5) \) dan \( (8;\ 8) \). Pusat pertama bergeser 1,8 satuan dan pusat kedua 1,41 satuan.

**Mall Customers.** Tabel `groupby` dan centroid K-Means identik di semua angka, dan `np.allclose` menghasilkan `True`. Misalnya kelompok 1 berpusat di \( (86{,}54;\ 82{,}13) \): pelanggan tipikalnya berpendapatan dan berbelanja tinggi.

## Practical Examples

**Menjelaskan segmen ke manajer.** Alih-alih membacakan 39 baris, katakan: "Kelompok 1 berpusat di pendapatan 86,5 ribu dolar dan skor belanja 82". Itu satu kalimat yang bisa langsung dipakai.

**Memilih contoh nyata.** Jika manajer ingin "satu pelanggan contoh" untuk wawancara, ambil **medoid** kelompok: ia pelanggan sungguhan yang paling mewakili kelompoknya.

**Data dengan outlier.** Pada data penjualan yang ada transaksi sangat besar sesekali, centroid bisa menyesatkan. Medoid atau penanganan outlier lebih aman.

**Data kategori.** Untuk data seperti jenis produk atau kota, rata-rata tidak berarti. Medoid, yang hanya butuh ukuran jarak, tetap bisa dipakai. Topik jarak untuk data kategori dibahas di Bab 4.

## Hands-on Exercises

1. Hitung centroid manual untuk \( \{(1,1), (2,3), (6,5)\} \).
2. Cari medoid dan centroid untuk data satu dimensi \( \{1, 2, 9\} \) secara manual. Apakah keduanya sama?
3. Pada Langkah 4, ganti outlier menjadi (100, 100). Apakah medoid berubah? Apakah centroid bergeser lebih jauh?
4. Mengapa centroid tidak cocok untuk data kategori seperti `Gender`?
5. Pada Langkah 5, tukar urutan pusat awal menjadi `[[7, 7], [2, 2]]`. Apa yang berubah pada hasil?

??? question "Jawaban"
    1. \( \mu_1 = (1+2+6)/3 = 3 \) dan \( \mu_2 = (1+3+5)/3 = 3 \). Centroid: \( (3, 3) \).
    2. Centroid: \( (1+2+9)/3 = 4 \). Jumlah jarak: titik 1 = \( |1-2| + |1-9| = 9 \); titik 2 = \( |2-1| + |2-9| = 8 \); titik 9 = \( |9-1| + |9-2| = 15 \). Terkecil adalah 8, jadi medoid = **2**. Keduanya berbeda: centroid (4) bukan anggota data dan tertarik oleh angka 9, sedangkan medoid (2) adalah data asli.
    3. Hasil eksekusi nyata: medoid **tetap** \( (4, 4) \), sedangkan centroid melonjak ke \( (20{,}00;\ 20{,}33) \). Makin jauh outlier, makin jauh centroid tertarik, sementara medoid tidak ikut.
    4. Rata-rata dari kategori ("Female" dan "Male") tidak punya arti. Kategori hanya bisa dihitung kemunculannya, jadi wakil yang masuk akal adalah **nilai yang paling sering muncul** atau medoid dengan ukuran jarak khusus kategori.
    5. Hasil eksekusi nyata: empat titik pertama kini masuk kelompok 1 dan \( P_5 \) masuk kelompok 0, jadi **nomor kelompok tertukar**. Pusat barunya tetap \( (3;\ 3{,}5) \) dan \( (8;\ 8) \) (urutannya ikut tertukar). Ini contoh bahwa nomor kelompok hanyalah penanda.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| Centroid berisi angka yang dibulatkan ke bilangan bulat | Larik bertipe integer | Buat larik dengan `dtype=float` |
| `axis` tertukar, hasil berbentuk salah | Bingung `axis=0` dan `axis=1` | Ingat: `axis=0` meringkas **turun** baris (satu hasil per kolom), `axis=1` meringkas **ke samping** (satu hasil per baris) |
| Centroid tampak aneh pada data dengan outlier | Rata-rata tertarik outlier | Tangani outlier (Level 2 Bab 7) atau pakai medoid |
| Medoid lambat pada data besar | Matriks jarak berukuran \( n \times n \) | Pakai sampel atau algoritma yang efisien. Untuk belajar, data kecil sudah cukup |
| Pusat K-Means berbeda dari `groupby` | Memakai data berbeda atau sudah diskalakan | Pastikan fitur yang dipakai untuk `fit` dan `groupby` sama dan dalam skala yang sama |

## Summary

- **Centroid** adalah rata-rata tiap fitur anggota kelompok: \( \mu = \frac{1}{n}\sum \mathbf{x}_i \). Ia belum tentu berupa data asli.
- **Medoid** adalah anggota nyata dengan jumlah jarak terkecil ke anggota lain.
- Centroid **sensitif outlier**: satu titik (30, 30) menggeser centroid dari \( (4;\ 4{,}4) \) ke \( (8{,}33;\ 8{,}67) \), sedangkan medoid tetap di \( (4, 4) \).
- Centroid **berpindah** mengikuti anggotanya. Banyak algoritma memanfaatkannya secara berulang.
- Centroid kelompok pada Mall Customers sama dengan rata-rata anggotanya, sehingga ia bisa dibaca sebagai profil kelompok.

**Bab berikutnya:** Bab 4 membahas cara mengukur kemiripan (*similarity*) dan perbedaan (*dissimilarity*) antar data, termasuk matriks jarak.

## References

- Tan, P.-N., Steinbach, M., Karpatne, A., & Kumar, V. *Introduction to Data Mining* (Pearson), bab tentang *Cluster Analysis*.
- Kaufman, L., & Rousseeuw, P. J. (1990). *Finding Groups in Data: An Introduction to Cluster Analysis*. Wiley. (Sumber klasik gagasan medoid.)
- NumPy documentation: [`numpy.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html) dan [`numpy.argmin`](https://numpy.org/doc/stable/reference/generated/numpy.argmin.html).
- Scikit-learn documentation: [`KMeans`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), atribut `cluster_centers_`.
