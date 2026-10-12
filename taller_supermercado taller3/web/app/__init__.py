import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "clave-local")
    from .routes import bp
    app.register_blueprint(bp)
    return app
