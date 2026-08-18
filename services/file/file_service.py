from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile


class FileService:

    BASE_PATH = Path("storage")

    MAX_SIZE = 20 * 1024 * 1024  # 20 MB

    ALLOWED_TYPES = {
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }

    # ==========================================
    # Carpetas
    # ==========================================

    def create_client_folder(
        self,
        client_id: int,
    ) -> Path:

        folder = self.BASE_PATH / f"client_{client_id}" / "documents"

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        return folder

    # ==========================================
    # Nombre único
    # ==========================================

    def generate_filename(
        self,
        original_filename: str,
    ) -> str:

        extension = Path(original_filename).suffix.lower()

        return f"{uuid4()}{extension}"

    # ==========================================
    # Validaciones
    # ==========================================

    async def validate_file(
        self,
        file: UploadFile,
    ) -> bytes:

        content = await file.read()

        if len(content) == 0:
            raise HTTPException(
                status_code=400,
                detail="El archivo está vacío.",
            )

        if len(content) > self.MAX_SIZE:
            raise HTTPException(
                status_code=400,
                detail="El archivo supera el tamaño máximo permitido (20 MB).",
            )

        if file.content_type not in self.ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no permitido: {file.content_type}",
            )

        return content

    # ==========================================
    # Guardar archivo
    # ==========================================

    async def save_file(
        self,
        client_id: int,
        file: UploadFile,
    ):

        folder = self.create_client_folder(client_id)

        filename = self.generate_filename(file.filename)

        filepath = folder / filename

        content = await self.validate_file(file)

        with open(filepath, "wb") as f:
            f.write(content)

        return {
            "stored_filename": filename,
            "original_filename": file.filename,
            "mime_type": file.content_type,
            "size": len(content),
            "path": str(filepath),
        }

    # ==========================================
    # Eliminar archivo
    # ==========================================

    def delete_file(
        self,
        client_id: int,
        stored_filename: str,
    ):

        path = self.get_path(
            client_id,
            stored_filename,
        )

        print("\n========== ELIMINANDO ==========")
        print("Archivo:", stored_filename)
        print("Ruta:", path)
        print("Existe:", path.exists())

        if path.exists():

            path.unlink()

            print("✅ Archivo eliminado")

        else:

            print("❌ El archivo NO existe")

        print("===============================\n")

        # ==========================================
        # Existe archivo
        # ==========================================

    def exists(
        self,
        client_id: int,
        stored_filename: str,
    ) -> bool:

        path = self.BASE_PATH / f"client_{client_id}" / "documents" / stored_filename

        return path.exists()

    # ==========================================
    # Ruta del archivo
    # ==========================================

    def get_path(
        self,
        client_id: int,
        stored_filename: str,
    ) -> Path:

        return self.BASE_PATH / f"client_{client_id}" / "documents" / stored_filename


file_service = FileService()
