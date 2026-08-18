import { useState } from "react";

import ConversationList from "./ConversationList/ConversationList";
import ConversationChat from "./ConversationChat/ConversationChat";

import "./Conversation.css";

function Conversations() {

    const [selectedContact, setSelectedContact] = useState(null);

    return (

        <div className="conversations-page">

            <ConversationList
                selectedContact={selectedContact}
                onSelectContact={setSelectedContact}
            />

            <ConversationChat
                contact={selectedContact}
            />

        </div>

    );

}

export default Conversations;