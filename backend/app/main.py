import os
from dotenv import load_dotenv

# Membangunkan file .env agar terbaca oleh seluruh sistem backend
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.routes.translate import router as translate_router
from app.routes.dashboard import router as dashboard_router  # BARU
from app.routes.auth import router as auth_router
from app.database import init_db

app = FastAPI(
    title="BicaraUntukku API",
    description="REST API untuk terjemah bahasa isyarat BISINDO",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Buat tabel pengguna dan akun awal kalau belum ada
init_db()

# Include routers
app.include_router(auth_router, tags=["Auth"])
app.include_router(translate_router, tags=["Translation"])
app.include_router(dashboard_router, tags=["Dashboard"])  # BARU

@app.get("/")
def root():
    return {"message": "BicaraUntukku API is running!"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

# =========================================================
# ENDPOINT BARU UNTUK AUDIO FLUTTER
# =========================================================
@app.get("/audio/{filename}")
async def get_audio(filename: str):
    # Hanya nama file saja (tanpa folder), supaya tidak bisa membaca file lain di server
    nama = os.path.basename(filename)
    if not nama.endswith(".mp3"):
        raise HTTPException(status_code=400, detail="Hanya file audio .mp3")
    if os.path.exists(nama):
        return FileResponse(nama, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="File audio tidak ditemukan")
