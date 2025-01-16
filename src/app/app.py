import os

from . import create_app
from .commands import appdatabp

app = create_app(config_mode=os.getenv("CONFIG_MODE"))


@app.route("/")
def health():
    return "Ping!"


app.register_blueprint(appdatabp)


if __name__ == "__main__":
    app.run()
