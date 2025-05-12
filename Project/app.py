from dotenv import load_dotenv, find_dotenv
from routes.UserRoutes import user_bp
from ultralytics import YOLO
from routes.MachineRoutes import machine_bp
from routes.UserMachineRoutes import user_machine_bp
from routes.ResultRoutes import result_bp
from routes.live_feed import live_feed_bp
from models.roles import Role
from extensions import db
from datetime import timedelta
import logging
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
import os
from flask_session import Session
from flask_migrate import Migrate
from PIL import Image
from flask_cors import CORS
import numpy as np
import torch


logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app)


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
    SESSION_TYPE='filesystem',  # Enable filesystem-based session storage
    SESSION_PERMANENT=True, 
    SESSION_COOKIE_NAME="session",
    SESSION_USE_SIGNER=True,  # Ensure secure signing
    SESSION_FILE_DIR='/tmp/flask_session',  # Store session files here
    SECRET_KEY=os.getenv('FLASK_SECRET_KEY', 'fallbacksecret'),
    PERMANENT_SESSION_LIFETIME=timedelta(hours=4)                      
    )
    
    Session(app)  


    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['MAIL_DEBUG'] = True

    app.config.from_prefixed_env()
        
    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()  # Create tables
        
    app.register_blueprint(user_bp)  
    app.register_blueprint(machine_bp)  
    app.register_blueprint(user_machine_bp)
    app.register_blueprint(result_bp)
    # app.register_blueprint(prediction_bp) 
    app.register_blueprint(live_feed_bp)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
