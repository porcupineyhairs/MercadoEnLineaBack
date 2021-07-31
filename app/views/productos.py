import os

from flask import Blueprint, jsonify, session, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from uuid import uuid4
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename

from app.db import db
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.schemes.producto_sch import ProductoSch

productos_bp = Blueprint('productos', __name__)

producto_schema = ProductoSch()
productos_schema = ProductoSch(many=True)


@productos_bp.route('/', methods=['GET'])
def obtenerProductos():
    q = Producto.query.all()
    res = productos_schema.dump(q)
    return jsonify(res)


@productos_bp.route('/<int:id>', methods=['GET'])
def obtenerProducto(id):
    producto = Producto.query.get_or_404(id)
    res = producto_schema.dump(producto)
    return jsonify(res)


@productos_bp.route('/<int:id>/actualizar', methods=['PATCH'])
@jwt_required()
def actualizarProducto(id):
    _usuario_id = get_jwt_identity()
    producto = Producto.query.get_or_404(id)
    usuario = Usuario.query.get_or_404(_usuario_id)
    if usuario.vendedor and producto not in usuario.productos:
        res = jsonify({'message': 'No se encontro el producto'})
        return res
    _json = request.form
    _icono = request.files['icono']
    try:
        producto.nombre = _json['nombre']
        producto.descripcion = _json['descripcion']
        producto.envio = _json['envio']
        producto.precio = _json['precio']

        nombre_archivo_split = _icono.filename.split('.')
        extension_archivo_icono = nombre_archivo_split[
            len(nombre_archivo_split) - 1
        ]
        nuevo_nombre_icono = secure_filename(
            f'{str(uuid4())}.{extension_archivo_icono}')
        ruta_icono = os.path.abspath(
            'app/static/productos_imgs/{}'.format(nuevo_nombre_icono))
        _icono.save(ruta_icono)
        producto.icono = nuevo_nombre_icono

        db.session.commit()

        return jsonify({'message': 'Producto actualizado exitosamente'})
    except BadRequestKeyError:
        res = jsonify({'message': 'Bad request - falta info'})
        return res


@productos_bp.route('/subir', methods=['POST'])
@jwt_required()
def subirProducto():
    _usuario_id = get_jwt_identity()
    producto = Producto.query.get_or_404(id)
    usuario = Usuario.query.get_or_404(_usuario_id)
    if usuario.vendedor and producto not in usuario.productos:
        res = jsonify({'message': 'No se encontro el producto'})
        return res
    _json = request.form
    _icono = request.files['icono']
    try:
        producto.nombre = _json['nombre']
        producto.descripcion = _json['descripcion']
        producto.envio = _json['envio']
        producto.precio = _json['precio']
    except BadRequestKeyError:
        res = jsonify({'message': 'Bad request - falta info'})
        return res


@productos_bp.route('/<int:id>/comprar', methods=['POST'])
def comprarProducto(id):
    return {'mensaje': f'Producto {id} comprado'}
