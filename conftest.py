import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("GLUCOTWIN_DATABASE_PATH", str(tmp_path / "test.sqlite3"))
    monkeypatch.setenv("GLUCOTWIN_MODEL_PATH", str(tmp_path / "missing-model.joblib"))
    monkeypatch.setenv("GLUCOTWIN_EVALUATION_PATH", str(tmp_path / "missing-evaluation.json"))
    with TestClient(app) as test_client:
        yield test_client
