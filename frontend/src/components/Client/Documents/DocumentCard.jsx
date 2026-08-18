import {
    FileText,
    Eye,
    Download,
    Trash2,
    CheckCircle,
    Loader2,
    AlertCircle,
    Calendar,
    HardDrive
} from "lucide-react";

import "./DocumentCard.css";

function DocumentCard({

    document,

    onView,

    onDownload,

    onDelete

}) {

    function getStatus() {

        switch (document.status) {

            case "processing":

                return {

                    text: "Procesando",

                    className: "processing",

                    icon: <Loader2 size={16} className="spin" />

                };

            case "processed":

                return {

                    text: "Procesado",

                    className: "processed",

                    icon: <CheckCircle size={16} />

                };

            case "error":

                return {

                    text: "Error",

                    className: "error",

                    icon: <AlertCircle size={16} />

                };

            default:

                return {

                    text: "Subido",

                    className: "uploaded",

                    icon: <CheckCircle size={16} />

                };

        }

    }

    const status = getStatus();

    const size = document.size
        ? `${(document.size / 1024).toFixed(1)} KB`
        : "-";

    const created = document.created_at
        ? new Date(document.created_at).toLocaleDateString()
        : "-";

    return (

        <div className="document-card">

            <div className="document-top">

                <div className="document-icon">

                    <FileText size={26} />

                </div>

                <div className="document-title">

                    <h3>

                        {document.title}

                    </h3>

                    <span>

                        {document.original_filename}

                    </span>

                </div>

            </div>

            <div className="document-summary">

                {

                    document.summary
                        ?

                        document.summary

                        :

                        "Todavía no se generó un resumen para este documento."

                }

            </div>

            <div className="document-info">

                <div>

                    <Calendar size={15} />

                    <span>

                        {created}

                    </span>

                </div>

                <div>

                    <HardDrive size={15} />

                    <span>

                        {size}

                    </span>

                </div>

            </div>

            <div className={`document-status ${status.className}`}>

                {status.icon}

                <span>

                    {status.text}

                </span>

            </div>

            <div className="document-actions">

                <button

                    className="view-button"

                    onClick={() => onView(document)}

                >

                    <Eye size={17} />

                    Ver

                </button>

                <button

                    className="download-button"

                    onClick={() => onDownload(document)}

                >

                    <Download size={17} />

                    Descargar

                </button>

                <button

                    className="delete-button"

                    onClick={() => onDelete(document)}

                >

                    <Trash2 size={17} />

                    Eliminar

                </button>

            </div>

        </div>

    );

}

export default DocumentCard;