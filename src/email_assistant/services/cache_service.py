import contextlib
import logging
import sqlite3
from collections.abc import Iterator
from pathlib import Path

from email_assistant.models.exceptions import CacheError

logger = logging.getLogger(__name__)


class EmailCacheService:
    """SQLite-backed cache mapping an email id to its classification."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextlib.contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
        finally:
            conn.close()

    def initialize(self) -> None:
        try:
            with self._connect() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS email_cache (
                        email_id TEXT PRIMARY KEY,
                        classification TEXT NOT NULL
                    )
                    """)
                conn.commit()
        except sqlite3.Error as exc:
            logger.exception("Failed to initialize cache database")
            raise CacheError("Failed to initialize cache database") from exc

        logger.info("Cache database initialized at %s", self._db_path)

    def get_classification(self, email_id: str) -> str | None:
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT classification FROM email_cache WHERE email_id = ?",
                    (email_id,),
                )
                row = cursor.fetchone()
        except sqlite3.Error as exc:
            logger.exception("Failed to fetch cached classification for %s", email_id)
            raise CacheError(f"Failed to fetch cached classification for {email_id}") from exc

        if row:
            logger.debug("Cache hit for email %s", email_id)
            return str(row[0])

        logger.debug("Cache miss for email %s", email_id)
        return None

    def save_classification(self, email_id: str, classification: str) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO email_cache (email_id, classification) VALUES (?, ?)",
                    (email_id, classification),
                )
                conn.commit()
        except sqlite3.Error as exc:
            logger.exception("Failed to save cached classification for %s", email_id)
            raise CacheError(f"Failed to save cached classification for {email_id}") from exc

        logger.info("Classification cached for %s", email_id)
