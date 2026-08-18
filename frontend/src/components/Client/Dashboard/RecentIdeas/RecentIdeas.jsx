import { Lightbulb, ArrowRight, CalendarDays } from "lucide-react";
import { Link } from "react-router-dom";

import Card from "../../../Card/card";

import "./RecentIdeas.css";

function RecentIdeas({

    ideas = [],

    loading

}) {

    function getPriorityClass(priority) {

        switch (priority?.toLowerCase()) {

            case "alta":
                return "priority-high";

            case "media":
                return "priority-medium";

            case "baja":
                return "priority-low";

            default:
                return "";

        }

    }

    return (

        <Card>

            <div className="widget-header">

                <div>

                    <h3>

                        Ideas recientes

                    </h3>

                    <p>

                        Detectadas automáticamente por IA

                    </p>

                </div>

                <Link

                    to="/client/ideas"

                    className="widget-link"

                >

                    Ver todas

                    <ArrowRight size={16} />

                </Link>

            </div>

            {

                loading ?

                    (

                        <div className="widget-loading">

                            Analizando ideas...

                        </div>

                    )

                    :

                    ideas.length === 0 ?

                        (

                            <div className="widget-empty">

                                No hay ideas registradas.

                            </div>

                        )

                        :

                        (

                            ideas.map((idea) => (

                                <Link

                                    key={idea.id}

                                    to="/client/ideas"

                                    className="idea-item"

                                >

                                    <div className="idea-icon">

                                        <Lightbulb size={20} />

                                    </div>

                                    <div className="idea-content">

                                        <strong>

                                            {idea.title}

                                        </strong>

                                        <div className="idea-date">

                                            <CalendarDays size={14} />

                                            {idea.created_at}

                                        </div>

                                    </div>

                                    <div

                                        className={`idea-priority ${getPriorityClass(idea.priority)}`}

                                    >

                                        {idea.priority}

                                    </div>

                                </Link>

                            ))

                        )

            }

        </Card>

    );

}

export default RecentIdeas;