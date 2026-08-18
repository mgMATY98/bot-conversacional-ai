from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==========================
    # OPENAI
    # ==========================
    OPENAI_API_KEY: str
    # ==========================
    # JWT
    # ==========================
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_HOURS: int = 24

    # ==========================
    # FRONTEND
    # ==========================
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def allowed_origins(self):
        return self.ALLOWED_ORIGINS.split(",")


settings = Settings()
