from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from .config import config
from app.db import db, ma

from .commands import appdata_bp
from .api import api_v1_bp


class Base(DeclarativeBase):
    pass


migrate = Migrate()


def create_app(config_mode):
    app = Flask(
        __name__,
    )
    app.register_blueprint(appdata_bp)
    app.register_blueprint(api_v1_bp)

    # Configuration settings
    app.config.from_object(config[config_mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app
