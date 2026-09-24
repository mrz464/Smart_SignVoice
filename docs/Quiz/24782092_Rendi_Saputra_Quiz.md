# QUIZ DIGITAL AWARENESS
## Interconnecting between Digital Awareness and Application Design

**Nama:** Rendi Saputra  
**NPM:** 24782092  
**Program Studi:** Teknologi Rekayasa Internet  
**Mata Kuliah:** Internet Programming II  
**Nama Aplikasi:** BicaraUntukku (Smart_SignVoice)  
**Peran:** Developer Web Dashboard  

---

# BAGIAN 1 — IDENTITAS DAN TOPIK PROYEK APLIKASI

## 1. Nama Aplikasi

**BicaraUntukku (Smart_SignVoice)**

## 2. Deskripsi Singkat dan Tujuan Utama Aplikasi

BicaraUntukku adalah aplikasi yang dikembangkan untuk membantu komunikasi dan proses pembelajaran bagi penyandang tunarungu dan tunawicara yang menggunakan bahasa isyarat BISINDO.

Permasalahan yang ingin diselesaikan adalah hambatan komunikasi antara pengguna bahasa isyarat dengan orang yang belum memahami BISINDO. Aplikasi menggunakan video gerakan tangan sebagai input yang kemudian diproses melalui sistem AI untuk menghasilkan teks dan suara. Dalam rancangan sistem, proses tersebut melibatkan aplikasi mobile, REST API, AI Engine, database PostgreSQL, dan web dashboard.

Selain membantu proses penerjemahan, BicaraUntukku juga memiliki fitur **Dashboard Monitoring Perkembangan Siswa**. Dashboard digunakan oleh guru SLB dan pendamping untuk melihat perkembangan kemampuan kosakata siswa berdasarkan riwayat sesi penerjemahan yang tersimpan pada database. Data tersebut dapat ditampilkan dalam bentuk grafik perkembangan kosakata, daftar kata yang telah dikuasai maupun belum dikuasai, serta laporan.

Dalam proyek ini, saya berperan sebagai **Developer Web Dashboard**. Saya membangun dashboard menggunakan **React.js** yang berfungsi sebagai antarmuka bagi guru atau pendamping.

Dashboard terhubung dengan backend melalui REST API. Dengan arsitektur tersebut, dashboard tidak mengambil data langsung dari database, tetapi meminta data melalui backend sebagai sumber data terpusat.

Fitur yang saya kerjakan meliputi:

- Login guru atau pendamping
- Dashboard Overview
- Statistik jumlah siswa
- Statistik kosakata yang dikuasai
- Statistik sesi latihan
- Statistik akurasi rata-rata
- Grafik perkembangan kosakata menggunakan Recharts
- Halaman daftar siswa
- Status siswa aktif atau tidak aktif
- Navigasi antar halaman
- Logout
- Protected route untuk membatasi akses pengguna yang belum login

Dengan dashboard tersebut, guru dan pendamping dapat memperoleh gambaran perkembangan siswa tanpa harus melihat setiap proses latihan secara manual.

## 3. Target Pengguna Utama

BicaraUntukku memiliki dua kelompok pengguna.

**Pengguna utama** adalah penyandang tunarungu dan tunawicara yang menggunakan aplikasi mobile untuk melakukan penerjemahan bahasa isyarat.

**Pengguna sekunder** adalah guru SLB dan pendamping. Mereka menggunakan web dashboard untuk memantau perkembangan siswa. Pembagian ini juga sesuai dengan proposal proyek yang menetapkan penyandang tunarungu/tunawicara sebagai target utama dan guru SLB serta pendamping sebagai pengguna sekunder.

---

# BAGIAN 2 — RESUME MODUL DIGITAL AWARENESS

## 1. Modul 1 — There's a whole new world out there!

Modul ini membahas perubahan aktivitas manusia akibat perkembangan teknologi digital. Banyak pekerjaan yang sebelumnya dilakukan secara manual dapat dilakukan dengan bantuan sistem digital sehingga informasi dapat dikelola dan diakses dengan lebih mudah.

Menurut saya, inti dari modul ini bukan hanya penggunaan teknologi, tetapi bagaimana teknologi digunakan untuk menyelesaikan permasalahan nyata.

## 2. Modul 2 — You'll Need Some Basic Tools

Modul ini membahas pengetahuan dasar dalam menggunakan perangkat digital, seperti sistem operasi, pengelolaan file dan folder, serta keamanan akun dan password.

Pengetahuan tersebut penting karena penggunaan teknologi tidak hanya berkaitan dengan menjalankan aplikasi, tetapi juga bagaimana data dan akun pengguna dikelola dengan aman.

## 3. Modul 3 — This is how you get around and find what you're looking for

Modul ini membahas cara menggunakan browser dan mencari informasi secara efektif. Selain itu, terdapat pembahasan mengenai penggunaan informasi digital serta perbedaan antara copyright dan public domain.

Bagi developer, kemampuan mencari dokumentasi yang tepat juga penting. Namun informasi atau aset yang ditemukan di internet tidak otomatis bebas digunakan. Developer harus memperhatikan sumber dan lisensinya.

## 4. Modul 4 — It just keeps getting better

Modul ini membahas perkembangan teknologi, khususnya AI, serta etika dalam berinteraksi di dunia digital.

Perkembangan AI memberikan banyak peluang untuk membuat aplikasi yang lebih pintar, tetapi penggunaan AI tetap membutuhkan tanggung jawab. Developer harus mempertimbangkan kemungkinan kesalahan AI dan dampaknya terhadap pengguna.

## 5. Modul 5 — Even Though It's Digital, It is Real, With Real Consequences

Modul ini menjelaskan bahwa aktivitas digital dapat memberikan konsekuensi nyata. Data pribadi, jejak digital, penipuan, komunikasi negatif, dan pembajakan merupakan beberapa hal yang perlu diperhatikan.

Karena aplikasi menyimpan informasi pengguna, developer harus mempertimbangkan keamanan dan privasi sejak tahap perancangan aplikasi.

## 6. Modul 6 — Learn About Anything and Everything

Modul ini membahas kemampuan memecahkan masalah teknis dan mengenali keterampilan digital yang masih perlu dikembangkan.

Troubleshooting sebaiknya dilakukan secara sistematis. Ketika aplikasi mengalami masalah, developer perlu menentukan sumber masalah terlebih dahulu sebelum melakukan perbaikan.

---

# BAGIAN 3 — HUBUNGAN DAN IMPLEMENTASI PADA PROYEK

## 1. Bagaimana rancangan aplikasi dapat mempermudah tugas sehari-hari pengguna?

BicaraUntukku membantu mengurangi hambatan komunikasi yang dialami pengguna BISINDO ketika berkomunikasi dengan orang yang tidak memahami bahasa isyarat.

Pada proses yang lebih tradisional, komunikasi dapat membutuhkan bantuan orang yang memahami BISINDO. Pada sistem BicaraUntukku, gerakan tangan dapat direkam melalui aplikasi mobile dan diproses secara digital untuk menghasilkan teks dan suara. Proposal menjelaskan bahwa video dikirim ke backend melalui endpoint `POST /translate/video`, kemudian diproses oleh AI Engine dan hasilnya dikembalikan kepada aplikasi mobile.

Dari sisi saya sebagai developer dashboard, proses manual yang ingin dikurangi adalah **pemantauan perkembangan siswa secara manual**.

Guru tidak harus mencatat perkembangan kosakata siswa satu per satu. Data sesi yang sudah tersimpan dapat ditampilkan melalui dashboard dalam bentuk statistik dan grafik.

Misalnya guru dapat melihat:

- jumlah sesi latihan
- jumlah kosakata yang telah dikuasai
- perkembangan kosakata setiap minggu
- status siswa
- data hasil latihan

Dengan demikian, aktivitas monitoring yang sebelumnya dapat dilakukan secara manual menjadi lebih terstruktur melalui sistem digital.

## 2. Jika aplikasi memiliki fitur penyimpanan file atau pendaftaran akun, bagaimana merancang penyimpanan dan password?

Pada dashboard BicaraUntukku terdapat halaman login untuk guru atau pendamping. Oleh karena itu, keamanan akun menjadi salah satu hal yang penting.

Saya akan membuat proses login melalui backend, bukan melakukan validasi password langsung pada frontend. Dashboard mengirimkan informasi login ke REST API dan backend melakukan proses autentikasi.

Setelah login berhasil, akses dashboard dibatasi menggunakan **protected route** sehingga pengguna yang belum terautentikasi tidak dapat langsung membuka halaman monitoring.

Dalam sistem yang kami rancang, backend menggunakan JWT untuk authentication. Dashboard menggunakan token tersebut untuk melakukan request ke endpoint yang membutuhkan autentikasi.

Untuk password, pengguna sebaiknya diarahkan membuat password yang sulit ditebak, misalnya menggunakan kombinasi huruf, angka, dan karakter khusus.

Password juga tidak boleh ditampilkan kembali pada dashboard dalam bentuk teks biasa.

Untuk struktur data, saya akan menghindari penyimpanan informasi yang tidak diperlukan oleh dashboard. Data yang ditampilkan cukup berupa informasi yang memang diperlukan untuk monitoring siswa.

## 3. Bagaimana mendesain fitur pencarian dan bagaimana dengan aset eksternal?

Jika jumlah siswa dan riwayat latihan semakin banyak, fitur pencarian akan membantu guru menemukan data dengan lebih cepat.

Contohnya, pada halaman **Students**, guru dapat mencari siswa berdasarkan nama. Placeholder pada search bar dapat dibuat sederhana:

> **Cari nama siswa...**

Hasil pencarian kemudian dapat ditampilkan pada tabel sehingga guru tidak perlu mencari secara manual dari seluruh daftar.

Untuk aset dan library, dashboard menggunakan beberapa teknologi beserta lisensinya:

- **React.js** — MIT License, untuk membangun antarmuka dashboard
- **Material UI (MUI)** — MIT License, untuk komponen antarmuka
- **Recharts** — MIT License, untuk grafik perkembangan kosakata
- **React Router DOM** — MIT License, untuk navigasi antar halaman
- **Axios** — MIT License, untuk komunikasi dengan REST API

Walaupun semua library tersebut bersifat open-source dengan lisensi MIT, penggunaannya tetap harus mengikuti ketentuan lisensi masing-masing, termasuk mencantumkan atribusi jika diperlukan.

## 4. Bagaimana memastikan AI bekerja secara etis dan bertanggung jawab?

BicaraUntukku menggunakan AI untuk membantu menerjemahkan bahasa isyarat. Model LSTM mengklasifikasikan sequence keypoint menjadi label kata BISINDO, kemudian Gemini digunakan untuk menyusun kata-kata tersebut menjadi kalimat yang lebih natural.

Menurut saya, hasil AI tidak boleh dianggap selalu benar.

Misalnya sistem menghasilkan terjemahan yang kurang sesuai, guru atau pendamping harus dapat melakukan koreksi. Hal ini sesuai dengan fungsi dashboard yang juga menyediakan fitur **koreksi hasil terjemahan** dalam rancangan sistem. Diagram arsitektur proposal juga menunjukkan adanya fungsi koreksi pada web dashboard.

Karena itu, AI sebaiknya digunakan sebagai alat bantu dan hasilnya tetap dapat diperiksa manusia.

Selain itu, dashboard tidak seharusnya memberikan informasi mengenai seorang siswa di luar kebutuhan monitoring. Data yang ditampilkan harus sesuai dengan hak akses pengguna.

## 5. Data pribadi apa yang dikumpulkan dan bagaimana melindunginya?

Data yang berkaitan dengan pengguna dalam sistem antara lain:

- nama siswa
- data akun guru atau pendamping
- riwayat sesi latihan
- kosakata yang telah dikuasai
- hasil penerjemahan
- status siswa

Proposal menyebut PostgreSQL digunakan untuk menyimpan **data pengguna, sesi, dan kosakata**.

Karena data tersebut berkaitan dengan pengguna, dashboard tidak boleh memberikan akses kepada sembarang orang.

Beberapa langkah perlindungan yang dapat diterapkan adalah:

1. Menggunakan login dan authentication
2. Menggunakan protected route pada dashboard
3. Membatasi akses berdasarkan role pengguna
4. Menggunakan HTTPS ketika berkomunikasi dengan backend
5. Tidak menampilkan password
6. Tidak menyimpan informasi pribadi yang tidak diperlukan
7. Membatasi akses terhadap data siswa hanya kepada pengguna yang memiliki hak

Untuk mengurangi risiko penipuan siber, aplikasi juga sebaiknya memberikan informasi bahwa pengguna tidak boleh membagikan password atau token autentikasi kepada orang lain.

## 6. Bagaimana aplikasi mengomunikasikan masalah teknis kepada pengguna?

Dashboard harus memberikan pesan error yang mudah dipahami oleh guru atau pendamping.

Sebagai developer dashboard, saya tidak akan menampilkan error teknis mentah seperti `AxiosError: Network Error` kepada pengguna.

Sebagai gantinya, dashboard dapat menampilkan pesan yang lebih ramah:

Jika koneksi ke server gagal:
> **Koneksi ke server gagal.**  
> Periksa koneksi internet Anda kemudian coba kembali.

Jika REST API mengembalikan error authentication:
> **Sesi login telah berakhir.**  
> Silakan login kembali untuk melanjutkan.

Jika data siswa gagal dimuat:
> **Data siswa belum dapat ditampilkan.**  
> Silakan coba muat ulang halaman beberapa saat lagi.

Jika server sedang mengalami masalah:
> **Layanan sedang mengalami gangguan sementara.**  
> Silakan coba kembali beberapa saat lagi.

Pesan tersebut memberikan dua informasi penting: **apa yang terjadi dan apa yang dapat dilakukan pengguna**.

Hal ini juga sesuai dengan konsep troubleshooting dalam Digital Awareness, karena pengguna diberikan langkah sederhana sebelum meminta bantuan developer.

---

# Kesimpulan

Sebagai **Developer Dashboard**, pemahaman Digital Awareness tidak hanya diterapkan pada tampilan aplikasi, tetapi juga pada cara dashboard mengelola akses, data, informasi, dan interaksi dengan pengguna.

Dashboard BicaraUntukku dirancang agar guru dan pendamping dapat memantau perkembangan siswa dengan lebih terstruktur. Data hasil sesi yang berasal dari sistem utama ditampilkan melalui REST API sehingga dashboard tidak menjadi sumber data terpisah. Arsitektur proposal memang menempatkan REST API sebagai penghubung antara mobile app, AI Engine, database, dan web dashboard.

Dengan demikian, peran saya sebagai developer bukan hanya membuat halaman React yang dapat menampilkan data, tetapi juga memastikan dashboard mudah digunakan, memiliki akses yang sesuai, memberikan informasi yang jelas, dan memperhatikan keamanan serta privasi data pengguna.
