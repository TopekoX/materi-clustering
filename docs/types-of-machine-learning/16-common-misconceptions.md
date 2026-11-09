# Miskonsepsi Umum dan Kesalahan Pemula

Berikut kesalahpahaman yang sering muncul saat pertama kali belajar jenis-jenis Machine Learning. Untuk setiap miskonsepsi, ada pemahaman yang benar dan alasannya.

## 1. "Semua Machine Learning membutuhkan labeled data."

**Pemahaman yang benar:** hanya **Supervised Learning** yang membutuhkan label untuk seluruh datanya. Unsupervised Learning tidak memakai label sama sekali. Semi-Supervised hanya butuh sedikit label. Reinforcement Learning memakai **reward**, bukan label.

**Mengapa penting:** jika kamu mengira semua ML butuh label, kamu mungkin menyerah pada data yang sebenarnya sangat berguna, misalnya data transaksi pelanggan yang tidak berlabel.

## 2. "Classification dan clustering itu sama saja."

**Pemahaman yang benar:** keduanya sama-sama menghasilkan kelompok, tetapi:

- **Classification** memasukkan data ke kelas yang **sudah ditentukan** dan belajar dari **contoh berlabel**.
- **Clustering** **menemukan** kelompok dari data **tanpa label**. Kelompoknya tidak bernama, dan jumlahnya harus kita pilih atau perkirakan.

**Contoh:** model klasifikasi buah hanya bisa menjawab "apel", "jeruk", atau "pisang", sesuai labelnya. Clustering mungkin menemukan kelompok "buah merah" yang berisi apel merah dan stroberi, karena keduanya mirip dari sisi warna. Lihat [Clustering](07-clustering.md).

## 3. "Unsupervised Learning berarti tidak ada evaluasi."

**Pemahaman yang benar:** evaluasi tetap ada, hanya **caranya berbeda**. Karena tidak ada kunci jawaban, kita memakai:

- **Ukuran internal**, misalnya seberapa rapat anggota satu cluster dan seberapa jauh antar cluster.
- **Penilaian ahli**, misalnya apakah kelompok pelanggan yang ditemukan masuk akal bagi tim pemasaran.
- **Kegunaan**, misalnya apakah strategi berdasarkan cluster meningkatkan penjualan.

Seluruh Level 5 kurikulum ini membahas evaluasi clustering.

## 4. "Semakin banyak fitur, semakin bagus modelnya."

**Pemahaman yang benar:** tidak selalu. Fitur yang tidak relevan bisa **mengganggu**:

- Pada clustering, fitur yang tidak berhubungan dengan tujuan bisa membuat data yang sebenarnya mirip tampak berjauhan.
- Pada data berdimensi sangat tinggi, jarak antar titik cenderung mirip semua (*curse of dimensionality*), sehingga algoritma berbasis jarak sulit membedakan kelompok.
- Pada supervised learning, terlalu banyak fitur dapat meningkatkan risiko *overfitting*.

Yang penting adalah **fitur yang relevan**, bukan jumlahnya. Lihat [Dimensionality Reduction](08-dimensionality-reduction.md).

## 5. "K-Means otomatis menentukan jumlah cluster yang benar."

**Pemahaman yang benar:** K-Means **selalu** membutuhkan jumlah cluster \(k\) dari kita (`n_clusters`). Jika kamu meminta 5 cluster, K-Means akan memberi 5 cluster, walaupun data sebenarnya hanya punya 2 kelompok alami.

Menentukan \(k\) yang tepat adalah pekerjaan tersendiri, dengan bantuan metode seperti *elbow method* dan *silhouette score* yang akan dipelajari nanti. Beberapa algoritma lain, seperti DBSCAN, memang tidak meminta jumlah cluster, tetapi meminta parameter lain.

## 6. "Reinforcement Learning sama dengan Supervised Learning."

**Pemahaman yang benar:** keduanya sangat berbeda.

| | Supervised | Reinforcement |
|---|---|---|
| Umpan balik | Jawaban benar untuk setiap contoh | Hanya skor reward, sering tertunda |
| Data | Dataset tetap | Dihasilkan dari interaksi agen |
| Keputusan | Berdiri sendiri | Berurutan; tindakan sekarang memengaruhi situasi berikutnya |

Pada RL, agen tidak pernah diberi tahu "tindakan yang benar adalah belok kiri". Ia hanya tahu bahwa hasil akhirnya bagus atau buruk, lalu harus mencari tahu sendiri tindakan mana yang menyebabkannya.

## 7. "Model dengan akurasi tinggi pasti cocok untuk semua masalah."

**Pemahaman yang benar:** akurasi tinggi belum tentu berarti model baik atau tepat.

- **Data tidak seimbang:** jika 99% transaksi wajar, model yang selalu menjawab "wajar" mendapat akurasi 99% tetapi tidak berguna untuk mendeteksi penipuan.
- **Data uji terlalu kecil atau terlalu mudah:** akurasi 100% pada Iris dengan 30 data uji tidak menjamin hasil yang sama pada data lain.
- **Masalah yang salah:** model klasifikasi akurat tidak berguna jika yang sebenarnya dibutuhkan adalah memahami kelompok pelanggan yang belum diketahui.
- **Biaya kesalahan berbeda:** pada diagnosis penyakit, melewatkan pasien yang sakit jauh lebih berbahaya daripada salah menandai pasien sehat.

Selalu tanyakan: **apakah ukuran ini sesuai dengan tujuan masalahnya?**

## Ringkasan

| Miskonsepsi | Yang benar |
|---|---|
| Semua ML butuh label | Hanya supervised yang butuh label penuh |
| Classification = clustering | Classification memakai kelas yang sudah ada; clustering menemukan kelompok |
| Unsupervised tanpa evaluasi | Ada evaluasi, dengan ukuran internal dan penilaian ahli |
| Lebih banyak fitur lebih baik | Fitur relevan lebih penting daripada jumlahnya |
| K-Means memilih \(k\) sendiri | \(k\) ditentukan oleh kita |
| RL = supervised | RL belajar dari reward atas tindakan berurutan |
| Akurasi tinggi = model tepat | Ukuran harus sesuai tujuan dan kondisi data |

Lanjut ke [Latihan](17-exercises.md).
