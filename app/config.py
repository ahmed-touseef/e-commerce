from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    database_url: str
    shop_host: str = "shop.eurofiora.it"
    app_host: str = "app.eurofiora.it"
    admin_host: str = "admin.eurofiora.it"


settings = Settings()
