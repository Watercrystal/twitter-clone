from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
# from flask_redis import FlaskRedis


# Package-globals.
#r = FlaskRedis()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                instance_relative_config=False,
                template_folder=DevConfig.TEMPLATE_DIR,
                static_folder=str(DevConfig.STATIC_DIR)
                )
    app.config.from_object('config.DevConfig')

    db.init_app(app)
    # r.init_app(app)

    # Register blueprints.
    from app import auth

    app.register_blueprint(auth.auth_bp)

    with app.app_context():
        #Create all models.
        db.create_all()

    return app
