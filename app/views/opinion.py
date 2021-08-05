from flask import Blueprint, jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required

from app.db import db
from app.models.opinion import Opinion
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.schemes.opinion_sch import OpinionSch

opiniones_bp = Blueprint("opiniones", __name__)

opinion_schema = OpinionSch(exclude=["id_producto", "id_usuario"])
opiniones_schema = OpinionSch(many=True, exclude=["id_producto", "id_usuario"])


@opiniones_bp.route("/create/<int:id_producto>", methods=["POST"])
@jwt_required()
def crearOpinion(id_producto):
    """Controlador que nos permite crear una opinion.
    Parameters
    ----------
    id_producto : int
    
    Returns
    -------
    Response"""

    _id_usuario = get_jwt_identity()

    usuario = Usuario.query.get_or_404(_id_usuario)
    producto = Producto.query.get_or_404(id_producto)

    if usuario.vendedor:
        return (jsonify({"message": "No puedes comentar"}), 401)

    try:
        _json = request.json
        _opinion = _json["opinion"]

        opinion = Opinion(
            id_producto=producto.id, id_usuario=usuario.id, opinion=_opinion
        )

        usuario.opiniones.append(opinion)
        producto.opiniones.append(opinion)

        db.session.commit()

        return jsonify({"message": "Opinion creada correctamente"})
    except (KeyError, TypeError):
        res = jsonify({"message": "Bad request"})
        res.status_code = 400
        return res
