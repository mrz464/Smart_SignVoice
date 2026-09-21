import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key dari .env
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
        raise ValueError("GEMINI_API_KEY belum diatur di file .env")

    # Handle input string atau list
    if isinstance(words, list):
        input_text = ', '.join(words)
    else:
        input_text = words

    genai.configure(api_key=api_key)

    prompt = f"""Kamu adalah modul pemrosesan bahasa untuk aplikasi BicaraUntukku.

Hasil pengenalan bahasa isyarat BISINDO: "{input_text}"

Ubahlah kata tersebut menjadi kalimat bahasa Indonesia yang natural dan sederhana.

Aturan:
- Gunakan bahasa Indonesia yang baik dan benar.
- Jangan menjelaskan prosesnya.
- Jangan memberikan tanda kutip pada hasil.
- Jika input hanya satu kata, buat kalimat pendek yang sesuai.
- Jangan menambahkan informasi yang tidak diperlukan.
- Pertahankan makna dari kata hasil pengenalan.

Hasil:"""

    # Retry otomatis kalau server Gemini sibuk
    max_retry = 3
    for i in range(max_retry):
        try:
            model = genai.GenerativeModel('gemini-3.6-flash')
            response = model.generate_content(prompt)

            if response.text:
                return response.text.strip()
            return input_text

        except Exception as e:
            if '503' in str(e) or 'UNAVAILABLE' in str(e):
                print(f"Gemini sibuk, retry {i+1}/{max_retry} dalam 5 detik...")
                time.sleep(5)
            else:
                print(f"Error Gemini: {e}")
                break

    # Fallback kalau semua retry gagal
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
            hasil     = generate_sentence(test)
            input_str = test if isinstance(test, str) else ', '.join(test)
            print(f"Input  : {input_str}")
            print(f"Output : {hasil}")
            print("-" * 30)
        except Exception as e:
            print(f"ERROR: {e}")