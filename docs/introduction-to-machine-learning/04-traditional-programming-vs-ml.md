# Pemrograman Tradisional vs Machine Learning

## Pemrograman tradisional

Pada **pemrograman tradisional**, manusia menulis **aturan** secara eksplisit. Komputer menerima **data** dan menerapkan aturan itu untuk menghasilkan **jawaban**.

Ini disebut juga **rule-based programming** (pemrograman berbasis aturan).

### Contoh: penyaring spam berbasis aturan

```python title="rule_spam.py"
def apakah_spam(pesan):
    kata_terlarang = ["hadiah", "gratis", "menang"]
    pesan = pesan.lower()
    for kata in kata_terlarang:
        if kata in pesan:
            return True
    return False

print(apakah_spam("Selamat! Anda menang hadiah"))
print(apakah_spam("Rapat dimulai jam 10"))
```

Output yang diharapkan:

```text
True
False
```

Program ini berjalan baik, tetapi punya kelemahan. Pelaku spam cukup menulis "h4diah" dan lolos. Manusia harus terus menambah aturan baru. Semakin banyak aturan, semakin sulit dirawat.

## Pendekatan Machine Learning

Pada **Machine Learning**, kita membalik prosesnya. Kita memberi komputer **data** *dan* **jawaban yang benar** (contoh-contoh), lalu komputer menemukan **aturannya** sendiri. Aturan itulah yang disebut **model**.

!!! note "Satu kalimat pembeda"
    Pemrograman tradisional: *data + aturan → jawaban*.  
    Machine Learning: *data + jawaban → aturan (model)*.

## Diagram alur

=== "Pemrograman tradisional"

    ```mermaid
    flowchart LR
        A[Data] --> P[Program dengan aturan buatan manusia]
        R[Aturan] --> P
        P --> J[Jawaban]
    ```

=== "Machine Learning"

    ```mermaid
    flowchart LR
        A[Data] --> L[Algoritma belajar]
        J[Jawaban contoh] --> L
        L --> M[Model = aturan hasil belajar]
    ```

## Tabel perbandingan

| Aspek | Pemrograman tradisional | Machine Learning |
|---|---|---|
| Input | Data dan aturan | Data dan jawaban contoh (pada kasus tertentu) |
| Proses | Menjalankan aturan | Mencari aturan dari data |
| Output | Jawaban | Model (aturan) yang kemudian menghasilkan jawaban |
| Siapa menulis aturan | Manusia | Algoritma, dari data |
| Cocok untuk | Aturan jelas dan stabil | Pola rumit atau sering berubah |
| Contoh | Menghitung gaji, validasi formulir | Rekomendasi film, pengenalan wajah |

!!! info "Catatan untuk clustering"
    Pada *clustering*, kita tidak memberi jawaban contoh. Algoritma mencari kelompok sendiri. Ini dibahas di [Peran ML dalam Clustering](10-role-of-ml-in-clustering.md).

## Contoh dunia nyata

- **Pajak dan gaji:** aturan pasti, cocok untuk pemrograman tradisional.
- **Mengenali tulisan tangan:** setiap orang menulis berbeda, sehingga aturannya sulit ditulis. Cocok untuk ML.
- **Rekomendasi produk:** selera pelanggan berubah, sehingga pola perlu dipelajari dari data terbaru.

## Cara menjalankan kode di atas

Simpan sebagai `rule_spam.py`, lalu jalankan:

```bash
python rule_spam.py
```

Lanjut ke [Bagaimana ML Bekerja](05-how-machine-learning-works.md).
