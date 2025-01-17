import os
from logging import DEBUG
from logging.config import dictConfig

from . import create_app
from .commands import appdata_bp
from .api import api_v1_bp

dictConfig({"version": 1, "root": {"level": DEBUG}})

app = create_app(config_mode=os.getenv("CONFIG_MODE"))


@app.route("/")
def health():
    return "Ping!"


app.register_blueprint(appdata_bp)
app.register_blueprint(api_v1_bp)


if __name__ == "__main__":
    app.run()
