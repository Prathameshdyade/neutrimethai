import redis
from app.core.config import settings


class _InMemoryCache:
	def __init__(self):
		self._store = {}

	def get(self, key):
		return self._store.get(key)

	def set(self, key, value):
		self._store[key] = value

	def setex(self, key, ttl, value):
		# TTL ignored for quick local fallback
		self._store[key] = value

	def delete(self, key):
		self._store.pop(key, None)


try:
	redis_url = getattr(settings, "REDIS_URL", None)
	if not redis_url:
		raise RuntimeError("REDIS_URL not configured")

	_client = redis.Redis.from_url(redis_url, decode_responses=True)
	# quick health check
	_client.ping()
	redis_client = _client
except Exception as e:
	# Fall back to an in-memory cache so the app runs without Redis
	print(f"Warning: Redis unavailable ({e}). Using in-memory fallback cache.")
	redis_client = _InMemoryCache()
