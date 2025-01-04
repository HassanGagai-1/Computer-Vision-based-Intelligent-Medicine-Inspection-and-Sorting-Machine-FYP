from dotenv import load_dotenv, find_dotenv
from routes.UserRoutes import user_bp
from routes.MachineRoutes import machine_bp
from routes.UserMachineRoutes import user_machine_bp
from routes.ResultRoutes import result_bp
from extensions import db
from flask import Flask
from models.users import User  
from models.machines import Machine
from models.user_machine import UserMachine
from models.results import Result  
from datetime import timedelta
import logging
from extensions import mail

import os

def create_app():    
    logging.basicConfig(
    level=logging.DEBUG,               # minimum severity level to log
    format='%(asctime)s %(levelname)s %(name)s:%(lineno)d - %(message)s'                
    )

    load_dotenv(find_dotenv())
    app = Flask(__name__)
    app.config.update(
    SESSION_COOKIE_HTTPONLY=True, # Prevents JavaScript from reading the cookie         
    SESSION_COOKIE_SECURE=False,  # True if using HTTPS                                 
    )
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'fallbacksecret')
    app.config['MAIL_DEBUG'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=4)                    

    app.config.from_prefixed_env()
        
    mail.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Create tables


    
    app.register_blueprint(user_bp)  
    app.register_blueprint(machine_bp)  
    app.register_blueprint(user_machine_bp)
    app.register_blueprint(result_bp)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)