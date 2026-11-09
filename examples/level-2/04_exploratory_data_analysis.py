"""Level 2, Bab 4: Exploratory Data Analysis (EDA) pada Mall Customers.

Jalankan dari folder utama proyek:
    python examples/level-2/04_exploratory_data_analysis.py
"""
# NB: setup=Siapkan alat dan muat data | box=Box plot tiap fitur | bar=Diagram batang untuk kolom kategori | pairs=Scatter plot untuk tiap pasangan fitur | gender=Scatter plot berwarna menurut Gender | heatmap=Heatmap korelasi | age=Spending Score menurut kelompok usia

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

_savefig.install(
    [
        "04-boxplot",
        "04-gender-bar",
        "04-scatter-pairs",
        "04-scatter-gender",
        "04-heatmap",
        "04-age-group",
    ]
)

# --8<-- [start:box]
fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, col in zip(axes, fitur):
    ax.boxplot(df[col])
    ax.set_title(col)
fig.tight_layout()
plt.show()
# --8<-- [end:box]

# --8<-- [start:bar]
jumlah = df["Gender"].value_counts()
print(jumlah)

fig, ax = plt.subplots(figsize=(4, 3.5))
ax.bar(jumlah.index, jumlah.values)
ax.set_ylabel("Jumlah pelanggan")
ax.set_title("Jumlah pelanggan per Gender")
plt.show()
# --8<-- [end:bar]

# --8<-- [start:pairs]
pasangan = [
    ("Age", "Annual Income (k$)"),
    ("Age", "Spending Score (1-100)"),
    ("Annual Income (k$)", "Spending Score (1-100)"),
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for ax, (x, y) in zip(axes, pasangan):
    ax.scatter(df[x], df[y], s=14)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
fig.tight_layout()
plt.show()
# --8<-- [end:pairs]

# --8<-- [start:gender]
fig, ax = plt.subplots(figsize=(6, 4.5))
for nama, kelompok in df.groupby("Gender"):
    ax.scatter(
        kelompok["Annual Income (k$)"],
        kelompok["Spending Score (1-100)"],
        s=18,
        label=nama,
        alpha=0.8,
    )
ax.set_xlabel("Annual Income (k$)")
ax.set_ylabel("Spending Score (1-100)")
ax.legend(title="Gender")
plt.show()
# --8<-- [end:gender]

# --8<-- [start:heatmap]
korelasi = df[fitur].corr()
print(korelasi.round(2))

fig, ax = plt.subplots(figsize=(5.5, 4.5))
gambar = ax.imshow(korelasi, vmin=-1, vmax=1, cmap="coolwarm")
ax.set_xticks(range(len(fitur)), fitur, rotation=30, ha="right")
ax.set_yticks(range(len(fitur)), fitur)
for i in range(len(fitur)):
    for j in range(len(fitur)):
        ax.text(j, i, f"{korelasi.iloc[i, j]:.2f}", ha="center", va="center")
fig.colorbar(gambar)
plt.show()
# --8<-- [end:heatmap]

# --8<-- [start:age]
df["Age Group"] = pd.cut(
    df["Age"],
    bins=[17, 30, 45, 60, 70],
    labels=["18-30", "31-45", "46-60", "61-70"],
)
rata = df.groupby("Age Group", observed=True)["Spending Score (1-100)"].mean()
print(rata.round(2))

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.bar(rata.index.astype(str), rata.values)
ax.set_xlabel("Kelompok usia")
ax.set_ylabel("Rata-rata Spending Score")
plt.show()
# --8<-- [end:age]
