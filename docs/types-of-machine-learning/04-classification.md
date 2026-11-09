# Classification

## Definisi sederhana

**Classification** (klasifikasi) adalah jenis Supervised Learning untuk **menebak kategori**. Jawabannya selalu berupa salah satu pilihan dari daftar yang **sudah ditentukan sebelumnya**.

## Penjelasan dengan bahasa sehari-hari

Petugas pos memilah surat ke kotak "Jakarta", "Bandung", atau "Surabaya". Setiap surat harus masuk ke salah satu kotak yang **sudah ada**. Petugas tidak membuat kotak baru. Itulah klasifikasi.

## Istilah: class dan class label

- **Class** (kelas) adalah salah satu kategori yang mungkin, misalnya "spam".
- **Class label** adalah label berupa nama kelas yang menempel pada tiap baris data.

| Jumlah tautan | Ada kata "gratis"? | Pengirim dikenal? | **Class label** |
|---|---|---|---|
| 8 | Ya | Tidak | **spam** |
| 0 | Tidak | Ya | **bukan spam** |
| 5 | Ya | Tidak | **spam** |
| 1 | Tidak | Ya | **bukan spam** |

Tiga kolom pertama adalah **fitur**. Kolom terakhir adalah **class label**.

## Tiga jenis klasifikasi

### Binary Classification

Hanya ada **dua** kelas. Kata *binary* berarti "dua".

- Spam atau bukan spam.
- Lulus atau tidak lulus.
- Transaksi wajar atau penipuan.

### Multiclass Classification

Ada **lebih dari dua** kelas, tetapi setiap data hanya masuk ke **satu** kelas.

- Jenis bunga: setosa, versicolor, atau virginica.
- Angka tulisan tangan: 0 sampai 9.
- Golongan kendaraan: motor, mobil, bus, atau truk.

### Multilabel Classification

Setiap data boleh punya **beberapa label sekaligus**.

- Sebuah film bisa bergenre "aksi" **dan** "komedi".
- Sebuah artikel berita bisa bertopik "ekonomi" **dan** "politik".
- Sebuah foto bisa berisi "kucing", "sofa", **dan** "jendela".

| Jenis | Jumlah kelas | Label per data | Contoh |
|---|---|---|---|
| Binary | 2 | Tepat 1 | Spam / bukan spam |
| Multiclass | Lebih dari 2 | Tepat 1 | Jenis bunga |
| Multilabel | 2 atau lebih | Bisa lebih dari 1 | Genre film |

## Contoh klasifikasi lain

- Mendeteksi apakah tumor jinak atau ganas dari hasil pemeriksaan.
- Menentukan sentimen ulasan: positif, netral, atau negatif.
- Mengenali rambu lalu lintas dari foto.

## Algoritma klasifikasi yang umum

Berikut gambaran singkat. Cara kerja detailnya tidak dibahas di sini.

| Algoritma | Ide utama dalam satu kalimat |
|---|---|
| **Logistic Regression** | Menghitung peluang suatu data masuk ke sebuah kelas. Walaupun namanya "regression", algoritma ini dipakai untuk klasifikasi |
| **Decision Tree** | Membuat serangkaian pertanyaan ya/tidak, seperti permainan tebak-tebakan, sampai sampai pada sebuah kelas |
| **K-Nearest Neighbors (KNN)** | Melihat \(k\) data latih yang paling dekat, lalu memilih kelas yang paling banyak di antara tetangga itu |
| **Naive Bayes** | Memakai aturan peluang (teorema Bayes) dengan asumsi sederhana bahwa fitur saling bebas |
| **Support Vector Machine (SVM)** | Mencari garis atau bidang pemisah yang memberi jarak selebar mungkin antar kelas |

!!! tip "Jangan menghafal semuanya sekarang"
    Cukup ingat bahwa ada banyak algoritma untuk tugas yang sama. Di [Praktik Supervised Learning](14-python-supervised-learning.md) kita akan mencoba KNN.

## Mengukur hasil klasifikasi: akurasi

Ukuran paling sederhana adalah **accuracy** (akurasi):

\[
\text{Accuracy} = \frac{\text{jumlah prediksi yang benar}}{\text{jumlah seluruh prediksi}}
\]

Contoh: dari 20 email uji, model menebak 18 dengan benar. Akurasinya \(18 / 20 = 0{,}9\), atau 90%.

!!! warning "Akurasi bisa menipu"
    Bayangkan 99 dari 100 transaksi adalah transaksi wajar. Model yang **selalu** menjawab "wajar" mendapat akurasi 99%, padahal tidak pernah menangkap satu pun penipuan. Ukuran lain seperti *precision* dan *recall* dipakai untuk kasus seperti ini. Topik itu di luar cakupan bab ini.

## Inti sub-bab ini

Classification menebak **kategori** dari daftar kelas yang sudah ditentukan. Ada tiga jenis: binary, multiclass, dan multilabel. Akurasi adalah ukuran paling sederhana, tetapi tidak selalu cukup.

Lanjut ke [Regression](05-regression.md).
