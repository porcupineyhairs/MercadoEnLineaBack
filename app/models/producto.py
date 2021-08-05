from sqlalchemy.orm import backref
from app.db import db


class Producto(db.Model):
    """Clase que nos sirve como modelo de la tabla 'producto' que se encuentra
    en la base de datos."""

    __tablename__ = "producto"
    __table_args__ = {"schema": "test_scheme"}
    __searchable__ = ["nombre"]

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("test_scheme.usuario.id"))
    nombre = db.Column(db.String(), nullable=False)
    descripcion = db.Column(db.String(350), nullable=False)
    envio = db.Column(db.String(), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    icono = db.Column(db.String(), nullable=False)
    vendido = db.Column(db.Boolean, nullable=False)

    usuario = db.relationship("Usuario", backref="productos")
