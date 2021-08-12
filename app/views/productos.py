import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_mail import Message

from smtplib import SMTPDataError
from uuid import uuid4
from werkzeug.exceptions import BadRequestKeyError
from werkzeug.utils import secure_filename

from app.db import db
from app.mail import mail
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.schemes.producto_sch import ProductoSch

productos_bp = Blueprint("productos", __name__)

producto_schema = ProductoSch(exclude=["id_usuario"])
productos_schema = ProductoSch(many=True, exclude=["id_usuario", "opiniones"])


@productos_bp.route("/", methods=["GET"])
def obtenerProductos():
    """Controlador que nos permite listar todos los productos guardados en
    la base de datos.

    Returns
    -------
    Response"""

    productos = Producto.query.all()
    res = jsonify(productos_schema.dump(productos))
    return res


@productos_bp.route("/<int:id>", methods=["GET"])
def obtenerProducto(id):
    """Controlador que nos permite obtener la información de un
    producto en particular.
    Parameters
    ----------
    id : int

    Returns
    -------
    Response"""

    producto = Producto.query.get_or_404(id)
    producto_res = producto_schema.dump(producto)
    res = jsonify(producto_res)
    return res


@productos_bp.route("/buscar", methods=["GET"])
def buscarProducto():
    """Controlador que nos permite buscar productos mediante sus nombres
    mediante un 'query'. Regresara una lista con todos los productos
    los cuales su 'nombre' coincida con el query.

    Returns
    -------
    Response"""

    busqueda = request.args["q"]
    productos = Producto.query.msearch(busqueda, fields=["nombre"], limit=20).all()
    res = productos_schema.dump(productos)
    return jsonify(res)


@productos_bp.route("/<int:id>/actualizar", methods=["PATCH"])
@jwt_required()
def actualizarProducto(id):
    """Controlador que nos permite actualizar la información de un
    producto.
    Parameters
    ----------
    id : int

    Returns
    -------
    Response"""

    _usuario_id = get_jwt_identity()
    producto = Producto.query.get_or_404(id)
    usuario = Usuario.query.get_or_404(_usuario_id)
    print(producto not in usuario.productos)
    print(producto.usuario.correo)
    if (not usuario.vendedor) or (producto not in usuario.productos):
        res = jsonify({"message": "No se encontro el producto"})
        return res
    _json = request.form.to_dict()
    _icono = request.files.to_dict().get("icono")

    producto.nombre = _json.get("nombre") or producto.nombre
    producto.descripcion = _json.get("descripcion") or producto.descripcion
    producto.envio = _json.get("envio") or producto.envio
    producto.precio = _json.get("precio") or producto.precio

    if _icono:
        nombre_archivo_split = _icono.filename.split(".")
        extension_archivo_icono = nombre_archivo_split[len(nombre_archivo_split) - 1]
        nuevo_nombre_icono = secure_filename(
            f"{str(uuid4())}.{extension_archivo_icono}"
        )
        ruta_icono = os.path.abspath(
            "app/static/productos_imgs/{}".format(nuevo_nombre_icono)
        )
        _icono.save(ruta_icono)
        producto.icono = nuevo_nombre_icono

    producto.vendido = False

    db.session.commit()

    return jsonify({"message": "Producto actualizado exitosamente"})


@productos_bp.route("/subir", methods=["POST"])
@jwt_required()
def subirProducto():
    """Controlador que nos permite subir la información de un producto
    para ponerlo a la venta.

    Returns
    -------
    Response"""

    _id_usuario = get_jwt_identity()
    usuario = Usuario.query.get_or_404(_id_usuario)
    if not usuario.vendedor:
        res = jsonify({"message": "No puede subir productos"})
        return res
    try:
        _json = request.form
        _icono = request.files["icono"]
        nombre = _json["nombre"]
        descripcion = _json["descripcion"]
        envio = _json["envio"]
        precio = _json["precio"]

        nombre_archivo_split = _icono.filename.split(".")
        extension_archivo_icono = nombre_archivo_split[len(nombre_archivo_split) - 1]
        nombre_icono = secure_filename(f"{str(uuid4())}.{extension_archivo_icono}")
        ruta_icono = os.path.abspath(
            "app/static/productos_imgs/{}".format(nombre_icono)
        )
        _icono.save(ruta_icono)

        producto = Producto(
            id_usuario=usuario.id,
            nombre=nombre,
            descripcion=descripcion,
            envio=envio,
            precio=precio,
            icono=nombre_icono,
            vendido=False,
        )

        usuario.productos.append(producto)

        db.session.commit()

        return jsonify({"message": "Producto subido correctamente"})
    except BadRequestKeyError:
        res = jsonify({"message": "Bad request - falta info"})
        return res


@productos_bp.route("/<int:id>/comprar", methods=["POST"])
@jwt_required()
def comprarProducto(id):
    """Controlador que permite al usuario realizar una compra.
    Parameters
    ----------
    id : int

    Returns
    -------
    Response"""

    try:
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.get_or_404(id_usuario)
        if usuario.vendedor:
            res = jsonify({"message": "Usted no puede comprar un producto"})
            res.status_code = 401
            return res

        producto = Producto.query.get_or_404(id)
        producto.vendido = True

        db.session.commit()

        msg = Message(
            "Compra", sender="support@mercado.en.linea.com", recipients=[usuario.correo]
        )
        msg.body = f"La compra fue realizada con exito {usuario.correo}"
        mail.send(msg)

        return jsonify({"message": "Compra realizada con exito"})
    except SMTPDataError:
        res = jsonify({"message": "Estamos en servidor de prueba :v"})
        res.status_code = 400
        return res
    except:
        res = jsonify({"message": "Sin informacion de pago"})
        res.status_code = 400
        return res
