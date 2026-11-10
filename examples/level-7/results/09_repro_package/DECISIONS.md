# Log keputusan

| id | tahap | jenis | keputusan | alasan |
|---|---|---|---|---|
| D1 | Bab 4 | dikunci | Kriteria data: I1 tidak ada nilai hilang pada 30 fitur | ditulis sebelum diterapkan |
| D2 | Bab 4 | dikunci | Kriteria data: I2 punya label diagnosis (hanya validasi) | ditulis sebelum diterapkan |
| D3 | Bab 4 | dikunci | Kriteria data: E1 bukan baris duplikat persis | ditulis sebelum diterapkan |
| D4 | Bab 4 | dikunci | Kriteria data: E2 fitur yang harus positif bernilai > 0 | ditulis sebelum diterapkan |
| D5 | Bab 5 | dikunci | Praproses baseline: StandardScaler pada ke-30 fitur | ditetapkan di protokol |
| D6 | Bab 5 | dikunci | Praproses outlier: tidak dibuang (keputusan Bab 4) | ditetapkan di protokol |
| D7 | Bab 5 | dikunci | Praproses seleksi_fitur: tidak ada pada analisis utama | ditetapkan di protokol |
| D8 | Bab 5 | dikunci | Kebijakan K_analisis_utama: 2 | ditetapkan di protokol |
| D9 | Bab 5 | dikunci | Kebijakan justifikasi_K: RQ3 membandingkan dengan diagnosis dua kelas; K = 2 adalah asumsi desain, bukan hasil pemilihan; sensitivitas K dilaporkan terpisah | ditetapkan di protokol |
| D10 | Bab 5 | dikunci | Kebijakan label_untuk_tuning: False | ditetapkan di protokol |
| D11 | Bab 5 | pengungkapan | Bab 1 menjalankan demonstrasi K-Means pada data yang sama dan menampilkan ARI terhadap diagnosis sebelum protokol ini ditulis | pengungkapan hal yang sudah dilihat |
| D12 | Bab 5 | pengungkapan | protokol ini karena itu tidak sepenuhnya buta terhadap data; K = 2 dipengaruhi jumlah kelas diagnosis | pengungkapan hal yang sudah dilihat |
| D13 | Bab 6 | klarifikasi | C1: titik noise dikeluarkan saat menghitung Silhouette, Davies-Bouldin, dan Calinski-Harabasz | metrik internal membutuhkan kelompok; noise bukan kelompok |
| D14 | Bab 6 | klarifikasi | C2: label noise (-1) diperlakukan sebagai satu kelompok tambahan pada ARI dan NMI | agar semua titik ikut dihitung dan hasil tidak tampak lebih baik karena noise dibuang |
| D15 | Bab 6 | klarifikasi | C3: StandardScaler dihitung ulang pada tiap subsampel; K-Means memakai seed 42; subsampel diambil tanpa pengembalian dengan generator seed 42 | seluruh alur praproses diulang agar sesuai praktik nyata; protokol hanya menyebut fraksi 0,8 |
| D16 | Bab 6 | klarifikasi | C4: baseline acuan RQ1 dan RQ2 adalah K-Means StandardScaler dengan seed 42, yang sama dengan K-Means pada RQ3 (dihitung sekali) | protokol menyebut random_state dasar 42 tetapi tidak menyebut dari mana acuan diambil |
| D17 | Bab 6 | klarifikasi | C5: jarak ke tetangga ke-k dihitung termasuk titik itu sendiri sebagai tetangga pertama | konsisten dengan cara scikit-learn menghitung min_samples (titik itu sendiri ikut dihitung) |
| D18 | Bab 8 | revisi | Kalimat masalah di Bab 2 diubah dari 'selalu menghasilkan kelompok' menjadi 'berbasis partisi menghasilkan kelompok pada data apa pun' | pemeriksa kata berlebihan menandainya dan DBSCAN tidak menghasilkan kelompok (Bab 6); hash protokol tidak berubah |
