import os

def load_config(app):
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SESSION_TYPE"] = os.getenv("SESSION_TYPE", "filesystem")
    app.config["SESSION_PERMANENT"] = False
