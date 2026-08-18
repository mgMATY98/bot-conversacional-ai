import api from "./api";

const conversationService = {

    async getConversations() {

        const { data } = await api.get("/conversations");

        return data;

    },

    async getConversation(contactId) {

        const { data } = await api.get(

            `/conversations/${contactId}`

        );

        return data;

    },

    async getRecentConversations(limit = 5) {

        const { data } = await api.get("/conversations");

        return data.slice(0, limit);

    }

};

export default conversationService;