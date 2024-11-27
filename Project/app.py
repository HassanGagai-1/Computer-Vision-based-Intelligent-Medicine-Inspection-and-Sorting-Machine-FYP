from flask import Flask
# from routes import routes
from dotenv import load_dotenv
from routes.UserRoutes import user_bp
from routes.routes import routes
def create_app():
    
    load_dotenv()
    
    app = Flask(__name__)
    
    app.register_blueprint(user_bp)
    app.register_blueprint(routes)
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
