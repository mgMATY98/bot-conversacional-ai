from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==========================================================
# ROUTERS
# ==========================================================

from services.routers.auth_router import router as auth_router
from services.routers.admin_router import router as admin_router
from services.routers.client_router import router as client_router
from services.routers.dashboard_router import router as dashboard_router
from services.routers.whatsapp_dashboard_router import (
    router as whatsapp_dashboard_router,
)
from services.routers.chat_router import router as chat_router
from services.routers.contact_router import router as contact_router
from services.routers.idea_router import router as idea_router
from services.routers.document_router import router as document_router
from services.routers.bot_config_router import router as bot_config_router
from services.routers.whatsapp_router import router as whatsapp_router
from services.routers.conversation_router import (
    router as conversation_router,
)
from services.routers.broadcast_router import (
    router as broadcast_router,
)
from services.routers.whatsapp_cloud_router import (
    router as whatsapp_cloud_router,
)
from services.routers.whatsapp_cloud_webhook_router import (
    router as whatsapp_cloud_webhook_router,
)

# ==========================================================
# APP
# ==========================================================

app = FastAPI(
    title="BotMunicipio API",
    version="1.0.0",
    description="Asistente Inteligente para Municipios",
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# ROUTERS
# ==========================================================

app.include_router(auth_router)

app.include_router(admin_router)

app.include_router(client_router)

app.include_router(dashboard_router)

app.include_router(chat_router)

app.include_router(contact_router)

app.include_router(idea_router)

app.include_router(document_router)

app.include_router(bot_config_router)

app.include_router(whatsapp_router)

app.include_router(broadcast_router)

app.include_router(whatsapp_dashboard_router)

app.include_router(conversation_router)

app.include_router(whatsapp_cloud_router)

app.include_router(whatsapp_cloud_webhook_router)
# ==========================================================
# HEALTH
# ==========================================================


@app.get("/")
def root():

    return {
        "name": "BotMunicipio",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
    }
