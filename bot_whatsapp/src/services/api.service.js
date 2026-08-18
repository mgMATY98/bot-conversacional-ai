const axios = require("axios");

const api = axios.create({
    baseURL: process.env.FASTAPI_URL,
    timeout: 60000,
});


// =========================================
// Sincronizar conexión
// =========================================

async function notifyConnected(data) {

    try {

        const response = await api.post(
            "/wsp/connected",
            data
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error sincronizando con FastAPI:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        throw err;

    }

}


// =========================================
// Sincronizar QR
// =========================================

async function notifyQR(data) {

    try {

        const response = await api.post(
            "/wsp/qr",
            data
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error enviando QR a FastAPI:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        throw err;

    }

}


// =========================================
// Sincronizar desconexión
// =========================================

async function notifyDisconnected(data) {

    try {

        const response = await api.post(
            "/wsp/disconnected",
            data
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error notificando desconexión a FastAPI:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        throw err;

    }

}


// =========================================
// Enviar mensaje al bot
// =========================================

async function sendMessage(data) {

    try {

        const response = await api.post(
            "/wsp/message",
            data
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error enviando mensaje a FastAPI:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        return {
            success: false,
            reply: null,
            error: err.message,
        };

    }

}


// ==========================================================
// BROADCAST
// OBTENER PRÓXIMO DESTINATARIO
// ==========================================================

async function getNextBroadcastRecipient(
    broadcastId
) {

    try {

        const response = await api.get(
            `/broadcasts/${broadcastId}/next`
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error obteniendo destinatario del boletín:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        throw err;

    }

}


// ==========================================================
// BROADCAST
// INFORMAR RESULTADO DEL ENVÍO
// ==========================================================

async function reportBroadcastResult(
    broadcastId,
    recipientId,
    success,
    error = null,
) {

    try {

        const response = await api.post(
            `/broadcasts/${broadcastId}/result`,
            {
                recipient_id: recipientId,
                success,
                error,
            }
        );

        return response.data;

    } catch (err) {

        console.error(
            "Error informando resultado del boletín:",
            err.message
        );

        if (err.response) {
            console.error(err.response.data);
        }

        throw err;

    }

}


// =========================================
// EXPORTS
// =========================================

module.exports = {

    sendMessage,

    notifyConnected,

    notifyQR,

    notifyDisconnected,

    getNextBroadcastRecipient,

    reportBroadcastResult,

};