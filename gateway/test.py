from app.core.redis import redis_client


value = redis_client.set("test:key", "hello")
print(value)

print(redis_client.get("test:key"))