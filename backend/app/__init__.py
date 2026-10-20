import os

from flask import Flask
from flask_smorest import Api

from app.accounts.routes import accounts_blueprint
from app.config import Config
from app.container import init_services
from app.errors import register_error_handlers
from app.extensions import db
from app.seed import seed_demo_accounts


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    api = Api(app)
    api.register_blueprint(accounts_blueprint)
    register_error_handlers(app)
    init_services(app)

    with app.app_context():
        db.create_all()
        seed_demo_accounts()

    return app
