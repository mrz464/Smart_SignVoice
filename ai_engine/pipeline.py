import os
import sys
import numpy as np
import pickle
import tensorflow as tf
from dotenv import load_dotenv

load_dotenv()

# Tambahkan path ai_engine agar bisa import llm dan tts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ── Load model & scaler ──
MODEL_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend', 'app', 'ai_models', 'model_bisindo_v2.keras')
SCALER_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend', 'app', 'ai_models', 'scaler.pkl')
ID_KATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend', 'app', 'ai_models', 'id_to_kata.npy')

model      = tf.keras.models.load_model(MODEL_PATH)
scaler     = pickle.load(open(SCALER_PATH, 'rb'))
id_to_kata = np.load(ID_KATA_PATH, allow_pickle=True).item()

SEQUENCE_LEN = 30


def predict_gesture(keypoints_sequence):
    """
    Prediksi kata dari sequence keypoint tangan.

    Args:
        keypoints_sequence: numpy array shape (n_frames, 63)

    Returns:
        Tuple (label kata, confidence)
    """
    if len(keypoints_sequence) >= SEQUENCE_LEN:
        data = keypoints_sequence[:SEQUENCE_LEN]
    else:
        pad  = np.zeros((SEQUENCE_LEN - len(keypoints_sequence), 63))
        data = np.vstack([keypoints_sequence, pad])

    data_flat   = data.reshape(-1, 63)
    data_scaled = scaler.transform(data_flat).reshape(1, SEQUENCE_LEN, 63)

    pred       = model.predict(data_scaled, verbose=0)
    label_id   = np.argmax(pred)
    confidence = float(np.max(pred))

    return id_to_kata[label_id], confidence


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

    # Prediksi kata dari keypoint
    keypoints_array  = np.array(keypoints)
    kata, confidence = predict_gesture(keypoints_array)
    print(f"✅ Prediksi: {kata} ({confidence*100:.2f}%)")

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
        "audio_path" : audio_path
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