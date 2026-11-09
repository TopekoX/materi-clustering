# QA Report — Level 3: Fundamental Clustering

Tanggal: 2026-11-09 · Lingkungan: Python 3.14.10, NumPy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0, matplotlib 3.11.1

## Bab selesai

7 dari 7 bab (`docs/fundamental-clustering/01`–`07`) plus `index.md`. Semua mengikuti 14 bagian standar `CLAUDE.md`.

## Validasi

| Pemeriksaan | Hasil |
|---|---|
| `mkdocs build --strict` | Lulus (tautan, anchor, gambar, snippet `check_paths`) |
| Skrip `examples/level-3/01`–`07` | Semua dijalankan; output disimpan di `examples/level-3/outputs/NN.txt` dan disertakan ke bab lewat snippet |
| Notebook `notebooks/level-3/01`–`07` | Semua dieksekusi dengan `jupyter nbconvert --execute` tanpa error. Hasil eksekusi hanya di folder sementara; notebook di repo tidak berisi output (sama seperti Level 2) |
| Penanda `--8<--` tersisa di HTML | Tidak ada |
| Mermaid | 1 diagram per bab ada di HTML hasil build |
| Rumus (arithmatex) | Ada di HTML hasil build. **Render visual MathJax belum diperiksa di browser** |
| Gambar | 16 gambar di `docs/assets/level-3/`. Yang dilihat langsung: `01-hasil-clustering`, `02-terpisah-vs-tumpang-tindih`, `02-bentuk-dan-ukuran`, `03-*` (3), `04-matriks-jarak` (versi pertama, warna teks sudah diperbaiki setelahnya), `05-bentuk-jarak`, `06-ruang-1d-2d-3d`, `06-efek-dimensi`. Belum dilihat: `01-data-mentah`, `02-keanggotaan-batas`, `05-cosine-arah`, `06-skala-ruang-fitur`, `07-*` |
| Angka di bab | Semua angka output dan jawaban latihan berasal dari eksekusi nyata atau hitungan manual yang dicek ulang dengan kode |
| Level 1 dan Level 2 | Isi tidak diubah di tugas ini. Perubahan di Level 2 hanya perbaikan tautan relatif akibat pemindahan folder (turn sebelumnya) |

## File dibuat

- `docs/fundamental-clustering/index.md`, `01`–`07-*.md`
- `examples/level-3/01`–`07_*.py`, `_savefig.py`, `outputs/01`–`07.txt`
- `docs/assets/level-3/*.png` (16 gambar)
- `notebooks/level-3/01`–`07-*.ipynb`
- `LEVEL3_QA_REPORT.md`

## File diubah

- `mkdocs.yml` (hanya `nav:`), `docs/curriculum/index.md`, `PRD.md`, `CLAUDE.md`, `IMPLEMENTATION_PLAN.md`

## Keterbatasan dan isu tersisa

- Notebook Level 2 tidak dieksekusi ulang di tugas ini.
- Render MathJax dan Mermaid belum dilihat di browser (perlu jaringan untuk CDN).
- Gambar memakai latar putih; di tema gelap tampil sebagai kotak putih (sama dengan gambar Level 2).
- Jawaban latihan yang bergantung pada eksekusi (mis. Bab 2 no. 1 dan 4, Bab 5 no. 5, Bab 7 no. 2) ditulis sebagai petunjuk, bukan angka, karena tidak dijalankan.
- Bab 7 memakai K-Means dan silhouette sebagai alat bantu sebelum Level 4 dan 5; keduanya ditandai sebagai pratinjau.
- Tidak ada commit, push, atau deploy.
