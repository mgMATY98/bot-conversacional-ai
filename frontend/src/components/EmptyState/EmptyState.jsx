import "./EmptyState.css";

import { SearchX } from "lucide-react";

function EmptyState({

    title,

    description

}) {

    return (

        <div className="empty-state">

            <SearchX size={64} />

            <h3>{title}</h3>

            <p>{description}</p>

        </div>

    );

}

export default EmptyState;