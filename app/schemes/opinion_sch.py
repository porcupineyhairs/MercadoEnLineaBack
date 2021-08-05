from flask_sqlalchemy import model
from app.marshmallow import ma
from app.models.opinion import Opinion
from app.schemes.usuario_sch import UsuarioSch


class OpinionSch(ma.SQLAlchemyAutoSchema):
    """Clase que nos sirve para convertir el modelo 'Opinion' en un 'dict'."""

    class Meta:
        model = Opinion
        include_fk = True

    usuario = ma.Nested(
        UsuarioSch, exclude=["contrasena", "correo", "genero", "direccion", "vendedor"]
    )
