from flask_sqlalchemy import model
from app.marshmallow import ma
from app.models.producto import Producto


class ProductoSch(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_fk = True

    # id = ma.auto_field()
    # id_usuario = ma.auto_field()
    # nombre = ma.auto_field()
    # descripcion = ma.auto_field()
    # envio = ma.auto_field()
    # precio = ma.auto_field()
    # icono = ma.auto_field()
    # opiniones = ma.auto_field()
    # usuario = ma.auto_field()