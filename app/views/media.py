import os

from flask import Blueprint, send_file

from app.configs import UPLOAD_FOLDER

media_bp = Blueprint("media", __name__)


@media_bp.route("/<path:filename>", methods=["GET"])
def obtenerImage(filename):
    """Controlador auxiliar para poder mandar las imagenes de los productos.
    Parameters
    ----------
    filename : StrPath
    
    Returns
    -------
    Response"""
    try:
        imagen = os.path.join(UPLOAD_FOLDER, filename)
        return send_file(imagen)
    except FileNotFoundError:
        return send_file(os.path.join(UPLOAD_FOLDER, 'fff.png'))
