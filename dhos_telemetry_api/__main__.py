import os

from flask_batteries_included.config import is_production_environment
from waitress import serve

from .app import create_app

SERVER_PORT = os.getenv("SERVER_PORT", 5000)

if __name__ == "__main__":
    app = create_app()
    serve(app, host="0.0.0.0", port=SERVER_PORT)
