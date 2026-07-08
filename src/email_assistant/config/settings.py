import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from email_assistant.models.exceptions import ConfigurationError

_REQUIRED_VARS = (
    "CUSTOM_LLM_BASE_URL",
    "CUSTOM_LLM_MODEL",
    "CUSTOM_LLM_API_KEY",
)


@dataclass(frozen=True)
class Settings:
    custom_llm_base_url: str
    custom_llm_model: str
    custom_llm_api_key: str
    gmail_credentials_path: Path
    gmail_token_path: Path
    log_dir: Path
    cache_db_path: Path

    @property
    def secrets(self) -> tuple[str, ...]:
        return (self.custom_llm_api_key,)

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> "Settings":
        load_dotenv(dotenv_path=env_file)

        missing = [name for name in _REQUIRED_VARS if not os.getenv(name)]
        if missing:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return cls(
            custom_llm_base_url=os.environ["CUSTOM_LLM_BASE_URL"],
            custom_llm_model=os.environ["CUSTOM_LLM_MODEL"],
            custom_llm_api_key=os.environ["CUSTOM_LLM_API_KEY"],
            gmail_credentials_path=Path(os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")),
            gmail_token_path=Path(os.getenv("GMAIL_TOKEN_PATH", "token.json")),
            log_dir=Path(os.getenv("LOG_DIR", "logs")),
            cache_db_path=Path(os.getenv("CACHE_DB_PATH", "database/cache.db")),
        )
