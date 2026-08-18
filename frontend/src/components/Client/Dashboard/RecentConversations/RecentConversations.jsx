import { useState } from "react";
import { MessageCircle, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import Card from "../../../Card/card";

import ConversationModal from "../../ConversationModal/conversationmodel";

import "./RecentConversations.css";

function RecentConversations({

    conversations = [],

    loading

}) {

    const [selectedConversation, setSelectedConversation] = useState(null);

    return (

        <Card>

            <div className="widget-header">

                <div>

                    <h3>

                        Conversaciones recientes

                    </h3>

                    <p>

                        Últimos ciudadanos atendidos

                    </p>

                </div>

                <Link

                    to="/client/conversations"

                    className="widget-link"

                >

                    Ver todas

                    <ArrowRight size={16} />

                </Link>

            </div>

            {

                loading ?

                    (

                        <div className="widget-loading">

                            Cargando conversaciones...

                        </div>

                    )

                    :

                    conversations.length === 0 ?

                        (

                            <div className="widget-empty">

                                No existen conversaciones.

                            </div>

                        )

                        :

                        (

                            conversations.map((conversation) => (

                                <button

                                    key={conversation.id}

                                    className="conversation-item"

                                    onClick={() => setSelectedConversation(conversation)}

                                >

                                    <div className="conversation-avatar">

                                        <MessageCircle size={20} />

                                    </div>

                                    <div className="conversation-content">

                                        <strong>

                                            {conversation.contact_name || "Sin nombre"}

                                        </strong>

                                        <span>

                                            {conversation.lastMessage}

                                        </span>

                                    </div>

                                    <small>

                                        {conversation.date}

                                    </small>

                                </button>

                            ))

                        )

            }

            <ConversationModal

                client={selectedConversation}

                onClose={() => setSelectedConversation(null)}

            />

        </Card>

    );

}

export default RecentConversations;