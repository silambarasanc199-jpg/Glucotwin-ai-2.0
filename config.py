"""Runtime paths and safe, environment-based configuration."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env", override=False)


def configured_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    path = Path(value).expanduser() if value else default
    return path if path.is_absolute() else (ROOT_DIR / path).resolve()


def database_path() -> Path:
    return configured_path("GLUCOTWIN_DATABASE_PATH", ROOT_DIR / "data" / "glucotwin.sqlite3")


def model_path() -> Path:
    return configured_path("GLUCOTWIN_MODEL_PATH", ROOT_DIR / "models" / "glucotwin_model.joblib")


def evaluation_path() -> Path:
    return configured_path("GLUCOTWIN_EVALUATION_PATH", ROOT_DIR / "models" / "evaluation.json")


def cors_origins() -> list[str]:
    return [origin.strip() for origin in os.getenv("GLUCOTWIN_CORS_ORIGINS", "").split(",") if origin.strip()]
