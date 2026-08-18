import { useEffect, useState } from "react";
import "./Settings.css";
import api from "../../../services/api";
import { Save, Settings as SettingsIcon, Loader2 } from "lucide-react";

export default function Settings() {

    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(true); // Estado para la carga inicial de datos

    const [form, setForm] = useState({
        organization_name: "",
        representative_name: "",
        municipality: "",
        province: "",
        bot_phone: "",
        prompt: "",
        tone: "Profesional",
        temperature: 0.7
    });

    useEffect(() => {
        loadSettings();
    }, []);

    async function loadSettings() {
        try {
            setFetching(true);
            const res = await api.get("/client/profile");

            // Autocompleta el formulario con los datos que vienen del backend
            setForm((prev) => ({
                ...prev,
                ...res.data
            }));

        } catch (err) {
            console.error("Error al cargar la configuración:", err);
            alert("No se pudo cargar la configuración actual.");
        } finally {
            setFetching(false);
        }
    }

    async function saveSettings() {
        setLoading(true);

        try {
            await api.put("/client/profile", form);
            alert("Configuración guardada correctamente. ✅");
        } catch (err) {
            console.error("Error al guardar:", err);
            alert("No se pudo guardar la configuración.");
        } finally {
            setLoading(false);
        }
    }

    function handleChange(e) {
        setForm({
            ...form,
            [e.target.name]: e.target.value
        });
    }

    // Si está cargando por primera vez los datos del back, mostramos un indicador estético
    if (fetching) {
        return (
            <div className="settings-page" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
                <div style={{ textAlign: 'center' }}>
                    <Loader2 className="animate-spin" size={40} />
                    <p style={{ marginTop: '10px' }}>Cargando configuración...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="settings-page">
            <div className="settings-header">
                <SettingsIcon size={34} />
                <div>
                    <h1>Configuración</h1>
                    <p>
                        Personalizá el comportamiento de tu asistente.
                    </p>
                </div>
            </div>

            <div className="settings-card">
                <label>Nombre de la organización</label>
                <input
                    name="organization_name"
                    value={form.organization_name}
                    onChange={handleChange}
                />

                <label>Representante</label>
                <input
                    name="representative_name"
                    value={form.representative_name}
                    onChange={handleChange}
                />

                <label>Municipio</label>
                <input
                    name="municipality"
                    value={form.municipality}
                    onChange={handleChange}
                />

                <label>Provincia</label>
                <input
                    name="province"
                    value={form.province}
                    onChange={handleChange}
                />

                <label>Teléfono del Bot</label>
                <input
                    name="bot_phone"
                    value={form.bot_phone}
                    onChange={handleChange}
                />

                <label>Prompt del asistente</label>
                <textarea
                    rows="8"
                    name="prompt"
                    value={form.prompt}
                    onChange={handleChange}
                />

                <label>Tono</label>
                <select
                    name="tone"
                    value={form.tone}
                    onChange={handleChange}
                >
                    <option>Profesional</option>
                    <option>Amigable</option>
                    <option>Formal</option>
                    <option>Casual</option>
                </select>

                <label>Temperatura IA</label>
                <input
                    type="number"
                    step="0.1"
                    min="0"
                    max="2"
                    name="temperature"
                    value={form.temperature}
                    onChange={handleChange}
                />

                <button
                    className="save-btn"
                    onClick={saveSettings}
                    disabled={loading || fetching}
                >
                    <Save size={18} />
                    {loading ? "Guardando..." : "Guardar cambios"}
                </button>
            </div>
        </div>
    );
}