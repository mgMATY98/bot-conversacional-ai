from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.login import LoginRequest

from app.models.admin import Admin
from app.models.client import Client

from app.core.auth import (
    verify_password,
    create_access_token,
)

from services.logs.login_logger import save_login_log
from services.logs.audit_logger import save_audit_log

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):

    ip = request.client.host

    # ==========================================================
    # Buscar administrador
    # ==========================================================

    admin = db.query(Admin).filter(Admin.username == credentials.username).first()

    if admin:

        if not verify_password(
            credentials.password,
            admin.password_hash,
        ):

            save_login_log(
                db=db,
                username=credentials.username,
                ip=ip,
                status="FAILED",
                detail="Credenciales inválidas",
                login_type="ADMIN",
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )

        token = create_access_token(
            admin.id,
            "admin",
        )

        save_login_log(
            db=db,
            username=admin.username,
            ip=ip,
            status="SUCCESS",
            login_type="ADMIN",
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "admin",
        }

    # ==========================================================
    # Buscar cliente
    # ==========================================================

    client = db.query(Client).filter(Client.username == credentials.username).first()

    if client:

        if not verify_password(
            credentials.password,
            client.password_hash,
        ):

            save_login_log(
                db=db,
                username=credentials.username,
                ip=ip,
                status="FAILED",
                detail="Credenciales inválidas",
                login_type="CLIENT",
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
            )

        token = create_access_token(
            client.id,
            "client",
        )

        save_login_log(
            db=db,
            username=client.username,
            ip=ip,
            status="SUCCESS",
            login_type="CLIENT",
        )

        save_audit_log(
            db=db,
            client_id=client.id,
            username=client.username,
            ip=ip,
            action="LOGIN",
            status="SUCCESS",
            details="Inicio de sesión del cliente",
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": "client",
        }

    # ==========================================================
    # Usuario inexistente
    # ==========================================================

    save_login_log(
        db=db,
        username=credentials.username,
        ip=ip,
        status="FAILED",
        detail="Usuario inexistente",
        login_type="UNKNOWN",
    )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuario o contraseña incorrectos",
    )
