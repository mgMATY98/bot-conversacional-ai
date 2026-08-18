from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_client
from app.db.database import get_db

from app.schemas.chat import ChatRequest
from services.chat.chat_service import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/test")
def chat_test(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return chat_service.process_message(
        db=db,
        client_id=current_client.id,
        user_id=request.user_id,
        channel=request.channel,
        message=request.message,
        name=request.name,
    )
