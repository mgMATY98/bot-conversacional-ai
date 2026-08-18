import { useEffect, useState } from "react";

import DashboardStats from "./DashboardStats/DashboardStats";
import ClientList from "./ClientList/ClientList";

import CreateClientModal from "../../Client/CreateClientModal";
import EditClientModal from "../../Client/EditClientModal";
import DeleteClientModal from "../../Client/DeleteClientModal";

import adminService from "../../../../services/adminService";

function AdminDashboard() {

    const [clients, setClients] = useState([]);

    const [openCreateModal, setOpenCreateModal] = useState(false);

    const [openEditModal, setOpenEditModal] = useState(false);

    const [openDeleteModal, setOpenDeleteModal] = useState(false);

    const [selectedClient, setSelectedClient] = useState(null);

    async function reloadClients() {

        try {

            const data = await adminService.getClients();

            setClients(data);

        }
        catch (err) {

            console.error(err);

        }

    }

    useEffect(() => {

        reloadClients();

    }, []);

    useEffect(() => {

        function handleOpenCreate() {

            setOpenCreateModal(true);

        }

        window.addEventListener(
            "open-create-client",
            handleOpenCreate
        );

        return () => {

            window.removeEventListener(
                "open-create-client",
                handleOpenCreate
            );

        };

    }, []);

    return (

        <div className="admin-dashboard">

            <DashboardStats
                clients={clients}
            />

            <div id="clients-section">

                <ClientList

                    clients={clients}

                    reloadClients={reloadClients}

                    onCreate={() => setOpenCreateModal(true)}

                    onEdit={(client) => {

                        setSelectedClient(client);

                        setOpenEditModal(true);

                    }}

                    onDelete={(client) => {

                        setSelectedClient(client);

                        setOpenDeleteModal(true);

                    }}

                />

            </div>

            <CreateClientModal

                open={openCreateModal}

                onClose={() => setOpenCreateModal(false)}

                onSuccess={() => {

                    reloadClients();

                    setOpenCreateModal(false);

                }}

            />

            <EditClientModal

                open={openEditModal}

                client={selectedClient}

                onClose={() => {

                    setOpenEditModal(false);

                    setSelectedClient(null);

                }}

                onSuccess={() => {

                    reloadClients();

                    setOpenEditModal(false);

                }}

            />

            <DeleteClientModal

                open={openDeleteModal}

                client={selectedClient}

                onClose={() => {

                    setOpenDeleteModal(false);

                    setSelectedClient(null);

                }}

                onSuccess={() => {

                    reloadClients();

                    setOpenDeleteModal(false);

                }}

            />

        </div>

    );

}

export default AdminDashboard;