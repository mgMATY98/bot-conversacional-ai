import { useState, useEffect } from "react";

import Modal from "../../../Modal/Modal";
import Input from "../../../Input/Input";
import Button from "../../../Button/Button";

import adminService from "../../../../services/adminService";

import toast from "react-hot-toast";

import {

    Building2,
    User,
    Lock,
    Eye,
    EyeOff,
    Phone

} from "lucide-react";

function EditClientModal({

    open,
    onClose,
    client,
    onSuccess

}) {

    const [showPassword, setShowPassword] = useState(false);

    const [form, setForm] = useState({

        organization_name: "",
        representative_name: "",
        representative_role: "",

        municipality: "",
        province: "",

        bot_phone: "",

        password: ""

    });

    useEffect(() => {

        if (!client) return;

        setForm({

            organization_name: client.organization_name || "",

            representative_name: client.representative_name || "",

            representative_role: client.representative_role || "",

            municipality: client.municipality || "",

            province: client.province || "",

            bot_phone: client.bot_phone || "",

            password: ""

        });

        setShowPassword(false);

    }, [client]);

    function handleChange(e) {

        setForm(prev => ({

            ...prev,

            [e.target.name]: e.target.value

        }));

    }

    async function handleSave() {

        if (!client) return;

        try {

            const data = {

                organization_name: form.organization_name,

                representative_name: form.representative_name,

                representative_role: form.representative_role,

                municipality: form.municipality,

                province: form.province,

                bot_phone: form.bot_phone

            };

            if (form.password.trim()) {

                data.password = form.password;

            }

            await adminService.updateClient(

                client.id,

                data

            );

            toast.success("Cliente actualizado correctamente");

            onSuccess?.();

        }
        catch (err) {

            console.error(err);

            toast.error(

                err.response?.data?.detail ||

                "No se pudo actualizar el cliente"

            );

        }

    }

    return (

        <Modal

            open={open}

            title="Editar Cliente"

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

                        onClick={handleSave}

                    >

                        Guardar Cambios

                    </Button>

                </>

            }

        >

            <h3>🏢 Organización</h3>

            <Input

                label="Organización"

                name="organization_name"

                icon={Building2}

                value={form.organization_name}

                onChange={handleChange}

            />

            <Input

                label="Municipio"

                name="municipality"

                icon={Building2}

                value={form.municipality}

                onChange={handleChange}

            />

            <Input

                label="Provincia"

                name="province"

                icon={Building2}

                value={form.province}

                onChange={handleChange}

            />

            <h3>👤 Representante</h3>

            <Input

                label="Nombre del representante"

                name="representative_name"

                icon={User}

                value={form.representative_name}

                onChange={handleChange}

            />

            <Input

                label="Cargo"

                name="representative_role"

                icon={User}

                value={form.representative_role}

                onChange={handleChange}

            />

            <h3>📱 WhatsApp</h3>

            <Input

                label="Número del Bot"

                name="bot_phone"

                icon={Phone}

                value={form.bot_phone}

                onChange={handleChange}

            />

            <h3>🔐 Seguridad</h3>

            <Input

                label="Nueva contraseña"

                type={showPassword ? "text" : "password"}

                name="password"

                icon={Lock}

                value={form.password}

                onChange={handleChange}

                placeholder="Dejar vacío para mantener la actual"

                rightIcon={

                    showPassword

                        ?

                        <EyeOff

                            size={18}

                            onClick={() => setShowPassword(false)}

                        />

                        :

                        <Eye

                            size={18}

                            onClick={() => setShowPassword(true)}

                        />

                }

            />

        </Modal>

    );

}

export default EditClientModal;