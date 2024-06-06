from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app.config.feature_flags import FEATURE_FLAGS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FEATURE_FLAGS"] = FEATURE_FLAGS
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    jwt = JWTManager(app)

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.user import User
    from app.models.role import Role
    from app.models.permission import Permission
    from app.models.relationship import Relationship
    from app.models.userRole import UserRoles
    from app.models.rolePermission import RolePermission
    # from app.models.movie import Movie

    db.init_app(app)
    migrate.init_app(app, db)

    # from app.routes.movie_routes import movies_bp
    from app.routes.feature_flags import feature_flags
    from app.routes.auth_routes import auth_bp
    # app.register_blueprint(movies_bp)
    app.register_blueprint(feature_flags)
    app.register_blueprint(auth_bp)

    return app
