import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(basedir, os.getenv(
            "DEVELOPMENT_DATABASE_FILENAME"
            ))}"
    )


config = {"development": DevelopmentConfig}
