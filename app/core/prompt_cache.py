from pathlib import Path

PROMPTS = {}


def load_all_prompts():
    """
    Carga todos los prompts de app/prompts en memoria.
    Se ejecuta una sola vez al iniciar FastAPI.
    """

    prompts_path = Path(__file__).parent.parent / "prompts"

    if not prompts_path.exists():
        raise RuntimeError(f"No existe la carpeta: {prompts_path}")

    PROMPTS.clear()

    for file in prompts_path.glob("*.txt"):

        with open(file, "r", encoding="utf-8") as f:
            PROMPTS[file.name] = f.read()

    print(f"✅ Prompts cargados: {len(PROMPTS)}")


def get_prompt(file_name: str) -> str:
    """
    Devuelve un prompt cargado en memoria.
    """

    if file_name not in PROMPTS:
        raise FileNotFoundError(f"Prompt '{file_name}' no encontrado.")

    return PROMPTS[file_name]
