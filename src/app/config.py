"""Config classes for any of the possible app configurations"""
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.getenv("DEVELOPMENT_DATABASE_FILENAME")}"
    )


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.getenv("DEVELOPMENT_DATABASE_FILENAME")}"
    )


config = {"development": DevelopmentConfig, "testing": TestingConfig}
