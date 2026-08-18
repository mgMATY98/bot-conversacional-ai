from app.models.bot_config import BotConfig

from app.core.bot_defaults import (
    DEFAULT_ASSISTANT_NAME,
    DEFAULT_PERSONALITY,
    DEFAULT_OBJECTIVE,
    DEFAULT_ADDITIONAL_INSTRUCTIONS,
    DEFAULT_WELCOME_MESSAGE,
    DEFAULT_FAREWELL_MESSAGE,
    DEFAULT_FORBIDDEN_TOPICS,
    DEFAULT_FORBIDDEN_WORDS,
    DEFAULT_POLITICAL_CAMPAIGNS,
)


def create_default_bot_config(client_id: int) -> BotConfig:

    return BotConfig(
        client_id=client_id,
        assistant_name=DEFAULT_ASSISTANT_NAME,
        personality=DEFAULT_PERSONALITY,
        objective=DEFAULT_OBJECTIVE,
        additional_instructions=DEFAULT_ADDITIONAL_INSTRUCTIONS,
        welcome_message=DEFAULT_WELCOME_MESSAGE,
        farewell_message=DEFAULT_FAREWELL_MESSAGE,
        forbidden_topics=DEFAULT_FORBIDDEN_TOPICS,
        forbidden_words=DEFAULT_FORBIDDEN_WORDS,
        political_campaigns=DEFAULT_POLITICAL_CAMPAIGNS,
    )
