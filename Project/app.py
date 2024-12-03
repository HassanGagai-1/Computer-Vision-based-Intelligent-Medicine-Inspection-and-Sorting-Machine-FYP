from flask import Flask
from dotenv import load_dotenv
from routes.UserRoutes import user_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db

def create_app():
    
    load_dotenv()
    
    app = Flask(__name__)
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    app.register_blueprint(user_bp)
    
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    