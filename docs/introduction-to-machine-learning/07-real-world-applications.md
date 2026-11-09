# Penerapan Machine Learning di Dunia Nyata

Untuk setiap bidang, kita lihat empat hal: **masalah**, **data masukan**, **tugas belajar**, dan **keluaran yang diharapkan**. Nama jenis tugas (classification, regression, clustering, dll.) dijelaskan di [Jenis Masalah ML](09-machine-learning-problems.md). Anggap saja sekarang sebagai gambaran awal.

## Healthcare (kesehatan)

| Aspek | Penjelasan |
|---|---|
| Masalah | Membantu dokter mendeteksi penyakit lebih dini |
| Data masukan | Hasil laboratorium, gambar rontgen, riwayat pasien |
| Tugas belajar | Classification |
| Keluaran | Pasien berisiko atau tidak berisiko |

## Finance (keuangan)

| Aspek | Penjelasan |
|---|---|
| Masalah | Mendeteksi transaksi kartu kredit yang mencurigakan |
| Data masukan | Jumlah, lokasi, waktu, dan kebiasaan transaksi |
| Tugas belajar | Anomaly detection |
| Keluaran | Tanda transaksi yang tidak wajar |

## Education (pendidikan)

| Aspek | Penjelasan |
|---|---|
| Masalah | Mengenali kelompok siswa dengan pola belajar serupa agar bantuan lebih tepat sasaran |
| Data masukan | Nilai, kehadiran, durasi mengakses materi |
| Tugas belajar | Clustering |
| Keluaran | Kelompok siswa dengan karakter belajar yang mirip |

## Cybersecurity (keamanan siber)

| Aspek | Penjelasan |
|---|---|
| Masalah | Menemukan serangan atau perilaku jaringan yang tidak biasa |
| Data masukan | Log lalu lintas jaringan, jumlah percobaan login |
| Tugas belajar | Anomaly detection atau classification |
| Keluaran | Peringatan aktivitas mencurigakan |

## E-commerce (perdagangan elektronik)

| Aspek | Penjelasan |
|---|---|
| Masalah | Memahami segmen pelanggan untuk promosi yang sesuai |
| Data masukan | Usia, pendapatan, frekuensi dan nilai belanja |
| Tugas belajar | Clustering |
| Keluaran | Segmen pelanggan, misalnya pembelanja hemat atau pembelanja besar |

## Transportation (transportasi)

| Aspek | Penjelasan |
|---|---|
| Masalah | Memperkirakan waktu tiba kendaraan |
| Data masukan | Jarak, jam berangkat, kondisi lalu lintas, cuaca |
| Tugas belajar | Regression |
| Keluaran | Perkiraan waktu tempuh dalam menit |

## Disaster management (penanggulangan bencana)

| Aspek | Penjelasan |
|---|---|
| Masalah | Mengelompokkan wilayah berdasarkan tingkat kerawanan banjir |
| Data masukan | Curah hujan, ketinggian lahan, kedekatan dengan sungai, riwayat kejadian |
| Tugas belajar | Clustering |
| Keluaran | Kelompok wilayah dengan tingkat kerawanan serupa |

## Environmental monitoring (pemantauan lingkungan)

| Aspek | Penjelasan |
|---|---|
| Masalah | Memperkirakan kualitas udara besok |
| Data masukan | Data sensor polusi, suhu, kecepatan angin |
| Tugas belajar | Regression |
| Keluaran | Perkiraan indeks kualitas udara |

!!! note "Satu bidang, banyak tugas"
    Bidang yang sama bisa memakai tugas ML yang berbeda. Misalnya, di kesehatan, pasien juga bisa dikelompokkan (*clustering*) berdasarkan kemiripan gejala. Contoh di atas hanyalah ilustrasi, bukan satu-satunya cara.

Lanjut ke [Workflow Machine Learning](08-machine-learning-workflow.md).
