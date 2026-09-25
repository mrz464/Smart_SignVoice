from pydantic import BaseModel
from typing import List


class ProgresMingguan(BaseModel):
    minggu: str
    kata: int


class DashboardStats(BaseModel):
    total_siswa: int
    kata_dikuasai: int
    total_kata: int
    sesi_hari_ini: int
    akurasi_rata_rata: float
    progres_mingguan: List[ProgresMingguan]


class SessionItem(BaseModel):
    id: int
    nama: str
    kata_dikuasai: int
    total_sesi: int
    status: str