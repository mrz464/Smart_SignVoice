"""
Database pengguna BicaraUntukku (SQLite, satu file).

File database dibuat otomatis di backend/bicarauntukku.db saat server menyala.
Tidak perlu memasang server database terpisah.
"""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.environ.get(
    "BICARA_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bicarauntukku.db"),
)

# Peran yang dikenal sistem
ROLE_GURU = "guru"          # boleh membuka dashboard dan memakai aplikasi
ROLE_PENGGUNA = "pengguna"  # hanya memakai aplikasi mobile
ROLES = {ROLE_GURU, ROLE_PENGGUNA}


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Buat tabel kalau belum ada, lalu isi akun awal untuk pengujian."""
    from app.security import hash_password  # import di sini agar tidak melingkar

    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                nama          TEXT    NOT NULL,
                email         TEXT    NOT NULL UNIQUE,
                password_hash TEXT    NOT NULL,
                role          TEXT    NOT NULL DEFAULT 'pengguna',
                created_at    TEXT    NOT NULL
            )
            """
        )

        # Akun awal (dipakai juga oleh tim tester). Hanya dibuat kalau belum ada.
        akun_awal = [
            ("Guru BicaraUntukku", "guru@bisindo.com", "admin123", ROLE_GURU),
            ("Pengguna Demo", "pengguna@bisindo.com", "pengguna123", ROLE_PENGGUNA),
        ]
        for nama, email, password, role in akun_awal:
            ada = conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone()
            if not ada:
                conn.execute(
                    "INSERT INTO users (nama, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
                    (nama, email, hash_password(password), role, datetime.now().isoformat(timespec="seconds")),
                )
        conn.commit()


def cari_user_email(email):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()


def cari_user_id(user_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def buat_user(nama, email, password_hash, role=ROLE_PENGGUNA):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO users (nama, email, password_hash, role, created_at) VALUES (?, ?, ?, ?, ?)",
            (nama, email, password_hash, role, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        return cur.lastrowid
