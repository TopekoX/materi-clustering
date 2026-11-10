# Laporan QA — Level 7 (Research Project)

Tanggal: 2026-11-10. Status: sepuluh bab siap ditinjau. Belum ada commit.

## 1. Struktur akhir

```
docs/research-project/            index.md + 10 bab (01-... sampai 10-...)
docs/assets/level-7/              gambar (01-, 06-, 07-)
examples/level-7/                 helper (_research.py, _savefig.py), skrip 01-10, outputs/NN.txt
examples/level-7/results/         berkas hasil berawalan 02_ sampai 10_ dan 09_repro_package/
notebooks/level-7/                8 notebook (bab 2, 3, 4, 5, 6, 7, 9, 10)
```

Bab 1 dan 8 konseptual dan tidak punya notebook (sesuai rencana yang disetujui).

## 2. Bab

| Bab | Judul | Skrip | Notebook |
|---|---|---|---|
| 1 | Introduction to Clustering Research | ya | tidak (konseptual) |
| 2 | Research Problem Formulation | ya | ya |
| 3 | Literature Review and Research Gap | ya | ya |
| 4 | Dataset Selection and Research Data Preparation | ya | ya |
| 5 | Research Methodology and Experimental Protocol | ya | ya |
| 6 | Research Implementation with Python | ya | ya |
| 7 | Results Presentation and Discussion | ya | ya |
| 8 | Scientific Research Writing | ya | tidak (konseptual) |
| 9 | Reproducibility and Research Documentation | ya | ya |
| 10 | Final Clustering Research Project | ya | ya |

## 3. Dataset dan lisensi

- Breast Cancer Wisconsin (Diagnostic), UCI Machine Learning Repository, DOI 10.24432/C5DW2B.
- Lisensi **CC BY 4.0 menurut halaman UCI** (dibaca langsung saat Bab 1 dan Bab 4 ditulis). Atribusi dan pernyataan perubahan ada di `results/09_repro_package/DATA_ATTRIBUTION.md`.
- Salinan yang dimuat: `sklearn.datasets.load_breast_cancer`. Kecocokan dengan dokumentasi scikit-learn diperiksa (Bab 4); **belum** dibandingkan dengan file asli UCI.
- Persetujuan etik dan status de-identifikasi **tidak dinyatakan** pada sumber yang dibaca. Tidak ada klaim klinis.
- Mall Customers, Wine, dan dataset lain tidak dipakai di Level 7; lisensinya tidak diverifikasi.

## 4. Validasi

| Pemeriksaan | Hasil |
|---|---|
| `mkdocs build --strict` | Lulus tanpa peringatan |
| Notebook (8) | Semua valid (nbformat) dan dieksekusi tanpa error; output sel tersimpan |
| Skrip (10) | Semua berjalan; keluaran nyata disimpan di `outputs/NN.txt` |
| Keterulangan (Bab 9) | Skrip 01-08 dijalankan ulang; 67 berkas dibandingkan, 0 berubah; selisih keluaran hanya baris waktu Bab 5 |
| Manifest paket | Hash 67 berkas cocok dengan berkas saat ini |
| Hash protokol | Cocok (`c65be407e00ab39b...`); 0 amendment; 156 dari 156 eksekusi |
| Seed | 16 pemanggilan acak diperiksa dengan AST; tidak ada tanpa seed |
| QA akhir Bab 10 | 11 lulus, 2 peringatan, 0 gagal |
| Level 1-6 | Tidak ada berkas Level 1-6 yang berubah (`git status`) |

Berkas yang diubah di luar folder Level 7: `mkdocs.yml` (hanya `nav`), `docs/curriculum/index.md` (termasuk perbaikan baris Level 5), `PRD.md`, `IMPLEMENTATION_PLAN.md`, `CLAUDE.md`.

## 5. Cacat yang ditemukan dan diperbaiki selama pengerjaan

1. Output skrip yang memuat tanda "—" rusak saat dialihkan di Windows; ditambahkan `sys.stdout.reconfigure(encoding="utf-8")`.
2. Jawaban latihan Bab 2 salah (aturan "dan" tidak menangkap contoh); ditulis ulang dari hitungan nyata.
3. Kalimat masalah Bab 2 memakai "selalu" padahal DBSCAN pada data ini tidak menghasilkan kelompok; diperbaiki di sumber, dengan catatan revisi, tanpa mengubah hash protokol.
4. Pemeriksa Bab 7 melewatkan tanda minus dan salah menandai "pasti" di dalam "ketidakpastian"; diperbaiki (pencocokan kata utuh, negasi sederhana).
5. Teks notebook Bab 7 menyiratkan interval bootstrap menyempit saat ulangan ditambah; eksekusi nyata menunjukkan tidak, teks dikoreksi.
6. Bab 9: tabel struktur tidak idempoten (bergantung urutan eksekusi), hitungan "berkas belum di-commit" menghitung folder, helper Git error bila Git tidak ada, dan `outputs/09.txt` ikut masuk manifest padahal sedang ditulis; semuanya diperbaiki.
7. Bab 10: QA menangkap dua angka laporan (1,43 dan 1,42) yang belum terdaftar di registri fakta; didaftarkan dari berkas sumber.

## 6. Keterbatasan dan peringatan yang tersisa

- **Pustaka:** 0 dari 7 sumber dibaca penuh (hanya abstrak atau ringkasan). Dua sumber RQ2 (Milligan & Cooper, 1988; Steinley, 2004) hanya diverifikasi keberadaannya lewat pencarian karena halaman penerbit memerlukan akses berlangganan.
- **Versi kode:** 97 berkas Level 7 belum di-commit, sehingga paket reproduksi belum bisa menunjuk satu commit. Angka ini berubah setelah commit.
- **Tautan repositori** pada pernyataan data naskah masih placeholder.
- **Keterulangan** hanya terbukti pada mesin dan lingkungan yang sama (Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, Matplotlib 3.11.1).
- **Rumus** belum dilihat dirender di browser (membutuhkan jaringan untuk MathJax CDN); build strict tidak memeriksa rendering rumus.
- **Metodologi:** satu dataset (569 sampel); K = 2 dipengaruhi jumlah kelas diagnosis; protokol ditulis setelah demonstrasi Bab 1 (tidak sepenuhnya buta terhadap data); hanya DBSCAN yang disetel; analisis bootstrap, pangsa varians, dan uji dominasi fitur bersifat eksploratori.
- **Dugaan belum diuji:** DBSCAN tidak menemukan kelompok karena kepadatan relatif seragam pada 30 dimensi terstandarisasi.
- **Pemeriksa otomatis** (judul, abstrak, kata berlebihan, angka terlacak, seed) berbasis aturan sederhana dan bisa meleset; lima butir daftar periksa penulisan bersifat manual dan belum dinilai.
- **Notebook** adalah salinan dari skrip dan menyimpan output saat eksekusi; angka dinamis seperti jumlah berkas belum di-commit pada notebook bab 9 mencerminkan saat eksekusi notebook.

## 7. Rekomendasi

1. Baca teks lengkap ketujuh sumber, isi kolom keterbatasan, dan perbarui pembahasan pustaka.
2. Setelah disetujui, commit Level 7, lalu jalankan ulang skrip Bab 9 dan Bab 10 agar paket menunjuk satu commit (urutan 9, 10, 9 karena Bab 10 membaca hasil Bab 9).
3. Lihat rendering rumus dan diagram dengan `mkdocs serve`.
4. Pertimbangkan membandingkan salinan dataset dengan file asli UCI (hash).
