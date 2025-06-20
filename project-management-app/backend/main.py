from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .core.config import settings
from .routers import auth as auth_router, users as user_router
from .routers import project as project_router
from .routers import deliverable as deliverable_router
from .routers import consultant as consultant_router
from .routers import finance as finance_router
from .routers import notifications as notification_router # New

from .database import engine

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
)

os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(project_router.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(deliverable_router.router, prefix="/api/v1/deliverables", tags=["Deliverables"])
app.include_router(consultant_router.router, prefix="/api/v1/consultants", tags=["Consultants"])
app.include_router(finance_router.router, prefix="/api/v1/finance", tags=["Finance"])
app.include_router(notification_router.router, prefix="/ws", tags=["Notifications & WebSockets"]) # Added WebSocket router


@app.get("/")
async def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} API - Now with WebSockets!"}
