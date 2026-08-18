import Card from "../../../../Card/Card";

import "./DashboardStats.css";

function DashboardStats({ clients }) {

    const totalClients = clients.length;

    const activeBots = clients.filter(
        (client) => client.active
    ).length;

    return (

        <div className="stats-grid">

            <Card>

                <h3>Clientes</h3>

                <h1>{totalClients}</h1>

            </Card>

            <Card>

                <h3>Bots Activos</h3>

                <h1>{activeBots}</h1>

            </Card>

        </div>

    );

}

export default DashboardStats;