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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Hapus file temporary
        if os.path.exists(tmp_path):
            os.remove(tmp_path)