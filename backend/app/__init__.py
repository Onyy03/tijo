import os

from flask import Flask
from flask_smorest import Api

from app.accounts.routes import accounts_blueprint
from app.clock import Clock, SystemClock
from app.codes.generator import CodeGenerator, SecureRandomCodeGenerator
from app.codes.routes import codes_blueprint
from app.config import Config
from app.container import init_services
from app.errors import register_error_handlers
from app.extensions import db
from app.payments.routes import payments_blueprint
from app.seed import seed_demo_accounts
from app.transfers.routes import transfers_blueprint


def create_app(
    config: type[Config] = Config,
    clock: Clock | None = None,
    code_generator: CodeGenerator | None = None,
) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    api = Api(app)
    api.register_blueprint(accounts_blueprint)
    api.register_blueprint(codes_blueprint)
    api.register_blueprint(payments_blueprint)
    api.register_blueprint(transfers_blueprint)
    register_error_handlers(app)
    init_services(app, clock or SystemClock(), code_generator or SecureRandomCodeGenerator())

    with app.app_context():
        db.create_all()
        seed_demo_accounts()

    return app
