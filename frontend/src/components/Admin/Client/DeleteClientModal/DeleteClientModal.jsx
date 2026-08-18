import Modal from "../../../Modal/Modal";
import Button from "../../../Button/Button";

import adminService from "../../../../services/adminService";

import { TriangleAlert } from "lucide-react";

import toast from "react-hot-toast";

import "./DeleteClientModal.css";

function DeleteClientModal({

    open,
    onClose,
    client,
    onSuccess

}) {

    async function handleDelete() {

        if (!client) return;

        try {

            await adminService.deleteClient(client.id);

            toast.success("Cliente eliminado correctamente");

            onSuccess?.();

        }
        catch (err) {

            console.error(err);

            toast.error(

                err.response?.data?.detail ||

                "No se pudo eliminar el cliente"

            );

        }

    }

    return (

        <Modal

            open={open}

            title="Eliminar Cliente"

            onClose={onClose}

            footer={

                <>

                    <Button

                        variant="outline"

                        onClick={onClose}

                    >

                        Cancelar

                    </Button>

                    <Button

                        variant="danger"

                        onClick={handleDelete}

                    >

                        Eliminar

                    </Button>

                </>

            }

        >

            <div className="delete-warning">

                <TriangleAlert size={60} />

                <h3>

                    ¿Eliminar este cliente?

                </h3>

                <p>

                    Se eliminará

                    <strong>

                        {" "}
                        {client?.organization_name}
                        {" "}

                    </strong>

                    junto con toda su información.

                </p>

                <p>

                    Esta acción no puede deshacerse.

                </p>

            </div>

        </Modal>

    );

}

export default DeleteClientModal;