import "./ClientCard.css";

import Button from "../../../../Button/Button";

import {
    Building2,
    User,
    Bot,
    MapPin,
    Phone,
    Pencil,
    Trash2,
    Power
} from "lucide-react";

function ClientCard({

    client,
    onEdit,
    onDelete,
    onToggleStatus,
    onChangeWhatsAppChannel
}) {

    return (

        <div className="client-card">

            <div className="client-card-header">

                <div>

                    <h3>{client.organization_name}</h3>

                    <span className={client.active ? "status active" : "status inactive"}>

                        {client.active ? "Activo" : "Inactivo"}

                    </span>

                </div>

                <Building2 size={32} />

            </div>

            <div className="client-card-body">

                <div className="info">

                    <User size={18} />

                    <span>{client.username}</span>

                </div>

                <div className="info">

                    <User size={18} />

                    <span>{client.representative_name}</span>

                </div>

                <div className="info">

                    <Bot size={18} />

                    <span>{client.active ? "Bot habilitado" : "Bot deshabilitado"}</span>

                </div>

                <div className="info">

                    <MapPin size={18} />

                    <span>

                        {client.municipality}, {client.province}

                    </span>

                </div>

                <div className="info">

                    <Phone size={18} />

                    <span>{client.bot_phone}</span>

                </div>
                <div className="info">

                    <Bot size={18} />

                    <span>
                        WhatsApp:{" "}
                        {client.active_channel === "whatsapp_cloud"
                            ? "Meta Cloud"
                            : "WhatsApp Web"}
                    </span>

                </div>

            </div>

            <div className="client-card-actions">

                <Button

                    variant="outline"

                    size="sm"

                    onClick={() => onEdit(client)}

                >

                    <Pencil size={18} />

                </Button>

                <Button

                    variant={client.active ? "danger" : "success"}

                    size="sm"

                    onClick={() => onToggleStatus(client)}

                >

                    <Power size={18} />

                </Button>

                <Button

                    variant="danger"

                    size="sm"

                    onClick={() => onDelete(client)}

                >

                    <Trash2 size={18} />

                </Button>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => onChangeWhatsAppChannel(client)}
                >
                    {client.active_channel === "whatsapp_cloud"
                        ? "Volver a Web"
                        : "Cambiar a Meta"
                    }
                </Button>

            </div>

        </div>

    );

}

export default ClientCard;