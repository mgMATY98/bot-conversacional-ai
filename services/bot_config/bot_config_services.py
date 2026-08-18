from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.bot_config import BotConfig
from app.schemas.bot_config import BotConfigUpdate


class BotConfigService:

    def get_config(self, db: Session, client_id: int):

        config = db.query(BotConfig).filter(BotConfig.client_id == client_id).first()

        if config is None:
            raise HTTPException(
                status_code=404,
                detail="Configuración no encontrada",
            )

        return config

    def update_config(
        self,
        db: Session,
        client_id: int,
        data: BotConfigUpdate,
    ):

        config = self.get_config(db, client_id)

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(config, key, value)

        db.commit()
        db.refresh(config)

        return config


bot_config_service = BotConfigService()
