"""
bisindo_preprocess.py

Modul ini dipakai SAMA PERSIS di dua tempat:
  1. saat training (Colab)            -> train_v3_colab.py
  2. saat inferensi (ai_engine)       -> pipeline.py

Input  : urutan keypoint MediaPipe hanya dari frame yang tangannya terdeteksi,
         bentuk (n_frame, 63) = 21 titik x (x, y, z).
Output : fitur bentuk (30, 66).

Ide utamanya:
  - Bentuk tangan dihitung relatif terhadap pergelangan (landmark 0) dan
    dibagi ukuran tangan, jadi tidak lagi bergantung pada posisi tangan di
    frame, jarak ke kamera, atau siapa yang berisyarat.
  - Gerak tangan tetap dipertahankan lewat 3 fitur lintasan pergelangan.
  - 30 frame diambil merata dari SELURUH gerakan, bukan 30 frame pertama.
"""
import numpy as np

SEQUENCE_LEN = 30
N_FEATURES = 66  # 63 bentuk tangan + 3 lintasan pergelangan

WRIST = 0
MIDDLE_MCP = 9


def sample_sequence(seq, target=SEQUENCE_LEN, rng=None):
    """Ambil `target` frame dari seluruh urutan.

    rng=None  -> deterministik (untuk inferensi dan validasi)
    rng=Generator -> titik acak per segmen (untuk augmentasi saat training)
    """
    seq = np.asarray(seq, dtype=np.float32)
    n = len(seq)
    if n == 0:
        raise ValueError("urutan keypoint kosong")

    if rng is None:
        idx = np.linspace(0, n - 1, target).round().astype(int)
    else:
        edges = np.linspace(0, n, target + 1)
        lo = np.floor(edges[:-1]).astype(int)
        hi = np.minimum(np.maximum(np.ceil(edges[1:]).astype(int), lo + 1), n)
        idx = np.array([rng.integers(a, b) for a, b in zip(lo, hi)])
    return seq[idx]


def extract_features(seq):
    """(30, 63) -> (30, 66): bentuk tangan ternormalisasi + lintasan pergelangan."""
    pts = np.asarray(seq, dtype=np.float32).reshape(-1, 21, 3)
    wrist = pts[:, WRIST, :]

    # ukuran tangan: jarak pergelangan ke pangkal jari tengah, median 1 sekuens
    size = np.linalg.norm((pts[:, MIDDLE_MCP, :2] - wrist[:, :2]), axis=1)
    size = max(float(np.median(size)), 1e-4)

    shape = (pts - wrist[:, None, :]) / size            # (n, 21, 3)
    traj = (wrist - wrist.mean(axis=0, keepdims=True)) / size  # (n, 3)

    return np.concatenate([shape.reshape(len(pts), 63), traj], axis=1).astype(np.float32)


def augment(seq, rng):
    """Augmentasi satu video mentah (n, 63) -> (m, 63). Hanya untuk training."""
    pts = np.asarray(seq, dtype=np.float32).reshape(-1, 21, 3).copy()
    n = len(pts)

    # 1. potong sedikit awal/akhir (video dataset dan video HP beda panjang)
    cut = int(n * 0.15)
    if cut > 0 and n - 2 * cut >= 8:
        a, b = rng.integers(0, cut + 1), rng.integers(0, cut + 1)
        pts = pts[a:n - b]

    # 2. mirror horizontal (kamera depan HP menghasilkan video terbalik)
    if rng.random() < 0.5:
        pts[:, :, 0] = 1.0 - pts[:, :, 0]

    # 3. skala x/y berbeda (rasio video portrait vs landscape)
    sx, sy = rng.uniform(0.8, 1.25, size=2)
    pts[:, :, 0] = (pts[:, :, 0] - 0.5) * sx + 0.5
    pts[:, :, 1] = (pts[:, :, 1] - 0.5) * sy + 0.5

    # 4. rotasi kecil di bidang gambar
    th = np.deg2rad(rng.uniform(-15, 15))
    c, s = np.cos(th), np.sin(th)
    x, y = pts[:, :, 0] - 0.5, pts[:, :, 1] - 0.5
    pts[:, :, 0] = c * x - s * y + 0.5
    pts[:, :, 1] = s * x + c * y + 0.5

    # 5. noise kecil
    pts += rng.normal(0, 0.004, pts.shape).astype(np.float32)

    return pts.reshape(len(pts), 63)