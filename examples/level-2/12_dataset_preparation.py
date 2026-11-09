"""Level 2, Bab 12: menyiapkan dataset akhir untuk clustering.

Jalankan dari folder utama proyek:
    python examples/level-2/12_dataset_preparation.py
"""
# NB: setup=Siapkan alat | pipeline=Menyusun alur persiapan dalam satu fungsi | run=Menjalankan alur pada data asli | sanity=Memeriksa dataset akhir | back=Mengembalikan ke satuan asli dan ke pelanggan | smoke=Uji coba: apakah algoritma menerima dataset ini?

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)

# --8<-- [start:setup]
import pandas as pd
from sklearn.preprocessing import StandardScaler

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", None)

DATA_PATH = "data/mall_customers.csv"
FITUR = ["Age", "Annual Income (k$)", "Spending Score (1-100)"]
# --8<-- [end:setup]


# --8<-- [start:pipeline]
def siapkan_dataset(path, fitur=FITUR):
    """Memuat, membersihkan, memilih fitur, dan menskalakan data pelanggan.

    Mengembalikan: tabel asli yang sudah bersih, tabel fitur terskala, dan scaler.
    """
    df = pd.read_csv(path)

    # 1. Bersihkan teks dan duplikat (Bab 6 dan 8)
    df["Gender"] = df["Gender"].str.strip().str.title()
    df = df.drop_duplicates().reset_index(drop=True)

    # 2. Pastikan tidak ada nilai kosong (Bab 5)
    if df[fitur].isna().any().any():
        raise ValueError("Masih ada nilai kosong pada fitur. Tangani dulu.")

    # 3. Outlier dipertahankan (Bab 7): hanya 2 baris dan nilainya masuk akal

    # 4. Pilih fitur (Bab 11): tiga kolom angka, tanpa CustomerID
    X = df[fitur]

    # 5. Samakan skala (Bab 10)
    scaler = StandardScaler()
    X_terskala = pd.DataFrame(scaler.fit_transform(X), columns=fitur, index=df.index)

    return df, X_terskala, scaler
# --8<-- [end:pipeline]


# --8<-- [start:run]
df_bersih, X, scaler = siapkan_dataset(DATA_PATH)

print("Tabel bersih   :", df_bersih.shape)
print("Dataset akhir  :", X.shape)
print("\nLima baris pertama dataset akhir:")
print(X.head().round(3))
# --8<-- [end:run]

# --8<-- [start:sanity]
print("Nilai kosong      :", X.isna().sum().sum())
print("Baris ganda       :", X.duplicated().sum())
print("Semua kolom angka :", all(X.dtypes == "float64"))

print("\nRata-rata (harus ~0):")
print(X.mean().round(6))

print("\nSimpangan baku (harus ~1):")
print(X.std(ddof=0).round(6))

print("\nBaris sama dengan data asli?", len(X) == len(df_bersih))
# --8<-- [end:sanity]

# --8<-- [start:back]
kembali = pd.DataFrame(
    scaler.inverse_transform(X), columns=FITUR, index=X.index
)
print("Tiga baris pertama, dikembalikan ke satuan asli:")
print(kembali.head(3).round(1))

print("\nSama dengan tabel bersih?",
      (kembali.round(6) == df_bersih[FITUR].astype(float).round(6)).all().all())

print("\nBaris 0 milik CustomerID:", df_bersih.loc[0, "CustomerID"])
# --8<-- [end:back]

# --8<-- [start:smoke]
from sklearn.cluster import KMeans

model = KMeans(n_clusters=5, n_init=10, random_state=42)
label = model.fit_predict(X)

print("Berhasil. Jumlah anggota per kelompok:")
print(pd.Series(label).value_counts().sort_index())
# --8<-- [end:smoke]
