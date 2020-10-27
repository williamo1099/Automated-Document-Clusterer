# Document Clustering

Perangkat lunak ini dibangun sebagai bagian dari Skripsi S1 Teknik Informatika UNPAR.

## Tentang Perangkat Lunak

Perangkat lunak yang dibangun adalah sebuah perangkat lunak sederhana yang memiliki tujuan utama mengelompokan sekumpulan dokumen teks berdasarkan informasi yang terkandung di dalamnya. Perangkat lunak ini dibangun dengan menggunakan Python dan beberapa *library* Python.

## *Library* yang Digunakan

Perangkat lunak dibangun dengan bantuan dari beberapa *library* Python. Berikut adalah *library-library* yang digunakan.

* _SciPy_, yang digunakan untuk melakukan proses pengelompokan dengan algoritma *clustering*.
* _Matplotlib_, yang digunakan untuk melakukan visualisasi hasil pengelompokan.
* _NLTK_, yang digunakan untuk melakukan pre-pemrosesan linguistik.


## Fitur Perangkat Lunak

Perangkat lunak yang dibangun memiliki beberapa fitur yang mendukung tujuan utama dari perangkat lunak. Berikut adalah beberapa fitur yang disediakan.

* Perangkat lunak mampu mengelompokkan dokumen-dokumen teks secara otomatis berdasarkan informasi yang terkandung di dalam dokumen teks. Algoritma yang digunakan adalah _agglomerative hierarchical clustering_ dan keluaran yang didapatkan adalah sebuah _dendrogram_.
* Perangkat lunak mampu mengorganisir *file* dokumen teks secara otomatis berdasarkan hasil pengelompokan yang telah didapatkan.
* Perangkat lunak mampu menyimpan sebuah indeks yang digunakan untuk menyimpan dokumen-dokumen teks (yaitu _inverted index_). Dengan indeks tersebut, pengguna dapat memuat dan menggunakannya kembali.

## Proses yang Dilakukan

Beberapa proses dilakukan oleh perangkat lunak untuk mencapai tujuan utama dari perangkat lunak. Berikut adalah urutan proses yang dilakukan.

* Menerima masukan sebuah *path folder* yang berisi sekumpulan dokumen teks yang akan dikelompokkan.
* Mengambil seluruh dokumen teks yang ada dalam *folder* dan isi dari setiap dokumen teks tersebut.
* Menyimpan isi dari setiap dokumen teks sebagai sebuah *character sequence* dan dilakukan tokenisasi (mendapatkan daftar token).
* Melakukan pre-pemrosesan linguistik terhadap setiap token yang ada (terdiri dari pembuangan *stop words* dan proses *stemming*) untuk mendapatkan daftar *term*.
* Menyimpan *term-term* yang ada dalam setiap dokumen teks dalam *inverted index* (untuk dapat disimpan dan digunakan kembali).
* Membuat vektor sebagai representasi masing-masing dokumen teks dan mengukur jarak antara masing-masing vektor.
* Membangun matriks jarak antara masing-masing dokumen teks dan melakukan pengelompokan dengan algoritma *agglomerative hierarchical clustering*.
* Menampilkan hasil pengelompokan dalam sebuah *dendrogram*.
