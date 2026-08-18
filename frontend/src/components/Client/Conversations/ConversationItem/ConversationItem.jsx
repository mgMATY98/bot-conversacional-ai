import { MessageCircle } from "lucide-react";

import "./ConversationItem.css";

function ConversationItem({

    contact,

    active,

    onClick,

}) {

    function formatDate(date) {

        if (!date) return "";

        return new Date(date).toLocaleTimeString([], {

            hour: "2-digit",

            minute: "2-digit",

        });

    }

    return (

        <button

            className={`conversation-item ${active ? "active" : ""}`}

            onClick={onClick}

        >

            <div className="conversation-avatar">

                <MessageCircle size={20} />

            </div>

            <div className="conversation-body">

                <div className="conversation-top">

                    <strong>

                        {contact.name || contact.user_id}

                    </strong>

                    <small>

                        {formatDate(contact.last_message_at)}

                    </small>

                </div>

                <div className="conversation-bottom">

                    <span>

                        {

                            contact.last_role === "assistant"

                                ? "🤖 "

                                : "👤 "

                        }

                        {contact.last_message || "Sin mensajes"}

                    </span>

                </div>

            </div>

        </button>

    );

}

export default ConversationItem;