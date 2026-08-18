from jose import jwt
from fastapi import Request

from app.core.config import settings


def client_rate_limit_key(request: Request):

    auth = request.headers.get("Authorization")

    if not auth:
        return request.client.host

    if not auth.startswith("Bearer "):
        return request.client.host

    token = auth.replace("Bearer ", "")

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            audience="BotMunicipioClient",
            issuer="BotMunicipio",
        )

        client_id = payload.get("client_id")

        if client_id:
            return f"client:{client_id}"

    except Exception:
        pass

    return request.client.host
