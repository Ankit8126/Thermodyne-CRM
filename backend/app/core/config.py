import tomllib
from pathlib import Path

from pydantic_settings import BaseSettings

_SETTINGS_PATH = Path(__file__).resolve().parents[2] / "settings.toml"

with _SETTINGS_PATH.open("rb") as f:
    _toml = tomllib.load(f)

_log_cfg = _toml.get("logging", {})


class LogSettings:
    log_dir: str = _log_cfg.get("log_dir", "logs")
    log_level: str = _log_cfg.get("log_level", "INFO")
    max_bytes: int = _log_cfg.get("max_bytes", 10_485_760)
    backup_count: int = _log_cfg.get("backup_count", 30)
    log_format: str = _log_cfg.get(
        "log_format", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    date_format: str = _log_cfg.get("date_format", "%Y-%m-%d %H:%M:%S")


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"
    HEALTH_CHECK_INTERVAL_SECONDS: int = 120

    log: LogSettings = LogSettings()

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
