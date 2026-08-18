import { useEffect, useState } from "react";

import {
    Bot,
    Brain,
    Target,
    FileText,
    MessageSquare,
    Shield,
} from "lucide-react";

import api from "../../../services/api";

import BehaviorCard from "./BehaviorCard";
import BehaviorField from "./BehaviorField";

import "./Behavior.css";

function BehaviorSection() {

    const emptyConfig = {
        assistant_name: "",
        personality: "",
        objective: "",
        additional_instructions: "",
        welcome_message: "",
        farewell_message: "",
        forbidden_topics: "",
        forbidden_words: "",
        political_campaigns: false,
    };

    const [config, setConfig] = useState(emptyConfig);

    const [originalConfig, setOriginalConfig] = useState(emptyConfig);
    // ==========================================================
    // LOAD
    // ==========================================================

    useEffect(() => {

        loadConfig();

    }, []);

    async function loadConfig() {

        try {

            const { data } = await api.get("/bot-config");

            console.log(data);

            setConfig(data);

            setOriginalConfig(data);

        }

        catch (error) {

            console.error(error);

            alert("No se pudo cargar la configuración.");

        }

    }
    // ==========================================================
    // UPDATE FIELD
    // ==========================================================

    function updateField(field, value) {
        setConfig(prev => {
            let updated = { ...prev, [field]: value };

            // Si cambian el nombre, actualizamos dinámicamente cualquier texto que use {assistant_name}
            if (field === "assistant_name") {
                // Si la personalidad tiene la etiqueta, la reemplazamos con el nuevo nombre
                if (updated.personality.includes("{assistant_name}")) {
                    updated.personality = updated.personality.replaceAll("{assistant_name}", value);
                }
            }
            return updated;
        });
    }
    const hasChanges =
        JSON.stringify(config) !==
        JSON.stringify(originalConfig);
    // ==========================================================
    // SAVE
    // ==========================================================

    async function saveConfig() {

        try {

            await api.put("/bot-config", config);

            setOriginalConfig(config);

            alert("Configuración guardada correctamente.");

        }

        catch (error) {

            console.error(error);

            alert("No se pudo guardar la configuración.");

        }

    }

    return (

        <div className="behavior-section">

            <h1>Comportamiento del Bot</h1>

            {/* ===================================================== */}

            <BehaviorCard
                icon={Bot}
                title="Identidad"
            >

                <BehaviorField

                    label="Nombre del asistente"

                    field="assistant_name"

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>

            {/* ===================================================== */}

            <BehaviorCard
                icon={Brain}
                title="Personalidad"
            >

                <BehaviorField

                    label="Definí cómo responderá el asistente."

                    field="personality"

                    multiline

                    rows={7}

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>

            {/* ===================================================== */}

            <BehaviorCard
                icon={Target}
                title="Objetivo"
            >

                <BehaviorField

                    label="Objetivo principal del asistente."

                    field="objective"

                    multiline

                    rows={5}

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>

            {/* ===================================================== */}

            <BehaviorCard
                icon={FileText}
                title="Instrucciones Adicionales"
            >

                <BehaviorField

                    label="Indicaciones especiales para el asistente."

                    field="additional_instructions"

                    multiline

                    rows={6}

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>

            {/* ===================================================== */}

            <BehaviorCard
                icon={MessageSquare}
                title="Mensajes"
            >

                <BehaviorField

                    label="Mensaje de bienvenida"

                    field="welcome_message"

                    multiline

                    rows={4}

                    config={config}

                    updateField={updateField}

                />

                <BehaviorField

                    label="Mensaje de despedida"

                    field="farewell_message"

                    multiline

                    rows={4}

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>

            {/* ===================================================== */}

            <BehaviorCard
                icon={Shield}
                title="Moderación"
            >

                <BehaviorField

                    label="Temas prohibidos"

                    field="forbidden_topics"

                    multiline

                    rows={4}

                    placeholder="Ej: Política partidaria, religión..."

                    config={config}

                    updateField={updateField}

                />

                <BehaviorField

                    label="Palabras prohibidas"

                    field="forbidden_words"

                    multiline

                    rows={4}

                    placeholder="Separadas por coma"

                    config={config}

                    updateField={updateField}

                />

            </BehaviorCard>
            <div className="behavior-footer">

                <div className="behavior-status">

                    {

                        hasChanges

                            ?

                            <span className="status-warning">

                                ● Hay cambios sin guardar

                            </span>

                            :

                            <span className="status-ok">

                                ✓ Todos los cambios guardados

                            </span>

                    }

                </div>

                <button

                    className="save-all-button"

                    disabled={!hasChanges}

                    onClick={saveConfig}

                >

                    Guardar todos los cambios

                </button>

            </div>
        </div>

    );

}

export default BehaviorSection;