from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.core.auth import get_current_client

router = APIRouter(
    prefix="/client",
    tags=["Client"],
)


@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    client = db.query(Client).filter(Client.id == current_client.id).first()

    return client


@router.put("/me")
def update_my_profile(
    data: dict,
    db: Session = Depends(get_db),
    current_client=Depends(get_current_client),
):

    client = db.query(Client).filter(Client.id == current_client.id).first()

    editable_fields = [
        "organization_name",
        "representative_name",
        "representative_role",
        "municipality",
        "province",
        "bot_phone",
    ]

    for field in editable_fields:
        if field in data:
            setattr(client, field, data[field])

    db.commit()
    db.refresh(client)

    return client
