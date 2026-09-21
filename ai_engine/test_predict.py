import numpy as np

from preprocessing.extract_keypoints import extract_video_keypoints
from classifier.predict import predict_keypoints

# ============================================================
# KONFIGURASI
# ============================================================

VIDEO_PATH = "ai_engine/test_video.mp4"


# ============================================================
# MULAI
# ============================================================

print("=" * 60)
print("TEST END-TO-END AI ENGINE BISINDO")
print("=" * 60)

print()
print("Video:", VIDEO_PATH)


# ============================================================
# TAHAP 1 - EKSTRAKSI KEYPOINTS
# ============================================================

print()
print("=" * 60)
print("TAHAP 1 - EKSTRAKSI KEYPOINTS")
print("=" * 60)

keypoints = extract_video_keypoints(
    VIDEO_PATH,
    sequence_length=30
)

print("Shape keypoints:", keypoints.shape)


# ============================================================
# VALIDASI SHAPE
# ============================================================

if keypoints.shape != (30, 63):

    raise ValueError(
        f"Shape tidak sesuai: {keypoints.shape}"
    )

print("Shape sesuai dengan input model.")


# ============================================================
# TAHAP 2 - PREDIKSI LSTM
# ============================================================

print()
print("=" * 60)
print("TAHAP 2 - PREDIKSI LSTM")
print("=" * 60)

predicted_id, predicted_word, confidence = predict_keypoints(
    keypoints
)


# ============================================================
# HASIL
# ============================================================

print()
print("=" * 60)
print("HASIL PREDIKSI")
print("=" * 60)

print("Predicted ID   :", predicted_id)
print("Predicted Word :", predicted_word)
print(
    "Confidence     :",
    f"{confidence * 100:.2f}%"
)


# ============================================================
# SELESAI
# ============================================================

print()
print("=" * 60)
print("SELESAI")
print("=" * 60)