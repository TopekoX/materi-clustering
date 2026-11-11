# Bab 10 — Final Clustering Research Project

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menyatukan seluruh tahap penelitian clustering (Bab 1 sampai 9) menjadi satu proyek yang utuh.
- [x] Menyusun laporan proyek dengan 17 bagian, masing-masing berlabel status isi.
- [x] Membedakan **ilustrasi didaktik**, **temuan eksperimen**, **eksploratori**, **dokumentasi**, dan **rencana**.
- [x] Menutup celah yang tercatat di bab sebelumnya (misalnya pustaka untuk RQ2) dengan sumber yang diverifikasi.
- [x] Menguji dugaan dari bab sebelumnya dengan analisis lanjutan yang berlabel eksploratori.
- [x] Menjalankan QA akhir dan membaca hasilnya dengan jujur, termasuk peringatan yang tersisa.
- [x] Merumuskan kesimpulan yang dibatasi dan pekerjaan lanjutan yang bisa diuji.
- [x] Menjelaskan apa yang membuat proyek ini penelitian, bukan tutorial.

## Introduction

Sembilan bab terakhir membangun satu proyek sepotong demi sepotong: rumusan masalah, pustaka, data, protokol, eksperimen, hasil, naskah, dan paket reproduksi. Bab ini merangkai semuanya.

Pertanyaan yang mengatur bab ini: **apa bedanya proyek ini dengan tutorial yang menjalankan K-Means pada dataset publik?** Jawabannya ada pada beberapa kebiasaan yang kamu pelajari dan kini terlihat bekerja bersama:

1. **Pertanyaan lebih dulu**, bukan algoritma (Bab 2).
2. **Pustaka ditelaah** dan keterbatasan bacaannya dicatat (Bab 3 dan bab ini).
3. **Data dipilih dan didokumentasikan** dengan lisensi, atribusi, dan ketidaktahuan yang dinyatakan (Bab 4).
4. **Protokol ditulis dan dikunci sebelum eksperimen**, termasuk pengungkapan hal yang sudah dilihat (Bab 5).
5. **Implementasi mengikuti protokol**, dan hasil nol dilaporkan apa adanya (Bab 6).
6. **Hasil, tafsiran, dan keterbatasan dipisahkan**, dengan ketidakpastian ditampilkan (Bab 7).
7. **Naskah dirakit dari fakta**, bukan dikarang (Bab 8).
8. **Semuanya diuji ulang** dan dikemas (Bab 9).

Bab ini menambahkan satu hal lagi yang sangat penting bagi proyek yang mengajarkan: **pembedaan yang tegas antara contoh untuk belajar dan temuan yang sebenarnya**. Banyak angka di Level 7 muncul sebagai demonstrasi (misalnya Bab 1) dan banyak yang hasil eksperimen terkunci (Bab 6). Pembaca berhak tahu mana yang mana. Karena itu setiap bagian laporan akhir memiliki label.

!!! note "Prasyarat"
    Seluruh bab Level 7. Skrip bab ini membaca keluaran Bab 2 sampai 9, jadi **jalankan skrip Bab 2 sampai 9 lebih dulu**. Bab ini tidak menjalankan ulang eksperimen utama (itu sudah diuji keterulangannya di Bab 9) dan tidak mengubah protokol terkunci.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Final project** | Penelitian utuh dari pertanyaan sampai paket reproduksi |
| **Status label** | Penanda jenis isi sebuah bagian atau item |
| **ILUSTRASI DIDAKTIK** | Contoh untuk belajar. Angkanya bukan temuan penelitian |
| **TEMUAN EKSPERIMEN** | Hasil analisis yang ditetapkan di protokol terkunci |
| **EKSPLORATORI** | Analisis di luar protokol, dilakukan setelah melihat data |
| **RENCANA DAN PROTOKOL** | Rancangan yang ditetapkan sebelum eksperimen |
| **DOKUMENTASI** | Catatan proses, data, kode, dan reproduksibilitas |
| **TINJAUAN PUSTAKA TERBATAS** | Telaah yang dibatasi tingkat bacaan (abstrak atau ringkasan) |
| **Follow-up analysis** | Analisis lanjutan yang menguji dugaan dari bab sebelumnya |
| **Final QA** | Pemeriksaan akhir terhadap kelengkapan, keterlacakan, dan kejujuran laporan |
| **Future work** | Pekerjaan lanjutan yang bisa diuji, bukan janji yang tidak jelas |

## Detailed Explanation

### Tujuh belas bagian proyek dan asalnya

Laporan akhir memiliki tujuh belas bagian. Setiap bagian **dirakit dari berkas hasil bab sebelumnya**, tidak ditulis ulang.

| No | Bagian | Berasal dari | Label status isi |
|---|---|---|---|
| 1 | Judul penelitian | Bab 8 | Dokumentasi |
| 2 | Latar belakang dan masalah | Bab 2 | Rencana dan protokol |
| 3 | Tujuan dan pertanyaan | Bab 2 | Rencana dan protokol |
| 4 | Matriks tinjauan pustaka | Bab 3 dan 10 | Tinjauan pustaka terbatas |
| 5 | Celah riset dan kontribusi | Bab 3 dan 10 | Tinjauan pustaka terbatas |
| 6 | Pemilihan dan deskripsi dataset | Bab 4 | Dokumentasi |
| 7 | Metodologi | Bab 5 | Rencana dan protokol |
| 8 | Praproses data | Bab 5 dan 6 | Rencana dan protokol |
| 9 | Implementasi clustering | Bab 5 dan 6 | Rencana dan protokol |
| 10 | Desain eksperimen | Bab 5 | Rencana dan protokol |
| 11 | Evaluasi | Bab 5 | Rencana dan protokol |
| 12 | Visualisasi hasil | Bab 6 dan 7 | Temuan eksperimen |
| 13 | Profil kelompok | Bab 6 dan 7 | Temuan eksperimen |
| 14 | Hasil dan pembahasan | Bab 7 dan 10 | Temuan eksperimen |
| 15 | Kesimpulan | Bab 6 dan 7 | Temuan eksperimen |
| 16 | Keterbatasan dan pekerjaan lanjutan | Bab 7 dan 10 | Keterbatasan dan rencana lanjutan |
| 17 | Dokumentasi reproduksibilitas | Bab 9 | Dokumentasi |

### Mengapa label status isi

Pada penelitian biasa, sebagian besar isi adalah temuan. Pada proyek **pembelajaran** seperti ini, pembaca melihat banyak angka dari banyak sumber, dan mudah menyalahartikan contoh sebagai temuan. Contoh nyata di proyek ini:

| Item | Label | Mengapa penting |
|---|---|---|
| Demonstrasi tiga pertanyaan riset (Bab 1: ARI 0,493; 0,066; 0,654) | **Ilustrasi didaktik** | Fitur dikelompokkan sembarang untuk mengajar. Bukan hasil seleksi fitur yang dijustifikasi |
| Contoh pertanyaan baik dan buruk (Bab 2) | **Ilustrasi didaktik** | Contoh kalimat, bukan hasil |
| RQ1, RQ2, RQ3 (Bab 6) | **Temuan eksperimen** | Dihasilkan protokol terkunci |
| Bootstrap, pangsa varians (Bab 7) | **Eksploratori** | Ditambahkan setelah melihat hasil |
| Uji dominasi fitur (bab ini) | **Eksploratori** | Menguji dugaan setelah protokol |

Angka Bab 1 (ARI 0,654 untuk Q3) kebetulan sama dengan ARI K-Means pada RQ3. Itu bukan kebetulan yang bermakna: keduanya K-Means, K = 2, ke-30 fitur, `StandardScaler`, seed 42. Tetapi Bab 1 **bukan** temuan: ia dijalankan sebelum protokol dan dipakai mengajar. Pengungkapan di Bab 5 mencatatnya.

### Menutup celah dari bab sebelumnya

Ada tiga hal yang dicatat sebagai peringatan di Bab 3 dan Bab 8. Bab ini menutup sebagian.

| Peringatan | Tindakan di Bab 10 | Hasil |
|---|---|---|
| RQ2 tidak punya pustaka | Mencari dan memverifikasi dua sumber tentang standardisasi variabel dalam analisis klaster | RQ2 kini punya 2 sumber |
| Dugaan Bab 7: dominasi fitur berskala besar belum diuji | Uji langsung dengan K-Means pada subset fitur | Dugaan didukung pada dataset ini |
| Sumber hanya dibaca abstrak atau ringkasan | **Tidak** bisa ditutup oleh skrip | Tetap peringatan: 0 dari 7 dibaca penuh |

!!! warning "Sumber baru hanya dibaca ringkasannya"
    Kedua sumber baru (Milligan & Cooper, 1988; Steinley, 2004) diverifikasi keberadaannya lewat pencarian web, tetapi halaman penerbit membutuhkan akses berlangganan sehingga **teks lengkap dan abstrak asli tidak dibaca**. Matriks mencatat `dibaca = ringkasan hasil pencarian` dan sel "—" untuk yang tidak tercantum. Pembahasan yang memakainya ditulis dengan kata "sejalan dengan" dan menyebut batas bacaan itu.

### Uji lanjutan dugaan dominasi fitur

Di Bab 7 kita menulis **dugaan** (I4): K-Means tanpa skala didominasi fitur berskala besar, dengan bukti pendukung berupa pangsa varians dua fitur teratas (99,1 persen). Pangsa varians mendukung tetapi tidak menguji. Uji langsungnya: bandingkan pengelompokan K-Means tanpa skala pada ke-30 fitur dengan pengelompokan K-Means yang hanya memakai satu atau dua fitur terbesar.

| Pembandingan | ARI |
|---|---|
| Semua fitur vs hanya `worst area` | **1,000** |
| Semua fitur vs `worst area` dan `mean area` | 0,992 |
| Semua fitur vs tanpa kedua fitur area | 0,849 |

ARI 1,000 berarti **pengelompokan K-Means tanpa skala pada ke-30 fitur identik** dengan pengelompokan yang hanya memakai `worst area`. Dugaan I4 didukung pada dataset ini. ARI 0,849 saat kedua fitur area dibuang menunjukkan pengelompokan berubah, karena fitur berskala besar lain (misalnya keliling) mengambil alih.

Batas kesimpulan: ini analisis **eksploratori** (tidak ada di protokol), pada **satu dataset**, dan tidak menunjukkan hal yang sama pada data lain. Ia juga tidak mengatakan bahwa `worst area` "penting" secara ilmiah, hanya bahwa pada skala asli ia mendominasi jarak.

### Kesimpulan yang dibatasi

Kesimpulan menjawab tiap pertanyaan dengan **jawaban yang dibatasi**:

| Pertanyaan | Jawaban yang dibatasi |
|---|---|
| **RQ1** | Pada dataset ini K-Means (K = 2, data terstandarisasi) tampak konsisten terhadap seed (ARI 0,981) dan subsampel (0,964; minimum 0,871) |
| **RQ2** | Cara menyamakan skala mengubah pengelompokan: ARI 0,496 tanpa skala dan 0,896 dengan MinMaxScaler, di bawah ambang 0,95 |
| **RQ3** | Pengelompokan cukup selaras dengan diagnosis (ARI 0,575 sampai 0,774); peringkat algoritma berbeda antar jenis metrik; selisih antar-algoritma tidak jelas melampaui ketidakpastian sampel; DBSCAN tanpa konfigurasi valid |

Perhatikan apa yang **tidak** ada: "algoritma terbaik", "kelompok ganas", "metode ini bisa mendiagnosis", atau "penyamaan skala selalu penting".

### Pekerjaan lanjutan yang bisa diuji

Pekerjaan lanjutan yang baik menyebut **cara mengujinya**, bukan sekadar "perlu penelitian lebih lanjut".

| Pekerjaan lanjutan | Cara mengujinya |
|---|---|
| Uji dugaan kepadatan seragam pada DBSCAN | Bandingkan sebaran jarak tetangga terdekat; coba grid yang ditetapkan lewat amendment |
| Baca teks lengkap ketujuh sumber | Isi kolom keterbatasan dan perbarui pembahasan pustaka |
| Uji pada dataset lain (*replicability*) | Terapkan protokol yang sama pada dataset berlisensi jelas |
| Seleksi fitur untuk mengurangi redundansi | Bandingkan dengan seluruh fitur memakai ARI antar-pengelompokan |
| Tinjauan pustaka sistematis | Tetapkan kueri dan kriteria inklusi lebih dulu, lalu laporkan alur seleksi |

### QA akhir

QA akhir memeriksa laporan, bukan hanya menyatakan "selesai". Butir yang diperiksa mencakup kelengkapan 17 bagian, label di tiap bagian, keterlacakan angka, kata berlebihan, hash protokol dan amendment, kecocokan eksekusi, keberadaan sumber dan gambar, label eksploratori, cakupan pustaka tiap pertanyaan, dan pemisahan ilustrasi dari temuan. Dua butir dijadikan **peringatan** (bukan kegagalan): sumber dibaca penuh, dan status paket reproduksi dari Bab 9.

QA ini menangkap cacat nyata saat bab ini disusun: dua angka (1,43 dan 1,42, ukuran inti sel kedua dan ketiga) muncul di laporan tanpa terdaftar di registri fakta. Perbaikannya: mendaftarkan angka itu dari berkas sumber dan mengutipnya lewat registri. Pelajaran yang sama dengan Bab 7: angka di teks harus bisa dilacak, dan pemeriksa menemukan pelanggarannya pada tulisan kita sendiri.

### Apa yang membuat ini penelitian

Proyek ini **bukan** penelitian dengan kebaruan ilmiah, dan tidak mengklaimnya. Ia penelitian dalam arti prosesnya: pertanyaan yang jelas, data yang didokumentasikan, protokol yang ditetapkan sebelumnya, hasil yang jujur termasuk hasil nol, ketidakpastian yang ditampilkan, keterbatasan yang spesifik, dan paket yang bisa diulang. Kontribusinya **didaktik dan metodologis**: mendemonstrasikan protokol penelitian clustering yang bisa diulang.

### Kesalahan umum pada proyek akhir

1. **Mencampur contoh dan temuan** tanpa label.
2. **Mengubah protokol agar hasil tampak lebih baik.**
3. **Menutup peringatan dengan menghapusnya**, bukan membereskannya.
4. **Menulis kesimpulan yang melampaui data.**
5. **Menganggap uji lanjutan eksploratori sebagai analisis terencana.**
6. **Menyatakan sumber "dibaca" padahal hanya ringkasannya.**
7. **Pekerjaan lanjutan yang tidak bisa diuji.**
8. **Menyembunyikan hasil nol.**
9. **Tidak menjalankan QA akhir**, atau mengabaikan butirnya.

## Mathematical Foundation

Bab ini tidak memerlukan rumus baru. Dua ukuran yang dipakai sudah dibahas: ARI (Bab 1) dan Silhouette serta metrik lain (Bab 6). Satu-satunya perhitungan baru adalah **ARI antara dua pengelompokan K-Means** untuk menguji dominasi fitur: nilai 1 berarti dua pengelompokan identik (hingga pertukaran nomor kelompok), dan nilai yang lebih rendah berarti berbeda.

## Python Implementation

Skrip lengkapnya ada di `examples/level-7/10_final_research_project.py`, dan notebook-nya di `notebooks/level-7/10-final-clustering-research-project.ipynb`. **Setiap potongan kode diikuti penjelasannya.**

**Konteks masalah:** menyatukan hasil Bab 1 sampai 9 menjadi laporan proyek akhir yang jujur dan bisa diperiksa.

**Penting:** skrip **tidak** menjalankan ulang eksperimen utama dan **tidak** mengubah protokol terkunci. Satu-satunya perhitungan baru adalah uji eksploratori lanjutan (empat K-Means).

**Pustaka:** NumPy, pandas, scikit-learn, serta `hashlib`, `json`, dan `re` dari pustaka standar. **Jalankan skrip Bab 2 sampai 9 lebih dulu.**

### Bagian A — Siapkan alat dan periksa protokol terkunci

```python
--8<-- "level-7/10_final_research_project.py:setup"
```

```text title="Output"
--8<-- "level-7/outputs/10/setup.txt"
```

**Penjelasan:** seperti di Bab 6, skrip menghitung ulang hash protokol dan **berhenti** (`raise SystemExit`) bila berbeda dari yang terkunci. Lalu skrip membaca rumusan masalah, kartu data, manifest eksekusi Bab 6, klarifikasi, fakta dan buku bukti Bab 7, matriks pustaka Bab 3, profil per ukuran, daftar periksa paket Bab 9, dan judul dari kerangka naskah Bab 8 (`splitlines()[0].lstrip("# ")` mengambil baris pertama dan membuang tanda judul Markdown). Tidak ada angka yang diketik ulang.

### Bagian B — Melengkapi tinjauan pustaka untuk RQ2

```python
--8<-- "level-7/10_final_research_project.py:literature"
```

```text title="Output"
--8<-- "level-7/outputs/10/literature.txt"
```

**Penjelasan:**

- `new_rows` adalah tabel dua baris untuk sumber baru, dengan kolom yang sama seperti matriks Bab 3. Isi hanya yang tercantum pada ringkasan hasil pencarian; sisanya `"—"`. Kolom `dibaca` mencatat **"ringkasan hasil pencarian"**.
- `pd.concat([literature, new_rows])` menggabungkan matriks lama dan baru (7 baris).
- `needs` memetakan tiap pertanyaan ke topik pustaka. `coverage` menghitung jumlah sumber per topik: RQ1 1, RQ2 **2**, RQ3 1.
- `read_full` menghitung sumber yang dibaca penuh (0).
- `final_gap` membangun pernyataan celah dengan **jumlah sumber dari data** (`len(final_literature)`), sehingga ia ikut berubah menjadi 7.

### Bagian C — Uji eksploratori lanjutan

```python
--8<-- "level-7/10_final_research_project.py:followup"
```

```text title="Output"
--8<-- "level-7/outputs/10/followup.txt"
```

**Penjelasan:** `kmeans = lambda data: ...` adalah fungsi pendek yang menjalankan K-Means (K = 2, `n_init=10`, seed 42). Kita memakainya empat kali: pada seluruh fitur tanpa skala (`raw_all`), hanya `worst area` (`X_df[["worst area"]]`), dua fitur area, dan seluruh fitur **kecuali** dua fitur area (`X_df.drop(columns=[...])`). `adjusted_rand_score(raw_all, ...)` membandingkan tiap pengelompokan dengan `raw_all`. Hasilnya disimpan di `followup`. Pengelompokan ini **tidak ada di protokol**, jadi semua keluarannya akan diberi label eksploratori.

### Bagian D — Peta status isi

```python
--8<-- "level-7/10_final_research_project.py:statusmap"
```

```text title="Output"
--8<-- "level-7/outputs/10/statusmap.txt"
```

**Penjelasan:** `status_items` mendaftar 15 item penting dengan **bab asal, label status, dan berkas sumber**. `status_map["sumber_ada"]` memeriksa bahwa tiap berkas sumber benar-benar ada. `value_counts()` menghitung jumlah item per label: 5 temuan eksperimen, 3 dokumentasi, 3 eksploratori, 2 ilustrasi didaktik, 1 tinjauan pustaka terbatas, 1 rencana dan protokol.

### Bagian E — Fakta yang boleh dikutip

```python
--8<-- "level-7/10_final_research_project.py:facts"
```

```text title="Output"
--8<-- "level-7/outputs/10/facts.txt"
```

**Penjelasan:** `facts_all` menggabungkan fakta Bab 7 dengan hasil uji lanjutan dan empat nilai profil per ukuran. `pool` adalah himpunan bentuk tulisan angka yang sah, dan `F(key, d)` mengutip fakta dengan format koma. Pemeriksa kata berlebihan dan keterlacakan angka sama dengan Bab 7 (pencocokan kata utuh, negasi sederhana, tanda minus). Empat nilai profil ditambahkan **setelah** QA pertama menangkap bahwa dua di antaranya (1,43 dan 1,42) belum terdaftar.

### Bagian F — Menyusun laporan 17 bagian

```python
--8<-- "level-7/10_final_research_project.py:report"
```

```text title="Output"
--8<-- "level-7/outputs/10/report.txt"
```

**Penjelasan:**

- `sec(title, label, sources, body)` menambahkan satu bagian: nomor otomatis, judul, **label status isi**, sumber, dan isi.
- `bullets(items)` membuat daftar berpoin, `md_table(frame)` membuat tabel Markdown, dan `led(kind)` mengambil kalimat buku bukti menurut jenis.
- Tiap bagian dirakit dari berkas: misalnya bagian 6 memakai `card[...]`, bagian 9 memakai `protocol["algoritma"]` dan manifest, bagian 15 memakai `F(...)` untuk angka.
- `extra_discussion` adalah kalimat pembahasan tambahan yang menghubungkan RQ2 dengan dua sumber baru, dengan kata "sejalan dengan" dan catatan bahwa itu berdasarkan ringkasan.
- `followup_text` merangkum uji lanjutan, berlabel **(Eksploratori, Bab 10)**.
- `conclusion` menjawab RQ1 sampai RQ3 dengan angka dari `F(...)` dan `min(ari_values)` serta `max(ari_values)` untuk rentang ARI.
- `future` adalah tabel pekerjaan lanjutan beserta cara mengujinya.

### Bagian G — QA akhir

```python
--8<-- "level-7/10_final_research_project.py:qa"
```

```text title="Output"
--8<-- "level-7/outputs/10/qa.txt"
```

**Penjelasan:** `all_text` menggabungkan isi semua bagian. `check(name, ok, detail, warn_only)` menambahkan butir dengan status `LULUS`, `PERINGATAN`, atau `GAGAL`. Butir yang bisa **gagal**: kelengkapan 17 bagian, label, keterlacakan angka, kata berlebihan, hash dan amendment, kecocokan eksekusi, sumber dan gambar, label eksploratori, cakupan pustaka, dan pemisahan label. Dua butir selalu **peringatan bila tidak terpenuhi**: sumber dibaca penuh dan status paket Bab 9.

### Bagian H — Menyimpan laporan dan hasil QA

```python
--8<-- "level-7/10_final_research_project.py:save"
```

```text title="Output"
--8<-- "level-7/outputs/10/save.txt"
```

**Penjelasan:** laporan ditulis sebagai Markdown dengan judul, tiap bagian beserta labelnya, dan **peta status isi** di akhir. Berkas lain: matriks pustaka akhir, pernyataan celah akhir, hasil uji lanjutan, status bagian, peta status, dan QA.

## Code Explanation

| Bagian kode | Peran |
|---|---|
| Pemeriksaan hash di awal | Menolak berjalan bila protokol berubah |
| `pd.concat([literature, new_rows])` | Menambah sumber tanpa mengubah matriks Bab 3 |
| `kmeans = lambda data: ...` | Uji lanjutan dengan pengaturan yang sama |
| `status_map` | Pembeda ilustrasi, temuan, dan eksploratori |
| `facts_all` dan `F(...)` | Semua angka laporan berasal dari registri fakta |
| `sec(...)` | Satu bagian laporan dengan label dan sumber |
| `check(...)` | QA akhir dengan LULUS, PERINGATAN, GAGAL |

## How to Run

Dari folder utama proyek (setelah mengaktifkan lingkungan virtual dan menjalankan skrip Bab 2 sampai 9):

```powershell
pip install -r requirements-notebooks.txt
python examples/level-7/10_final_research_project.py
```

Skrip berjalan beberapa detik dan menyimpan tujuh berkas berawalan `10_` di `examples/level-7/results/`. Notebook interaktifnya:

```powershell
jupyter notebook notebooks/level-7/10-final-clustering-research-project.ipynb
```

Notebook memuat Bagian A sampai H, ditambah tiga bagian **Praktik**: menambahkan analisis eksploratori berlabel ke laporan, menguji peta status isi, dan menulis draf amendment untuk satu pekerjaan lanjutan.

Semua output pada bab ini berasal dari eksekusi nyata dengan Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, dan scikit-learn 1.9.0.

## Expected Output

Output setiap langkah ditampilkan langsung di bawah kodenya pada bagian [Python Implementation](#python-implementation).

Laporan proyek akhir yang dirakit skrip (`results/10_final_report.md`), ditampilkan sebagai teks mentah. **Inilah proyek Level 7 secara utuh**:

```markdown
--8<-- "level-7/results/10_final_report.md"
```

### Interpretasi output

**1. Protokol dan eksekusi.** Hash protokol terverifikasi (`c65be407e00ab39b`), dan eksekusi Bab 6: **156 dari 156**.

**2. Pustaka.** Matriks akhir 7 sumber, **0 dibaca penuh**. Cakupan per pertanyaan: RQ1 1, **RQ2 2**, RQ3 1. RQ2 kini punya dukungan pustaka (dua sumber, hanya dari ringkasan).

**3. Uji lanjutan (eksploratori).** ARI K-Means tanpa skala pada seluruh fitur terhadap `worst area` saja adalah **1,000**, terhadap dua fitur area **0,992**, dan terhadap pengelompokan tanpa kedua fitur area **0,849**. Ukuran kelompok K-Means tanpa skala: [131, 438]; tanpa dua fitur area: [454, 115]. Dugaan dominasi fitur berskala besar **didukung** pada dataset ini.

**4. Peta status isi.** 15 item: 5 temuan eksperimen, 3 dokumentasi, 3 eksploratori, 2 ilustrasi didaktik, 1 tinjauan pustaka terbatas, 1 rencana dan protokol. Semua berkas sumber ada.

**5. Laporan.** 17 bagian, sekitar 1.900 kata. Bagian terpanjang adalah bagian 14 (hasil dan pembahasan); yang paling singkat adalah judul (19 kata), visualisasi (28 kata), dan evaluasi (33 kata).

**6. QA akhir.** **11 LULUS, 2 PERINGATAN, 0 GAGAL.** Dua peringatan: (a) 0 dari 7 sumber pustaka dibaca penuh, dan (b) paket reproduksi Bab 9 masih memiliki satu peringatan (kode belum di-commit).

!!! warning "Batas kesimpulan"
    Semua temuan berlaku untuk **satu dataset (569 sampel), K = 2 sebagai asumsi desain, dan konfigurasi protokol**. Uji lanjutan bersifat eksploratori. Pustaka hanya dibaca abstrak atau ringkasan (0 dari 7 dibaca penuh). Protokol tidak sepenuhnya buta terhadap data, dan hanya DBSCAN yang disetel. Dugaan tentang DBSCAN (kepadatan seragam) **belum diuji**. Persetujuan etik dan de-identifikasi data tidak diketahui. Tidak ada klaim klinis, sebab-akibat, atau "algoritma terbaik", dan tidak ada klaim kebaruan ilmiah.

## Practical Examples

**Menyerahkan skripsi atau laporan penelitian.** Laporan 17 bagian ini adalah kerangka lengkap: tiap bagian punya sumber, label, dan angka yang terlacak. Yang tersisa adalah menulis prosa (Bab 8) dan membereskan peringatan.

**Mereview penelitian orang lain.** Pakai peta status isi sebagai alat: untuk tiap klaim, tanyakan "ini temuan terencana, eksploratori, atau contoh?" dan "sumbernya apa?". Penelitian yang tidak bisa menjawab keduanya perlu dibaca kritis.

**Merencanakan penelitian berikutnya.** Tabel pekerjaan lanjutan memberi daftar yang bisa diuji, lengkap dengan cara mengujinya. Pilih satu, tulis protokol barunya, kunci, lalu kerjakan seperti Bab 5 sampai 9.

## Hands-on Exercises

Semua angka di jawaban berasal dari eksekusi nyata, kecuali disebut lain.

1. Dari QA akhir, sebutkan dua butir berstatus PERINGATAN dan apa yang diperlukan untuk membereskan masing-masing.
2. Mengapa demonstrasi Bab 1 berlabel **ilustrasi didaktik**, meskipun salah satu angkanya (ARI 0,654) kebetulan sama dengan temuan RQ3 untuk K-Means?
3. Jelaskan apa arti ARI 1,000 antara K-Means tanpa skala pada seluruh fitur dan K-Means hanya pada `worst area`. Apa yang **tidak** bisa disimpulkan?
4. Mengapa uji dominasi fitur diberi label eksploratori dan bukan temuan eksperimen?
5. Mengapa QA tidak menjadikan "0 dari 7 sumber dibaca penuh" sebagai kegagalan?
6. Pilih satu pekerjaan lanjutan dari tabel, lalu tulis satu pertanyaan penelitian baru yang spesifik, terukur, dan terbatas untuknya.

??? question "Jawaban"
    Nomor 1, 3, dan 4 memakai output nyata.

    1. (a) 0 dari 7 sumber dibaca penuh: perlu mengakses dan membaca teks lengkap, yang tidak bisa dilakukan skrip. (b) Paket Bab 9 punya peringatan commit: perlu melakukan commit berkas Level 7 (keputusan pemilik repositori) lalu menjalankan ulang skrip Bab 9.
    2. Karena Bab 1 dijalankan **sebelum** protokol dan dipakai mengajar (pengelompokan fitur Q1 sampai Q3 dipilih sembarang untuk ilustrasi). Kebetulan angka sama muncul karena Q3 memakai pengaturan yang sama dengan K-Means pada RQ3, tetapi statusnya tetap demonstrasi. Pengungkapan di Bab 5 mencatatnya.
    3. ARI 1,000 berarti kedua pengelompokan **identik** (hingga pertukaran nomor kelompok): pada data tanpa skala, K-Means pada seluruh 30 fitur menghasilkan pembagian yang sama dengan memakai `worst area` saja. Yang tidak bisa disimpulkan: bahwa `worst area` penting secara ilmiah atau klinis, atau bahwa hal yang sama terjadi pada dataset lain. Itu hanya menunjukkan fitur berskala besar mendominasi jarak pada skala asli.
    4. Karena uji itu dibuat **setelah** protokol dikunci dan setelah melihat hasil Bab 7. Ia bukan bagian dari 156 eksekusi terencana. Melabelinya sebagai eksploratori mencegah pembaca mengira ia analisis terencana.
    5. Karena membaca teks lengkap adalah pekerjaan manusia di luar kendali skrip, dan angka itu jujur mencerminkan keadaan. Ia peringatan agar penulis tahu bahwa kajian pustaka belum matang, bukan kegagalan kode.
    6. Contoh (dari pekerjaan "uji pada dataset lain"): "Seberapa stabil pengelompokan K-Means (K = 2, data terstandarisasi) pada dataset publik lain berlisensi jelas dibanding pada Breast Cancer Wisconsin, diukur dengan ARI antar-seed dan antar-subsampel?" Spesifik, terukur, dan terbatas.

## Troubleshooting

### Masalah teknis

| Masalah | Penyebab | Solusi |
|---|---|---|
| `SystemExit: Protokol berubah sejak dikunci` | `05_protocol.json` berbeda dari hash | Pulihkan protokol atau buat amendment resmi |
| `FileNotFoundError` untuk `09_package_checklist.csv` | Skrip Bab 9 belum dijalankan | Jalankan skrip Bab 2 sampai 9 |
| QA "angka tak terlacak" gagal | Angka diketik atau belum didaftarkan di `facts_all` | Daftarkan dari berkas sumber dan kutip dengan `F(...)` |
| QA "label eksploratori" gagal | Kalimat uji lanjutan kehilangan "(Eksploratori" | Pertahankan label di awal kalimat |
| Peta status melaporkan sumber hilang | Berkas belum dihasilkan | Jalankan skrip bab yang bersangkutan |
| Angka jumlah berkas pada laporan berbeda | Jumlah berkas yang dilacak Bab 9 berubah | Jalankan ulang Bab 9 lalu Bab 10 |

### Kesalahan umum

1. **Menghapus butir QA yang gagal**, bukan memperbaikinya.
2. **Mengubah label agar tampak lebih meyakinkan** (misalnya menandai eksploratori sebagai temuan).
3. **Menulis kesimpulan sebelum QA dijalankan.**
4. **Melupakan bahwa notebook adalah salinan** dari skrip; hasil resmi tetap dari skrip.

## Summary

- **Proyek akhir** menyatukan Bab 1 sampai 9 menjadi laporan 17 bagian yang dirakit dari berkas hasil, bukan ditulis ulang.
- **Label status isi** memisahkan ilustrasi didaktik (2 item), temuan eksperimen (5), eksploratori (3), dokumentasi (3), tinjauan pustaka terbatas (1), dan rencana protokol (1).
- **Celah ditutup sebagian:** RQ2 kini punya 2 sumber (hanya dari ringkasan), tetapi 0 dari 7 sumber dibaca penuh.
- **Dugaan dominasi fitur diuji langsung (eksploratori):** K-Means tanpa skala identik dengan pengelompokan `worst area` saja (ARI 1,000), dan berubah (0,849) bila kedua fitur area dibuang.
- **Kesimpulan dibatasi:** RQ1 tampak konsisten (ARI 0,981 dan 0,964), RQ2 skala mengubah pengelompokan (0,496 dan 0,896), RQ3 cukup selaras dengan diagnosis (0,575 sampai 0,774) dengan peringkat berbeda antar metrik dan DBSCAN tanpa konfigurasi valid.
- **QA akhir:** 11 lulus, 2 peringatan, 0 gagal. QA juga menangkap dua angka yang belum terdaftar saat bab ini disusun.
- **Kontribusi** tetap didaktik dan metodologis. Tidak ada klaim klinis, sebab-akibat, atau "algoritma terbaik".

**Penutup Level 7:** Level ini selesai. Kamu sudah melihat satu penelitian clustering dari pertanyaan sampai paket reproduksi, dengan kejujuran tentang apa yang diketahui dan belum diketahui. Langkah berikutnya ada padamu: membereskan peringatan (membaca sumber penuh, commit kode), menulis prosa naskah (Bab 8), lalu menerapkan protokol ini pada penelitianmu sendiri.

## References

- Milligan, G. W., & Cooper, M. C. (1988). A study of standardization of variables in cluster analysis. *Journal of Classification*, 5(2), 181–204. [doi.org/10.1007/BF01897163](https://doi.org/10.1007/BF01897163). (Hanya ringkasan hasil pencarian; teks lengkap tidak dibaca.)
- Steinley, D. (2004). Standardizing variables in K-means clustering. Dalam D. Banks dkk. (Eds.), *Classification, Clustering, and Data Mining Applications* (hlm. 53–60). Springer. [doi.org/10.1007/978-3-642-17103-1_6](https://doi.org/10.1007/978-3-642-17103-1_6). (Hanya ringkasan hasil pencarian; teks lengkap tidak dibaca.)
- von Luxburg, U., Williamson, R. C., & Guyon, I. (2012). Clustering: Science or Art? *JMLR Workshop and Conference Proceedings*, 27, 65–79. [proceedings.mlr.press/v27/luxburg12a.html](https://proceedings.mlr.press/v27/luxburg12a.html)
- Hennig, C. (2015). What are the true clusters? arXiv:1502.02555 [stat.OT]. [arxiv.org/abs/1502.02555](https://arxiv.org/abs/1502.02555)
- Ben-Hur, A., Elisseeff, A., & Guyon, I. (2002). A stability based method for discovering structure in clustered data. *Pacific Symposium on Biocomputing*, 7, 6–17.
- Vinh, N. X., Epps, J., & Bailey, J. (2010). Information theoretic measures for clusterings comparison. *Journal of Machine Learning Research*, 11, 2837–2854. [jmlr.org/papers/v11/vinh10a.html](https://jmlr.org/papers/v11/vinh10a.html)
- Jain, A. K. (2010). Data clustering: 50 years beyond K-means. *Pattern Recognition Letters*, 31(8), 651–666. [doi.org/10.1016/j.patrec.2009.09.011](https://doi.org/10.1016/j.patrec.2009.09.011)
- Wolberg, W., Mangasarian, O., Street, N., & Street, W. (1993). *Breast Cancer Wisconsin (Diagnostic)* [Dataset]. UCI Machine Learning Repository. [doi.org/10.24432/C5DW2B](https://doi.org/10.24432/C5DW2B). Lisensi CC BY 4.0 menurut halaman dataset.
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92. [doi.org/10.1145/3458723](https://doi.org/10.1145/3458723)
- Kerr, N. L. (1998). HARKing: Hypothesizing after the results are known. *Personality and Social Psychology Review*, 2(3), 196–217. [doi.org/10.1207/s15327957pspr0203_4](https://doi.org/10.1207/s15327957pspr0203_4)
