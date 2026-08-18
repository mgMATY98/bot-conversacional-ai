from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.models.admin import Admin
from app.models.client import Client
from app.models.bot_config import BotConfig
from app.models.whatsapp_connection import WhatsAppConnection
from app.models.whatsapp_cloud_connection import WhatsAppCloudConnection  # noqa: F401
from app.models.broadcast import Broadcast  # noqa: F401
from app.models.broadcast_recipient import (
    BroadcastRecipient,
)  # noqa: F401 - ¡Importante para resolver la relación en Contact!
from app.models.contact import (
    Contact,
)  # noqa: F401 - También recomendado si Contact tiene relaciones

from app.core.auth import hash_password
from app.core.bot_config_factory import create_default_bot_config

# ==========================================================
# ADMIN
# ==========================================================


def create_admin(db: Session):

    admin = db.query(Admin).filter(Admin.username == "admin").first()

    if admin:
        print("✅ Admin ya existe.")
        return

    admin = Admin(
        username="admin",
        password_hash=hash_password("admin123"),
        active=True,
    )

    db.add(admin)
    db.commit()

    print("✅ Admin creado.")


# ==========================================================
# CLIENTE DEMO
# ==========================================================


def create_demo_client(db: Session):

    client = db.query(Client).filter(Client.username == "demo").first()

    if client:
        print("✅ Cliente demo ya existe.")
        return

    client = Client(
        # ------------------------------------------
        # Acceso
        # ------------------------------------------
        username="demo",
        password_hash=hash_password("demo123"),
        active=True,
        # ------------------------------------------
        # Organización
        # ------------------------------------------
        organization_name="Municipio Demo",
        representative_name="Administrador",
        representative_role="Director de Sistemas",
        municipality="Cañuelas",
        province="Buenos Aires",
        # ------------------------------------------
        # Bot
        # ------------------------------------------
        bot_phone="+5491111111111",
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    print("✅ Cliente demo creado.")

    create_demo_bot_config(
        db=db,
        client_id=client.id,
    )


# ==========================================================
# BOT CONFIG
# ==========================================================


def create_demo_bot_config(
    db: Session,
    client_id: int,
):

    config = db.query(BotConfig).filter(BotConfig.client_id == client_id).first()

    if config:
        print("✅ Configuración del bot ya existe.")
        return

    config = create_default_bot_config(client_id)

    db.add(config)
    db.commit()

    print("✅ Configuración del bot creada.")


# ==========================================================
# WHATSAPP
# ==========================================================


def create_whatsapp_connection(
    db: Session,
    client_id: int,
):

    connection = (
        db.query(WhatsAppConnection)
        .filter(WhatsAppConnection.client_id == client_id)
        .first()
    )

    if connection:
        print("✅ Configuración de WhatsApp ya existe.")
        return

    connection = WhatsAppConnection(
        client_id=client_id,
        session_id=f"client_{client_id}",
        phone=None,
        push_name=None,
        status="DISCONNECTED",
        connected=False,
        last_qr=None,
        last_error=None,
        last_seen=None,
    )

    db.add(connection)
    db.commit()

    print("✅ Configuración de WhatsApp creada.")


# ==========================================================
# MAIN
# ==========================================================


def main():

    db = SessionLocal()

    try:
        create_admin(db)

        create_demo_client(db)

        client = db.query(Client).filter(Client.username == "demo").first()

        if client:
            create_whatsapp_connection(
                db=db,
                client_id=client.id,
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()
