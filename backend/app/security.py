"""
Keamanan: hash password dan token login (JWT).

Kunci rahasia token diambil dari variabel JWT_SECRET di file .env backend.
Kalau belum diisi, server memakai kunci sementara (semua orang harus login ulang
setiap server di-restart). Isi JWT_SECRET untuk pemakaian sungguhan.
"""
import os
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import database

_pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

JWT_ALGORITHM = "HS256"
TOKEN_BERLAKU_HARI = 7

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    JWT_SECRET = secrets.token_urlsafe(32)
    print("[PERINGATAN] JWT_SECRET belum diatur di .env, memakai kunci sementara. "
          "Pengguna harus login ulang setiap server di-restart.")

_bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def cek_password(password: str, password_hash: str) -> bool:
    try:
        return _pwd.verify(password, password_hash)
    except Exception:
        return False


def buat_token(user_id: int, role: str) -> str:
    kedaluwarsa = datetime.now(timezone.utc) + timedelta(days=TOKEN_BERLAKU_HARI)
    data = {"sub": str(user_id), "role": role, "exp": kedaluwarsa}
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def user_saat_ini(cred: HTTPAuthorizationCredentials = Depends(_bearer)):
    """Dependency FastAPI: wajib login. Mengembalikan baris user dari database."""
    if cred is None or cred.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Silakan login terlebih dahulu.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        data = jwt.decode(cred.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(data.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesi login tidak valid atau sudah habis. Silakan login ulang.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = database.cari_user_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Akun tidak ditemukan. Silakan login ulang.",
        )
    return user


def wajib_guru(user=Depends(user_saat_ini)):
    """Dependency FastAPI: hanya untuk peran guru (dashboard)."""
    if user["role"] != database.ROLE_GURU:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Halaman ini hanya untuk akun guru.",
        )
    return user
