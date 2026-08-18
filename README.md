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
```
---
## 🛠️ Tecnologías

### Backend
* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT
* OpenAI API

### WhatsApp
* Node.js
* JavaScript
* WhatsApp Web
* WhatsApp Cloud API

### Frontend
* React
* Vite
* JavaScript
* Axios

### Base de datos
* SQLAlchemy
* SQLite

---

## 🔐 Seguridad

El proyecto implementa diferentes mecanismos relacionados con seguridad:

* Autenticación mediante JWT
* Hashing de contraseñas
* Control de acceso
* Registro de autenticaciones
* Bloqueo por IP temporal ante una cantidad determinada de ingresos fallidos
* Auditoría de acciones
* Separación de configuraciones por cliente
* Variables de entorno para credenciales
* Exclusión de información sensible mediante `.gitignore`

> **Nota:** No se incluyen credenciales, tokens, sesiones de WhatsApp ni bases de datos reales en este repositorio por motivos de seguridad y privacidad.

---

## 🧠 Inteligencia Artificial

La plataforma utiliza inteligencia artificial para implementar asistentes conversacionales configurables. La arquitectura permite separar:

* Configuración del cliente
* Contexto del negocio
* Reglas de comportamiento
* Historial de conversaciones
* Conocimiento documental
* Servicios de IA
* Implementación de ideas o mejoras captadas de manera automática
* Simulación de respuesta humana

> *Los detalles internos del sistema de prompts y determinadas reglas de negocio específicas no forman parte de la versión pública del repositorio.*

---

## 💬 WhatsApp

La plataforma contempla diferentes mecanismos de integración con WhatsApp:

* **Gateway independiente:** Arquitectura que incluye un servicio separado encargado de manejar las comunicaciones y las sesiones de WhatsApp.
* **Soporte Cloud API:** Arquitectura preparada para trabajar de manera nativa con la API oficial de WhatsApp Cloud.

---

## 📊 Panel Administrativo

El frontend incluye un panel administrativo para gestionar diferentes aspectos de la plataforma:

### Gestión de Clientes
* Estado de los bots
* Configuración
* Contactos
* Conversaciones
* Difusión de mensajes
* Información relacionada con WhatsApp

### Administración General
* Estado de los clientes
* Eliminación o adición de clientes
* Activación o desactivación remota del bot
* Cambio entre WhatsApp Web y API oficial *(en proceso)*

---

## 🎯 Objetivo del Proyecto

El objetivo es desarrollar una plataforma reutilizable que permita implementar asistentes conversacionales para diferentes organizaciones sin necesidad de construir una aplicación independiente para cada cliente.

### Arquitectura general

```text
Cliente 
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
