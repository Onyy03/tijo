import os

from flask import Flask
from flask_smorest import Api

from app.config import Config
from app.extensions import db


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    Api(app)

    with app.app_context():
        db.create_all()

    return app
