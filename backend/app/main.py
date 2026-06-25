from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(title=settings.APP_NAME, debug=settings.APP_DEBUG)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
def root_health():
    return {"status": "ok", "service": "ari-backend", "api": "/api/v1"}
