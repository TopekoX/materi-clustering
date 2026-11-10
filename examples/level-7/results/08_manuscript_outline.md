# Kestabilan dan Keselarasan Eksternal Pengelompokan pada Profil Morfologi Inti Sel: Studi Metodologis dengan Protokol Terkunci pada Satu Dataset Publik

## Abstrak

**Latar belakang.** Algoritma clustering berbasis partisi menghasilkan kelompok pada data apa pun, tetapi belum tentu kelompok itu stabil atau bermakna.

**Tujuan.** Penelitian ini bertujuan mengukur kestabilan pengelompokan terhadap seed dan sampel data; mengukur kepekaan pengelompokan terhadap penyamaan skala dan pilihan algoritma; mengukur keselarasan kelompok dengan diagnosis yang tercatat sebagai validasi eksternal.

**Metode.** Data: Breast Cancer Wisconsin (Diagnostic) (569 sampel, 30 fitur; UCI, CC BY 4.0). Algoritma: KMeans, Agglomerative, GMM, DBSCAN. Praproses StandardScaler. Protokol dikunci dengan hash sebelum eksperimen; label diagnosis hanya untuk validasi.

**Hasil.** Pada 20 seed, ARI rata-rata antar-pasangan K-Means (K = 2) adalah 0,981 (minimum 0,965; 190 pasangan). ARI terhadap baseline: StandardScaler 0,982, tanpa skala 0,496, MinMaxScaler 0,896. Ambang praktis sama adalah 0,95. Delapan konfigurasi DBSCAN semuanya menghasilkan satu kelompok, dengan noise 2,3 sampai 13,2 persen; tidak ada yang valid menurut protokol.

**Kesimpulan.** Pengelompokan K-Means dua kelompok pada data terstandarisasi tampak konsisten terhadap seed dan pengambilan sampel pada dataset ini. Peringkat algoritma berbeda antar jenis metrik: K-Means unggul pada metrik internal, GMM unggul pada ARI dan NMI terhadap diagnosis pada eksekusi utama. Namun pada analisis eksploratori, interval selisih ARI GMM dikurangi K-Means mencakup nol (-0,012 sampai 0,157), sehingga keunggulan GMM tidak jelas melampaui ketidakpastian sampel.

**Keterbatasan.** Hasil berlaku untuk satu dataset (569 sampel) dan konfigurasi yang ditetapkan protokol. K = 2 dipengaruhi jumlah kelas diagnosis, sehingga ARI terhadap diagnosis tidak independen dari pilihan itu.

*Kata abstrak: 234.*

## Pendahuluan

Sumber: 02_research_problem.json; 03_gap_statement.json. Isi utama: Masalah, konteks, celah yang dibatasi, tujuan, pertanyaan. Saran panjang: 500-800 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Kajian pustaka

Sumber: 03_literature_matrix.csv. Isi utama: Dikelompokkan per tema, bukan per makalah. Saran panjang: 600-1000 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Metode

Sumber: 04_dataset_card.json; 05_protocol.json; 05_environment.json. Isi utama: Data, praproses, algoritma, metrik, protokol, hash. Saran panjang: 800-1200 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Hasil

Sumber: 06_rq2_scaling.csv; 06_rq3_algorithms.csv; 07_tables.md. Isi utama: Angka dan pengamatan, tanpa alasan. Saran panjang: 700-1000 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Pembahasan

Sumber: 07_claim_ledger.csv. Isi utama: Interpretasi, hasil tak terduga, hubungan dengan pustaka. Saran panjang: 700-1000 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Keterbatasan

Sumber: 07_claim_ledger.csv. Isi utama: Batas data, metode, protokol, bacaan pustaka. Saran panjang: 200-400 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Kesimpulan

Sumber: 07_claim_ledger.csv. Isi utama: Jawaban terbatas untuk tiap pertanyaan. Saran panjang: 150-300 kata.

[TODO penulis: ditulis dari bagian sumber di atas; skrip tidak menulis prosa ini]

## Tabel konfigurasi eksperimen (untuk bagian Metode)

| Algoritma | Pengaturan | Disetel |
|---|---|---|
| KMeans | n_clusters=2; n_init=10 | tidak |
| Agglomerative | n_clusters=2; linkage=ward | tidak |
| GMM | n_components=2; covariance_type=full; n_init=5 | tidak |
| DBSCAN | min_samples=[5, 10]; eps_kuantil_jarak_tetangga=[0.8, 0.85, 0.9, 0.95] | ya |

## Daftar tabel dan gambar

- **Tabel 1** (07_tables.md): Perbandingan empat algoritma pada K = 2 di ruang baseline terstandarisasi; arah metrik ditulis pada kepala kolom, dan DBSCAN tidak memiliki konfigurasi valid menurut protokol.
- **Tabel 2** (07_tables.md): ARI terhadap baseline menurut perlakuan skala (20 seed per perlakuan); ambang praktis sama ditetapkan 0,95 sebelum eksperimen.
- **Gambar 1** (06-kestabilan-dan-skala.png): Kestabilan K-Means (K = 2) antar-seed dan antar-subsampel, serta ARI terhadap baseline untuk tiga perlakuan skala; garis putus-putus menandai ambang 0,95.
- **Gambar 2** (06-empat-algoritma.png): Proyeksi PCA dua komponen dengan pengelompokan K-Means, Agglomerative, dan GMM; proyeksi hanya untuk visualisasi dan DBSCAN tidak ditampilkan karena tidak ada konfigurasi valid.
- **Gambar 3** (07-ari-dan-ketidakpastian.png): ARI terhadap diagnosis per algoritma dengan interval bootstrap 95 persen (eksploratori) dan ukuran inti sel yang paling berbeda antar dua kelompok K-Means.

## Ketersediaan data dan kode

Data: Breast Cancer Wisconsin (Diagnostic), UCI Machine Learning Repository, DOI 10.24432/C5DW2B, lisensi CC BY 4.0 menurut halaman UCI; salinan yang dipakai dimuat melalui scikit-learn. Pembuat: William Wolberg, Olvi Mangasarian, Nick Street, W. Street. Sidik jari data final: 6b202a2072f9. Protokol dikunci dengan hash SHA-256 c65be407e00ab39b...; seluruh kode dan berkas hasil tersedia di [TAUTAN REPOSITORI: diisi penulis].

## Pernyataan etik

Data publik berlisensi CC BY 4.0. Persetujuan etik dan status de-identifikasi tidak dinyatakan pada sumber yang dibaca. Penelitian ini tidak membuat klaim klinis.

## Referensi

- von Luxburg, Williamson, & Guyon (2012). https://proceedings.mlr.press/v27/luxburg12a.html (dibaca: abstrak)
- Hennig (2015). https://arxiv.org/abs/1502.02555 (dibaca: ringkasan halaman arXiv)
- Ben-Hur, Elisseeff, & Guyon (2002). Pacific Symposium on Biocomputing 7:6-17 (2002) (dibaca: ringkasan hasil pencarian)
- Vinh, Epps, & Bailey (2010). https://jmlr.org/papers/v11/vinh10a.html (dibaca: ringkasan halaman JMLR)
- Jain (2010). https://doi.org/10.1016/j.patrec.2009.09.011 (dibaca: ringkasan hasil pencarian)
