from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db

from app.models.client import Client
from app.models.admin import Admin

security = HTTPBearer()


def get_current_client(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            audience="BotMunicipioClient",
            issuer="BotMunicipio",
        )

        client_id = payload.get("client_id")

        if client_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
            )

        client = db.query(Client).filter(Client.id == client_id).first()

        if client is None:
            raise HTTPException(
                status_code=401,
                detail="Cliente inexistente",
            )

        if not client.active:
            raise HTTPException(
                status_code=403,
                detail="Cliente deshabilitado",
            )

        return client

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            audience="BotMunicipioAdmin",
            issuer="BotMunicipio",
        )

        admin_id = payload.get("admin_id")

        if admin_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
            )

        admin = db.query(Admin).filter(Admin.id == admin_id).first()

        if admin is None:
            raise HTTPException(
                status_code=401,
                detail="Administrador inexistente",
            )

        if not admin.active:
            raise HTTPException(
                status_code=403,
                detail="Administrador deshabilitado",
            )

        return admin

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )
