import { useEffect, useState } from "react";
import "./Ideas.css";

import api from "../../../services/api";
import { useSearchParams } from "react-router-dom";
import IdeaTable from "./IdeaTable";
import IdeaModal from "./IdeaModal";

import { Plus } from "lucide-react";

export default function Ideas() {

    const [ideas, setIdeas] = useState([]);

    const [loading, setLoading] = useState(true);

    const [openModal, setOpenModal] = useState(false);

    const [selectedIdea, setSelectedIdea] = useState(null);
    const [searchParams] = useSearchParams();

    async function loadIdeas() {

        try {

            const response = await api.get("/ideas");

            setIdeas(response.data);

        } catch (err) {

            console.error(err);

        } finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        loadIdeas();

    }, []);
    useEffect(() => {

        if (!ideas.length) return;

        const id = searchParams.get("id");

        if (!id) return;

        const idea = ideas.find(

            i => i.id === Number(id)

        );

        if (!idea) return;

        setSelectedIdea(idea);

        setOpenModal(true);

    }, [

        ideas,

        searchParams

    ]);
    return (

        <div className="ideas-page">

            <div className="ideas-header">

                <div>

                    <h1>Ideas</h1>

                    <p>
                        Administrá ideas, sugerencias y mejoras para el asistente.
                    </p>

                </div>

                <button
                    className="new-idea-btn"
                    onClick={() => {

                        setSelectedIdea(null);

                        setOpenModal(true);

                    }}
                >

                    <Plus size={18} />

                    Nueva Idea

                </button>

            </div>

            <IdeaTable
                ideas={ideas}
                onOpen={(idea) => {

                    setSelectedIdea(idea);
                    setOpenModal(true);

                }}
            />

            <IdeaModal
                open={openModal}
                onClose={() => setOpenModal(false)}
                reload={loadIdeas}
                idea={selectedIdea}
            />

        </div>

    );

}