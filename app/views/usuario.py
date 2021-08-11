from app.schemes.producto_sch import ProductoSch
from app.models.producto import Producto
from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import create_access_token, get_jwt, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.cahce import cache
from app.db import db
from app.models.usuario import Usuario
from app.schemes.usuario_sch import UsuarioSch

usuario_bp = Blueprint("usuario", __name__)

usuario_schema = UsuarioSch(exclude=["contrasena"])
usuarios_schema = UsuarioSch(many=True, exclude=["contrasena"])
productos_schema = ProductoSch(many=True, exclude=["usuario", "id_usuario"])


@usuario_bp.route("/login", methods=["POST"])
def login():
    """Controlador que permite al usuario iniciar sesión.

    Returns
    -------
    Response"""

    try:
        _json = request.json
        _correo = _json["correo"]
        _contrasena = _json["contrasena"]
        usuario = Usuario.query.filter_by(correo=_correo).first()
        if usuario and check_password_hash(usuario.contrasena, _contrasena):
            token = create_access_token(
                identity=usuario.id,
                additional_claims={
                    "nombre": usuario.nombre,
                    "vendedor": usuario.vendedor,
                },
            )
            res = jsonify({"message": "Inicio de sesión correcto", "token": token})
            return res
        else:
            res = jsonify({"message": "Correo o contraseña incorrectos"})
            res.status_code = 400
            return res
    except (KeyError, TypeError):
        res = jsonify({"message": "Bad request"})
        res.status_code = 400
        return res


@usuario_bp.route("/logout", methods=["POST"])
@jwt_required()
def cerrarSesion():
    """Controlador que es utilizado para que un usuario 'cierre sesión',
    esto se realiza invalidando el token que uso para autenticarse.

    Returns
    -------
    Response"""

    jti = get_jwt()["jti"]
    cache.set(jti, jti)
    res = jsonify({"message": "Sesión cerrada"})
    return res


@usuario_bp.route("/signup", methods=["POST"])
def crearUsuario():
    """Controlador que sirve para poder registrar a nuevos usuarios.

    Returns
    -------
    Response"""

    try:
        _json = request.json

        _correo = _json["correo"]
        print(_correo)
        _contrasena = _json["contrasena"]
        _vendedor = _json["vendedor"]
        _nombre = _json["nombre"]
        _direccion = _json["direccion"]
        _genero = _json["genero"]
        usuario = Usuario(
            correo=_correo,
            contrasena=generate_password_hash(_contrasena),
            vendedor=_vendedor,
            nombre=_nombre,
            direccion=_direccion,
            genero=_genero,
        )

        db.session.add(usuario)
        db.session.commit()

        return jsonify({"message": "Usuario creado"})
    except (KeyError, TypeError):
        res = jsonify({"message": "Bad request"})
        res.status_code = 400
        return res
    except IntegrityError:
        res = jsonify({"message": "Correo ya registrado"})
        res.status_code = 401
        return res


@usuario_bp.route("/profile", methods=["GET"])
@jwt_required()
def perfil():
    id_usuario = get_jwt_identity()
    usuario = Usuario.query.get_or_404(id_usuario)
    productos = Producto.query.filter_by(id_usuario=usuario.id).all()
    productos_res = productos_schema.dump(productos)
    res = usuario_schema.dump(usuario)
    res["productos"] = productos_res
    return jsonify(res)
