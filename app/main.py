from dotenv import load_dotenv
from flask import Flask
from app.api.routes import api_blueprint

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)    

    return app