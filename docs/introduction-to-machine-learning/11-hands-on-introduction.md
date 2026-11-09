# Praktik Pertama dengan Scikit-learn

Sekarang kita praktikkan semua istilah tadi dalam kode kecil. Tujuannya bukan mengejar akurasi, tetapi melihat dengan mata sendiri hubungan antara **dataset → algoritma → model → training → prediction**.

## Persiapan

Pastikan Python 3 sudah terpasang, lalu pasang paket yang dibutuhkan:

```bash
pip install pandas scikit-learn
```

*Scikit-learn* adalah pustaka Python yang populer untuk Machine Learning klasik. Kita memakainya karena sederhana dan dokumentasinya baik.

## Kode lengkap

Simpan sebagai `praktik_pertama.py`:

```python title="praktik_pertama.py"
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# 1. Dataset: jam belajar (fitur) dan nilai ujian (target)
data = pd.DataFrame({
    "jam_belajar": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "nilai_ujian": [52, 55, 61, 64, 70, 72, 78, 83, 85, 92],
})
print(data.head())

X = data[["jam_belajar"]]  # fitur (input)
y = data["nilai_ujian"]    # target (jawaban yang ingin ditebak)

# 2. Bagi data: 70% untuk belajar (train), 30% untuk menguji (test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
print("Data latih:", len(X_train), "baris | Data uji:", len(X_test), "baris")

# 3. Algoritma + training -> menghasilkan model
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Model: nilai = {model.coef_[0]:.2f} x jam + {model.intercept_:.2f}")

# 4. Prediksi untuk data baru
data_baru = pd.DataFrame({"jam_belajar": [6.5]})
print("Prediksi nilai untuk 6.5 jam:", round(model.predict(data_baru)[0], 1))

# 5. Evaluasi pada data uji
prediksi = model.predict(X_test)
print("MAE data uji:", round(mean_absolute_error(y_test, prediksi), 2))
```

## Cara menjalankan

```bash
python praktik_pertama.py
```

## Output yang diharapkan

```text
   jam_belajar  nilai_ujian
0            1           52
1            2           55
2            3           61
3            4           64
4            5           70
Data latih: 7 baris | Data uji: 3 baris
Model: nilai = 4.45 x jam + 47.28
Prediksi nilai untuk 6.5 jam: 76.2
MAE data uji: 1.82
```

!!! note "Kalau angkamu sedikit berbeda"
    Pembagian data memakai pengacakan. Parameter `random_state=42` mengunci pengacakan itu agar hasilnya sama setiap kali dijalankan. Versi pustaka yang jauh berbeda dapat menghasilkan selisih sangat kecil pada angka desimal.

## Penjelasan kode

| Bagian | Yang terjadi | Istilah |
|---|---|---|
| `pd.DataFrame({...})` | Membuat tabel 10 baris | **Dataset** |
| `X = data[["jam_belajar"]]` | Memilih kolom masukan | **Feature** |
| `y = data["nilai_ujian"]` | Memilih kolom yang ditebak | **Target** |
| `train_test_split(...)` | Memisahkan data latih dan uji | **Training data** dan **testing data** |
| `LinearRegression()` | Menyiapkan algoritma, belum belajar apa pun | **Algorithm** |
| `model.fit(X_train, y_train)` | Algoritma belajar dari data latih | **Training** |
| `model.coef_`, `model.intercept_` | Angka hasil belajar | **Parameter** model (\(w\) dan \(b\)) |
| `model.predict(...)` | Menebak nilai untuk data baru | **Prediction** |
| `mean_absolute_error(...)` | Menghitung rata-rata selisih | **Evaluation** |

Perhatikan polanya. Hampir semua model Scikit-learn dipakai dengan pola yang sama:

1. Buat objek model.
2. Panggil `.fit(...)` untuk melatih.
3. Panggil `.predict(...)` untuk memprediksi.

Pola ini akan berulang pada algoritma clustering nanti.

## Membaca hasilnya

- `4.45 x jam + 47.28` berarti: tiap tambahan 1 jam belajar, model memperkirakan nilai naik sekitar 4,45 poin. Orang yang belajar 0 jam diperkirakan bernilai sekitar 47,28.
- Prediksi 76,2 untuk 6,5 jam adalah hasil \(4{,}45 \times 6{,}5 + 47{,}28\).
- MAE 1,82 berarti rata-rata tebakan meleset sekitar 1,82 poin pada data uji.

!!! warning "Jangan terlalu percaya pada data sekecil ini"
    Sepuluh baris hanya untuk belajar konsep. Pada proyek nyata, data jauh lebih banyak, dan hubungan antar variabel jarang serapi ini.

## Pemecahan masalah

| Gejala | Kemungkinan penyebab | Solusi |
|---|---|---|
| `ModuleNotFoundError: No module named 'sklearn'` | Scikit-learn belum terpasang | Jalankan `pip install scikit-learn` (nama paketnya `scikit-learn`, nama impornya `sklearn`) |
| `ValueError: Expected 2D array, got 1D array` | Fitur diberikan sebagai satu kolom `Series` | Pakai dua kurung siku: `data[["jam_belajar"]]` |
| Angka berbeda dari output di atas | `random_state` diubah atau dihapus | Gunakan `random_state=42` |
| `python` tidak dikenali | Python belum masuk PATH | Coba `py praktik_pertama.py` (Windows) atau `python3 praktik_pertama.py` |

Lanjut ke [Latihan](12-exercises.md).
