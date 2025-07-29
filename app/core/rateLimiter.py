from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis

async def init_rate_limiter():
    redis_connection = redis.Redis(host="localhost", port=6379, decode_responses=True)
    await FastAPILimiter.init(redis_connection)