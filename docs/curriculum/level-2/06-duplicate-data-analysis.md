# Bab 6 — Duplicate Data Analysis

## Learning Objectives

Setelah mempelajari bab ini, kamu mampu:

- [x] Menjelaskan apa itu data duplikat dan mengapa ia mengganggu clustering.
- [x] Membedakan duplikat penuh dan duplikat parsial.
- [x] Menemukan baris ganda dengan `duplicated()`.
- [x] Membuang baris ganda dengan `drop_duplicates()`.
- [x] Menjelaskan arti `keep="first"`, `keep="last"`, dan `keep=False`.
- [x] Memutuskan kapan baris yang tampak sama **bukan** duplikat.

## Introduction

**Data duplikat** adalah baris yang muncul lebih dari sekali. Penyebabnya macam-macam: data diunggah dua kali, dua file digabung tanpa disaring, atau formulir terkirim ganda.

Dalam clustering, duplikat berbahaya karena ia **memberi bobot ekstra** pada satu titik. Algoritma tidak tahu bahwa dua titik itu sebenarnya satu pelanggan. Jika satu pelanggan tercatat tiga kali, ia seolah menjadi tiga pelanggan, dan bisa menarik pusat kelompok ke arahnya.

!!! warning "Dataset ini sebenarnya tidak punya duplikat"
    Mall Customers **tidak punya baris ganda**, baik penuh maupun parsial (kita buktikan di bawah). Supaya bisa berlatih, bab ini **sengaja menambahkan 8 baris ganda ke salinan data** (simulasi, seed tetap). Itu bukan temuan dari data asli. Data asli tidak diubah.

## Fundamental Concepts

| Jenis | Arti | Contoh |
|---|---|---|
| **Duplikat penuh** | **Semua** kolom sama persis | Dua baris yang identik, termasuk `CustomerID` |
| **Duplikat parsial** | Hanya **sebagian** kolom yang sama | Dua `CustomerID` berbeda dengan usia, pendapatan, dan skor sama |
| **Hampir duplikat** | Mirip tetapi tidak identik | `"Jakarta"` dan `"jakarta "` |

Parameter `keep` pada pandas menentukan baris mana yang dianggap "asli":

| `keep=` | Arti |
|---|---|
| `"first"` (bawaan) | Baris pertama dianggap asli, baris berikutnya dianggap ganda |
| `"last"` | Baris terakhir dianggap asli |
| `False` | **Semua** baris yang kembar ditandai (berguna untuk melihat pasangannya) |

## Detailed Explanation

### Duplikat belum tentu kesalahan

Dua pelanggan berbeda bisa saja kebetulan punya usia, pendapatan, dan skor belanja yang sama. Itu **bukan** duplikat. Karena itu kita perlu memahami arti tiap baris:

- Jika data punya **kolom identitas** (seperti `CustomerID`) dan identitas itu **sama**, baris itu kemungkinan besar memang ganda.
- Jika identitas berbeda tetapi sifat lain sama, **periksa dulu**. Mungkin kebetulan, mungkin satu orang yang tercatat dua kali dengan ID berbeda.

### Alur penanganan

1. **Deteksi.** `duplicated()` dan hitung jumlahnya.
2. **Lihat contoh.** Gunakan `keep=False` supaya pasangan duplikat terlihat bersama-sama.
3. **Putuskan.** Apakah benar-benar ganda?
4. **Buang.** `drop_duplicates()` dengan `keep` yang sesuai.
5. **Verifikasi.** Pastikan tidak ada yang tersisa dan jumlah baris masuk akal.

## Mathematical Foundation

Bab ini tidak memerlukan rumus. Deteksi duplikat hanyalah pembandingan nilai antar baris.

## Python Implementation

Kita kerjakan dalam tujuh langkah kecil. **Setiap potongan kode diikuti penjelasannya.** Skrip lengkapnya ada di `examples/level-2/06_duplicate_data.py`, dan versi notebook-nya di `notebooks/level-2/06-duplicate-data-analysis.ipynb`.

### Langkah 1 — Siapkan alat dan muat data

```python
--8<-- "level-2/06_duplicate_data.py:setup"
```

**Penjelasan:**

- Kita membaca file CSV menjadi tabel `df`.
- `kolom_sifat` adalah daftar kolom yang menggambarkan **sifat pelanggan**. Kita sengaja tidak memasukkan `CustomerID`, karena nanti kita ingin membandingkan baris berdasarkan sifatnya saja.

### Langkah 2 — Periksa data asli

```python
--8<-- "level-2/06_duplicate_data.py:real"
```

**Penjelasan:**

- `df.duplicated()` mengembalikan `True` untuk baris yang **sama persis** dengan baris sebelumnya. `.sum()` menghitung jumlah `True`.
- `df["CustomerID"].duplicated()` memeriksa apakah ada **ID yang berulang**. Karena `CustomerID` seharusnya unik, setiap ID berulang berarti ada masalah.

### Langkah 3 — Duplikat tanpa memperhitungkan CustomerID

```python
--8<-- "level-2/06_duplicate_data.py:partial"
```

**Penjelasan:**

- `subset=kolom_sifat` membatasi pembandingan **hanya pada kolom-kolom itu**. Dua baris dianggap sama jika keempat sifatnya sama, walaupun `CustomerID` berbeda.
- `keep=False` menandai **semua** baris yang punya kembaran, bukan hanya yang kedua dan seterusnya.
- `df[sama_sifat]` menampilkan baris-baris yang ditandai. `sort_values(kolom_sifat)` mengurutkannya agar pasangan kembar berdekatan.

### Langkah 4 — Buat salinan dengan baris ganda buatan

```python
--8<-- "level-2/06_duplicate_data.py:simulate"
```

**Penjelasan:**

- `df.sample(n=8, random_state=42)` mengambil 8 baris acak. `random_state=42` adalah *seed*: hasilnya selalu sama setiap dijalankan.
- `pd.concat([df, tambahan], ignore_index=True)` **menempelkan** 8 baris itu di bawah tabel asli. `ignore_index=True` membuat nomor baris dihitung ulang dari 0.
- Hasilnya tabel `df_ganda` berisi 208 baris: 200 asli + 8 salinan.

### Langkah 5 — Temukan baris ganda

```python
--8<-- "level-2/06_duplicate_data.py:detect"
```

**Penjelasan:**

- `df_ganda.duplicated().sum()` menghitung baris ganda. Hasilnya harus 8.
- `duplicated(keep=False)` menandai **baik yang asli maupun salinannya**, sehingga kita bisa melihat pasangannya.
- `sort_values("CustomerID")` mengurutkan berdasarkan ID, jadi dua baris kembar tampil berdekatan.

### Langkah 6 — Buang baris ganda

```python
--8<-- "level-2/06_duplicate_data.py:drop"
```

**Penjelasan:**

- `drop_duplicates()` membuang baris ganda dan mengembalikan tabel baru. Karena `keep` tidak ditulis, nilai bawaannya `"first"` dipakai: baris pertama dipertahankan, salinannya dibuang.
- Kita bandingkan ukuran sebelum dan sesudah.

### Langkah 7 — Pastikan hasilnya benar

```python
--8<-- "level-2/06_duplicate_data.py:verify"
```

**Penjelasan:**

- Langkah ini **memverifikasi**: apakah masih ada baris ganda, dan apakah jumlah baris kembali ke 200.
- Selalu lakukan verifikasi seperti ini setelah mengubah data. Jangan hanya percaya bahwa kodenya berhasil.

## Code Explanation

Ringkasan fungsi baru di bab ini:

| Perintah | Kegunaan |
|---|---|
| `df.duplicated()` | Menandai baris ganda (`True`/`False`) |
| `df.duplicated(subset=[...])` | Membandingkan hanya pada kolom tertentu |
| `df.duplicated(keep=False)` | Menandai semua baris kembar |
| `df.drop_duplicates()` | Membuang baris ganda |
| `df.sample(n=..., random_state=...)` | Mengambil baris acak |
| `pd.concat([a, b])` | Menempelkan dua tabel |
| `df.sort_values(kolom)` | Mengurutkan tabel |

## How to Run

Jalankan dari **folder utama proyek**:

```powershell
python examples/level-2/06_duplicate_data.py
```

Untuk notebook:

```powershell
jupyter notebook notebooks/level-2/06-duplicate-data-analysis.ipynb
```

## Expected Output

Output berikut berasal dari eksekusi nyata skrip di atas (pandas 3.1.1, Python 3.14.7):

```text
--8<-- "level-2/outputs/06.txt"
```

**Cara membaca output:**

- **Data asli bersih.** Baris ganda penuh: 0. `CustomerID` berulang: 0. Baris dengan sifat sama tanpa memperhitungkan `CustomerID`: 0 (tabelnya kosong, `Empty DataFrame`). Jadi tidak ada duplikat parsial juga.
- **Setelah penambahan buatan:** 208 baris, dengan **8** baris ganda.
- Daftar baris yang terlibat berisi 16 baris, yaitu 8 pasangan. Misalnya `CustomerID` 16 muncul di indeks 15 (asli) dan 201 (salinan).
- Setelah `drop_duplicates()`: kembali ke 200 baris, tanpa baris ganda tersisa.

## Practical Examples

**Kapan duplikat parsial menjadi alarm?** Pada data yang punya kolom ID, ID yang berulang hampir pasti kesalahan. Pada data **tanpa** kolom ID (misalnya hasil survei anonim), dua baris identik bisa berarti dua orang berbeda yang kebetulan menjawab sama. Pada kasus itu, membuang duplikat bisa menghilangkan data yang sah. Pahami asal data sebelum membuang.

**Mengapa `keep` penting.** Bayangkan satu pelanggan tercatat dua kali, kedua kali dengan `Spending Score` berbeda (update terbaru). `keep="first"` mempertahankan versi lama, `keep="last"` mempertahankan versi terbaru. Pilih sesuai makna datanya.

**Dampak pada clustering.** Pada data kita, delapan baris ganda berarti delapan pelanggan "dihitung dua kali". Pada cluster kecil, itu bisa mengubah letak pusat dan jumlah anggota. Selisih ini mudah luput jika kita tidak memeriksanya.

## Hands-on Exercises

1. Ubah `n=8` pada Langkah 4 menjadi `n=20`. Berapa baris ganda terdeteksi, dan berapa baris setelah dibuang?
2. Gunakan `drop_duplicates(keep="last")`. Baris mana yang bertahan, yang asli atau salinannya? (petunjuk: lihat `CustomerID` 16 dan nomor indeksnya)
3. Mengapa `df.duplicated()` pada data asli menghasilkan 0 walaupun mungkin ada pelanggan yang mirip?
4. Gunakan `duplicated(subset=["CustomerID"])` pada `df_ganda`. Hasilnya sama atau beda dengan `duplicated()`? Mengapa?
5. Kapan baris yang tampak identik bukan duplikat?

??? question "Jawaban"
    1. Jumlah baris ganda terdeteksi sama dengan `n`, selama baris yang diambil acak tidak terambil dua kali. Dengan `sample`, tidak ada baris yang terambil dua kali dalam satu pengambilan. Setelah dibuang, kembali 200 baris. Jalankan dan cocokkan.
    2. Dengan `keep="last"`, yang bertahan adalah baris **terakhir**, yaitu salinan yang ditempel di bawah (indeks 200 ke atas). Karena isinya identik, hasil akhirnya tampak sama, hanya nomor indeksnya berbeda.
    3. `duplicated()` hanya menandai baris yang **identik di semua kolom**, termasuk `CustomerID`. Pelanggan berbeda selalu punya ID berbeda. Untuk membandingkan hanya sifat, pakai `subset`.
    4. Hasilnya sama (8), karena pada data ini salinan memiliki `CustomerID` yang sama dengan aslinya. Namun jika baris ganda punya ID berbeda, `subset=["CustomerID"]` tidak akan menemukannya.
    5. Ketika baris mewakili entitas berbeda yang kebetulan bernilai sama, misalnya dua responden survei anonim dengan jawaban sama.

## Troubleshooting

| Masalah | Penyebab | Solusi |
|---|---|---|
| `duplicated()` menghasilkan 0 padahal terlihat ada kembar | Ada perbedaan kecil, misalnya spasi atau huruf besar-kecil | Bersihkan teks dulu (Bab 8), lalu cek lagi |
| Baris ganda tidak terbuang | Hasil `drop_duplicates()` tidak disimpan | Simpan: `df = df.drop_duplicates()` |
| Nomor indeks melompat setelah `drop_duplicates()` | Baris dibuang tetapi nomornya dipertahankan | `df.reset_index(drop=True)` |
| `KeyError` pada `subset` | Nama kolom salah | Salin nama dari `df.columns` |
| Jumlah duplikat berbeda tiap dijalankan | `sample` tanpa `random_state` | Tambahkan `random_state=42` |

## Summary

- Duplikat memberi bobot ekstra pada titik tertentu, sehingga bisa menyesatkan clustering.
- Deteksi: `duplicated()`, dengan `subset` untuk kolom tertentu dan `keep=False` untuk melihat pasangannya.
- Buang: `drop_duplicates()`. Selalu verifikasi setelahnya.
- Baris yang tampak sama belum tentu duplikat. Pahami arti datanya.
- Pada Mall Customers: **tidak ada** duplikat penuh maupun parsial. Bab ini memakai **8 baris ganda buatan** pada salinan data untuk latihan.

## References

- pandas documentation: [`DataFrame.duplicated`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html) dan [`DataFrame.drop_duplicates`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop_duplicates.html).
- Wickham, H. (2014). *Tidy Data*. Journal of Statistical Software, 59(10).
