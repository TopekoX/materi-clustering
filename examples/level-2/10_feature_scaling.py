"""Level 2, Bab 10: feature scaling pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/10_feature_scaling.py
"""
# NB: setup=Siapkan alat dan muat data | raw=Masalah: rentang dan varians tiap fitur berbeda | minmax=Min-Max scaling | standard=Standardization (z-score) | sklearn=Hasil yang sama dengan scikit-learn | after=Porsi varians setelah skala disamakan | plot=Melihat efeknya pada grafik

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

DATA_PATH = "data/mall_customers.csv"
df = pd.read_csv(DATA_PATH)

fitur = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
X = df[fitur]
# --8<-- [end:setup]

import _savefig

_savefig.install(["10-scaling-scatter"])

# --8<-- [start:raw]
print("Rentang tiap fitur:")
print(X.agg(["min", "max"]))

varians = X.var()
print("\nVarians tiap fitur:")
print(varians.round(1))

print("\nPorsi varians (persen) pada skala asli:")
print((varians / varians.sum() * 100).round(1))
# --8<-- [end:raw]

# --8<-- [start:minmax]
X_minmax = (X - X.min()) / (X.max() - X.min())

print("Min-Max scaling (5 baris pertama):")
print(X_minmax.head().round(3))

print("\nMin dan max setiap kolom:")
print(X_minmax.agg(["min", "max"]))
# --8<-- [end:minmax]

# --8<-- [start:standard]
X_standar = (X - X.mean()) / X.std(ddof=0)

print("Standardization (5 baris pertama):")
print(X_standar.head().round(3))

print("\nRata-rata dan simpangan baku setiap kolom:")
print(X_standar.agg(["mean", "std"]).round(3))
# --8<-- [end:standard]

# --8<-- [start:sklearn]
from sklearn.preprocessing import MinMaxScaler, StandardScaler

X_minmax_sk = MinMaxScaler().fit_transform(X)
X_standar_sk = StandardScaler().fit_transform(X)

print("Min-Max sama dengan hitungan manual?",
      abs(X_minmax_sk - X_minmax.to_numpy()).max() < 1e-9)
print("Standardization sama dengan hitungan manual?",
      abs(X_standar_sk - X_standar.to_numpy()).max() < 1e-9)
# --8<-- [end:sklearn]

# --8<-- [start:after]
for nama, data in [("Min-Max", X_minmax), ("Standardization", X_standar)]:
    v = data.var()
    print(f"Porsi varians (persen) setelah {nama}:")
    print((v / v.sum() * 100).round(1))
    print()
# --8<-- [end:after]

# --8<-- [start:plot]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

axes[0].scatter(X["Annual Income (k$)"], X["Age"], s=14)
axes[0].set_title("Skala asli")
axes[0].set_xlabel("Annual Income (k$)")
axes[0].set_ylabel("Age")
axes[0].set_aspect("equal")

axes[1].scatter(X_standar["Annual Income (k$)"], X_standar["Age"], s=14)
axes[1].set_title("Setelah standardization")
axes[1].set_xlabel("Annual Income (z-score)")
axes[1].set_ylabel("Age (z-score)")
axes[1].set_aspect("equal")

fig.tight_layout()
plt.show()
# --8<-- [end:plot]
