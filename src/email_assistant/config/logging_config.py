import logging
from collections.abc import Iterable
from pathlib import Path

from email_assistant.utils.masking import SensitiveDataFilter

_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logging(
    log_dir: Path,
    sensitive_values: Iterable[str] = (),
    level: int = logging.INFO,
) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(_LOG_FORMAT)
    sensitive_filter = SensitiveDataFilter(sensitive_values)

    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)
    file_handler.addFilter(sensitive_filter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(sensitive_filter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)
