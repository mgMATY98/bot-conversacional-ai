from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.admin import Admin
from app.models.client import Client
from app.core.config import settings

# ==================================================
# PASSWORDS
# ==================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


# ==================================================
# JWT
# ==================================================


def _create_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        hours=settings.TOKEN_EXPIRE_HOURS
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM,
    )


def create_access_token(user_id: int, role: str):

    if role == "admin":

        payload = {
            "user_id": user_id,
            "role": "admin",
            "aud": "BotMunicipioAdmin",
        }

    elif role == "client":

        payload = {
            "user_id": user_id,
            "role": "client",
            "aud": "BotMunicipioClient",
        }

    else:

        raise ValueError("Rol inválido")

    return _create_token(payload)


# ==================================================
# TOKEN DECODER
# ==================================================


def _decode_token(
    token: str,
    audience: str,
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            audience=audience,
        )

        return payload

    except JWTError:

        raise credentials_exception


# ==================================================
# CURRENT ADMIN
# ==================================================


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):

    payload = _decode_token(
        credentials.credentials,
        "BotMunicipioAdmin",
    )

    if payload.get("role") != "admin":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado",
        )

    admin = db.query(Admin).filter(Admin.id == payload["user_id"]).first()

    if admin is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrador inexistente",
        )

    return admin


# ==================================================
# CURRENT CLIENT
# ==================================================


def get_current_client(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):

    payload = _decode_token(
        credentials.credentials,
        "BotMunicipioClient",
    )

    if payload.get("role") != "client":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado",
        )

    client = db.query(Client).filter(Client.id == payload["user_id"]).first()

    if client is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente inexistente",
        )

    return client
