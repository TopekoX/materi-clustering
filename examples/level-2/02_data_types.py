"""Level 2, Bab 2: memahami tipe data pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/02_data_types.py
"""
# NB: setup=Siapkan alat dan muat data | dtypes=Lihat tipe data tiap kolom | split=Pisahkan kolom angka dan kolom teks | unique=Hitung nilai unik | category=Ubah teks menjadi tipe category | scale=Cek rentang nilai untuk mengenali jenis angka

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)
# --8<-- [end:setup]

# --8<-- [start:dtypes]
print("Tipe data per kolom:")
print(df.dtypes)

print("\nInfo ringkas:")
df.info()
# --8<-- [end:dtypes]

# --8<-- [start:split]
kolom_angka = df.select_dtypes(include="number").columns.tolist()
kolom_teks = df.select_dtypes(exclude="number").columns.tolist()

print("Kolom angka:", kolom_angka)
print("Kolom teks :", kolom_teks)
# --8<-- [end:split]

# --8<-- [start:unique]
print("Jumlah nilai unik per kolom:")
print(df.nunique())

print("\nNilai unik pada Gender:", df["Gender"].unique())
# --8<-- [end:unique]

# --8<-- [start:category]
print("Memori sebelum :", df["Gender"].memory_usage(deep=True), "byte")

df["Gender"] = df["Gender"].astype("category")

print("Memori sesudah :", df["Gender"].memory_usage(deep=True), "byte")
print("Tipe sekarang  :", df["Gender"].dtype)
print("Kategori       :", list(df["Gender"].cat.categories))
# --8<-- [end:category]

# --8<-- [start:scale]
for kolom in ["Age", "Annual Income (k$)", "Spending Score (1-100)"]:
    print(f"{kolom}: min={df[kolom].min()}, max={df[kolom].max()}")

print("\nCustomerID berurutan 1..200?", df["CustomerID"].tolist() == list(range(1, 201)))
# --8<-- [end:scale]
