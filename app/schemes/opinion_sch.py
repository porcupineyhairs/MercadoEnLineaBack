from flask_sqlalchemy import model
from app.marshmallow import ma
from app.models.opinion import Opinion


class OpinionSch(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Opinion
        include_fk = True

    # id = ma.auto_field()
    # id_producto = ma.auto_field()
    # id_usuario = ma.auto_field()
    # opinion = ma.auto_field()
    # usuario = ma.auto_field()