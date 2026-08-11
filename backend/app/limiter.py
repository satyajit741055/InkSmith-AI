from limits.storage import RedisStorage
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings


def create_limiter() -> tuple[Limiter, str]:
    """Use Redis in production; fall back to in-memory storage locally."""
    try:
        storage = RedisStorage(settings.REDIS_URL)
        if not storage.check():
            raise ConnectionError("Redis did not respond to ping")
        limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL)
        return limiter, "redis"
    except Exception:
        limiter = Limiter(key_func=get_remote_address)
        return limiter, "memory"

# Single shared instance, created once at import time
limiter, rate_limiter_storage = create_limiter()