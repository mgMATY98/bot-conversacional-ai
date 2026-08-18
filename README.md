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

🛠️ Tecnologías
Backend
Python
FastAPI
SQLAlchemy
Pydantic
JWT
OpenAI API

WhatsApp
Node.js
JavaScript
WhatsApp Web
WhatsApp Cloud API

Frontend
React
Vite
JavaScript
Axios
Base de datos
SQLAlchemy
SQLite

🔐 Seguridad

El proyecto implementa diferentes mecanismos relacionados con seguridad:

Autenticación mediante JWT
Hashing de contraseñas
Control de acceso
Registro de autenticaciones
Bloqueo por ip temporal a cierta cantidad de ingresos fallidos
Auditoría de acciones
Separación de configuraciones por cliente
Variables de entorno para credenciales
Exclusión de información sensible mediante .gitignore

No se incluyen credenciales, tokens, sesiones de WhatsApp ni bases de datos reales en este repositorio.

🧠 Inteligencia Artificial

La plataforma utiliza inteligencia artificial para implementar asistentes conversacionales configurables.

La arquitectura permite separar:

Configuración del cliente
Contexto del negocio
Reglas de comportamiento
Historial de conversaciones
Conocimiento documental
Servicios de IA
Implementacion de ideas o mejoras captadas de manera automatica
Simulacion de respuesta humana

Los detalles internos del sistema de prompts y determinadas reglas de negocio no forman parte de la versión pública del repositorio.

💬 WhatsApp

La plataforma contempla diferentes mecanismos de integración con WhatsApp.

Actualmente la arquitectura incluye un gateway independiente encargado de manejar las comunicaciones y sesiones de WhatsApp.

También existe una arquitectura preparada para trabajar con WhatsApp Cloud API.

📊 Panel administrativo

El frontend incluye un panel administrativo para gestionar diferentes aspectos de la plataforma.

Entre ellos:

Clientes
Estado de los bots
Configuración
Contactos
Conversaciones
Difusión de mensajes
Información relacionada con WhatsApp

Admin
Estado de los clientes
Eliminacion o adicion de clientes
Activacion o desactivacion remota del bot
Cambio entre wsp web y api oficial (en proceso)

🎯 Objetivo del proyecto

El objetivo es desarrollar una plataforma reutilizable que permita implementar asistentes conversacionales para diferentes organizaciones sin necesidad de construir una aplicación independiente para cada cliente.

La arquitectura busca separar:

Cliente
   │
   ├── Configuración
   ├── Conocimiento
   ├── Conversaciones
   └── Canal de comunicación
             │
             ▼
      Motor conversacional
             │
             ▼
       Servicio de IA
📌 Estado del proyecto

🚧 Proyecto en desarrollo.

La arquitectura principal, autenticación, gestión de clientes, integración conversacional, panel administrativo y componentes de WhatsApp se encuentran implementados en diferentes etapas.
