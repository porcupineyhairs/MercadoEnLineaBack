from flask_jwt_extended import JWTManager

from app.cahce import cache

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return cache.get(jti) is not None
