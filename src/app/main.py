from flask import Flask
from flask_session import Session
import os

from app.core.config import load_config
from app.api.billing import bp as billing_bp
from app.api.auth import bp as auth_bp

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

    app.register_blueprint(auth_bp)
    app.register_blueprint(billing_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
