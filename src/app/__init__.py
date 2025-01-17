from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase
from .config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
migrate = Migrate()


def create_app(config_mode):
    app = Flask(
        __name__,
    )

    # Configuration settings
    app.config.from_object(config[config_mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    return app
