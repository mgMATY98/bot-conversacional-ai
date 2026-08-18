import { useState } from "react";

import { Search } from "lucide-react";

import Input from "../../../../Input/Input";
import Card from "../../../../Card/Card";
import Button from "../../../../Button/Button";

import ClientGrid from "../ClientGrid/ClientGrid";

import adminService from "../../../../../services/adminService";

import toast from "react-hot-toast";


function ClientList({

    clients,

    reloadClients,

    onCreate,

    onEdit,

    onDelete

}) {

    const [search, setSearch] = useState("");


    // ==========================================================
    // ACTIVAR / DESACTIVAR CLIENTE
    // ==========================================================

    async function handleToggleStatus(client) {

        try {

            await adminService.toggleClient(

                client.id,

                !client.active

            );

            toast.success(

                client.active
                    ? "Cliente desactivado"
                    : "Cliente activado"

            );

            reloadClients();

        }

        catch (err) {

            console.error(err);

            toast.error(
                "No se pudo actualizar el estado"
            );

        }

    }


    // ==========================================================
    // CAMBIAR CANAL WHATSAPP
    // ==========================================================

    async function handleChangeWhatsAppChannel(client) {

        const newChannel =
            client.active_channel === "whatsapp_cloud"
                ? "whatsapp_web"
                : "whatsapp_cloud";


        try {

            await adminService.changeWhatsAppChannel(

                client.id,

                newChannel

            );


            toast.success(

                newChannel === "whatsapp_cloud"

                    ? "WhatsApp cambiado a Meta Cloud"

                    : "WhatsApp cambiado a WhatsApp Web"

            );


            reloadClients();

        }

        catch (err) {

            console.error(err);


            const message =
                err?.response?.data?.detail ||
                "No se pudo cambiar el canal de WhatsApp";


            toast.error(message);

        }

    }


    // ==========================================================
    // FILTRAR CLIENTES
    // ==========================================================

    const filteredClients = clients.filter((client) => {

        const text = search.toLowerCase();

        return (

            client.organization_name
                .toLowerCase()
                .includes(text)

            ||

            client.username
                .toLowerCase()
                .includes(text)

        );

    });


    return (

        <Card

            title="Clientes"

            subtitle="Empresas registradas"

            actions={

                <div className="client-list-actions">

                    <Input

                        placeholder="Buscar cliente..."

                        icon={Search}

                        value={search}

                        onChange={(e) =>
                            setSearch(e.target.value)
                        }

                        fullWidth={false}

                    />


                    <Button

                        size="sm"

                        onClick={onCreate}

                    >

                        Nuevo Cliente

                    </Button>

                </div>

            }

        >

            <ClientGrid

                clients={filteredClients}

                onEdit={onEdit}

                onDelete={onDelete}

                onToggleStatus={handleToggleStatus}

                onChangeWhatsAppChannel={
                    handleChangeWhatsAppChannel
                }

            />

        </Card>

    );

}


export default ClientList;