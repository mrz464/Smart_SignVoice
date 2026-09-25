from app.models.schemas import DashboardStats, SessionItem, ProgresMingguan

# Data sementara (dummy) sebelum tersambung ke PostgreSQL
# Nanti fungsi ini tinggal diganti isinya jadi query database, tanpa mengubah routes


def get_dashboard_stats() -> DashboardStats:
    return DashboardStats(
        total_siswa=4,
        kata_dikuasai=30,
        total_kata=32,
        sesi_hari_ini=8,
        akurasi_rata_rata=94.2,
        progres_mingguan=[
            ProgresMingguan(minggu="M1", kata=5),
            ProgresMingguan(minggu="M2", kata=12),
            ProgresMingguan(minggu="M3", kata=18),
            ProgresMingguan(minggu="M4", kata=25),
            ProgresMingguan(minggu="M5", kata=30),
        ],
    )


def get_sessions() -> list[SessionItem]:
    return [
        SessionItem(id=1, nama="Muhammad Rezaldi Zazky", kata_dikuasai=28, total_sesi=15, status="aktif"),
        SessionItem(id=2, nama="Ikrom Safei", kata_dikuasai=20, total_sesi=10, status="aktif"),
        SessionItem(id=3, nama="Riyan Rahmadan", kata_dikuasai=30, total_sesi=18, status="aktif"),
        SessionItem(id=4, nama="Rendi Saputra", kata_dikuasai=15, total_sesi=7, status="tidak_aktif"),
    ]