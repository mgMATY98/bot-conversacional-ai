const broadcastService =
    require("../services/broadcast.service");

const sessionService =
    require("../services/session.service");


class BroadcastController {

    // ==========================================================
    // INICIAR BOLETÍN
    // ==========================================================

    async start(req, res) {

        try {

            const {
                client_id,
                broadcast_id,
            } = req.body;


            if (!client_id) {

                return res.status(400).json({
                    success: false,
                    message: "client_id es obligatorio.",
                });

            }


            if (!broadcast_id) {

                return res.status(400).json({
                    success: false,
                    message: "broadcast_id es obligatorio.",
                });

            }


            const session =
                sessionService.getSession(
                    client_id
                );


            if (!session) {

                return res.status(404).json({
                    success: false,
                    message:
                        "La sesión de WhatsApp no existe.",
                });

            }


            if (!session.connected) {

                return res.status(400).json({
                    success: false,
                    message:
                        "WhatsApp no está conectado.",
                });

            }


            if (
                broadcastService.isRunning(
                    session.sessionId
                )
            ) {

                return res.status(409).json({
                    success: false,
                    message:
                        "Ya existe un boletín ejecutándose.",
                });

            }


            // ==================================================
            // INICIAR EN SEGUNDO PLANO
            // ==================================================

            broadcastService
                .start(
                    session,
                    broadcast_id,
                )
                .catch(error => {

                    console.error("");
                    console.error(
                        "===================================="
                    );
                    console.error(
                        "❌ Error ejecutando boletín"
                    );
                    console.error(
                        error
                    );
                    console.error(
                        "===================================="
                    );

                });


            return res.json({

                success: true,

                message:
                    "Boletín iniciado correctamente.",

                broadcast_id,

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

}


module.exports =
    new BroadcastController();