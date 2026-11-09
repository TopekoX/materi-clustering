"""Level 2, Bab 1: eksplorasi pertama dataset Mall Customers."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # simpan gambar ke file, tanpa membuka jendela
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "mall_customers.csv"
FIG_DIR = ROOT / "docs" / "assets" / "level-2"

# 1. Muat data
df = pd.read_csv(DATA_PATH)

# 2. Lihat sekilas
print("Lima baris pertama:")
print(df.head())

print("\nUkuran (baris, kolom):", df.shape)

print("\nTipe data per kolom:")
print(df.dtypes)

# 3. Ringkasan statistik kolom numerik
print("\nRingkasan statistik:")
print(df.describe().round(2))

# 4. Pemeriksaan kualitas dasar
print("\nJumlah nilai kosong per kolom:")
print(df.isna().sum())
print("\nJumlah baris duplikat:", df.duplicated().sum())

print("\nJumlah per Gender:")
print(df["Gender"].value_counts())

# 5. Visualisasi awal
features = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, col in zip(axes, features):
    ax.hist(df[col], bins=15, edgecolor="white")
    ax.set_title(col)
    ax.set_ylabel("Jumlah pelanggan")
fig.tight_layout()
fig.savefig(FIG_DIR / "01-distribusi-fitur.png", dpi=120)
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.scatter(df["Annual Income (k$)"], df["Spending Score (1-100)"], s=18)
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1-100)")
ax.set_title("Pendapatan vs skor belanja")
fig.tight_layout()
fig.savefig(FIG_DIR / "01-scatter-income-spending.png", dpi=120)
plt.close(fig)

print("\nGambar disimpan di:", FIG_DIR.relative_to(ROOT))
