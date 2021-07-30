from flask import Blueprint, jsonify, request, session

from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import db
from app.models.usuario import Usuario
from app.schemes.usuario_sch import UsuarioSch

usuario_bp = Blueprint('usuario', __name__)

usuario_schema = UsuarioSch()
usuarios_schema = UsuarioSch(many=True)


@usuario_bp.route('/login', methods=['POST'])
def login():
    _json = request.json
    if _json:
        _correo = _json['correo']
        _contrasena = _json['contrasena']
        if _correo and _contrasena:
            q = Usuario.query.filter_by(correo=_correo).first()
            if q:
                if check_password_hash(q.contrasena, _contrasena):
                    u = usuario_schema.dump(q)
                    session['username'] = q.correo
                    return jsonify({'nombre': u['nombre'], 'vendedor': u['vendedor']})
                else:
                    res = jsonify({'message': 'Invalid password'})
                    res.status_code = 400
                    return res
            else:
                res = jsonify({'message': 'Usuario no encontrado'})
                res.status_code = 404
                return res

    else:
        res = jsonify({'message': 'Bad request'})
        res.status_code = 400
        return res


@usuario_bp.route('/logout', methods=['GET'])
def cerrarSesion():
    if 'username' in session:
        session.pop('username', None)
        return jsonify({'message': 'Cerraste sesión'})
    else:
        res = jsonify({'message': 'No hay sesión activa'})
        return res


@usuario_bp.route('/signup', methods=['POST'])
def crearUsuario():
    _json = request.json
    if _json:
        _correo = _json['correo']
        _contrasena = _json['contrasena']
        _vendedor = _json['vendedor']
        _nombre = _json['nombre']
        _direccion = _json['direccion']
        _genero = _json['genero']
        if _correo and _contrasena and (_vendedor is not None) and _nombre and _direccion and _genero:
            try:
                usuario = Usuario(
                    correo=_correo,
                    contrasena=generate_password_hash(_contrasena),
                    vendedor=_vendedor,
                    nombre=_nombre,
                    direccion=_direccion,
                    genero=_genero
                )
                db.session.add(usuario)
                db.session.commit()
                return jsonify({'message': 'Usuario creado'})
            except IntegrityError:
                res = jsonify({'message': 'Correo ya registrado'})
                return res
        else:
            res = jsonify({'message': 'Bad request - falta datos'})
            res.status_code = 400
            return res
    else:
        res = jsonify({'message': 'Bad request'})
        res.status_code = 400
        return res
