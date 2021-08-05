from app.schemes.opinion_sch import OpinionSch
from app.schemes.usuario_sch import UsuarioSch
from app.marshmallow import ma
from app.models.producto import Producto


class ProductoSch(ma.SQLAlchemyAutoSchema):
    """Clase que nos sirve para convertir el modelo 'Producto' en un 'dict'."""

    class Meta:
        model = Producto
        include_fk = True

    usuario = ma.Nested(
        UsuarioSch, exclude=["contrasena", "correo", "genero", "direccion", "vendedor"]
    )
    opiniones = ma.List(ma.Nested(OpinionSch(exclude=["id_producto", "id_usuario"])))
