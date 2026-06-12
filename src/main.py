from fastapi import FastAPI, Depends, HTTPException
from redis.asyncio import Redis
from src import routes
from src.auth import get_current_user

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, db=0)

@app.on_event("startup")
async def startup_event():
    await redis_client.ping()

@app.on_event("shutdown")
async def shutdown_event():
    await redis_client.close()

app.include_router(routes.router, prefix="/api")

# Dependency
async def get_redis() -> Redis:
    return redis_client

# Optional: add middleware or exception handlers if needed

