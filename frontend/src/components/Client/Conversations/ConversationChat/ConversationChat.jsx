import { useEffect, useState } from "react";
import { Phone } from "lucide-react";

import conversationService from "../../../../services/conversationService";

import MessageBubble from "../MessageBubble/MessageBubble";

import "./ConversationChat.css";

function ConversationChat({

    contact,

}) {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    useEffect(() => {

        if (!contact) {

            setMessages([]);

            return;

        }

        loadConversation();

    }, [contact]);

    async function loadConversation() {

        try {

            setLoading(true);

            const data = await conversationService.getConversation(
                contact.id
            );

            setMessages(data);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    }

    if (!contact) {

        return (

            <div className="conversation-chat-empty">

                <h2>

                    Seleccioná una conversación

                </h2>

                <p>

                    Elegí un ciudadano para visualizar el historial.

                </p>

            </div>

        );

    }

    return (

        <div className="conversation-chat">

            <div className="conversation-chat-header">

                <div>

                    <h2>

                        {contact.name || contact.user_id}

                    </h2>

                    <span>

                        <Phone size={16} />

                        {contact.user_id}

                    </span>

                </div>

            </div>

            <div className="conversation-chat-body">

                {

                    loading ?

                        (

                            <p>

                                Cargando conversación...

                            </p>

                        )

                        :

                        messages.map(message => (

                            <MessageBubble

                                key={message.id}

                                sender={message.role}

                                text={message.text}

                                sources={message.sources}

                                attachments={message.attachments}

                                time={new Date(message.created_at).toLocaleString()}

                            />

                        ))

                }

            </div>

        </div>

    );

}

export default ConversationChat;