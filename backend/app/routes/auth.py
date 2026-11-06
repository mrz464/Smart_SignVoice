"""
Endpoint login dan registrasi.

POST /auth/register  -> buat akun baru (peran: pengguna)
POST /auth/login     -> tukar email + password dengan token
GET  /auth/me        -> data akun yang sedang login
"""
import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app import database
from app.security import buat_token, cek_password, hash_password, user_saat_ini

router = APIRouter(prefix="/auth")

POLA_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PANJANG_MIN_PASSWORD = 6


class RegisterInput(BaseModel):
    nama: str = ""
    email: str = ""
    password: str = ""


class LoginInput(BaseModel):
    email: str = ""
    password: str = ""


def _data_user(user):
    return {"id": user["id"], "nama": user["nama"], "email": user["email"], "role": user["role"]}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterInput):
    nama = data.nama.strip()
    email = data.email.strip().lower()
    password = data.password

    if not nama or not email or not password:
        raise HTTPException(status_code=422, detail="Nama, email, dan password wajib diisi.")
    if len(nama) > 100:
        raise HTTPException(status_code=422, detail="Nama maksimal 100 karakter.")
    if not POLA_EMAIL.match(email):
        raise HTTPException(status_code=422, detail="Format email tidak valid. Contoh: nama@email.com")
    if len(password) < PANJANG_MIN_PASSWORD:
        raise HTTPException(status_code=422, detail=f"Password minimal {PANJANG_MIN_PASSWORD} karakter.")
    if database.cari_user_email(email):
        raise HTTPException(status_code=409, detail="Email sudah terdaftar. Silakan login atau pakai email lain.")

    user_id = database.buat_user(nama, email, hash_password(password), database.ROLE_PENGGUNA)
    user = database.cari_user_id(user_id)
    return {"message": "Registrasi berhasil. Silakan login.", "user": _data_user(user)}


@router.post("/login")
def login(data: LoginInput):
    email = data.email.strip().lower()
    password = data.password

    if not email or not password:
        raise HTTPException(status_code=422, detail="Email dan password wajib diisi.")

    user = database.cari_user_email(email)
    # Pesan sengaja disamakan, supaya orang lain tidak bisa menebak email mana yang terdaftar
    if user is None or not cek_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Email atau password salah.")

    return {
        "access_token": buat_token(user["id"], user["role"]),
        "token_type": "bearer",
        "user": _data_user(user),
    }


@router.get("/me")
def me(user=Depends(user_saat_ini)):
    return _data_user(user)
