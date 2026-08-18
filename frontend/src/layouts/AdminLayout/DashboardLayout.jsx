import "./DashboardLayout.css";

import Sidebar from "../../components/Sidebar/Sidebar";
import Topbar from "../../components/Topbar/Topbar";

function DashboardLayout({

    children,

    menu,

    title

}) {

    return (

        <div className="dashboard">

            <Sidebar menu={menu} />

            <div className="dashboard-content">

                <Topbar title={title} />

                <main className="dashboard-main">

                    {children}

                </main>

            </div>

        </div>

    );

}

export default DashboardLayout;