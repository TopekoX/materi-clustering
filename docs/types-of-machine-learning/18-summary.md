# Ringkasan Bab

## Empat paradigma Machine Learning

| Paradigma | Data | Tujuan | Contoh |
|---|---|---|---|
| **Supervised Learning** | Fitur + label | Menebak label | Filter spam, taksiran harga rumah |
| **Unsupervised Learning** | Fitur saja | Menemukan struktur | Segmentasi pelanggan |
| **Semi-Supervised Learning** | Sedikit label + banyak tanpa label | Menebak label dengan biaya pelabelan rendah | Klasifikasi dokumen dengan 1% label |
| **Reinforcement Learning** | Interaksi + reward | Memaksimalkan total reward | Agen permainan, robot |

## Poin-poin penting

**Labeled vs unlabeled data**

- **Fitur** adalah ciri yang dipakai untuk menebak. **Label** adalah jawabannya. **Target** adalah kolom yang berisi label.
- Ada atau tidaknya label adalah pembeda utama antara supervised dan unsupervised.
- Label sering mahal karena membutuhkan ahli, waktu, dan biaya.

**Classification dan Regression** (supervised)

- **Classification** menebak **kategori**: binary, multiclass, atau multilabel.
- **Regression** menebak **angka kontinu**.
- Pembedanya adalah bentuk target, bukan algoritma.

**Clustering dan Dimensionality Reduction** (unsupervised)

- **Clustering** mengelompokkan data yang mirip, biasanya berdasarkan **jarak**. Algoritma hanya memberi **nomor** cluster. Manusia yang menafsirkan.
- Clustering **bukan** classification: tidak ada kelas yang ditentukan sebelumnya.
- **Dimensionality reduction** meringkas banyak fitur menjadi sedikit, dengan *feature selection* atau *feature extraction* seperti PCA.
- **Association rule learning** mencari item yang sering muncul bersama, diukur dengan support, confidence, dan lift.

**Memilih pendekatan**

- Tanyakan: apa masalahnya, data apa yang ada, adakah label, keluaran apa yang diharapkan, apa tujuannya, dan bagaimana mengevaluasinya.
- Di dunia nyata, beberapa pendekatan sering digabungkan.

**Praktik**

- Pola Scikit-learn: buat model, `fit`, lalu `predict`.
- Supervised: `fit(X_train, y_train)`, dievaluasi dengan akurasi.
- Unsupervised (K-Means): `fit_predict(X)` tanpa `y`, dan `n_clusters` ditentukan oleh kita.

## Hubungan dengan fokus kurikulum

Clustering adalah bagian dari Unsupervised Learning. Bab ini menunjukkan **kapan** clustering tepat dipakai: ketika data tidak berlabel dan tujuannya menemukan kelompok yang belum diketahui. Kamu juga sudah melihat bahwa hasil clustering sangat dipengaruhi oleh **fitur yang dipilih**, **skala fitur**, dan **jumlah cluster**.

## Cek diri

Kembali ke [tujuan pembelajaran](index.md) di halaman awal bab. Jika kamu bisa menjelaskan setiap poin dengan kata-katamu sendiri, kamu siap lanjut.

## Jembatan ke Bab 3

Kedua praktik di bab ini memakai data yang sudah rapi. Di dunia nyata, data jarang serapi itu. Bab berikutnya akan memperdalam alur kerja Machine Learning, khususnya bagaimana data disiapkan dan dibagi, serta bagaimana model dinilai. Bekal ini dibutuhkan sebelum kita masuk ke eksplorasi dan pra-pemrosesan data untuk clustering di Level 2.

Lanjut ke [Referensi](19-references.md).
