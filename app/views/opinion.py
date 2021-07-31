from flask import Blueprint, jsonify
from flask_jwt_extended.view_decorators import jwt_required

from app.models.opinion import Opinion
from app.schemes.opinion_sch import OpinionSch

opiniones_bp = Blueprint('opiniones', __name__)

opinion_schema = OpinionSch()
opinioes_schema = OpinionSch(many=True)


@opiniones_bp.route('/create/<int:id_producto>', methods=['POST'])
@jwt_required()
def crearOpinion(id_producto):
    return {'mensaje': 'Opinio creada'}


@opiniones_bp.route('/<int:id_producto>', methods=['GET'])
def obtenerOpinionesProducto(id_producto):
    q = Opinion.query.all()
    res = opinioes_schema.dump(q)
    return jsonify(res)
