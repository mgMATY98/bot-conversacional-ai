import { Outlet } from "react-router-dom";

import ClientSidebar from "../../components/Client/Sidebar/ClientSidebar";
import ClientTopbar from "../../components/Client/Topbar/ClientTopbar";

import "./ClientLayout.css";

function ClientLayout() {

    return (

        <div className="client-layout">

            <ClientSidebar />

            <div className="client-content">

                <ClientTopbar />

                <main className="client-main">

                    <Outlet />

                </main>

            </div>

        </div>

    );

}

export default ClientLayout;