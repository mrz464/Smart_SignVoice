import cv2
import mediapipe as mp
import numpy as np


# ============================================================
# KONFIGURASI
# ============================================================

MODEL_PATH = "ai_engine/models/hand_landmarker.task"

SEQUENCE_LENGTH = 30
FEATURES_PER_FRAME = 63


# ============================================================
# MEDIA PIPE HAND LANDMARKER
# ============================================================

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,

    # Sama seperti konfigurasi training Rendi
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


# ============================================================
# EKSTRAKSI KEYPOINT DARI SATU FRAME
# ============================================================

def extract_keypoints_from_frame(frame, landmarker):
    """
    Mengambil 21 landmark tangan dari satu frame.

    Output:
        numpy array shape (63,)
        21 landmark × 3 koordinat:
        x, y, z

    Jika tangan tidak terdeteksi:
        return None
    """

    # OpenCV menggunakan BGR
    # MediaPipe menggunakan RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Buat MediaPipe Image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Deteksi tangan
    result = landmarker.detect(mp_image)

    # Training Rendi:
    # frame tanpa tangan TIDAK dimasukkan
    if not result.hand_landmarks:
        return None

    # Ambil tangan pertama
    hand = result.hand_landmarks[0]

    keypoints = []

    # 21 landmark × 3 = 63 fitur
    for landmark in hand:
        keypoints.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    return np.array(
        keypoints,
        dtype=np.float32
    )


# ============================================================
# EKSTRAKSI VIDEO
# ============================================================

def extract_video_keypoints(
    video_path,
    sequence_length=SEQUENCE_LENGTH
):
    """
    Mengikuti preprocessing training Rendi.

    Proses:
        Video
        ↓
        baca frame secara berurutan
        ↓
        deteksi tangan
        ↓
        hanya frame yang terdeteksi disimpan
        ↓
        ambil maksimal 30 frame pertama
        ↓
        jika kurang dari 30 → padding nol

    Output:
        shape (30, 63)
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(
            f"Tidak dapat membuka video: {video_path}"
        )

    frames = []

    # Buat MediaPipe Hand Landmarker
    landmarker = (
        mp.tasks.vision.HandLandmarker
        .create_from_options(options)
    )

    try:

        while len(frames) < sequence_length:

            ret, frame = cap.read()

            if not ret:
                break

            # Ekstraksi keypoints
            keypoints = extract_keypoints_from_frame(
                frame,
                landmarker
            )

            # Hanya simpan jika tangan terdeteksi
            if keypoints is not None:

                frames.append(keypoints)

    finally:

        cap.release()
        landmarker.close()

    # ========================================================
    # PADDING
    # ========================================================

    while len(frames) < sequence_length:

        frames.append(
            np.zeros(
                FEATURES_PER_FRAME,
                dtype=np.float32
            )
        )

    # ========================================================
    # HASIL AKHIR
    # ========================================================

    result = np.array(
        frames[:sequence_length],
        dtype=np.float32
    )

    return result