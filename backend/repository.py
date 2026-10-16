import sqlite3
from contextlib import closing

from backend.models import ShortLink


class LinkRepository:
    def __init__(self, database_path):
        self.database_path = str(database_path)

        with closing(self._connect()) as connection:
            with connection:
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS links (
                        code TEXT PRIMARY KEY,
                        original_url TEXT NOT NULL
                    )
                """)

    def _connect(self):
        return sqlite3.connect(self.database_path, timeout=10)

    def save(self, link):
        with closing(self._connect()) as connection:
            try:
                with connection:
                    connection.execute(
                        "INSERT INTO links (code, original_url) VALUES (?, ?)",
                        (link.code, link.original_url),
                    )
                return True
            except sqlite3.IntegrityError:
                # The code already exists. The service can try another.
                return False

    def find_by_code(self, code):
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT code, original_url FROM links WHERE code = ?",
                (code,),
            ).fetchone()

        if row is None:
            return None

        return ShortLink(code=row[0], original_url=row[1])