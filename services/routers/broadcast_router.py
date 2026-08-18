from app.core.auth import get_current_client
from app.db.database import get_db

from app.models.broadcast import Broadcast
from app.schemas.broadcast_schema import (
    BroadcastCreateRequest,
    BroadcastRecipientResultRequest,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks,
)

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from services.broadcast.broadcast_service import (
    broadcast_service,
)

router = APIRouter(
    prefix="/broadcasts",
    tags=["Broadcasts"],
)


# ==========================================================
# CREAR BOLETÍN
# ==========================================================


@router.post("")
def create_broadcast(
    data: BroadcastCreateRequest,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    try:

        broadcast = broadcast_service.create_broadcast(
            db=db,
            client_id=current_client.id,
            message=data.message,
        )

        return {
            "success": True,
            "broadcast": {
                "id": broadcast.id,
                "client_id": broadcast.client_id,
                "message": broadcast.message,
                "status": broadcast.status,
                "total_recipients": broadcast.total_recipients,
                "sent_count": broadcast.sent_count,
                "failed_count": broadcast.failed_count,
                "created_at": broadcast.created_at,
            },
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# INICIAR BOLETÍN
# ==========================================================


@router.post("/{broadcast_id}/start")
def start_broadcast(
    broadcast_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    # ======================================================
    # VERIFICAR QUE EL BOLETÍN EXISTA
    # ======================================================

    broadcast = (
        db.query(Broadcast)
        .filter(
            Broadcast.id == broadcast_id,
            Broadcast.client_id == current_client.id,
        )
        .first()
    )

    if broadcast is None:

        raise HTTPException(
            status_code=404,
            detail="El boletín no existe.",
        )

    # ======================================================
    # EVITAR DOBLE EJECUCIÓN
    # ======================================================

    if broadcast.status == "SENDING":

        raise HTTPException(
            status_code=409,
            detail="El boletín ya está siendo ejecutado.",
        )

    # ======================================================
    # VALIDAR ESTADO
    # ======================================================

    if broadcast.status == "COMPLETED":

        raise HTTPException(
            status_code=400,
            detail="El boletín ya fue completado.",
        )

    if broadcast.status == "CANCELLED":

        raise HTTPException(
            status_code=400,
            detail="El boletín fue cancelado.",
        )

    # ======================================================
    # CREAR SESIÓN INDEPENDIENTE
    # ======================================================

    engine = db.get_bind()

    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
    )

    # ======================================================
    # EJECUTAR EN SEGUNDO PLANO
    # ======================================================

    def execute_broadcast():

        background_db = SessionLocal()

        try:

            broadcast_service.run_broadcast(
                db=background_db,
                client_id=current_client.id,
                broadcast_id=broadcast_id,
                delay_seconds=3,
            )

        except Exception as e:

            print("")
            print("====================================")
            print("❌ ERROR EJECUTANDO BOLETÍN")
            print("====================================")
            print(e)

            background_db.rollback()

        finally:

            background_db.close()

    background_tasks.add_task(execute_broadcast)

    return {
        "success": True,
        "message": "Boletín iniciado correctamente.",
        "broadcast_id": broadcast_id,
        "status": "STARTING",
    }


# ==========================================================
# PRÓXIMO DESTINATARIO
# ==========================================================


@router.get("/{broadcast_id}/next")
def get_next_recipient(
    broadcast_id: int,
    db: Session = Depends(get_db),
):

    try:

        recipient = broadcast_service.get_next_recipient(
            db=db,
            broadcast_id=broadcast_id,
        )

        if recipient is None:

            return {
                "success": True,
                "finished": True,
            }

        return {
            "success": True,
            "finished": False,
            "recipient": {
                "id": recipient.id,
                "broadcast_id": recipient.broadcast_id,
                "contact_id": recipient.contact_id,
                "phone": recipient.phone,
                "status": recipient.status,
            },
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ==========================================================
# RESULTADO DEL ENVÍO
# ==========================================================


@router.post("/{broadcast_id}/result")
def recipient_result(
    broadcast_id: int,
    data: BroadcastRecipientResultRequest,
    db: Session = Depends(get_db),
):

    try:

        if data.success:

            recipient = broadcast_service.mark_sent(
                db=db,
                recipient_id=data.recipient_id,
            )

        else:

            recipient = broadcast_service.mark_failed(
                db=db,
                recipient_id=data.recipient_id,
                error=data.error or "Error desconocido.",
            )

        return {
            "success": True,
            "recipient": {
                "id": recipient.id,
                "status": recipient.status,
            },
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
