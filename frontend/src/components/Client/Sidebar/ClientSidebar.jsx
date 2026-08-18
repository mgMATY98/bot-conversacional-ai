import { NavLink, useNavigate } from "react-router-dom";

import {
    Bot,
    FileText,
    MessageCircle,
    Smartphone,
    Lightbulb,
    LogOut,
    LayoutDashboard
} from "lucide-react";

import "./ClientSidebar.css";

function ClientSidebar() {

    const navigate = useNavigate();

    function logout() {

        localStorage.removeItem("token");
        localStorage.removeItem("role");

        navigate("/");

    }

    return (

        <aside className="client-sidebar">

            <div className="sidebar-header">

                <div className="sidebar-logo">

                    🤖

                </div>

                <div>

                    <h2>Bot Conversacional</h2>

                    <span>Panel Cliente</span>

                </div>

            </div>

            <nav className="sidebar-menu">

                <NavLink
                    to="/client"
                    end
                >

                    <LayoutDashboard size={20} />

                    <span>Dashboard</span>

                </NavLink>

                <NavLink to="/client/behavior">

                    <Bot size={20} />

                    <span>Comportamiento</span>

                </NavLink>

                <NavLink to="/client/conversations">

                    <MessageCircle size={20} />

                    <span>Conversaciones</span>

                </NavLink>

                <NavLink to="/client/documents">

                    <FileText size={20} />

                    <span>Documentos</span>

                </NavLink>

                <NavLink to="/client/ideas">

                    <Lightbulb size={20} />

                    <span>Ideas</span>

                </NavLink>

                <NavLink to="/client/whatsapp">

                    <Smartphone size={20} />

                    <span>WhatsApp</span>

                </NavLink>

            </nav>

            <div className="sidebar-footer">

                <button
                    className="logout-button"
                    onClick={logout}
                >

                    <LogOut size={18} />

                    Cerrar sesión

                </button>

            </div>

        </aside>

    );

}

export default ClientSidebar;