const {
    notifyConnected,
    notifyQR,
    notifyDisconnected,
} = require("./api.service");

class SyncService {

    async notifyConnected(clientId, phone, pushName) {

        try {

            await notifyConnected({
                client_id: clientId,
                phone,
                push_name: pushName,
            });

            console.log("=================================");
            console.log("WhatsApp conectado");
            console.log(clientId);
            console.log(pushName);
            console.log("=================================");

        } catch (error) {

            console.error("Error sincronizando con FastAPI:");

            if (error.response) {
                console.error(error.response.data);
            } else {
                console.error(error.message);
            }

        }

    }
    async notifyQR(clientId, qr) {

        try {

            await notifyQR({

                client_id: clientId,

                qr,

            });

            console.log("=================================");
            console.log("✅ QR sincronizado con FastAPI");
            console.log("Cliente:", clientId);
            console.log("=================================");

        }

        catch (error) {

            console.error("Error enviando QR:");

            if (error.response) {

                console.error(error.response.data);

            }

            else {

                console.error(error.message);

            }

        }

    }
    async notifyDisconnected(clientId) {

        try {

            await notifyDisconnected({

                client_id: clientId,

            });

            console.log("=================================");
            console.log("🔴 WhatsApp desconectado");
            console.log("Cliente:", clientId);
            console.log("=================================");

        }

        catch (error) {

            console.error("Error notificando desconexión:");

            if (error.response) {

                console.error(error.response.data);

            }

            else {

                console.error(error.message);

            }

        }

    }
    async notifyStatus(clientId, status) {

        try {

            await axios.post(
                `${FASTAPI_URL}/wsp/status`,
                {
                    client_id: clientId,
                    status: status,
                }
            );

            console.log("");
            console.log("=================================");
            console.log("📡 Estado sincronizado");
            console.log("Cliente:", clientId);
            console.log("Estado :", status);
            console.log("=================================");

        }

        catch (err) {

            console.error(
                "Error notificando estado:",
                err.message
            );

        }

    }
}

module.exports = new SyncService();