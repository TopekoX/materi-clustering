# Bab 4 — Dataset Selection and Research Data Preparation

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Memilih dataset berdasarkan kecocokannya dengan pertanyaan riset, bukan berdasarkan kemudahan.
- [x] Membedakan data primer dan sekunder, dan mengenali sumber dataset publik.
- [x] Menyusun kartu dokumentasi dataset: sumber, asal-usul (*provenance*), lisensi, dan keterbatasan.
- [x] Membaca lisensi data dan mengetahui apa yang diizinkan dan diwajibkan.
- [x] Memeriksa kualitas dan keterwakilan (*representativeness*) data.
- [x] Menyusun daftar periksa etika dan privasi yang jujur tentang hal yang **tidak diketahui**.
- [x] Menulis kriteria inklusi dan eksklusi sebelum menerapkannya, dan mencatat berapa baris yang dikeluarkan.
- [x] Menyiapkan dataset penelitian final yang bisa diverifikasi dengan sidik jari data.

## Introduction

Di Bab 2 kamu menulis pertanyaan, dan di Bab 3 kamu melihat bahwa pustaka belum cukup mendukung salah satunya. Sekarang kamu harus memilih data. Pemula biasanya memilih data yang paling mudah ditemukan, lalu menyesuaikan pertanyaan dengan data itu. Penelitian yang baik melakukan sebaliknya: **pertanyaan dulu, lalu data yang sanggup menjawabnya**.

Ada alasan yang lebih dalam. Sebuah dataset bukan sekadar tabel angka. Ia punya **asal-usul**: siapa yang mengumpulkan, untuk apa, bagaimana, dan dengan izin apa. Kalau kamu tidak tahu itu, kamu tidak tahu seberapa jauh kesimpulanmu boleh melangkah, dan kamu mungkin melanggar aturan pemakaian tanpa sadar.

Bab ini mengajarkan lima hal: memilih, mendokumentasikan, memeriksa kualitas, mempertimbangkan etika, dan menyiapkan dataset final. Semuanya dikerjakan pada dataset yang sama dengan bab sebelumnya, dengan satu prinsip yang berulang: **tuliskan apa yang diketahui, dan tuliskan juga apa yang tidak diketahui**.

!!! note "Prasyarat"
    - [Bab 2](02-research-problem-formulation.md) dan [Bab 3](03-literature-review-and-research-gap.md).
    - [Level 2](../data-exploration-and-preprocessing/index.md): nilai hilang (Bab 5), data duplikat (Bab 6), outlier (Bab 7), pembersihan (Bab 8), dan persiapan dataset (Bab 12). Bab ini tidak mengulang cara melakukannya, hanya menempatkannya dalam konteks penelitian.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Primary data** (data primer) | Data yang kamu kumpulkan sendiri untuk penelitianmu |
| **Secondary data** (data sekunder) | Data yang dikumpulkan pihak lain dan kamu pakai ulang |
| **Public dataset** | Dataset yang bisa diakses umum. **Bisa diakses tidak berarti bebas dipakai untuk apa saja** |
| **Provenance** (asal-usul) | Riwayat data: siapa pembuatnya, bagaimana dikumpulkan, dan perubahan yang pernah terjadi |
| **License** (lisensi) | Aturan resmi tentang apa yang boleh dan wajib dilakukan terhadap data |
| **Attribution** | Kewajiban mencantumkan pembuat dan sumber |
| **Representativeness** | Seberapa baik data mewakili populasi yang ingin kamu bicarakan |
| **Inclusion / exclusion criteria** | Aturan tertulis tentang baris atau fitur yang dipakai atau dibuang |
| **Datasheet / dataset card** | Dokumen ringkas yang mencatat asal, isi, penggunaan, dan keterbatasan dataset |
| **De-identification** | Penghapusan informasi yang bisa mengidentifikasi individu |
| **Data fingerprint** | Hash isi data yang berubah bila isi berubah (Level 6 Bab 9) |

## Detailed Explanation

### Memilih dataset yang cocok dengan pertanyaan

Mulai dari pertanyaan, lalu periksa apa yang dibutuhkannya. Untuk RQ1 sampai RQ3 kebutuhannya:

| Kebutuhan | Berasal dari |
|---|---|
| Cukup sampel untuk diulang dan dicuplik | RQ1 (kestabilan) |
| Fitur numerik dengan skala berbeda | RQ2 (kepekaan terhadap penyamaan skala) |
| **Label eksternal** | RQ3 (keselarasan dengan diagnosis) |
| Lisensi jelas dan boleh dipakai ulang | Tuntutan penelitian yang bisa diulang |
| Dokumentasi yang cukup | Agar keterbatasan bisa dinyatakan |

**Perbandingan beberapa kandidat.** Tabel berikut mencerminkan apa yang sudah kamu temui di Level 2–6 dan apa yang **sudah atau belum diverifikasi** di proyek ini.

| Kandidat | Label untuk RQ3? | Lisensi di proyek ini | Catatan |
|---|---|---|---|
| **Breast Cancer Wisconsin (Diagnostic)** | Ada (diagnosis) | **Terverifikasi**: CC BY 4.0 menurut halaman UCI | Dipilih |
| Wine (scikit-learn) | Ada (tiga kelas) | Belum diverifikasi di proyek ini | Sudah dipakai di Level 6 |
| Mall Customers | Tidak ada | **Belum dipastikan**; Level 2 Bab 1 menyarankan memeriksa lisensi di sumber asli (Kaggle) | Cocok untuk belajar, belum untuk penelitian |
| Data sintetis (`make_blobs`) | Ada (dibangkitkan) | Tidak berlaku, buatan sendiri | Tidak mendukung klaim empiris tentang dunia nyata |

!!! tip "Lisensi yang belum dipastikan = belum boleh diasumsikan"
    Kolom lisensi sengaja berbunyi "belum diverifikasi". Dua dataset di tabel itu mungkin saja berlisensi longgar, tetapi proyek ini belum memeriksanya, jadi kita tidak menyatakannya. Untuk penelitian yang akan dipublikasikan, periksa lisensi dan syarat penggunaan di sumber aslinya sebelum menjadikannya data utama.

**Mengapa Breast Cancer Wisconsin (Diagnostic) dipilih:** ia punya label untuk RQ3, 569 sampel untuk RQ1, 30 fitur dengan rentang nilai yang sangat berbeda untuk RQ2, dan lisensi yang terverifikasi. Ia juga **sensitif** karena data kesehatan, dan itu justru kesempatan belajar tentang etika. Pilihan ini bukan klaim bahwa data ini yang terbaik untuk setiap penelitian.

### Data primer dan sekunder

| | Primer | Sekunder |
|---|---|---|
| Sumber | Kamu mengumpulkan sendiri | Dikumpulkan pihak lain |
| Kontrol atas pengumpulan | Penuh | Tidak ada |
| Biaya dan waktu | Tinggi | Rendah |
| Etika | Kamu bertanggung jawab atas izin dan persetujuan | Kamu bertanggung jawab atas pemakaian yang sesuai izin asal |
| Risiko khas | Sampel kecil, bias pengumpulan | Dokumentasi kurang, tujuan asli berbeda |

Proyek akhir kita memakai **data sekunder publik**. Konsekuensinya: kita tidak bisa mengubah cara data dikumpulkan, dan kita wajib jujur tentang apa yang tidak kita ketahui dari proses itu.

### Dataset publik dan sumbernya

Sumber umum: repositori seperti UCI Machine Learning Repository, platform seperti Kaggle dan OpenML, portal data pemerintah, repositori khusus bidang, dan data tambahan yang menyertai makalah. Hal yang perlu dicek pada **setiap** sumber:

1. **Siapa pembuat atau pemilik aslinya?** Salinan di platform lain bisa berbeda dari aslinya.
2. **Apa lisensinya?** Bukan lisensi platform, tetapi lisensi dataset itu.
3. **Adakah dokumentasi dan makalah pengantar?**
4. **Versi mana yang kamu pakai?** Sidik jari data membantu membuktikannya.

Pada proyek ini ada dua tingkat sumber: **file asli di UCI** (sumber yang dikutip dan menjadi acuan lisensi) dan **salinan di scikit-learn** (yang benar-benar dimuat oleh kode). Keduanya dicatat di kartu dokumentasi.

### Dokumentasi dataset dan asal-usulnya

Gunakan **kartu dokumentasi** (*dataset card*), yang terinspirasi gagasan *datasheets for datasets* (Gebru dkk., 2021). Templat minimal untuk penelitian clustering:

| Bagian | Pertanyaan yang dijawab |
|---|---|
| **Identitas** | Nama, versi, sumber asli, DOI atau URL |
| **Pembuat dan tanggal** | Siapa, kapan |
| **Lisensi** | Nama lisensi dan syarat utamanya |
| **Salinan yang dipakai** | Dari mana kamu memperolehnya, bila bukan dari sumber asli |
| **Pengumpulan** | Cara data dikumpulkan atau dihitung |
| **Isi** | Jumlah baris, fitur, tipe, label |
| **Tujuan asli** | Untuk apa data dibuat |
| **Penggunaan yang kamu lakukan** | Dan apakah berbeda dari tujuan asli |
| **Etika dan privasi** | Persetujuan, de-identifikasi, data sensitif |
| **Keterbatasan** | Yang diketahui dan yang tidak diketahui |
| **Sidik jari** | Hash data yang dipakai |

Prinsip penting: **isi "tidak dinyatakan pada sumber yang dibaca" bila memang demikian**, jangan menebak. Kolom kosong yang jujur lebih berguna daripada kolom terisi dugaan. Gagasan ini sejalan dengan prinsip FAIR (*Findable, Accessible, Interoperable, Reusable*; Wilkinson dkk., 2016): data dan metadatanya harus bisa ditemukan, diakses, dioperasikan, dan dipakai ulang.

### Lisensi dan izin pemakaian

Bila sebuah data tidak punya lisensi yang jelas, **hak cipta default berlaku**, artinya kamu tidak otomatis boleh memakainya ulang atau membagikannya. Berikut gambaran umum beberapa lisensi yang sering dijumpai:

| Lisensi | Gambaran umum |
|---|---|
| **CC0** | Pembuat melepaskan hak, bebas dipakai tanpa syarat |
| **CC BY** | Boleh dibagikan dan diadaptasi, termasuk untuk keperluan komersial, dengan syarat atribusi |
| **CC BY-SA** | Seperti CC BY, hasil turunan harus dibagikan dengan lisensi yang sama |
| **CC BY-NC** | Atribusi wajib, tidak untuk keperluan komersial |
| **CC BY-ND** | Atribusi wajib, tidak boleh membagikan hasil modifikasi |
| **Tidak ada lisensi** | Jangan mengasumsikan boleh. Hubungi pemilik atau cari data lain |

Untuk dataset kita, halaman UCI menyatakan **CC BY 4.0**. Artinya kamu boleh membagikan dan mengadaptasi data itu, asalkan mencantumkan atribusi yang layak, memberi tautan ke lisensi, dan menyatakan bila kamu mengubahnya. Karena kita menyimpan salinan dataset penelitian final di `results/`, kartu dokumentasi memuat atribusi lengkapnya.

!!! warning "Bukan nasihat hukum"
    Tabel di atas adalah ringkasan umum untuk belajar. Syarat sebenarnya ada pada teks lisensi. Untuk penelitian yang akan diterbitkan atau memakai data yang rumit, baca teks lisensinya langsung dan tanyakan pada pembimbing atau bagian hukum institusimu.

### Kualitas dan keterwakilan data

**Kualitas** (sudah dibahas di Level 2) mencakup: nilai hilang, duplikat, nilai mustahil, kolom konstan, dan outlier. Dalam konteks penelitian, tambahkan satu hal: **catat temuan dan keputusannya**. Keputusan "tidak membuang outlier" pun perlu dicatat beserta alasannya.

**Keterwakilan** adalah pertanyaan yang lebih sulit: *kesimpulan dari data ini berlaku untuk siapa atau apa?* Beberapa hal yang perlu dicek:

| Aspek | Pertanyaan |
|---|---|
| **Sumber tunggal** | Apakah semua sampel berasal dari satu lembaga atau satu proses? |
| **Keseimbangan kelas** | Seberapa besar proporsi tiap kelas? |
| **Variabel pengelompok yang tidak ada** | Apakah ada faktor penting (misalnya demografi) yang tidak tercatat? |
| **Waktu** | Kapan data dikumpulkan, dan apakah masih relevan? |
| **Seleksi** | Apakah sampel dipilih dengan cara yang bisa bias? |

Pada dataset kita, hal yang diketahui: 569 sampel, proporsi *malignant* 37,3 persen (212 dari 569). Hal yang **tidak** kita ketahui dari sumber yang dibaca: karakteristik demografi pasien, satuan fitur, serta cara sampel dipilih. Karena itu kita **tidak** menggeneralisasi hasil ke populasi pasien.

### Etika dan privasi

Data kesehatan termasuk **kategori sensitif**. Bahkan bila data publik, pertimbangkan:

1. **Persetujuan dan tinjauan etik.** Apakah subjek menyetujui pemakaian data? Apakah ada tinjauan komite etik? Bila sumber tidak menyatakannya, catat sebagai **tidak diketahui**.
2. **De-identifikasi.** Apakah data sudah tidak bisa dihubungkan ke individu? Bila tidak dinyatakan, jangan menganggap sudah.
3. **Kolom identitas.** Pastikan tidak ada kolom yang bisa mengenali individu pada salinan yang kamu pakai.
4. **Penggunaan di luar tujuan asli.** Tujuan asli dataset ini adalah klasifikasi. Kita memakainya untuk mempelajari metodologi clustering. Selisih ini dicatat.
5. **Jangan mencoba mengidentifikasi individu**, jangan menggabungkannya dengan data lain yang bisa membuka identitas, dan jangan membuat klaim yang bisa memengaruhi keputusan terhadap orang nyata.
6. **Batas klaim.** Penelitian ini tidak membuat klaim klinis.

Hasil pemeriksaan kita: dari tujuh butir, **dua butir berstatus "tidak diketahui"** (persetujuan dan tinjauan etik; status de-identifikasi), karena halaman UCI tidak membahasnya. Itu temuan penting: kita memakai data ini karena lisensinya jelas, tidak ada kolom identitas pada salinan kita, dan klaim kita terbatas pada metodologi, **bukan** karena kita tahu bahwa semua aspek etiknya beres.

### Kriteria inklusi dan eksklusi

Kriteria adalah aturan tertulis tentang apa yang masuk dan apa yang keluar. Dua alasan menuliskannya:

1. **Mencegah seleksi yang dipengaruhi hasil.** Kamu tidak boleh membuang baris karena mereka "merusak" kelompok.
2. **Membuat penelitian bisa diulang.** Orang lain bisa menerapkan aturan yang sama dan mendapat dataset yang sama.

Tuliskan kriteria **sebelum** menerapkannya, lalu laporkan alur pengurangan data (sering disebut *flow* atau *funnel*): berapa baris awal, berapa yang dikeluarkan di tiap langkah, dan berapa yang tersisa. Pada proyek kita ada empat aturan (dua inklusi, dua eksklusi), dan hasilnya adalah **nol baris dikeluarkan**. Itu hasil yang valid: kriteria ditulis tegas, lalu data memenuhinya semua.

### Menyiapkan dataset penelitian final

Dataset final adalah hasil kriteria itu. Beberapa prinsip:

1. **Pisahkan fitur dan label.** Label hanya untuk validasi (Bab 1).
2. **Jangan menyamakan skala di sini.** Penyamaan skala adalah bagian dari protokol (Bab 5), karena ia salah satu variabel yang kita uji di RQ2. Dataset final disimpan **apa adanya**.
3. **Simpan salinan beku** beserta sidik jarinya. Bila sidik jari tidak berubah setelah penyiapan, kamu tahu data tidak berubah.
4. **Jangan membuang outlier tanpa alasan tertulis.** Pada proyek kita, keputusan awalnya: nilai di luar pagar IQR **tidak dibuang** karena merupakan pengukuran yang valid pada sel nyata, dan membuangnya mengubah populasi yang kita telaah. Keputusan ini dikunci di Bab 5.

### Kesalahan umum

1. **Memilih data dulu, bertanya kemudian.**
2. **Menganggap data yang bisa diunduh boleh dipakai untuk apa saja.**
3. **Menyalin lisensi dari platform, bukan dari dataset.**
4. **Menulis kolom dokumentasi berdasarkan dugaan.**
5. **Menggeneralisasi hasil ke populasi** padahal keterwakilan tidak diketahui.
6. **Membuang baris karena "tidak cocok"** tanpa kriteria tertulis.
7. **Menyamakan skala sebelum protokol**, padahal skala adalah variabel yang akan diuji.
8. **Tidak menyimpan sidik jari data.**
9. **Mengabaikan etika karena datanya publik.**

## Mathematical Foundation

Bab ini tidak memerlukan rumus baru. Dua ukuran sederhana dipakai pada pemeriksaan kualitas:

- **Korelasi Pearson** antara dua fitur \( x \) dan \( y \): \( r = \dfrac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2 \sum (y_i-\bar y)^2}} \). Nilai mendekati 1 atau -1 berarti hubungan linear yang sangat kuat. Kita memakai nilai mutlak \( |r| \).
- **Pagar IQR** untuk menandai nilai di luar rentang wajar: \( [Q_1 - 1{,}5\,\mathrm{IQR},\; Q_3 + 1{,}5\,\mathrm{IQR}] \) dengan \( \mathrm{IQR} = Q_3 - Q_1 \). Ini sudah dibahas di [Level 2 Bab 7](../data-exploration-and-preprocessing/07-outlier-detection-and-handling.md).

## Python Implementation

Skrip lengkapnya ada di `examples/level-7/04_dataset_selection_and_preparation.py`, dan notebook-nya di `notebooks/level-7/04-dataset-selection-and-preparation.ipynb`. **Setiap potongan kode diikuti penjelasannya.**

**Konteks masalah:** kita perlu mendokumentasikan dataset, memastikan salinan yang kita muat cocok dengan dokumentasinya, memeriksa kualitas, dan menyiapkan dataset final yang tercatat.

**Dataset:** Breast Cancer Wisconsin (Diagnostic), UCI, CC BY 4.0. Bukan alat diagnosis.

**Pustaka:** NumPy, pandas, serta `json` dari pustaka standar.

### Bagian A — Siapkan alat

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:setup"
```

**Penjelasan:** `rs.load_wdbc()` memuat fitur dan diagnosis (Bab 1). `RESULTS` adalah folder hasil. Baris cetak memastikan 569 baris fitur dan 569 label termuat.

### Bagian B — Kartu dokumentasi dataset

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:datacard"
```

**Penjelasan:**

- `UNKNOWN` adalah satu kalimat untuk hal yang tidak diketahui, dipakai di tiga kolom: persetujuan etika, demografi pasien, dan satuan fitur. Memakai konstanta menjamin penulisan yang konsisten.
- `card` adalah dictionary: kunci berupa bagian kartu, nilai berupa isinya. Perhatikan frasa "(menurut halaman UCI)" dan "(menurut scikit-learn)". **Setiap fakta diberi sumbernya**, supaya pembaca tahu dari mana asalnya.
- Fitur dan label dirujuk ke scikit-learn karena deskripsi fiturnya (mean, standard error, worst) tercantum di dokumentasi scikit-learn, sedangkan lisensi, pembuat, dan tanggal donasi berasal dari halaman UCI.
- Perulangan `for key, value in card.items()` mencetak semuanya. `{key:34s}` memberi lebar 34 karakter.

### Bagian C — Mencocokkan dokumentasi dengan data

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:verify"
```

**Penjelasan:**

- `documented` berisi angka dari dokumentasi (deskripsi scikit-learn): jumlah sampel dan fitur, tidak ada nilai hilang, jumlah tiap kelas, serta nilai minimum dan maksimum dua fitur.
- `observed` berisi angka yang **dihitung dari data yang dimuat**. `diagnosis.value_counts()` menghitung tiap kelas, `X_all["mean radius"].min()` mengambil nilai terkecil sebuah kolom, dan `round(..., 3)` membulatkan agar bisa dibandingkan dengan angka dokumentasi.
- `pd.DataFrame({...})` menyusun dua dictionary menjadi dua kolom bersebelahan.
- `np.where(kondisi, "cocok", "BERBEDA")` memberi "cocok" pada baris yang kedua kolomnya sama.
- `(check["status"] == "cocok").all()` bernilai `True` hanya bila **semua** baris cocok.

!!! note "Pemeriksaan ini bukan perbandingan independen"
    Dokumentasi yang kita pakai adalah deskripsi scikit-learn untuk salinan yang sama. Jadi kecocokan ini menunjukkan bahwa **salinan konsisten dengan dokumentasinya**, bukan bahwa ia identik dengan file asli di UCI. Pemeriksaan independen membutuhkan unduhan file UCI dan perbandingan hash.

### Bagian D — Pemeriksaan kualitas

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:quality"
```

**Penjelasan:**

- `X_all.corr().abs()` menghitung korelasi antar semua pasangan fitur dalam nilai mutlak. `np.triu(..., k=1)` membuat penanda segitiga atas di atas diagonal, agar tiap pasangan hanya dihitung sekali dan korelasi fitur dengan dirinya sendiri dibuang. `.where(...)` mengganti nilai di luar segitiga itu dengan kosong. `.stack()` mengubah tabel menjadi daftar pasangan, dan `.sort_values(ascending=False)` mengurutkannya dari yang terbesar.
- `q1`, `q3`, dan `iqr` menghitung kuartil pertama, kuartil ketiga, dan rentang antarkuartil tiap fitur.
- `(X_all < q1 - 1.5 * iqr) | (X_all > q3 + 1.5 * iqr)` menandai nilai di luar pagar. Tanda `|` berarti "atau". `.sum()` menghitung banyaknya per fitur.
- `quality` merangkum enam angka: baris duplikat (`duplicated().sum()`), kolom konstan (`nunique() <= 1`), nilai negatif, pasangan fitur berkorelasi di atas 0,95, fitur yang miring kuat (`skew()` mutlak di atas 1), dan total nilai di luar pagar.

### Bagian E — Kriteria inklusi dan eksklusi

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:criteria"
```

**Penjelasan:**

- `positive_by_definition` memilih nama kolom yang mengandung kata radius, texture, perimeter, atau area. Ukuran-ukuran ini secara definisi harus positif.
- `rules` adalah daftar pasangan (nama aturan, fungsi). Tiap fungsi `lambda f, d: ...` menerima fitur `f` dan diagnosis `d`, lalu mengembalikan deret `True`/`False`: `True` untuk baris yang **lolos**. Aturan I1 memakai `~f.isna().any(axis=1)`: `~` membalik, jadi baris lolos bila **tidak ada** nilai hilang pada barisnya.
- `keep = pd.Series(True, index=X_all.index)` memulai dengan semua baris lolos.
- Dalam perulangan, `removed = int((keep & ~passed).sum())` menghitung baris yang **masih lolos sebelumnya tetapi gagal aturan ini**. `keep &= passed` memperbarui daftar baris yang lolos. Hasilnya dicatat di `funnel` sebagai tabel alur pengurangan.

### Bagian F — Daftar periksa etika dan privasi

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:ethics"
```

**Penjelasan:** tabel berisi tiga kolom: pemeriksaan, status, dan dasar. Status kolom identitas **dihitung dengan kode** dari nama kolom (`any(c.lower() in (...) for c in X_all.columns)`). Status lain berasal dari halaman UCI dan dari keputusan kita, dan kolom `dasar` mencatat sumbernya. `(ethics["status"] == "Tidak diketahui").sum()` menghitung butir yang tidak diketahui, supaya ketidaktahuan terlihat sebagai angka dan tidak tersembunyi.

!!! warning "Pemeriksaan identitas hanya berdasarkan nama kolom"
    Kode hanya memeriksa **nama** kolom. Nama kolom yang tidak mencurigakan tidak menjamin tidak ada data yang bisa mengenali individu. Ini pemeriksaan minimal, bukan jaminan de-identifikasi.

### Bagian G — Dataset penelitian final

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:prepare"
```

**Penjelasan:** `X_all.loc[keep]` memilih baris yang lolos semua aturan, dan `.reset_index(drop=True)` memberi nomor baris baru berurutan. Fitur dan diagnosis dipilih dengan cara yang sama agar tetap sejajar. Lalu dua sidik jari dicetak dan dibandingkan: `!=` bernilai `True` bila data berubah.

### Bagian H — Menyimpan kartu, laporan, dan dataset

```python
--8<-- "level-7/04_dataset_selection_and_preparation.py:save"
```

**Penjelasan:** kartu diperkaya dengan sidik jari final, jumlah sampel final, jumlah baris dikeluarkan, dan daftar kriteria, lalu disimpan sebagai JSON. Hasil pencocokan, alur inklusi, dan daftar periksa etika disimpan sebagai CSV. `final_features.assign(diagnosis=final_diagnosis)` menambahkan kolom label ke fitur sebagai salinan beku `04_research_dataset.csv`. `reset_index(names="item")` mengubah indeks (nama pemeriksaan) menjadi kolom biasa sebelum disimpan.

## Code Explanation

| Bagian kode | Peran |
|---|---|
| `card = {...}` | Kartu dokumentasi dengan sumber tiap fakta |
| `UNKNOWN` | Penanda jujur untuk hal yang tidak diketahui |
| `documented` vs `observed` | Konsistensi salinan dengan dokumentasinya |
| `corr().abs()` dan `np.triu` | Pasangan fitur berkorelasi tanpa duplikasi |
| `rules = [(nama, lambda ...)]` | Kriteria sebagai kode yang bisa diulang |
| `keep &= passed` | Menumpuk aturan dan menghitung alur pengurangan |
| `ethics` | Daftar periksa yang menghitung hal yang tidak diketahui |
| `rs.dataset_fingerprint(...)` | Membuktikan data berubah atau tidak |

## How to Run

Dari folder utama proyek (setelah mengaktifkan lingkungan virtual):

```powershell
pip install -r requirements-notebooks.txt
python examples/level-7/04_dataset_selection_and_preparation.py
```

Skrip mencetak output dan menyimpan lima berkas di `examples/level-7/results/`, termasuk salinan beku dataset (`04_research_dataset.csv`, sekitar 125 KB). Notebook interaktifnya:

```powershell
jupyter notebook notebooks/level-7/04-dataset-selection-and-preparation.ipynb
```

Notebook memuat Bagian A sampai H, ditambah tiga bagian **Praktik**: menambah kriteria eksklusi sendiri, mengisi kartu untuk dataset lain, dan memeriksa keterwakilan.

Output di bawah berasal dari eksekusi nyata dengan Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, dan scikit-learn 1.9.0.

## Expected Output

```text
--8<-- "level-7/outputs/04.txt"
```

### Interpretasi output

**1. Kartu dokumentasi.** Sumber, DOI, pembuat, tanggal donasi, dan lisensi (CC BY 4.0) berasal dari halaman UCI. Fitur dan label berasal dari scikit-learn dan UCI. **Tiga hal tidak dinyatakan** pada sumber yang dibaca: persetujuan atau tinjauan etik, demografi pasien, dan satuan fitur.

**2. Dokumentasi cocok dengan data.** Kesembilan butir cocok: 569 sampel, 30 fitur, tanpa nilai hilang, 212 *malignant*, 357 *benign*, serta minimum dan maksimum `mean radius` (6,981 dan 28,11) dan `mean area` (143,5 dan 2501,0). Seperti dicatat di atas, ini konsistensi dengan dokumentasi scikit-learn, bukan perbandingan dengan file asli UCI.

**3. Kualitas.**

| Pemeriksaan | Hasil |
|---|---|
| Baris duplikat | 0 |
| Kolom konstan | 0 |
| Nilai negatif | 0 |
| Pasangan fitur dengan \|r\| > 0,95 | **15** |
| Fitur miring kuat (\|skew\| > 1) | **22 dari 30** |
| Total nilai di luar pagar IQR | **608** |

Pasangan paling berkorelasi: `mean radius` dan `mean perimeter` (0,998), disusul `worst radius` dan `worst perimeter` (0,994). Banyak fitur ukuran saling berlebihan. Fitur dengan nilai luar pagar terbanyak adalah `area error` (65), `radius error` (38), dan `perimeter error` (38).

**4. Alur inklusi.** Data awal 569 baris, dan tiap aturan (I1, I2, E1, E2) mengeluarkan **0 baris**. Tersisa 569. Itu hasil yang valid: kriteria ditulis tegas dan data memenuhi semuanya, jadi tidak ada baris yang dibuang.

**5. Etika.** Tujuh butir pemeriksaan: **dua berstatus "tidak diketahui"** (persetujuan atau tinjauan etik, dan de-identifikasi). Tidak ada kolom identitas pada salinan yang dipakai. Lisensi mengizinkan pemakaian ulang dengan atribusi. Tujuan kita (metodologi clustering) **berbeda** dari tujuan asli (classification), dan perbedaan itu dicatat.

**6. Dataset final.** 569 baris, 30 fitur, 357 *benign* dan 212 *malignant*. Sidik jari awal dan final sama (`6b202a2072f9`, sama dengan Bab 1), dan `Data berubah: False`.

!!! warning "Batas kesimpulan"
    Pemeriksaan kualitas menunjukkan data bersih secara teknis, tetapi **tidak** menjawab apakah data itu mewakili populasi tertentu. Kita tidak tahu demografi pasien, kapan dan bagaimana sampel dipilih, atau satuan fitur. Maka hasil penelitian ini hanya berlaku untuk **salinan data ini**, dan klaim tentang populasi pasien tidak dibuat. Banyaknya fitur yang saling berkorelasi dan miring juga akan mempengaruhi hasil clustering, dan kita mengujinya di bab berikutnya, bukan mengasumsikannya.

## Practical Examples

**Memilih data untuk skripsi.** Tulis dulu tiga kebutuhan dari pertanyaanmu (misalnya label, ukuran, fitur). Cari tiga kandidat, isi kartu dokumentasi untuk masing-masing, lalu pilih yang kebutuhannya terpenuhi dan lisensinya jelas.

**Menerima data dari pihak lain.** Bila rekan atau instansi memberimu data, tanyakan hal yang di kartu bertanda "tidak diketahui": persetujuan, de-identifikasi, dan batas pemakaian. Minta jawabannya tertulis.

**Menulis bagian "Data" pada makalah.** Kartu dokumentasi hampir langsung menjadi bagian itu: sumber, lisensi, ukuran, kriteria, alur pengurangan, dan keterbatasan.

## Hands-on Exercises

Semua angka di jawaban berasal dari eksekusi nyata, kecuali disebut lain.

1. Dari output, berapa baris yang dikeluarkan oleh keempat kriteria, dan apakah sidik jari data berubah? Apa artinya?
2. Pasangan fitur mana yang paling berkorelasi? Apa implikasinya bagi jarak Euclidean pada clustering dengan semua 30 fitur?
3. Tambahkan kriteria eksklusi E3: buang baris dengan `worst area` lebih dari 4000. Berapa baris yang keluar, dari kelas apa, dan apakah sidik jari berubah?
4. Mengapa Breast Cancer Wisconsin dipilih dan Mall Customers tidak, untuk proyek penelitian ini?
5. Mengapa "dokumentasi cocok dengan data" belum membuktikan salinan scikit-learn identik dengan file asli UCI? Bagaimana membuktikannya?
6. Dua butir etika berstatus "tidak diketahui". Mengapa itu tidak berarti data tidak boleh dipakai, dan apa yang harus dilakukan dengan butir itu di laporan?

??? question "Jawaban"
    Nomor 1 sampai 3 memakai output dan penghitungan nyata.

    1. **0 baris** dikeluarkan oleh keempat kriteria dan sidik jari **tidak berubah** (`6b202a2072f9`). Artinya data awal sudah memenuhi semua kriteria. Kriteria tetap perlu ditulis agar orang lain tahu aturannya.
    2. `mean radius` dan `mean perimeter` (|r| = 0,998). Ada 15 pasangan dengan |r| > 0,95. Pada jarak Euclidean, fitur yang saling berlebihan membuat satu aspek (di sini ukuran) memberi sumbangan jarak lebih besar daripada yang tampak dari jumlah fitur. Ini yang perlu dipertimbangkan saat memilih fitur, dan diuji, bukan diasumsikan.
    3. **1 baris** dikeluarkan, dari kelas *malignant*. Tersisa 568 baris dan sidik jari berubah menjadi `bf3dbe425b4f`. Satu baris itu adalah nilai ekstrem yang valid. Membuangnya mengubah data dan harus dicatat serta dijustifikasi.
    4. Breast Cancer Wisconsin punya label untuk RQ3 dan lisensi yang terverifikasi (CC BY 4.0). Mall Customers tidak punya label, dan lisensinya belum dipastikan di proyek ini (Level 2 Bab 1 menyarankan memeriksanya di Kaggle). Mall Customers tetap cocok untuk belajar di Level 2–6.
    5. Dokumentasi yang dipakai adalah deskripsi scikit-learn tentang salinan yang sama, sehingga cocok-tidaknya tidak independen. Pembuktiannya: unduh file asli dari UCI, muat dengan cara yang sama, lalu bandingkan sidik jari atau isi per baris.
    6. "Tidak diketahui" berarti informasinya tidak tersedia pada sumber yang dibaca, bukan bahwa ada pelanggaran. Data tetap boleh dipakai bila lisensinya mengizinkan dan klaim dibatasi, tetapi ketidaktahuan itu **wajib dinyatakan** di bagian data dan keterbatasan laporan. Bila memungkinkan, hubungi pembuat atau cari dokumentasi tambahan.

## Troubleshooting

### Masalah teknis

| Masalah | Penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: _research` | Skrip dijalankan dari tempat yang salah | Jalankan dari folder utama proyek |
| Hasil "BERBEDA" pada pencocokan | Versi scikit-learn berbeda atau data berubah | Periksa versi dan sidik jari |
| `KeyError: 'malignant'` | Label dipetakan terbalik | Di dataset ini 0 = *malignant*, 1 = *benign* (Bab 1) |
| Berkas CSV besar | Salinan beku dataset ikut disimpan | Normal (sekitar 125 KB) |

### Kesalahan umum

1. **Menganggap "cocok dengan dokumentasi" sama dengan "identik dengan sumber asli".**
2. **Mengisi kartu dokumentasi dengan dugaan.**
3. **Menyembunyikan butir etika yang tidak diketahui.**
4. **Menyamakan skala sebelum protokol ditetapkan.**
5. **Membuang baris tanpa kriteria tertulis.**
6. **Menganggap data bersih berarti data representatif.**

## Summary

- **Pilih data setelah punya pertanyaan.** Kebutuhan RQ1–RQ3 (sampel, fitur, label, lisensi, dokumentasi) menentukan pilihan.
- **Data publik tidak otomatis bebas dipakai.** Periksa lisensi dataset aslinya. Dataset ini berlisensi **CC BY 4.0** (atribusi wajib), sedangkan Wine dan Mall Customers belum diverifikasi di proyek ini.
- **Kartu dokumentasi** mencatat sumber tiap fakta, dan menandai dengan jujur hal yang tidak dinyatakan: persetujuan etika, demografi pasien, dan satuan fitur.
- **Kualitas:** tanpa duplikat, nilai hilang, atau nilai negatif; tetapi 15 pasangan fitur berkorelasi di atas 0,95, 22 dari 30 fitur miring kuat, dan 608 nilai berada di luar pagar IQR.
- **Etika:** dua dari tujuh butir "tidak diketahui". Ketidaktahuan itu dilaporkan, dan klaim dibatasi pada metodologi.
- **Kriteria inklusi dan eksklusi** ditulis sebelum diterapkan. Pada data ini keempat aturan mengeluarkan **0 baris** (569 tersisa) dan sidik jari tetap `6b202a2072f9`.
- **Dataset final** disimpan apa adanya, tanpa penyamaan skala, karena skala adalah variabel yang akan diuji.

**Bab berikutnya:** Bab 5 membahas **metodologi penelitian dan protokol eksperimen**: variabel, baseline, algoritma, hyperparameter, metrik, prosedur perbandingan, dan pencatatan konfigurasi.

## References

- Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1993). *Breast Cancer Wisconsin (Diagnostic)* [Dataset]. UCI Machine Learning Repository. [doi.org/10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B). Lisensi CC BY 4.0 menurut halaman dataset.
- Street, W. N., Wolberg, W. H., & Mangasarian, O. L. (1993). Nuclear feature extraction for breast tumor diagnosis. *Electronic Imaging* (artikel pengantar dataset yang dicantumkan UCI).
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92. [doi.org/10.1145/3458723](https://doi.org/10.1145/3458723)
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., dkk. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. [doi.org/10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
- Scikit-learn documentation: [*Toy datasets, Breast cancer Wisconsin (diagnostic) dataset*](https://scikit-learn.org/stable/datasets/toy_dataset.html).
- Creative Commons. *Attribution 4.0 International (CC BY 4.0)*. [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/)
