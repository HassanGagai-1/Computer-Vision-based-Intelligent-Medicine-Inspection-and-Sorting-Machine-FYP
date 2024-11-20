from flask import Flask
from routes import routes
from dotenv import load_dotenv
from config import Config

import os

def create_app():
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(routes)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
