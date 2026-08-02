from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.blog import router as blog_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup: Initialize database, caches, etc.
    print("Application starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    # Shutdown: Clean up resources
    print("Application shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"]
)
app.include_router(blog_router, prefix="/api/v1/blog", tags=["blog"])

app.mount("/blogs", StaticFiles(directory="blogs"), name="blogs")