from fastapi.testclient import TestClient

from app.main import app


def test_top_level_reading_and_prediction_routes(client):
    patient_id = client.post("/api/patients", json={"is_synthetic": True}).json()["patient_id"]
    reading = client.post("/api/readings", json={
        "patient_id": patient_id,
        "timestamp": "2026-01-10T12:00:00Z",
        "glucose_mg_dl": 132,
        "is_synthetic": True,
    })
    assert reading.status_code == 201
    assert reading.json()["patient_id"] == patient_id

    prediction = client.post("/api/predictions", json={"patient_id": patient_id})
    assert prediction.status_code == 503
    history = client.get("/api/predictions", params={"patient_id": patient_id})
    assert history.status_code == 200
    assert history.json() == {"predictions": [], "count": 0, "limit": 100}


def test_workflow_routes_are_documented(client):
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/readings" in paths
    assert "/api/predictions" in paths
    assert "post" in paths["/api/readings"]
    assert {"get", "post"}.issubset(paths["/api/predictions"])


def test_dashboard_uses_configurable_api_and_serves_assets(client):
    page = client.get("/").text
    script = client.get("/static/js/app.js").text
    config = client.get("/static/js/config.js").text
    chart = client.get("/static/js/vendor/chart.umd.min.js")
    styles = client.get("/static/css/style.css")
    assert "static/js/config.js" in page
    assert "static/js/vendor/chart.umd.min.js" in page
    assert "GLUCO_TWIN_CONFIG" in script
    assert "Chart library unavailable" in script
    assert 'apiBaseUrl: ""' in config
    assert chart.status_code == 200
    assert styles.status_code == 200


def test_sqlite_records_survive_application_restart(tmp_path, monkeypatch):
    database = tmp_path / "persistent.sqlite3"
    monkeypatch.setenv("GLUCOTWIN_DATABASE_PATH", str(database))
    monkeypatch.setenv("GLUCOTWIN_MODEL_PATH", str(tmp_path / "missing-model.joblib"))
    monkeypatch.setenv("GLUCOTWIN_EVALUATION_PATH", str(tmp_path / "missing-evaluation.json"))

    with TestClient(app) as first_run:
        patient_id = first_run.post("/api/patients", json={"is_synthetic": True}).json()["patient_id"]
        created = first_run.post("/api/readings", json={
            "patient_id": patient_id,
            "timestamp": "2026-01-10T12:00:00Z",
            "glucose_mg_dl": 132,
            "is_synthetic": True,
        })
        assert created.status_code == 201

    with TestClient(app) as restarted:
        patients = restarted.get("/api/patients").json()
        readings = restarted.get(f"/api/patients/{patient_id}/readings").json()
        assert any(item["patient_id"] == patient_id for item in patients)
        assert readings["count"] == 1
