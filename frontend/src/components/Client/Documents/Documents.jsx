import { useEffect, useMemo, useState, useRef } from "react";

import {
    Upload,
    Search
} from "lucide-react";

import toast from "react-hot-toast";

import documentService from "../../../services/documentsService";

import DocumentCard from "./DocumentCard";
import UploadDocumentModal from "./UploadDocumentModal";

import "./Documents.css";

function Documents() {

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(true);

    const [uploadOpen, setUploadOpen] = useState(false);

    const [search, setSearch] = useState("");

    const [status, setStatus] = useState("all");

    const pollingRef = useRef(null);

    async function loadDocuments() {

        try {

            setLoading(true);

            const data = await documentService.getDocuments();

            setDocuments(data);

            const processing = data.some(
                document => document.status === "processing"
            );

            if (processing) {

                startPolling();

            }

        }

        catch (err) {

            console.error(err);

            toast.error("No se pudieron cargar los documentos");

        }

        finally {

            setLoading(false);

        }

    }
    function startPolling() {

        if (pollingRef.current) {

            return;

        }

        pollingRef.current = setInterval(async () => {

            const data = await documentService.getDocuments();

            setDocuments(data);

            const processing = data.some(

                document => document.status === "processing"

            );

            if (!processing) {

                clearInterval(pollingRef.current);

                pollingRef.current = null;

            }

        }, 2000);

    }
    useEffect(() => {

        loadDocuments();

    }, []);
    useEffect(() => {

        return () => {

            if (pollingRef.current) {

                clearInterval(pollingRef.current);

            }

        };

    }, []);

    async function handleUpload(title, file) {

        const formData = new FormData();

        formData.append("title", title);

        formData.append("file", file);

        await documentService.uploadDocument(formData);

        toast.success("Documento subido correctamente");

        // Esperar un instante para asegurar que el documento exista
        setTimeout(() => {

            loadDocuments();

        }, 300);

    }

    async function handleDelete(document) {

        if (!window.confirm(`Eliminar "${document.title}"?`)) {

            return;

        }

        await documentService.deleteDocument(document.id);

        toast.success("Documento eliminado");

        loadDocuments();

    }

    async function handleView(document) {

        await documentService.viewDocument(document.id);

    }

    async function handleDownload(document) {

        await documentService.downloadDocument(

            document.id,

            document.original_filename

        );

    }

    const filteredDocuments = useMemo(() => {

        return documents.filter((doc) => {

            const matchesSearch =

                doc.title.toLowerCase().includes(search.toLowerCase())

                ||

                doc.original_filename
                    .toLowerCase()
                    .includes(search.toLowerCase());

            const matchesStatus =

                status === "all"

                ||

                doc.status === status;

            return matchesSearch && matchesStatus;

        });

    }, [

        documents,

        search,

        status

    ]);

    return (

        <div className="documents-page">

            <div className="documents-header">

                <div>

                    <h1>

                        Base de Conocimiento

                    </h1>

                    <p>

                        Los documentos alimentan el conocimiento del asistente mediante IA.

                    </p>

                </div>

                <button

                    className="upload-button"

                    onClick={() => setUploadOpen(true)}

                >

                    <Upload size={18} />

                    Subir Documento

                </button>

            </div>

            <div className="documents-toolbar">

                <div className="documents-search">

                    <Search size={18} />

                    <input

                        placeholder="Buscar documento..."

                        value={search}

                        onChange={(e) =>

                            setSearch(e.target.value)

                        }

                    />

                </div>

                <select

                    value={status}

                    onChange={(e) =>

                        setStatus(e.target.value)

                    }

                >

                    <option value="all">

                        Todos

                    </option>

                    <option value="processed">

                        Procesados

                    </option>

                    <option value="processing">

                        Procesando

                    </option>

                    <option value="uploaded">

                        Subidos

                    </option>

                    <option value="error">

                        Error

                    </option>

                </select>

            </div>

            <div className="documents-counter">

                {filteredDocuments.length} documentos

            </div>

            {

                loading

                    ?

                    (

                        <div className="documents-loading">

                            Cargando documentos...

                        </div>

                    )

                    :

                    filteredDocuments.length === 0

                        ?

                        (

                            <div className="documents-empty">

                                No hay documentos.

                            </div>

                        )

                        :

                        (

                            <div className="documents-grid">

                                {

                                    filteredDocuments.map((document) => (

                                        <DocumentCard

                                            key={document.id}

                                            document={document}

                                            onView={handleView}

                                            onDownload={handleDownload}

                                            onDelete={handleDelete}

                                        />

                                    ))

                                }

                            </div>

                        )

            }

            <UploadDocumentModal

                open={uploadOpen}

                onClose={() =>

                    setUploadOpen(false)

                }

                onUpload={handleUpload}

            />

        </div>

    );

}

export default Documents;