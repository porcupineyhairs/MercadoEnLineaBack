from app.db import db


class Usuario(db.Model):
    """Clase que nos sirve como modelo de la tabla 'usuario' que se encuentra
    en la base de datos."""

    __tablename__ = "usuario"
    __table_args__ = {"schema": "test_scheme"}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    direccion = db.Column(db.String(), nullable=False)
    correo = db.Column(db.String(), nullable=False)
    genero = db.Column(db.String(), nullable=False)
    vendedor = db.Column(db.Boolean, nullable=False)
    contrasena = db.Column(db.String(), nullable=False)
