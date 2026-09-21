import numpy as np

from preprocessing.extract_keypoints import extract_video_keypoints


# ============================================================
# KONFIGURASI
# ============================================================

VIDEO_PATH = "ai_engine/test_video.mp4"
SEQUENCE_LENGTH = 30


# ============================================================
# MULAI EKSTRAKSI
# ============================================================

print("=" * 60)
print("TEST EKSTRAKSI KEYPOINTS BISINDO")
print("=" * 60)

print()
print("Video:", VIDEO_PATH)
print("Sequence length:", SEQUENCE_LENGTH)

print()
print("Mulai ekstraksi keypoints...")


# ============================================================
# EKSTRAKSI KEYPOINTS
# ============================================================

keypoints = extract_video_keypoints(
    VIDEO_PATH,
    sequence_length=SEQUENCE_LENGTH
)


# ============================================================
# HASIL EKSTRAKSI
# ============================================================

print()
print("=" * 60)
print("HASIL EKSTRAKSI")
print("=" * 60)

print("Shape:", keypoints.shape)
print("Jumlah frame:", len(keypoints))
print("Jumlah fitur per frame:", keypoints.shape[1])
print("Tipe data:", keypoints.dtype)


# ============================================================
# CEK FRAME
# ============================================================

print()
print("=" * 60)
print("CEK FRAME YANG MEMILIKI KEYPOINTS")
print("=" * 60)

jumlah_frame_terdeteksi = 0
jumlah_frame_kosong = 0

for i, frame in enumerate(keypoints):

    jumlah_nilai_nol = np.count_nonzero(frame == 0)

    if jumlah_nilai_nol < 63:

        jumlah_frame_terdeteksi += 1

        print(
            f"Frame {i}: "
            f"TERDETEKSI - "
            f"non-zero={63 - jumlah_nilai_nol}/63"
        )

    else:

        jumlah_frame_kosong += 1

        print(
            f"Frame {i}: "
            f"TIDAK TERDETEKSI"
        )


# ============================================================
# RINGKASAN DETEKSI
# ============================================================

print()
print("=" * 60)
print("RINGKASAN")
print("=" * 60)

print(
    "Frame terdeteksi:",
    jumlah_frame_terdeteksi
)

print(
    "Frame tidak terdeteksi:",
    jumlah_frame_kosong
)

print(
    "Total frame:",
    len(keypoints)
)


# ============================================================
# CEK BENTUK DATA UNTUK MODEL
# ============================================================

print()
print("=" * 60)
print("VALIDASI INPUT MODEL")
print("=" * 60)

expected_shape = (30, 63)

if keypoints.shape == expected_shape:

    print("Shape sesuai:", keypoints.shape)
    print("STATUS: BERHASIL")
    print("Data siap digunakan sebagai input model LSTM.")

else:

    print("Shape aktual :", keypoints.shape)
    print("Shape yang diharapkan:", expected_shape)
    print("STATUS: TIDAK SESUAI")


# ============================================================
# CONTOH DATA
# ============================================================

print()
print("=" * 60)
print("CONTOH DATA")
print("=" * 60)

print("5 nilai pertama frame pertama:")

print(keypoints[0][:5])


# ============================================================
# SELESAI
# ============================================================

print()
print("=" * 60)
print("SELESAI")
print("=" * 60)