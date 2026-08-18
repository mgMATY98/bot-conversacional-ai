from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_client

from app.schemas.bot_config import BotConfigUpdate
from services.bot_config.bot_config_services import bot_config_service

router = APIRouter(
    prefix="/bot-config",
    tags=["Bot Configuration"],
)


@router.get("/")
def get_bot_config(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return bot_config_service.get_config(
        db,
        current_client.id,
    )


@router.put("/")
def update_bot_config(
    data: BotConfigUpdate,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return bot_config_service.update_config(
        db,
        current_client.id,
        data,
    )
