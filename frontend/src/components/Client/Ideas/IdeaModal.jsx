import { useEffect, useState } from "react";

import {
    X,
    Trash2,
    Lightbulb,
    Tag,
    Flag,
    User,
    Phone,
    Info,
    CircleDot,
    TrendingUp,
    Calendar,
    MessageSquare,
    Bot
} from "lucide-react";

import Modal from "../../Modal/Modal";
import Button from "../../Button/Button";

import api from "../../../services/api";
import toast from "react-hot-toast";

import "./IdeaModal.css";


function IdeaModal({
    open,
    idea,
    onClose,
    reload,
}) {

    const [loading, setLoading] = useState(false);
    const [summary, setSummary] = useState("");

    useEffect(() => {

        if (!idea) return;

        setSummary(idea.summary || "");

    }, [idea]);


    if (!open || !idea) {
        return null;
    }


    // =====================================================
    // ELIMINAR
    // =====================================================

    async function handleDelete() {

        try {

            setLoading(true);

            await api.delete(
                `/ideas/${idea.id}`
            );

            toast.success(
                "Idea eliminada correctamente"
            );

            reload?.();

            onClose();

        } catch (error) {

            console.error(error);

            toast.error(
                error.response?.data?.detail ||
                "No se pudo eliminar la idea"
            );

        } finally {

            setLoading(false);

        }

    }


    // =====================================================
    // FORMATEAR MENSAJE
    // =====================================================

    function getMessageText(message) {

        if (!message) {
            return "";
        }

        // Los mensajes del asistente pueden estar
        // almacenados como JSON.

        if (typeof message === "string") {

            try {

                const parsed = JSON.parse(message);

                if (
                    parsed &&
                    typeof parsed === "object" &&
                    parsed.text
                ) {

                    return parsed.text;

                }

            } catch {

                // Es texto normal.
            }

        }

        return message;

    }


    // =====================================================
    // FECHA
    // =====================================================

    function formatDate(date) {

        if (!date) {
            return "-";
        }

        return new Date(date).toLocaleString(
            "es-AR",
            {
                dateStyle: "short",
                timeStyle: "short",
            }
        );

    }


    return (
        <Modal
            open={open}
            onClose={onClose}
            title=""
            footer={null}
            className="idea-modal"
        >

            <div className="idea-detail">

                {/* =================================================
                    CABECERA
                ================================================= */}

                <div className="idea-detail-header">

                    <div className="idea-detail-icon">

                        <Lightbulb size={25} />

                    </div>

                    <div className="idea-detail-header-info">

                        <div className="idea-detail-type">

                            Idea #{idea.id}

                        </div>

                        <h2>

                            {idea.summary}

                        </h2>

                        <div className="idea-detail-tags">

                            <span className="idea-detail-tag category">

                                <Tag size={14} />

                                {idea.category}

                            </span>

                        </div>

                    </div>

                    <button
                        className="idea-detail-close"
                        onClick={onClose}
                        type="button"
                    >

                        <X size={22} />

                    </button>

                </div>


                {/* =================================================
                    CONTENIDO PRINCIPAL
                ================================================= */}

                <div className="idea-detail-layout">


                    {/* =================================================
                        COLUMNA IZQUIERDA
                    ================================================= */}

                    <div className="idea-detail-left">


                        {/* RESUMEN */}

                        <section className="idea-detail-section">

                            <h3 className="idea-detail-section-title">

                                📝 Resumen

                            </h3>

                            <textarea
                                className="idea-summary-textarea"
                                value={summary}
                                readOnly
                                rows={4}
                            />

                        </section>


                        <div className="idea-detail-divider" />


                        {/* INFORMACIÓN */}

                        <section className="idea-detail-section">

                            <h3 className="idea-detail-section-title">

                                <Info size={18} />

                                Información

                            </h3>


                            <div className="idea-info-card">

                                <div className="idea-info-row">

                                    <span>

                                        <Tag size={16} />

                                        Categoría

                                    </span>

                                    <strong>

                                        {idea.category || "-"}

                                    </strong>

                                </div>


                                <div className="idea-info-row">

                                    <span>

                                        <Flag size={16} />

                                        Prioridad

                                    </span>

                                    <strong
                                        className={
                                            `idea-value-badge priority ${idea.priority?.toLowerCase()
                                            }`
                                        }
                                    >

                                        {idea.priority || "-"}

                                    </strong>

                                </div>


                                <div className="idea-info-row">

                                    <span>

                                        <CircleDot size={16} />

                                        Estado

                                    </span>

                                    <strong
                                        className="idea-value-badge status"
                                    >

                                        {idea.status || "-"}

                                    </strong>

                                </div>


                                <div className="idea-info-row">

                                    <span>

                                        <TrendingUp size={16} />

                                        Confianza IA

                                    </span>

                                    <strong>

                                        {idea.ai_confidence != null
                                            ? `${Math.round(
                                                idea.ai_confidence * 100
                                            )}%`
                                            : "-"
                                        }

                                    </strong>

                                </div>


                                <div className="idea-info-row">

                                    <span>

                                        <Calendar size={16} />

                                        Fecha de creación

                                    </span>

                                    <strong>

                                        {formatDate(
                                            idea.created_at
                                        )}

                                    </strong>

                                </div>

                            </div>

                        </section>


                        {/* CONTACTO */}

                        <section className="idea-detail-section">

                            <h3 className="idea-detail-section-title">

                                <User size={18} />

                                Contacto

                            </h3>


                            <div className="idea-contact-card">

                                <div className="idea-contact-avatar">

                                    <Phone size={18} />

                                </div>

                                <div className="idea-contact-info">

                                    <strong>

                                        {idea.contact_phone || "-"}

                                    </strong>

                                </div>

                            </div>

                        </section>


                        {/* MENSAJE ORIGINAL */}

                        <section className="idea-detail-section">

                            <h3 className="idea-detail-section-title">

                                <MessageSquare size={18} />

                                Mensaje original

                            </h3>

                            <div className="idea-original-message">

                                {idea.original_message || "-"}

                            </div>

                        </section>


                    </div>


                    {/* =================================================
                        COLUMNA DERECHA
                    ================================================= */}

                    <div className="idea-detail-right">

                        <section className="idea-detail-section conversation-section">

                            <h3 className="idea-detail-section-title">

                                <MessageSquare size={18} />

                                Conversación de la idea

                            </h3>


                            <div className="idea-conversation">

                                {idea.conversation?.length ? (

                                    idea.conversation.map(
                                        (message) => {

                                            const isUser =
                                                message.role === "user";

                                            const text =
                                                getMessageText(
                                                    message.message
                                                );

                                            return (

                                                <div
                                                    key={message.id}
                                                    className={
                                                        `idea-message ${isUser
                                                            ? "idea-message-user"
                                                            : "idea-message-assistant"
                                                        }`
                                                    }
                                                >

                                                    <div className="idea-message-avatar">

                                                        {isUser
                                                            ? <User size={17} />
                                                            : <Bot size={17} />
                                                        }

                                                    </div>


                                                    <div className="idea-message-content">

                                                        <div className="idea-message-author">

                                                            {isUser
                                                                ? "Ciudadano"
                                                                : "Asistente"
                                                            }

                                                        </div>


                                                        <div className="idea-message-bubble">

                                                            {text}

                                                        </div>


                                                        <div className="idea-message-date">

                                                            {formatDate(
                                                                message.created_at
                                                            )}

                                                        </div>

                                                    </div>

                                                </div>

                                            );

                                        }
                                    )

                                ) : (

                                    <div className="idea-conversation-empty">

                                        No hay conversación disponible.

                                    </div>

                                )}

                            </div>

                        </section>

                    </div>

                </div>


                {/* =================================================
                    FOOTER
                ================================================= */}

                <div className="idea-detail-footer">

                    <Button
                        variant="outline"
                        onClick={onClose}
                    >

                        <X size={17} />

                        Cerrar

                    </Button>


                    <div className="idea-detail-footer-actions">

                        <Button
                            variant="danger"
                            onClick={handleDelete}
                            disabled={loading}
                        >

                            <Trash2 size={17} />

                            Eliminar

                        </Button>

                    </div>

                </div>

            </div>

        </Modal>

    );

}


export default IdeaModal;