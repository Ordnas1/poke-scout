from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from .config import config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(config_mode):
    app = Flask(
        __name__,
    )

    # Configuration settings
    app.config.from_object(config[config_mode])

    db.init_app(app)

    return app
