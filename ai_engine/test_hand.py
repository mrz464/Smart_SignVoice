import cv2
import mediapipe as mp

VIDEO_PATH = "ai_engine/test_video.mp4"
MODEL_PATH = "ai_engine/models/hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Video tidak dapat dibuka.")
    landmarker.close()
    exit()

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Total frame video:", total_frames)
print("Mulai mengecek frame...")

# Ambil maksimal 10 frame yang tersebar sepanjang video
jumlah_test = min(10, total_frames)

if jumlah_test == 0:
    print("ERROR: Video tidak memiliki frame.")
    cap.release()
    landmarker.close()
    exit()

frame_indices = [
    int(i * (total_frames - 1) / max(jumlah_test - 1, 1))
    for i in range(jumlah_test)
]

berhasil = False

for nomor, target_frame in enumerate(frame_indices, start=1):

    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    ret, frame = cap.read()

    if not ret:
        print(f"Frame {target_frame}: gagal dibaca")
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    result = landmarker.detect(mp_image)

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        keypoints = []

        for landmark in hand:
            keypoints.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        print(
            f"Frame {target_frame}: "
            f"TANGAN TERDETEKSI - "
            f"landmark={len(hand)}, "
            f"fitur={len(keypoints)}"
        )

        if not berhasil:
            print("\nCONTOH 5 LANDMARK PERTAMA:")

            for i in range(5):
                print(
                    i,
                    "x=", round(keypoints[i * 3], 4),
                    "y=", round(keypoints[i * 3 + 1], 4),
                    "z=", round(keypoints[i * 3 + 2], 4)
                )

        berhasil = True

    else:
        print(f"Frame {target_frame}: tangan tidak terdeteksi")

cap.release()
landmarker.close()

print()

if berhasil:
    print("HASIL: MediaPipe berhasil mendeteksi tangan.")
    print("Format fitur: 21 landmark x 3 = 63 fitur")
else:
    print("HASIL: Tidak ada tangan yang terdeteksi pada 10 frame yang diuji.")