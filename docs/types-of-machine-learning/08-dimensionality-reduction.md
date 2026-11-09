# Dimensionality Reduction

## Definisi sederhana

**Dimensionality Reduction** (reduksi dimensi) adalah teknik untuk **mengurangi jumlah fitur** dalam data, sambil tetap mempertahankan informasi yang paling penting.

## Apa itu dimensi?

Dalam Machine Learning, **dimensi** = **jumlah fitur** (jumlah kolom yang dipakai).

- Data dengan 2 fitur (pendapatan, usia) disebut data **2 dimensi**. Bisa digambar di kertas sebagai grafik x–y.
- Data dengan 3 fitur bisa dibayangkan sebagai ruang 3 dimensi.
- Data dengan 50 fitur adalah data **50 dimensi**. Kita tidak bisa membayangkan atau menggambarnya secara langsung.

## Apa itu high-dimensional dataset?

**High-dimensional dataset** (dataset berdimensi tinggi) adalah data dengan **sangat banyak fitur**. Contoh:

- Foto berukuran 100 × 100 piksel punya 10.000 nilai piksel. Jika setiap piksel dianggap fitur, ada 10.000 dimensi.
- Hasil survei dengan 80 pertanyaan berarti 80 dimensi.
- Data ekspresi gen bisa memiliki ribuan kolom.

## Mengapa perlu mengurangi dimensi?

Analogi: kamu diminta menceritakan film dua jam kepada teman. Kamu tidak mengulang setiap adegan. Kamu meringkasnya menjadi beberapa kalimat yang tetap menyampaikan inti cerita. Reduksi dimensi melakukan hal serupa pada data.

Alasan praktisnya:

1. **Visualisasi.** Data 50 dimensi bisa diringkas menjadi 2 dimensi agar bisa digambar dan dilihat polanya.
2. **Kecepatan.** Lebih sedikit fitur berarti komputasi lebih cepat.
3. **Mengurangi gangguan.** Fitur yang tidak penting atau berulang bisa membingungkan model.
4. **Mengatasi *curse of dimensionality*.** Saat dimensi sangat banyak, data menjadi "renggang" dan jarak antar titik cenderung mirip semua. Ini menyulitkan algoritma berbasis jarak seperti clustering.

## Feature Selection vs Feature Extraction

Ada dua cara besar untuk mengurangi fitur:

| Cara | Ide | Analogi | Contoh |
|---|---|---|---|
| **Feature Selection** (pemilihan fitur) | **Memilih** sebagian fitur asli dan membuang sisanya | Memilih 5 pemain terbaik dari 20 pemain | Dari 30 kolom, pakai hanya 8 kolom yang paling relevan |
| **Feature Extraction** (ekstraksi fitur) | **Membuat fitur baru** yang merupakan gabungan dari fitur-fitur asli | Membuat jus dari beberapa buah: rasanya gabungan semua buah | PCA mengubah 30 kolom menjadi 3 kolom baru |

Perbedaan pentingnya: pada feature selection, fitur yang tersisa **masih bermakna asli** (misalnya "usia"). Pada feature extraction, fitur baru adalah **campuran** sehingga maknanya perlu ditafsirkan.

!!! note "Catatan istilah"
    Feature selection sering dikerjakan dengan bantuan label (supervised), tetapi bisa juga tanpa label. PCA adalah contoh feature extraction yang **unsupervised**, karena tidak memakai label sama sekali.

## Pengenalan Principal Component Analysis (PCA)

**PCA** adalah metode reduksi dimensi yang paling terkenal.

**Ide intuitifnya:** PCA mencari **arah** di dalam data tempat data paling banyak "menyebar" atau bervariasi. Arah dengan sebaran terbesar disebut **komponen utama pertama** (*first principal component*). Arah terbesar berikutnya, yang tegak lurus dengan arah pertama, adalah komponen utama kedua, dan seterusnya.

Analogi: bayangkan kamu memotret sekelompok orang yang berbaris memanjang. Jika memotret dari samping barisan, semua orang tumpang tindih. Jika memotret dari depan, kamu melihat seluruh barisan dengan jelas. PCA mencari "sudut pandang" terbaik yang memperlihatkan sebaran data sejelas mungkin.

Dengan memakai hanya beberapa komponen utama pertama, kita mendapat data dengan dimensi lebih sedikit, tetapi sebagian besar informasinya tetap terjaga.

!!! info "Matematika PCA ditunda"
    PCA melibatkan konsep aljabar linear seperti variansi, kovarians, dan vektor eigen. Detailnya akan dibahas pada topik tersendiri. Untuk sekarang, cukup pahami idenya: **meringkas banyak fitur menjadi sedikit fitur baru yang paling informatif**.

## Penerapan reduksi dimensi

- Menggambar data berdimensi tinggi dalam grafik 2D untuk melihat apakah ada kelompok.
- Mempercepat algoritma clustering atau klasifikasi pada data dengan ribuan fitur.
- Kompresi gambar.
- Meringkas puluhan pertanyaan survei menjadi beberapa "faktor" pokok.

## Hubungannya dengan clustering

Reduksi dimensi sering dipakai **bersama** clustering:

1. Sebelum clustering, untuk membuang gangguan dan mempercepat proses.
2. Setelah clustering, untuk **memvisualisasikan** hasil cluster dalam grafik 2D.

## Inti sub-bab ini

Dimensi adalah jumlah fitur. Reduksi dimensi meringkas banyak fitur menjadi sedikit fitur, baik dengan **memilih** fitur (selection) maupun **membuat** fitur baru (extraction, misalnya PCA). Tujuannya: visualisasi, kecepatan, dan mengurangi gangguan.

Lanjut ke [Association Rule Learning](09-association-rule-learning.md).
