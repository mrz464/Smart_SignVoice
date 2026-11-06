from fastapi import APIRouter, Depends
from app.models.schemas import DashboardStats, SessionItem
from app.services.dashboard_service import get_dashboard_stats, get_sessions
from app.security import wajib_guru

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardStats)
def dashboard_stats(user=Depends(wajib_guru)):
    return get_dashboard_stats()


@router.get("/sessions", response_model=list[SessionItem])
def sessions(user=Depends(wajib_guru)):
    return get_sessions()