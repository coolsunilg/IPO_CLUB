from fastapi import FastAPI


from app.core.config import settings
from app.core.database import Base, engine
from app.core.logger import app_logger
from app.models.user import Member
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.users import router as member_router
from app.api.angelone import router as angel_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_NAME,
    version=settings.API_VERSION,
)
app.include_router(dashboard_router)
app.include_router(member_router)
app.include_router(angel_router)

@app.on_event("startup")
def startup():
    app_logger.info("IPO CLUB Backend Started")


@app.get("/")
def root():
    return {
        "application": settings.API_NAME,
        "version": settings.API_VERSION,
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/version")
def version():
    return {"version": settings.API_VERSION}