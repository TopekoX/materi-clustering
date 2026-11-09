# Latihan

Kerjakan dulu dengan jujur, baru buka kunci jawaban pada kotak yang bisa dibuka.

## A. Pertanyaan konseptual

**1.** Jelaskan Machine Learning dengan kata-katamu sendiri, dalam satu atau dua kalimat.

??? success "Kunci jawaban"
    Machine Learning adalah cara membuat komputer menemukan pola dari data (contoh) sehingga bisa membuat tebakan atau keputusan pada data baru, tanpa semua aturannya ditulis manual oleh manusia.

**2.** Sebutkan hubungan antara AI, ML, dan Deep Learning.

??? success "Kunci jawaban"
    Deep Learning adalah bagian dari Machine Learning, dan Machine Learning adalah bagian dari Artificial Intelligence. AI paling luas, DL paling sempit.

**3.** Apa beda *algoritma* dan *model*?

??? success "Kunci jawaban"
    Algoritma adalah prosedur belajar. Model adalah hasil yang diperoleh setelah algoritma belajar dari data, dan dipakai untuk membuat prediksi.

**4.** Mengapa data dibagi menjadi data latih dan data uji?

??? success "Kunci jawaban"
    Agar kualitas model diuji pada data yang belum pernah dilihatnya. Jika diuji dengan data yang sama dengan data latih, hasilnya terlalu optimis dan tidak menunjukkan kemampuan menghadapi data baru.

**5.** Mengapa clustering disebut *unsupervised learning*?

??? success "Kunci jawaban"
    Karena datanya tidak memiliki label atau target. Algoritma hanya memakai fitur untuk mencari kelompok yang alami.

## B. Pertanyaan analitis

**6.** Sebuah bank ingin tahu apakah pelamar kredit akan gagal bayar atau tidak, memakai data pelamar sebelumnya yang sudah diketahui hasilnya. Termasuk jenis masalah apa (classification, regression, atau clustering)? Beri alasan.

??? success "Kunci jawaban"
    Classification, sebab keluarannya adalah kategori (gagal bayar atau tidak), dan datanya berlabel (hasil pelamar sebelumnya diketahui), sehingga bersifat supervised.

**7.** Sebuah toko ingin membagi pelanggan menjadi beberapa tipe, tetapi belum pernah menentukan tipe apa saja. Jenis masalah apa ini? Siapa yang memberi nama pada tiap kelompok hasilnya?

??? success "Kunci jawaban"
    Clustering (unsupervised). Algoritma hanya memberi nomor kelompok. Manusia, yaitu analis atau pemilik toko, yang menafsirkan ciri tiap kelompok lalu memberinya nama.

**8.** Sebuah model menebak nilai 60, 75, dan 90, sedangkan nilai sebenarnya 58, 80, dan 88. Hitung MAE-nya dan jelaskan artinya.

??? success "Kunci jawaban"
    Selisih absolut: \(|58-60| = 2\), \(|80-75| = 5\), \(|88-90| = 2\). Jumlahnya 9, dibagi 3 menjadi \(\text{MAE} = 3\). Artinya rata-rata tebakan meleset 3 poin.

## C. Latihan praktik

**9.** Gunakan pola kode di [Praktik Pertama](11-hands-on-introduction.md) untuk data berikut. Latih model `LinearRegression` pada **seluruh** data (tanpa pembagian latih dan uji, karena datanya sangat sedikit), tampilkan koefisien dan intersep, lalu prediksi skor fokus untuk tidur 7,5 jam.

| jam_tidur | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|
| skor_fokus | 40 | 50 | 62 | 70 | 82 | 90 |

??? success "Kunci jawaban"
    ```python
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    df = pd.DataFrame({
        "jam_tidur": [4, 5, 6, 7, 8, 9],
        "skor_fokus": [40, 50, 62, 70, 82, 90],
    })
    m = LinearRegression().fit(df[["jam_tidur"]], df["skor_fokus"])
    print(round(m.coef_[0], 2), round(m.intercept_, 2))
    print(round(m.predict(pd.DataFrame({"jam_tidur": [7.5]}))[0], 1))
    ```

    Output:

    ```text
    10.11 -0.08
    75.8
    ```

**10.** Pada data soal 9, bagi data dengan `train_test_split(X, y, test_size=0.33, random_state=...)`, lalu cetak nilai `jam_tidur` pada data uji untuk `random_state=1` dan `random_state=42`. Apa yang kamu amati?

??? success "Kunci jawaban"
    ```python
    from sklearn.model_selection import train_test_split

    X = df[["jam_tidur"]]
    y = df["skor_fokus"]
    for rs in (1, 42):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.33, random_state=rs
        )
        print(rs, sorted(X_test["jam_tidur"].tolist()))
    ```

    Output:

    ```text
    1 [5, 6]
    42 [4, 5]
    ```

    Nilai `random_state` yang berbeda menghasilkan pembagian data yang berbeda. Nilai yang sama selalu menghasilkan pembagian yang sama, sehingga hasil percobaan bisa diulang oleh orang lain (reproducible).

Lanjut ke [Ringkasan](13-summary.md).
