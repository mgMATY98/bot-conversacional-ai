import api from "./api";

const adminService = {

    async getClients() {

        const { data } = await api.get("/admin/clients");

        return data;

    },

    async getClient(id) {

        const { data } = await api.get(`/admin/clients/${id}`);

        return data;

    },
    async toggleClient(id, active) {

        const { data } = await api.put(

            `/admin/clients/${id}`,

            {
                active
            }

        );

        return data;

    },
    async createClient(client) {

        const { data } = await api.post(
            "/admin/clients",
            client
        );

        return data;

    },

    async updateClient(id, client) {

        const { data } = await api.put(
            `/admin/clients/${id}`,
            client
        );

        return data;

    },

    async deleteClient(id) {

        const { data } = await api.delete(
            `/admin/clients/${id}`
        );

        return data;

    },

    // ==========================================================
    // CAMBIAR CANAL WHATSAPP
    // ==========================================================

    async changeWhatsAppChannel(id, channel) {

        const { data } = await api.post(
            `/admin/clients/${id}/whatsapp-channel`,
            {
                channel
            }
        );

        return data;

    },

};

export default adminService;