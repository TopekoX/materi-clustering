# Pendahuluan

## Apa itu Machine Learning?

Bayangkan kamu mengajari adik membedakan buah apel dan jeruk. Kamu tidak menyodorkan daftar aturan panjang. Kamu cukup menunjukkan banyak contoh: "ini apel", "ini jeruk". Lama-lama adik mulai bisa menebak sendiri, bahkan untuk buah yang belum pernah ia lihat.

**Machine Learning (ML)** bekerja dengan cara serupa. Komputer diberi banyak **contoh (data)**, lalu ia menemukan **pola** dari contoh itu. Pola tersebut kemudian dipakai untuk menebak atau memutuskan hal baru.

!!! note "Intinya"
    Pada Machine Learning, komputer **belajar dari data**, bukan hanya mengikuti aturan yang ditulis manusia satu per satu.

## Mengapa Machine Learning penting?

Ada beberapa alasan utama:

1. **Data makin banyak.** Ponsel, toko online, sensor, dan media sosial menghasilkan data terus-menerus. Manusia tidak sanggup menelitinya satu per satu.
2. **Aturan terlalu rumit untuk ditulis manual.** Coba tuliskan aturan agar komputer mengenali wajah seseorang. Hampir mustahil, tetapi komputer bisa mempelajarinya dari ribuan foto.
3. **Situasi berubah.** Kebiasaan pelanggan atau pola penipuan terus berubah. Model ML bisa dilatih ulang dengan data terbaru.
4. **Keputusan berbasis bukti.** Pola dalam data membantu kita mengambil keputusan yang lebih terarah.

## Di mana kita menemui Machine Learning?

Kamu mungkin sudah memakainya hari ini tanpa sadar:

- Rekomendasi video atau lagu.
- Filter *spam* pada email.
- Terjemahan otomatis.
- Pembuka kunci ponsel dengan wajah atau sidik jari.
- Prakiraan waktu tempuh di aplikasi peta.

Contoh yang lebih lengkap ada di [Penerapan di Dunia Nyata](07-real-world-applications.md).

## Hubungan data dan algoritma belajar

Dua hal ini selalu berjalan berdampingan:

- **Data** adalah bahan belajar. Tanpa data, tidak ada yang bisa dipelajari.
- **Algoritma belajar** adalah *cara* belajar: langkah-langkah yang dipakai komputer untuk menemukan pola dari data.

Data yang sama bisa menghasilkan hasil berbeda jika algoritmanya berbeda. Sebaliknya, algoritma yang sama akan menghasilkan hasil berbeda jika datanya berbeda.

!!! warning "Kualitas data menentukan hasil"
    Ada pepatah populer di dunia data: *garbage in, garbage out*. Jika data yang diberikan berantakan atau salah, hasil belajar juga akan buruk. Karena itu ada satu level khusus nanti (Data Exploration and Preprocessing) yang membahas cara merapikan data.

Lanjut ke [Definisi Machine Learning](02-definition-of-machine-learning.md).
