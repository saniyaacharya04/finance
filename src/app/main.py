from flask import Flask
from flask_session import Session
import os

from app.core.config import load_config
from app.core.filters import usd
from app.core.errors import forbidden
from app.api.billing import bp as billing_bp
from app.api.auth import bp as auth_bp
from app.api.history import bp as history_bp
from app.api.quotes import bp as quotes_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "web", "templates"),
        static_folder=os.path.join(BASE_DIR, "web", "static"),
        static_url_path="/static",
    )

    load_config(app)
    Session(app)

    app.jinja_env.filters["usd"] = usd
    app.register_error_handler(403, forbidden)

    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(billing_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
