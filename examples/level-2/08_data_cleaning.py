"""Level 2, Bab 8: membersihkan data (data cleaning).

Data asli sudah cukup bersih, jadi kita berlatih juga pada tabel kecil
yang SENGAJA dibuat kotor (artifisial) di dalam kode.

Jalankan dari folder utama proyek:
    python examples/level-2/08_data_cleaning.py
"""
# NB: setup=Siapkan alat dan muat data | check=Periksa konsistensi data asli | messy=Buat tabel kecil yang sengaja kotor | text=Merapikan teks | numeric=Mengubah teks menjadi angka | ranges=Memeriksa rentang nilai yang masuk akal | rename=Merapikan nama kolom | pipeline=Membungkus semuanya dalam satu fungsi

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd

pd.set_option("display.width", 120)  # agar tabel lebar tidak dipotong
pd.set_option("display.max_columns", None)

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

# --8<-- [start:check]
print("Nilai pada Gender:", sorted(df["Gender"].unique()))
print("Spasi berlebih pada Gender:", (df["Gender"] != df["Gender"].str.strip()).sum())

print("\nNama kolom:", df.columns.tolist())

print("\nUsia di luar 18-100         :", (~df["Age"].between(18, 100)).sum())
print("Skor di luar 1-100          :", (~df["Spending Score (1-100)"].between(1, 100)).sum())
print("Pendapatan negatif atau nol :", (df["Annual Income (k$)"] <= 0).sum())
# --8<-- [end:check]

# --8<-- [start:messy]
kotor = pd.DataFrame(
    {
        "CustomerID": [1, 2, 3, 4, 5],
        "Gender": [" male", "FEMALE", "Female ", "Male", "female"],
        "Age": ["19", "21", "tidak diketahui", "23", "250"],
        "Annual Income (k$)": [15, 15, 16, 16, 17],
        "Spending Score (1-100)": [39, 81, 6, 77, 40],
    }
)
print(kotor)
print()
print(kotor.dtypes)
# --8<-- [end:messy]

# --8<-- [start:text]
bersih = kotor.copy()
bersih["Gender"] = bersih["Gender"].str.strip().str.title()

print("Nilai Gender sebelum:", kotor["Gender"].tolist())
print("Nilai Gender sesudah:", bersih["Gender"].tolist())
# --8<-- [end:text]

# --8<-- [start:numeric]
bersih["Age"] = pd.to_numeric(bersih["Age"], errors="coerce")

print(bersih["Age"].tolist())
print("Tipe sekarang:", bersih["Age"].dtype)
print("Jumlah nilai kosong pada Age:", bersih["Age"].isna().sum())
# --8<-- [end:numeric]

# --8<-- [start:ranges]
tidak_masuk_akal = ~bersih["Age"].between(18, 100) & bersih["Age"].notna()
print("Usia tidak masuk akal:")
print(bersih[tidak_masuk_akal])

bersih.loc[tidak_masuk_akal, "Age"] = float("nan")
print("\nUsia setelah dikosongkan:", bersih["Age"].tolist())
# --8<-- [end:ranges]

# --8<-- [start:rename]
bersih = bersih.rename(
    columns={
        "CustomerID": "customer_id",
        "Annual Income (k$)": "annual_income_k",
        "Spending Score (1-100)": "spending_score",
        "Gender": "gender",
        "Age": "age",
    }
)
print(bersih.columns.tolist())
# --8<-- [end:rename]

# --8<-- [start:pipeline]
def bersihkan(data):
    """Membersihkan tabel pelanggan. Mengembalikan tabel baru."""
    hasil = data.copy()
    hasil["Gender"] = hasil["Gender"].str.strip().str.title()
    hasil["Age"] = pd.to_numeric(hasil["Age"], errors="coerce")
    hasil.loc[~hasil["Age"].between(18, 100), "Age"] = float("nan")
    return hasil


hasil_kotor = bersihkan(kotor)
print("Tabel kotor setelah dibersihkan:")
print(hasil_kotor)

hasil_asli = bersihkan(df)
print("\nIsi kolom Age pada data asli tetap sama?", (hasil_asli["Age"] == df["Age"]).all())
print("Tipe Age sebelum :", df["Age"].dtype)
print("Tipe Age sesudah :", hasil_asli["Age"].dtype)
# --8<-- [end:pipeline]
