import os

from . import create_app

app = create_app(config_mode=os.getenv("CONFIG_MODE"))


@app.route("/")
def health():
    return "Ping!"


if __name__ == "__main__":
    app.run()
