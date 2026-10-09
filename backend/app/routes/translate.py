from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
import tempfile
import os
import sys
import shutil
import threading
from datetime import datetime

router = APIRouter()

# Hanya satu video diproses pada satu waktu (RAM server dipakai bersama kelompok lain)
_PROSES_LOCK = threading.Lock()

# Tambahkan path ai_engine
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ai_engine'))

# Muat model saat server menyala (bukan saat rekaman pertama), supaya versi model
# dan error pemuatan langsung terlihat di terminal.
try:
    import pipeline  # noqa: F401
except Exception as e:
    print(f"[PERINGATAN] Model belum bisa dimuat saat startup: {e}")

# Salinan video yang dikirim aplikasi disimpan di backend/debug_videos untuk diperiksa
# kalau prediksinya salah. Matikan dengan environment variable SIMPAN_VIDEO_DEBUG=0.
DEBUG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'debug_videos')


def _simpan_video_debug(path, hasil):
    if os.environ.get("SIMPAN_VIDEO_DEBUG", "1") == "0":
        return
    try:
        os.makedirs(DEBUG_DIR, exist_ok=True)
        label = hasil.get("kata") or "gagal"
        nama = f"{datetime.now():%Y%m%d_%H%M%S}_{label}.mp4"
        shutil.copyfile(path, os.path.join(DEBUG_DIR, nama))
    except Exception as e:
        print(f"Gagal menyimpan video debug: {e}")

@router.post("/translate/video")
async def translate_video(video: UploadFile = File(...)):
    """
    Endpoint utama: terima video isyarat, kembalikan teks + kalimat + audio
    """
    # Validasi format file
    if not video.filename.endswith('.mp4'):
        raise HTTPException(status_code=400, detail="Hanya file MP4 yang diterima")

    # Simpan video sementara
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        content = await video.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        from pipeline import full_pipeline

        def _jalankan():
            with _PROSES_LOCK:
                return full_pipeline(tmp_path)

        # Proses berat dijalankan di thread terpisah supaya server (/health dll) tetap responsif
        hasil = await run_in_threadpool(_jalankan)
        _simpan_video_debug(tmp_path, hasil)

        if "error" in hasil:
            raise HTTPException(status_code=422, detail=hasil["error"])

        # ===============================================================
        # PERBAIKAN: FORMAT DATA DISESUAIKAN DENGAN PERMINTAAN FLUTTER
        # ===============================================================
        
        # 1. Flutter meminta 'words' berupa List berisi object kata & confidence
        words_formatted = [
            {
                "word": hasil["kata"],
                "confidence": hasil["confidence"]
            }
        ]

        # 2. Ambil hanya nama filenya saja (misal: "output_Siang.mp3") 
        # dari audio_path, lalu gabungkan dengan rute /audio/
        nama_file_audio = os.path.basename(hasil["audio_path"])
        audio_url_formatted = f"/audio/{nama_file_audio}"

        # 3. Kembalikan menggunakan keys bahasa inggris persis seperti di main.dart
        return {
            "success": True,
            "words": words_formatted,
            "sentence": hasil["kalimat"],
            "audio_url": audio_url_formatted
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc() # <--- Tambahan untuk mencetak detail error di terminal
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Hapus file temporary
        if os.path.exists(tmp_path):
            os.remove(tmp_path)