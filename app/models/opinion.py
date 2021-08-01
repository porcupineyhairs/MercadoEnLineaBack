from sqlalchemy.orm import backref
from app.db import db


class Opinion(db.Model):
    __tablename__ = "opinion"
    __table_args__ = {"schema": "test_scheme"}

    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey("test_scheme.producto.id"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("test_scheme.usuario.id"))
    opinion = db.Column(db.String(140), nullable=False)
    producto = db.relationship("Producto", backref="opiniones")
    usuario = db.relationship("Usuario", backref="opiniones")
