import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.core.config import settings

_LOG_DIR = Path(settings.log.log_dir)
_LOG_DIR.mkdir(parents=True, exist_ok=True)


class DailyRotatingFileHandler(RotatingFileHandler):
    """RotatingFileHandler that creates a new file each day and rotates by size."""

    def __init__(self, log_dir: Path, prefix: str, **kwargs):
        self._log_dir = log_dir
        self._prefix = prefix
        self._current_date = self._today()
        filepath = self._build_path()
        super().__init__(filepath, **kwargs)

    @staticmethod
    def _today() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _build_path(self) -> str:
        return str(self._log_dir / f"{self._prefix}_{self._current_date}.log")

    def shouldRollover(self, record):  # noqa: N802
        today = self._today()
        if today != self._current_date:
            self._current_date = today
            self.baseFilename = os.fspath(self._build_path())
            if self.stream:
                self.stream.close()
                self.stream = self._open()
        return super().shouldRollover(record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.log.log_level.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt=settings.log.log_format,
        datefmt=settings.log.date_format,
    )

    file_handler = DailyRotatingFileHandler(
        log_dir=_LOG_DIR,
        prefix="backend",
        maxBytes=settings.log.max_bytes,
        backupCount=settings.log.backup_count,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger
