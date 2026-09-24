# **QUIZ DIGITAL AWARENESS** 

#### **Interconnecting between Digital Awareness and Application Design** 

|**Nama**|Muhammad Rezaldi Zazky|
|---|---|
|**NPM**|24782086|
|**Program Studi**|Teknologi Rekayasa Internet|
|**Mata Kuliah**|Internet Programming II|
|**Nama Aplikasi**|BicaraUntukku (Smart_SignVoice)|
|**Peran**|Developer Mobile Flutter|
|**Fokus**|Aplikasi mobile untuk merekam video BISINDO<br>dan menerima hasil penerjemahan|



## **BAGIAN 1 — IDENTITAS DAN TOPIK PROYEK APLIKASI** 

### **1. Nama Aplikasi** 

BicaraUntukku (Smart_SignVoice) 

### **2. Deskripsi Singkat dan Tujuan Utama Aplikasi** 

BicaraUntukku merupakan aplikasi yang dikembangkan untuk membantu komunikasi bagi penyandang tunarungu dan tunawicara yang menggunakan bahasa isyarat BISINDO. Aplikasi memanfaatkan teknologi mobile dan Artificial Intelligence untuk membantu mengubah gerakan bahasa isyarat menjadi teks dan suara. 

Dalam proyek ini, saya berperan sebagai Developer Mobile Flutter. Fokus pekerjaan saya adalah membangun aplikasi mobile sebagai antarmuka utama pengguna. Aplikasi digunakan untuk menerima input berupa rekaman video gerakan bahasa isyarat, mengirimkan video tersebut ke backend melalui REST API, serta menampilkan hasil penerjemahan yang dikembalikan sistem. 

Setelah video dikirim, backend meneruskannya ke AI Engine. AI Engine memproses video menggunakan MediaPipe, LSTM, Gemini, dan gTTS. Hasilnya kemudian dikembalikan ke aplikasi mobile untuk ditampilkan sebagai teks dan digunakan sebagai output suara. 

Dengan demikian, aplikasi mobile menjadi penghubung langsung antara pengguna dan sistem AI. Pengguna tidak perlu berinteraksi langsung dengan proses teknis seperti ekstraksi keypoint, model LSTM, atau API Gemini. 

### **3. Target Pengguna Utama** 

Target pengguna utama adalah penyandang tunarungu dan tunawicara yang menggunakan bahasa isyarat BISINDO. Mobile app memudahkan mereka menggunakan kamera smartphone untuk memberikan input gerakan tangan dan mendapatkan hasil dalam bentuk teks serta suara. Guru SLB dan pendamping merupakan pengguna sekunder yang memantau perkembangan melalui web dashboard. 

## **BAGIAN 2 — RESUME MODUL DIGITAL AWARENESS** 

### **1. Modul 1 — There's a whole new world out there!** 

Modul ini menjelaskan perubahan aktivitas manusia akibat perkembangan teknologi digital. Pada BicaraUntukku, proses komunikasi dibantu melalui aplikasi mobile sehingga pengguna dapat menggunakan smartphone untuk memberikan input bahasa isyarat kepada sistem. 

### **2. Modul 2 — You'll Need Some Basic Tools** 

Modul ini membahas perangkat digital, sistem operasi, file dan folder, serta keamanan akun. Dalam aplikasi mobile, pengelolaan project, asset, konfigurasi, permission perangkat, dan credential perlu diperhatikan. Informasi rahasia tidak boleh dibagikan sembarangan. 

### **3. Modul 3 — This is how you get around and find what you're looking for** 

Modul ini membahas penggunaan browser, pencarian informasi, copyright, dan public domain. Developer Flutter perlu menggunakan dokumentasi dan library secara tepat. Icon, gambar, font, package, dan asset dari internet harus diperiksa sumber dan lisensinya. 

### **4. Modul 4 — It just keeps getting better** 

Modul ini membahas perkembangan teknologi dan AI serta tanggung jawab dalam menggunakannya. Mobile app menggunakan hasil AI untuk membantu komunikasi, tetapi hasil AI tidak selalu benar. Pengguna perlu dapat melakukan perekaman ulang jika hasil pengenalan tidak sesuai. 

### **5. Modul 5 — Even Though It's Digital, It is Real, With Real Consequences** 

Modul ini menjelaskan bahwa aktivitas digital memiliki konsekuensi nyata. Aplikasi berhubungan dengan video pengguna sehingga privacy dan keamanan harus diperhatikan. Permission kamera dan akses data harus digunakan hanya ketika diperlukan. 

### **6. Modul 6 — Learn About Anything and Everything** 

Modul ini membahas troubleshooting. Pada mobile app, masalah dapat terjadi pada permission kamera, file video, koneksi internet, REST API, atau proses penerjemahan. Masalah perlu diperiksa secara bertahap dan pesan error harus mudah dipahami pengguna. 

## **BAGIAN 3 — HUBUNGAN DAN IMPLEMENTASI PADA PROYEK** 

### **1. Bagaimana rancangan aplikasi dapat mempermudah tugas sehari-hari pengguna?** 

BicaraUntukku membantu pengguna bahasa isyarat berkomunikasi dengan orang yang belum memahami BISINDO. Dari sisi mobile, pengguna cukup menggunakan smartphone untuk merekam gerakan tangan. Video dikirim ke backend melalui REST API untuk diproses AI Engine. Hasil penerjemahan kemudian dikembalikan ke aplikasi dan ditampilkan sebagai teks serta suara. Pengguna tidak perlu melakukan penerjemahan secara manual atau memahami proses teknis AI. 

### **2. Jika aplikasi memiliki penyimpanan file atau pendaftaran akun, bagaimana merancang penyimpanan dan password?** 

Video sebaiknya hanya dikirim ketika pengguna menjalankan proses penerjemahan. Jika video tidak diperlukan setelah proses selesai, penyimpanan permanen sebaiknya dihindari. Password 

tidak boleh disimpan secara langsung dalam bentuk yang mudah dibaca. Jika autentikasi digunakan, login dilakukan melalui backend dan token dikelola dengan mekanisme penyimpanan yang sesuai. 

### **3. Bagaimana mendesain fitur pencarian dan bagaimana dengan asset eksternal?** 

Fitur pencarian lebih relevan pada dashboard, sedangkan mobile app berfokus pada input video dan hasil penerjemahan. Mobile tetap perlu menyediakan navigasi yang sederhana untuk fitur utama seperti mulai rekam dan melihat hasil. Package Flutter, icon, font, gambar, dan komponen UI dari pihak lain harus diperiksa sumber dan lisensinya sebelum digunakan. 

### **4. Bagaimana memastikan AI bekerja secara etis dan bertanggung jawab?** 

Mobile app harus menampilkan hasil AI sebagai hasil penerjemahan, bukan sesuatu yang selalu benar. Jika gerakan tidak dikenali atau hasil tidak sesuai, pengguna sebaiknya dapat melakukan perekaman ulang. Desain aplikasi juga dapat memberi instruksi agar tangan terlihat jelas, posisi kamera sesuai, dan pencahayaan cukup. Keterbatasan model perlu diperhatikan ketika merancang pengalaman pengguna. 

### **5. Data pribadi sensitif apa yang dikumpulkan dan bagaimana melindunginya?** 

Data yang paling berkaitan dengan mobile app adalah video gerakan pengguna. Video dapat mengandung informasi tentang pengguna dan lingkungan sekitar. Aplikasi sebaiknya meminta permission kamera secara jelas dan hanya mengakses kamera ketika diperlukan. Video dikirim melalui koneksi yang aman dan tidak disimpan permanen jika tidak diperlukan. 

### **6. Bagaimana aplikasi mengomunikasikan masalah teknis kepada pengguna?** 

Mobile app sebaiknya mengubah error teknis menjadi pesan yang mudah dipahami. Jika kamera bermasalah: “Kamera tidak dapat digunakan. Periksa permission kamera lalu coba kembali.” Jika koneksi gagal: “Tidak dapat terhubung ke server. Periksa koneksi internet Anda.” Jika video gagal diproses: “Video belum dapat diproses. Silakan coba rekam ulang dengan posisi tangan terlihat jelas.” Pesan tersebut lebih berguna daripada menampilkan kode error API atau exception. 

## **KESIMPULAN** 

Sebagai Developer Mobile Flutter, penerapan Digital Awareness dalam BicaraUntukku berkaitan dengan cara aplikasi berinteraksi langsung dengan pengguna. Mobile app menjadi bagian yang digunakan untuk merekam bahasa isyarat, mengirim video ke backend, dan menerima hasil penerjemahan. 

Karena mobile app menjadi titik interaksi langsung, desain aplikasi perlu memperhatikan kemudahan penggunaan, permission perangkat, keamanan data, penggunaan asset, komunikasi error, serta keterbatasan hasil AI. Dengan prinsip tersebut, teknologi dapat digunakan sebagai alat bantu komunikasi yang lebih mudah dan bertanggung jawab. 

