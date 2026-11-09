# Regression

## Definisi sederhana

**Regression** (regresi) adalah jenis Supervised Learning untuk **menebak angka**.

## Penjelasan dengan bahasa sehari-hari

Saat menaksir berapa lama perjalanan ke kampus, kamu tidak memilih dari "cepat" atau "lambat". Kamu menyebut angka: "kira-kira 35 menit". Angka itu bisa 34, 35,5, atau 41. Menebak angka seperti ini adalah regresi.

## Istilah: continuous numerical target

**Continuous numerical target** (target numerik kontinu) adalah target berupa angka yang bisa bernilai **berapa saja** dalam suatu rentang, termasuk pecahan.

- Harga rumah: Rp452.500.000.
- Suhu besok: 31,7 °C.
- Waktu tempuh: 35,5 menit.

Bandingkan dengan klasifikasi yang jawabannya hanya pilihan terbatas.

## Contoh regresi

| Masalah | Fitur | Target (angka) |
|---|---|---|
| Menaksir harga rumah | Luas, kamar, lokasi | Harga (Rp) |
| Memperkirakan penjualan bulan depan | Penjualan bulan lalu, musim, promosi | Jumlah barang terjual |
| Memperkirakan kualitas udara | Data sensor, cuaca | Indeks kualitas udara |
| Menebak nilai ujian | Jam belajar, kehadiran | Nilai (0–100) |

Contoh terakhir sudah kamu coba di [Bab 1](../introduction-to-machine-learning/11-hands-on-introduction.md) dengan *Linear Regression*.

## Algoritma regresi yang umum

| Algoritma | Ide utama dalam satu kalimat |
|---|---|
| **Linear Regression** | Mencari garis lurus (atau bidang datar) yang paling dekat dengan titik-titik data |
| **Decision Tree Regressor** | Seperti Decision Tree, tetapi ujung pohonnya berisi angka, bukan kelas |
| **Random Forest Regressor** | Menggabungkan banyak pohon keputusan lalu merata-ratakan tebakannya agar lebih stabil |
| **Support Vector Regression (SVR)** | Versi SVM untuk menebak angka, dengan toleransi kesalahan tertentu |

## Perbedaan classification dan regression

Kunci pembedanya hanya satu: **bentuk targetnya**.

| Aspek | Classification | Regression |
|---|---|---|
| Bentuk target | Kategori | Angka kontinu |
| Contoh pertanyaan | "Termasuk kelas mana?" | "Berapa nilainya?" |
| Contoh keluaran | "spam", "setosa" | 452,5; 31,7 |
| Contoh ukuran evaluasi | Accuracy | Mean Absolute Error (MAE) |
| Contoh algoritma | Logistic Regression, KNN, Decision Tree | Linear Regression, Random Forest Regressor |

!!! warning "Jebakan: angka belum tentu regresi"
    Kelas bisa ditulis dengan angka, misalnya 0 = setosa, 1 = versicolor, 2 = virginica. Itu tetap **klasifikasi**, karena angka 1,5 tidak bermakna. Tanyakan: "Apakah nilai di antara dua angka masuk akal?" Jika ya, itu regresi. Jika tidak, itu klasifikasi.

## Mengukur hasil regresi: MAE

Kamu sudah mengenal **Mean Absolute Error** di Bab 1:

\[
\text{MAE} = \frac{1}{n}\sum_{i=1}^{n} \left| y_i - \hat{y}_i \right|
\]

Cara membacanya: "rata-rata dari selisih mutlak antara nilai sebenarnya \(y_i\) dan tebakan \(\hat{y}_i\), untuk \(n\) data."

Contoh: harga sebenarnya 500 dan 700 (juta), tebakan model 520 dan 650. Selisihnya 20 dan 50, sehingga \(\text{MAE} = (20 + 50)/2 = 35\). Artinya rata-rata tebakan meleset Rp35 juta.

## Inti sub-bab ini

Regression menebak **angka kontinu**. Bedanya dengan classification terletak pada bentuk target, bukan pada algoritma atau datanya.

Lanjut ke [Unsupervised Learning](06-unsupervised-learning.md).
