from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.blog import router as blog_router
from app.limiter import limiter,rate_limiter_storage
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.config import settings
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

Path(settings.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

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
app.state.limiter = limiter
app.state.rate_limiter_storage = rate_limiter_storage
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000","http://localhost:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    origin = request.headers.get("origin", "")
    allowed = ["http://localhost:5173", "http://localhost:3000", "http://localhost:8001"]
    headers = {}
    if origin in allowed:
        headers["Access-Control-Allow-Origin"] = origin
        headers["Access-Control-Allow-Credentials"] = "true"
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers=headers,
    )

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(blog_router, prefix="/api/v1/blog", tags=["blog"])

