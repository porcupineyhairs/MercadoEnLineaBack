from sqlalchemy.orm import backref
from app.db import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    __table_args__ = {'schema': 'test_scheme'}

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    direccion = db.Column(db.String(), nullable=False)
    correo = db.Column(db.String(), nullable=False)
    genero = db.Column(db.String(), nullable=False)
    vendedor = db.Column(db.Boolean)
    contrasena = db.Column(db.String(), nullable=False)

