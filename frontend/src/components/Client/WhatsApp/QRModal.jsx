import { useEffect, useState } from "react";

import {
    X,
    LoaderCircle,
    QrCode,
    Smartphone,
    CheckCircle2,
} from "lucide-react";

import QRCode from "qrcode";

import "./QRModal.css";


function QRModal({
    open,
    qr,
    connection,
    loading,
    onClose,
}) {

    const [qrImage, setQrImage] = useState("");


    // ==========================================================
    // CONVERTIR EL STRING DEL QR EN UNA IMAGEN
    // ==========================================================

    useEffect(() => {

        if (!qr) {

            setQrImage("");

            return;

        }

        let cancelled = false;

        async function generateQR() {

            try {

                console.log("🔄 Generando imagen del QR...");

                const image = await QRCode.toDataURL(
                    qr,
                    {
                        width: 300,
                        margin: 2,
                    }
                );

                if (!cancelled) {

                    setQrImage(image);

                    console.log(
                        "✅ Imagen QR generada"
                    );

                }

            }

            catch (error) {

                console.error(
                    "❌ Error generando imagen QR:",
                    error
                );

                if (!cancelled) {
                    setQrImage("");
                }

            }

        }

        generateQR();

        return () => {

            cancelled = true;

        };

    }, [qr]);


    if (!open) {
        return null;
    }


    // ==========================================================
    // ESTADOS
    // ==========================================================

    const connected =
        connection?.connected === true;

    const authenticated =
        connection?.status === "AUTHENTICATED";

    const qrReady =
        Boolean(qrImage);


    // ==========================================================
    // RENDER
    // ==========================================================

    return (

        <div className="qr-modal-overlay">

            <div className="qr-modal">


                {/* ================================================= */}
                {/* HEADER */}
                {/* ================================================= */}

                <div className="qr-modal-header">

                    <div>

                        <h2>
                            Conectar WhatsApp
                        </h2>

                        <p>
                            Vinculá tu cuenta de WhatsApp
                        </p>

                    </div>


                    <button
                        className="close-button"
                        onClick={onClose}
                    >

                        <X size={20} />

                    </button>

                </div>


                {/* ================================================= */}
                {/* BODY */}
                {/* ================================================= */}

                <div className="qr-modal-body">


                    {/* ================================================= */}
                    {/* CONECTADO */}
                    {/* ================================================= */}

                    {connected && (

                        <div className="qr-loading-state">

                            <div className="qr-success-icon">

                                <CheckCircle2 size={48} />

                            </div>

                            <h3>
                                WhatsApp conectado
                            </h3>

                            <p>
                                La conexión se realizó correctamente.
                            </p>

                        </div>

                    )}


                    {/* ================================================= */}
                    {/* AUTENTICADO / CONECTANDO */}
                    {/* ================================================= */}

                    {!connected && authenticated && (

                        <div className="qr-loading-state">

                            <div className="qr-loading-icon">

                                <LoaderCircle
                                    size={46}
                                    className="qr-spinner"
                                />

                            </div>

                            <h3>
                                Conectando WhatsApp...
                            </h3>

                            <p>
                                El código fue escaneado correctamente.
                            </p>

                            <div className="qr-progress">

                                <div className="qr-progress-bar" />

                            </div>

                            <span className="qr-loading-hint">
                                Esperá mientras terminamos de conectar.
                            </span>

                        </div>

                    )}


                    {/* ================================================= */}
                    {/* GENERANDO QR */}
                    {/* ================================================= */}

                    {!connected &&
                        !authenticated &&
                        !qrReady && (

                            <div className="qr-loading-state">

                                <div className="qr-loading-icon">

                                    <LoaderCircle
                                        size={46}
                                        className="qr-spinner"
                                    />

                                </div>

                                <h3>
                                    Generando código QR...
                                </h3>

                                <p>
                                    Estamos preparando la conexión con WhatsApp.
                                </p>

                                <div className="qr-progress">

                                    <div className="qr-progress-bar" />

                                </div>

                                <span className="qr-loading-hint">
                                    No cierres esta ventana.
                                </span>

                            </div>

                        )}


                    {/* ================================================= */}
                    {/* QR LISTO */}
                    {/* ================================================= */}

                    {!connected &&
                        !authenticated &&
                        qrReady && (

                            <div className="qr-ready-state">

                                <div className="qr-title">

                                    <QrCode size={22} />

                                    <span>
                                        Código QR listo
                                    </span>

                                </div>


                                <div className="qr-container">

                                    <img
                                        src={qrImage}
                                        alt="Código QR de WhatsApp"
                                        className="qr-image"
                                    />

                                </div>


                                <div className="qr-instructions">

                                    <Smartphone size={20} />

                                    <span>
                                        Abrí WhatsApp en tu teléfono
                                        y escaneá este código.
                                    </span>

                                </div>

                            </div>

                        )}

                </div>


                {/* ================================================= */}
                {/* FOOTER */}
                {/* ================================================= */}

                {!connected && (

                    <div className="qr-modal-footer">

                        <span>
                            La conexión se realiza de forma segura.
                        </span>

                    </div>

                )}

            </div>

        </div>

    );

}


export default QRModal;