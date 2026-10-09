import os
import json
import time
import threading
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key dari environment / .env
load_dotenv()

# Batas waktu satu panggilan Gemini (milidetik). Minimum yang diizinkan Google: 10000.
GEMINI_TIMEOUT_MS = 10000

# Nama model bisa diganti lewat .env: GEMINI_MODEL=nama-model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# GEMINI_AKTIF=0 di .env untuk mematikan Gemini sepenuhnya (pakai kalimat bawaan saja)
GEMINI_AKTIF = os.getenv("GEMINI_AKTIF", "1") != "0"

# Setelah kena rate limit / quota, Gemini diistirahatkan selama ini (detik)
ISTIRAHAT_SETELAH_429 = 600

# Kalimat bawaan untuk 32 kata. Dipakai langsung sehingga pengguna tidak menunggu
# Gemini. Gemini memperbagusnya di latar belakang dan hasilnya disimpan di cache.
KALIMAT_BAWAAN = {
    "Air": "Saya ingin minum air.",
    "Apa": "Apa itu?",
    "Bagaimana": "Bagaimana caranya?",
    "Belajar": "Saya sedang belajar.",
    "Berangkat": "Saya akan berangkat sekarang.",
    "Cari": "Saya sedang mencari sesuatu.",
    "Datang": "Dia sudah datang.",
    "Dengar": "Saya mendengarkan.",
    "Di_mana": "Di mana tempatnya?",
    "Hari": "Selamat menjalani hari ini.",
    "Hijau": "Warnanya hijau.",
    "Hitam": "Warnanya hitam.",
    "Ingat": "Saya ingat.",
    "Kapan": "Kapan waktunya?",
    "Keluarga": "Ini keluarga saya.",
    "Kuning": "Warnanya kuning.",
    "Lagi": "Tolong ulangi lagi.",
    "Maaf": "Maaf, saya minta maaf.",
    "Makan": "Saya ingin makan.",
    "Malam": "Selamat malam.",
    "Mengapa": "Mengapa begitu?",
    "Merah": "Warnanya merah.",
    "Motor": "Saya naik motor.",
    "Pagi": "Selamat pagi.",
    "Rumah": "Saya ada di rumah.",
    "Saya": "Ini saya.",
    "Siang": "Selamat siang.",
    "Siapa": "Siapa itu?",
    "Sore": "Selamat sore.",
    "Teman": "Dia teman saya.",
    "Terima_kasih": "Terima kasih.",
    "Tuli": "Saya tuli.",
}

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kalimat_cache.json")
_cache_lock = threading.Lock()
_sedang_diproses = set()
_istirahat_sampai = 0.0


def _muat_cache():
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _simpan_cache(cache):
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Gagal menyimpan cache kalimat: {e}")


def _buat_prompt(input_text):
    return f"""
Kamu adalah modul pemrosesan bahasa untuk aplikasi BicaraUntukku.

Hasil pengenalan bahasa isyarat BISINDO:
"{input_text}"

Ubahlah kata tersebut menjadi kalimat bahasa Indonesia
yang natural dan sederhana.

Aturan:
- Gunakan bahasa Indonesia yang baik dan benar.
- Jangan menjelaskan prosesnya.
- Jangan memberikan tanda kutip pada hasil.
- Jika input hanya satu kata, buat kalimat pendek yang sesuai.
- Jangan menambahkan informasi yang tidak diperlukan.
- Pertahankan makna dari kata hasil pengenalan.
- Jangan mengubah makna kata.

Hasil:
"""


def _panggil_gemini(input_text):
    """Satu kali panggilan Gemini. Mengembalikan kalimat, atau None kalau gagal."""
    global _istirahat_sampai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY belum diatur, Gemini dilewati.")
        return None

    if time.time() < _istirahat_sampai:
        return None

    try:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=GEMINI_TIMEOUT_MS),
        )
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=_buat_prompt(input_text),
        )
        if response.text:
            return response.text.strip()
        return None

    except Exception as e:
        error_text = str(e)
        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            _istirahat_sampai = time.time() + ISTIRAHAT_SETELAH_429
            print("Quota / rate limit Gemini tercapai, Gemini diistirahatkan 10 menit.")
        else:
            print(f"Error Gemini: {error_text}")
        return None


def _perbagus_di_latar_belakang(input_text):
    """Minta Gemini membuat kalimat lalu simpan di cache untuk rekaman berikutnya."""
    with _cache_lock:
        if input_text in _sedang_diproses:
            return
        _sedang_diproses.add(input_text)

    def kerja():
        try:
            kalimat = _panggil_gemini(input_text)
            if kalimat:
                with _cache_lock:
                    cache = _muat_cache()
                    cache[input_text] = kalimat
                    _simpan_cache(cache)
                print(f"Gemini: kalimat untuk '{input_text}' disimpan ke cache.")
        finally:
            with _cache_lock:
                _sedang_diproses.discard(input_text)

    threading.Thread(target=kerja, daemon=True).start()


def generate_sentence(words):
    """
    Mengubah hasil prediksi kata/list kata BISINDO
    menjadi kalimat bahasa Indonesia yang natural.

    Urutan: cache Gemini -> kalimat bawaan (Gemini memperbagusnya di latar
    belakang) -> untuk beberapa kata sekaligus, panggil Gemini langsung.

    Args:
        words: string satu kata atau list kata
               contoh: "Saya" atau ["Saya", "Makan", "Air"]

    Returns:
        String kalimat Bahasa Indonesia
    """

    if isinstance(words, list):
        input_text = ", ".join(words)
    else:
        input_text = words

    # 1. Kalimat dari Gemini yang sudah tersimpan
    with _cache_lock:
        cache = _muat_cache()
    if input_text in cache:
        print(f"Kalimat diambil dari cache untuk '{input_text}'")
        return cache[input_text]

    # 2. Satu kata: pakai kalimat bawaan, Gemini memperbagus di latar belakang
    if input_text in KALIMAT_BAWAAN:
        if GEMINI_AKTIF:
            _perbagus_di_latar_belakang(input_text)
        print(f"Kalimat bawaan dipakai untuk '{input_text}'")
        return KALIMAT_BAWAAN[input_text]

    # 3. Gabungan beberapa kata: coba Gemini langsung, kalau gagal pakai input
    if GEMINI_AKTIF:
        kalimat = _panggil_gemini(input_text)
        if kalimat:
            return kalimat

    print("Gemini tidak tersedia, menggunakan hasil LSTM langsung.")
    return input_text


if __name__ == "__main__":

    print("=" * 50)
    print("TEST KALIMAT — BicaraUntukku")
    print("=" * 50)

    test_cases = [
        "Apa",
        "Saya",
        ["Saya", "Makan", "Air"],
        ["Terima_kasih", "Teman"],
    ]

    for test in test_cases:
        try:
            hasil = generate_sentence(test)
            input_str = test if isinstance(test, str) else ", ".join(test)
            print(f"Input  : {input_str}")
            print(f"Output : {hasil}")
            print("-" * 30)
        except Exception as e:
            print(f"ERROR: {e}")