import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import AuthLayout from "../layouts/AdminLayout/AuthLayout";
import Card from "../components/Card/Card";
import Input from "../components/Input/Input";
import Button from "../components/Button/Button";

import api from "../services/api";
import { setToken } from "../utils/token";

const MAX_ATTEMPTS = 5;

function LoginPage() {

    const navigate = useNavigate();

    const [credentials, setCredentials] = useState({
        username: "",
        password: ""
    });

    const [attempts, setAttempts] = useState(0);

    const [isBlocked, setIsBlocked] = useState(false);

    const [lockoutTime, setLockoutTime] = useState(0);

    useEffect(() => {

        let timer;

        if (isBlocked && lockoutTime > 0) {

            timer = setTimeout(() => {

                setLockoutTime(prev => prev - 1);

            }, 1000);

        }

        if (isBlocked && lockoutTime === 0) {

            setAttempts(0);

            setIsBlocked(false);

        }

        return () => clearTimeout(timer);

    }, [isBlocked, lockoutTime]);

    function handleInputChange(e) {

        const { name, value } = e.target;

        setCredentials(prev => ({
            ...prev,
            [name]: value
        }));

    }

    async function login() {

        if (isBlocked) return;

        try {

            const { data } = await api.post("/auth/login", credentials);

            setToken(data.access_token);

            localStorage.setItem("role", data.role);

            if (data.role === "admin") {

                navigate("/admin", { replace: true });

            }
            else {

                navigate("/client", { replace: true });

            }

            setCredentials({

                username: "",

                password: ""

            });

        } catch (error) {

            if (!error.response) {

                alert("No se pudo conectar con el servidor.");

                return;

            }

            const next = attempts + 1;

            setAttempts(next);

            if (next >= MAX_ATTEMPTS) {

                setIsBlocked(true);

                setLockoutTime(30);

                alert("Demasiados intentos.");

            } else {

                alert(

                    `Intentos restantes: ${MAX_ATTEMPTS - next}`

                );

            }

        }

    }

    return (

        <AuthLayout>

            <Card title="Iniciar sesión">

                <form

                    onSubmit={(e) => {

                        e.preventDefault();

                        login();

                    }}

                >

                    <Input

                        label="Usuario"

                        name="username"

                        placeholder="Ingresá tu usuario"

                        value={credentials.username}

                        onChange={handleInputChange}

                        disabled={isBlocked}

                    />

                    <div style={{ height: 16 }} />

                    <Input

                        label="Contraseña"

                        type="password"

                        name="password"

                        placeholder="Ingresá tu raseña"

                        value={credentials.password}

                        onChange={handleInputChange}

                        disabled={isBlocked}

                    />

                    <div style={{ height: 24 }} />

                    <Button

                        fullWidth

                        type="submit"

                        disabled={isBlocked}

                    >

                        {

                            isBlocked

                                ?

                                `Bloqueado (${lockoutTime}s)`

                                :

                                "Ingresar"

                        }

                    </Button>

                </form>

            </Card>

        </AuthLayout>

    );

}

export default LoginPage;