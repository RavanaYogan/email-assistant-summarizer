import logging
from collections.abc import Iterable


def mask_secret(value: str, visible_chars: int = 4) -> str:
    if not value:
        return value
    if len(value) <= visible_chars:
        return "*" * len(value)
    masked_len = len(value) - visible_chars
    return f"{'*' * masked_len}{value[-visible_chars:]}"


class SensitiveDataFilter(logging.Filter):
    """Redacts known secret values from log records before they are emitted."""

    def __init__(self, secrets: Iterable[str]) -> None:
        super().__init__()
        self._secrets = [secret for secret in secrets if secret]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for secret in self._secrets:
            if secret in message:
                message = message.replace(secret, mask_secret(secret))
        record.msg = message
        record.args = ()
        return True
