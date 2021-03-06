from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from config import DevConfig

# from flask_redis import FlaskRedis


# Package-globals.
# r = FlaskRedis()
db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(conf_obj=DevConfig):
    app = Flask(__name__,
                instance_relative_config=False,
                template_folder=DevConfig.TEMPLATE_DIR,
                static_folder=str(DevConfig.STATIC_DIR)
                )
    app.config.from_object(conf_obj)

    # Initialize application context to "globals".
    # r.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints.
    from app import auth
    from app import twitter

    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(twitter.twitter_bp)

    with app.app_context():
        if app.config['TESTING']:
            db.drop_all()
        # Create all models.
        db.create_all()

    return app
