import { useEffect, useState } from "react";
import { X, Phone } from "lucide-react";

import conversationService from "../../../services/conversationService";

import MessageBubble from "../Conversations/MessageBubble/MessageBubble";

import "./conversationmodel.css";

function ConversationModal({

    client,

    onClose

}) {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (!client) return;

        loadConversation();

    }, [client]);

    async function loadConversation() {

        try {

            setLoading(true);

            const data = await conversationService.getConversation(

                client.contact_id

            );

            setMessages(data);

        } catch (error) {

            console.error(error);

            alert("No se pudo cargar la conversación.");

        } finally {

            setLoading(false);

        }

    }

    if (!client) return null;

    return (

        <div className="conversation-modal-overlay">

            <div className="conversation-modal">

                <div className="conversation-modal-header">

                    <div>

                        <h2>

                            {client.contact_name || "Sin nombre"}

                        </h2>

                        <span>

                            <Phone size={16} />

                            {client.user_id}

                        </span>

                    </div>

                    <button onClick={onClose}>

                        <X size={22} />

                    </button>

                </div>

                <div className="conversation-modal-body">

                    {

                        loading ? (

                            <p>

                                Cargando conversación...

                            </p>

                        ) : messages.length === 0 ? (

                            <p>

                                No hay mensajes.

                            </p>

                        ) : (

                            messages.map((message) => (

                                <MessageBubble

                                    key={message.id}

                                    sender={message.role}

                                    text={message.text}

                                    sources={message.sources}

                                    attachments={message.attachments}

                                    time={
                                        new Date(
                                            message.created_at
                                        ).toLocaleString()
                                    }

                                />

                            ))

                        )

                    }

                </div>

            </div>

        </div>

    );

}

export default ConversationModal;