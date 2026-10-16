import secrets
import string
from urllib.parse import urlsplit

from models import ShortLink


class LinkService:
    def __init__(self, repository):
        self.repository = repository

    def shorten(self, original_url):
        url = self._validate_url(original_url)
        alphabet = string.ascii_letters + string.digits

        for _ in range(10):
            code = "".join(secrets.choice(alphabet) for _ in range(7))
            link = ShortLink(code=code, original_url=url)

            if self.repository.save(link):
                return link

        raise RuntimeError("Could not generate a unique code. Please try again.")

    def get_link(self, code):
        return self.repository.find_by_code(code)

    @staticmethod
    def _validate_url(value):
        if not isinstance(value, str):
            raise ValueError("Please enter a URL.")

        url = value.strip()

        if not url or len(url) > 4096:
            raise ValueError("Enter a URL containing 1–4096 characters.")

        if any(character.isspace() or ord(character) < 32 for character in url):
            raise ValueError("The URL cannot contain spaces or control characters.")

        if "\\" in url or "\x7f" in url:
            raise ValueError("The URL contains invalid characters.")

        try:
            parsed = urlsplit(url)

            if parsed.scheme.lower() not in ("http", "https"):
                raise ValueError()

            if not parsed.hostname:
                raise ValueError()

            if parsed.username is not None or parsed.password is not None:
                raise ValueError()

            # Accessing port also checks for invalid port values.
            parsed.port

        except ValueError:
            raise ValueError(
                "Enter a valid http:// or https:// URL without login credentials."
            ) from None

        return url