import api from "./api";

const whatsappService = {

    // ==========================================
    // ESTADO
    // ==========================================

    async getStatus() {

        const { data } = await api.get(
            "/whatsapp/status"
        );

        return data;

    },

    // ==========================================
    // QR
    // ==========================================

    async getQR() {

        const { data } = await api.get(
            "/whatsapp/qr"
        );

        return data;

    },

    // ==========================================
    // RECONECTAR
    // ==========================================

    async reconnect() {

        const { data } = await api.post(
            "/whatsapp/reconnect"
        );

        return data;

    },

    // ==========================================
    // DESCONECTAR
    // ==========================================

    async disconnect() {

        const { data } = await api.post(
            "/whatsapp/disconnect"
        );

        return data;

    }

};

export default whatsappService;