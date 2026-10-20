def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "available"


def test_dashboard_and_openapi_pages(client):
    dashboard = client.get("/")
    assert dashboard.status_code == 200
    assert "GlucoTwin" in dashboard.text
    assert client.get("/docs").status_code == 200


def test_create_and_retrieve_anonymous_patient(client):
    created = client.post("/api/patients", json={"age": 43, "hba1c": 7.1})
    assert created.status_code == 201
    patient_id = created.json()["patient_id"]
    assert patient_id.startswith("PT-")
    retrieved = client.get(f"/api/patients/{patient_id}")
    assert retrieved.status_code == 200
    assert retrieved.json()["patient"]["age"] == 43
    assert retrieved.json()["patient"]["bmi"] is None
    assert retrieved.json()["reading_count"] == 0


def test_invalid_patient_input_is_rejected(client):
    assert client.post("/api/patients", json={"age": 0}).status_code == 422
    assert client.post("/api/patients", json={"name": "not accepted"}).status_code == 422


def test_sensor_ingestion_and_duplicate_handling(client):
    patient_id = client.post("/api/patients", json={}).json()["patient_id"]
    payload = {"timestamp": "2026-01-10T12:00:00Z", "glucose_mg_dl": 132,
               "heart_rate_bpm": 72, "sleep_hours": 7.5, "steps": 400}
    inserted = client.post(f"/api/patients/{patient_id}/readings", json=payload)
    assert inserted.status_code == 201
    assert inserted.json()["glucose_mg_dl"] == 132
    assert client.post(f"/api/patients/{patient_id}/readings", json=payload).status_code == 409
    fetched = client.get(f"/api/patients/{patient_id}/readings")
    assert fetched.status_code == 200
    assert fetched.json()["count"] == 1


def test_invalid_or_incomplete_reading_is_rejected(client):
    patient_id = client.post("/api/patients", json={}).json()["patient_id"]
    base = {"timestamp": "2026-01-10T12:00:00Z", "glucose_mg_dl": 132}
    assert client.post(f"/api/patients/{patient_id}/readings", json={"timestamp": base["timestamp"]}).status_code == 422
    assert client.post(f"/api/patients/{patient_id}/readings", json={**base, "glucose_mg_dl": 1000}).status_code == 422
    assert client.post(f"/api/patients/{patient_id}/readings", json={**base, "timestamp": "2026-01-10T12:00:00"}).status_code == 422


def test_batch_import_is_atomic_and_prevents_duplicates(client):
    patient_id = client.post("/api/patients", json={}).json()["patient_id"]
    url = f"/api/patients/{patient_id}/readings/batch"
    payload = {"readings": [
        {"timestamp": "2026-01-10T12:00:00Z", "glucose_mg_dl": 120, "source_record_id": "row-1"},
        {"timestamp": "2026-01-10T12:15:00Z", "glucose_mg_dl": 126, "source_record_id": "row-2"},
    ]}
    imported = client.post(url, json=payload)
    assert imported.status_code == 201
    assert imported.json()["created_count"] == 2
    duplicate_batch = {"readings": [
        {"timestamp": "2026-01-10T12:30:00Z", "glucose_mg_dl": 132, "source_record_id": "row-3"},
        {"timestamp": "2026-01-10T12:15:00Z", "glucose_mg_dl": 126, "source_record_id": "row-2"},
    ]}
    assert client.post(url, json=duplicate_batch).status_code == 409
    assert client.get(f"/api/patients/{patient_id}/readings").json()["count"] == 2


def test_prediction_requires_readings_and_trained_model(client):
    patient_id = client.post("/api/patients", json={}).json()["patient_id"]
    empty = client.post(f"/api/patients/{patient_id}/predict")
    assert empty.status_code == 422
    client.post(f"/api/patients/{patient_id}/readings", json={"timestamp": "2026-01-10T12:00:00Z", "glucose_mg_dl": 130})
    response = client.post(f"/api/patients/{patient_id}/predict")
    assert response.status_code == 503
    assert "python -m app.ml.train" in response.json()["detail"]


def test_dashboard_summary_reports_backend_counts(client):
    client.post("/api/patients", json={"is_synthetic": True})
    summary = client.get("/api/dashboard/summary").json()
    assert summary["counts"]["patients"] == 1
    assert summary["model"]["trained"] is False
    assert summary["model"]["test_metrics"] is None
