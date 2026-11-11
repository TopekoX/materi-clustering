# Bab 10 — Experimental Reporting and Interpretation

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menyusun laporan eksperimen clustering dengan struktur yang jelas: pertanyaan, data, praproses, algoritma, kondisi, metrik, hasil, keterbatasan, dan kesimpulan.
- [x] Menyajikan hasil dalam **tabel** dan **gambar** yang bisa dibaca sendiri tanpa harus membaca kodenya.
- [x] Menjelaskan **hasil metrik yang bertentangan** tanpa memilih angka yang menguntungkan.
- [x] Menulis tafsir ilmiah yang membedakan **temuan**, **tafsiran**, dan **dugaan**.
- [x] Mengenali dan menghindari **klaim berlebihan** (*overclaiming*), termasuk klaim sebab-akibat.
- [x] Menyusun laporan dari file hasil sehingga **tidak ada angka yang diketik tangan**.
- [x] Mencatat detail reproduksibilitas dalam laporan.
- [x] Menjelaskan apa yang sudah dan belum dicakup Level 6, dan apa yang dibawa ke Level 7.
- [x] Menjalankan **Eksperimen G** dari awal sampai akhir dan mencatatnya.

## Introduction

Bab 1 sampai 9 mengajarkan cara menjalankan eksperimen: merancang, menyetel, membandingkan, menggambar, menafsirkan, dan menguji kestabilan. Hasil semua itu ada di berbagai tabel, gambar, dan file CSV. Tetapi pekerjaan belum selesai sebelum orang lain bisa **memahami, memeriksa, dan mengulangnya**.

Bab ini mengajarkan cara mengomunikasikan hasil. Pertanyaan yang ingin dijawab:

**"Bagaimana melaporkan eksperimen clustering supaya jujur, bisa diperiksa, dan tidak menyatakan lebih dari yang didukung datanya?"**

Pelaporan sering dianggap pekerjaan terakhir yang tinggal "menulis hasil". Padahal di sinilah banyak eksperimen yang baik menjadi menyesatkan: angka yang menguntungkan dipilih, keterbatasan tidak disebut, dan "asosiasi" diam-diam menjadi "sebab". Bab ini membahas cara menghindarinya.

Contoh yang dipakai adalah **eksperimen Mall Customers** dari Bab 7 dan 9. Kita menyusun laporannya dari **file hasil yang sudah tersimpan**, sehingga tabel dan angkanya berasal dari eksekusi nyata dan bukan hasil ketikan.

!!! note "Batas dengan Level 7"
    Bab ini mengajarkan **pelaporan satu rangkaian eksperimen**. Makalah akademik lengkap, tinjauan pustaka sistematis, perumusan celah riset, dan persiapan publikasi adalah materi **Level 7 (Research Project)**. Di sini kita hanya menyiapkan bahan dan kebiasaan untuk ke sana.

!!! note "Prasyarat"
    [Bab 2](02-experimental-design-and-configuration.md) (pencatatan), [Bab 4](04-algorithm-comparison-and-benchmarking.md) (tabel hasil dan metrik bertentangan), [Bab 7](07-cluster-interpretation-and-profiling.md) (profil), [Bab 8](08-cluster-visualization-and-analysis.md) (visualisasi), dan [Bab 9](09-cluster-stability-and-reproducibility.md) (kestabilan). Skrip bab ini membaca file hasil dari Bab 4, 7, dan 9, jadi jalankan skrip Bab 7 dan 9 terlebih dahulu.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Experimental report** | Dokumen yang menjelaskan apa yang dikerjakan, bagaimana, dan apa hasilnya, cukup rinci untuk diperiksa |
| **Finding (temuan)** | Hal yang **diamati** langsung dari data (misalnya "Silhouette K = 5 adalah 0,555") |
| **Interpretation (tafsiran)** | Makna yang kita berikan pada temuan, beserta alasannya |
| **Speculation (dugaan)** | Penjelasan yang **belum diuji**; harus ditandai sebagai dugaan |
| **Overclaiming** | Menyatakan lebih dari yang didukung bukti |
| **Limitation** | Batas yang membuat kesimpulan tidak boleh digeneralisasi |
| **Result table** | Tabel angka hasil eksperimen, dengan satuan, jumlah data, dan konfigurasi yang jelas |
| **Figure caption** | Keterangan gambar yang menyebut apa yang digambar, data apa, dan apa yang perlu dibaca |
| **Reproducibility statement** | Pernyataan seed, versi, data, dan file yang diperlukan untuk mengulang eksperimen |
| **Single source of truth** | Prinsip bahwa setiap angka dalam laporan berasal dari satu file sumber, bukan disalin tangan |

## Detailed Explanation

### Laporan bukan catatan kronologis

Laporan tidak menceritakan semua yang kamu coba menurut urutan waktu. Laporan menjawab satu pertanyaan, dengan bukti yang tersusun. Namun **jangan menyembunyikan** percobaan yang tidak berhasil jika memengaruhi kesimpulan. Misalnya, jika kamu mencoba K = 2 sampai 8 dan hanya melaporkan K = 5, pembaca tidak tahu bahwa K = 3 lebih stabil.

### Struktur laporan

Urutan yang dipakai dalam bab ini:

1. **Pertanyaan dan tujuan.** Apa yang ingin diketahui? Apakah eksperimen bersifat eksploratif atau menguji hipotesis? (Bab 1: pada clustering tanpa label acuan, tujuan sering eksploratif.)
2. **Data.** Sumber, ukuran, kolom, nilai kosong, rentang nilai, dan sidik jari data.
3. **Praproses dan fitur.** Apa yang dilakukan pada data, fitur mana yang dipakai dan mana yang tidak.
4. **Algoritma dan konfigurasi.** Algoritma, hyperparameter, seed, dan cara memilih parameter.
5. **Kondisi eksperimen.** Apa yang divariasikan dan apa yang dikontrol (Bab 2).
6. **Metrik.** Metrik apa yang dipakai dan mengapa. Metrik eksternal hanya bila ada label acuan.
7. **Hasil.** Tabel dan gambar, dengan pembacaan singkat.
8. **Pembahasan.** Tafsiran, hasil yang bertentangan, dan perbandingan.
9. **Keterbatasan.**
10. **Kesimpulan yang didukung data.**
11. **Reproduksibilitas.** Seed, versi, file.

Laporan contoh di bawah menggabungkan beberapa bagian supaya ringkas: kondisi eksperimen dan metrik dimasukkan ke bagian algoritma, dan pembahasan dimasukkan ke bagian hasil. Strukturnya boleh disesuaikan, selama semua informasi di daftar ini tersedia.

### Mendeskripsikan data dan praproses

Pembaca harus bisa menjawab: *data apa persisnya yang dipakai?* Laporkan:

- Sumber dan cara memperolehnya (dan lisensinya bila relevan).
- Jumlah baris dan kolom, nilai kosong, rentang tiap kolom penting.
- Sidik jari data (Bab 9), supaya orang bisa memeriksa bahwa data yang sama dipakai.
- Setiap langkah praproses **berurutan**: skala, pembuangan kolom, penanganan nilai kosong.

Menyatakan "data dibersihkan" tidak cukup. Sebutkan apa yang dibersihkan.

### Tabel hasil

Tabel yang baik memuat **konfigurasi** dan **hasil** yang cukup agar baris bisa dipahami sendiri:

- Beri judul dan satuan pada kolom.
- Sebutkan jumlah data tiap baris (misalnya ukuran kelompok).
- Pakai jumlah desimal yang konsisten, dan jangan memberi kesan presisi palsu (tiga desimal untuk Silhouette sudah cukup).
- Laporkan **minimum atau sebaran**, bukan hanya rata-rata (Bab 7 dan 9).
- Jangan menyoroti hanya sel yang menguntungkan.

### Gambar

Gambar yang baik (Bab 8) memiliki judul, label sumbu, legenda, dan **keterangan** (*caption*) yang menyebut data, konfigurasi, dan apa yang perlu dibaca. Rujuk gambar dari teks ("Gambar 1b menunjukkan..."). Gambar juga harus **jujur**: sumbu tidak menyesatkan, warna konsisten, dan ketidakpastian ditandai.

### Melaporkan profil kelompok

Dari Bab 7: laporkan ukuran, rata-rata dan median, sebaran, serta **variabel di luar clustering** yang diuji dengan uji permutasi. Beri nama kelompok yang **deskriptif** (berbasis aturan tertulis), bukan menghakimi. Pemisahan antara variabel yang dipakai dan tidak dipakai harus **tertulis** di laporan.

### Membandingkan perilaku algoritma

Dari Bab 4: perbandingan hanya adil bila kondisinya sama dan terdokumentasi. Laporkan protokolnya (dataset, praproses, cara menentukan parameter), hasil semua metrik, dan **jangan menyimpulkan algoritma terbaik secara umum**. Sebut kondisi tempat algoritma itu unggul atau gagal, dan batasan data yang dipakai.

### Menjelaskan hasil yang bertentangan

Metrik sering tidak sepakat. Cara melaporkannya:

1. **Tampilkan keduanya.** Jangan memilih metrik yang mendukung kesimpulan yang diinginkan.
2. **Jelaskan apa yang diukur tiap metrik.** Silhouette menilai keterpisahan dan kekompakan, kestabilan menilai konsistensi terhadap sampel, ARI menilai kecocokan dengan label acuan.
3. **Cari penyebab pertentangan** (misalnya bentuk kelompok tidak bulat, sehingga metrik berbasis jarak ke pusat menyesatkan).
4. **Nyatakan keputusan dan alasannya**, serta bahwa itu keputusan, bukan fakta.

Contoh dalam bab ini: pada data bulan sabit (Bab 4), Silhouette dan Davies-Bouldin lebih menyukai K-Means, sedangkan ARI terhadap label acuan jauh lebih menyukai DBSCAN. Di Eksperimen G kita melihat angkanya.

### Menulis tafsir ilmiah

Bedakan tiga jenis pernyataan, dan tulis dengan bahasa yang sesuai:

| Jenis | Contoh | Bahasa |
|---|---|---|
| **Temuan** (diamati) | "Silhouette K = 5 adalah 0,555, tertinggi di antara K = 2 sampai 8." | Langsung, dengan angka |
| **Tafsiran** (alasan dari temuan) | "Ini menunjukkan bahwa K = 5 memberi kelompok yang paling kompak dan terpisah menurut Silhouette." | "menunjukkan", "sejalan dengan", "konsisten dengan" |
| **Dugaan** (belum diuji) | "Kelompok E mungkin terdiri atas pelanggan muda yang belanja banyak." | "mungkin", "dugaan kami", disertai cara mengujinya |

Selalu tuliskan **batas**: pada data apa, dengan konfigurasi apa, dan pada kondisi apa kesimpulan itu berlaku.

### Menghindari klaim berlebihan

| Klaim berlebihan | Mengapa bermasalah | Tulisan yang lebih tepat |
|---|---|---|
| "Hasil ini membuktikan ada lima segmen pelanggan." | Clustering membagi data, bukan membuktikan ada segmen nyata | "Data ini dapat dibagi menjadi lima kelompok yang konsisten terhadap seed dan sampel." |
| "K = 5 adalah yang terbaik." | Terbaik menurut apa? Silhouette? Stabilitas? | "K = 5 memberi Silhouette tertinggi di antara K = 2 sampai 8." |
| "Umur membuat kelompok E berbelanja banyak." | Sebab-akibat tidak bisa disimpulkan dari clustering | "Kelompok E rata-rata lebih muda daripada kelompok lain." |
| "Kelompok C pelanggan pelit." | Penilaian, bukan deskripsi, dan tidak didukung bukti | "Kelompok C: pendapatan tinggi, skor belanja rendah." |
| "Hasil stabil, jadi kelompoknya nyata." | Stabil tidak berarti nyata (Bab 9) | "Hasil konsisten terhadap seed dan sampel yang diuji." |
| "Algoritma X lebih baik dari Y." | Bergantung pada data dan metrik | "Pada dataset ini, dengan konfigurasi ini, X mendapat skor lebih tinggi menurut metrik M." |

### Keterbatasan

Bagian keterbatasan bukan formalitas. Ia memberi tahu pembaca **sejauh mana** kesimpulan boleh dipercaya. Pertanyaan untuk menyusunnya:

- Seberapa besar dan seberapa mewakili datanya?
- Berapa algoritma, fitur, dan konfigurasi yang diuji?
- Apa yang tidak diuji (kestabilan, praproses lain, data lain)?
- Apa yang diandalkan pada pilihan subjektif (ambang, penamaan, ambang Silhouette)?
- Apakah ada label acuan, dan bagaimana dipakai?
- Apakah ada potensi bias dalam data atau pemilihan fitur?

### Reproduksibilitas dalam laporan

Sertakan bagian pendek yang memuat seed, versi Python dan pustaka, sistem operasi, sidik jari data, serta daftar file hasil dan skrip. Bab 9 menunjukkan cara mencatat semuanya. Laporan yang tidak memuat ini sulit diperiksa orang lain.

### Satu sumber kebenaran

Angka yang **diketik tangan** ke laporan rawan salah, dan bisa tidak sinkron bila eksperimen diulang. Praktik yang lebih aman: **laporan dibuat oleh kode dari file hasil**. Dengan begitu, mengulang eksperimen memperbarui laporan secara otomatis, dan setiap angka bisa ditelusuri ke satu file.

Kita tetap menulis **kata-kata tafsiran** sendiri, tetapi angka di dalamnya diisi dari file sumber.

### Pemeriksa kata berlebihan

Bab ini memperkenalkan pemeriksa sederhana: fungsi yang menandai kalimat yang memuat kata berisiko ("membuktikan", "pasti", "menyebabkan", "terbaik", dan sebagainya) bila kalimat itu **tidak** memuat kata penyangkal. Ia hanya **heuristik**. Ia bisa terlewat (kalimat berlebihan yang memakai kata lain) dan bisa salah tangkap. Ia membantu membiasakan diri, bukan pengganti membaca laporan dengan teliti.

### Persiapan untuk Level 7

Level 7 membawa pelaporan ke tingkat makalah penelitian. Hal-hal yang sudah kamu miliki dari Level 6:

| Dari Level 6 | Dipakai di Level 7 |
|---|---|
| Pertanyaan eksperimen dan variabel (Bab 1, 2) | Pertanyaan riset dan rancangan metodologi |
| Pencatatan konfigurasi (Bab 2, 9) | Bagian metode yang bisa direproduksi |
| Perbandingan adil (Bab 4) | Dasar membandingkan dengan penelitian lain |
| Kestabilan dan keterbatasan (Bab 9) | Analisis keterbatasan makalah |
| Laporan eksperimen (bab ini) | Bagian hasil dan pembahasan |

Yang **belum** dicakup dan menjadi materi Level 7: tinjauan pustaka sistematis, perumusan celah riset, pemilihan dataset berdasarkan literatur, pengujian statistik yang lebih formal, penulisan makalah, dan persiapan publikasi.

### Kesalahan umum

1. **Hanya melaporkan hasil yang menguntungkan.**
2. **Mengetik angka tangan**, lalu angka tidak sinkron dengan hasil.
3. **Tidak menyebutkan keterbatasan.**
4. **Klaim sebab-akibat** dari clustering.
5. **Menyatakan satu algoritma terbaik secara umum.**
6. **Melaporkan metrik tanpa konfigurasi** (K, seed, praproses).
7. **Tidak memberi keterangan pada gambar** atau tabel.
8. **Menyembunyikan metrik yang bertentangan.**
9. **Memberi label kelompok yang menghakimi** atau stereotip.
10. **Tidak mencatat seed, versi, dan sidik jari data.**

## Mathematical Foundation

Bab ini tidak memperkenalkan rumus baru. Angka yang muncul dalam laporan (Silhouette, ARI, Jaccard, uji permutasi) sudah dijelaskan di Level 5 dan Bab 3 sampai 9. Pelaporan berarti **menempatkan angka-angka itu pada konteks yang benar**, bukan menghitung ulang.

Satu hal yang berhubungan dengan angka: **jumlah desimal**. Silhouette, ARI, dan Jaccard bernilai antara -1 dan 1, dan tiga desimal sudah lebih dari cukup bagi data berukuran ratusan. Menulis enam desimal memberi kesan presisi yang tidak dimiliki hasil tersebut, karena hasilnya sendiri bergeser dengan seed atau sampel.

## Experimental Procedure (Eksperimen G)

1. **Tujuan:** menyusun laporan eksperimen yang lengkap, dapat diperiksa, dan tidak berlebihan, dari file hasil yang sudah tersimpan.
2. **Dataset (alasan):** **Mall Customers** (200 pelanggan), karena eksperimen pemilihan K, profil, dan kestabilannya sudah dilakukan di Bab 7 dan 9. Untuk contoh **metrik yang bertentangan**, dipakai hasil benchmark **data bulan sabit** dari Bab 4.
3. **Sumber file:** `07_cluster_profile.csv`, `09_stability_by_k.csv`, `09_cluster_jaccard.csv`, `09_config.json`, dan `04_benchmark.csv` di `examples/level-6/results/`.
4. **Langkah:** (a) baca file hasil, (b) deskripsikan data, (c) hitung ulang uji permutasi umur (sebagai pemeriksaan silang dengan Bab 7), (d) susun tabel hasil, (e) contoh metrik bertentangan, (f) periksa kata berlebihan, (g) susun dan simpan laporan, (h) buat gambar untuk laporan.
5. **Hasil disimpan:** `10_report.md` dan `10_config.json` di `examples/level-6/results/`, serta satu gambar di `docs/assets/level-6/`.

## Python Implementation

Skrip lengkapnya ada di `examples/level-6/10_experimental_reporting_and_interpretation.py`, dan notebook-nya di `notebooks/level-6/10-experimental-reporting-and-interpretation.ipynb`. **Setiap potongan kode diikuti penjelasannya.**

**Konteks masalah:** kamu harus menyerahkan laporan eksperimen kepada rekan atau dosen yang belum melihat prosesnya.

**Tujuan eksperimen:** menghasilkan laporan yang angkanya berasal dari file sumber dan yang kalimatnya tidak melebih-lebihkan.

**Pustaka:** NumPy, pandas, Matplotlib, scikit-learn (`KMeans`), pustaka standar (`json`, `re`), dan alat pencatat `_experiment.py`.

!!! warning "Jalankan Bab 7 dan Bab 9 dahulu"
    Skrip ini membaca `07_cluster_profile.csv`, `09_stability_by_k.csv`, `09_cluster_jaccard.csv`, dan `09_config.json`. Jika file-file itu belum ada, jalankan `07_cluster_interpretation_and_profiling.py` dan `09_cluster_stability_and_reproducibility.py` terlebih dahulu. Pesan galatnya adalah `FileNotFoundError`.

### Bagian A — Siapkan alat

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:setup"
```

**Penjelasan:**

- `fmt(value, digits)` memformat angka dengan **koma desimal**, seperti penulisan bahasa Indonesia. `f"{value:.{digits}f}"` memformat dengan jumlah desimal yang kita tentukan, lalu `.replace(".", ",")` mengganti titik dengan koma.
- `md_table(frame)` mengubah DataFrame menjadi tabel Markdown. Header dibuat dari nama kolom, garis pemisah dari `---`, dan setiap baris dari `itertuples`. Dengan fungsi ini kita tidak perlu pustaka tambahan (seperti `tabulate`).

### Bagian B — Membaca file hasil

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:load"
```

```text title="Output"
--8<-- "level-6/outputs/10/load.txt"
```

**Penjelasan:** `pd.read_csv` membaca tabel hasil, dan `json.loads` membaca file konfigurasi Bab 9. `index_col` menjadikan kolom kelompok sebagai indeks. Perulangan di bawahnya mencetak jumlah baris tiap file, sebagai pemeriksaan bahwa file terbaca dan ukurannya wajar (misalnya 5 kelompok, 7 nilai K).

### Bagian C — Deskripsi data

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:dataset"
```

```text title="Output"
--8<-- "level-6/outputs/10/dataset.txt"
```

**Penjelasan:** `data_facts` mengumpulkan fakta data langsung dari file: jumlah baris, daftar kolom, jumlah nilai kosong (`df.isna().sum().sum()`), jumlah tiap gender, dan rentang tiga kolom numerik. Bagian ini akan masuk ke bagian "Data" laporan. Sidik jari data dari konfigurasi Bab 9 dicetak untuk dicocokkan.

### Bagian D — Uji permutasi umur

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:permtest"
```

```text title="Output"
--8<-- "level-6/outputs/10/permtest.txt"
```

**Penjelasan:**

- Kita membangun ulang label kelompok dengan konfigurasi yang sama dengan Bab 7 (K-Means K = 5, `n_init=10`, seed 42, huruf menurut ukuran).
- `assert [...] == profile["n"].tolist()` adalah **pemeriksaan silang**: ukuran kelompok hasil bangun ulang harus sama dengan yang tersimpan di `07_cluster_profile.csv`. Jika berbeda, skrip berhenti dengan pesan, karena berarti kita bukan lagi melaporkan kelompok yang sama.
- Uji permutasi sama seperti Bab 7: mengacak label 2000 kali dan menghitung seberapa sering selisih acak sama besar atau lebih besar dari selisih asli.

### Bagian E — Tabel hasil

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:tables"
```

```text title="Output"
--8<-- "level-6/outputs/10/tables.txt"
```

**Penjelasan:**

- `k_table["silhouette"].idxmax()` memberi indeks baris Silhouette tertinggi. `.loc[...]` mengambil baris itu. Hal yang sama untuk kestabilan. Dengan cara ini, kalimat "Silhouette tertinggi pada K = 5" **dihasilkan dari data**, bukan diketik.
- `table_k` dan `table_profile` adalah tabel yang siap dicetak. `.map(fmt)` memformat setiap sel dengan koma desimal. Kolom Jaccard diambil dengan `.to_numpy()` agar indeksnya tidak ikut (indeks `jaccard` adalah huruf kelompok, sedangkan `table_profile` memakai nomor baris).

### Bagian F — Metrik yang bertentangan

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:conflict"
```

```text title="Output"
--8<-- "level-6/outputs/10/conflict.txt"
```

**Penjelasan:** dari hasil benchmark Bab 4 kita ambil baris dataset "Bulan sabit" untuk dua algoritma (K-Means dan DBSCAN), lalu menyusunnya per algoritma dengan `set_index("algorithm")`. `idxmax()` pada Silhouette dan ARI menunjukkan algoritma mana yang dipilih tiap metrik. Dua baris yang dicetak di akhir menyatakan pertentangannya secara eksplisit.

### Bagian G — Pemeriksa kata berlebihan

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:wording"
```

```text title="Output"
--8<-- "level-6/outputs/10/wording.txt"
```

**Penjelasan baris demi baris:**

- `RISKY` adalah daftar kata yang cenderung melebih-lebihkan. `NEGATIONS` adalah kata penyangkal. Pencocokan memakai kata utuh (`RISKY_PATTERNS`), sehingga "dipastikan" tidak dianggap "pasti", dan kata penyangkal dikenali walau menempel pada tanda baca ("tidak,").
- `re.split(r"(?<=[.!?])\s+", text)` memecah teks menjadi kalimat: memotong pada spasi yang didahului titik, tanda tanya, atau tanda seru.
- Untuk tiap kalimat, `hits` adalah kata berisiko yang muncul. Kalimat ditandai hanya bila ada `hits` **dan** tidak ada kata penyangkal di kalimat itu. Dengan begitu "tidak membuktikan" tidak ditandai.
- `draft` adalah contoh draf yang sengaja buruk. Fungsi menandai kalimat yang berlebihan, dan melewatkan kalimat yang memakai kata penyangkal.
- Fungsi ini heuristik. Latihan 1 menunjukkan kalimat yang lolos.

### Bagian H — Menyusun laporan

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:report"
```

```text title="Output"
--8<-- "level-6/outputs/10/report.txt"
```

**Penjelasan:**

- `report` adalah f-string Markdown yang menyatukan kata-kata tafsiran (ditulis tangan) dengan angka (dari variabel). Contoh: `{fmt(best_sil['silhouette'])}` mengisi nilai Silhouette tertinggi, `{int(best_sil['k'])}` mengisi nilai K-nya.
- Setiap bagian mengikuti struktur: pertanyaan, data, praproses, algoritma, hasil, profil, keterbatasan, kesimpulan, dan reproduksibilitas.
- Bagian lingkungan (`env`) diambil dari `09_config.json`, sehingga versi yang dilaporkan adalah versi yang benar-benar dipakai saat eksperimen Bab 9.
- `flag_overclaims(report)` memeriksa laporan itu sendiri. Hasil yang diharapkan: tidak ada kalimat berisiko.

### Bagian I — Menyimpan laporan

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:save"
```

```text title="Output"
--8<-- "level-6/outputs/10/save.txt"
```

**Penjelasan:** `write_text` menyimpan laporan ke `10_report.md`. `10_config.json` mencatat sumber yang dipakai dan bahwa pemeriksaan kata dilakukan. Laporan ikut tercatat sebagai bagian dari eksperimen.

### Bagian J — Gambar untuk laporan

```python
--8<-- "level-6/10_experimental_reporting_and_interpretation.py:plotreport"
```

![Tiga panel untuk laporan. (a) Silhouette dan kestabilan menurut K dari 2 sampai 8 dengan area berarsir antara rata-rata dan minimum kestabilan. (b) Ukuran lima kelompok pelanggan dengan nilai Jaccard 0,97 sampai 1,00 di atas tiap batang. (c) Pada data bulan sabit, Silhouette menyukai K-Means (0,492 versus 0,389) tetapi ARI terhadap label acuan menyukai DBSCAN (0,960 versus 0,486)](../assets/level-6/10-gambar-laporan.png)

**Penjelasan:** satu figur tiga panel yang bisa langsung dimasukkan ke laporan. Panel (a) menyandingkan Silhouette dan kestabilan menurut K, dengan area berarsir dari rata-rata sampai minimum untuk menunjukkan sebaran. Panel (b) menampilkan ukuran kelompok dengan nilai Jaccard di atas tiap batang. Panel (c) memperlihatkan pertentangan metrik pada data bulan sabit. Warna kelompok sama dengan Bab 7 dan 8.

## Code Explanation

| Bagian kode | Peran |
|---|---|
| `fmt` dan `md_table` | Format angka (koma desimal) dan tabel Markdown tanpa pustaka tambahan |
| `pd.read_csv` dan `json.loads` | Membaca file hasil sebagai satu sumber kebenaran |
| `assert ... == profile["n"].tolist()` | Pemeriksaan silang bahwa kelompok yang dilaporkan sama dengan yang tersimpan |
| `idxmax()` | Menentukan K terbaik menurut tiap kriteria, dari data |
| f-string dengan `{...}` | Mengisi angka ke kalimat tanpa mengetik tangan |
| `flag_overclaims` | Pemeriksa heuristik untuk kata berlebihan |
| `write_text` | Menyimpan laporan sebagai file Markdown |

!!! tip "Mengapa laporan berupa file Markdown?"
    File Markdown mudah dibaca manusia, mudah dibandingkan versinya (git diff), dan mudah diubah menjadi HTML atau PDF. Pada bab ini formatnya sengaja sederhana. Penyusunan makalah akademik lengkap (LaTeX, format jurnal) adalah materi Level 7.

## How to Run

Dari folder utama proyek (setelah mengaktifkan lingkungan virtual), jalankan skrip Bab 7 dan Bab 9 lebih dulu bila file hasilnya belum ada, lalu skrip Bab 10:

```powershell
pip install -r requirements-notebooks.txt
python examples/level-6/07_cluster_interpretation_and_profiling.py
python examples/level-6/09_cluster_stability_and_reproducibility.py
python examples/level-6/10_experimental_reporting_and_interpretation.py
```

Skrip Bab 10 mencetak output ke terminal, menyimpan satu gambar ke `docs/assets/level-6/`, dan laporan ke `examples/level-6/results/10_report.md`. Notebook interaktifnya:

```powershell
jupyter notebook notebooks/level-6/10-experimental-reporting-and-interpretation.ipynb
```

Semua output pada bab ini berasal dari eksekusi nyata dengan Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, dan Matplotlib 3.11.1.

## Expected Output

Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).

Gambar yang dihasilkan:

![Tiga panel untuk laporan. (a) Silhouette dan kestabilan menurut K dari 2 sampai 8 dengan area berarsir antara rata-rata dan minimum kestabilan. (b) Ukuran lima kelompok pelanggan dengan nilai Jaccard 0,97 sampai 1,00 di atas tiap batang. (c) Pada data bulan sabit, Silhouette menyukai K-Means (0,492 versus 0,389) tetapi ARI terhadap label acuan menyukai DBSCAN (0,960 versus 0,486)](../assets/level-6/10-gambar-laporan.png)

### Interpretasi output

**1. File hasil terbaca dengan ukuran yang wajar.** Profil 5 baris (lima kelompok), kestabilan menurut K 7 baris (K = 2 sampai 8), Jaccard 5 baris, benchmark 30 baris (6 dataset dikali 5 algoritma). Sidik jari data `edb2a3858344` sama dengan yang tercatat di Bab 9.

**2. Deskripsi data (dari file, bukan diketik).** 200 pelanggan, lima kolom, **tidak ada nilai kosong**, 112 perempuan dan 88 laki-laki, pendapatan 15 sampai 137 k$, skor belanja 1 sampai 99, umur 18 sampai 70 tahun.

**3. Pemeriksaan silang uji permutasi cocok dengan Bab 7.** Selisih rata-rata umur antar kelompok **19,945 tahun**, batas acak 95% **9,890**, p ≤ **0,0005**, sama persis dengan Bab 7. Angka 0,0005 adalah batas bawah uji permutasi 2000 kali (1/2001): tidak satu pun permutasi acak mencapai selisih teramati, sehingga p dilaporkan sebagai batas, bukan nilai pasti. Pernyataan `assert` juga lolos: ukuran kelompok hasil bangun ulang (81, 39, 35, 23, 22) sama dengan yang tersimpan.

**4. Tabel hasil.** Tabel menurut K dan tabel profil dicetak dalam format yang akan masuk laporan, dengan koma desimal (misalnya `0,555`). Perhatikan bahwa kolom "Kestabilan (minimum)" ikut dilaporkan, termasuk nilai negatif -0,013 pada K = 2, supaya sebaran terlihat.

**5. Metrik yang bertentangan (data bulan sabit).**

| Algoritma | Silhouette | Davies-Bouldin (lebih kecil lebih baik) | ARI terhadap label acuan |
|---|---|---|---|
| K-Means | **0,492** | **0,816** | 0,486 |
| DBSCAN | 0,389 | 1,016 | **0,960** |

Silhouette dan Davies-Bouldin sama-sama memilih K-Means, tetapi ARI memilih DBSCAN dengan selisih besar. Metrik internal mengukur kekompakan dan keterpisahan berdasarkan jarak, sehingga lebih menyukai kelompok yang bulat dan padat. Dua bulan sabit yang saling melingkar tidak memenuhi gambaran itu, dan K-Means membelahnya menjadi dua bagian yang kompak tetapi salah. ARI membandingkan dengan label acuan, dan di sini DBSCAN mengikuti bentuk yang sebenarnya. Laporan yang baik menyajikan **ketiganya**, menjelaskan alasannya, dan tidak memilih salah satu secara diam-diam.

**6. Pemeriksa kata berlebihan.** Dari draf buruk, tiga kalimat ditandai: "membuktikan ... benar-benar ada", "pasti boros", dan "pilihan terbaik". Kalimat keempat ("Kelompok C tidak berbelanja banyak.") lolos karena tidak berisi kata berisiko. Pada **laporan yang dihasilkan**, kalimat berisiko yang ditandai adalah **0** dari 61 baris dan 633 kata.

**7. Laporan dan gambar tersimpan.** `10_report.md` (contoh lengkap di bawah) dan `10_config.json`.

### Contoh laporan lengkap

Berikut laporan yang dihasilkan skrip, apa adanya (`10_report.md`). Perhatikan bagian "Kesimpulan yang didukung data" dan "Keterbatasan": keduanya berhati-hati, dan K = 3 yang lebih stabil tetap **disebut**.

```markdown
--8<-- "level-6/results/10_report.md"
```

Beberapa hal yang patut dicatat dari laporan ini:

- **Menyebut sifat eksperimen.** "Eksploratif: tidak ada label acuan dan tidak ada hipotesis yang diuji secara statistik formal."
- **Menjelaskan pilihan, bukan hanya hasil.** K = 5 dipilih karena Silhouette tertinggi dan kestabilannya juga tinggi, dan laporan menyebut bahwa K = 3 lebih stabil.
- **Menandai asosiasi.** "Ini asosiasi, bukan sebab."
- **Keterbatasan konkret**, bukan umum: kelompok terkecil hanya 22 pelanggan, satu dataset, satu algoritma, dua fitur.
- **Reproduksibilitas lengkap**: seed, versi pustaka, sidik jari data, dan nama file.

!!! warning "Yang boleh dan tidak boleh disimpulkan dari bab ini"
    **Boleh:** laporan ini mendukung pernyataan bahwa pada 200 pelanggan ini, K-Means (K = 5) pada pendapatan dan skor belanja menghasilkan kelompok yang konsisten terhadap seed, sampel, dan bootstrap. **Tidak boleh:** menyimpulkan bahwa laporan yang rapi berarti hasilnya benar. Laporan hanya mengomunikasikan bukti yang ada dengan jujur. Pemeriksa kata pun hanya heuristik dan tidak menjamin tidak ada klaim berlebihan.

## Practical Application

**Laporan ke tim atau dosen.** Gunakan struktur laporan di atas. Mulailah dengan pertanyaan dan akhiri dengan kesimpulan yang didukung data dan keterbatasannya.

**Menyiapkan laporan otomatis.** Jika eksperimen akan diulang dengan data baru (misalnya tiap bulan), pisahkan **kode eksperimen** (menghasilkan file hasil) dari **kode laporan** (membaca file hasil). Laporan lalu dapat dibuat ulang dengan satu perintah.

**Menjawab pertanyaan pembaca.** Pembaca sering bertanya "datanya apa persisnya?", "parameter apa yang dipakai?", "kenapa K ini?", dan "apakah hasilnya stabil?". Struktur laporan menjawab semuanya.

**Membandingkan dengan laporan lain.** Konfigurasi dan metrik yang dilaporkan dengan baik memungkinkan orang lain membandingkan hasil mereka dengan hasilmu, dan menemukan sumber perbedaan.

**Menuju Level 7.** Bagian "Persiapan untuk Level 7" di atas memetakan apa yang dibawa dari Level 6.

## Hands-on Exercises

1. Jalankan `flag_overclaims` pada enam kalimat berikut, lalu catat mana yang ditandai: (a) "Hasil ini mengonfirmasi bahwa lima segmen ada." (b) "Kelompok E memang boros." (c) "Tidak diragukan lagi K = 5 optimal." (d) "Umur menyebabkan perilaku belanja." (e) "Umur tidak menyebabkan perilaku belanja." (f) "Kelompok ini terbukti benar." Mana yang lolos padahal berlebihan?
2. Dari `04_benchmark.csv`, pada dataset mana saja Silhouette dan ARI memilih algoritma yang berbeda jika hanya K-Means dan DBSCAN yang dibandingkan?
3. Tuliskan ulang tiga kalimat berlebihan berikut dalam bentuk temuan, tafsiran, atau dugaan: "Kelompok C adalah pelanggan pelit." "Hasil stabil, jadi kelompoknya nyata." "K-Means lebih baik daripada DBSCAN."
4. Bagian apa yang **belum** ada di laporan contoh dan sebaiknya ditambahkan, jika laporan akan diserahkan ke pihak lain?
5. Mengapa angka dalam laporan sebaiknya dihasilkan dari file hasil, bukan diketik tangan?
6. Mengapa kalimat "Kami memilih K = 5 karena Silhouette tertinggi dan kestabilannya juga tinggi, bukan karena K = 5 terbukti benar" lebih baik daripada "K = 5 adalah yang terbaik"?
7. Tambahkan satu bagian "Perbandingan algoritma" ke laporan dengan memakai hasil Bab 4. Apa yang harus dinyatakan agar perbandingannya adil dan tidak berlebihan?

??? question "Jawaban"
    Hasil nomor 1 dan 2 berasal dari eksekusi nyata.

    1. Hanya kalimat **(d)** yang ditandai (kata "menyebabkan" tanpa penyangkal). Kalimat lain **tidak** ditandai: (a) "mengonfirmasi" tidak ada di daftar `RISKY`, (b) "memang boros" juga tidak, (c) "Tidak diragukan lagi" memuat kata "tidak" sehingga dianggap sebagai penyangkal, padahal kalimatnya justru sangat yakin, dan (f) "terbukti benar" tidak ada di daftar. Kalimat (e) memang tidak berlebihan dan dengan benar tidak ditandai. Jadi pemeriksa ini hanya menangkap kata yang ada di daftar dan bisa tertipu kata penyangkal. Ia membantu, tetapi tidak menggantikan membaca laporan.
    2. Silhouette dan ARI memilih algoritma berbeda pada **4 dari 6** dataset: **Jelas** (Silhouette memilih DBSCAN dengan selisih sangat kecil, 0,899 versus 0,892, ARI memilih K-Means), **Bulan sabit** (Silhouette K-Means, ARI DBSCAN), **Kepadatan berbeda** (Silhouette DBSCAN, ARI K-Means), dan **Miring (elips)** (Silhouette DBSCAN, ARI K-Means). Keduanya sepakat pada **Tumpang tindih** (K-Means) dan **Dengan noise** (DBSCAN). Pada dataset "Jelas", selisihnya sangat kecil, sehingga pertentangan itu tidak berarti banyak. Pada "Bulan sabit" selisihnya besar dan berarti.
    3. "Kelompok C: pendapatan tinggi (rata-rata 88,2 k$) dan skor belanja rendah (17,1)." Ini **temuan**. Sebutan "pelit" adalah penilaian yang tidak didukung data, dan tidak boleh dipakai. Untuk kalimat kedua: "Hasil konsisten terhadap seed, sampel, dan bootstrap yang diuji." (temuan) dan "Konsistensi ini belum membuktikan bahwa kelompok itu bermakna secara praktis." (tafsiran yang berhati-hati). Untuk kalimat ketiga: "Pada data bulan sabit, dengan konfigurasi ini, K-Means mendapat Silhouette lebih tinggi, tetapi DBSCAN jauh lebih cocok dengan label acuan (ARI 0,960 versus 0,486)." Ini temuan dengan batasnya.
    4. Contoh yang bisa ditambahkan: (a) gambar sebaran kelompok (Bab 8) dengan keterangan, (b) hasil kepekaan terhadap seed dan praproses dari Bab 9, (c) kaitan dengan tujuan praktis (apa keputusan yang akan diambil dari kelompok ini), (d) sumber dan lisensi data secara lebih lengkap, (e) uji kestabilan pada data tanpa struktur sebagai pembanding, dan (f) tautan ke skrip dan file hasil.
    5. Angka yang diketik tangan bisa salah ketik atau tidak sinkron setelah eksperimen diulang. Angka yang diisi dari file hasil bisa ditelusuri ke satu sumber, dan laporan ikut diperbarui saat eksperimen diulang. Ini juga menjaga bahwa angka di laporan sama dengan angka di tabel dan gambar.
    6. Kalimat pertama menyebut **kriteria** pilihan (Silhouette tertinggi dan kestabilan tinggi) dan menegaskan bahwa itu keputusan, bukan kebenaran. Kalimat kedua tidak menyebut "terbaik menurut apa" dan bisa dibaca sebagai klaim umum, padahal K = 3 lebih stabil.
    7. Nyatakan dataset dan praproses yang sama untuk semua algoritma, cara menentukan parameter tiap algoritma (apakah diberi K, atau dicari tanpa label), seluruh metrik (bukan hanya yang menguntungkan), serta batas: hasil berlaku untuk dataset ini, dan tidak menyimpulkan algoritma terbaik secara umum. Cantumkan juga hasil yang bertentangan, seperti pada data bulan sabit.

## Troubleshooting

### Masalah teknis

| Masalah | Penyebab | Solusi |
|---|---|---|
| `FileNotFoundError` saat membaca `07_cluster_profile.csv` atau `09_*.csv` | Skrip Bab 7 atau Bab 9 belum dijalankan | Jalankan keduanya lebih dulu |
| `AssertionError: ukuran kelompok tidak cocok` | Versi pustaka atau konfigurasi berbeda dari saat Bab 7 dijalankan | Samakan seed dan konfigurasi, jalankan ulang Bab 7, atau periksa versi pustaka |
| Angka di laporan memakai titik, bukan koma | Memformat dengan `f"{x:.3f}"` tanpa `fmt` | Pakai fungsi `fmt` |
| Tabel Markdown tidak terbentuk | Kolom atau baris berisi karakter `\|` | Hindari karakter `\|` di isi sel atau gantikan dengan `\\|` |
| Pemeriksa kata menandai kalimat yang aman | Heuristik tidak memahami konteks | Baca ulang kalimat, ubah daftar `RISKY` bila perlu |
| Pemeriksa kata melewatkan kalimat berlebihan | Kata tidak ada di daftar, atau ada kata penyangkal | Pemeriksa bukan pengganti membaca |
| Gambar panel (c) kosong atau error | `04_benchmark.csv` tidak memuat dataset "Bulan sabit" | Jalankan ulang skrip Bab 4 |

### Kesalahan umum

1. **Hanya melaporkan hasil yang menguntungkan.**
2. **Mengetik angka tangan** sehingga tidak sinkron.
3. **Tidak menyebut keterbatasan.**
4. **Klaim sebab-akibat** atau klaim umum dari satu dataset.
5. **Menyembunyikan metrik yang bertentangan.**
6. **Label kelompok yang menghakimi.**
7. **Laporan tanpa seed, versi, dan sidik jari data.**
8. **Gambar dan tabel tanpa keterangan.**
9. **Menganggap pemeriksa kata sebagai jaminan.**

## Summary

- **Laporan menjawab satu pertanyaan dengan bukti yang tersusun.** Strukturnya: pertanyaan, data, praproses, algoritma, kondisi, metrik, hasil, pembahasan, keterbatasan, kesimpulan, reproduksibilitas.
- Bedakan **temuan** (diamati), **tafsiran** (alasan dari temuan), dan **dugaan** (belum diuji), dan tulis dengan bahasa yang sesuai.
- **Jangan menyembunyikan hasil yang bertentangan.** Pada data bulan sabit, Silhouette (0,492 versus 0,389) dan Davies-Bouldin (0,816 versus 1,016) memilih K-Means, tetapi ARI memilih DBSCAN (0,960 versus 0,486). Silhouette dan ARI memilih algoritma berbeda pada 4 dari 6 dataset benchmark.
- **Hindari klaim berlebihan**: bukan "membuktikan", bukan "terbaik", bukan "menyebabkan". Tulis kondisi dan batasnya.
- **Satu sumber kebenaran:** laporan dibuat oleh kode dari file hasil. Pada eksperimen Mall Customers, ukuran kelompok, uji permutasi (19,945 tahun, p ≤ 0,0005), dan sidik jari data cocok dengan Bab 7 dan 9.
- Pemeriksa kata hanya **heuristik**. Ia menandai "menyebabkan", tetapi melewatkan kalimat berlebihan yang memakai kata lain atau tertipu kata penyangkal.
- Level 7 melanjutkan ke makalah penuh: tinjauan pustaka, celah riset, dan publikasi.

**Bab berikutnya:** Level 6 berhenti di sini. [Level 7 (Research Project)](../curriculum/index.md) membawa kebiasaan ini ke penelitian yang utuh.

## References

- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). Ten simple rules for reproducible computational research. *PLOS Computational Biology*, 9(10), e1003285.
- Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.
- Hennig, C. (2015). What are the true clusters? *Pattern Recognition Letters*, 64, 53–62.
- Hennig, C. (2007). Cluster-wise assessment of cluster stability. *Computational Statistics & Data Analysis*, 52(1), 258–271.
- Pineau, J., et al. (2021). Improving reproducibility in machine learning research. *Journal of Machine Learning Research*, 22(164), 1–20.
- Kaufman, L., & Rousseeuw, P. J. (1990). *Finding Groups in Data: An Introduction to Cluster Analysis*. Wiley.
- Pandas documentation: [*IO tools (text, CSV, HDF5, ...)*](https://pandas.pydata.org/docs/user_guide/io.html).
