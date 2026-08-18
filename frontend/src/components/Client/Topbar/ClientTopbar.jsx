import "./ClientTopbar.css";
import { UserCircle, LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function ClientTopbar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("role");
        navigate("/");
    };

    return (
        <header className="client-topbar">

            <div className="client-topbar-left">

                <h2>Panel del Cliente</h2>

                <p>

                    Administrá tu asistente inteligente

                </p>

            </div>

            <div className="client-topbar-right">

                <div className="client-user">

                    <UserCircle size={24} />

                    <span>

                        Cliente

                    </span>

                </div>

                <button
                    className="logout-btn"
                    onClick={handleLogout}
                >

                    <LogOut size={18} />

                    Cerrar sesión

                </button>

            </div>

        </header>
    );
}