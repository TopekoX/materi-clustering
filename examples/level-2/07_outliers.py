"""Level 2, Bab 7: mendeteksi dan menangani outlier pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/07_outliers.py
"""
# NB: setup=Siapkan alat dan muat data | iqr=Mendeteksi outlier dengan aturan IQR | zscore=Mendeteksi outlier dengan z-score | plot=Melihat outlier pada grafik | remove=Pilihan 1: buang baris outlier | cap=Pilihan 2: batasi nilai (capping) | compare=Bandingkan ketiga pilihan

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)

fitur = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
# --8<-- [end:setup]

import _savefig

_savefig.install(["07-outlier-income"])

# --8<-- [start:iqr]
q1 = df[fitur].quantile(0.25)
q3 = df[fitur].quantile(0.75)
iqr = q3 - q1

batas_bawah = q1 - 1.5 * iqr
batas_atas = q3 + 1.5 * iqr

print("Batas bawah:")
print(batas_bawah)
print("\nBatas atas:")
print(batas_atas)

di_luar = (df[fitur] < batas_bawah) | (df[fitur] > batas_atas)
print("\nJumlah outlier per kolom (aturan IQR):")
print(di_luar.sum())

print("\nBaris yang punya outlier:")
print(df[di_luar.any(axis=1)])
# --8<-- [end:iqr]

# --8<-- [start:zscore]
z = (df[fitur] - df[fitur].mean()) / df[fitur].std()

print("Nilai |z| terbesar per kolom:")
print(z.abs().max().round(2))

print("\nJumlah |z| > 3 per kolom:")
print((z.abs() > 3).sum())
# --8<-- [end:zscore]

# --8<-- [start:plot]
kolom = "Annual Income (k$)"
is_outlier = di_luar[kolom]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(
    df.loc[~is_outlier, kolom],
    df.loc[~is_outlier, "Spending Score (1-100)"],
    s=16,
    label="Normal",
)
ax.scatter(
    df.loc[is_outlier, kolom],
    df.loc[is_outlier, "Spending Score (1-100)"],
    s=60,
    color="red",
    label="Outlier (IQR)",
)
ax.set_xlabel(kolom)
ax.set_ylabel("Spending Score (1-100)")
ax.legend()
plt.show()
# --8<-- [end:plot]

# --8<-- [start:remove]
df_buang = df[~di_luar.any(axis=1)]

print("Sebelum:", df.shape)
print("Sesudah:", df_buang.shape)
# --8<-- [end:remove]

# --8<-- [start:cap]
df_batas = df.copy()
for k in fitur:
    df_batas[k] = df_batas[k].clip(lower=batas_bawah[k], upper=batas_atas[k])

print("Ukuran:", df_batas.shape)
print("Nilai maksimum Annual Income sebelum:", df[kolom].max())
print("Nilai maksimum Annual Income sesudah :", df_batas[kolom].max())
# --8<-- [end:cap]

# --8<-- [start:compare]
ringkas = pd.DataFrame(
    {
        "asli": df[kolom].agg(["count", "mean", "std", "max"]),
        "dibuang": df_buang[kolom].agg(["count", "mean", "std", "max"]),
        "dibatasi": df_batas[kolom].agg(["count", "mean", "std", "max"]),
    }
).round(2)

print(ringkas)
# --8<-- [end:compare]
