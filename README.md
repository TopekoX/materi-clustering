# Materi Clustering

Dokumentasi belajar **Clustering pada Machine Learning** berbahasa Indonesia, dari konsep dasar sampai penerapan riset. Dibangun dengan [MkDocs](https://www.mkdocs.org/) dan tema [Material](https://squidfunnel.github.io/mkdocs-material/).

Pendekatan belajar: konsep → fondasi matematika → implementasi Python → latihan → eksperimen → evaluasi model → aplikasi riset.

## Kurikulum

| Level | Topik | Status |
|---|---|---|
| 1 | Machine Learning Fundamentals | Direncanakan |
| 2 | Data Exploration and Preprocessing | Dalam penyusunan |
| 3 | Fundamental Clustering | Direncanakan |
| 4 | Clustering Algorithms | Direncanakan |
| 5 | Clustering Evaluation | Direncanakan |
| 6 | Experimentation and Interpretation | Direncanakan |
| 7 | Research Project | Direncanakan |

Lingkup awal adalah Level 2 (12 bab). Detailnya ada di [`PRD.md`](PRD.md) dan [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md).

## Menjalankan situs secara lokal

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Buka <http://127.0.0.1:8000>. Untuk memverifikasi build dan tautan:

```bash
mkdocs build --strict
```

Persamaan matematika dirender oleh MathJax dari CDN (`cdn.jsdelivr.net`), sehingga memerlukan koneksi internet.

## Deploy ke GitHub Pages

1. Pastikan repositori GitHub sudah dibuat dan `origin` mengarah ke sana:

    ```bash
    git remote -v
    git remote set-url origin git@github.com:TopekoX/materi-clustering.git
    ```

2. Pastikan `site_url` dan `repo_url` di `mkdocs.yml` sesuai:
   `https://topekox.github.io/materi-clustering/` dan `https://github.com/topekox/materi-clustering`.
3. Push kode ke branch `main`, lalu aktifkan lingkungan virtual dan jalankan:

    ```bash
    mkdocs gh-deploy --strict
    ```

    Perintah ini membangun situs dan mendorong hasilnya ke branch `gh-pages`. Build gagal bila ada tautan atau anchor yang rusak.
4. Di GitHub buka **Settings → Pages → Build and deployment → Deploy from a branch**, pilih branch `gh-pages` dan folder `/ (root)`, lalu simpan.
5. Situs tersedia di `site_url` setelah beberapa menit.

> **Catatan:** `mkdocs gh-deploy` menimpa isi branch `gh-pages` setiap kali dijalankan. Jangan mengedit branch itu secara manual. Jalankan hanya setelah `mkdocs build --strict` lulus.

## Struktur proyek

```
mkdocs.yml                 identitas situs, tema, navigasi, ekstensi
requirements.txt           dependensi situs dokumentasi
docs/                      konten yang dipublikasikan
  index.md
  curriculum/              kurikulum dan bab per level
  stylesheets/extra.css    penyesuaian CSS kecil
  javascripts/             konfigurasi MathJax dan Mermaid
  assets/vendor/mermaid/   Mermaid yang di-vendor
```

Struktur berikut direncanakan untuk Level 2: `docs/data-exploration-and-preprocessing/`, `data/`, `notebooks/level-2/`, dan `requirements-notebooks.txt`.

## Menulis konten

Aturan penulisan, standar bab (14 bagian), dan konvensi Markdown ada di [`CLAUDE.md`](CLAUDE.md). Singkatnya:

- Materi dalam bahasa Indonesia; istilah teknis internasional tetap dalam bahasa Inggris.
- Satu `# Judul` per halaman; tambahkan halaman baru ke `nav:` di `mkdocs.yml`.
- Rumus: `\( ... \)` inline dan `$$ ... $$` display.
- Diagram: blok kode `mermaid`.

## Dokumen proyek

| File | Isi |
|---|---|
| [`PROJECT_AUDIT.md`](PROJECT_AUDIT.md) | Audit repositori awal |
| [`PRD.md`](PRD.md) | Kebutuhan produk |
| [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) | Fase dan rencana pengerjaan |
| [`CLAUDE.md`](CLAUDE.md) | Aturan kerja dan standar konten |
| `PRD_TEMPLATE.md`, `TECHNICAL_DESIGN.md`, `VALIDATION_REPORT.md`, `PROMPT_MKDOCS_TEMPLATE.md` | Dokumen dari template MkDocs asal |

## Lisensi

[MIT](LICENSE). Pustaka Mermaid di `docs/assets/vendor/mermaid/` juga berlisensi MIT dan menyertakan `LICENSE` sendiri.
