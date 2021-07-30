from app.configs import UPLOAD_FOLDER
import os

from flask import Blueprint, jsonify, session, request

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
def actualizarProducto(id):
    if 'username' in session:
        _correo = session['username']
        producto = Producto.query.get_or_404(id)
        usuario = Usuario.query.filter_by(correo=_correo).first()
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

            nombre_archivo_icono = secure_filename(
                str(usuario.id)+'_'+_icono.filename)
            ruta_icono = os.path.abspath('app/static/productos_imgs/{}'.format(nombre_archivo_icono))
            _icono.save(ruta_icono)
            producto.icono = nombre_archivo_icono

            db.session.commit()

            return jsonify({'message': 'Producto actualizado exitosamente'})
        except BadRequestKeyError:
            res = jsonify({'message': 'Bad request - falta info'})
            return res
    else:
        res = jsonify({'message': 'Desautorizado'})
        res.status_code = 401
        return res


@productos_bp.route('/subir', methods=['POST'])
def subirProducto():
    if 'username' in session:
        _correo = session['username']
        producto = Producto.query.get_or_404(id)
        usuario = Usuario.query.filter_by(correo=_correo).first()
        if  usuario.vendedor and producto not in usuario.productos:
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
    else:
        res = jsonify({'message': 'Desautorizado'})
        res.status_code = 401
        return res


@productos_bp.route('/<int:id>/comprar', methods=['POST'])
def comprarProducto(id):
    return {'mensaje': f'Producto {id} comprado'}
