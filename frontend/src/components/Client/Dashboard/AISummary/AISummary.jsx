import { Sparkles, Bot } from "lucide-react";

import Card from "../../../Card/card";

import "./AISummary.css";

function AISummary({

    summary,

    loading

}) {

    return (

        <Card className="ai-summary-card">

            <div className="ai-summary-header">

                <div className="ai-summary-icon">

                    <Bot size={26} />

                </div>

                <div>

                    <h2>

                        Informe Ejecutivo

                    </h2>

                    <span>

                        Generado por Inteligencia Artificial

                    </span>

                </div>

            </div>

            {

                loading

                    ?

                    (

                        <div className="ai-summary-loading">

                            <Sparkles size={20} />

                            Analizando información...

                        </div>

                    )

                    :

                    (

                        <div className="ai-summary-content">

                            <p>

                                {summary}

                            </p>

                        </div>

                    )

            }

        </Card>

    );

}

export default AISummary;