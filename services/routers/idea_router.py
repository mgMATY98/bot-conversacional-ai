from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.core.auth import get_current_client
from app.db.database import get_db
from app.schemas.idea import (
    IdeaResponse,
    IdeaUpdate,
    IdeaConversationMessage,
)
from services.ideas import idea_service

router = APIRouter(
    prefix="/ideas",
    tags=["Ideas"],
)


# ==========================================================
# CONSTRUIR RESPUESTA DE IDEA
# ==========================================================


def build_idea_response(db: Session, idea):
    conversation = []

    idea_conversations = idea_service.get_idea_conversation(
        db=db,
        idea=idea,
    )

    for message in idea_conversations:

        conversation.append(
            IdeaConversationMessage(
                id=message.id,
                role=message.role,
                message=message.message,
                created_at=message.created_at,
            )
        )
    return IdeaResponse(
        id=idea.id,
        summary=idea.summary,
        original_message=idea.original_message,
        type=idea.type,
        category=idea.category,
        priority=idea.priority,
        status=idea.status,
        ai_confidence=idea.ai_confidence,
        created_at=idea.created_at,
        contact_name=idea.contact.name if idea.contact else None,
        contact_phone=idea.contact.user_id if idea.contact else "",
        conversation=conversation,
    )


# ==========================================================
# LISTAR IDEAS
# ==========================================================


@router.get(
    "/",
    response_model=list[IdeaResponse],
)
def list_ideas(
    status: str | None = None,
    category: str | None = None,
    priority: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    ideas = idea_service.list_ideas(
        db=db,
        client_id=current_client.id,
        status=status,
        category=category,
        priority=priority,
        search=search,
    )

    return [
        build_idea_response(
            db=db,
            idea=idea,
        )
        for idea in ideas
    ]


# ==========================================================
# OBTENER DETALLE DE IDEA + CONVERSACIÓN
# ==========================================================


@router.get(
    "/{idea_id}",
    response_model=IdeaResponse,
)
def get_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    idea = idea_service.get_idea_for_client(
        db=db,
        client_id=current_client.id,
        idea_id=idea_id,
    )

    if not idea:

        raise HTTPException(
            status_code=404,
            detail="Idea no encontrada",
        )

    return build_idea_response(
        db=db,
        idea=idea,
    )


# ==========================================================
# ACTUALIZAR IDEA
# ==========================================================


@router.put(
    "/{idea_id}",
    response_model=IdeaResponse,
)
def update_idea(
    idea_id: int,
    data: IdeaUpdate,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    idea = idea_service.get_idea_for_client(
        db=db,
        client_id=current_client.id,
        idea_id=idea_id,
    )

    if not idea:

        raise HTTPException(
            status_code=404,
            detail="Idea no encontrada",
        )

    idea = idea_service.update_idea(
        db=db,
        idea=idea,
        summary=data.summary,
        category=data.category,
        priority=data.priority,
        status=data.status,
    )

    return build_idea_response(
        db=db,
        idea=idea,
    )


# ==========================================================
# ELIMINAR IDEA
# ==========================================================


@router.delete("/{idea_id}")
def delete_idea(
    idea_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    idea = idea_service.get_idea_for_client(
        db=db,
        client_id=current_client.id,
        idea_id=idea_id,
    )

    if not idea:

        raise HTTPException(
            status_code=404,
            detail="Idea no encontrada",
        )

    idea_service.delete_idea_for_client(
        db=db,
        idea=idea,
    )

    return {"message": "Idea eliminada correctamente"}
