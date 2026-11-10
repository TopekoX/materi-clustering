# QA Report — Level 5: Clustering Evaluation

Tanggal: 2026-11-10 · Lingkungan: Python 3.14.7, NumPy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1, SciPy 1.18.1, matplotlib 3.11.2, MkDocs 1.6.1 + Material 9.8.1

## Bab selesai

8 dari 8 bab (`docs/clustering-evaluation/01`–`08`) plus `index.md`. Semua mengikuti 14 bagian standar `CLAUDE.md` (keputusan 2026-11-10, bukan 15 bagian dari prompt tugas). Pemetaan: *Step-by-Step Calculation* masuk *Mathematical Foundation*; *Step-by-Step Code Explanation* menjadi penjelasan di bawah tiap blok kode pada *Python Implementation*; *Output and Interpretation* dan *Visualization* masuk *Expected Output*; *Advantages and Limitations* masuk *Detailed Explanation*; *Common Mistakes* masuk *Troubleshooting*; *Preparation for Level 6* masuk *Summary* Bab 8.

| Bab | File | Isi | Hitungan manual |
|---|---|---|---|
| 1 | `01-introduction-to-clustering-evaluation.md` | Evaluasi vs klasifikasi, ciri clustering baik, internal/eksternal/relatif | — |
| 2 | `02-internal-clustering-evaluation.md` | Jarak dalam/antar kelompok, cohesion, separation, density | Enam titik |
| 3 | `03-inertia-and-wcss.md` | Inertia/WCSS, pengaruh K, skala, jumlah data | Enam titik |
| 4 | `04-elbow-method.md` | Elbow, persentase penurunan, heuristik jarak ke garis | Persentase penurunan |
| 5 | `05-silhouette-score.md` | Silhouette, silhouette plot, `sample_size`, noise DBSCAN | Tujuh titik |
| 6 | `06-davies-bouldin-index.md` | DBI | Sembilan titik |
| 7 | `07-calinski-harabasz-index.md` | CHI, perbandingan tiga metrik internal | Sembilan titik |
| 8 | `08-external-evaluation-and-metric-comparison.md` | ARI, NMI, Homogeneity, Completeness, V-measure, perbandingan empat algoritma | ARI dan NMI pada sembilan titik |

Total 3510 baris Markdown (termasuk `index.md`).

## Validasi

| Pemeriksaan | Hasil |
|---|---|
| `mkdocs build --strict` | Lulus (tautan, anchor, gambar, snippet `check_paths`) |
| Skrip `examples/level-5/01`–`08` | Semua dijalankan ulang di akhir: output identik byte demi byte dengan `outputs/NN.txt`. Output nyata disertakan ke bab lewat snippet |
| Notebook `notebooks/level-5/01`–`08` | Semua dieksekusi dengan `jupyter nbconvert --execute`, 0 error. Hasil eksekusi hanya di folder sementara. Notebook di repo tidak berisi output (sama seperti Level 2 sampai 4). Notebook dibangun dari potongan skrip dan teks bab yang sama |
| Rumus | 468 rumus pada halaman hasil build diurai dengan parser TeX MathJax 3.2.2 (paket `base`, `ams`, `newcommand`, `configmacros`): 0 galat. Pemeriksa diuji dahulu dengan rumus yang sengaja salah (terdeteksi) dan rumus benar (diterima). Pemeriksaan menemukan `\boldsymbol` di Bab 2 dan 3, yang tidak didukung di situs ini, dan sudah diganti dengan `\mu` |
| Hitungan manual vs kode | Cocok: cohesion 0,654 dan jarak antar centroid 6,403 (Bab 2); WCSS 2,667 (Bab 3); Silhouette 0,729 dan 0,044, rata-rata 0,656 (Bab 5); DBI 0,2177 (Bab 6); CH 93,0 (Bab 7); ARI 0,3571 dan NMI 0,5895 (Bab 8) |
| Penanda `--8<--` tersisa di HTML | Tidak ada |
| Mermaid | Diagram ada di HTML hasil build (3 halaman: Bab 1, 4, 8). **Sintaks Mermaid belum dirender di browser** |
| Gambar | 17 gambar di `docs/assets/level-5/`. Semuanya dilihat langsung selama pengerjaan. Satu legenda yang menutupi batang (Bab 8) diperbaiki |
| Angka di bab | Semua output, tabel interpretasi, dan jawaban latihan berasal dari eksekusi nyata atau hitungan manual yang dicek dengan kode |
| Level 1–4 | Tidak diubah. Perubahan git hanya pada file Level 5 dan berkas koordinasi di bawah |
| Dependensi | Tidak ada dependensi baru. `requirements-notebooks.txt` tidak diubah |

## Verifikasi formula

Rumus di bab dicocokkan dengan definisi scikit-learn:

- Silhouette: \( s(i) = (b-a)/\max(a,b) \), `silhouette_samples` memberi hasil identik dengan fungsi manual.
- Davies-Bouldin: sebaran = rata-rata jarak ke centroid, \( R_{ij} = (S_i+S_j)/M_{ij} \), DBI = rata-rata nilai maksimum. Identik dengan `davies_bouldin_score`.
- Calinski-Harabasz: \( [B/(k-1)]/[W/(n-k)] \), dan \( B+W = \) jumlah kuadrat total (diperiksa dengan kode). Identik dengan `calinski_harabasz_score`.
- ARI dan NMI: identik dengan `adjusted_rand_score` dan `normalized_mutual_info_score` (rata-rata aritmetika). V-measure sama dengan NMI aritmetika di semua baris output, sesuai teori.
- Sifat yang ditegaskan dan diuji: Inertia dikali \( c^2 \) saat skala dikali \( c \) (rasio 100,0); Silhouette, DBI, dan CHI tidak berubah saat seluruh data dikali 10; CHI naik sekitar 2,01 kali pada data yang digandakan.

## Temuan penting yang disampaikan di bab

- Data acak tanpa kelompok tetap menghasilkan skor dan kurva yang tampak seperti siku (Bab 1, 4, 6, 7).
- Heuristik siku otomatis menjawab K = 3 pada data dengan 4 gerombol jelas (rentang K 1 sampai 10), dan berubah menjadi 4 bila rentang sampai 15 (Bab 4).
- Metrik internal menyukai kelompok bulat: pada moons, label benar mendapat skor lebih rendah daripada K-Means yang memotong bentuk (Silhouette, DBI, CHI, Inertia; Bab 2 sampai 7).
- CHI menunjuk K = 9 pada Mall Customers dan K = 10 pada data acak, sedangkan Silhouette dan DBI menunjuk K = 5 (Bab 7).
- Metrik internal dan eksternal berlawanan pada hasil DBSCAN untuk Moons dan Circles (Bab 8).
- Perlakuan noise DBSCAN memengaruhi angka dan dinyatakan: dikeluarkan untuk metrik internal, dijadikan satu kelompok untuk metrik eksternal (Bab 5 dan 8).
- Nomor kelompok sembarang: kecocokan langsung 0,333 padahal ARI 1,000 (Bab 8).

## Cakupan terhadap Level 4 dan Level 6

- **Level 4:** Bab 3 dan 4 Level 5 menautkan ke Level 4 Bab 2 (WCSS dan elbow singkat) lalu memperdalam (hitungan manual, batas elbow, skala). Tidak ada penulisan ulang K-Means. Eksperimen Bab 8 memakai K-Means, Hierarchical, DBSCAN, dan GMM dari Level 4. Mean Shift tidak dipakai di eksperimen agar tabel tetap terbaca.
- **Level 6:** tidak ada desain eksperimen sistematis. Parameter DBSCAN dipilih sama (`eps = 0,30`) setelah melihat data, dan kepekaannya ditunjukkan dengan peringatan eksplisit bahwa menyetel `eps` memakai label acuan adalah kebocoran informasi. Pencarian parameter dan uji stabilitas dirujuk ke Level 6.

## File dibuat

- `docs/clustering-evaluation/index.md`, `01`–`08-*.md`
- `examples/level-5/01`–`08_*.py`, `_savefig.py`, `outputs/01`–`08.txt`
- `docs/assets/level-5/*.png` (17 gambar)
- `notebooks/level-5/01`–`08-*.ipynb`
- `LEVEL5_QA_REPORT.md`

## File diubah

- `mkdocs.yml`: hanya `nav:` (Level 5, 8 bab).
- `CLAUDE.md`: lingkup proyek mencantumkan Level 5 dan folder `docs/clustering-evaluation/`.
- `PRD.md`: bagian Level 5 menggantikan kalimat "Level 5–7 di luar lingkup".
- `IMPLEMENTATION_PLAN.md`: tabel status Level 5.
- `docs/curriculum/index.md`: daftar bab Level 5 menggantikan baris "Level 5–7"; Level 6 dan 7 tetap "Direncanakan".

## Masalah yang diketahui

- Sintaks Mermaid (3 diagram) belum dirender di browser. Hanya keberadaannya di HTML hasil build yang dicek.
- Rumus diperiksa lewat penguraian TeX di Node, bukan lewat tampilan browser. MathJax di situs memuat dari CDN dan membutuhkan jaringan.
- Tampilan gambar pada tema gelap tidak diperiksa (gambar matplotlib berlatar putih, sama seperti Level 2 sampai 4).
- Seluruh pengujian pada satu lingkungan (Python 3.14.7 dan versi pustaka di atas). Batas bawah versi di `requirements-notebooks.txt` masih perkiraan.
- Dataset sintetis lebih bersih daripada data nyata. Dinyatakan di bab, tetapi pembaca tetap perlu berhati-hati menyamakan skor dengan data nyata.
- Paket Python (`numpy`, `scikit-learn`, dan lain-lain) dipasang ke `.venv` selama pengerjaan. `.venv` tidak dilacak git.
- Inertia Mall Customers (K = 4, 5, 6: 108,92; 65,57; 55,06) dan ukuran kelompok K-Means K = 5 (81, 39, 22, 35, 23) sama dengan angka di Level 4 Bab 2, sehingga konsisten antar level.

## Tugas tersisa

- Tinjauan isi oleh pengguna, terutama nada penjelasan untuk pemula.
- Pemeriksaan Mermaid dan tampilan tema gelap di browser (`mkdocs serve`).
- Commit dan penerbitan, hanya atas instruksi eksplisit (`origin` masih `mkdocs-template`).
- Penyusunan daftar bab Level 6 (Experimentation and Interpretation), menunggu persetujuan Level 5.
