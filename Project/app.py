from flask import Flask
from dotenv import load_dotenv
from routes.UserRoutes import user_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

def create_app():
    
    load_dotenv()
    
    app = Flask(__name__)
    
    app.config.from_prefixed_env()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    app.register_blueprint(user_bp)
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    