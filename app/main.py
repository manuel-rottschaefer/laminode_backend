from fastapi import FastAPI
from .api.v1.endpoints import plugins, releases
from .core.logging_config import logger

app = FastAPI(
    title="LamiNode Plugin Backend",
    description="Backend for managing LamiNode plugins, schemas, and adapters.",
    version="1.0.0"
)

# Include Routers
app.include_router(plugins.router, prefix="/api/v1/plugins", tags=["Plugins"])
app.include_router(releases.router, prefix="/api/v1/releases", tags=["Releases"])

@app.on_event("startup")
async def startup_event():
    logger.info("LamiNode Backend is starting up...")

@app.get("/")
async def root():
    return {"message": "Welcome to LamiNode Plugin Backend API"}
