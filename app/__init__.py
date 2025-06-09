import dotenv
from flask import Flask

dotenv.load_dotenv()


def create_app():
    app = Flask(__name__)

    from .routes import routes
    app.register_blueprint(routes)

    return app
