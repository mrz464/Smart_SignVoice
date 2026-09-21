import pickle
import numpy as np
import tensorflow as tf


# ============================================================
# LOKASI MODEL
# ============================================================

MODEL_PATH = "backend/app/ai_models/model_bisindo_v2.keras"
SCALER_PATH = "backend/app/ai_models/scaler.pkl"
LABEL_PATH = "backend/app/ai_models/id_to_kata.npy"


# ============================================================
# LOAD MODEL
# ============================================================

print("Memuat model LSTM...")

model = tf.keras.models.load_model(
    MODEL_PATH
)

print("Model berhasil dimuat.")


# ============================================================
# LOAD SCALER
# ============================================================

print("Memuat scaler...")

with open(SCALER_PATH, "rb") as file:
    scaler = pickle.load(file)

print("Scaler berhasil dimuat.")


# ============================================================
# LOAD LABEL MAPPING
# ============================================================

print("Memuat label mapping...")

id_to_kata = np.load(
    LABEL_PATH,
    allow_pickle=True
).item()

print("Label mapping berhasil dimuat.")


# ============================================================
# FUNGSI PREDIKSI
# ============================================================

def predict_keypoints(keypoints):
    """
    Melakukan prediksi dari data keypoints.

    Input:
        keypoints -> shape (30, 63)

    Output:
        predicted_id
        predicted_word
        confidence
    """

    # Pastikan input berupa numpy array
    keypoints = np.asarray(
        keypoints,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # VALIDASI SHAPE
    # --------------------------------------------------------

    if keypoints.shape != (30, 63):

        raise ValueError(
            f"Shape input tidak sesuai: {keypoints.shape}. "
            "Model membutuhkan (30, 63)."
        )

    # --------------------------------------------------------
    # STANDARD SCALER
    # --------------------------------------------------------

    scaled = scaler.transform(
        keypoints
    )

    # Tambahkan batch dimension
    #
    # Sebelum:
    # (30, 63)
    #
    # Sesudah:
    # (1, 30, 63)

    model_input = np.expand_dims(
        scaled,
        axis=0
    )

    # --------------------------------------------------------
    # PREDIKSI MODEL
    # --------------------------------------------------------

    probabilities = model.predict(
        model_input,
        verbose=0
    )

    # Ambil ID dengan probabilitas tertinggi
    predicted_id = int(
        np.argmax(probabilities[0])
    )

    # Ambil confidence
    confidence = float(
        probabilities[0][predicted_id]
    )

    # Ambil nama kata
    predicted_word = id_to_kata[
        predicted_id
    ]

    return (
        predicted_id,
        predicted_word,
        confidence
    )