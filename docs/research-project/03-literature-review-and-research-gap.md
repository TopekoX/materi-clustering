# Bab 3 — Literature Review and Research Gap

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan fungsi tinjauan pustaka dalam penelitian clustering.
- [x] Mencari publikasi ilmiah yang relevan dan mencatat proses pencariannya.
- [x] Membedakan tinjauan pustaka terarah (*narrative*) dari tinjauan sistematis.
- [x] Mengisi matriks tinjauan pustaka dengan jujur, termasuk menandai informasi yang belum diverifikasi.
- [x] Mengekstrak dataset, algoritma, metrik, temuan, dan keterbatasan dari sebuah makalah.
- [x] Membandingkan penelitian terdahulu tanpa membandingkan hal yang tidak sebanding.
- [x] Merumuskan celah riset yang bisa dipertanggungjawabkan dan menghindari klaim mutlak.
- [x] Memeriksa apakah setiap pertanyaan riset sudah punya dukungan pustaka.

## Introduction

Di Bab 2 kamu menulis rumusan masalah dan tiga pertanyaan riset. Sekarang muncul pertanyaan yang mudah dilupakan pemula: **apakah orang lain sudah menjawabnya?** Kalau sudah, penelitianmu mengulang. Kalau belum, mengapa belum? Mungkin karena memang belum ada yang mencoba, mungkin karena tidak dianggap penting, mungkin juga karena sulit.

Tinjauan pustaka menjawab pertanyaan itu. Ia punya tiga fungsi:

1. **Menempatkan penelitianmu.** Menunjukkan apa yang sudah diketahui, sehingga kamu tidak membangun dari nol.
2. **Menyempurnakan pertanyaan.** Kadang pustaka menunjukkan bahwa pertanyaanmu terlalu luas, sudah terjawab, atau butuh definisi lain.
3. **Membuka celah.** Menunjukkan hal yang belum dijawab, yang kemudian menjadi dasar kontribusi.

Dalam bab ini kamu mengerjakan semuanya dengan **lima sumber nyata** yang diverifikasi saat bab ini ditulis. Ada satu pelajaran yang sengaja ditonjolkan: **kejujuran tentang apa yang sudah kamu baca**. Kelima sumber di bab ini hanya dibaca abstraknya atau ringkasannya, dan itu dicatat di matriks. Kamu akan melihat bagaimana batas itu mengubah apa yang boleh kamu klaim.

!!! note "Prasyarat"
    - [Bab 2 — Research Problem Formulation](02-research-problem-formulation.md): rumusan masalah dan RQ1 sampai RQ3, yang dibaca oleh skrip bab ini.
    - [Bab 1](01-introduction-to-clustering-research.md): hubungan pertanyaan, data, algoritma, dan evaluasi.

## Fundamental Concepts

| Istilah | Arti |
|---|---|
| **Literature review** | Telaah terhadap publikasi ilmiah yang berkaitan dengan pertanyaan risetmu |
| **Narrative / terarah** | Tinjauan yang memilih sumber penting secara terarah, tanpa prosedur pencarian yang bisa diulang sepenuhnya |
| **Systematic review** | Tinjauan dengan prosedur pencarian, kriteria seleksi, dan pelaporan yang terdokumentasi sehingga orang lain bisa mengulangnya |
| **Primary source** | Makalah yang melaporkan penelitian aslinya |
| **Secondary source** | Tinjauan atau rangkuman atas makalah lain |
| **Preprint** | Naskah yang diunggah sebelum atau tanpa *peer review* (contoh: arXiv) |
| **Peer review** | Penilaian naskah oleh ahli sebelum diterbitkan |
| **Literature matrix** | Tabel yang merangkum tiap makalah dengan kolom yang sama |
| **Search log** | Catatan kueri, sumber, tanggal, dan hasil pencarian |
| **Inclusion / exclusion criteria** | Aturan tertulis tentang makalah yang dimasukkan dan dikeluarkan |
| **Research gap** | Hal yang belum dijawab atau belum cukup dijawab oleh pustaka yang ditelaah |
| **Snowballing** | Mencari makalah lain dari daftar pustaka sebuah makalah (*backward*) atau dari makalah yang mengutipnya (*forward*) |

## Detailed Explanation

### Menemukan publikasi yang relevan

**Sumber pencarian yang umum**

| Jenis | Contoh | Catatan |
|---|---|---|
| Mesin pencari akademik | Google Scholar, Semantic Scholar | Cakupan luas, hasil perlu disaring |
| Basis data bibliografi | Scopus, Web of Science, dblp | Sering butuh akses institusi |
| Penerbit dan prosiding | JMLR/PMLR, ACM Digital Library, IEEE Xplore, ScienceDirect | Sumber primer |
| Repositori preprint | arXiv | Cepat, tetapi belum tentu melewati *peer review* |

**Menyusun kata kunci.** Mulai dari istilah di pertanyaanmu, lalu tambahkan sinonim dan variannya. Untuk RQ1 kita mencari seperti "clustering stability", "stability of clustering", "cluster validation". Tanda kutip mencari frasa utuh, dan operator seperti AND/OR membatasi hasil, tetapi sintaksnya berbeda antar basis data. Periksa panduan tiap sumber.

**Snowballing.** Makalah yang bagus biasanya menunjuk makalah lain yang bagus. Lihat daftar pustakanya (*backward*), lalu lihat siapa yang mengutipnya (*forward*).

**Menyaring.** Tentukan di awal: tahun, bahasa, jenis (jurnal, prosiding, preprint), dan topik. Tulis alasan memasukkan atau mengeluarkan sebuah makalah. Tanpa kriteria tertulis, seleksi mudah terpengaruh apa yang menguatkan keyakinanmu.

!!! warning "Verifikasi data bibliografi"
    Jangan menyalin referensi dari ingatan atau dari hasil yang tidak dicek. Periksa judul, penulis, tahun, penerbit, dan nomor halaman pada halaman penerbit atau DOI. Di bab ini setiap sumber sudah dicek pada halaman penerbit, repositori resmi, atau hasil pencarian, dan matriks mencatat sampai sejauh mana bacaannya.

### Terarah atau sistematis?

| | Terarah (*narrative*) | Sistematis |
|---|---|---|
| Tujuan | Memberi landasan untuk satu penelitian | Menjawab pertanyaan tinjauan dengan prosedur yang bisa diulang |
| Pencarian | Dipandu pengetahuan peneliti | Kueri, basis data, dan tanggal dicatat penuh |
| Seleksi | Penilaian peneliti | Kriteria inklusi dan eksklusi tertulis |
| Klaim yang sah | "Dari sumber yang kami telaah..." | Klaim yang lebih kuat tentang keseluruhan pustaka |
| Kebutuhan waktu | Rendah sampai sedang | Tinggi |

Tinjauan sistematis dilaporkan dengan panduan seperti **PRISMA 2020** (Page dkk., 2021) yang berasal dari bidang kesehatan, berisi daftar periksa 27 butir dan diagram alir seleksi. Bab ini membuat tinjauan **terarah**, dan kita mengatakannya terus terang. Konsekuensinya: kita tidak berhak mengatakan "tidak ada penelitian yang..." Kita hanya boleh mengatakan "dari sumber yang kami telaah".

### Membaca makalah dengan efisien

Kamu tidak perlu membaca semua makalah dari awal sampai akhir. Cara bertahap yang umum:

1. **Lihat sekilas:** judul, abstrak, gambar, dan kesimpulan. Putuskan apakah relevan.
2. **Baca inti:** pendahuluan, metode, hasil. Catat dataset, algoritma, metrik, dan temuan.
3. **Baca kritis:** periksa asumsi, keterbatasan, dan apakah klaimnya didukung hasil.

Catat di matriks **tahap yang sudah kamu capai** untuk tiap makalah. Itulah kolom `dibaca` di kode bab ini. Informasi yang hanya diambil dari abstrak tidak boleh dilaporkan seolah dari bacaan penuh.

### Matriks tinjauan pustaka

Matriks memaksa kamu membaca dengan pertanyaan yang sama untuk setiap makalah. Kolomnya:

| Kolom | Isi |
|---|---|
| Penulis dan tahun | Referensi yang terverifikasi |
| Tujuan penelitian | Apa yang ingin dijawab makalah itu |
| Dataset | Data yang dipakai, sumber, ukuran |
| Praproses | Cara menyiapkan data |
| Algoritma | Metode clustering yang dipakai atau dibahas |
| Metrik evaluasi | Cara hasil dinilai |
| Temuan utama | Hasil yang dilaporkan penulis |
| Keterbatasan | Batas yang disebut penulis atau yang kamu temukan |
| Celah potensial | Peluang bagi penelitianmu, **ditandai sebagai inferensimu** |
| Tingkat bacaan | Abstrak, ringkasan, atau teks lengkap |

!!! tip "Tanda \"—\" bukan sekadar kosong"
    Sel yang diisi "—" berarti **tidak tercantum pada sumber yang kamu baca**. Itu berbeda dari "makalah itu tidak punya". Bila kamu membaca teks lengkapnya, sel itu mungkin bisa diisi. Membedakan dua hal ini mencegah kamu menyimpulkan "tidak ada dataset" padahal kamu baru membaca abstrak.

### Membandingkan penelitian terdahulu

Membandingkan dua makalah hanya adil bila dasarnya sama. Periksa:

1. **Dataset yang sama atau setara?** Hasil pada data berbeda tidak bisa dibandingkan angkanya.
2. **Praproses yang sama?** Standardisasi bisa mengubah hasil (Level 6).
3. **Metrik yang sama?** Silhouette dan ARI menjawab pertanyaan berbeda (Bab 1).
4. **Nilai K dan parameter yang sama?**
5. **Tujuan yang sama?** Makalah tentang evaluasi konsep tidak bisa dibandingkan dengan makalah yang melaporkan eksperimen.

Karena itu, daripada membandingkan angka, bandingkan **rancangan dan temuan kualitatif**: apa yang diukur, bagaimana, dan kesimpulan apa yang ditarik.

### Mengekstrak informasi: contoh pada lima sumber

Kode di bab ini mengisi matriks dengan lima sumber yang dicek. Isinya ditampilkan di bagian *Expected Output*. Hal penting yang terlihat:

- **Empat dari lima** sumber tidak punya dataset tercantum. Dua di antaranya (L1 dan L2) makalah konseptual, dan untuk semuanya kita hanya membaca abstrak atau ringkasan.
- **Tidak satu pun** keterbatasan terisi, karena keterbatasan jarang ada di abstrak. Itu memaksa kita jujur: kolom itu baru bisa diisi setelah membaca teks lengkap.

### Keterbatasan penelitian terdahulu

Keterbatasan adalah bahan mentah bagi celah. Jenis yang umum:

| Jenis | Contoh |
|---|---|
| **Data** | Hanya satu dataset, ukuran kecil, data sintetis |
| **Metode** | Hanya satu algoritma atau satu metrik |
| **Praproses** | Tidak melaporkan cara menyiapkan data |
| **Evaluasi** | Tanpa uji kestabilan atau pembanding |
| **Reproduksibilitas** | Kode atau konfigurasi tidak dibagikan |
| **Generalisasi** | Hasil berlaku untuk kondisi sempit |

Keterbatasan yang kamu tulis tentang makalah orang lain harus **bersumber**: kutip pernyataan penulis, atau tunjukkan dengan jelas bahwa itu pengamatanmu. Jangan menyebut sebuah penelitian "lemah" tanpa dasar.

### Merumuskan celah riset

Celah bukan sekadar "belum ada yang melakukan". Ia harus **bermakna**: ada alasan mengapa jawabannya perlu diketahui. Jenis celah:

| Jenis celah | Contoh pola |
|---|---|
| **Empiris** | Hasil serupa belum diuji pada kondisi atau data tertentu |
| **Metodologis** | Protokol yang ada kurang ketat atau tidak terdokumentasi |
| **Kontradiksi** | Dua penelitian memberi hasil berbeda tanpa penjelasan |
| **Kontekstual** | Temuan di satu domain belum diperiksa di domain lain |
| **Reproduksibilitas** | Temuan belum diulang oleh pihak lain |

**Cara menulis celah yang bisa dipertanggungjawabkan:**

1. **Batasi dengan sumber yang kamu telaah.** "Dari 5 sumber yang ditelaah..." bukan "tidak ada penelitian...".
2. **Sebut tingkat bacaanmu.** "Berdasarkan abstrak..." membuat pembaca tahu seberapa kuat klaimnya.
3. **Sebut jenis tinjauan.** Terarah atau sistematis.
4. **Jelaskan mengapa celah itu penting**, bukan hanya bahwa ia ada.
5. **Hindari kata mutlak:** "belum pernah", "pertama kali", "satu-satunya", "tidak ada penelitian".

| Rumusan | Penilaian | Alasan |
|---|---|---|
| "Belum pernah ada penelitian tentang kestabilan clustering pada data medis." | Buruk | Klaim mutlak, tanpa batas pencarian |
| "Penelitian ini adalah yang pertama kali membandingkan kestabilan dan keselarasan eksternal." | Buruk | Klaim mutlak dan kebaruan yang tidak dibuktikan |
| "Dari 5 sumber yang ditelaah berdasarkan abstrak, tidak satu pun yang kami baca menyajikan protokol terpadu ... Ini bukan klaim bahwa studi serupa tidak ada." | Lebih baik | Dibatasi jumlah sumber, tingkat bacaan, dan jenis tinjauan |

!!! warning "Rumusan 'lebih baik' belum tentu 'kuat'"
    Rumusan ketiga lolos pemeriksa kata kunci pada kode, tetapi **kekuatannya tetap terbatas**: ia bersandar pada lima sumber yang hanya dibaca abstraknya. Bila kamu menulisnya di makalah, penelaah akan meminta tinjauan yang lebih luas. Rumusan itu jujur, bukan kuat.

### Dari celah ke kontribusi

Celah yang jujur menghasilkan kontribusi yang jujur. Pada proyek kita, kontribusinya (Bab 2) tetap **didaktik dan metodologis**: mendemonstrasikan protokol yang bisa diulang, dengan semua konfigurasi dibagikan. Kita tidak menyimpulkan bahwa topik ini "belum pernah diteliti".

### Memeriksa dukungan pustaka untuk tiap pertanyaan

Satu langkah yang jarang dilakukan pemula: memetakan **tiap pertanyaan riset** ke pustaka yang mendukungnya. Pada kode kita memberi tiap makalah satu label topik, lalu menghitung berapa makalah yang mendukung RQ1, RQ2, dan RQ3. Hasilnya menunjukkan sesuatu yang berguna: ada pertanyaan yang tidak punya pustaka sama sekali pada set ini. Itu bukan kegagalan, tetapi sinyal untuk mencari lagi sebelum melanjutkan.

### Kesalahan umum

1. **Menyalin referensi tanpa memeriksa.**
2. **Mengklaim "belum pernah diteliti"** tanpa tinjauan sistematis.
3. **Melaporkan isi makalah yang hanya dibaca judulnya atau abstraknya** seolah dibaca penuh.
4. **Mengisi matriks dengan dugaan.** Tulis "—" bila tidak ada.
5. **Membandingkan angka antar makalah** tanpa memeriksa dataset, praproses, dan metrik.
6. **Mencari hanya yang mendukung pendapatmu** (*confirmation bias*).
7. **Tidak mencatat kueri dan tanggal pencarian.**
8. **Menyebut makalah lain "lemah" tanpa dasar.**
9. **Menulis celah yang tidak penting**: belum dilakukan bukan berarti perlu dilakukan.
10. **Melupakan pertanyaan yang tidak punya pustaka pendukung.**

## Mathematical Foundation

Bab ini tidak memerlukan rumus baru. Tinjauan pustaka adalah kerja membaca, mencatat, dan menalar. Satu-satunya "hitungan" di kode adalah penghitungan sel yang terisi dan jumlah makalah per topik.

## Python Implementation

Skrip lengkapnya ada di `examples/level-7/03_literature_review_and_research_gap.py`, dan notebook-nya di `notebooks/level-7/03-literature-review-and-research-gap.ipynb`. **Setiap potongan kode diikuti penjelasannya.**

**Konteks masalah:** kita perlu mengetahui apa kata pustaka tentang kestabilan, perbandingan pengelompokan, dan makna kelompok, serta apakah ketiga pertanyaan riset kita punya dukungan.

**Tujuan:** membangun matriks tinjauan pustaka dari lima sumber terverifikasi, memetakan cakupannya, mencatat pencarian, memeriksa klaim celah, dan menyimpan pernyataan celah yang dibatasi.

**Data:** bukan dataset clustering. Datanya adalah **metadata lima makalah**. Skrip ini juga membaca `02_research_problem.json` dari Bab 2, jadi **jalankan skrip Bab 2 lebih dulu**.

**Pustaka:** pandas, serta `json` dan `re` dari pustaka standar.

!!! warning "Isi matriks berasal dari abstrak atau ringkasan"
    Kelima sumber **tidak dibaca penuh**. Kolom `dibaca` mencatat tingkat bacaan masing-masing: satu dari abstrak penerbit, empat dari ringkasan halaman atau hasil pencarian. Sel yang tidak tercantum di sumber yang dibaca diisi "—". Sebelum dikutip di makalah sungguhan, setiap makalah perlu dibaca teks lengkapnya.

### Bagian A — Siapkan alat dan baca rumusan Bab 2

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:setup"
```

**Penjelasan:** `json.loads(... .read_text(encoding="utf-8"))` membaca berkas JSON dari Bab 2 dan mengubahnya menjadi dictionary Python. `RESULTS / "02_research_problem.json"` menyusun jalur berkas dengan operator `/` dari `pathlib`. Kita mencetak kunci `pertanyaan` untuk memastikan RQ1 sampai RQ3 terbaca. Bab ini memakai rumusan Bab 2 sebagai satu sumber kebenaran, bukan menyalinnya ulang.

### Bagian B — Matriks tinjauan pustaka

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:matrix"
```

**Penjelasan:**

- `NA = "—"` adalah satu tanda untuk "tidak tercantum pada sumber yang dibaca".
- `rows` adalah daftar dictionary, satu dictionary per makalah, dengan kunci yang sama (kolom matriks). Kunci `topik` memberi label yang dipakai untuk memetakan cakupan, dan `dibaca` mencatat tingkat bacaan.
- Kolom `celah_potensial` diawali "Inferensi penulis bab" agar jelas bahwa itu pendapat, bukan temuan makalah.
- `pd.DataFrame(rows).set_index("id")` mengubah daftar itu menjadi tabel dengan `id` sebagai indeks baris.
- `matrix[show]` memilih beberapa kolom saja, dan `.to_string()` mencetaknya penuh tanpa dipotong.

### Bagian C — Kelengkapan dan tingkat verifikasi

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:completeness"
```

**Penjelasan:**

- `matrix[fields] != NA` menghasilkan tabel `True`/`False`: `True` bila sel **bukan** "—". `.sum(axis=1)` menjumlahkan per baris, sehingga hasilnya adalah banyaknya sel terisi untuk tiap makalah (`True` dihitung sebagai 1).
- `pd.DataFrame({...})` merangkum jumlah sel terisi, jumlah kolom (`len(fields)` = 7), dan tingkat bacaan.
- `(matrix["dibaca"] == "teks lengkap").sum()` menghitung berapa makalah yang dibaca penuh. `int(...)` mengubah hasilnya menjadi bilangan bulat biasa.
- Dua baris cetak terakhir menyorot dua fakta jujur: tidak ada makalah yang dibaca penuh, dan tidak ada keterbatasan yang terisi.

### Bagian D — Cakupan pustaka terhadap pertanyaan riset

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:coverage"
```

**Penjelasan:**

- `needs` memetakan tiap pertanyaan ke **topik pustaka yang dibutuhkan**: RQ1 butuh pustaka kestabilan, RQ2 butuh pustaka sensitivitas praproses, RQ3 butuh pustaka pembanding partisi.
- `matrix.index[matrix["topik"] == topic].tolist()` memilih `id` makalah yang labelnya sama dengan topik itu.
- `coverage[rq] = {...}` menyimpan hasilnya dalam dictionary bertingkat.
- `uncovered` adalah daftar pertanyaan yang jumlah makalahnya nol. Daftar komprehensi `[rq for rq, info in coverage.items() if ...]` menyaringnya.

### Bagian E — Log pencarian

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:searchlog"
```

**Penjelasan:** log mencatat tanggal, sumber, kueri, dan makalah yang dipilih. Isinya adalah pencarian yang **benar-benar dilakukan** saat bab ini ditulis. Baris terakhir menyatakan jenis tinjauannya: **terarah**, bukan sistematis. Pencatatan semacam ini adalah syarat dasar agar orang lain bisa menilai atau mengulang pencarianmu.

### Bagian F — Memeriksa kata-kata klaim celah

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:gapcheck"
```

**Penjelasan:**

- `re.search(r"\b(dari|di antara)\s+\d+\s+(makalah|sumber|studi)", low)` mencari pola seperti "dari 5 sumber". `\b` menandai batas kata, `\s+` satu atau lebih spasi, `\d+` satu atau lebih angka. `tanpa_batas_pencarian` bernilai `True` bila pola itu **tidak** ditemukan.
- `klaim_mutlak` mendeteksi frasa seperti "belum pernah" atau "pertama kali". `klaim_kebaruan` mendeteksi kata seperti "baru" atau "inovatif".
- `claims` berisi tiga contoh: C1 dan C2 buruk, C3 yang dibatasi.

!!! warning "Alat bantu yang mudah dikelabui"
    Seperti pemeriksa di Bab 2, ini hanya kata kunci. Siapa pun bisa menulis "dari 100 sumber" tanpa pernah membacanya dan lolos. Pemeriksa hanya mengingatkan bentuk, bukan kebenaran isinya.

### Bagian G — Pernyataan celah yang dibatasi

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:statement"
```

**Penjelasan:** `n_sources = len(matrix)` menghitung jumlah makalah, lalu f-string memasukkannya ke kalimat. Angka itu **tidak diketik tangan**: bila kamu menambah baris di matriks, kalimatnya ikut berubah. Pernyataan lalu diperiksa pemeriksa yang sama.

### Bagian H — Menyimpan hasil

```python
--8<-- "level-7/03_literature_review_and_research_gap.py:save"
```

**Penjelasan:** fungsi `to_markdown` mengubah tabel menjadi teks tabel Markdown (`str(v).replace("|", "/")` mengganti tanda `|` agar tabel tidak rusak). Kita menyimpan empat berkas: matriks (CSV dan Markdown), log pencarian (CSV), dan pernyataan celah (JSON). Berkas `03_gap_statement.json` mencatat bahwa teks pertanyaan tidak berubah dari Bab 2, tetapi RQ2 ditandai butuh pustaka tambahan. Pencatatan perubahan seperti ini mencegah *HARKing* (Bab 2).

## Code Explanation

| Bagian kode | Peran |
|---|---|
| `json.loads(...)` | Membaca rumusan Bab 2 sebagai satu sumber kebenaran |
| `NA = "—"` | Menandai informasi yang tidak tercantum pada sumber yang dibaca |
| `rows = [{...}, ...]` | Matriks tinjauan pustaka sebagai data |
| `(matrix[fields] != NA).sum(axis=1)` | Menghitung sel terisi per makalah |
| `needs` dan `coverage` | Memetakan tiap pertanyaan ke pustaka pendukungnya |
| `search_log` | Catatan pencarian yang benar-benar dilakukan |
| `check_gap_claim(text)` | Pemeriksa kata-kata klaim celah |
| `f"Dari {n_sources} sumber..."` | Angka batas diambil dari data |
| `to_markdown(...)` | Mengubah tabel menjadi Markdown untuk laporan |

## How to Run

Dari folder utama proyek (setelah mengaktifkan lingkungan virtual dan menjalankan skrip Bab 2):

```powershell
pip install -r requirements-notebooks.txt
python examples/level-7/02_research_problem_formulation.py
python examples/level-7/03_literature_review_and_research_gap.py
```

Skrip mencetak output dan menyimpan empat berkas di `examples/level-7/results/`. Notebook interaktifnya:

```powershell
jupyter notebook notebooks/level-7/03-literature-review-and-research-gap.ipynb
```

Notebook memuat Bagian A sampai H, ditambah tiga bagian **Praktik**: menambah makalah ke matriks, menambah catatan pencarian, dan menulis pernyataan celahmu sendiri.

Output di bawah berasal dari eksekusi nyata dengan Python 3.14.10 dan pandas 3.0.5.

## Expected Output

```text
--8<-- "level-7/outputs/03.txt"
```

Matriks lengkap yang disimpan skrip (`results/03_literature_matrix.md`):

--8<-- "level-7/results/03_literature_matrix.md"

### Interpretasi output

**1. Matriks.** Lima sumber, satu per baris. Hanya L3 (Ben-Hur dkk., 2002) yang menyebut dataset ("Data buatan dan data microarray") dan algoritma yang jelas (Hierarchical clustering). L1, L2, L4, dan L5 tidak mencantumkan dataset pada sumber yang dibaca.

**2. Kelengkapan.** Sel terisi dari tujuh kolom: L1 dua, L2 dua, L3 lima, L4 tiga, L5 tiga. **Tidak ada makalah yang dibaca penuh (0 dari 5)** dan **tidak ada keterbatasan yang terisi (0 dari 5)**. Matriks ini adalah awal tinjauan, bukan hasil akhir.

**3. Cakupan pertanyaan.**

| Pertanyaan | Topik dibutuhkan | Makalah | Keterangan |
|---|---|---|---|
| RQ1 | kestabilan | 1 (L3) | Ada dukungan, tipis |
| RQ2 | sensitivitas-praproses | **0** | **Tidak ada pustaka pada set ini** |
| RQ3 | pembanding-partisi | 1 (L4) | Ada dukungan, tipis |

Hasil ini **bukan bukti bahwa tidak ada pustaka tentang RQ2**. Artinya hanya bahwa lima sumber yang kita telaah tidak membahasnya. Langkah yang benar: cari pustaka tentang pengaruh penyamaan skala (*feature scaling*) pada clustering sebelum menulis latar belakang RQ2 di Bab 10. Teks pertanyaan belum diubah, tetapi RQ2 dicatat butuh pustaka tambahan.

**4. Log pencarian.** Lima entri pada 2026-11-10, jenis tinjauan **terarah**. Karena terarah, kita tidak boleh menyimpulkan apa pun tentang "seluruh pustaka".

**5. Klaim celah.** C1 dan C2 ditandai (`klaim_mutlak` dan `tanpa_batas_pencarian`). C3 lolos karena memuat batas "Dari 5 sumber" dan tidak memuat frasa terlarang. Pernyataan celah proyek (Bagian G) juga lolos.

!!! warning "Batas kesimpulan"
    Pernyataan celah proyek bersandar pada **lima sumber yang hanya dibaca abstrak atau ringkasannya**. Ia jujur tentang batas itu, tetapi bukan klaim bahwa celah itu nyata di seluruh pustaka. Bab 10 memperlakukannya sebagai **dasar kerja**, bukan temuan, dan kontribusi tetap dinyatakan didaktik dan metodologis.

## Practical Examples

**Menyusun Bab 2 (Tinjauan Pustaka) skripsi.** Isi matriks lebih dulu, baru tulis narasi. Narasi yang baik mengelompokkan makalah menurut tema (misalnya "kestabilan", "pembandingan pengelompokan"), bukan menjabarkan makalah satu per satu.

**Mengecek ide penelitian cepat.** Sebelum menginvestasikan berminggu-minggu, cari 5 sampai 10 makalah, isi matriks, lalu tanyakan: apakah pertanyaanku sudah terjawab? Bila ya, bagaimana aku bisa berbeda?

**Membaca makalah pembanding.** Saat sebuah makalah mengklaim "metode kami lebih baik", isi matriks untuk makalah itu dan periksa: dataset apa, praproses apa, metrik apa, dan apakah pembandingnya adil.

## Hands-on Exercises

1. Dari output, makalah mana yang paling lengkap isinya dan mana yang paling sedikit? Mengapa ada makalah dengan sel terisi hanya dua dari tujuh?
2. Mengapa kolom `keterbatasan` kosong untuk kelima makalah? Apa yang harus kamu lakukan agar bisa mengisinya?
3. RQ2 tidak punya makalah pendukung. Tuliskan dua kueri pencarian yang akan kamu pakai, lalu jelaskan satu kriteria inklusi dan satu kriteria eksklusi.
4. Mengapa C3 lolos pemeriksa tetapi belum tentu kuat? Bagaimana cara menguatkannya secara jujur?
5. Tambahkan satu makalah yang kamu verifikasi sendiri ke matriks (di notebook). Berapa `jumlah_sumber` sekarang, dan bagaimana kalimat celah berubah?
6. Bedakan tinjauan terarah dan sistematis, dan sebutkan satu klaim yang boleh dibuat dari yang kedua tetapi tidak dari yang pertama.

??? question "Jawaban"
    Nomor 1 sampai 4 memakai output nyata.

    1. L3 paling lengkap (5 dari 7), L1 dan L2 paling sedikit (2 dari 7). L1 dan L2 adalah makalah konseptual yang hanya dibaca abstraknya, jadi dataset, praproses, algoritma, metrik, dan keterbatasan tidak tercantum. Itu wajar untuk makalah jenis itu, bukan kesalahan matriks.
    2. Karena keterbatasan jarang disebut pada abstrak, dan kita hanya membaca abstrak atau ringkasan. Untuk mengisinya, baca teks lengkap (khususnya bagian diskusi dan kesimpulan), lalu isi dengan kutipan atau parafrasa yang bersumber.
    3. Contoh kueri: "feature scaling effect on clustering" dan "standardization K-means cluster stability". Contoh inklusi: makalah yang melaporkan eksperimen perbandingan perlakuan skala pada clustering. Contoh eksklusi: makalah yang hanya membahas klasifikasi tanpa clustering. Kueri dan kriteria dicatat di log sebelum pencarian dijalankan.
    4. C3 lolos karena memuat "Dari 5 sumber" dan tidak memuat frasa terlarang, bukan karena kebenarannya diperiksa. Lima sumber yang dibaca abstraknya adalah dasar yang tipis. Penguatan yang jujur: perluas pencarian, baca teks lengkap, catat kueri, dan sebutkan jenis tinjauan.
    5. Hasil bergantung pada makalah yang kamu tambahkan. `jumlah_sumber` bertambah satu, dan kalimat celah otomatis memuat angka baru karena `n_sources = len(matrix)`.
    6. Terarah: sumber dipilih peneliti tanpa prosedur yang bisa diulang penuh. Sistematis: kueri, basis data, dan kriteria dicatat sehingga bisa diulang. Dari tinjauan sistematis, peneliti lebih berhak mengklaim sesuatu tentang cakupan pustaka (misalnya jumlah studi yang memenuhi kriteria). Dari tinjauan terarah, klaim terbatas pada "sumber yang kami telaah".

## Troubleshooting

### Masalah teknis

| Masalah | Penyebab | Solusi |
|---|---|---|
| `FileNotFoundError: 02_research_problem.json` | Skrip Bab 2 belum dijalankan | Jalankan skrip Bab 2 lebih dulu |
| Tanda "—" tercetak sebagai `?` atau karakter aneh | Konsol Windows memakai encoding lain | Skrip sudah memanggil `sys.stdout.reconfigure(encoding="utf-8")`; pada notebook tidak ada masalah |
| `KeyError` pada kolom matriks | Ada baris di `rows` yang kuncinya berbeda | Pastikan semua dictionary punya kunci sama |
| Tabel Markdown rusak | Isi sel mengandung tanda `\|` | Fungsi `to_markdown` menggantinya dengan `/` |
| Jumlah sel terisi tidak sesuai | Menulis "-" (tanda hubung) bukan "—" | Pakai konstanta `NA` agar konsisten |

### Kesalahan umum

1. **Mengisi sel dari ingatan.**
2. **Menandai makalah "dibaca penuh" padahal baru abstrak.**
3. **Menganggap lolos pemeriksa sama dengan kuat.**
4. **Menyimpulkan tidak ada pustaka** hanya karena set kecilmu tidak memuatnya.
5. **Mengubah pertanyaan setelah membaca pustaka tanpa mencatatnya.**
6. **Melupakan log pencarian.**

## Summary

- **Tinjauan pustaka** menempatkan penelitianmu, menyempurnakan pertanyaan, dan membuka celah.
- Tinjauan **terarah** memberi klaim terbatas ("dari sumber yang kami telaah"), tinjauan **sistematis** memberi klaim yang lebih kuat tetapi membutuhkan prosedur yang terdokumentasi (PRISMA 2020).
- **Matriks pustaka** memaksa pembacaan dengan pertanyaan sama. Tanda "—" berarti **tidak tercantum pada sumber yang dibaca**, bukan "tidak ada".
- **Catat tingkat bacaan** tiap makalah. Pada bab ini 0 dari 5 makalah dibaca penuh dan 0 dari 5 keterbatasan terisi.
- **Celah yang jujur** dibatasi jumlah sumber, tingkat bacaan, dan jenis tinjauan, serta tidak memakai kata mutlak.
- **Peta cakupan** menunjukkan RQ1 dan RQ3 masing-masing punya satu makalah pendukung, sedangkan **RQ2 belum punya**. Itu sinyal mencari lagi, bukan bukti bahwa pustaka itu tidak ada.
- Kontribusi proyek tetap **didaktik dan metodologis**.

**Bab berikutnya:** Bab 4 membahas **pemilihan dataset dan persiapan data penelitian**: sumber, lisensi, kualitas, etika, kriteria inklusi dan eksklusi, serta dokumentasi dataset.

## References

- von Luxburg, U., Williamson, R. C., & Guyon, I. (2012). Clustering: Science or Art? *JMLR Workshop and Conference Proceedings*, 27, 65–79. [proceedings.mlr.press/v27/luxburg12a.html](https://proceedings.mlr.press/v27/luxburg12a.html)
- Hennig, C. (2015). What are the true clusters? arXiv:1502.02555 [stat.OT]. [arxiv.org/abs/1502.02555](https://arxiv.org/abs/1502.02555)
- Ben-Hur, A., Elisseeff, A., & Guyon, I. (2002). A stability based method for discovering structure in clustered data. *Pacific Symposium on Biocomputing*, 7, 6–17.
- Vinh, N. X., Epps, J., & Bailey, J. (2010). Information theoretic measures for clusterings comparison: Variants, properties, normalization and correction for chance. *Journal of Machine Learning Research*, 11, 2837–2854. [jmlr.org/papers/v11/vinh10a.html](https://jmlr.org/papers/v11/vinh10a.html)
- Jain, A. K. (2010). Data clustering: 50 years beyond K-means. *Pattern Recognition Letters*, 31(8), 651–666. [doi.org/10.1016/j.patrec.2009.09.011](https://doi.org/10.1016/j.patrec.2009.09.011)
- Page, M. J., McKenzie, J. E., Bossuyt, P. M., dkk. (2021). The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*, 372, n71. [doi.org/10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71)
- Booth, W. C., Colomb, G. G., Williams, J. M., Bizup, J., & FitzGerald, W. T. (2016). *The Craft of Research* (4th ed.). University of Chicago Press.
