import 'dart:convert';
import 'dart:io';

import 'package:audioplayers/audioplayers.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(BicaraUntukkuApp(cameras: cameras));
}

class BicaraUntukkuApp extends StatelessWidget {
  final List<CameraDescription> cameras;

  const BicaraUntukkuApp({
    super.key,
    required this.cameras,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'BicaraUntukku',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: const Color(0xFFF5F7FA),
      ),
      home: LoginScreen(cameras: cameras),
    );
  }
}

// ============================================================
// LOGIN SCREEN (MODERN UI)
// ============================================================

class LoginScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const LoginScreen({
    super.key,
    required this.cameras,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  bool _obscurePassword = true;

  void login() {
    final email = emailController.text.trim();
    final password = passwordController.text.trim();

    if (email == 'guru@bisindo.com' && password == 'admin123') {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => HomeScreen(cameras: widget.cameras),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Row(
            children: [
              Icon(Icons.error_outline, color: Colors.white),
              SizedBox(width: 8),
              Text('Email atau password salah!'),
            ],
          ),
          backgroundColor: Colors.red.shade600,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        ),
      );
    }
  }

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.fromLTRB(24, 60, 24, 40),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.blue.shade800, Colors.blue.shade500],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: const BorderRadius.only(
                  bottomLeft: Radius.circular(36),
                  bottomRight: Radius.circular(36),
                ),
              ),
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.18),
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white.withOpacity(0.3), width: 1.5),
                    ),
                    child: const Icon(
                      Icons.sign_language_rounded,
                      size: 64,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'BicaraUntukku',
                    style: TextStyle(
                      fontSize: 30,
                      fontWeight: FontWeight.w800,
                      color: Colors.white,
                      letterSpacing: 0.5,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    'Smart SignVoice Translator',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.white.withOpacity(0.85),
                      fontWeight: FontWeight.w400,
                    ),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
              child: Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.04),
                      blurRadius: 20,
                      offset: const Offset(0, 8),
                    ),
                  ],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Masuk Akun',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF1E293B)),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Masukkan email dan password untuk melanjutkan',
                      style: TextStyle(fontSize: 13, color: Color(0xFF64748B)),
                    ),
                    const SizedBox(height: 24),
                    TextField(
                      controller: emailController,
                      keyboardType: TextInputType.emailAddress,
                      decoration: InputDecoration(
                        labelText: 'Email',
                        hintText: 'contoh@bisindo.com',
                        prefixIcon: const Icon(Icons.email_outlined, color: Colors.blue),
                        filled: true,
                        fillColor: const Color(0xFFF8FAFC),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Colors.blue, width: 1.5)),
                      ),
                    ),
                    const SizedBox(height: 18),
                    TextField(
                      controller: passwordController,
                      obscureText: _obscurePassword,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        prefixIcon: const Icon(Icons.lock_outline_rounded, color: Colors.blue),
                        filled: true,
                        fillColor: const Color(0xFFF8FAFC),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
                        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
                        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Colors.blue, width: 1.5)),
                        suffixIcon: IconButton(
                          onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                          icon: Icon(_obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined, color: const Color(0xFF94A3B8)),
                        ),
                      ),
                    ),
                    const SizedBox(height: 28),
                    Container(
                      width: double.infinity,
                      height: 52,
                      decoration: BoxDecoration(
                        gradient: LinearGradient(colors: [Colors.blue.shade600, Colors.blue.shade800]),
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(color: Colors.blue.withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 4)),
                        ],
                      ),
                      child: ElevatedButton(
                        onPressed: login,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.transparent,
                          shadowColor: Colors.transparent,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                        ),
                        child: const Text('LOGIN', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 0.5, color: Colors.white)),
                      ),
                    ),
                    const SizedBox(height: 20),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Text('Belum punya akun? ', style: TextStyle(color: Color(0xFF64748B), fontSize: 14)),
                        GestureDetector(
                          onTap: () {
                            Navigator.push(context, MaterialPageRoute(builder: (context) => RegisterScreen(cameras: widget.cameras)));
                          },
                          child: Text('Daftar di sini', style: TextStyle(color: Colors.blue.shade700, fontWeight: FontWeight.bold, fontSize: 14)),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              margin: const EdgeInsets.only(bottom: 20),
              decoration: BoxDecoration(
                color: const Color(0xFFE2E8F0).withOpacity(0.5),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Text('Demo Akun: guru@bisindo.com / admin123', style: TextStyle(color: Color(0xFF64748B), fontSize: 12)),
            ),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// REGISTER SCREEN (MODERN UI)
// ============================================================

class RegisterScreen extends StatefulWidget {
  final List<CameraDescription> cameras;

  const RegisterScreen({
    super.key,
    required this.cameras,
  });

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final confirmPasswordController = TextEditingController();

  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;

  void register() {
    final name = nameController.text.trim();
    final email = emailController.text.trim();
    final password = passwordController.text.trim();
    final confirmPassword = confirmPasswordController.text.trim();

    if (name.isEmpty || email.isEmpty || password.isEmpty || confirmPassword.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Semua kolom wajib diisi!'), backgroundColor: Colors.orange.shade700, behavior: SnackBarBehavior.floating),
      );
      return;
    }

    if (password != confirmPassword) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Password dan Konfirmasi Password tidak cocok!'), backgroundColor: Colors.red.shade600, behavior: SnackBarBehavior.floating),
      );
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Row(children: [Icon(Icons.check_circle, color: Colors.white), SizedBox(width: 8), Text('Registrasi berhasil! Silakan login.')]),
        backgroundColor: Colors.green.shade600,
        behavior: SnackBarBehavior.floating,
      ),
    );

    Navigator.pop(context);
  }

  @override
  void dispose() {
    nameController.dispose();
    emailController.dispose();
    passwordController.dispose();
    confirmPasswordController.dispose();
    super.dispose();
  }

  InputDecoration _customInputDecoration({required String label, required IconData prefixIcon, Widget? suffixIcon}) {
    return InputDecoration(
      labelText: label,
      prefixIcon: Icon(prefixIcon, color: Colors.blue),
      suffixIcon: suffixIcon,
      filled: true,
      fillColor: const Color(0xFFF8FAFC),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Color(0xFFE2E8F0))),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: Colors.blue, width: 1.5)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Daftar Akun', style: TextStyle(fontWeight: FontWeight.bold)),
        elevation: 0,
        backgroundColor: Colors.transparent,
        foregroundColor: const Color(0xFF1E293B),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 20, offset: const Offset(0, 8))],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Buat Akun Baru', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF1E293B))),
                const SizedBox(height: 6),
                const Text('Lengkapi data di bawah untuk bergabung', style: TextStyle(fontSize: 13, color: Color(0xFF64748B))),
                const SizedBox(height: 24),
                TextField(controller: nameController, decoration: _customInputDecoration(label: 'Nama Lengkap', prefixIcon: Icons.person_outline_rounded)),
                const SizedBox(height: 16),
                TextField(controller: emailController, keyboardType: TextInputType.emailAddress, decoration: _customInputDecoration(label: 'Email', prefixIcon: Icons.email_outlined)),
                const SizedBox(height: 16),
                TextField(
                  controller: passwordController,
                  obscureText: _obscurePassword,
                  decoration: _customInputDecoration(
                    label: 'Password',
                    prefixIcon: Icons.lock_outline_rounded,
                    suffixIcon: IconButton(
                      onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                      icon: Icon(_obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined, color: const Color(0xFF94A3B8)),
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: confirmPasswordController,
                  obscureText: _obscureConfirmPassword,
                  decoration: _customInputDecoration(
                    label: 'Konfirmasi Password',
                    prefixIcon: Icons.lock_reset_rounded,
                    suffixIcon: IconButton(
                      onPressed: () => setState(() => _obscureConfirmPassword = !_obscureConfirmPassword),
                      icon: Icon(_obscureConfirmPassword ? Icons.visibility_outlined : Icons.visibility_off_outlined, color: const Color(0xFF94A3B8)),
                    ),
                  ),
                ),
                const SizedBox(height: 28),
                Container(
                  width: double.infinity,
                  height: 52,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: [Colors.blue.shade600, Colors.blue.shade800]),
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [BoxShadow(color: Colors.blue.withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 4))],
                  ),
                  child: ElevatedButton(
                    onPressed: register,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.transparent,
                      shadowColor: Colors.transparent,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                    ),
                    child: const Text('DAFTAR SEKARANG', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 0.5, color: Colors.white)),
                  ),
                ),
                const SizedBox(height: 18),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Sudah punya akun? ', style: TextStyle(color: Color(0xFF64748B))),
                    GestureDetector(
                      onTap: () => Navigator.pop(context),
                      child: Text('Login di sini', style: TextStyle(color: Colors.blue.shade700, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ============================================================
// HOME SCREEN
// ============================================================

class HomeScreen extends StatelessWidget {
  final List<CameraDescription> cameras;

  const HomeScreen({
    super.key,
    required this.cameras,
  });

  void openCamera(BuildContext context) {
    if (cameras.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Kamera tidak ditemukan.')),
      );
      return;
    }

    Navigator.push(
      context,
      MaterialPageRoute(
        // --- SEKARANG MENGIRIM SELURUH LIST KAMERA BUKAN CUMA SATU ---
        builder: (context) => CameraScreen(cameras: cameras),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('BicaraUntukku'), centerTitle: true),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(child: Icon(Icons.sign_language, size: 80, color: Colors.blue)),
            const SizedBox(height: 20),
            const Center(child: Text('Selamat Datang!', style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold))),
            const SizedBox(height: 10),
            const Center(
              child: Text(
                'Terjemahkan bahasa isyarat BISINDO menjadi teks dan suara menggunakan AI.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 15, color: Colors.grey),
              ),
            ),
            const SizedBox(height: 30),
            Card(
              elevation: 3,
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.videocam, color: Colors.blue),
                        SizedBox(width: 10),
                        Text('Terjemahkan Bahasa Isyarat', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    const SizedBox(height: 15),
                    const Text('Rekam gerakan bahasa isyarat BISINDO dan sistem AI akan memprosesnya.', style: TextStyle(color: Colors.grey)),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      height: 50,
                      child: ElevatedButton.icon(
                        onPressed: () => openCamera(context),
                        icon: const Icon(Icons.camera_alt),
                        label: const Text('MULAI REKAM ISYARAT'),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            Card(
              child: ListTile(
                leading: const Icon(Icons.history, color: Colors.blue),
                title: const Text('Riwayat Terjemahan'),
                subtitle: const Text('Lihat hasil terjemahan sebelumnya'),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const HistoryScreen()));
                },
              ),
            ),
            const SizedBox(height: 20),
            Card(
              color: Colors.blue.shade50,
              child: const Padding(
                padding: EdgeInsets.all(20),
                child: Row(
                  children: [
                    Icon(Icons.auto_awesome, color: Colors.blue, size: 35),
                    SizedBox(width: 15),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('AI Smart SignVoice', style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold)),
                          SizedBox(height: 5),
                          Text('MediaPipe + Bidirectional LSTM + Gemini AI', style: TextStyle(fontSize: 13, color: Colors.grey)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 30),
            const Center(child: Text('BicaraUntukku v1.0', style: TextStyle(color: Colors.grey, fontSize: 12))),
          ],
        ),
      ),
    );
  }
}

// ============================================================
// CAMERA SCREEN (BISA SWITCH KAMERA DEPAN/BELAKANG)
// ============================================================

class CameraScreen extends StatefulWidget {
  final List<CameraDescription> cameras; // <-- SEKARANG MENERIMA LIST KAMERA

  const CameraScreen({
    super.key,
    required this.cameras,
  });

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  final AudioPlayer _audioPlayer = AudioPlayer();

  bool _isInitialized = false;
  bool _isRecording = false;
  bool _isProcessing = false;
  bool _isPlayingAudio = false;

  int _selectedCameraIndex = 0; // <-- INDEKS KAMERA YANG SEDANG AKTIF (0 biasa belakang, 1 biasa depan)

  String? _videoPath;
  int? _videoSize;
  String? _sentence;
  List<dynamic> _words = [];
  String? _audioUrl;

  static const String _backendUrl = 'http://10.210.51.30:8000';

  Future<void> _testBackend() async {
    try {
      final response = await http.get(Uri.parse('$_backendUrl/health'));
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Backend: ${response.statusCode} ${response.body}')));
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gagal konek backend: $e')));
    }
  }

  String _buildAudioUrl(String rawUrl) {
    String audioUrl = rawUrl.trim();
    if (audioUrl.startsWith('http://') || audioUrl.startsWith('https://')) return audioUrl;
    if (audioUrl.startsWith('/')) return '$_backendUrl$audioUrl';
    return '$_backendUrl/$audioUrl';
  }

  Future<void> _playAudio() async {
    if (_audioUrl == null || _audioUrl!.trim().isEmpty) return;
    try {
      final audioUrl = _buildAudioUrl(_audioUrl!);
      await _audioPlayer.stop();
      await _audioPlayer.play(UrlSource(audioUrl));
      if (mounted) setState(() => _isPlayingAudio = true);
    } catch (e) {
      if (mounted) {
        setState(() => _isPlayingAudio = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gagal memutar audio:\n$e')));
      }
    }
  }

  Future<void> _stopAudio() async {
    try {
      await _audioPlayer.stop();
      if (mounted) setState(() => _isPlayingAudio = false);
    } catch (_) {}
  }

  Future<void> _sendVideoToAI() async {
    if (_videoPath == null || _isProcessing) return;

    setState(() {
      _isProcessing = true;
      _sentence = null;
      _words = [];
      _audioUrl = null;
      _isPlayingAudio = false;
    });

    try {
      final file = File(_videoPath!);
      if (!await file.exists()) throw Exception('File video tidak ditemukan.');

      final request = http.MultipartRequest('POST', Uri.parse('$_backendUrl/translate/video'));
      request.files.add(await http.MultipartFile.fromPath('video', _videoPath!));
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw Exception('Status ${response.statusCode}: ${response.body}');
      }

      final dynamic decoded = jsonDecode(response.body);
      if (decoded is! Map<String, dynamic>) throw Exception('Format response tidak valid.');
      final data = decoded;

      String? resultSentence = data['sentence']?.toString();

      if (!mounted) return;
      setState(() {
        _sentence = resultSentence;
        _words = data['words'] is List ? data['words'] as List<dynamic> : [];

        final rawAudioUrl = data['audio_url'];
        if (rawAudioUrl != null && rawAudioUrl.toString().trim().isNotEmpty && rawAudioUrl.toString().toLowerCase() != 'null') {
          _audioUrl = rawAudioUrl.toString().trim();
        }
        _isProcessing = false;
      });

      if (resultSentence != null && resultSentence.trim().isNotEmpty) {
        try {
          final prefs = await SharedPreferences.getInstance();
          final historyList = prefs.getStringList('translation_history') ?? [];
          final newEntry = jsonEncode({
            'sentence': resultSentence,
            'timestamp': DateTime.now().toIso8601String(),
          });
          historyList.insert(0, newEntry);
          await prefs.setStringList('translation_history', historyList);
        } catch (e) {
          debugPrint('Gagal menyimpan riwayat: $e');
        }
      }

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Video berhasil diproses oleh AI.'), duration: Duration(seconds: 4)),
      );
    } catch (e) {
      if (mounted) {
        setState(() => _isProcessing = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gagal memproses: $e')));
      }
    }
  }

  @override
  void initState() {
    super.initState();
    _audioPlayer.onPlayerStateChanged.listen((PlayerState state) {
      if (mounted) setState(() => _isPlayingAudio = state == PlayerState.playing);
    });
    _initializeCamera();
  }

  // --- FUNGSI MENGINISIALISASI KAMERA BERDASARKAN INDEKS ---
  Future<void> _initializeCamera() async {
    _controller = CameraController(
        widget.cameras[_selectedCameraIndex],
        ResolutionPreset.medium,
        enableAudio: false
    );
    try {
      await _controller.initialize();
      await _controller.prepareForVideoRecording();
      if (mounted) setState(() => _isInitialized = true);
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Kamera error: $e')));
    }
  }

  // --- FUNGSI BARU UNTUK SWITCH KAMERA ---
  Future<void> _switchCamera() async {
    // Jangan izinkan ganti kamera saat merekam/memproses atau jika kamera cuma ada 1
    if (_isRecording || _isProcessing || widget.cameras.length < 2) return;

    setState(() {
      _isInitialized = false; // Tampilkan loading sebentar
    });

    await _controller.dispose(); // Matikan kamera yang aktif

    // Ganti indeks (misal: dari 0 ke 1, atau dari 1 ke 0)
    setState(() {
      _selectedCameraIndex = (_selectedCameraIndex + 1) % widget.cameras.length;
    });

    await _initializeCamera(); // Hidupkan kamera yang baru
  }

  Future<void> _startRecording() async {
    if (!_isInitialized || _isProcessing || _controller.value.isRecordingVideo) return;
    try {
      await _audioPlayer.stop();
      if (mounted) setState(() => _isPlayingAudio = false);

      await _controller.prepareForVideoRecording();
      await _controller.startVideoRecording();

      if (mounted) {
        setState(() {
          _isRecording = true;
          _isProcessing = false;
          _videoPath = null;
          _videoSize = null;
          _sentence = null;
          _words = [];
          _audioUrl = null;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isRecording = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gagal mulai rekam: $e')));
      }
    }
  }

  Future<void> _stopRecording() async {
    if (!_isInitialized || _isProcessing || !_controller.value.isRecordingVideo) return;
    setState(() => _isProcessing = true);
    try {
      final video = await _controller.stopVideoRecording();
      final size = await video.length();
      if (mounted) {
        setState(() {
          _isRecording = false;
          _isProcessing = false;
          _videoPath = video.path;
          _videoSize = size;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isRecording = false;
          _isProcessing = false;
        });
      }
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: const Text(
          'Rekam Bahasa Isyarat',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        elevation: 0,
        backgroundColor: Colors.blue.shade700,
        foregroundColor: Colors.white,
        actions: [
          // --- TOMBOL SWITCH KAMERA (Hanya muncul jika kamera > 1) ---
          if (widget.cameras.length > 1)
            IconButton(
              icon: const Icon(Icons.flip_camera_android),
              tooltip: 'Tukar Kamera Depan/Belakang',
              onPressed: (_isRecording || _isProcessing) ? null : _switchCamera,
            ),
          IconButton(
            icon: const Icon(Icons.cloud_sync),
            tooltip: 'Test Backend',
            onPressed: _isProcessing ? null : _testBackend,
          ),
        ],
      ),
      body: !_isInitialized
          ? const Center(child: CircularProgressIndicator())
          : Column(
        children: [
          Container(
            height: MediaQuery.of(context).size.height * 0.4,
            width: double.infinity,
            color: Colors.black,
            child: ClipRect(
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Builder(
                    builder: (context) {
                      final screenWidth = MediaQuery.of(context).size.width;
                      double ratio = _controller.value.aspectRatio;

                      if (ratio > 1.0) {
                        ratio = 1.0 / ratio;
                      }

                      return FittedBox(
                        fit: BoxFit.cover,
                        child: SizedBox(
                          width: screenWidth,
                          height: screenWidth / ratio,
                          child: CameraPreview(_controller),
                        ),
                      );
                    },
                  ),
                  if (_isRecording)
                    Positioned(
                      top: 20,
                      left: 20,
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: Colors.red.withOpacity(0.9),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.fiber_manual_record, color: Colors.white, size: 14),
                            SizedBox(width: 6),
                            Text('MEREKAM', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                    ),
                  if (_isProcessing)
                    Container(
                      color: Colors.black54,
                      child: const Center(child: CircularProgressIndicator(color: Colors.white)),
                    ),
                ],
              ),
            ),
          ),
          Expanded(
            child: Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(topLeft: Radius.circular(24), topRight: Radius.circular(24)),
                boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 10, offset: Offset(0, -2))],
              ),
              child: Column(
                children: [
                  Expanded(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.all(20),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          if (_videoPath != null) ...[
                            const Icon(Icons.check_circle, color: Colors.green, size: 40),
                            const SizedBox(height: 10),
                            const Text('Video siap diproses', textAlign: TextAlign.center, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Colors.green)),
                            const SizedBox(height: 20),
                          ],

                          if (_sentence != null) ...[
                            Container(
                              padding: const EdgeInsets.all(20),
                              decoration: BoxDecoration(
                                color: Colors.blue.shade50,
                                borderRadius: BorderRadius.circular(16),
                                border: Border.all(color: Colors.blue.shade100),
                              ),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Row(
                                    children: [
                                      Icon(Icons.translate, color: Colors.blue),
                                      SizedBox(width: 8),
                                      Text('Hasil Terjemahan', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.blue)),
                                    ],
                                  ),
                                  const SizedBox(height: 15),
                                  Text(_sentence!, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.black87)),
                                  const SizedBox(height: 15),
                                  const Divider(),
                                  const SizedBox(height: 10),
                                  if (_words.isNotEmpty)
                                    Wrap(
                                      spacing: 8,
                                      children: _words.map((item) {
                                        if (item is Map) {
                                          return Chip(
                                            avatar: const Icon(Icons.check_circle, size: 16, color: Colors.green),
                                            label: Text(item['word']?.toString() ?? '-'),
                                            backgroundColor: Colors.white,
                                            side: BorderSide(color: Colors.grey.shade300),
                                          );
                                        }
                                        return Text(item.toString());
                                      }).toList(),
                                    ),
                                ],
                              ),
                            ),
                            const SizedBox(height: 20),

                            if (_audioUrl != null && _audioUrl!.trim().isNotEmpty) ...[
                              Container(
                                padding: const EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(16),
                                  boxShadow: [BoxShadow(color: Colors.grey.shade200, blurRadius: 10, spreadRadius: 1)],
                                ),
                                child: Column(
                                  children: [
                                    const Text('Suara Tersedia', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.grey)),
                                    const SizedBox(height: 12),
                                    SizedBox(
                                      width: double.infinity,
                                      height: 55,
                                      child: ElevatedButton.icon(
                                        onPressed: _isPlayingAudio ? _stopAudio : _playAudio,
                                        icon: Icon(_isPlayingAudio ? Icons.stop : Icons.volume_up, size: 28),
                                        label: Text(_isPlayingAudio ? 'HENTIKAN' : 'DENGARKAN', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: _isPlayingAudio ? Colors.red : Colors.blue.shade600,
                                          foregroundColor: Colors.white,
                                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ]
                          ],
                        ],
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.fromLTRB(20, 15, 20, 25),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border(top: BorderSide(color: Colors.grey.shade200)),
                    ),
                    child: SafeArea(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (_videoPath != null && _sentence == null) ...[
                            SizedBox(
                              width: double.infinity,
                              height: 55,
                              child: ElevatedButton.icon(
                                onPressed: _isProcessing ? null : _sendVideoToAI,
                                icon: const Icon(Icons.auto_awesome),
                                label: Text(
                                  _isProcessing ? 'SEDANG MEMPROSES...' : 'KIRIM KE AI',
                                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                                ),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.purple.shade600,
                                  foregroundColor: Colors.white,
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                ),
                              ),
                            ),
                            const SizedBox(height: 12),
                          ],
                          SizedBox(
                            width: double.infinity,
                            height: 60,
                            child: ElevatedButton.icon(
                              onPressed: _isProcessing ? null : (_isRecording ? _stopRecording : _startRecording),
                              icon: Icon(_isRecording ? Icons.stop_circle : Icons.videocam, size: 30),
                              label: Text(
                                _isProcessing ? 'MOHON TUNGGU...' : (_isRecording ? 'HENTIKAN REKAMAN' : 'MULAI REKAM ISYARAT'),
                                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: _isRecording ? Colors.red : Colors.blue.shade800,
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                                elevation: 3,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ============================================================
// HISTORY SCREEN
// ============================================================

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<Map<String, dynamic>> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final historyList = prefs.getStringList('translation_history') ?? [];

      if (!mounted) return;
      setState(() {
        _history = historyList
            .map((item) => jsonDecode(item) as Map<String, dynamic>)
            .toList();
        _isLoading = false;
      });
    } catch (e) {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('translation_history');

    if (!mounted) return;
    setState(() {
      _history = [];
    });

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Riwayat berhasil dihapus.')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Riwayat Terjemahan'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_outline),
            tooltip: 'Hapus Semua Riwayat',
            onPressed: _history.isEmpty ? null : _clearHistory,
          )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _history.isEmpty
          ? Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.history, size: 80, color: Colors.grey.shade300),
            const SizedBox(height: 16),
            Text(
              'Belum ada riwayat terjemahan.',
              style: TextStyle(color: Colors.grey.shade600, fontSize: 16),
            ),
          ],
        ),
      )
          : ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _history.length,
        itemBuilder: (context, index) {
          final item = _history[index];
          final date = DateTime.tryParse(item['timestamp'] ?? '');

          String formattedDate = '-';
          if (date != null) {
            formattedDate = '${date.day}/${date.month}/${date.year} ${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}';
          }

          return Card(
            elevation: 2,
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: Colors.blue.shade50,
                child: const Icon(Icons.translate, color: Colors.blue),
              ),
              title: Text(
                item['sentence'] ?? '',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(formattedDate),
              ),
            ),
          );
        },
      ),
    );
  }
}