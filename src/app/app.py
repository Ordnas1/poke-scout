import os
from logging import DEBUG
from logging.config import dictConfig

from . import create_app

dictConfig({"version": 1, "root": {"level": DEBUG}})

app = create_app(config_mode=os.getenv("CONFIG_MODE"))


@app.route("/")
def health():
    return "Ping!"


if __name__ == "__main__":
    app.run()
