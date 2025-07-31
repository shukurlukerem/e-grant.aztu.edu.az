from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi import FastAPI, Request
from app.api.endpoints.v1.routes import expertRouter
from app.api.endpoints.v1.routes.prioritetRouter import router as prioritet_router
from app.api.endpoints.v1.routes.userRouter import router as user_router
from app.api.endpoints.v1.routes.projectRouter import router as project_router
from app.api.endpoints.v1.routes.expertRouter import router as expert_router
from app.api.endpoints.v1.routes.authRouter import router as auth_router
from app.api.endpoints.v1.routes.smetaRouter.otherExpenses import router as other_expenses_router
from app.api.endpoints.v1.routes.smetaRouter.rentRouter import router as rent_router
from app.api.endpoints.v1.routes.smetaRouter.salaryRouter import router as salary_router
from app.api.endpoints.v1.routes.smetaRouter.smetaRouter import router as smeta_router
from app.api.endpoints.v1.routes.smetaRouter.subjectRouter import router as subject_router

app = FastAPI(
    title="AzTU E-Grant",
    description="Azərbaycan Texniki Universiteti E-Grant tətbiqi",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(prioritet_router, prefix="/api", tags=["Prioritet"])
app.include_router(expert_router, prefix= "/api", tags=["Experts"])
app.include_router(user_router, prefix="/api", tags=["Profile"])
app.include_router(project_router, prefix="/api", tags=["Projects"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(other_expenses_router, prefix="/api", tags=["Other Expenses"])
app.include_router(rent_router, prefix="/api", tags=["Rent"])
app.include_router(salary_router, prefix="/api", tags=["Salary"])
app.include_router(smeta_router, prefix="/api", tags=["Smeta"])
app.include_router(subject_router, prefix="/api", tags=["Subject"])


@app.get("/test")
def test():
    return {"message": "OK"}

# @app.on_event("startup")
# async def startup():
#     await init_rate_limiter()

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger.info(f"Incoming request: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Response status: {response.status_code}")
#     return response