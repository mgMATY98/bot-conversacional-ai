import api from "./api";

const documentsService = {

    // ==========================================
    // LISTAR
    // ==========================================

    async getDocuments() {

        const { data } = await api.get(
            "/documents"
        );

        return data;

    },

    // ==========================================
    // OBTENER UNO
    // ==========================================

    async getDocument(id) {

        const { data } = await api.get(
            `/documents/${id}`
        );

        return data;

    },

    // ==========================================
    // SUBIR
    // ==========================================

    async uploadDocument(formData) {

        const { data } = await api.post(

            "/documents",

            formData,

            {

                headers: {

                    "Content-Type": "multipart/form-data"

                }

            }

        );

        return data;

    },

    // ==========================================
    // VER DOCUMENTO
    // ==========================================

    async viewDocument(id) {

        const response = await api.get(

            `/documents/${id}/download`,

            {

                responseType: "blob",

            }

        );

        const blob = response.data;

        const url = window.URL.createObjectURL(blob);

        window.open(
            url,
            "_blank"
        );

    },

    // ==========================================
    // DESCARGAR DOCUMENTO
    // ==========================================

    async downloadDocument(id, filename = "documento") {

        const response = await api.get(

            `/documents/${id}/download`,

            {

                responseType: "blob",

            }

        );

        const blob = response.data;

        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;

        link.download = filename;

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    },

    // ==========================================
    // ELIMINAR
    // ==========================================

    async deleteDocument(id) {

        const { data } = await api.delete(

            `/documents/${id}`

        );

        return data;

    }

};

export default documentsService;