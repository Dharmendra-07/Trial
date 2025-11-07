from flask import Flask, jsonify
from dotenv import load_dotenv
from config import LocalDevelopmentConfig
from extensions import db, security
from models import User, Role
from flask_security import SQLAlchemyUserDatastore

def create_app():
    app = Flask(__name__)

    # Load environment variables (if any)
    load_dotenv()

    # Config setup
    app.config.from_object(LocalDevelopmentConfig)

    # Initialize extensions
    db.init_app(app)

    # Flask-Security setup
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    app.datastore = datastore

    # Create tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5007)

    