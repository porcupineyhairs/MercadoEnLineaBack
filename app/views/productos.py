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
productos_schema = ProductoSch(many=True, exclude=["id_usuario"])


@productos_bp.route("/", methods=["GET"])
def obtenerProductos():
    productos = Producto.query.all()
    res = jsonify(
        [
            {
                "producto": producto_schema.dump(producto),
                "usuario": producto.usuario.nombre,
            }
            for producto in productos
        ]
    )
    return jsonify(res)


@productos_bp.route("/<int:id>", methods=["GET"])
def obtenerProducto(id):
    producto = Producto.query.get_or_404(id)
    producto_res = producto_schema.dump(producto)
    res = jsonify(
        {
            "producto": producto_res,
            "usuario": {"nombre": producto.usuario.nombre},
        }
    )
    return res


@productos_bp.route("/<int:id>/actualizar", methods=["PATCH"])
@jwt_required()
def actualizarProducto(id):
    _usuario_id = get_jwt_identity()
    producto = Producto.query.get_or_404(id)
    usuario = Usuario.query.get_or_404(_usuario_id)
    if not usuario.vendedor and producto not in usuario.productos:
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

    db.session.commit()

    return jsonify({"message": "Producto actualizado exitosamente"})


@productos_bp.route("/subir", methods=["POST"])
@jwt_required()
def subirProducto():
    _usuario_id = get_jwt_identity()
    usuario = Usuario.query.get_or_404(_usuario_id)
    if not usuario.vendedor:
        res = jsonify({"message": "No puede subir productos"})
        return res
    _json = request.form
    _icono = request.files["icono"]
    try:
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
    try:
        id_usuario = get_jwt_identity()
        usuario = Usuario.query.get_or_404(id_usuario)
        msg = Message("Hola", sender=usuario.correo, recipients=["cheo2090@gmail.com"])
        msg.body = "Hola"
        mail.send(msg)
        print(id_usuario)
        return jsonify({"message": "Compra realizada con exito"})
    except SMTPDataError:
        res = jsonify({"message": "Estamos en servidor de prueba :v"})
        res.status_code = 400
        return res
    except:
        res = jsonify({"message": "Sin informacion de pago"})
        res.status_code = 400
        return res
