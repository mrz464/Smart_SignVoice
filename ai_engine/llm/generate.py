import os
import time
from dotenv import load_dotenv
from google import genai

# Load API key dari environment / .env
load_dotenv()


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

    # Buat client Gemini menggunakan API key
    client = genai.Client(api_key=api_key)

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

    # Retry otomatis jika Gemini sedang sibuk
    max_retry = 3

    for i in range(max_retry):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                return response.text.strip()

            return input_text

        except Exception as e:

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:
                print(
                    f"Gemini sedang sibuk, "
                    f"retry {i + 1}/{max_retry} dalam 5 detik..."
                )
                time.sleep(5)

            elif "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                print("Quota / rate limit Gemini tercapai.")
                break

            else:
                print(f"Error Gemini: {error_text}")
                break

    # Fallback kalau Gemini tidak tersedia
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
        ["Halo", "Nama", "Saya"],
        ["Terima_kasih", "Bantu"],
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