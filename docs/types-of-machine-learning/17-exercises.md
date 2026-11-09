# Latihan

Kerjakan semua soal terlebih dahulu. Kunci jawaban dan pembahasan ada di bagian [Kunci Jawaban](#kunci-jawaban) di akhir halaman, dalam kotak yang harus dibuka.

## A. Latihan konseptual

### Pilihan ganda

**1.** Data yang memiliki kolom jawaban untuk setiap baris disebut ...

- a. unlabeled data
- b. labeled data
- c. reinforcement data
- d. feature data

**2.** Kolom yang ingin ditebak oleh model disebut ...

- a. feature
- b. cluster
- c. target variable
- d. centroid

**3.** Menebak harga mobil bekas dari tahun pembuatan dan jarak tempuh termasuk ...

- a. classification
- b. clustering
- c. regression
- d. association rule learning

**4.** Menentukan apakah sebuah foto berisi kucing, anjing, atau burung (satu jawaban per foto) termasuk ...

- a. binary classification
- b. multiclass classification
- c. multilabel classification
- d. regression

**5.** Ciri utama Unsupervised Learning adalah ...

- a. memakai reward dari lingkungan
- b. memakai data dengan label lengkap
- c. memakai data tanpa label
- d. selalu menghasilkan angka

**6.** Pada K-Means, siapa yang menentukan jumlah cluster?

- a. algoritma, secara otomatis
- b. pengguna, melalui parameter `n_clusters`
- c. jumlah fitur dalam data
- d. jumlah baris dalam data

**7.** PCA adalah contoh ...

- a. feature selection
- b. feature extraction
- c. classification
- d. reinforcement learning

**8.** Dalam Association Rule Learning, ukuran yang menunjukkan apakah hubungan dua item lebih kuat dari kebetulan adalah ...

- a. support
- b. confidence
- c. lift
- d. accuracy

**9.** Pendekatan yang paling cocok ketika hanya 2% data yang berlabel adalah ...

- a. supervised learning dengan seluruh data
- b. semi-supervised learning
- c. reinforcement learning
- d. association rule learning

**10.** Dalam Reinforcement Learning, strategi agen untuk memilih tindakan di setiap keadaan disebut ...

- a. reward
- b. episode
- c. policy
- d. environment

### Jawaban singkat

**11.** Jelaskan perbedaan *feature* dan *label* dengan satu contoh buatanmu sendiri.

**12.** Mengapa clustering tidak membutuhkan label?

**13.** Sebutkan dua alasan mengapa labeled data sering mahal.

**14.** Apa perbedaan *exploration* dan *exploitation* dalam Reinforcement Learning?

**15.** Apa perbedaan `fit()`, `predict()`, dan `fit_predict()` pada K-Means?

## B. Latihan analitis

Untuk setiap skenario, tentukan **jenis Machine Learning** yang paling cocok dan **jelaskan alasanmu** (label, keluaran, dan tujuan).

**16.** Sebuah rumah sakit punya 10.000 data pasien lengkap dengan hasil diagnosis akhir "diabetes" atau "tidak diabetes". Rumah sakit ingin memperkirakan risiko pasien baru.

**17.** Sebuah dinas pariwisata punya data 500 desa wisata: jumlah pengunjung, jarak dari kota, jumlah homestay, dan rata-rata pengeluaran wisatawan. Mereka ingin tahu apakah desa-desa ini membentuk beberapa tipe yang berbeda, agar program pembinaannya bisa disesuaikan.

**18.** Sebuah perusahaan logistik ingin memperkirakan berapa menit keterlambatan pengiriman berdasarkan jarak, cuaca, dan jam berangkat. Mereka punya data 2 tahun beserta keterlambatan sebenarnya.

**19.** Sebuah perusahaan game ingin membuat karakter lawan yang belajar bermain lebih baik dengan memainkan game itu ribuan kali melawan dirinya sendiri.

**20.** Sebuah toko buku online punya 1 juta riwayat pesanan. Mereka ingin membuat fitur "pembeli buku ini juga membeli ...".

## C. Latihan praktik

### Latihan 21: Klasifikasi

Gunakan pola dari [Praktik Supervised Learning](14-python-supervised-learning.md) pada dataset **Wine** dari Scikit-learn (`load_wine`).

1. Muat dataset dengan `load_wine(as_frame=True)`.
2. Tampilkan ukuran `X` dan jumlah kelas di `y`.
3. Bagi data dengan `test_size=0.25`, `random_state=42`, dan `stratify=y`.
4. Latih `DecisionTreeClassifier(random_state=42)` (impor dari `sklearn.tree`).
5. Hitung akurasi pada data uji.

### Latihan 22: Clustering

Gunakan data pelanggan dari [Praktik Unsupervised Learning](15-python-unsupervised-learning.md).

1. Jalankan K-Means dengan `n_clusters=2`, lalu dengan `n_clusters=4` (tetap `n_init=10`, `random_state=42`).
2. Untuk setiap nilai \(k\), tampilkan rata-rata pendapatan, rata-rata skor belanja, dan jumlah anggota tiap cluster.
3. Bandingkan dengan hasil \(k = 3\). Mana yang paling masuk akal untuk data ini, dan mengapa?

---

## Kunci Jawaban

??? success "Kunci A. Pilihan ganda (1–10)"
    | No | Jawaban | Pembahasan |
    |---|---|---|
    | 1 | b | Labeled data punya kolom jawaban |
    | 2 | c | Target variable adalah kolom yang ditebak |
    | 3 | c | Harga adalah angka kontinu, sehingga termasuk regression |
    | 4 | b | Lebih dari dua kelas, satu jawaban per data |
    | 5 | c | Unsupervised tidak memakai label |
    | 6 | b | K-Means tidak menentukan \(k\) sendiri |
    | 7 | b | PCA membuat fitur baru dari gabungan fitur asli |
    | 8 | c | Lift > 1 berarti hubungan lebih kuat dari kebetulan |
    | 9 | b | Sedikit label + banyak data tanpa label |
    | 10 | c | Policy adalah strategi memilih tindakan |

??? success "Kunci A. Jawaban singkat (11–15)"
    **11.** Contoh: menebak kelulusan mahasiswa. *Feature* adalah informasi yang dipakai untuk menebak, misalnya IPK dan kehadiran. *Label* adalah jawaban yang ingin ditebak, misalnya "lulus tepat waktu" atau "tidak".

    **12.** Karena tujuan clustering adalah **menemukan** kelompok yang belum diketahui berdasarkan kemiripan antar data. Jika labelnya sudah ada, kita tidak perlu mencari kelompok.

    **13.** Contoh alasan: membutuhkan ahli (misalnya dokter untuk gambar medis), membutuhkan banyak waktu (melabeli ribuan data satu per satu), dan membutuhkan biaya. Kadang jawaban yang benar juga belum diketahui siapa pun.

    **14.** *Exploitation* memilih tindakan yang sudah diketahui memberi reward bagus. *Exploration* mencoba tindakan baru yang belum diketahui hasilnya, karena mungkin lebih baik. Agen perlu menyeimbangkan keduanya.

    **15.** `fit(X)` melatih model, yaitu mencari posisi centroid. `predict(X_baru)` memasukkan data ke centroid terdekat tanpa mengubah centroid. `fit_predict(X)` melatih lalu langsung mengembalikan nomor cluster untuk data yang sama.

??? success "Kunci B. Latihan analitis (16–20)"
    **16. Supervised, Classification (binary).** Ada label historis (diagnosis akhir), dan keluarannya kategori dua pilihan.

    **17. Unsupervised, Clustering.** Tidak ada label tipe desa, dan tujuannya menemukan kelompok desa yang mirip. Hasilnya perlu ditafsirkan oleh dinas, misalnya "desa ramai dekat kota" atau "desa terpencil dengan pengeluaran tinggi". Catatan: skala fitur sangat berbeda (jarak dalam km, pengeluaran dalam rupiah), sehingga perlu disamakan dulu.

    **18. Supervised, Regression.** Ada data keterlambatan sebenarnya (label), dan keluarannya angka (menit).

    **19. Reinforcement Learning.** Tidak ada "jawaban benar" untuk setiap langkah, tetapi ada reward berupa menang atau kalah, dan agen belajar dari ribuan percobaan dalam lingkungan game.

    **20. Unsupervised, Association Rule Learning** (market basket analysis). Data berupa transaksi, dan tujuannya menemukan buku yang sering dibeli bersama. Periksa *lift* agar rekomendasi tidak hanya menampilkan buku yang memang populer.

??? success "Kunci C. Latihan 21: Klasifikasi"
    ```python
    from sklearn.datasets import load_wine
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier

    wine = load_wine(as_frame=True)
    X = wine.data
    y = wine.target
    print("Ukuran X:", X.shape)
    print("Jumlah kelas:", y.nunique())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Akurasi: {accuracy_score(y_test, y_pred):.2f}")
    ```

    Output:

    ```text
    Ukuran X: (178, 13)
    Jumlah kelas: 3
    Akurasi: 0.96
    ```

    **Pembahasan:** dataset Wine punya 178 sampel anggur, 13 fitur hasil analisis kimia, dan 3 kelas. Decision Tree menebak sekitar 96% data uji dengan benar. `y.nunique()` menghitung jumlah nilai unik di kolom label.

??? success "Kunci C. Latihan 22: Clustering"
    ```python
    import pandas as pd
    from sklearn.cluster import KMeans

    pelanggan = pd.DataFrame({
        "pendapatan": [15, 16, 17, 18, 19, 20, 55, 57, 60, 62, 58, 61,
                       90, 95, 92, 98, 94, 99],
        "skor_belanja": [80, 85, 78, 90, 82, 88, 50, 45, 52, 48, 55, 47,
                         15, 20, 12, 18, 10, 22],
    })
    X = pelanggan[["pendapatan", "skor_belanja"]]

    for k in (2, 4):
        kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
        pelanggan["cluster"] = kmeans.fit_predict(X)
        print(f"k = {k}")
        print(pelanggan.groupby("cluster")[["pendapatan", "skor_belanja"]]
              .agg(["mean", "count"]).round(1))
    ```

    Output:

    ```text
    k = 2
            pendapatan       skor_belanja      
                  mean count         mean count
    cluster                                    
    0             76.8    12         32.8    12
    1             17.5     6         83.8     6
    k = 4
            pendapatan       skor_belanja      
                  mean count         mean count
    cluster                                    
    0             58.8     6         49.5     6
    1             97.3     3         20.0     3
    2             17.5     6         83.8     6
    3             92.0     3         12.3     3
    ```

    **Pembahasan:**

    - Dengan \(k = 2\), kelompok "menengah" dan "pendapatan tinggi" **digabung** menjadi satu cluster berisi 12 pelanggan. Rata-ratanya (76,8; 32,8) tidak mewakili kedua kelompok dengan baik.
    - Dengan \(k = 4\), kelompok "pendapatan tinggi" **dipecah** menjadi dua cluster kecil berisi 3 pelanggan. Perbedaan keduanya kecil dan kemungkinan tidak bermakna.
    - \(k = 3\) paling masuk akal untuk data ini, karena data memang dibuat dengan tiga kelompok yang terpisah jelas.

    **Pelajaran:** K-Means selalu memberi tepat \(k\) cluster sesuai permintaan, walaupun pembagiannya tidak alami. Memilih \(k\) adalah tanggung jawab kita.

    `.agg(["mean", "count"])` menghitung rata-rata dan jumlah sekaligus. Nomor cluster bisa berbeda pada versi Scikit-learn lain, tetapi isi kelompoknya sama.
