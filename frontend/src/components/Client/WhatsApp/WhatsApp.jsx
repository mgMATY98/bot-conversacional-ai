import { useEffect, useRef, useState } from "react";

import {
    Smartphone,
    Wifi,
    WifiOff,
    QrCode,
    RefreshCcw,
    LogOut,
    User,
    Clock,
    Hash,
} from "lucide-react";

import toast from "react-hot-toast";

import whatsappService from "../../../services/whatsappService";

import QRModal from "./QRModal";

import "./WhatsApp.css";


function WhatsApp() {

    const statusIntervalRef = useRef(null);
    const qrIntervalRef = useRef(null);

    const [connection, setConnection] = useState(null);

    const [loading, setLoading] = useState(true);

    const [showQR, setShowQR] = useState(false);

    const [qr, setQr] = useState("");

    const [connecting, setConnecting] = useState(false);


    // ==========================================================
    // CARGAR ESTADO
    // ==========================================================

    async function loadStatus() {

        try {

            const data =
                await whatsappService.getStatus();

            setConnection(data);

            return data;

        }

        catch (err) {

            console.error(err);

            toast.error(
                "No se pudo obtener el estado."
            );

            return null;

        }

        finally {

            setLoading(false);

        }

    }


    // ==========================================================
    // ESTADO INICIAL
    // ==========================================================

    useEffect(() => {

        loadStatus();

    }, []);


    // ==========================================================
    // LIMPIAR INTERVALOS
    // ==========================================================

    useEffect(() => {

        return () => {

            if (statusIntervalRef.current) {

                clearInterval(
                    statusIntervalRef.current
                );

                statusIntervalRef.current = null;

            }

            if (qrIntervalRef.current) {

                clearInterval(
                    qrIntervalRef.current
                );

                qrIntervalRef.current = null;

            }

        };

    }, []);


    // ==========================================================
    // DETECTAR CONEXIÓN
    // ==========================================================

    useEffect(() => {

        if (!connection) {
            return;
        }

        if (
            connection.connected &&
            showQR
        ) {

            stopPolling();

            setConnecting(false);

            setShowQR(false);

            setQr("");

            toast.success(
                "WhatsApp conectado correctamente."
            );

        }

    }, [
        connection,
        showQR
    ]);

    useEffect(() => {

        if (!connection) {
            return;
        }

        console.log("🔎 Revisando conexión para cerrar QR:", connection);

        if (connection.connected === true) {

            console.log("✅ FRONTEND: cerrando modal QR");

            stopPolling();

            setConnecting(false);
            setQr("");
            setShowQR(false);

        }

    }, [connection]);

    // ==========================================================
    // POLLING DEL ESTADO
    // ==========================================================

    function startStatusPolling() {

        if (statusIntervalRef.current) {
            return;
        }

        console.log("📡 Iniciando polling de estado...");

        statusIntervalRef.current = setInterval(async () => {

            try {

                const data = await whatsappService.getStatus();

                console.log("📡 Estado WhatsApp:", data);

                setConnection(data);

                if (data.connected === true) {

                    console.log(
                        "✅ WhatsApp conectado. Deteniendo polling."
                    );

                    clearInterval(statusIntervalRef.current);

                    statusIntervalRef.current = null;

                    if (qrIntervalRef.current) {

                        clearInterval(qrIntervalRef.current);

                        qrIntervalRef.current = null;

                    }

                }

            }

            catch (err) {

                console.error(
                    "❌ Error consultando estado:",
                    err
                );

            }

        }, 1000);
    }

    function stopPolling() {

        console.log("🛑 Deteniendo polling WhatsApp");

        if (statusIntervalRef.current) {

            clearInterval(statusIntervalRef.current);

            statusIntervalRef.current = null;

        }

        if (qrIntervalRef.current) {

            clearInterval(qrIntervalRef.current);

            qrIntervalRef.current = null;

        }

    }
    // ==========================================================
    // OBTENER QR
    // ==========================================================

    function startQRPolling() {

        if (qrIntervalRef.current) {
            return;
        }

        console.log("📡 Esperando QR...");

        qrIntervalRef.current = setInterval(async () => {

            try {

                const data =
                    await whatsappService.getQR();

                if (
                    data.ready &&
                    data.qr
                ) {

                    console.log("✅ QR recibido");

                    setQr(data.qr);

                    setConnecting(false);

                    clearInterval(
                        qrIntervalRef.current
                    );

                    qrIntervalRef.current = null;

                }

            }

            catch (err) {

                console.error(
                    "❌ Error obteniendo QR:",
                    err
                );

            }

        }, 500);

    }


    // ==========================================================
    // MOSTRAR QR
    // ==========================================================
    async function openQR() {

        if (connection?.connected) {
            return;
        }

        try {

            console.log("🔄 Solicitando nueva sesión WhatsApp...");

            setShowQR(true);
            setQr("");
            setConnecting(true);

            await whatsappService.reconnect();

            console.log("✅ Sesión solicitada");

            startStatusPolling();
            startQRPolling();

        }

        catch (err) {

            console.error(
                "❌ Error iniciando WhatsApp:",
                err
            );

            stopPolling();

            setShowQR(false);
            setQr("");
            setConnecting(false);

            toast.error(
                "No fue posible iniciar WhatsApp."
            );

        }

    }


    // ==========================================================
    // CONECTAR / RECONEXIÓN
    // ==========================================================

    async function handleReconnect() {

        await openQR();

    }


    // ==========================================================
    // DESCONECTAR
    // ==========================================================
    async function handleDisconnect() {

        try {

            stopPolling();

            toast.loading(
                "Desconectando WhatsApp...",
                {
                    id: "whatsapp-disconnect",
                }
            );

            // Pedimos la desconexión completa
            const result =
                await whatsappService.disconnect();

            console.log(
                "🔴 Resultado desconexión:",
                result
            );

            // Limpiamos inmediatamente el estado visual
            setShowQR(false);
            setQr("");
            setConnecting(false);

            // Consultamos el estado real del backend
            const data =
                await whatsappService.getStatus();

            console.log(
                "📡 Estado después de desconectar:",
                data
            );

            setConnection(data);

            toast.success(
                "WhatsApp desconectado.",
                {
                    id: "whatsapp-disconnect",
                }
            );

            // Esperamos un poquito para que termine
            // la limpieza de Node/WhatsApp
            setTimeout(() => {

                window.location.reload();

            }, 1000);

        }

        catch (err) {

            console.error(
                "❌ Error desconectando:",
                err
            );

            toast.error(
                "No fue posible desconectar WhatsApp.",
                {
                    id: "whatsapp-disconnect",
                }
            );

        }

    }


    // ==========================================================
    // CERRAR MODAL
    // ==========================================================

    function closeQR() {

        stopPolling();

        setShowQR(false);

        setQr("");

        setConnecting(false);

    }


    // ==========================================================
    // FECHA
    // ==========================================================

    function formatLastSeen(date) {

        if (!date) {
            return "-";
        }

        return new Date(
            date
        ).toLocaleString();

    }


    // ==========================================================
    // LOADING
    // ==========================================================

    if (loading) {

        return (
            <p>
                Cargando WhatsApp...
            </p>
        );

    }


    // ==========================================================
    // RENDER
    // ==========================================================

    return (

        <div className="whatsapp-page">

            <div className="whatsapp-header">

                <div>

                    <h1>
                        WhatsApp Business
                    </h1>

                    <p>
                        Estado actual de la conexión del asistente.
                    </p>

                </div>

            </div>


            {/* ================================================= */}
            {/* ESTADO */}
            {/* ================================================= */}

            <div className="whatsapp-card">

                <div className="status-row">

                    <span>
                        Estado
                    </span>

                    <div
                        className={`status ${connection?.connected
                            ? "connected"
                            : "offline"
                            }`}
                    >

                        {
                            connection?.connected
                                ?
                                <Wifi size={18} />
                                :
                                <WifiOff size={18} />
                        }

                        {
                            connection?.connected
                                ?
                                "Conectado"
                                :
                                "Desconectado"
                        }

                    </div>

                </div>


                <div className="status-row">

                    <User size={18} />

                    <span>
                        Nombre
                    </span>

                    <strong>
                        {
                            connection?.push_name ||
                            "-"
                        }
                    </strong>

                </div>


                <div className="status-row">

                    <Smartphone size={18} />

                    <span>
                        Número
                    </span>

                    <strong>
                        {
                            connection?.phone ||
                            "-"
                        }
                    </strong>

                </div>


                <div className="status-row">

                    <Hash size={18} />

                    <span>
                        Sesión
                    </span>

                    <strong>
                        {
                            connection?.session_id ||
                            "-"
                        }
                    </strong>

                </div>


                <div className="status-row">

                    <Clock size={18} />

                    <span>
                        Última actividad
                    </span>

                    <strong>
                        {
                            formatLastSeen(
                                connection?.last_seen
                            )
                        }
                    </strong>

                </div>


                <div className="status-row">

                    <span>
                        Estado interno
                    </span>

                    <strong>
                        {
                            connection?.status ||
                            "-"
                        }
                    </strong>

                </div>

            </div>


            {/* ================================================= */}
            {/* BOTONES */}
            {/* ================================================= */}

            <div className="actions">

                <button
                    onClick={openQR}
                    disabled={connection?.connected}
                    className={
                        connection?.connected
                            ? "disabled"
                            : ""
                    }
                >

                    <QrCode size={18} />

                    Mostrar QR

                </button>


                <button
                    onClick={handleReconnect}
                >

                    <RefreshCcw size={18} />

                    Reconectar

                </button>


                <button
                    className="disconnect"
                    onClick={handleDisconnect}
                >

                    <LogOut size={18} />

                    Desconectar

                </button>

            </div>


            {/* ================================================= */}
            {/* QR */}
            {/* ================================================= */}

            <QRModal

                open={showQR}

                qr={qr}

                connection={connection}

                loading={connecting}

                onClose={closeQR}

            />

        </div>

    );

}


export default WhatsApp;