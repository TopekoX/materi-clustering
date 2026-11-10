"""Level 4, Bab 5: Gaussian Mixture Models (GMM) dan algoritma EM.

Jalankan dari folder utama proyek:
    python examples/level-4/05_gaussian_mixture_models.py
"""
# NB: setup=Siapkan alat | gauss1d=Distribusi Gaussian satu dimensi | gauss2d=Distribusi Gaussian multivariat | plotcov=Bentuk Gaussian menurut kovarians | em1d=Algoritma EM dari nol (1 dimensi) | plotem=Menggambar hasil EM 1 dimensi | emsk=Membandingkan dengan scikit-learn | data2d=Data dua dimensi berbentuk elips | helpers=Fungsi bantu elips | fit=GMM scikit-learn | proba=Label dan peluang keanggotaan | manual=Menghitung peluang secara manual | iterations=Iterasi EM | covtypes=Empat tipe kovarians | plotcov2=Menggambar empat tipe kovarians | plotcmp=K-Means dibanding GMM | mall=GMM pada Mall Customers | newpoint=Peluang pelanggan baru | plotmall=Menggambar hasil Mall

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --8<-- [start:setup]
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.cluster import KMeans
from sklearn.exceptions import ConvergenceWarning
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
# --8<-- [end:setup]

import _savefig

_savefig.install(
    ["05-gaussian-kovarians", "05-em-1d", "05-tipe-kovarians", "05-kmeans-vs-gmm", "05-mall-customers"]
)

# --8<-- [start:gauss1d]
def normal_pdf(x, mean, var):
    """Kepadatan Gaussian satu dimensi N(x | mean, var)."""
    return np.exp(-((x - mean) ** 2) / (2 * var)) / np.sqrt(2 * np.pi * var)

print("N(3 | mean=1, var=4) =", round(float(normal_pdf(3, 1, 4)), 5))
print("N(3 | mean=8, var=4) =", round(float(normal_pdf(3, 8, 4)), 5))
# --8<-- [end:gauss1d]

# --8<-- [start:gauss2d]
def mvn_pdf(X, mean, cov):
    """Kepadatan Gaussian multivariat. X berbentuk (n, d), mean (d,), cov (d, d)."""
    d = len(mean)
    diff = X - mean
    inv_cov = np.linalg.inv(cov)
    # Jarak Mahalanobis kuadrat tiap baris: (x - mean)^T Sigma^-1 (x - mean)
    mahalanobis_sq = np.einsum("ij,jk,ik->i", diff, inv_cov, diff)
    norm_const = 1.0 / np.sqrt((2 * np.pi) ** d * np.linalg.det(cov))
    return norm_const * np.exp(-0.5 * mahalanobis_sq)

point = np.array([[1.0, 1.0]])
print("Sigma = I, selisih (1, 1):", round(float(mvn_pdf(point, np.zeros(2), np.eye(2))[0]), 5))

diff = np.array([[2.0, 1.0]])
cov_diag = np.diag([4.0, 1.0])
m_sq = float(np.einsum("ij,jk,ik->i", diff, np.linalg.inv(cov_diag), diff)[0])
print("Sigma = diag(4, 1), selisih (2, 1): jarak Mahalanobis kuadrat =", m_sq)
# --8<-- [end:gauss2d]

# --8<-- [start:plotcov]
grid_x, grid_y = np.meshgrid(np.linspace(-4, 4, 200), np.linspace(-4, 4, 200))
grid = np.column_stack([grid_x.ravel(), grid_y.ravel()])

shapes = {
    "spherical\nSigma = [[1, 0], [0, 1]]": np.array([[1.0, 0.0], [0.0, 1.0]]),
    "diag\nSigma = [[3, 0], [0, 0.5]]": np.array([[3.0, 0.0], [0.0, 0.5]]),
    "full (korelasi positif)\nSigma = [[1, 0.8], [0.8, 1]]": np.array([[1.0, 0.8], [0.8, 1.0]]),
    "full (korelasi negatif)\nSigma = [[1, -0.8], [-0.8, 1]]": np.array([[1.0, -0.8], [-0.8, 1.0]]),
}

fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharex=True, sharey=True)
for ax, (title, cov) in zip(axes, shapes.items()):
    density = mvn_pdf(grid, np.zeros(2), cov).reshape(grid_x.shape)
    ax.contour(grid_x, grid_y, density, levels=6, cmap="Blues")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("x1")
    ax.set_aspect("equal")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotcov]

# --8<-- [start:em1d]
x = np.array([1.0, 2.0, 3.0, 6.0, 7.0, 9.0])  # enam titik satu dimensi

# Tebakan awal untuk dua komponen
means = np.array([1.0, 8.0])
variances = np.array([4.0, 4.0])
weights = np.array([0.5, 0.5])
initial_params = (means.copy(), variances.copy(), weights.copy())

for iteration in range(1, 9):
    # E-step: peluang tiap komponen "bertanggung jawab" atas tiap titik
    weighted_density = weights * normal_pdf(x[:, None], means, variances)  # bentuk (6, 2)
    log_likelihood = np.log(weighted_density.sum(axis=1)).sum()
    responsibilities = weighted_density / weighted_density.sum(axis=1, keepdims=True)

    # M-step: hitung ulang parameter berdasarkan tanggung jawab itu
    n_k = responsibilities.sum(axis=0)
    weights = n_k / len(x)
    means = (responsibilities * x[:, None]).sum(axis=0) / n_k
    variances = (responsibilities * (x[:, None] - means) ** 2).sum(axis=0) / n_k

    print(f"Iterasi {iteration}: log-likelihood = {log_likelihood:8.4f} | "
          f"means = {means.round(4).tolist()} | variances = {variances.round(4).tolist()} | "
          f"weights = {weights.round(4).tolist()}")
    if iteration == 1:
        print("  Tanggung jawab (kolom: komponen 1, komponen 2) pada iterasi 1:")
        print(pd.DataFrame(responsibilities, index=x, columns=["r_1", "r_2"]).round(4).to_string())
# --8<-- [end:em1d]

# --8<-- [start:plotem]
xs = np.linspace(-2, 12, 400)
fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
for ax, (m, v, w), title in zip(
    axes, [initial_params, (means, variances, weights)], ["Tebakan awal", "Setelah 8 iterasi EM"]
):
    for k, color in enumerate(["#0072B2", "#E69F00"]):
        ax.plot(xs, w[k] * normal_pdf(xs, m[k], v[k]), color=color, label=f"Komponen {k + 1}")
    ax.plot(xs, sum(w[k] * normal_pdf(xs, m[k], v[k]) for k in range(2)), color="black", linestyle="--",
            label="Campuran")
    ax.scatter(x, np.zeros_like(x), color="#444444", zorder=3, label="Data")
    ax.set_title(title)
    ax.set_xlabel("x")
axes[0].set_ylabel("Kepadatan (terbobot)")
axes[0].legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotem]

# --8<-- [start:emsk]
# Scikit-learn dengan tebakan awal yang sama, dibiarkan konvergen
gm_1d = GaussianMixture(
    n_components=2, means_init=[[1.0], [8.0]], weights_init=[0.5, 0.5],
    precisions_init=[[[0.25]], [[0.25]]], tol=1e-8, max_iter=500,
).fit(x[:, None])

print("scikit-learn means    :", gm_1d.means_.ravel().round(4).tolist())
print("scikit-learn variances:", gm_1d.covariances_.ravel().round(4).tolist())
print("scikit-learn weights  :", gm_1d.weights_.round(4).tolist())
print("scikit-learn log-likelihood total:", round(gm_1d.score(x[:, None]) * len(x), 4))
# --8<-- [end:emsk]

# --8<-- [start:data2d]
# Data dua dimensi yang diambil dari tiga distribusi Gaussian yang kita tentukan sendiri.
# Tiap kelompok berbentuk elips berbeda, ukurannya berbeda, dan sebagian saling tumpang tindih.
rng = np.random.default_rng(42)
true_components = [
    # (jumlah titik, rata-rata, matriks kovarians)
    (270, [0.0, 0.0], [[2.0, 1.6], [1.6, 2.0]]),     # elips miring ke kanan atas, besar
    (120, [1.5, 4.5], [[1.0, 0.0], [0.0, 0.3]]),     # elips mendatar, kecil
    (210, [4.5, 0.5], [[1.2, -0.7], [-0.7, 0.9]]),   # elips miring ke kanan bawah
]
X = np.vstack([rng.multivariate_normal(mean, cov, size=n) for n, mean, cov in true_components])
print("Bentuk X:", X.shape)
# --8<-- [end:data2d]

# --8<-- [start:helpers]
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00", "#56B4E9"]

def full_covariances(gmm):
    """Mengubah atribut covariances_ dari tipe apa pun menjadi matriks penuh (K, d, d)."""
    k, d = gmm.n_components, gmm.means_.shape[1]
    kind = gmm.covariance_type
    if kind == "full":
        return gmm.covariances_
    if kind == "tied":
        return np.array([gmm.covariances_] * k)
    if kind == "diag":
        return np.array([np.diag(c) for c in gmm.covariances_])
    return np.array([np.eye(d) * c for c in gmm.covariances_])  # spherical

def draw_ellipse(ax, mean, cov, color, n_std=2.0):
    """Menggambar elips n_std simpangan baku dari sebuah Gaussian."""
    values, vectors = np.linalg.eigh(cov)
    order = values.argsort()[::-1]
    values, vectors = values[order], vectors[:, order]
    angle = np.degrees(np.arctan2(vectors[1, 0], vectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(values)
    ax.add_patch(Ellipse(mean, width, height, angle=angle, fill=False, edgecolor=color, linewidth=2))
# --8<-- [end:helpers]

# --8<-- [start:fit]
gmm = GaussianMixture(
    n_components=3, covariance_type="full", max_iter=100, tol=1e-3,
    reg_covar=1e-6, n_init=5, random_state=42,
)
gmm.fit(X)

print("Konvergen?          :", gmm.converged_)
print("Iterasi (n_iter_)   :", gmm.n_iter_)
print("weights_            :", gmm.weights_.round(3).tolist())
print("means_ (bentuk)     :", gmm.means_.shape)
print("covariances_ (bentuk):", gmm.covariances_.shape)
print("Rata-rata log-likelihood per titik:", round(gmm.score(X), 4))

# Urutkan komponen menurut x1 supaya mudah dibandingkan dengan parameter pembangkit data
order = np.argsort(gmm.means_[:, 0])
true_weights = np.array([n for n, _, _ in true_components]) / len(X)
true_means = np.array([m for _, m, _ in true_components])
print("\nBobot sebenarnya   :", true_weights.round(3).tolist())
print("Bobot hasil GMM    :", gmm.weights_[order].round(3).tolist())
print("Rata-rata sebenarnya:\n", true_means)
print("Rata-rata hasil GMM :\n", gmm.means_[order].round(2))
# --8<-- [end:fit]

# --8<-- [start:proba]
labels_gmm = gmm.predict(X)
proba = gmm.predict_proba(X)

print("Ukuran tiap komponen:", np.bincount(labels_gmm).tolist())
print("\nPeluang lima titik pertama (tiap baris berjumlah 1):")
print(pd.DataFrame(proba[:5], columns=["p_0", "p_1", "p_2"]).round(3).to_string())
print("Jumlah tiap baris:", proba[:5].sum(axis=1).round(6).tolist())
print("\nlabel = argmax(peluang) untuk semua titik?", np.array_equal(labels_gmm, proba.argmax(axis=1)))

confidence = proba.max(axis=1)
print(f"Titik dengan peluang tertinggi < 0.9: {int((confidence < 0.9).sum())} dari {len(X)}")
print(f"Titik dengan peluang tertinggi < 0.6: {int((confidence < 0.6).sum())} dari {len(X)}")
# --8<-- [end:proba]

# --8<-- [start:manual]
# Hitung peluang keanggotaan sendiri dengan rumus: r_ik = pi_k * N(x_i | mu_k, Sigma_k) / jumlah
weighted = np.column_stack(
    [gmm.weights_[k] * mvn_pdf(X, gmm.means_[k], gmm.covariances_[k]) for k in range(3)]
)
manual_proba = weighted / weighted.sum(axis=1, keepdims=True)
print("Selisih terbesar dengan predict_proba:", float(np.abs(manual_proba - proba).max()))
# --8<-- [end:manual]

# --8<-- [start:iterations]
print("max_iter -> n_iter_, konvergen?, rata-rata log-likelihood per titik (tol sangat kecil)")
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=ConvergenceWarning)  # abaikan peringatan "belum konvergen"
    for max_iter in [1, 2, 3, 5, 10, 20, 50]:
        model = GaussianMixture(n_components=3, max_iter=max_iter, tol=1e-8,
                                n_init=1, random_state=0).fit(X)
        print(f"max_iter = {max_iter:<3} -> n_iter_ = {model.n_iter_:<3} konvergen = {str(model.converged_):<5} "
              f"log-likelihood = {model.score(X):.4f}")
# --8<-- [end:iterations]

# --8<-- [start:covtypes]
n_samples, d = X.shape
k = 3
param_formula = {
    "full": k * d * (d + 1) // 2,
    "tied": d * (d + 1) // 2,
    "diag": k * d,
    "spherical": k,
}

models = {}
for kind in ["full", "tied", "diag", "spherical"]:
    models[kind] = GaussianMixture(n_components=3, covariance_type=kind, n_init=5, random_state=42).fit(X)
    print(f"{kind:<10} covariances_ bentuk = {str(models[kind].covariances_.shape):<10} "
          f"parameter kovarians = {param_formula[kind]:<2} ukuran komponen = "
          f"{np.bincount(models[kind].predict(X)).tolist()}")
# --8<-- [end:covtypes]

# --8<-- [start:plotcov2]
fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharex=True, sharey=True)
for ax, (kind, model) in zip(axes, models.items()):
    labels = model.predict(X)
    for j in range(3):
        ax.scatter(X[labels == j, 0], X[labels == j, 1], s=8, color=palette[j])
        draw_ellipse(ax, model.means_[j], full_covariances(model)[j], "black")
    ax.set_title(f"covariance_type = '{kind}'")
    ax.set_xlabel("x1")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotcov2]

# --8<-- [start:plotcmp]
km = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X)
print("Ukuran K-Means:", np.bincount(km.labels_).tolist(), "| Ukuran GMM (full):", np.bincount(labels_gmm).tolist())

fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True, sharey=True)
for j in range(3):
    axes[0].scatter(X[km.labels_ == j, 0], X[km.labels_ == j, 1], s=10, color=palette[j])
axes[0].scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=160, marker="X", color="black")
axes[0].set_title("K-Means (K = 3): batas lurus, kelompok bulat")

for j in range(3):
    in_j = labels_gmm == j
    axes[1].scatter(X[in_j, 0], X[in_j, 1], s=10 + 60 * (1 - confidence[in_j]) ** 0.5, color=palette[j], alpha=0.7)
    draw_ellipse(axes[1], gmm.means_[j], gmm.covariances_[j], "black")
axes[1].set_title("GMM (full): elips 2 simpangan baku; titik besar = kurang yakin")
for ax in axes:
    ax.set_xlabel("x1")
axes[0].set_ylabel("x2")
plt.tight_layout()
plt.show()
# --8<-- [end:plotcmp]

# --8<-- [start:mall]
df = pd.read_csv("data/mall_customers.csv")
features = ["Annual Income (k$)", "Spending Score (1-100)"]
scaler = StandardScaler()
X_mall = scaler.fit_transform(df[features])

gmm_mall = GaussianMixture(n_components=5, covariance_type="full", n_init=5, random_state=42).fit(X_mall)
df["Cluster"] = gmm_mall.predict(X_mall)
proba_mall = gmm_mall.predict_proba(X_mall)
df["Confidence"] = proba_mall.max(axis=1)

print("Konvergen?:", gmm_mall.converged_, "| iterasi:", gmm_mall.n_iter_)
print("Bobot komponen:", gmm_mall.weights_.round(3).tolist())
print("Ukuran komponen:", np.bincount(df["Cluster"]).tolist())
print("Pusat dalam satuan asli:")
print(pd.DataFrame(scaler.inverse_transform(gmm_mall.means_), columns=features).round(1))
print(f"Pelanggan dengan peluang tertinggi < 0.9: {int((df['Confidence'] < 0.9).sum())} dari {len(df)}")

print("\nPeluang tiga pelanggan paling tidak pasti:")
uncertain = df["Confidence"].nsmallest(3).index
print(pd.DataFrame(proba_mall[uncertain], index=df.loc[uncertain, "CustomerID"],
                   columns=[f"p_{j}" for j in range(5)]).round(3).to_string())
# --8<-- [end:mall]

# --8<-- [start:newpoint]
new_customer = scaler.transform(pd.DataFrame([[60, 50]], columns=features))
print("Peluang pelanggan baru (pendapatan 60, skor 50):", gmm_mall.predict_proba(new_customer).round(3).tolist())
print("Label:", gmm_mall.predict(new_customer).tolist())
# --8<-- [end:newpoint]

# --8<-- [start:plotmall]
fig, ax = plt.subplots(figsize=(7, 5.5))
for j in range(5):
    members = df[df["Cluster"] == j]
    ax.scatter(members[features[0]], members[features[1]], s=14 + 70 * (1 - members["Confidence"]) ** 0.5,
               color=palette[j % len(palette)], alpha=0.8, label=f"Komponen {j}")
    # Ubah kovarians dari satuan terskala ke satuan asli
    cov_original = gmm_mall.covariances_[j] * np.outer(scaler.scale_, scaler.scale_)
    mean_original = scaler.inverse_transform(gmm_mall.means_[j][None, :])[0]
    draw_ellipse(ax, mean_original, cov_original, "black")
ax.set_xlabel(features[0])
ax.set_ylabel(features[1])
ax.set_title("GMM (5 komponen) pada Mall Customers; titik besar = kurang yakin")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
# --8<-- [end:plotmall]
