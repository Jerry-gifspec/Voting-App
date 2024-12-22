from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configurations from .env or other files
    app.config.from_mapping(
        SECRET_KEY="your_secret_key_here",
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/votingsystemdb",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Initialize extensions
    db.init_app(app)

    # Import and register routes
    with app.app_context():
        from server import routes
        app.register_blueprint(routes.bp)

    return app
