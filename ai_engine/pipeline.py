import os
import sys
import numpy as np
import pickle
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

# Tambahkan path ai_engine agar bisa import llm dan tts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ── Load model ──
# Model v3 (fitur ternormalisasi, tanpa scaler) dipakai kalau file-nya ada.
# Kalau belum, otomatis kembali ke model v2 lama supaya aplikasi tetap jalan.
AI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend', 'app', 'ai_models')
V3_MODEL = os.path.join(AI_DIR, 'model_bisindo_v3.keras')
V3_LABEL = os.path.join(AI_DIR, 'id_to_kata_v3.npy')

SEQUENCE_LEN = 30
CONFIDENCE_THRESHOLD = 0.6   # di bawah ini dianggap "isyarat tidak dikenali"

# ── Pengaturan akurasi (boleh diubah) ──
# Kata yang TIDAK dijawab karena akurasinya rendah pada uji jujur (signer 4):
# Mengapa 0%, Siang 0%, Maaf 60%, Halo 80%. Hapus sebuah nama dari daftar ini
# kalau ingin mengaktifkannya lagi. Kosongkan ( set() ) untuk memakai semua kata.
KATA_DIKECUALIKAN = {"Mengapa", "Siang", "Maaf", "Halo"}

# Rekaman dengan tangan terdeteksi di frame lebih sedikit dari ini ditolak,
# karena terlalu sedikit data untuk ditebak dengan benar.
MIN_FRAME_TERDETEKSI = 20

if os.path.exists(V3_MODEL) and os.path.exists(V3_LABEL):
    from bisindo_preprocess import sample_sequence, extract_features
    MODEL_VERSION = 'v3'
    model      = tf.keras.models.load_model(V3_MODEL)
    scaler     = None
    id_to_kata = np.load(V3_LABEL, allow_pickle=True).item()
else:
    MODEL_VERSION = 'v2'
    model      = tf.keras.models.load_model(os.path.join(AI_DIR, 'model_bisindo_v2.keras'))
    scaler     = pickle.load(open(os.path.join(AI_DIR, 'scaler.pkl'), 'rb'))
    id_to_kata = np.load(os.path.join(AI_DIR, 'id_to_kata.npy'), allow_pickle=True).item()

ALLOWED_IDS = np.array([i for i, k in id_to_kata.items() if k not in KATA_DIKECUALIKAN])

print(f"Model BISINDO dipakai: {MODEL_VERSION}")
print(f"Kata aktif: {len(ALLOWED_IDS)} dari {len(id_to_kata)} (dikecualikan: {sorted(KATA_DIKECUALIKAN) or '-'})")


def predict_gesture(keypoints_sequence):
    """
    Prediksi kata dari sequence keypoint tangan.

    Args:
        keypoints_sequence: numpy array shape (n_frames, 63), hanya frame
                            yang tangannya terdeteksi

    Returns:
        Tuple (label kata, confidence, top3) dengan top3 berisi
        [(kata, confidence), ...] tiga tebakan teratas.
    """
    seq = np.asarray(keypoints_sequence, dtype=np.float32)

    if MODEL_VERSION == 'v3':
        # preprocessing SAMA PERSIS dengan saat training
        x = extract_features(sample_sequence(seq))[None]
    else:
        # jalur lama model v2: 30 frame pertama + pad nol + scaler
        if len(seq) >= SEQUENCE_LEN:
            data = seq[:SEQUENCE_LEN]
        else:
            data = np.vstack([seq, np.zeros((SEQUENCE_LEN - len(seq), 63))])
        x = scaler.transform(data.reshape(-1, 63)).reshape(1, SEQUENCE_LEN, 63)

    pred = model.predict(x, verbose=0)[0]
    order = np.argsort(pred)[::-1][:3]
    top3 = [(id_to_kata[int(i)], float(pred[i])) for i in order]

    # Jawaban hanya dipilih dari kata yang aktif. Probabilitasnya dipakai apa adanya
    # (tidak dinormalisasi ulang), jadi kalau model yakin pada kata yang dikecualikan,
    # probabilitas kata aktif terbaik kecil dan rekaman ditolak oleh ambang keyakinan.
    best = int(ALLOWED_IDS[int(np.argmax(pred[ALLOWED_IDS]))])
    return id_to_kata[best], float(pred[best]), top3


def full_pipeline(video_path):
    """
    Pipeline lengkap: video → keypoint → kata → kalimat → audio

    Args:
        video_path: path ke file video MP4

    Returns:
        dict berisi kata, confidence, kalimat, dan path audio
    """
    import cv2
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    import urllib.request
    from llm.generate import generate_sentence
    from tts.speak import text_to_speech

    # Download model MediaPipe kalau belum ada
    model_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'hand_landmarker.task'
    )
    if not os.path.exists(model_path):
        print("Downloading MediaPipe model...")
        urllib.request.urlretrieve(
            'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
            model_path
        )
        print("✅ MediaPipe model downloaded!")

    # Setup MediaPipe Hand Landmarker
    base_options = python.BaseOptions(model_asset_path=model_path)
    options      = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    landmarker = vision.HandLandmarker.create_from_options(options)

    # Ekstrak keypoint dari video
    cap       = cv2.VideoCapture(video_path)
    keypoints = []

    print("Mengekstrak keypoint dari video...")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image  = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        hasil     = landmarker.detect(mp_image)

        if hasil.hand_landmarks:
            lm    = hasil.hand_landmarks[0]
            baris = []
            for titik in lm:
                baris.extend([titik.x, titik.y, titik.z])
            keypoints.append(baris)

    cap.release()

    if not keypoints:
        return {"error": "Tangan tidak terdeteksi di video"}

    print(f"✅ {len(keypoints)} frame terdeteksi")

    if len(keypoints) < MIN_FRAME_TERDETEKSI:
        return {"error": f"Tangan hanya terlihat di {len(keypoints)} frame (minimal {MIN_FRAME_TERDETEKSI}). "
                         "Pastikan tangan terlihat penuh di layar dengan cahaya cukup, lalu rekam ulang."}

    # Prediksi kata dari keypoint
    keypoints_array  = np.array(keypoints)
    kata, confidence, top3 = predict_gesture(keypoints_array)
    top3_teks = ", ".join(f"{k} {c*100:.0f}%" for k, c in top3)
    print(f"✅ Prediksi: {kata} ({confidence*100:.2f}%) | Top-3: {top3_teks}")

    # Jangan paksakan tebakan kalau model sendiri tidak yakin
    if confidence < CONFIDENCE_THRESHOLD:
        return {"error": f"Isyarat tidak dikenali dengan yakin (tebakan terdekat: {top3_teks}). Coba rekam ulang."}

    # Rangkai kalimat dengan LLM Gemini
    print("Merangkai kalimat dengan Gemini...")
    kalimat = generate_sentence(kata)
    print(f"✅ Kalimat: {kalimat}")

    # Generate audio dengan gTTS
    audio_path = f'output_{kata}.mp3'
    text_to_speech(kalimat, audio_path)

    return {
        "kata"       : kata,
        "confidence" : f"{confidence*100:.2f}%",
        "kalimat"    : kalimat,
        "audio_path" : audio_path,
        "top3"       : top3_teks
    }


if __name__ == "__main__":
    VIDEO_TEST = input("Masukkan path video test: ")

    if not os.path.exists(VIDEO_TEST):
        print(f"❌ File tidak ditemukan: {VIDEO_TEST}")
        sys.exit(1)

    print("\nMemproses video...")
    hasil = full_pipeline(VIDEO_TEST)

    print("\n" + "=" * 50)
    print("HASIL PIPELINE LENGKAP")
    print("=" * 50)
    if "error" in hasil:
        print(f"❌ Error: {hasil['error']}")
    else:
        for key, val in hasil.items():
            print(f"{key:<12}: {val}")