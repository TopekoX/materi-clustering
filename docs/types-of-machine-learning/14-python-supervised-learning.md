# Praktik Supervised Learning: Klasifikasi Bunga Iris

## A. Konteks masalah

Kita ingin membuat program yang bisa **menebak jenis bunga iris** dari ukuran kelopaknya. Ada tiga jenis: *setosa*, *versicolor*, dan *virginica*.

Ini masalah **Supervised Learning**, tepatnya **multiclass classification**:

- **Supervised**, karena setiap bunga di dataset sudah diberi label jenisnya.
- **Classification**, karena jawabannya kategori, bukan angka.
- **Multiclass**, karena ada tiga kelas.

## B. Prasyarat

**Pustaka yang dibutuhkan:**

| Pustaka | Kegunaan |
|---|---|
| `pandas` | Mengolah data berbentuk tabel |
| `scikit-learn` | Dataset, algoritma, dan alat evaluasi Machine Learning |

Pasang dengan:

```bash
pip install pandas scikit-learn
```

**Data:** dataset **Iris**, yang sudah tersedia di dalam Scikit-learn sehingga tidak perlu diunduh. Dataset ini berisi 150 bunga yang diukur oleh ahli botani dan dipopulerkan oleh statistikawan Ronald Fisher pada 1936.

**Konsep yang perlu diingat:** fitur, label, data latih, data uji (lihat [Labeled dan Unlabeled Data](02-labeled-and-unlabeled-data.md) dan [Supervised Learning](03-supervised-learning.md)).

**Tentang Scikit-learn.** Scikit-learn (diimpor dengan nama `sklearn`) adalah pustaka Python untuk Machine Learning klasik. Hampir semua modelnya dipakai dengan pola yang sama:

1. Buat objek model, misalnya `model = KNeighborsClassifier()`.
2. Latih dengan `model.fit(X_train, y_train)`.
3. Tebak dengan `model.predict(X_test)`.

## C. Kode lengkap

Simpan sebagai `klasifikasi_iris.py`:

```python title="klasifikasi_iris.py"
# Langkah 1: impor pustaka
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Langkah 2: muat dataset Iris
iris = load_iris(as_frame=True)
X = iris.data          # fitur: 4 ukuran bunga
y = iris.target        # label: jenis bunga (0, 1, 2)

# Langkah 3: kenali fitur dan target
print(X.head())
print("Nama kelas:", iris.target_names.tolist())

# Langkah 4: periksa ukuran data
print("Ukuran X:", X.shape)
print("Ukuran y:", y.shape)
print("Jumlah per kelas:", y.value_counts().sort_index().tolist())

# Langkah 5: bagi data latih dan data uji
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Data latih:", X_train.shape, "| Data uji:", X_test.shape)

# Langkah 6: buat model klasifikasi
model = KNeighborsClassifier(n_neighbors=5)

# Langkah 7: latih model
model.fit(X_train, y_train)

# Langkah 8: buat prediksi
y_pred = model.predict(X_test)
print("5 prediksi pertama :", y_pred[:5].tolist())
print("5 jawaban sebenarnya:", y_test[:5].tolist())

bunga_baru = pd.DataFrame(
    [[5.0, 3.4, 1.5, 0.2]], columns=X.columns
)
kelas_baru = model.predict(bunga_baru)[0]
print("Bunga baru diprediksi:", iris.target_names[kelas_baru])

# Langkah 9: evaluasi akurasi
akurasi = accuracy_score(y_test, y_pred)
print(f"Akurasi: {akurasi:.2f}")
```

Jalankan dengan:

```bash
python klasifikasi_iris.py
```

**Output:**

```text
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
0                5.1               3.5                1.4               0.2
1                4.9               3.0                1.4               0.2
2                4.7               3.2                1.3               0.2
3                4.6               3.1                1.5               0.2
4                5.0               3.6                1.4               0.2
Nama kelas: ['setosa', 'versicolor', 'virginica']
Ukuran X: (150, 4)
Ukuran y: (150,)
Jumlah per kelas: [50, 50, 50]
Data latih: (120, 4) | Data uji: (30, 4)
5 prediksi pertama : [0, 2, 1, 1, 0]
5 jawaban sebenarnya: [0, 2, 1, 1, 0]
Bunga baru diprediksi: setosa
Akurasi: 1.00
```

## D. Penjelasan kode langkah demi langkah

### Langkah 1: Mengimpor pustaka

```python
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
```

**Tujuan:** mengambil alat-alat yang dibutuhkan, seperti mengeluarkan peralatan dari kotak sebelum bekerja.

| Baris | Apa yang diambil | Untuk apa |
|---|---|---|
| `import pandas as pd` | Pustaka pandas, disingkat `pd` | Membuat tabel data bunga baru di langkah 8 |
| `load_iris` | Fungsi pemuat dataset Iris | Langkah 2 |
| `accuracy_score` | Fungsi penghitung akurasi | Langkah 9 |
| `train_test_split` | Fungsi pembagi data | Langkah 5 |
| `KNeighborsClassifier` | Algoritma K-Nearest Neighbors untuk klasifikasi | Langkah 6 |

Bentuk `from A import B` berarti "dari pustaka A, ambil alat B saja".

### Langkah 2: Memuat dataset

```python
iris = load_iris(as_frame=True)
X = iris.data          # fitur: 4 ukuran bunga
y = iris.target        # label: jenis bunga (0, 1, 2)
```

- `load_iris(as_frame=True)` memuat dataset. Parameter `as_frame=True` meminta data dikembalikan sebagai **tabel pandas** (DataFrame), sehingga ada nama kolom dan lebih mudah dibaca. Tanpa parameter ini, data dikembalikan sebagai array angka biasa.
- Hasilnya disimpan di variabel `iris`, sebuah wadah yang berisi beberapa bagian: data, target, nama kelas, dan keterangan lain.
- `X = iris.data` mengambil **tabel fitur**: empat ukuran tiap bunga. Huruf besar `X` adalah kebiasaan umum untuk tabel fitur.
- `y = iris.target` mengambil **kolom label**: jenis tiap bunga dalam bentuk angka 0, 1, atau 2. Huruf kecil `y` adalah kebiasaan umum untuk target.

**Hubungan dengan proses ML:** inilah tahap *data collection*. Bedanya, datanya sudah disiapkan oleh Scikit-learn.

### Langkah 3: Mengenali fitur dan target

```python
print(X.head())
print("Nama kelas:", iris.target_names.tolist())
```

- `X.head()` menampilkan **5 baris pertama** tabel fitur. Ini cara cepat "mengintip" data.
- `iris.target_names` berisi nama asli tiap kelas. `.tolist()` mengubahnya menjadi list Python biasa agar tampil rapi.

**Output:**

```text
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
0                5.1               3.5                1.4               0.2
1                4.9               3.0                1.4               0.2
2                4.7               3.2                1.3               0.2
3                4.6               3.1                1.5               0.2
4                5.0               3.6                1.4               0.2
Nama kelas: ['setosa', 'versicolor', 'virginica']
```

**Interpretasi:**

- Ada 4 fitur: panjang dan lebar *sepal* (kelopak luar), serta panjang dan lebar *petal* (mahkota bunga), semuanya dalam sentimeter.
- Angka paling kiri (0–4) adalah **indeks**, yaitu nomor baris, bukan fitur.
- Label 0 berarti setosa, 1 berarti versicolor, dan 2 berarti virginica. Urutannya mengikuti `target_names`.

### Langkah 4: Memeriksa ukuran data

```python
print("Ukuran X:", X.shape)
print("Ukuran y:", y.shape)
print("Jumlah per kelas:", y.value_counts().sort_index().tolist())
```

- `.shape` memberi ukuran data dalam bentuk `(jumlah baris, jumlah kolom)`.
- `y.value_counts()` menghitung berapa kali setiap label muncul. `.sort_index()` mengurutkan hasilnya berdasarkan label 0, 1, 2.

**Output:**

```text
Ukuran X: (150, 4)
Ukuran y: (150,)
Jumlah per kelas: [50, 50, 50]
```

**Interpretasi:**

- `X` punya 150 baris (bunga) dan 4 kolom (fitur).
- `y` berukuran `(150,)`. Tanda koma tanpa angka kedua berarti `y` hanya satu kolom, berisi satu label untuk setiap bunga.
- Setiap kelas punya 50 bunga. Dataset ini **seimbang** (*balanced*).

**Mengapa penting?** Jumlah baris `X` dan `y` harus sama. Jika berbeda, ada yang salah dengan data.

### Langkah 5: Membagi data latih dan data uji

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print("Data latih:", X_train.shape, "| Data uji:", X_test.shape)
```

**Tujuan:** menyisihkan sebagian data untuk ujian, agar model diuji dengan bunga yang **belum pernah dilihatnya**.

| Parameter | Nilai | Arti |
|---|---|---|
| `X, y` | — | Data yang akan dibagi |
| `test_size` | `0.2` | 20% data dipakai untuk uji, 80% untuk latih |
| `random_state` | `42` | Mengunci pengacakan agar hasil pembagian selalu sama setiap kali dijalankan. Angka 42 hanyalah kebiasaan. Angka lain juga boleh |
| `stratify` | `y` | Menjaga proporsi kelas tetap sama di data latih dan data uji |

Fungsi ini mengembalikan **empat** hasil dalam urutan tetap: fitur latih, fitur uji, label latih, label uji.

**Output:**

```text
Data latih: (120, 4) | Data uji: (30, 4)
```

**Interpretasi:** 120 bunga untuk belajar dan 30 bunga untuk ujian. Karena `stratify=y`, data uji berisi 10 bunga dari tiap kelas.

### Langkah 6: Membuat model

```python
model = KNeighborsClassifier(n_neighbors=5)
```

- Baris ini **hanya menyiapkan** algoritma. Model belum belajar apa pun.
- **K-Nearest Neighbors (KNN)** bekerja seperti ini: untuk menebak jenis sebuah bunga, cari `k` bunga di data latih yang ukurannya **paling mirip** (paling dekat), lalu pilih jenis yang paling banyak di antara tetangga itu.
- `n_neighbors=5` berarti \(k = 5\): lihat 5 tetangga terdekat.

**Analogi:** jika kamu ingin menebak selera musik seseorang, lihat 5 teman terdekatnya. Jika 4 dari 5 suka jazz, kemungkinan besar ia juga suka jazz.

### Langkah 7: Melatih model

```python
model.fit(X_train, y_train)
```

- `fit` berarti "sesuaikan" atau "latih". Model menerima **fitur latih** dan **label latih** sekaligus. Inilah ciri Supervised Learning: label ikut diberikan saat belajar.
- Khusus KNN, "belajar" berarti **mengingat** seluruh data latih, karena tebakan dibuat dengan membandingkan data baru dengan data latih. Algoritma lain, seperti Decision Tree, benar-benar membangun aturan saat `fit`.

**Penting:** `fit` hanya memakai data **latih**. Data uji tidak boleh dipakai di sini.

### Langkah 8: Membuat prediksi

```python
y_pred = model.predict(X_test)
print("5 prediksi pertama :", y_pred[:5].tolist())
print("5 jawaban sebenarnya:", y_test[:5].tolist())
```

- `predict` hanya menerima **fitur** (`X_test`), tanpa label. Model harus menebak sendiri.
- Hasilnya `y_pred`: 30 tebakan, satu untuk setiap bunga uji.
- `[:5]` mengambil 5 elemen pertama. `.tolist()` agar tampil rapi.

**Output:**

```text
5 prediksi pertama : [0, 2, 1, 1, 0]
5 jawaban sebenarnya: [0, 2, 1, 1, 0]
```

**Interpretasi:** untuk 5 bunga pertama, tebakan model sama persis dengan jawaban sebenarnya.

Kita juga bisa menebak bunga yang benar-benar baru:

```python
bunga_baru = pd.DataFrame(
    [[5.0, 3.4, 1.5, 0.2]], columns=X.columns
)
kelas_baru = model.predict(bunga_baru)[0]
print("Bunga baru diprediksi:", iris.target_names[kelas_baru])
```

- `bunga_baru` adalah tabel dengan **satu baris** berisi 4 ukuran. Kurung siku ganda `[[...]]` berarti "daftar baris", dan di sini hanya ada satu baris.
- `columns=X.columns` memberi nama kolom yang **sama persis** dengan data latih.
- `model.predict(...)` mengembalikan array berisi satu tebakan. `[0]` mengambil elemen pertamanya.
- `iris.target_names[kelas_baru]` mengubah angka label menjadi nama jenis.

**Output:**

```text
Bunga baru diprediksi: setosa
```

### Langkah 9: Evaluasi akurasi

```python
akurasi = accuracy_score(y_test, y_pred)
print(f"Akurasi: {akurasi:.2f}")
```

- `accuracy_score(jawaban_sebenarnya, tebakan)` menghitung proporsi tebakan yang benar. Urutan parameternya: jawaban sebenarnya **dulu**, baru tebakan.
- `f"...{akurasi:.2f}"` menampilkan angka dengan 2 angka di belakang koma.

**Output:**

```text
Akurasi: 1.00
```

## E. Ringkasan output yang diharapkan

Output teks lengkap program ditampilkan langsung di bawah kode pada bagian [C. Kode lengkap](#c-kode-lengkap). Output tiap langkah juga ada tepat di bawah kodenya masing-masing pada bagian D.

Output ini dihasilkan dengan Python 3.14, pandas 3.1.1, dan scikit-learn 1.9.1. Versi lain bisa sedikit berbeda.

## F. Interpretasi hasil

- **Akurasi 1.00** berarti 30 dari 30 bunga uji ditebak dengan benar: \(30 / 30 = 1{,}00\).
- Hasil sempurna ini terjadi karena Iris adalah dataset **kecil dan sangat rapi**. Ketiga jenis bunganya cukup mudah dibedakan dari ukuran mahkotanya.
- **Jangan berharap hasil seperti ini pada data nyata.** Dengan pembagian data yang berbeda (`random_state` lain), akurasi bisa sedikit lebih rendah. Pada data dunia nyata, akurasi 100% justru patut dicurigai sebagai tanda ada yang salah.

## G. Kesalahan umum pemula

| Kesalahan | Akibat | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Program berhenti di baris impor | `pip install scikit-learn`. Nama paket untuk dipasang adalah `scikit-learn`, nama untuk impor adalah `sklearn` |
| Memanggil `predict` sebelum `fit` | Muncul `NotFittedError` | Selalu `fit` dulu |
| Melatih dengan data uji: `model.fit(X_test, y_test)` | Evaluasi menjadi tidak jujur | `fit` hanya dengan `X_train, y_train` |
| Urutan hasil `train_test_split` tertukar | Ukuran data tidak cocok, muncul error | Urutannya selalu `X_train, X_test, y_train, y_test` |
| Memberi satu bunga sebagai list biasa `[5.0, 3.4, 1.5, 0.2]` | Error *Expected 2D array* | Bungkus menjadi tabel satu baris, seperti `bunga_baru` di langkah 8 |
| Mengira akurasi 1.00 berarti model sempurna | Kepercayaan berlebihan | Ingat bahwa data uji hanya 30 bunga dan datanya sangat rapi |

## H. Latihan mini

1. Ubah `n_neighbors=5` menjadi `n_neighbors=1`, lalu menjadi `n_neighbors=50`. Apa yang terjadi pada akurasi? Mengapa nilai \(k\) yang sangat besar bisa merugikan?
2. Ubah `random_state=42` menjadi `random_state=7`. Apakah akurasinya tetap 1.00?
3. Tebak jenis bunga dengan ukuran `[6.7, 3.0, 5.2, 2.3]`.

Lanjut ke [Praktik Unsupervised Learning](15-python-unsupervised-learning.md).
