import os

from flask import Blueprint, send_file

from app.configs import UPLOAD_FOLDER

media_bp = Blueprint('media', __name__)


@media_bp.route('/<path:filename>', methods=['GET'])
def obtenerImage(filename):
    imagen = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(imagen)
