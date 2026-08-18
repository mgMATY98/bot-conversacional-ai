import { useEffect, useState } from "react";

import api from "../../../../services/api";

import ConversationItem from "../ConversationItem/ConversationItem";

import "./ConversationList.css";

function ConversationList({

    selectedContact,

    onSelectContact,

}) {

    const [contacts, setContacts] = useState([]);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        loadContacts();

    }, []);

    async function loadContacts() {

        try {

            const { data } = await api.get("/contacts");

            setContacts(data);

        }

        catch (error) {

            console.error(error);

        }

        finally {

            setLoading(false);

        }

    }

    return (

        <div className="conversation-list">

            <div className="conversation-list-header">

                <h2>

                    Conversaciones

                </h2>

            </div>

            {

                loading ?

                    (

                        <p>

                            Cargando...

                        </p>

                    )

                    :

                    contacts.map(contact => (

                        <ConversationItem

                            key={contact.id}

                            contact={contact}

                            active={selectedContact?.id === contact.id}

                            onClick={() => onSelectContact(contact)}

                        />

                    ))

            }

        </div>

    );

}

export default ConversationList;