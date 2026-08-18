import { useRef, useState } from "react";
import { X, Upload, FileText } from "lucide-react";

import "./UploadDocumentModal.css";

function UploadDocumentModal({

    open,

    onClose,

    onUpload

}) {

    const inputRef = useRef(null);

    const [selectedFile, setSelectedFile] = useState(null);
    const [title, setTitle] = useState("");

    const [uploading, setUploading] = useState(false);

    if (!open) return null;

    function handleFile(event) {

        const file = event.target.files[0];
        if (!file) return;

        setSelectedFile(file);
        setTitle(file.name.replace(/\.[^/.]+$/, ""));

    }

    function openExplorer() {

        inputRef.current.click();

    }

    async function handleUpload() {

        if (!selectedFile) return;

        try {

            setUploading(true);

            await onUpload(title, selectedFile);

            setSelectedFile(null);

            onClose();

        } catch (error) {

            console.error(error);

            alert("No se pudo subir el documento.");

        } finally {

            setUploading(false);

        }

    }

    function handleClose() {

        if (uploading) return;

        setSelectedFile(null);

        onClose();

    }

    return (

        <div className="upload-overlay">

            <div className="upload-modal">

                <div className="upload-header">

                    <h2>

                        Subir Documento

                    </h2>

                    <button

                        className="close-button"

                        onClick={handleClose}

                    >

                        <X size={22} />

                    </button>

                </div>

                <p className="upload-description">

                    Agregá documentos para ampliar la base de conocimiento del asistente.

                </p>

                <input

                    ref={inputRef}

                    type="file"

                    hidden

                    accept=".pdf,.txt"

                    onChange={handleFile}

                />

                <div

                    className="upload-dropzone"

                    onClick={openExplorer}

                >

                    <Upload size={42} />

                    <h3>

                        Seleccionar archivo

                    </h3>

                    <p>

                        PDF o TXT

                    </p>

                </div>

                {

                    selectedFile && (

                        <div className="selected-file">

                            <FileText size={20} />

                            <div>

                                <strong>

                                    {selectedFile.name}

                                </strong>

                                <span>

                                    {(selectedFile.size / 1024).toFixed(2)} KB

                                </span>

                            </div>

                        </div>

                    )

                }
                <div className="upload-title">

                    <label>

                        Título

                    </label>

                    <input

                        type="text"

                        value={title}

                        onChange={(e) => setTitle(e.target.value)}

                        placeholder="Nombre del documento"

                    />

                </div>
                <div className="upload-actions">

                    <button

                        className="cancel-button"

                        onClick={handleClose}

                        disabled={uploading}

                    >

                        Cancelar

                    </button>

                    <button

                        className="confirm-button"

                        disabled={!selectedFile || !title.trim() || uploading}

                        onClick={handleUpload}

                    >

                        {

                            uploading

                                ? "Subiendo..."

                                : "Subir Documento"

                        }

                    </button>

                </div>

            </div>

        </div>

    );

}

export default UploadDocumentModal;