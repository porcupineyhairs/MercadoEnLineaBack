from app.marshmallow import ma
from app.models.usuario import Usuario


class UsuarioSch(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
