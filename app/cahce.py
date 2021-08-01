from flask_caching import Cache

from app.configs import JWT_ACCESS_TOKEN_EXPIRES

cache = Cache(
    config={
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": JWT_ACCESS_TOKEN_EXPIRES.total_seconds(),
    }
)
