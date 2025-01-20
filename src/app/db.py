from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_marshmallow import Marshmallow


class Base(DeclarativeBase):
    __abstract__ = True


db = SQLAlchemy()
ma = Marshmallow()
