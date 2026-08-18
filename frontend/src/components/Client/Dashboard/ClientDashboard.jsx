import { useEffect, useState } from "react";

import "./Dashboards.css";

import dashboardService from "../../../services/dashboardService";

import AISummary from "./AISummary/AISummary";
import DashboardStats from "./DashboardStats/ClientDashboardStats";
import RecentConversations from "./RecentConversations/RecentConversations";
import RecentIdeas from "./RecentIdeas/RecentIdeas";
import RecentDocuments from "./RecentDocuments/RecentDocuments";
import WhatsAppStatus from "./WhatsAppStatus/WhatsAppStatus";

function ClientDashboard() {

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    async function loadDashboard() {

        try {

            const data = await dashboardService.getDashboard();

            setDashboard(data);

        }

        catch (err) {

            console.error(err);

        }

        finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        loadDashboard();

    }, []);

    if (loading) {

        return (

            <div className="client-dashboard">

                <div className="dashboard-loading">

                    Cargando Dashboard...

                </div>

            </div>

        );

    }

    if (!dashboard) {

        return (

            <div className="client-dashboard">

                <div className="dashboard-error">

                    No se pudo cargar el Dashboard.

                </div>

            </div>

        );

    }

    return (

        <div className="client-dashboard">

            <AISummary
                summary={dashboard.summary}
            />

            <DashboardStats
                stats={dashboard.stats}
            />

            <section className="dashboard-grid">

                <RecentConversations
                    conversations={dashboard.recentConversations}
                />

                <WhatsAppStatus
                    whatsapp={dashboard.whatsapp}
                />

                <RecentIdeas
                    ideas={dashboard.recentIdeas}
                />

                <RecentDocuments
                    documents={dashboard.recentDocuments}
                />

            </section>

        </div>

    );

}

export default ClientDashboard;