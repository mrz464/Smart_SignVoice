from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
import sys

router = APIRouter()

# Tambahkan path ai_engine
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'ai_engine'))

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
        hasil = full_pipeline(tmp_path)

        if "error" in hasil:
            raise HTTPException(status_code=422, detail=hasil["error"])

        return {
            "status"    : "success",
            "kata"      : hasil["kata"],
            "confidence": hasil["confidence"],
            "kalimat"   : hasil["kalimat"],
            "audio_path": hasil["audio_path"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Hapus file temporary
        if os.path.exists(tmp_path):
            os.remove(tmp_path)