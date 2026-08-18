import "./AI.css";
import { Bot, Sparkles, Send } from "lucide-react";
import { useState } from "react";
import api from "../../../services/api";

export default function AI() {
    const [prompt, setPrompt] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleAsk() {
        if (!prompt.trim()) return;

        setLoading(true);

        try {
            const res = await api.post("/ai/test", {
                prompt,
            });

            setResponse(res.data.response);
        } catch (err) {
            console.error(err);
            setResponse("No se pudo obtener una respuesta del servidor.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="ai-page">

            <div className="ai-header">
                <Bot size={36} />
                <div>
                    <h1>Asistente IA</h1>
                    <p>Probá el comportamiento del bot antes de publicarlo.</p>
                </div>
            </div>

            <div className="ai-card">

                <label>Mensaje</label>

                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Escribí un mensaje..."
                />

                <button
                    onClick={handleAsk}
                    disabled={loading}
                >
                    <Send size={18} />

                    {loading ? "Consultando..." : "Enviar"}
                </button>

            </div>

            <div className="response-card">

                <div className="response-title">
                    <Sparkles size={20} />
                    <h2>Respuesta</h2>
                </div>

                <div className="response-body">

                    {response ? (
                        response
                    ) : (
                        <span className="placeholder">
                            Todavía no hay respuestas.
                        </span>
                    )}

                </div>

            </div>

        </div>
    );
}