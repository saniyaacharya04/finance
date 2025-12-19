from flask import Flask
from flask_session import Session

from app.core.config import load_config
from app.api.billing import bp as billing_bp

def create_app():
    app = Flask(__name__)

    # Load config
    load_config(app)

    # Session
    Session(app)

    # Register blueprints
    app.register_blueprint(billing_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
