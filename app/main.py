from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.database import engine, Base
from app.core.config import settings
from app.api.v1.routers import (
    auth_router, incidents_router, media_router, resources_router,
    reports_router, websocket_router, integrations_router, debug_router
)

# Lifespan context manager
async def lifespan(app: FastAPI):
    # Startup
    print("[STARTUP] Civil Defense Emergency Management System started")
    yield
    # Shutdown
    await engine.dispose()
    print("[SHUTDOWN] Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="Civil Defense Emergency Management System",
    description="Production-ready backend for emergency management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(incidents_router)
app.include_router(media_router)
app.include_router(resources_router)
app.include_router(reports_router)
app.include_router(websocket_router)
app.include_router(integrations_router)
app.include_router(debug_router)  # DEBUG/TESTING ROUTER - NO AUTHENTICATION


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Civil Defense Emergency Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
