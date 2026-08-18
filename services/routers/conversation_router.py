from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_client
from app.db.database import get_db

from app.schemas.conversation import (
    ConversationSummaryResponse,
    ConversationMessageResponse,
)

from services.conversation.conversation_service import conversation_service

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


# ==========================================
# Listar conversaciones
# ==========================================


@router.get(
    "/",
    response_model=list[ConversationSummaryResponse],
)
def list_conversations(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return conversation_service.list_conversations(
        db=db,
        client_id=current_client.id,
    )


# ==========================================
# Obtener historial completo
# ==========================================


@router.get(
    "/{contact_id}",
    response_model=list[ConversationMessageResponse],
)
def get_conversation(
    contact_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):
    return conversation_service.get_conversation(
        db=db,
        client_id=current_client.id,
        contact_id=contact_id,
    )


# ==========================================
# Eliminar historial
# ==========================================


@router.delete(
    "/{contact_id}",
)
def delete_conversation(
    contact_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    conversation_service.clear_history(
        db=db,
        client_id=current_client.id,
        contact_id=contact_id,
    )

    return {"message": "Conversación eliminada correctamente."}
