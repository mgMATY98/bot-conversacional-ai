# Bot Conversacional Multicliente

Plataforma de automatización conversacional orientada a empresas y organizaciones, con integración de inteligencia artificial, WhatsApp y un panel web de administración.

El proyecto está diseñado con una arquitectura modular que permite gestionar múltiples clientes, configuraciones independientes, conversaciones y diferentes canales de WhatsApp desde una plataforma centralizada.

> ⚠️ Este repositorio contiene una versión pública del proyecto. Se han omitido credenciales, configuraciones privadas, datos reales y componentes propietarios.

---

## 🚀 Características

- 🤖 Integración con modelos de inteligencia artificial
- 💬 Integración con WhatsApp
- 🏢 Arquitectura orientada a múltiples clientes
- 🔐 Autenticación y autorización
- 📊 Panel administrativo
- 👥 Gestión de clientes y contactos
- 💬 Gestión de conversaciones
- 📚 Gestión de documentos y conocimiento
- 📢 Sistema de difusión de mensajes
- 📝 Registro de actividad y auditoría
- ☁️ Arquitectura preparada para WhatsApp Cloud API
- ⚙️ API REST
- 🧩 Arquitectura modular

---

## 🏗️ Arquitectura

```text
                         ┌─────────────────────┐
                         │      Frontend       │
                         │     React + Vite    │
                         └──────────┬──────────┘
                                    │
                                    │ REST API
                                    ▼
                         ┌─────────────────────┐
                         │       Backend       │
                         │       FastAPI       │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
             PostgreSQL/       AI Services       WhatsApp
              SQLite*              │                 │
                                  │                 │
                                  ▼                 ▼
                              OpenAI API       WhatsApp Gateway
                                                    │
                                                    ▼
                                               WhatsApp
