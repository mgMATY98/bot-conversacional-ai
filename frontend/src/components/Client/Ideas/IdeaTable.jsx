import {
    Eye
} from "lucide-react";

import "./IdeaTable.css";

function IdeaTable({

    ideas,

    search,

    onOpen

}) {

    const filteredIdeas = ideas.filter((idea) => {

        if (!search) return true;

        const value = search.toLowerCase();

        return (

            idea.contact_name?.toLowerCase().includes(value) ||

            idea.contact_phone?.toLowerCase().includes(value) ||

            idea.summary?.toLowerCase().includes(value) ||

            idea.original_message?.toLowerCase().includes(value)

        );

    });

    return (

        <div className="idea-table-container">

            <table className="idea-table">

                <thead>

                    <tr>

                        <th>Usuario</th>

                        <th>Teléfono</th>

                        <th>Resumen</th>

                        <th>Categoría</th>

                        <th>Estado</th>

                        <th>Prioridad</th>

                        <th></th>

                    </tr>

                </thead>

                <tbody>

                    {

                        filteredIdeas.map((idea) => (

                            <tr key={idea.id}>

                                <td>

                                    {idea.contact_name || "-"}

                                </td>

                                <td>

                                    {idea.contact_phone || "-"}

                                </td>

                                <td className="summary-column">

                                    {idea.summary}

                                </td>

                                <td>

                                    {idea.category}

                                </td>

                                <td>

                                    <span className={`status ${idea.status}`}>

                                        {idea.status}

                                    </span>

                                </td>

                                <td>

                                    <span className={`priority ${idea.priority}`}>

                                        {idea.priority}

                                    </span>

                                </td>

                                <td>

                                    <button

                                        className="view-button"

                                        onClick={() => onOpen(idea)}

                                    >

                                        <Eye size={18} />

                                    </button>

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    );

}

export default IdeaTable;