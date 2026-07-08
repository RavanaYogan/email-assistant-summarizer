import sqlite3
import logging

logger = logging.getLogger(__name__)
DB_PATH = "database/cache.db"

def initialize_database():

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS email_cache (
            email_id TEXT PRIMARY KEY,
            classification TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()

    logger.info(
        "Cache database initialized"
    )

def get_cached_classification(
    email_id: str
):

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.execute(
            """
            SELECT classification
            FROM email_cache
            WHERE email_id = ?
            """,
            (email_id,)
        )

        row = cursor.fetchone()

        conn.close()

        if row:

            logger.info(
                "Cache hit for email %s",
                email_id
            )

            return row[0]

        logger.info(
            "Cache miss for email %s",
            email_id
        )

        return None

    except Exception as error:

        logger.exception(
            "Failed to fetch cache"
        )

        return None

def save_classification(
    email_id: str,
    classification: str
):

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """
            INSERT OR REPLACE INTO email_cache (
                email_id,
                classification
            )
            VALUES (?, ?)
            """,
            (
                email_id,
                classification
            )
        )
        conn.commit()
        conn.close()

        logger.info(
            "Classification cached for %s",
            email_id
        )

    except Exception:
        logger.exception(
            "Failed to save cache"
        )