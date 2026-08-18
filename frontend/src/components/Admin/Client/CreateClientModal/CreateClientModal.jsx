import { useState } from "react";

import Modal from "../../../Modal/Modal";
import Input from "../../../Input/Input";
import Button from "../../../Button/Button";

import toast from "react-hot-toast";

import adminService from "../../../../services/adminService";

import {
    Building2,
    User,
    Lock,
    Eye,
    EyeOff,
    Phone
} from "lucide-react";

function CreateClientModal({

    open,
    onClose,
    onSuccess

}) {

    const [showPassword, setShowPassword] = useState(false);

    const [form, setForm] = useState({

        username: "",
        password: "",

        organization_name: "",
        representative_name: "",
        representative_role: "",

        municipality: "",
        province: "",

        bot_phone: ""

    });

    const [errors, setErrors] = useState({});

    function resetForm() {

        setForm({

            username: "",
            password: "",

            organization_name: "",
            representative_name: "",
            representative_role: "",

            municipality: "",
            province: "",

            bot_phone: ""

        });

        setErrors({});

        setShowPassword(false);

    }

    function handleChange(e) {

        setForm(prev => ({

            ...prev,

            [e.target.name]: e.target.value

        }));

    }

    function validate() {

        const newErrors = {};

        if (!form.organization_name.trim())
            newErrors.organization_name = "Ingrese la organización";

        if (!form.representative_name.trim())
            newErrors.representative_name = "Ingrese el nombre del representante";

        if (!form.representative_role.trim())
            newErrors.representative_role = "Ingrese el cargo";

        if (!form.municipality.trim())
            newErrors.municipality = "Ingrese el municipio";

        if (!form.province.trim())
            newErrors.province = "Ingrese la provincia";

        if (!form.bot_phone.trim())
            newErrors.bot_phone = "Ingrese el teléfono del bot";

        if (!form.username.trim())
            newErrors.username = "Ingrese un usuario";

        if (form.password.length < 8)
            newErrors.password = "La contraseña debe tener al menos 8 caracteres";

        setErrors(newErrors);

        return Object.keys(newErrors).length === 0;

    }

    async function handleCreate() {

        if (!validate()) return;

        try {

            await adminService.createClient(form);

            toast.success("Cliente creado correctamente");

            resetForm();

            onSuccess?.();

        }
        catch (err) {

            console.error(err);

            toast.error(

                err.response?.data?.detail ||

                "No se pudo crear el cliente"

            );

        }

    }

    return (

        <Modal

            open={open}

            title="Nuevo Cliente"

            onClose={() => {

                resetForm();

                onClose();

            }}

            footer={

                <>

                    <Button

                        variant="outline"

                        onClick={() => {

                            resetForm();

                            onClose();

                        }}

                    >

                        Cancelar

                    </Button>

                    <Button

                        onClick={handleCreate}

                    >

                        Crear Cliente

                    </Button>

                </>

            }

        >

            <h3 style={{ marginTop: 0 }}>🏢 Organización</h3>

            <Input
                label="Organización"
                required
                name="organization_name"
                icon={Building2}
                value={form.organization_name}
                onChange={handleChange}
                error={errors.organization_name}
                placeholder="Organización"
            />

            <Input
                label="Municipio"
                required
                name="municipality"
                icon={Building2}
                value={form.municipality}
                onChange={handleChange}
                error={errors.municipality}
                placeholder="Municipio"
            />

            <Input
                label="Provincia"
                required
                name="province"
                icon={Building2}
                value={form.province}
                onChange={handleChange}
                error={errors.province}
                placeholder="Provincia"
            />

            <h3>👤 Representante</h3>

            <Input
                label="Nombre del representante"
                required
                name="representative_name"
                icon={User}
                value={form.representative_name}
                onChange={handleChange}
                error={errors.representative_name}
                placeholder="Nombre del representante"
            />

            <Input
                label="Cargo"
                required
                name="representative_role"
                icon={User}
                value={form.representative_role}
                onChange={handleChange}
                error={errors.representative_role}
                placeholder="Cargo"
            />

            <h3>📱 WhatsApp</h3>

            <Input
                label="Número del Bot"
                required
                name="bot_phone"
                icon={Phone}
                value={form.bot_phone}
                onChange={handleChange}
                error={errors.bot_phone}
                placeholder="54911..."
            />

            <h3>🔐 Acceso</h3>

            <Input
                label="Usuario"
                required
                name="username"
                icon={User}
                value={form.username}
                onChange={handleChange}
                error={errors.username}
                placeholder="Usuario"
            />

            <Input
                label="Contraseña"
                required
                type={showPassword ? "text" : "password"}
                name="password"
                icon={Lock}
                value={form.password}
                onChange={handleChange}
                error={errors.password}
                placeholder="********"
                rightIcon={
                    showPassword
                        ? (
                            <EyeOff
                                size={18}
                                onClick={() => setShowPassword(false)}
                            />
                        )
                        : (
                            <Eye
                                size={18}
                                onClick={() => setShowPassword(true)}
                            />
                        )
                }
            />

        </Modal>

    );

}

export default CreateClientModal;