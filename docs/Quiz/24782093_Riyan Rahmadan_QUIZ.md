**QUIZ DIGITAL AWARENESS**

**Interconnecting between Digital Awareness and Application Design**

| **Nama**          | Riyan Rahmadan                                                       |
| ----------------- | -------------------------------------------------------------------- |
| **NPM**           | 24782093                                                             |
| **Program Studi** | Teknologi Rekayasa Internet                                          |
| **Mata Kuliah**   | Internet Programming II                                              |
| **Nama Aplikasi** | BicaraUntukku (Smart_SignVoice)                                      |
| **Peran**         | Developer AI Engine                                                  |
| **Fokus**         | Pipeline AI untuk menerjemahkan video BISINDO menjadi teks dan suara |

# BAGIAN 1 — IDENTITAS DAN TOPIK PROYEK APLIKASI

## 1\. Nama Aplikasi

BicaraUntukku (Smart_SignVoice)

## 2\. Deskripsi Singkat dan Tujuan Utama Aplikasi

BicaraUntukku merupakan aplikasi yang dikembangkan untuk membantu komunikasi antara penyandang tunarungu atau tunawicara yang menggunakan bahasa isyarat BISINDO dengan orang yang belum memahami bahasa isyarat tersebut.

Pengguna memberikan input berupa video gerakan tangan melalui aplikasi mobile. Video dikirim ke backend untuk diproses oleh AI Engine. Video diproses menjadi keypoint tangan menggunakan MediaPipe Hands, kemudian sequence keypoint digunakan oleh LSTM Classifier untuk mengenali kata BISINDO.

Setelah kata dikenali, hasilnya diteruskan ke Gemini API untuk menyusun kalimat Bahasa Indonesia yang lebih natural. Selanjutnya gTTS mengubah kalimat tersebut menjadi suara.

Sebagai Developer AI Engine, saya membangun pipeline yang menghubungkan ekstraksi keypoint, klasifikasi LSTM, penyusunan kalimat menggunakan LLM, dan konversi teks menjadi suara.

Pipeline AI yang saya kerjakan:

- Video BISINDO
- MediaPipe Hands
- 21 keypoint × 3 koordinat
- Sequence 30 frame × 63 fitur
- LSTM Bidirectional
- Label kata BISINDO
- Gemini LLM
- Kalimat Bahasa Indonesia
- gTTS
- Audio MP3

## 3\. Target Pengguna Utama

Target pengguna utama adalah penyandang tunarungu dan tunawicara yang menggunakan bahasa isyarat BISINDO. Guru SLB dan pendamping menjadi pengguna sekunder yang dapat memantau perkembangan siswa melalui dashboard.

# BAGIAN 2 — RESUME MODUL DIGITAL AWARENESS

## 1\. Modul 1 — There's a whole new world out there

Modul ini menjelaskan bagaimana teknologi digital mengubah aktivitas manusia. Dalam AI Engine, video gerakan tangan diubah menjadi data keypoint yang dapat diproses komputer sehingga proses pengenalan gerakan dapat dibantu oleh sistem digital.

## 2\. Modul 2 — You'll Need Some Basic Tools

Modul ini membahas perangkat digital, sistem operasi, file dan folder, serta keamanan password. Dalam AI Engine, source code, model, dataset, konfigurasi, dan dependency perlu dikelola dengan baik. API key tidak boleh ditulis langsung di source code dan sebaiknya disimpan sebagai environment variable atau .env yang tidak di-push ke Git.

## 3\. Modul 3 — This is how you get around and find what you're looking for

Modul ini membahas penggunaan browser, pencarian informasi, copyright, dan public domain. Developer AI perlu menggunakan dokumentasi resmi MediaPipe, TensorFlow, OpenCV, dan Gemini serta memeriksa sumber dan lisensi dataset, model, dan library.

## 4\. Modul 4 — It just keeps getting better

Modul ini membahas perkembangan AI dan tanggung jawab penggunaannya. AI dalam BicaraUntukku membantu mengenali pola gerakan, tetapi hasilnya dapat dipengaruhi kualitas video, pencahayaan, posisi tangan, background, dan perbedaan pengguna dengan data training. Karena itu keterbatasan AI harus diperhatikan.

## 5\. Modul 5 — Even Though It's Digital, It is Real, With Real Consequences

Modul ini menjelaskan bahwa data digital dapat menimbulkan konsekuensi nyata. Video pengguna harus diproses sesuai kebutuhan dan tidak disimpan permanen jika tidak diperlukan. API key juga harus dijaga karena dapat mengakses layanan eksternal.

## 6\. Modul 6 — Learn About Anything and Everything

Modul ini membahas troubleshooting. Jika prediksi salah, developer dapat memeriksa video, deteksi tangan, jumlah keypoint, preprocessing, input model, dan output prediksi secara bertahap untuk menemukan sumber masalah.

# BAGIAN 3 — HUBUNGAN DAN IMPLEMENTASI PADA TOPIK PROYEK

## 1\. Bagaimana rancangan aplikasi dapat mempermudah tugas sehari-hari pengguna?

BicaraUntukku membantu mengurangi hambatan komunikasi pengguna BISINDO. Pengguna memberikan video gerakan tangan, kemudian AI Engine memproses video menjadi keypoint, mengenali kata, menyusun kalimat, dan menghasilkan suara.

Contohnya:

- gerakan tangan
- video
- AI mengenali pola
- Apa
- Ada apa
- Suara

Proses ini membantu pengguna menyampaikan maksud tanpa harus selalu mencari orang yang memahami BISINDO.

## 2\. Jika aplikasi memiliki penyimpanan file atau pendaftaran akun, bagaimana merancang penyimpanan dan password?

Video sebaiknya diproses sementara dan dihapus jika tidak diperlukan lagi. Hasil yang diperlukan dapat disimpan sebagai data sesi, kata, atau hasil penerjemahan. Password harus diproses di backend dan tidak disimpan plaintext. API key Gemini juga harus disimpan sebagai environment variable atau .env dan tidak dimasukkan ke repository.

## 3\. Bagaimana mendesain fitur pencarian dan bagaimana dengan asset eksternal?

AI Engine tidak memiliki search bar seperti dashboard, tetapi developer membutuhkan pencarian dokumentasi untuk MediaPipe, TensorFlow/Keras, OpenCV, NumPy, Scikit-learn, Gemini API, dan gTTS. Dataset WL-BISINDO juga merupakan asset eksternal yang sumber dan lisensinya harus diperhatikan. Library, dataset, dan model harus digunakan sesuai ketentuan lisensinya.

## 4\. Bagaimana memastikan AI bekerja secara etis dan bertanggung jawab?

Model LSTM digunakan untuk mengklasifikasikan sequence keypoint menjadi kata BISINDO dan memiliki akurasi pengujian 99,69% pada dataset yang digunakan. Angka tersebut tidak berarti model selalu benar pada semua pengguna dan kondisi. Keterbatasan seperti variasi BISINDO, pencahayaan rendah, background ramai, dan dukungan gerakan dua tangan harus diperhatikan. AI sebaiknya menjadi alat bantu, hasilnya dapat dikoreksi manusia, dan Gemini tidak boleh diarahkan untuk menambahkan informasi yang tidak berasal dari hasil pengenalan.

## 5\. Data pribadi sensitif apa yang dikumpulkan dan bagaimana melindunginya?

Data utama dari AI Engine adalah video gerakan pengguna. Video dapat mengandung informasi lain sehingga prinsip data minimization perlu diterapkan. Sistem cukup memproses data yang dibutuhkan untuk penerjemahan. Setelah keypoint diperoleh, video dapat dihapus jika tidak diperlukan. API key Gemini juga harus dijaga dan tidak boleh di-upload ke GitHub.

## 6\. Bagaimana aplikasi mengomunikasikan masalah teknis kepada pengguna?

Error AI harus diterjemahkan menjadi pesan yang mudah dipahami. Contohnya: "Video belum dapat diproses. Silakan coba rekam ulang." Jika tangan tidak terdeteksi: "Gerakan tangan belum terlihat dengan jelas. Pastikan tangan berada di dalam kamera dan pencahayaan cukup." Jika layanan AI gagal: "Layanan penerjemahan sedang tidak tersedia. Periksa koneksi internet dan coba kembali." Jika confidence rendah, pengguna dapat diminta mengulangi gerakan.

# KESIMPULAN

Sebagai Developer AI Engine, penerapan Digital Awareness bukan hanya tentang membuat model AI, tetapi juga memastikan AI digunakan secara aman, bertanggung jawab, dan sesuai kebutuhan pengguna. Pipeline BicaraUntukku mengubah video bahasa isyarat menjadi keypoint, menggunakan LSTM untuk mengenali kata, Gemini untuk menyusun kalimat, dan gTTS untuk menghasilkan suara.

AI Engine perlu memperhatikan keterbatasan model, privasi video, keamanan API key, lisensi dataset dan library, serta cara sistem menangani kesalahan. Keberhasilan AI tidak hanya diukur dari akurasi, tetapi juga dari penggunaan teknologi yang aman dan bertanggung jawab.