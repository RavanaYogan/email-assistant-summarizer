from pathlib import Path

from email_assistant.services.cache_service import EmailCacheService


def test_cache_roundtrip(tmp_path: Path) -> None:
    cache = EmailCacheService(tmp_path / "cache.db")
    cache.initialize()

    assert cache.get_classification("email-1") is None

    cache.save_classification("email-1", "IMPORTANT")
    assert cache.get_classification("email-1") == "IMPORTANT"


def test_cache_save_overwrites_existing(tmp_path: Path) -> None:
    cache = EmailCacheService(tmp_path / "cache.db")
    cache.initialize()

    cache.save_classification("email-1", "SPAM")
    cache.save_classification("email-1", "IMPORTANT")

    assert cache.get_classification("email-1") == "IMPORTANT"
