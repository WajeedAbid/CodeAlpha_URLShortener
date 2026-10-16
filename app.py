from pathlib import Path
from flask import Flask

from backend.repository import LinkRepository
from backend.routes import create_routes
from backend.service import LinkService


def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    database_path = Path(__file__).resolve().parent / "links.db"

    repository = LinkRepository(database_path)
    service = LinkService(repository)

    app.register_blueprint(create_routes(service))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)