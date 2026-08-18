from pydantic import BaseModel, ConfigDict

# =====================================
# STATS
# =====================================


class DashboardStats(BaseModel):

    conversations: int

    ideas: int

    documents: int

    whatsappConnected: bool

    model_config = ConfigDict(from_attributes=True)


# =====================================
# RECENT CONVERSATIONS
# =====================================


class RecentConversation(BaseModel):

    id: int

    contact_id: int

    contact_name: str | None = None

    user_id: str

    lastMessage: str

    date: str

    model_config = ConfigDict(from_attributes=True)


# =====================================
# RECENT IDEAS
# =====================================


class RecentIdea(BaseModel):

    id: int

    title: str

    priority: str

    created_at: str

    model_config = ConfigDict(from_attributes=True)


# =====================================
# RECENT DOCUMENTS
# =====================================


class RecentDocument(BaseModel):

    id: int

    name: str

    uploaded_at: str

    model_config = ConfigDict(from_attributes=True)


# =====================================
# WHATSAPP
# =====================================


class DashboardWhatsapp(BaseModel):

    connected: bool

    phone: str

    lastSync: str

    model_config = ConfigDict(from_attributes=True)


# =====================================
# DASHBOARD
# =====================================


class DashboardResponse(BaseModel):

    # Resumen generado por IA
    summary: str

    # Tarjetas del dashboard
    stats: DashboardStats

    # Últimas conversaciones
    recentConversations: list[RecentConversation]

    # Últimas ideas detectadas
    recentIdeas: list[RecentIdea]

    # Últimos documentos
    recentDocuments: list[RecentDocument]

    # Estado de WhatsApp
    whatsapp: DashboardWhatsapp

    model_config = ConfigDict(from_attributes=True)
