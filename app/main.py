from fastapi import FastAPI
from app.core.config import Base, engine
from fastapi_cache import FastAPICache
from app.core.rateLimiter import init_rate_limiter
from fastapi import FastAPI, Request
from app.core.log import logger

from app.api.endpoints.v1.routes import expertRouter
from app.api.endpoints.v1.routes.prioritetRouter import router as prioritet_router


Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="AzTU E-Grant",
    description="Azərbaycan Texniki Universiteti E-Grant  tətbiqi",
    version="1.0.0"
)


app.include_router(prioritet_router.router, prefix="/api", tags=["Prioritet"])
app.include_router(expertRouter.router, prefix= "/api", tags=["Experts"])


@app.get("/test")
def test():
    return {"message": "OK"}

@app.on_event("startup")
async def startup():
    await init_rate_limiter()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response