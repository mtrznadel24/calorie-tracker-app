import redis as redis
from app.core.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def add_refresh_token(jti: str, user_id: int, ttl: int):
    redis_client.set(f"refresh:{jti}", user_id, ex=ttl)

def is_refresh_token_valid(jti: str) -> bool:
    return redis_client.exists(f"refresh:{jti}") == 1

def delete_refresh_token(jti: str):
    redis_client.delete(f"refresh:{jti}")