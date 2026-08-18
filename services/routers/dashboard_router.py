from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_client

from app.schemas.dashboard import DashboardResponse

from services.dashboard.dashboard_service import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    db: Session = Depends(get_db),
    client=Depends(get_current_client),
):

    return dashboard_service.get_dashboard(
        db,
        client,
    )
