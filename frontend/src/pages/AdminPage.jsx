import DashboardLayout from "../layouts/AdminLayout/DashboardLayout";

import Dashboard from "../components/Admin/DashAdmin/Dashboard/DashBoard";

function AdminPage() {

    const adminMenu = [

        {
            icon: "🏠",
            label: "Dashboard",
            onClick: () => { }
        },

        {
            icon: "👥",
            label: "Clientes",
            onClick: () => {

                const section = document.getElementById("clients-section");

                if (section) {

                    section.scrollIntoView({
                        behavior: "smooth"
                    });

                }

            }
        },

        {
            icon: "➕",
            label: "Nuevo Cliente",
            onClick: () => {

                window.dispatchEvent(
                    new Event("open-create-client")
                );

            }
        },

        {
            icon: "🚪",
            label: "Cerrar sesión",
            onClick: () => {

                localStorage.removeItem("token");
                localStorage.removeItem("role");

                window.location.href = "/";

            }
        }

    ];

    return (

        <DashboardLayout
            title="Dashboard"
            menu={adminMenu}
        >

            <Dashboard />

        </DashboardLayout>

    );

}

export default AdminPage;