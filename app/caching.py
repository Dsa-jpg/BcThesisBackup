import redis
import hashlib
from config import CACHE_EXPIRATION, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


r = redis.Redis(
    host= REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD)


def cache_response(message: str, response: str) -> None:
    # Create a unique key for the cache
    cache_key = hashlib.sha256(f"{message}".encode()).hexdigest()
    # Store the response in Redis with an expiration time
    r.setex(cache_key, CACHE_EXPIRATION, response)

def get_cached_response(message: str) -> str:
    # Create a unique key for the cache
    cache_key = hashlib.sha256(f"{message}".encode()).hexdigest()
    # Retrieve the cached response
    cached_response = r.get(cache_key)
    if cached_response:
        return cached_response.decode('utf-8')
    return None
    

