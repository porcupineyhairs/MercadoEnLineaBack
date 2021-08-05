from app.marshmallow import ma
from app.models.usuario import Usuario


class UsuarioSch(ma.SQLAlchemyAutoSchema):
    """Clase que nos sirve para convertir el modelo 'Usuario' en un 'dict'."""

    class Meta:
        model = Usuario
