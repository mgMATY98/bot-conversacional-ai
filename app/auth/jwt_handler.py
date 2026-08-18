from datetime import datetime, timedelta, timezone
import uuid

from jose import jwt

from app.core.config import settings


def _create_token(data: dict, audience: str):

    now = datetime.now(timezone.utc)

    payload = data.copy()

    payload.update(
        {
            "exp": now + timedelta(hours=settings.TOKEN_EXPIRE_HOURS),
            "iat": now,
            "iss": "BotMunicipio",
            "aud": audience,
            "jti": str(uuid.uuid4()),
        }
    )

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM,
    )


def create_client_token(client_id: int):

    return _create_token(
        {
            "client_id": client_id,
        },
        audience="BotMunicipioClient",
    )


def create_admin_token(admin_id: int):

    return _create_token(
        {
            "admin_id": admin_id,
        },
        audience="BotMunicipioAdmin",
    )
