import { Bot, User } from "lucide-react";

import "./MessageBubble.css";

function MessageBubble({

    sender,

    text,

    sources = [],

    attachments = [],

    time,

}) {

    const isUser = sender === "user";

    return (

        <div className={`message-row ${isUser ? "user" : "assistant"}`}>

            {

                !isUser && (

                    <div className="message-avatar bot-avatar">

                        <Bot size={18} />

                    </div>

                )

            }

            <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>

                <div className="message-header">

                    <strong>

                        {

                            isUser

                                ? "Ciudadano"

                                : "Ricky"

                        }

                    </strong>

                </div>

                <p>{text}</p>

                {

                    sources.length > 0 && (

                        <div className="message-sources">

                            <strong>

                                📄 Fuentes consultadas

                            </strong>

                            {

                                sources.map(source => (

                                    <div
                                        key={source}
                                        className="message-source"
                                    >

                                        • {source}

                                    </div>

                                ))

                            }

                        </div>

                    )

                }

                {

                    attachments.length > 0 && (

                        <div className="message-attachments">

                            <strong>

                                📎 Archivos

                            </strong>

                        </div>

                    )

                }

                <span>

                    {time}

                </span>

            </div>

            {

                isUser && (

                    <div className="message-avatar user-avatar">

                        <User size={18} />

                    </div>

                )

            }

        </div>

    );

}

export default MessageBubble;