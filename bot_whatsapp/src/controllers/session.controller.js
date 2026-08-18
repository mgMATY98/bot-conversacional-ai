const sessionService = require("../services/session.service");

class SessionController {

    // ==========================================================
    // CREAR SESIÓN
    // ==========================================================

    async create(req, res) {

        try {

            const { client_id } = req.body;

            if (!client_id) {

                return res.status(400).json({
                    success: false,
                    message: "client_id es obligatorio.",
                });

            }

            const session = sessionService.getSession(client_id);

            // Si ya existe y está completamente lista
            if (session && session.initialized) {

                return res.json({
                    success: true,
                    message: "La sesión ya está iniciada.",
                });

            }

            // Si existe pero todavía está arrancando
            if (session && !session.initialized) {

                return res.json({
                    success: true,
                    message: "La sesión todavía se está inicializando.",
                });

            }

            // No existe -> crear una nueva
            await sessionService.create(client_id);

            return res.json({
                success: true,
                message: "Sesión creada.",
            });

        }

        catch (error) {

            console.error(error);

            return res.status(500).json({
                success: false,
                message: error.message,
            });

        }

    }

    // ==========================================================
    // ESTADO
    // ==========================================================

    async get(req, res) {

        try {

            const { id } = req.params;

            const clientId = Number(
                id.replace("client_", "")
            );

            return res.json(
                sessionService.getStatus(clientId)
            );

        }

        catch (error) {

            console.error(error);

            return res.status(500).json({
                success: false,
                message: error.message,
            });

        }

    }

    // ==========================================================
    // DESCONECTAR
    // ==========================================================

    async disconnect(req, res) {

        try {

            const { id } = req.params;

            const clientId = Number(
                id.replace("client_", "")
            );

            const ok = await sessionService.disconnect(clientId);

            return res.json({
                success: ok,
            });

        }

        catch (error) {

            console.error(error);

            return res.status(500).json({
                success: false,
                message: error.message,
            });

        }

    }

    // ==========================================================
    // RECONECTAR
    // ==========================================================

    async reconnect(req, res) {

        try {

            const { id } = req.params;

            const clientId = Number(
                id.replace("client_", "")
            );

            await sessionService.reconnect(clientId);

            return res.json({
                success: true,
                message: "Reconectando...",
            });

        }

        catch (error) {

            console.error(error);

            return res.status(500).json({
                success: false,
                message: error.message,
            });

        }

    }

    // ==========================================================
    // QR
    // ==========================================================

    async getQR(req, res) {

        try {

            const { id } = req.params;

            const clientId = Number(
                id.replace("client_", "")
            );

            const status = sessionService.getStatus(clientId);

            if (!status.exists) {

                return res.json({
                    exists: false,
                    ready: false,
                    qr: "",
                });

            }

            const qr = sessionService.getQR(clientId);

            return res.json({

                exists: true,

                ready: !!qr,

                qr,

            });

        }

        catch (error) {

            console.error(error);

            return res.status(500).json({
                success: false,
                message: error.message,
            });

        }

    }
    // ==========================================================
    // ENVIAR MENSAJE EXTERNO
    // ==========================================================

    async sendMessage(req, res) {

        try {

            const { id } = req.params;

            const clientId = Number(
                id.replace("client_", "")
            );

            const { to, message } = req.body;

            // ==================================================
            // VALIDAR DESTINATARIO
            // ==================================================

            if (!to) {

                return res.status(400).json({
                    success: false,
                    message: "El destinatario es obligatorio.",
                });

            }

            // ==================================================
            // VALIDAR MENSAJE
            // ==================================================

            if (!message || !message.trim()) {

                return res.status(400).json({
                    success: false,
                    message: "El mensaje no puede estar vacío.",
                });

            }

            // ==================================================
            // BUSCAR SESIÓN
            // ==================================================

            const session =
                sessionService.getSession(clientId);

            if (!session) {

                return res.status(404).json({
                    success: false,
                    message: "La sesión no existe.",
                });

            }

            // ==================================================
            // VALIDAR CONEXIÓN
            // ==================================================

            if (!session.client || !session.connected) {

                return res.status(400).json({
                    success: false,
                    message: "WhatsApp no está conectado.",
                });

            }

            // ==================================================
            // NORMALIZAR DESTINATARIO
            // ==================================================

            let chatId = String(to).trim();

            if (!chatId.endsWith("@c.us")) {

                chatId = `${chatId}@c.us`;

            }

            // ==================================================
            // ENVIAR
            // ==================================================

            const messageService =
                require("../services/message.service");

            const result =
                await messageService.sendExternalMessage(
                    session,
                    chatId,
                    message.trim(),
                );

            // ==================================================
            // RESULTADO
            // ==================================================

            if (!result.success) {

                return res.status(400).json(
                    result
                );

            }

            return res.json({

                success: true,

                message:
                    "Mensaje enviado correctamente.",

                client_id: clientId,

                to: chatId,

            });

        }

        catch (error) {

            console.error(
                "❌ Error enviando mensaje externo:",
                error
            );

            return res.status(500).json({

                success: false,

                message: error.message,

            });

        }

    }

}

module.exports = new SessionController();