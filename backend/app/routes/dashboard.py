from fastapi import APIRouter
from app.models.schemas import DashboardStats, SessionItem
from app.services.dashboard_service import get_dashboard_stats, get_sessions

router = APIRouter()


@router.get("/dashboard/stats", response_model=DashboardStats)
def dashboard_stats():
    return get_dashboard_stats()


@router.get("/sessions", response_model=list[SessionItem])
def sessions():
    return get_sessions()