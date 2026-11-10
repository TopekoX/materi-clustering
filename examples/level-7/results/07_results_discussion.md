**Hasil**

- (H1) Pada 20 seed, ARI rata-rata antar-pasangan K-Means (K = 2) adalah 0,981 (minimum 0,965; 190 pasangan).
- (H2) Pada 50 subsampel (80 persen), ARI rata-rata terhadap pengelompokan data penuh adalah 0,964 dengan rentang 0,871 sampai 1,000.
- (H3) ARI terhadap baseline: StandardScaler 0,982, tanpa skala 0,496, MinMaxScaler 0,896. Ambang praktis sama adalah 0,95.
- (H4) Silhouette: K-Means 0,343, Agglomerative 0,339, GMM 0,314. ARI terhadap diagnosis: K-Means 0,654, Agglomerative 0,575, GMM 0,774.
- (H5) Delapan konfigurasi DBSCAN semuanya menghasilkan satu kelompok, dengan noise 2,3 sampai 13,2 persen; tidak ada yang valid menurut protokol.
- (H6) Pada K-Means baseline, proporsi malignant adalah 0,096 pada kelompok 0 (375 titik) dan 0,907 pada kelompok 1 (194 titik).
- (H7) (Eksploratori) Selisih ARI terhadap diagnosis, GMM dikurangi K-Means, memiliki interval bootstrap 95 persen -0,012 sampai 0,157; K-Means dikurangi Agglomerative -0,112 sampai 0,278.
- (H8) (Eksploratori) Pada data tanpa skala, dua fitur dengan varians terbesar menyumbang 99,1 persen dari total varians.

**Interpretasi**

- (I1) Pengelompokan K-Means dua kelompok pada data terstandarisasi tampak konsisten terhadap seed dan pengambilan sampel pada dataset ini.
- (I2) Konsisten tidak sama dengan bermakna: hasil ini tidak menunjukkan bahwa kelompok mencerminkan kategori nyata.
- (I3) Cara menyamakan skala mengubah pengelompokan pada data ini: tanpa skala (0,496) jauh berbeda dari baseline, dan MinMaxScaler (0,896) pun tidak memenuhi ambang praktis sama (0,95).
- (I4) Dugaan: pada data tanpa skala, jarak didominasi beberapa fitur berskala besar. Dua fitur teratas menyumbang 99,1 persen dari total varians, sejalan dengan dugaan ini, tetapi dugaan belum diuji langsung.
- (I5) Peringkat algoritma berbeda antar jenis metrik: K-Means unggul pada metrik internal, GMM unggul pada ARI dan NMI terhadap diagnosis pada eksekusi utama. Namun pada analisis eksploratori, interval selisih ARI GMM dikurangi K-Means mencakup nol (-0,012 sampai 0,157), sehingga keunggulan GMM tidak jelas melampaui ketidakpastian sampel.
- (I6) Tidak ada algoritma yang dapat dinyatakan unggul secara umum tanpa menyebut tujuan evaluasinya.
- (I7) Kelompok 1 pada K-Means ditandai nilai tinggi pada fitur kontur dan ukuran (concavity, concave points, perimeter), dan memuat proporsi malignant yang tinggi; ini deskripsi keselarasan, bukan penjelasan sebab.
- (I8) Dugaan: kepadatan titik pada 30 dimensi terstandarisasi relatif seragam sehingga DBSCAN tidak menemukan kelompok terpisah. Dugaan ini belum diuji.

**Pembahasan terhadap penelitian terdahulu**

- (P1) Gagasan bahwa pengelompokan yang baik seharusnya stabil terhadap gangguan data (Ben-Hur dkk., 2002) sejalan dengan cara RQ1 diukur; hasil RQ1 konsisten dengan gagasan itu, tetapi tidak membuktikan adanya struktur kelompok.
- (P2) Perbedaan peringkat antara metrik internal dan eksternal sejalan dengan pandangan bahwa evaluasi clustering bergantung pada konteks dan tujuan (von Luxburg dkk., 2012; Hennig, 2015).
- (P3) ARI dan NMI yang dikoreksi untuk kebetulan (Vinh dkk., 2010) dipakai pada validasi eksternal; dengan 569 titik dan dua kelompok, koreksi ini tidak menjadi masalah utama.
- (P4) Angka penelitian ini tidak dibandingkan dengan angka makalah lain karena tidak ada makalah pada matriks Bab 3 yang memakai data, protokol, dan metrik yang sama.

**Keterbatasan**

- (K1) Hasil berlaku untuk satu dataset (569 sampel) dan konfigurasi yang ditetapkan protokol.
- (K2) K = 2 dipengaruhi jumlah kelas diagnosis, sehingga ARI terhadap diagnosis tidak independen dari pilihan itu.
- (K3) Protokol ditulis setelah demonstrasi Bab 1 pada data yang sama, sehingga tidak sepenuhnya buta terhadap data.
- (K4) Hanya DBSCAN yang disetel, sehingga upaya penyetelan antar algoritma tidak setara.
- (K5) Tinjauan pustaka bersifat terarah dan kelima sumber hanya dibaca abstrak atau ringkasannya.
- (K6) Persetujuan etik dan status de-identifikasi data tidak diketahui; tidak ada klaim klinis.
- (K7) Analisis bootstrap dan pangsa varians bersifat eksploratori dan tidak ada di protokol.
