import { Smartphone, Wifi, WifiOff, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";

import Card from "../../../Card/card";

import "./WhatsAppStatus.css";

function WhatsAppStatus({

    whatsapp,

    loading

}) {

    if (loading) {

        return (

            <Card>

                <h3>WhatsApp</h3>

                <p>Cargando...</p>

            </Card>

        );

    }

    return (

        <Card>

            <div className="widget-header">

                <h3>

                    Estado de WhatsApp

                </h3>

                <Link

                    to="/client/whatsapp"

                    className="widget-link"

                >

                    Administrar

                    <ArrowRight size={16} />

                </Link>

            </div>

            <div className="whatsapp-status">

                <div className="whatsapp-status-icon">

                    {

                        whatsapp.connected

                            ?

                            <Wifi size={26} />

                            :

                            <WifiOff size={26} />

                    }

                </div>

                <div className="whatsapp-status-info">

                    <strong>

                        {

                            whatsapp.connected

                                ?

                                "Conectado"

                                :

                                "Desconectado"

                        }

                    </strong>

                    <span>

                        <Smartphone size={15} />

                        {whatsapp.phone}

                    </span>

                    <small>

                        Última sincronización

                    </small>

                    <small>

                        {whatsapp.lastSync}

                    </small>

                </div>

            </div>

        </Card>

    );

}

export default WhatsAppStatus;