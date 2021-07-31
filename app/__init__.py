from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.configs import JWT_ACCESS_TOKEN_EXPIRES, SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, UPLOAD_FOLDER
from app.views.usuario import usuario_bp
from app.views.productos import productos_bp
from app.views.opinion import opiniones_bp
from app.views.media import media_bp

from app.db import db
from app.marshmallow import ma


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['JWT_TOKEN_LOCATION'] = ["headers", "cookies"]
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    CORS(app)

    jwt = JWTManager(app)
    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(opiniones_bp, url_prefix='/opiniones/')
    app.register_blueprint(media_bp, url_prefix='/media/')

    db.create_all(app=app)

    return app
