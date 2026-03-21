import pytest
import json

# All tests use the Flask test client from conftest.py

# 1. Missing X-API-Key header returns 401
def test_sensor_data_no_api_key(client):
    print("\n[TEST] POST /api/sensor_data (no API key)")
    resp = client.post("/api/sensor_data", data=json.dumps({"temp": 22}), content_type="application/json")
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 401
    assert b"Missing X-API-Key header" in resp.data

# 2. Wrong API key value returns 401
def test_sensor_data_wrong_key(client):
    print("\n[TEST] POST /api/sensor_data (wrong API key)")
    resp = client.post(
        "/api/sensor_data",
        data=json.dumps({"temp": 22}),
        content_type="application/json",
        headers={"X-API-Key": "wrong-key"}
    )
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 401
    assert b"Invalid API key" in resp.data or b"Unauthorized" in resp.data

# 3. Correct key + valid JSON returns 201
def test_sensor_data_valid_key(client):
    print("\n[TEST] POST /api/sensor_data (valid API key)")
    resp = client.post(
        "/api/sensor_data",
        data=json.dumps({"temp": 22}),
        content_type="application/json",
        headers={"X-API-Key": "test-sensor-key"}
    )
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 201
    assert b"success" in resp.data or b"created" in resp.data or resp.status_code == 201
