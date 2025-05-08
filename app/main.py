from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from app.api.routes import api_blueprint
from app.extensions import db

load_dotenv()

def create_app(config_class="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(api_blueprint)    

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app