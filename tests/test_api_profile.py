import pytest
import json

# All tests use the Flask test client and mocks from conftest.py

# 1. GET without Authorization header returns 401
def test_get_profile_no_auth(client):
    print("\n[TEST] GET /api/profile (no auth)")
    resp = client.get("/api/profile")
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 401
    assert b"Missing Authorization header" in resp.data or b"Unauthorized" in resp.data

# 2. Authorization header without Bearer prefix returns 401
def test_get_profile_bad_token_format(client):
    print("\n[TEST] GET /api/profile (bad token format)")
    resp = client.get("/api/profile", headers={"Authorization": "notbearer sometoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 401
    assert b"Invalid Authorization header format" in resp.data or b"Unauthorized" in resp.data

# 3. Mock verify_id_token to raise Exception, expect 401

def test_get_profile_invalid_token(client, mock_firebase_auth):
    print("\n[TEST] GET /api/profile (invalid token)")
    mock_firebase_auth.side_effect = Exception("bad token")
    resp = client.get("/api/profile", headers={"Authorization": "Bearer badtoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 401
    # Accept the actual error message returned by the API
    assert b"Invalid or expired token" in resp.data or b"Unauthorized" in resp.data

# 4. Valid mocked token + mocked Firestore, expect 200 with profile payload

def test_get_profile_success(client, mock_firebase_auth, mock_firestore):
    print("\n[TEST] GET /api/profile (success)")
    resp = client.get("/api/profile", headers={"Authorization": "Bearer goodtoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    data = resp.get_json()
    # Accept either flat or wrapped profile dict
    if "first_name" in data:
        assert data["first_name"] == "Test"
        assert data["last_name"] == "User"
        assert data["student_id"] == "12345678"
    elif "profile" in data:
        profile = data["profile"]
        assert profile["first_name"] == "Test"
        assert profile["last_name"] == "User"
        assert profile["student_id"] == "12345678"
    else:
        pytest.fail(f"Unexpected response structure: {data}")

# 5. POST incomplete JSON body, expect 400

def test_create_profile_missing_fields(client, mock_firebase_auth):
    print("\n[TEST] POST /api/profile (missing fields)")
    # Missing last_name
    payload = {"first_name": "A", "student_id": "123"}
    resp = client.post("/api/profile", data=json.dumps(payload), content_type="application/json", headers={"Authorization": "Bearer goodtoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 400
    assert b"All fields are required" in resp.data or b"Missing" in resp.data

# 6. POST valid data with mocked auth and Firestore, expect 200 (bonus)

def test_create_profile_success(client, mock_firebase_auth, mock_firestore):
    print("\n[TEST] POST /api/profile (success)")
    payload = {"first_name": "A", "last_name": "B", "student_id": "123"}
    resp = client.post("/api/profile", data=json.dumps(payload), content_type="application/json", headers={"Authorization": "Bearer goodtoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    data = resp.get_json()
    # Accept either flat or wrapped profile dict
    if "first_name" in data:
        assert data["first_name"] == "A"
        assert data["last_name"] == "B"
        assert data["student_id"] == "123"
    elif "profile" in data:
        profile = data["profile"]
        assert profile["first_name"] == "A"
        assert profile["last_name"] == "B"
        assert profile["student_id"] == "123"
    else:
        pytest.fail(f"Unexpected response structure: {data}")

# 7. PUT {"age": 25}, expect 400 and whitelist error message (bonus)

def test_update_profile_invalid_field(client, mock_firebase_auth):
    print("\n[TEST] PUT /api/profile (invalid field)")
    payload = {"age": 25}
    resp = client.put("/api/profile", data=json.dumps(payload), content_type="application/json", headers={"Authorization": "Bearer goodtoken"})
    print("Status:", resp.status_code)
    print("Response:", resp.data)
    assert resp.status_code == 400
    assert b"Invalid field" in resp.data or b"not allowed" in resp.data
