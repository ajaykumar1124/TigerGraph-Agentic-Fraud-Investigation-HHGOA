from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.api.health import router as health_router
from backend.api.investigations import router as investigations_router
from backend.api.data import router as data_router
from backend.api.fraud import router as fraud_router
from backend.api.cases import router as cases_router
from backend.api.investigation import router as investigation_router

app = FastAPI(
    title="TigerGraph Agentic Fraud Investigation API", 
    version="0.1.0", 
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost", "http://127.0.0.1", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers with /api prefix
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(investigations_router, prefix="/api/v1", tags=["investigations"])
app.include_router(fraud_router, prefix="/api/v1", tags=["fraud"])
app.include_router(cases_router, prefix="/api/v1", tags=["cases"])
app.include_router(data_router, prefix="/api/v1", tags=["data-upload"])
app.include_router(investigation_router, prefix="/api", tags=["ai-investigation"])


@app.get("/")
def read_root():
    return {"service": "tigergraph-agentic", "status": "ok", "version": "0.1.0"}


@app.get("/api")
def api_root():
    return {"message": "TigerGraph Agentic Fraud Investigation API", "version": "0.1.0", "docs": "/api/docs"}


