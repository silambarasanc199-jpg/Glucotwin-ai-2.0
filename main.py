"""FastAPI application for the GlucoTwin AI research prototype."""

import json
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import ROOT_DIR, cors_origins, evaluation_path, model_path
from app.database import connect, init_db
from app.routes import api, patients, predictions, sensors

logger = logging.getLogger("glucotwin")

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="GlucoTwin AI 2.0",
    description="Synthetic-data diabetes digital-twin research prototype. Not for clinical use.",
    version="2.0.0",
    lifespan=lifespan,
)

allowed_origins = cors_origins()
if allowed_origins:
    app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=False,
                       allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

app.include_router(patients.router)
app.include_router(sensors.router)
app.include_router(predictions.router)
app.include_router(api.router)
app.mount("/static", StaticFiles(directory=ROOT_DIR / "app" / "static"), name="static")


@app.middleware("http")
async def log_unhandled_errors(request, call_next):
    try:
        return await call_next(request)
    except Exception:
        route = request.scope.get("route")
        logger.exception("Unhandled request error on %s", getattr(route, "path", "unmatched route"))
        raise


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(ROOT_DIR / "app" / "templates" / "index.html")


@app.get("/health", tags=["system"])
def health() -> dict:
    with connect() as connection:
        connection.execute("SELECT 1").fetchone()
    return {"status": "ok", "service": "GlucoTwin AI 2.0", "database": "available", "model_trained": model_path().exists()}


@app.get("/api/dashboard/summary", tags=["dashboard"])
def dashboard_summary() -> dict:
    with connect() as connection:
        counts = connection.execute(
            """SELECT (SELECT COUNT(*) FROM patients) AS patients,
                      (SELECT COUNT(*) FROM readings) AS readings,
                      (SELECT COUNT(*) FROM predictions) AS predictions,
                      (SELECT COUNT(*) FROM readings WHERE is_synthetic = 1) AS synthetic_readings"""
        ).fetchone()
    report = None
    if evaluation_path().exists():
        try:
            report = json.loads(evaluation_path().read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            report = None
    return {
        "counts": dict(counts),
        "model": {"trained": model_path().exists(), "version": "2.0.0" if model_path().exists() else None,
                  "evaluation_available": report is not None,
                  "selected_model": report.get("selected_model") if report else None,
                  "test_metrics": report.get("test_metrics_at_threshold_0_5") if report else None,
                  "synthetic_only": bool(report and report.get("dataset", {}).get("synthetic"))},
        "data_notice": "Synthetic demo records are examples, not real patients." if counts["synthetic_readings"] else "No synthetic demo readings are currently stored.",
        "disclaimer": "Research prototype only. Do not use for diagnosis, treatment, or care decisions.",
    }
