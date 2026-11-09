# Association Rule Learning

## Definisi sederhana

**Association Rule Learning** adalah teknik untuk menemukan **aturan "jika ... maka ..."** tentang item-item yang **sering muncul bersama** dalam data.

Contoh aturan: "Jika pelanggan membeli roti, maka ia cenderung juga membeli mentega."

!!! note "Posisinya dalam taksonomi"
    Association Rule Learning umumnya dibahas sebagai pendekatan **unsupervised** untuk *pattern mining* (penggalian pola), karena tidak memakai label. Namun pengelompokan jenis-jenis ML berbeda antar buku. Beberapa buku membahasnya di bidang *data mining*, bukan Machine Learning secara khusus.

## Item dan transaksi

- **Item** adalah satu barang atau kejadian, misalnya "roti" atau "susu".
- **Transaksi** adalah satu kumpulan item yang terjadi bersama, misalnya satu struk belanja.
- **Itemset** adalah sekumpulan item, misalnya {roti, susu}.

Contoh data lima transaksi:

| Transaksi | Item yang dibeli |
|---|---|
| T1 | roti, susu |
| T2 | roti, mentega |
| T3 | roti, susu, mentega |
| T4 | susu, telur |
| T5 | roti, susu, telur |

## Market Basket Analysis

**Market Basket Analysis** (analisis keranjang belanja) adalah penerapan paling terkenal dari Association Rule Learning. Tujuannya mengetahui barang apa yang sering dibeli bersamaan, sehingga toko bisa:

- menata letak barang yang saling berkaitan berdekatan,
- membuat paket promosi,
- memberi rekomendasi "sering dibeli bersama".

## Tiga ukuran utama

Sebuah aturan ditulis \(A \Rightarrow B\), dibaca "jika \(A\), maka \(B\)". \(A\) disebut *antecedent* (sebab) dan \(B\) disebut *consequent* (akibat).

### Support

**Tujuan:** mengukur seberapa **sering** sebuah itemset muncul di seluruh transaksi.

\[
\text{support}(A) = \frac{\text{jumlah transaksi yang mengandung } A}{\text{jumlah seluruh transaksi}}
\]

**Contoh:** {roti} ada di T1, T2, T3, T5, yaitu 4 dari 5 transaksi.

\[
\text{support}(\{\text{roti}\}) = \frac{4}{5} = 0{,}8
\]

{roti, susu} ada di T1, T3, T5, yaitu 3 dari 5 transaksi, sehingga \(\text{support}(\{\text{roti}, \text{susu}\}) = 0{,}6\).

**Artinya:** roti dan susu dibeli bersama di 60% transaksi.

### Confidence

**Tujuan:** mengukur seberapa **sering aturan terbukti benar**. Dari semua transaksi yang berisi \(A\), berapa bagian yang juga berisi \(B\)?

\[
\text{confidence}(A \Rightarrow B) = \frac{\text{support}(A \cup B)}{\text{support}(A)}
\]

Simbol \(A \cup B\) berarti "\(A\) dan \(B\) muncul bersama dalam satu transaksi".

**Contoh:** aturan {roti} ⇒ {susu}:

\[
\text{confidence} = \frac{0{,}6}{0{,}8} = 0{,}75
\]

**Artinya:** dari pembeli roti, 75% juga membeli susu.

### Lift

**Tujuan:** mengukur apakah hubungan \(A\) dan \(B\) **lebih kuat dari kebetulan**.

\[
\text{lift}(A \Rightarrow B) = \frac{\text{confidence}(A \Rightarrow B)}{\text{support}(B)}
\]

Cara membaca nilai lift:

| Nilai lift | Arti |
|---|---|
| Lebih dari 1 | Membeli \(A\) **meningkatkan** peluang membeli \(B\) |
| Sama dengan 1 | Tidak ada hubungan. \(A\) dan \(B\) saling bebas |
| Kurang dari 1 | Membeli \(A\) **menurunkan** peluang membeli \(B\) |

**Contoh 1:** {roti} ⇒ {susu}. Susu ada di T1, T3, T4, T5, sehingga \(\text{support}(\{\text{susu}\}) = 0{,}8\).

\[
\text{lift} = \frac{0{,}75}{0{,}8} \approx 0{,}94
\]

Walaupun confidence-nya 75%, lift-nya **di bawah 1**. Ini karena susu memang dibeli di 80% transaksi, siapa pun pembelinya. Membeli roti tidak membuat orang lebih mungkin membeli susu.

**Contoh 2:** {mentega} ⇒ {roti}. Mentega ada di T2 dan T3, sehingga \(\text{support}(\{\text{mentega}\}) = 0{,}4\). {mentega, roti} juga ada di T2 dan T3, sehingga support-nya 0,4.

\[
\text{confidence} = \frac{0{,}4}{0{,}4} = 1{,}0 \qquad \text{lift} = \frac{1{,}0}{0{,}8} = 1{,}25
\]

Setiap pembeli mentega juga membeli roti, dan lift 1,25 menunjukkan hubungan yang **lebih kuat dari kebetulan**.

!!! tip "Pelajaran penting"
    Confidence yang tinggi saja tidak cukup. Selalu periksa lift untuk memastikan hubungan itu bukan sekadar karena item \(B\) memang sangat populer.

## Penerapan sederhana

- Rekomendasi produk di toko online.
- Penataan rak supermarket.
- Analisis menu restoran: hidangan apa yang sering dipesan bersama.
- Analisis rekam medis: gejala atau kondisi apa yang sering muncul bersama.

## Algoritma yang terkenal

Algoritma **Apriori** adalah algoritma klasik untuk mencari aturan asosiasi. Kamu tidak perlu mempelajarinya sekarang.

## Inti sub-bab ini

Association Rule Learning mencari aturan "jika A maka B" dari data transaksi. Tiga ukurannya: **support** (seberapa sering), **confidence** (seberapa sering aturan benar), dan **lift** (apakah lebih kuat dari kebetulan).

Lanjut ke [Semi-Supervised Learning](10-semi-supervised-learning.md).
