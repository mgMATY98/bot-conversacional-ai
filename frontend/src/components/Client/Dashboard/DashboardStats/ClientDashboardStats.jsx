import {
    MessageCircle,
    Lightbulb,
    FileText,
    Smartphone,
    ArrowRight
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import Card from "../../../Card/card";

import "./ClientDashboardStats.css";

function DashboardStats({

    stats,

    loading

}) {

    const navigate = useNavigate();

    if (loading) {

        return (

            <div className="dashboard-stats">

                <Card className="dashboard-stat-card">

                    Cargando estadísticas...

                </Card>

            </div>

        );

    }

    const cards = [

        {
            title: "Conversaciones",
            value: stats.conversations,
            icon: MessageCircle,
            route: "/client/conversations",
            description: "Ciudadanos atendidos",
            color: "#2563eb"
        },
        {
            title: "Ideas",
            value: stats.ideas,
            icon: Lightbulb,
            route: "/client/ideas",
            description: "Detectadas por IA",
            color: "#f59e0b"
        },
        {
            title: "Documentos",
            value: stats.documents,
            icon: FileText,
            route: "/client/documents",
            description: "Base de conocimiento",
            color: "#10b981"
        },
        {
            title: "WhatsApp",
            value: stats.whatsappConnected
                ? "Conectado"
                : "Desconectado",
            icon: Smartphone,
            route: "/client/whatsapp",
            status: stats.whatsappConnected,
            description: "Estado actual",
            color: "#22c55e"
        }

    ];

    return (

        <div className="dashboard-stats">

            {

                cards.map((card) => {

                    const Icon = card.icon;

                    return (

                        <Card
                            key={card.title}
                            className="dashboard-stat-card"
                        >

                            <button
                                className="dashboard-stat-button"
                                onClick={() => navigate(card.route)}
                            >

                                <div className="dashboard-stat-top">

                                    <div
                                        className="dashboard-stat-icon-box"
                                        style={{ background: `${card.color}15` }}
                                    >

                                        <Icon
                                            size={20}
                                            className="dashboard-stat-icon"
                                            style={{ color: card.color }}
                                        />

                                    </div>

                                    <span className="dashboard-stat-name">

                                        {card.title}

                                    </span>

                                </div>

                                <div className="dashboard-stat-number">

                                    {

                                        card.status === undefined

                                            ?

                                            card.value

                                            :

                                            <span
                                                className={
                                                    card.status
                                                        ?
                                                        "status-connected"
                                                        :
                                                        "status-disconnected"
                                                }
                                            >

                                                {card.value}

                                            </span>

                                    }

                                </div>

                                <div className="dashboard-stat-description">

                                    {card.description}

                                </div>

                                <div className="dashboard-stat-link">

                                    Ver detalles

                                    <ArrowRight size={15} />

                                </div>

                            </button>

                        </Card>

                    );

                })

            }

        </div>

    );

}

export default DashboardStats;