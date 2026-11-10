# CLAUDE.md — Materi Clustering

Situs dokumentasi berbahasa Indonesia tentang Clustering Machine Learning, di atas template MkDocs + Material yang sudah ada. Lingkup saat ini: **Level 2 — Data Exploration and Preprocessing** (12 bab), **Level 3 — Fundamental Clustering** (7 bab), **Level 4 — Clustering Algorithms** (7 bab, disetujui 2026-11-10), **Level 5 — Clustering Evaluation** (8 bab, disetujui 2026-11-10), dan **Level 6 — Experimentation and Interpretation** (10 bab, dikerjakan bertahap, disetujui 2026-11-10; proyek riset penuh tetap milik Level 7). Lihat `PRD.md`, `IMPLEMENTATION_PLAN.md`, `PROJECT_AUDIT.md`.

## Aturan keras

- Jangan membangun ulang situs; jangan mengganti tema; jangan menimpa nav, CSS, JS, atau komponen yang ada. Perubahan `mkdocs.yml` hanya `nav:` dan identitas yang sudah disetujui.
- Jangan menghapus/menimpa file tanpa justifikasi tertulis. `PRD_TEMPLATE.md`, `PROMPT_MKDOCS_TEMPLATE.md`, `TECHNICAL_DESIGN.md`, `VALIDATION_REPORT.md`, `README.md` dipertahankan.
- Jangan commit, push, atau `gh-deploy` tanpa instruksi eksplisit. `origin` masih `mkdocs-template`.
- Kerjakan satu bab per iterasi. Validasi sebelum lanjut. Laporkan file yang berubah dan hasil validasi.
- Jangan mengarang output, kutipan, atau data. Output yang diharapkan harus berasal dari eksekusi nyata.

## Bahasa

Isi dalam bahasa Indonesia. Istilah teknis internasional tetap Inggris (clustering, outlier, feature scaling, one-hot encoding, dll.), dicetak miring atau dijelaskan saat pertama muncul. Nama file dan kode dalam bahasa Inggris.

## Standar bab (14 bagian, urut)

Learning Objectives, Introduction, Fundamental Concepts, Detailed Explanation, Mathematical Foundation (jika relevan), Python Implementation, Code Explanation, How to Run, Expected Output, Practical Examples, Hands-on Exercises, Troubleshooting, Summary, References.

## Konvensi MkDocs yang ada

- Satu `# Judul` per halaman; folder dengan `index.md` menjadi landing section.
- Objective: task list `- [x]`. Peringatan/tips: `!!! warning|tip|note`; jawaban latihan: `??? question`.
- Kode: fence dengan bahasa, `title="..."`; potongan dari file via `--8<-- "path"` (base `examples/`, `check_paths: true`). Beberapa bahasa/varian: `=== "Tab"`.
- Math: `\( … \)` inline, `$$ … $$` display (arithmatex). `$` literal ditulis `\$`.
- Diagram: fence `mermaid`. Warna CSS hanya lewat `var(--md-*)`.
- Validasi link/anchor berstatus `warn`, sehingga `mkdocs build --strict` gagal bila ada yang rusak.

## Struktur target

Aturan: setiap level berada langsung di bawah `docs/`, dalam folder bernama sesuai topik level (slug Inggris, huruf kecil). Jangan menaruh level di dalam `docs/curriculum/`; folder itu hanya berisi `index.md` (roadmap).

```
docs/<topik-level>/index.md, NN-slug.md     contoh: docs/data-exploration-and-preprocessing/ (Level 2), docs/fundamental-clustering/ (Level 3), docs/clustering-algorithms/ (Level 4), docs/clustering-evaluation/ (Level 5), docs/experimentation-and-interpretation/ (Level 6)
docs/assets/level-2/          gambar
data/mall_customers.csv
notebooks/level-2/NN-slug.ipynb
requirements-notebooks.txt
```

## Perintah

```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
mkdocs build --strict
jupyter nbconvert --to notebook --execute notebooks/level-2/NN-slug.ipynb --output-dir <scratch>
```

## Kualitas

Akurasi teori, relevansi praktis, penjelasan ramah pemula. Seed acak tetap (`random_state=42`). Setiap bab: kode dijalankan, output dicocokkan, build strict lulus, rumus dirender (butuh jaringan untuk MathJax CDN).
