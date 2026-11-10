# Kestabilan dan Keselarasan Eksternal Pengelompokan pada Profil Morfologi Inti Sel: Studi Metodologis dengan Protokol Terkunci pada Satu Dataset Publik

*Laporan proyek akhir Level 7 (17 bagian). Setiap bagian diberi label status isi.*

## 1. Judul penelitian

*Status isi: DOKUMENTASI. Sumber: 08_manuscript_outline.md.*

Kestabilan dan Keselarasan Eksternal Pengelompokan pada Profil Morfologi Inti Sel: Studi Metodologis dengan Protokol Terkunci pada Satu Dataset Publik

## 2. Latar belakang dan masalah penelitian

*Status isi: RENCANA DAN PROTOKOL. Sumber: 02_research_problem.json.*

Algoritma clustering berbasis partisi menghasilkan kelompok pada data apa pun, tetapi belum tentu kelompok itu stabil atau bermakna.

Kontribusi yang dinyatakan: didaktik dan metodologis: mendemonstrasikan protokol penelitian clustering yang bisa diulang. Tidak mengklaim kebaruan ilmiah.

## 3. Tujuan dan pertanyaan penelitian

*Status isi: RENCANA DAN PROTOKOL. Sumber: 02_research_problem.json.*

Tujuan:
- Mengukur kestabilan pengelompokan terhadap seed dan sampel data.
- Mengukur kepekaan pengelompokan terhadap penyamaan skala dan pilihan algoritma.
- Mengukur keselarasan kelompok dengan diagnosis yang tercatat sebagai validasi eksternal.

Pertanyaan:
- RQ1: Seberapa stabil pengelompokan K-Means pada 30 fitur morfologi bila seed dan sampel data diubah?
- RQ2: Apakah pengelompokan pada 30 fitur morfologi berubah bila fitur tidak distandarkan, dan seberapa besar perubahannya (ARI)?
- RQ3: Seberapa selaras pengelompokan tak terawasi pada profil morfologi dengan diagnosis yang tercatat (ARI dan NMI)?

## 4. Matriks tinjauan pustaka

*Status isi: TINJAUAN PUSTAKA TERBATAS. Sumber: 03_literature_matrix.csv; Bab 10.*

| id | referensi | topik | dibaca |
|---|---|---|---|
| L1 | von Luxburg, Williamson, & Guyon (2012) | konteks-evaluasi | abstrak |
| L2 | Hennig (2015) | konteks-evaluasi | ringkasan halaman arXiv |
| L3 | Ben-Hur, Elisseeff, & Guyon (2002) | kestabilan | ringkasan hasil pencarian |
| L4 | Vinh, Epps, & Bailey (2010) | pembanding-partisi | ringkasan halaman JMLR |
| L5 | Jain (2010) | tinjauan-umum | ringkasan hasil pencarian |
| L6 | Milligan & Cooper (1988) | sensitivitas-praproses | ringkasan hasil pencarian |
| L7 | Steinley (2004) | sensitivitas-praproses | ringkasan hasil pencarian |

Dibaca penuh: 0 dari 7. Cakupan per pertanyaan: {'RQ1': 1, 'RQ2': 2, 'RQ3': 1}.

## 5. Celah riset dan kontribusi

*Status isi: TINJAUAN PUSTAKA TERBATAS. Sumber: Bab 3 dan 10.*

Dari 7 sumber yang ditelaah berdasarkan abstrak atau ringkasan, tidak satu pun yang kami baca menyajikan protokol terpadu yang mengukur kestabilan, kepekaan terhadap praproses, dan keselarasan eksternal pada satu dataset publik dengan seluruh konfigurasi dibagikan. Ini bukan klaim bahwa studi serupa tidak ada; tinjauan ini terarah, bukan sistematis.

Kontribusi: didaktik dan metodologis: mendemonstrasikan protokol penelitian clustering yang bisa diulang. Tidak mengklaim kebaruan ilmiah.

## 6. Pemilihan dan deskripsi dataset

*Status isi: DOKUMENTASI. Sumber: 04_dataset_card.json.*

- Dataset: Breast Cancer Wisconsin (Diagnostic) (569 sampel, 30 fitur)
- Sumber: UCI Machine Learning Repository, DOI 10.24432/C5DW2B, lisensi CC BY 4.0 menurut halaman UCI
- Baris dikeluarkan oleh kriteria: 0
- Sidik jari data final: 6b202a2072f9
- Persetujuan etik dan de-identifikasi: tidak dinyatakan pada sumber yang dibaca; tidak ada klaim klinis

## 7. Metodologi penelitian

*Status isi: RENCANA DAN PROTOKOL. Sumber: 05_protocol.json.*

- RQ1: faktor seed dan sampel data
- RQ2: faktor perlakuan skala fitur
- RQ3: faktor algoritma
- sensitivitas_K: faktor jumlah kelompok K

Protokol dikunci sebelum eksperimen (SHA-256 c65be407e00ab39b...). Pengungkapan:
- Bab 1 menjalankan demonstrasi K-Means pada data yang sama dan menampilkan ARI terhadap diagnosis sebelum protokol ini ditulis
- protokol ini karena itu tidak sepenuhnya buta terhadap data; K = 2 dipengaruhi jumlah kelas diagnosis

## 8. Praproses data

*Status isi: RENCANA DAN PROTOKOL. Sumber: 05_protocol.json; 06_clarifications.json.*

- baseline: StandardScaler pada ke-30 fitur
- outlier: tidak dibuang (keputusan Bab 4)
- seleksi_fitur: tidak ada pada analisis utama
- StandardScaler dihitung ulang pada tiap subsampel; K-Means memakai seed 42; subsampel diambil tanpa pengembalian dengan generator seed 42

## 9. Implementasi clustering

*Status isi: RENCANA DAN PROTOKOL. Sumber: 05_protocol.json; 06_run_manifest.json.*

| Algoritma | Pengaturan | Disetel |
|---|---|---|
| KMeans | n_clusters=2; n_init=10 | tidak |
| Agglomerative | n_clusters=2; linkage=ward | tidak |
| GMM | n_components=2; covariance_type=full; n_init=5 | tidak |
| DBSCAN | min_samples=[5, 10]; eps_kuantil_jarak_tetangga=[0.8, 0.85, 0.9, 0.95] | ya |

Eksekusi dijalankan: 156 dari 156 ({'RQ1': 70, 'RQ2': 60, 'RQ3': 11, 'K': 15}). Klarifikasi implementasi: 5.

## 10. Desain eksperimen

*Status isi: RENCANA DAN PROTOKOL. Sumber: 05_protocol.json.*

- RQ1: faktor seed dan sampel data; metrik ARI antar-seed, ARI pengelompokan subsampel vs data penuh
- RQ2: faktor perlakuan skala fitur; metrik ARI vs baseline
- RQ3: faktor algoritma; metrik ARI vs diagnosis, NMI vs diagnosis
- sensitivitas_K: faktor jumlah kelompok K; metrik Silhouette

Ambang praktis sama (ARI): 0,95, ditetapkan sebelum eksperimen.

## 11. Evaluasi

*Status isi: RENCANA DAN PROTOKOL. Sumber: 05_protocol.json.*

Metrik internal (Silhouette naik lebih baik, Davies-Bouldin turun lebih baik, Calinski-Harabasz naik lebih baik) dihitung di ruang baseline. ARI dan NMI terhadap diagnosis dipakai hanya sebagai validasi eksternal, bukan target optimasi.

## 12. Visualisasi hasil

*Status isi: TEMUAN EKSPERIMEN. Sumber: docs/assets/level-7/.*

- 06-kestabilan-dan-skala.png (ada: True)
- 06-empat-algoritma.png (ada: True)
- 06-sensitivitas-k-dan-dbscan.png (ada: True)
- 07-ari-dan-ketidakpastian.png (ada: True)

## 13. Profil kelompok

*Status isi: TEMUAN EKSPERIMEN. Sumber: 06_cluster_profile.csv; 07_profile_by_measure.csv.*

Pada K-Means baseline, proporsi malignant adalah 0,096 pada kelompok 0 (375 titik) dan 0,907 pada kelompok 1 (194 titik).

Ukuran inti sel yang paling berbeda antar kelompok: concave points (1,53), perimeter (1,43), concavity (1,42); paling mirip: texture (0,50). Ini deskripsi, bukan penjelasan sebab.

## 14. Hasil dan pembahasan

*Status isi: TEMUAN EKSPERIMEN. Sumber: 07_claim_ledger.csv; Bab 10.*

Hasil:
- (H1) Pada 20 seed, ARI rata-rata antar-pasangan K-Means (K = 2) adalah 0,981 (minimum 0,965; 190 pasangan).
- (H2) Pada 50 subsampel (80 persen), ARI rata-rata terhadap pengelompokan data penuh adalah 0,964 dengan rentang 0,871 sampai 1,000.
- (H3) ARI terhadap baseline: StandardScaler 0,982, tanpa skala 0,496, MinMaxScaler 0,896. Ambang praktis sama adalah 0,95.
- (H4) Silhouette: K-Means 0,343, Agglomerative 0,339, GMM 0,314. ARI terhadap diagnosis: K-Means 0,654, Agglomerative 0,575, GMM 0,774.
- (H5) Delapan konfigurasi DBSCAN semuanya menghasilkan satu kelompok, dengan noise 2,3 sampai 13,2 persen; tidak ada yang valid menurut protokol.
- (H6) Pada K-Means baseline, proporsi malignant adalah 0,096 pada kelompok 0 (375 titik) dan 0,907 pada kelompok 1 (194 titik).
- (H7) (Eksploratori) Selisih ARI terhadap diagnosis, GMM dikurangi K-Means, memiliki interval bootstrap 95 persen -0,012 sampai 0,157; K-Means dikurangi Agglomerative -0,112 sampai 0,278.
- (H8) (Eksploratori) Pada data tanpa skala, dua fitur dengan varians terbesar menyumbang 99,1 persen dari total varians.

Interpretasi:
- (I1) Pengelompokan K-Means dua kelompok pada data terstandarisasi tampak konsisten terhadap seed dan pengambilan sampel pada dataset ini.
- (I2) Konsisten tidak sama dengan bermakna: hasil ini tidak menunjukkan bahwa kelompok mencerminkan kategori nyata.
- (I3) Cara menyamakan skala mengubah pengelompokan pada data ini: tanpa skala (0,496) jauh berbeda dari baseline, dan MinMaxScaler (0,896) pun tidak memenuhi ambang praktis sama (0,95).
- (I4) Dugaan: pada data tanpa skala, jarak didominasi beberapa fitur berskala besar. Dua fitur teratas menyumbang 99,1 persen dari total varians, sejalan dengan dugaan ini, tetapi dugaan belum diuji langsung.
- (I5) Peringkat algoritma berbeda antar jenis metrik: K-Means unggul pada metrik internal, GMM unggul pada ARI dan NMI terhadap diagnosis pada eksekusi utama. Namun pada analisis eksploratori, interval selisih ARI GMM dikurangi K-Means mencakup nol (-0,012 sampai 0,157), sehingga keunggulan GMM tidak jelas melampaui ketidakpastian sampel.
- (I6) Tidak ada algoritma yang dapat dinyatakan unggul secara umum tanpa menyebut tujuan evaluasinya.
- (I7) Kelompok 1 pada K-Means ditandai nilai tinggi pada fitur kontur dan ukuran (concavity, concave points, perimeter), dan memuat proporsi malignant yang tinggi; ini deskripsi keselarasan, bukan penjelasan sebab.
- (I8) Dugaan: kepadatan titik pada 30 dimensi terstandarisasi relatif seragam sehingga DBSCAN tidak menemukan kelompok terpisah. Dugaan ini belum diuji.

Pembahasan terhadap penelitian terdahulu:
- (P1) Gagasan bahwa pengelompokan yang baik seharusnya stabil terhadap gangguan data (Ben-Hur dkk., 2002) sejalan dengan cara RQ1 diukur; hasil RQ1 konsisten dengan gagasan itu, tetapi tidak membuktikan adanya struktur kelompok.
- (P2) Perbedaan peringkat antara metrik internal dan eksternal sejalan dengan pandangan bahwa evaluasi clustering bergantung pada konteks dan tujuan (von Luxburg dkk., 2012; Hennig, 2015).
- (P3) ARI dan NMI yang dikoreksi untuk kebetulan (Vinh dkk., 2010) dipakai pada validasi eksternal; dengan 569 titik dan dua kelompok, koreksi ini tidak menjadi masalah utama.
- (P4) Angka penelitian ini tidak dibandingkan dengan angka makalah lain karena tidak ada makalah pada matriks Bab 3 yang memakai data, protokol, dan metrik yang sama.
- (P5, Bab 10) Hasil RQ2 sejalan dengan gagasan bahwa pilihan cara standardisasi memengaruhi pengelompokan (Milligan & Cooper, 1988; Steinley, 2004; berdasarkan ringkasan hasil pencarian, bukan teks lengkap). Kami tidak menilai cara standardisasi mana yang lebih baik, karena tidak ada kebenaran dasar pada clustering.

Uji lanjutan:
- (Eksploratori, Bab 10) Uji langsung dugaan I4. Pada K-Means tanpa skala, ARI terhadap pengelompokan yang hanya memakai worst area adalah 1,000, terhadap dua fitur area 0,992, dan terhadap pengelompokan tanpa kedua fitur area 0,849. Pada dataset ini pengelompokan tanpa skala tampak ditentukan oleh worst area, sehingga dugaan I4 didukung; ini tidak menunjukkan hal yang sama pada data lain.

## 15. Kesimpulan penelitian

*Status isi: TEMUAN EKSPERIMEN. Sumber: Bab 6 dan 7.*

- RQ1: pada dataset ini K-Means (K = 2, data terstandarisasi) tampak konsisten terhadap seed (ARI rata-rata 0,981) dan subsampel (0,964; minimum 0,871).
- RQ2: cara menyamakan skala mengubah pengelompokan; ARI terhadap baseline 0,496 tanpa skala dan 0,896 dengan MinMaxScaler, di bawah ambang 0,95.
- RQ3: pengelompokan cukup selaras dengan diagnosis (ARI 0,575 sampai 0,774), peringkat algoritma berbeda antar jenis metrik, selisih ARI antar-algoritma tidak jelas melampaui ketidakpastian sampel (eksploratori), dan DBSCAN tidak memiliki konfigurasi valid.

## 16. Keterbatasan dan pekerjaan lanjutan

*Status isi: KETERBATASAN DAN RENCANA LANJUTAN. Sumber: 07_claim_ledger.csv.*

Keterbatasan:
- (K1) Hasil berlaku untuk satu dataset (569 sampel) dan konfigurasi yang ditetapkan protokol.
- (K2) K = 2 dipengaruhi jumlah kelas diagnosis, sehingga ARI terhadap diagnosis tidak independen dari pilihan itu.
- (K3) Protokol ditulis setelah demonstrasi Bab 1 pada data yang sama, sehingga tidak sepenuhnya buta terhadap data.
- (K4) Hanya DBSCAN yang disetel, sehingga upaya penyetelan antar algoritma tidak setara.
- (K5) Tinjauan pustaka bersifat terarah dan kelima sumber hanya dibaca abstrak atau ringkasannya.
- (K6) Persetujuan etik dan status de-identifikasi data tidak diketahui; tidak ada klaim klinis.
- (K7) Analisis bootstrap dan pangsa varians bersifat eksploratori dan tidak ada di protokol.

Pekerjaan lanjutan:
| Pekerjaan lanjutan | Cara mengujinya |
|---|---|
| Uji dugaan kepadatan seragam pada DBSCAN | Bandingkan sebaran jarak tetangga terdekat; coba kerangka grid yang ditetapkan lewat amendment |
| Baca teks lengkap ketujuh sumber | Isi kolom keterbatasan dan perbarui pembahasan pustaka |
| Uji pada dataset lain (replicability) | Terapkan protokol yang sama pada dataset berlisensi jelas |
| Seleksi fitur untuk mengurangi redundansi | Bandingkan dengan seluruh fitur memakai ARI antar-pengelompokan |
| Tinjauan pustaka sistematis | Tetapkan kueri dan kriteria inklusi lebih dulu, lalu laporkan alur seleksi |

## 17. Dokumentasi reproduksibilitas

*Status isi: DOKUMENTASI. Sumber: 09_package_checklist.csv; 09_repro_package/.*

Paket reproduksi: 6 berkas di results/09_repro_package/. Daftar periksa Bab 9: {'LULUS': 8, 'PERINGATAN': 1}. Uji keterulangan: skrip Bab 1 sampai 8 diulang dan 67 berkas dibandingkan (lihat output Bab 9). Peringatan yang tersisa: kode belum di-commit dan tautan repositori belum ditentukan.

## Peta status isi

| isi | bab | label |
|---|---|---|
| Demonstrasi tiga pertanyaan riset pada data yang sama | Bab 1 | ILUSTRASI DIDAKTIK |
| Contoh pertanyaan baik dan buruk, pemeriksa kata kunci | Bab 2 | ILUSTRASI DIDAKTIK |
| Matriks pustaka (abstrak atau ringkasan) | Bab 3 dan 10 | TINJAUAN PUSTAKA TERBATAS |
| Kartu data, kriteria, etika | Bab 4 | DOKUMENTASI |
| Protokol terkunci (156 eksekusi) | Bab 5 | RENCANA DAN PROTOKOL |
| RQ1 kestabilan | Bab 6 | TEMUAN EKSPERIMEN |
| RQ2 kepekaan skala | Bab 6 | TEMUAN EKSPERIMEN |
| RQ3 perbandingan algoritma dan validasi | Bab 6 | TEMUAN EKSPERIMEN |
| Sensitivitas K dan grid DBSCAN | Bab 6 | TEMUAN EKSPERIMEN |
| Profil kelompok | Bab 6 | TEMUAN EKSPERIMEN |
| Bootstrap ARI | Bab 7 | EKSPLORATORI |
| Pangsa varians fitur | Bab 7 | EKSPLORATORI |
| Uji dominasi fitur berskala besar | Bab 10 | EKSPLORATORI |
| Kerangka naskah dan daftar periksa penulisan | Bab 8 | DOKUMENTASI |
| Paket reproduksi dan uji keterulangan | Bab 9 | DOKUMENTASI |
