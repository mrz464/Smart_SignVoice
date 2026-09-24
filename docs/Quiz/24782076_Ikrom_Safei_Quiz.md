# QUIZ DIGITAL AWARENESS

**Nama:** Ikrom Safei
**NPM:** 24782076
**Program Studi:** Teknologi Rekayasa Internet
**Mata Kuliah:** Internet Programming II
**Nama Aplikasi:** BicaraUntukku (Smart_SignVoice)
**Peran dalam Tim:** Developer Backend


# BAGIAN 1 — IDENTITY AND APPLICATION TOPIC

## 1. Nama Aplikasi

**BicaraUntukku (Smart_SignVoice)**

## 2. Deskripsi Singkat dan Tujuan Aplikasi

BicaraUntukku adalah aplikasi yang dibuat untuk membantu proses komunikasi menggunakan bahasa isyarat BISINDO. Pengguna dapat memberikan input berupa video gerakan tangan, kemudian sistem memproses video tersebut menggunakan AI sampai menghasilkan teks yang lebih mudah dipahami.

Selain menghasilkan teks, sistem juga dirancang agar hasil terjemahan dapat diubah menjadi suara. Di dalam project ini saya berperan sebagai **Developer Backend**, jadi saya lebih fokus pada bagian server dan REST API yang menjadi penghubung antara aplikasi mobile, AI Engine, dan database.

Backend bertugas menerima request dari client, mengatur proses data, menghubungkan request dengan proses AI, kemudian mengembalikan hasilnya lagi ke client dalam bentuk response API.

## 3. Target Pengguna

Target pengguna dari aplikasi ini yaitu:

* Pengguna bahasa isyarat BISINDO.
* Masyarakat umum yang ingin berkomunikasi dengan pengguna bahasa isyarat.
* Guru atau pendamping yang berhubungan dengan pengguna bahasa isyarat.
* Pihak lain yang membutuhkan bantuan dalam memahami komunikasi menggunakan bahasa isyarat.


# BAGIAN 2 — RESUME 6 MODULE DIGITAL AWARENESS

## Module 1 — There's a Whole New World Out There!

Pada module ini saya memahami bahwa teknologi sekarang sudah banyak membantu kegiatan sehari-hari. Hal yang sebelumnya dilakukan secara manual mulai berubah menjadi digital sehingga pekerjaan bisa dilakukan dengan lebih mudah dan cepat.

Kalau dikaitkan dengan project BicaraUntukku, proses memahami bahasa isyarat yang biasanya membutuhkan bantuan orang lain coba dibantu dengan teknologi AI. Video gerakan tangan dapat diproses oleh sistem dan hasilnya diteruskan menjadi teks atau suara.

## Module 2 — You'll Need Some Basic Tools

Module ini membahas dasar-dasar penggunaan perangkat digital, mulai dari perangkat yang digunakan, sistem operasi, file dan folder, sampai keamanan akun dan password.

Menurut saya bagian ini cukup penting dalam project karena setiap anggota tim menggunakan perangkat dan software yang berbeda. Dalam pengembangan backend misalnya, saya perlu memahami Python, virtual environment, Git, struktur folder, dan cara menjalankan server.

Selain itu, keamanan password dan akun juga perlu diperhatikan supaya akses ke sistem tidak mudah disalahgunakan.

## Module 3 — This is How You Get Around and Find What You're Looking For

Module ini mengajarkan cara menggunakan internet dan browser untuk mencari informasi yang dibutuhkan. Tidak semua informasi yang ditemukan di internet bisa langsung dipercaya, jadi kita perlu melihat sumber dan menggunakan kata kunci yang sesuai.

Dalam pengerjaan backend, hal ini cukup sering digunakan. Ketika menemukan error pada FastAPI, library Python, database, atau REST API, saya perlu mencari dokumentasi dan referensi yang sesuai supaya solusi yang digunakan tidak asal mengambil dari internet.

## Module 4 — It Just Keeps Getting Better

Module ini membahas perkembangan teknologi, termasuk perkembangan AI yang semakin banyak digunakan dalam kehidupan sehari-hari. Teknologi yang terus berkembang bisa memberikan banyak manfaat, tetapi penggunaannya juga harus tetap memperhatikan tanggung jawab dan etika digital.

Dalam BicaraUntukku, AI digunakan untuk membantu menerjemahkan bahasa isyarat. Dari sisi backend, saya perlu memastikan komunikasi antara aplikasi dan layanan AI berjalan dengan benar serta data yang dikirim tidak digunakan sembarangan.

## Module 5 — Even Though It's Digital, It Is Real, With Real Consequences

Module ini mengingatkan bahwa aktivitas di dunia digital tetap memiliki dampak nyata. Data pribadi yang tersebar atau komunikasi yang tidak dilakukan dengan baik bisa menimbulkan masalah.

Hal ini berhubungan dengan backend karena server bisa menerima data pengguna dan file video. Oleh karena itu, data tersebut harus diperlakukan dengan hati-hati. Informasi yang tidak diperlukan sebaiknya tidak dikumpulkan dan akses ke data juga perlu dibatasi.

## Module 6 — Learn About Anything and Everything

Module ini menjelaskan pentingnya kemampuan untuk belajar dan menyelesaikan masalah menggunakan teknologi. Saat menggunakan perangkat atau software, terkadang akan muncul masalah yang harus dicari penyebab dan solusinya.

Sebagai developer backend, saya cukup sering berhadapan dengan error saat menjalankan server, install library, membuat endpoint, atau menghubungkan API. Jadi kemampuan mencari informasi dan melakukan troubleshooting sangat dibutuhkan.


# BAGIAN 3 — DIGITAL AWARENESS & PROJECT

## 1. Bagaimana desain aplikasi dapat mempermudah pekerjaan sehari-hari? Proses analog/tradisional apa yang menjadi digital?

BicaraUntukku dibuat untuk membantu proses komunikasi antara pengguna bahasa isyarat dengan orang yang belum memahami BISINDO.

Sebelumnya, ketika seseorang menggunakan bahasa isyarat, orang yang diajak berkomunikasi mungkin membutuhkan orang lain yang bisa menerjemahkan. Dengan aplikasi ini, proses tersebut coba dibantu menggunakan teknologi.

Pengguna dapat memberikan video gerakan bahasa isyarat, kemudian video tersebut dikirim melalui aplikasi ke backend. Backend menerima data tersebut dan meneruskan prosesnya ke bagian AI. Setelah mendapatkan hasil, backend mengirimkan kembali hasil terjemahan ke aplikasi.

Jadi proses yang sebelumnya dilakukan secara manual, seperti memahami gerakan dan menyampaikan maksudnya secara langsung, dibantu menjadi proses digital melalui aplikasi.

Dari sisi backend, bagian pentingnya adalah membuat komunikasi antarbagian tersebut berjalan melalui REST API sehingga aplikasi mobile tidak perlu berkomunikasi langsung dengan setiap komponen sistem.

---

## 2. Jika aplikasi memiliki penyimpanan file atau registrasi akun, bagaimana cara membuat penyimpanan yang mudah digunakan oleh pengguna awam? Bagaimana membantu pengguna membuat password yang aman?

Pada bagian backend, penyimpanan data harus dibuat sederhana dari sisi pengguna tetapi tetap teratur di dalam sistem.

Untuk file video, backend dapat menerima file melalui endpoint tertentu kemudian memberikan response yang jelas kepada aplikasi. Pengguna tidak perlu mengetahui bagaimana file tersebut sebenarnya disimpan di server.

Untuk akun, data yang diperlukan sebaiknya hanya data yang memang dibutuhkan oleh aplikasi. Password juga tidak boleh disimpan dalam bentuk teks biasa. Password seharusnya diproses menggunakan metode hashing sebelum disimpan ke database.

Dari sisi tampilan aplikasi, pengguna dapat diberikan aturan sederhana saat membuat password, misalnya menggunakan kombinasi huruf besar, huruf kecil, angka, dan karakter khusus. Sistem juga bisa memberikan pesan apabila password yang dibuat terlalu mudah.

Dengan cara tersebut, pengguna tetap mendapatkan proses yang sederhana sedangkan keamanan datanya tetap diperhatikan dari sisi backend.



## 3. Bagaimana desain search bar pada aplikasi? Sebutkan aset eksternal yang digunakan dan lisensinya.

Untuk BicaraUntukku, fitur pencarian bukan merupakan fitur utama karena fungsi utama aplikasi adalah menerjemahkan bahasa isyarat.

Kalau nantinya ditambahkan fitur pencarian, search bar dapat dibuat sederhana dengan satu kolom input dan tombol pencarian. Pengguna cukup memasukkan kata yang ingin dicari tanpa harus memahami proses yang terjadi di backend.

Pada sisi backend, input pencarian tersebut dapat dikirim melalui endpoint API dan server akan mengolah parameter pencarian lalu mengembalikan hasilnya dalam bentuk response JSON.

Untuk pengembangan aplikasi, project juga menggunakan beberapa library atau framework dari pihak lain. Penggunaan library, icon, API, dataset, maupun aset lainnya perlu memperhatikan lisensinya. Aset yang digunakan harus berasal dari sumber yang mengizinkan penggunaannya, misalnya open-source dengan lisensi yang sesuai atau public domain. Jika suatu aset memiliki copyright khusus, penggunaannya harus mengikuti ketentuan dari pemiliknya.


## 4. Jika aplikasi memiliki interaksi sosial, bagaimana mencegah pelanggaran etika digital? Jika menggunakan AI, bagaimana memastikan AI digunakan secara bertanggung jawab?

BicaraUntukku tidak berfokus pada media sosial, tetapi tetap ada kemungkinan data atau hasil terjemahan digunakan oleh pengguna lain. Karena itu, sistem harus dibuat supaya data pengguna tidak sembarangan ditampilkan atau dibagikan.

Dari sisi backend, akses ke endpoint tertentu perlu dibatasi sesuai kebutuhan. Data yang bersifat pribadi juga sebaiknya tidak dikembalikan dalam response jika memang tidak diperlukan oleh client.

Untuk penggunaan AI, AI pada aplikasi digunakan sebagai alat untuk membantu proses penerjemahan bahasa isyarat, bukan untuk mengambil keputusan penting tentang pengguna. Hasil dari AI juga sebaiknya dianggap sebagai hasil pemrosesan sistem yang masih dapat memiliki kesalahan.

Backend berperan sebagai penghubung antara aplikasi dengan AI Engine sehingga data yang dikirim ke AI harus sesuai kebutuhan dan tidak membawa data pribadi yang tidak diperlukan.


## 5. Data pribadi sensitif apa yang mungkin dikumpulkan aplikasi? Bagaimana cara melindunginya dari kebocoran dan penyalahgunaan?

Data yang mungkin berhubungan dengan pengguna antara lain data akun seperti nama, username, password, serta video yang dikirim untuk proses penerjemahan.

Video juga perlu diperhatikan karena dapat mengandung informasi tentang pengguna atau orang lain yang ikut terekam. Oleh karena itu, data tersebut tidak sebaiknya disimpan atau dibagikan tanpa alasan yang jelas.

Dari sisi backend, beberapa hal yang dapat dilakukan yaitu:

* Password disimpan dalam bentuk hash, bukan password asli.
* Endpoint tertentu diberi autentikasi.
* Data yang dikirim melalui API menggunakan koneksi yang aman.
* File yang tidak diperlukan lagi sebaiknya tidak disimpan terlalu lama.
* Response API hanya memberikan data yang memang diperlukan.
* Informasi sensitif tidak ditampilkan di log server.
* Akses database dan file dibatasi agar tidak bisa diakses sembarang orang.

Dengan begitu, risiko kebocoran data dan penyalahgunaan informasi pengguna dapat dikurangi.


## 6. Bagaimana aplikasi memberikan informasi ketika terjadi masalah teknis seperti internet atau data gagal? Berikan contoh pesan error yang ramah dan cara troubleshooting.

Karena backend menjadi penghubung antara aplikasi mobile dan komponen lainnya, kemungkinan error tetap ada. Misalnya server sedang tidak aktif, koneksi internet pengguna terputus, file video gagal dikirim, atau proses AI mengalami masalah.

Pesan error sebaiknya tidak menampilkan pesan teknis yang sulit dimengerti pengguna. Backend dapat mengirimkan response dengan status code dan pesan yang jelas sehingga aplikasi bisa menampilkan informasi yang lebih mudah dipahami.

Contohnya:

> **"Video belum berhasil dikirim. Periksa koneksi internet kamu lalu coba lagi."**

Jika masalah berasal dari server:

> **"Server sedang mengalami kendala. Silakan coba beberapa saat lagi."**

Jika file yang dikirim tidak sesuai:

> **"Video tidak dapat diproses. Silakan gunakan video dengan format dan ukuran yang sesuai."**

Untuk troubleshooting, pengguna bisa diarahkan untuk memeriksa koneksi internet, mencoba mengirim ulang video, memastikan file sesuai ketentuan, atau mencoba kembali beberapa saat kemudian.

Dari sisi backend, error juga perlu dicatat di server agar developer dapat mengetahui penyebab masalah tanpa menampilkan informasi teknis yang sensitif kepada pengguna.

