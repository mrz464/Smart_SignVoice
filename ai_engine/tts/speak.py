from gtts import gTTS
import os

def text_to_speech(kalimat, output_path='output.mp3'):
    """Konversi teks ke file audio MP3"""
    tts = gTTS(text=kalimat, lang='id')
    tts.save(output_path)
    print(f"✅ Audio disimpan: {output_path}")
    return output_path

if __name__ == "__main__":
    test_kalimat = "Saya makan dan minum air."
    text_to_speech(test_kalimat, 'test_output.mp3')
    print(f"Kalimat: {test_kalimat}")