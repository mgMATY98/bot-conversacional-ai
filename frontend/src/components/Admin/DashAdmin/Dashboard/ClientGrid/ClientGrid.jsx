import "./ClientGrid.css";
import EmptyState from "../../../../EmptyState/EmptyState";
import ClientCard from "../ClientCard/ClientCard";
function ClientGrid({
    clients,
    onEdit,
    onDelete,
    onToggleStatus,
    onChangeWhatsAppChannel
}) {

    if (clients.length === 0) {

        return (

            <EmptyState

                title="No se encontraron clientes"

                description="Intente otra búsqueda."

            />

        );

    }

    return (

        <div className="client-grid">

            {clients.map((client) => (

                <ClientCard

                    key={client.id}

                    client={client}

                    onEdit={onEdit}

                    onDelete={onDelete}

                    onToggleStatus={onToggleStatus}

                    onChangeWhatsAppChannel={
                        onChangeWhatsAppChannel
                    }

                />

            ))}

        </div>

    );

}

export default ClientGrid;