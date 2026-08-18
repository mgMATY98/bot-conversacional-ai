import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:3001",
});

const CLIENT_ID = 1;
console.log("SE CARGÓ EL NUEVO whatsappService");
const whatsappService = {

    async getStatus() {

        const { data } = await api.get(
            `/sessions/client_${CLIENT_ID}`
        );

        return data;

    },

    async create() {

        const { data } = await api.post(
            "/sessions",
            {
                client_id: CLIENT_ID,
            }
        );

        return data;

    },

    async disconnect() {

        const { data } = await api.post(
            `/sessions/client_${CLIENT_ID}/disconnect`
        );

        return data;

    },

    async reconnect() {

        const { data } = await api.post(
            `/sessions/client_${CLIENT_ID}/reconnect`
        );

        return data;

    },

    async getQR() {

        const { data } = await api.get(
            `/sessions/client_${CLIENT_ID}/qr`
        );

        return data;

    }

};

export default whatsappService;