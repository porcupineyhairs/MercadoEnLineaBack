#Importes de Flask.
from flask import Flask
from flask_cors import CORS
from flask_msearch import Search

#Importes de rutas.
from app.views.usuario import usuario_bp
from app.views.productos import productos_bp
from app.views.opinion import opiniones_bp
from app.views.media import media_bp

#Importes de configuración.
from app.configs import (
    JWT_ACCESS_TOKEN_EXPIRES,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    MAIL_USE_SSL,
    MAIL_USE_TLS,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    UPLOAD_FOLDER,
)
from app.cahce import cache
from app.db import db
from app.jwt import jwt
from app.mail import mail
from app.marshmallow import ma


def create_app():
    """Función que crea la aplicación de Flask y añade sus configuraciones."""
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_SECRET_KEY"] = SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["MAIL_SERVER"] = MAIL_SERVER
    app.config["MAIL_PORT"] = MAIL_PORT
    app.config["MAIL_USERNAME"] = MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config["MAIL_USE_SSL"] = True

    CORS(app)

    cache.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    db.create_all(app=app)
    ma.init_app(app)
    mail.init_app(app)
    search = Search(db=db)
    search.init_app(app)

    app.register_blueprint(media_bp, url_prefix="/media/")
    app.register_blueprint(usuario_bp, url_prefix="/usuario")
    app.register_blueprint(productos_bp, url_prefix="/productos")
    app.register_blueprint(opiniones_bp, url_prefix="/opiniones/")

    return app
