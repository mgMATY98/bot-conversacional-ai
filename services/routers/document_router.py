from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.auth import get_current_client

from app.schemas.documents import DocumentResponse

from services.document.document_service import document_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


# ==========================================================
# LISTAR
# ==========================================================


@router.get(
    "/",
    response_model=list[DocumentResponse],
)
def list_documents(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return document_service.list_documents(
        db,
        current_client.id,
    )


# ==========================================================
# OBTENER
# ==========================================================


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return document_service.get_document(
        db,
        document_id,
        current_client.id,
    )


# ==========================================================
# SUBIR
# ==========================================================


@router.post(
    "/",
    response_model=DocumentResponse,
)
async def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return await document_service.upload_document(
        db=db,
        client_id=current_client.id,
        title=title,
        file=file,
    )


# ==========================================================
# DESCARGAR
# ==========================================================


@router.get(
    "/{document_id}/download",
)
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return document_service.download_document(
        db,
        document_id,
        current_client.id,
    )


# ==========================================================
# ELIMINAR
# ==========================================================


@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    return document_service.delete_document(
        db,
        document_id,
        current_client.id,
    )
