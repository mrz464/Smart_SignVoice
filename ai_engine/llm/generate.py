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

# Total waktu maksimal yang dihabiskan untuk Gemini per rekaman (detik).
# Lewat dari ini, langsung pakai kata asli supaya aplikasi tidak lama menunggu.
GEMINI_ANGGARAN_DETIK = 12

# Nama model bisa diganti lewat .env tanpa mengubah kode: GEMINI_MODEL=nama-model
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

# Kalimat yang sudah berhasil dibuat disimpan, jadi kata yang sama tidak perlu
# memanggil Gemini lagi (hanya ada 32 kata).
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kalimat_cache.json")
_cache_lock = threading.Lock()


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


def generate_sentence(words):
    """
    Mengubah hasil prediksi kata/list kata BISINDO
    menjadi kalimat bahasa Indonesia yang natural.

    Args:
        words: bisa string satu kata atau list kata
               contoh: "Saya" atau ["Saya", "Makan", "Air"]

    Returns:
        String kalimat natural Bahasa Indonesia
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY belum diatur di environment variable atau .env"
        )

    # Handle input string atau list
    if isinstance(words, list):
        input_text = ", ".join(words)
    else:
        input_text = words

    # Pakai kalimat yang sudah pernah dibuat
    with _cache_lock:
        cache = _muat_cache()
    if input_text in cache:
        print(f"Kalimat diambil dari cache untuk '{input_text}'")
        return cache[input_text]

    # Buat client Gemini menggunakan API key, dengan batas waktu tunggu
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=GEMINI_TIMEOUT_MS),
    )

    prompt = f"""
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

    mulai = time.time()
    max_retry = 2

    for i in range(max_retry):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if response.text:
                kalimat = response.text.strip()
                with _cache_lock:
                    cache = _muat_cache()
                    cache[input_text] = kalimat
                    _simpan_cache(cache)
                return kalimat

            return input_text

        except Exception as e:

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:
                sisa = GEMINI_ANGGARAN_DETIK - (time.time() - mulai)
                if i + 1 < max_retry and sisa > 4:
                    print(f"Gemini sedang sibuk, retry {i + 1}/{max_retry} dalam 1 detik...")
                    time.sleep(1)
                    continue
                print("Gemini sibuk dan waktu habis, pakai kata asli.")
                break

            elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print("Quota / rate limit Gemini tercapai.")
                break

            else:
                # Termasuk error waktu habis (timeout) -> langsung fallback
                print(f"Error Gemini: {error_text}")
                break

    # Fallback kalau Gemini tidak tersedia (tidak disimpan ke cache)
    print("Gemini tidak tersedia, menggunakan hasil LSTM langsung.")
    return input_text


if __name__ == "__main__":

    print("=" * 50)
    print("TEST GEMINI LLM — BicaraUntukku")
    print("=" * 50)

    test_cases = [
        "Apa",
        "Saya",
        ["Saya", "Makan", "Air"],
        ["Saya", "Belajar", "Rumah"],
        ["Terima_kasih", "Teman"],
    ]

    for test in test_cases:

        try:
            hasil = generate_sentence(test)

            input_str = (
                test
                if isinstance(test, str)
                else ", ".join(test)
            )

            print(f"Input  : {input_str}")
            print(f"Output : {hasil}")
            print("-" * 30)

        except Exception as e:
            print(f"ERROR: {e}")