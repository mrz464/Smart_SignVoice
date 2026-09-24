# QUIZ DIGITAL AWARENESS

* **Nama:** Ikrom Safei
* **NPM:** 24782076
* **Program Studi:** Teknologi Rekayasa Internet
* **Mata Kuliah:** Pemrograman Internet II
* **Nama Aplikasi:** BicaraUntukku (Smart_SignVoice)
* **Peran dalam Tim:** Developer Backend

---

# BAGIAN 1 — IDENTITY AND APPLICATION TOPIC

### 1. Nama Aplikasi
**BicaraUntukku (Smart_SignVoice)**

### 2. Deskripsi Singkat dan Tujuan Aplikasi
BicaraUntukku adalah aplikasi yang dibuat untuk membantu proses komunikasi penerjemahan bahasa isyarat BISINDO menjadi teks dan suara. Sistem menerima input berupa video gerakan tangan, memprosesnya dengan AI untuk klasifikasi kata, menyusun kalimat yang natural, dan mengubahnya menjadi output audio.

Di dalam tim, peran saya adalah **Developer Backend**. Tanggung jawab utama saya yaitu:
* Mengembangkan arsitektur server dan REST API menggunakan FastAPI.
* Menerima request video/data dari client (mobile/web) dan melakukan validasi format.
* Mengorkestrasi integrasi data antara client dengan AI Engine (MediaPipe, classifier kata, Gemini API, gTTS).
* Mengelola respon API dan integrasi basis data jika diperlukan.

### 3. Target Pengguna
* Komunitas Tuli dan teman-teman pengguna bahasa isyarat BISINDO.
* Masyarakat umum yang ingin berkomunikasi secara lancar dengan pengguna BISINDO.
* Guru, relawan, tenaga medis, atau pendamping komunitas Tuli.
* Institusi layanan publik yang membutuhkan aksesibilitas komunikasi ramah disabilitas.

---

# BAGIAN 2 — RESUME 6 MODULE DIGITAL AWARENESS

### Module 1 — There's a Whole New World Out There!
Modul ini menjelaskan transformasi digital yang mengubah berbagai aktivitas manual menjadi lebih cepat dan efisien. Pada proyek BicaraUntukku, proses menerjemahkan bahasa isyarat yang biasanya memerlukan juru bahasa isyarat (JBI) secara langsung dibantu menggunakan teknologi AI terintegrasi, sehingga komunikasi dua arah bisa dilakukan lebih mandiri dan fleksibel kapan saja.

### Module 2 — You'll Need Some Basic Tools
Modul ini membahas perangkat keras, sistem operasi, struktur berkas, dan penggunaan *tools* pendukung secara aman. Bagi saya di sisi backend, modul ini langsung terhubung dengan penggunaan Python, isolasi paket melalui *virtual environment* (`venv`), struktur folder proyek, pengelolaan environment variable (`.env`), serta version control Git untuk kolaborasi tim yang rapi tanpa merusak kode repositori.

### Module 3 — This is How You Get Around and Find What You're Looking For
Modul ini menekankan kemampuan navigasi internet, pencarian informasi kredibel, dan verifikasi sumber. Dalam konteks backend, kebiasaan ini sangat krusial saat membaca dokumentasi resmi (seperti FastAPI, Pydantic, SQLAlchemy) serta mencari solusi *debugging* error teknis agar kode yang diimplementasikan aman, stabil, dan bukan sekadar *copy-paste* tanpa dipahami.

### Module 4 — It Just Keeps Getting Better
Modul ini mengulas evolusi teknologi digital dan kecerdasan buatan (AI) beserta tanggung jawab etis pemanfaatannya. Di proyek ini, AI (MediaPipe, LSTM/BiLSTM, dan LLM) dimanfaatkan untuk meningkatkan aksesibilitas sosial. Sebagai backend, tanggung jawab saya adalah memastikan data frame/video yang dikirim ke AI Engine diproses secara efisien tanpa kebocoran data pengguna.

### Module 5 — Even Though It's Digital, It Is Real, With Real Consequences
Modul ini mengingatkan bahwa rekam jejak dan keamanan digital memiliki konsekuensi hukum serta dampak nyata bagi orang lain. Karena backend menangani input video wajah dan gerakan tangan pengguna yang bersifat personal, saya harus memastikan file tersebut tidak disalahgunakan, tidak disimpan permanen tanpa izin, dan hak privasi pengguna tetap terjaga dengan aman.

### Module 6 — Learn About Anything and Everything
Modul ini mengajarkan pola pikir pembelajar mandiri (*troubleshooting mindset*). Menghadapi error pada koneksi database, routing API, integrasi service AI, hingga penyesuaian dependensi library menuntut saya untuk terus belajar, membaca log server secara runtut, dan menyelesaikan masalah teknis secara terstruktur.

---

# BAGIAN 3 — DIGITAL AWARENESS & PROJECT

### 1. Bagaimana desain aplikasi dapat mempermudah pekerjaan sehari-hari? Proses analog/tradisional apa yang menjadi digital?
Proses analog yang diubah menjadi digital adalah penerjemahan percakapan bahasa isyarat yang awalnya membutuhkan kehadiran juru bahasa isyarat (JBI) manusia secara langsung di lokasi. 

Melalui BicaraUntukku, pengguna cukup merekam gerakan isyarat. Client mengirim file video ke backend melalui REST API FastAPI. Backend kemudian mengalirkan data ke pipeline AI untuk ekstraksi koordinat tangan, memetakan ke label kata BISINDO, menyusunnya menjadi kalimat utuh via Gemini API, serta menghasilkan suara via gTTS. Hasil JSON teks dan link file audio dikembalikan lagi ke aplikasi secara instan.

### 2. Jika aplikasi memiliki penyimpanan file atau registrasi akun, bagaimana cara membuat penyimpanan yang mudah digunakan oleh pengguna awam? Bagaimana membantu pengguna membuat password yang aman?
* **Penyimpanan Ramah Pengguna:** Dari sisi backend, alur upload video dibuat transparan. User hanya perlu menekan tombol unggah/rekam di UI, sementara backend menangani validasi MIME type, ukuran file (maksimal frame/MB), penamaan UUID acak, dan pembersihan file sementara (*temporary storage cleanup*).
* **Keamanan Password:**
  * Backend **tidak pernah** menyimpan password teks polos, melainkan menerapkan enkripsi *hashing* menggunakan algoritma modern seperti `bcrypt`.
  * Sistem memberikan aturan validasi minimum 8 karakter (kombinasi huruf besar, huruf kecil, angka, dan simbol).
  * Pesan error validasi ditampilkan secara jelas di antarmuka jika password terlalu lemah.

### 3. Bagaimana desain search bar pada aplikasi? Sebutkan aset eksternal yang digunakan dan lisensinya.
* **Desain Fitur Pencarian:** Fitur pencarian dirancang sederhana untuk mencari riwayat terjemahan teks atau kamus glosarium 32 kosakata BISINDO yang didukung. Backend menerima parameter query (misal: `GET /api/dictionary?search=makan`) dan mengembalikan data secara cepat dalam format JSON terstruktur.
* **Aset Eksternal dan Lisensi:**
  * **Dataset WL-BISINDO:** Dataset video bahasa isyarat untuk keperluan riset dan akademik.
  * **MediaPipe Hands:** Toolkit machine learning Google di bawah lisensi *Apache License 2.0*.
  * **FastAPI Framework:** Web framework backend di bawah lisensi *MIT License*.
  * **Google Gemini API:** Layanan cloud AI mengikuti ketentuan *Google APIs Terms of Service*.
  * **gTTS (Google Text-to-Speech):** Modul Python open-source di bawah lisensi *MIT License*.

### 4. Jika aplikasi memiliki interaksi sosial, bagaimana mencegah pelanggaran etika digital? Jika menggunakan AI, bagaimana memastikan AI digunakan secara bertanggung jawab?
* **Pencegahan Penyalahgunaan:** Backend membatasi payload data pengguna, menerapkan sanitasi input, dan tidak menyediakan akses publik ke raw video pengguna lain.
* **Etika dan Tanggung Jawab AI:** 
  * AI pada sistem ini diposisikan sebagai alat bantu aksesibilitas komunikasi (*assistive tool*), bukan penentu keputusan krusial.
  * Backend menyertakan disclaimer bahwa hasil penerjemahan AI berbasis probabilitas dan masih dapat terjadi ketidaksesuaian konteks gerakan tangan.
  * Video hanya digunakan untuk pemrosesan ekstraksi koordinat landmark secara langsung di memori/server sementara dan tidak digunakan untuk melatih model lain tanpa persetujuan pengguna.

### 5. Data pribadi sensitif apa yang mungkin dikumpulkan aplikasi? Bagaimana cara melindunginya dari kebocoran dan penyalahgunaan?
* **Data Sensitif:** Data identitas akun (nama, email, hash password) dan rekaman visual video pengguna (wajah dan gestur tubuh).
* **Langkah Perlindungan di Sisi Backend:**
  1. Komunikasi jaringan wajib menggunakan protokol terenkripsi HTTPS/TLS.
  2. Implementasi enkripsi password satu arah menggunakan *hashing salt* (`bcrypt`).
  3. Mengamankan API menggunakan otentikasi token JWT (*JSON Web Token*) pada endpoint terproteksi.
  4. Menerapkan mekanisme penghapusan otomatis (*auto-purge*) pada file video sementara setelah ekstraksi fitur AI selesai.
  5. Memisahkan kredensial database dan API key ke dalam berkas environment tersembunyi (`.env`) yang tidak di-push ke Git publik.

### 6. Bagaimana aplikasi memberikan informasi ketika terjadi masalah teknis seperti internet atau data gagal? Berikan contoh pesan error yang ramah dan cara troubleshooting.
Backend merespons masalah dengan HTTP Status Code standar (400, 422, 500, dll.) dan payload JSON berisi pesan informatif yang mudah diterjemahkan oleh antarmuka aplikasi.

Contoh pesan error yang ramah pengguna:
* **Gagal Jaringan / Koneksi:**
  > *"Gagal terhubung ke server. Periksa kembali koneksi internet Anda dan coba beberapa saat lagi."*
* **Format Video Tidak Sesuai (HTTP 422 / 400):**
  > *"Format video tidak didukung. Mohon rekam atau unggah video berformat MP4 dengan durasi maksimal 5 detik."*
* **Kendala Pemrosesan AI / Server (HTTP 500):**
  > *"Layanan penerjemah sedang sibuk memproses antrean. Silakan tekan tombol 'Coba Lagi' dalam beberapa detik."*

**Langkah Troubleshooting:** 
Pengguna diberikan opsi tombol *“Coba Lagi”*, petunjuk ringkas untuk memposisikan tangan tepat di depan kamera dengan pencahayaan cukup, serta log teknis tetap tersimpan rapi hanya di sisi server (*server logs*) tanpa membeberkan celah sistem ke publik.
