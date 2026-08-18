import api from "./api";

const dashboardService = {

    async getDashboard() {

        const { data } = await api.get("/dashboard");

        return data;

    }

};

export default dashboardService;