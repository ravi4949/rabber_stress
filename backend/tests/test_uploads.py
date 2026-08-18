"""Unit Tests for CSV Upload & Validation."""

import pytest
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_invalid_csv_missing_columns():
    token_res = client.post("/api/v1/auth/register", json={"email": "val@test.com", "password": "password123"})
    token = token_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    csv_content = b"colA,colB\n1.0,2.0\n3.0,4.0"
    res = client.post(
        "/api/v1/analyses",
        files={"file": ("invalid.csv", io.BytesIO(csv_content), "text/csv")},
        headers=headers
    )
    assert res.status_code == 422
    assert "missing required columns" in res.json()["detail"].lower()
