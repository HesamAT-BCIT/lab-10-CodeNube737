[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/2GzK8MHN)
## Overview

In this lab, you will build a complete automated test suite for your Flask application.

You will practice:

1. Unit testing pure validation helpers
2. Building reusable pytest fixtures
3. Integration testing profile API endpoints
4. Testing device authentication using API keys

The goal is to make your app testable without real Firebase credentials or network access.

---

## Quick Setup (One-Time)

1. Create and activate a virtual environment:
   - python -m venv .venv
   - .\\.venv\\Scripts\\Activate.ps1

2. Install dependencies:
   - pip install -r requirements.txt
   - pip install pytest pytest-cov

3. Make sure your project runs locally before starting tests.

4. Run tests with:
   - pytest tests/ -v
   - pytest tests/ --cov=utils --cov=blueprints --cov=decorators

---

## Task 1: Unit Testing Your Validators

Create tests/test_validators.py and write parametrized tests for the pure functions in utils/.

### What to test

1. validate_profile_data(first_name, last_name, student_id)
   - Cover all equivalence partitions from lecture:
     - Empty strings
     - None
     - Whitespace-only strings
     - Valid combinations
     - All-empty values

2. normalize_profile_data(first_name, last_name, student_id)
   - Whitespace stripping behavior
   - None handling
   - Conversion of student_id to string

### Suggested scope

1. 8 to 10 parametrized test cases for validate_profile_data
2. 4 to 5 test cases for normalize_profile_data
3. Run pytest --cov=utils and target at least 90 percent coverage for utils

---

## Task 2: Setting Up Test Infrastructure

A starter tests/conftest.py is provided. Complete it and adjust it to match your code paths.

### Fixtures to complete

1. client
   - Flask test client with TESTING = True

2. mock_firebase_auth
   - Patch firebase_admin.auth.verify_id_token
   - Return {"uid": "test_user_123"}

3. mock_firestore
   - Patch firebase.db with a MagicMock
   - Support chained calls used by your app, such as:
     - db.collection().document().get()
     - db.collection().document().set()
     - db.collection().document().update()

### Guidance

1. Start from the provided starter fixtures in tests/conftest.py
2. Complete the mock_firebase_auth fixture as needed for your token scenarios
3. Complete/mock mock_firestore chaining by inspecting your own route and helper code paths

---

## Task 3: Integration Testing API Endpoints

Create tests/test_api_profile.py and write integration tests for profile CRUD endpoints.

### Required test cases (minimum 5)

1. test_get_profile_no_auth
   - GET without Authorization header returns 401

2. test_get_profile_bad_token_format
   - Authorization header without Bearer prefix returns 401

3. test_get_profile_invalid_token
   - Mock verify_id_token to raise Exception, expect 401

4. test_get_profile_success
   - Valid mocked token + mocked Firestore, expect 200 with profile payload

5. test_create_profile_missing_fields
   - POST incomplete JSON body, expect 400

6. test_create_profile_success (recommended bonus)
   - POST valid data with mocked auth and Firestore, expect 200

7. test_update_profile_invalid_field (recommended bonus)
   - PUT {"age": 25}, expect 400 and whitelist error message

---

## Task 4: Testing Device Authentication

Create tests/test_api_sensor.py and test the require_api_key decorator path.

### Required test cases (minimum 3)

1. test_sensor_data_no_api_key
   - Missing X-API-Key header returns 401

2. test_sensor_data_wrong_key
   - Wrong API key value returns 401

3. test_sensor_data_valid_key
   - Correct key + valid JSON returns 201

---

## Task 5: Continuous Integration with GitHub Actions

Use the provided GitHub Actions workflow to run tests automatically on every push.

### Steps

1. Review the provided workflow at .github/workflows/ci.yml.
2. Update it only if needed for your project setup.
3. Push at least one commit to trigger GitHub Actions.
4. Ensure that the pipeline runs successfully and reports test results.
5. Capture proof of one successful (green) run.

---

## Deliverables

Complete and submit the following files/artifacts:

```
tests/
├── conftest.py              # Starter fixtures: client, mock_firebase_auth, mock_firestore
├── test_validators.py       # 12+ parametrized unit tests
├── test_api_profile.py      # 5+ required integration tests for /api/profile
└── test_api_sensor.py       # 3+ tests for /api/sensor_data

.github/
└── workflows/
   └── ci.yml               # Starter GitHub Actions workflow running pytest on push
```

CI proof (include in your submission):
- One screenshot of a successful (green) GitHub Actions run
- The commit SHA that triggered that run
- The GitHub Actions run URL

---

## Success Criteria

1. All tests pass with:
   - pytest tests/ -v

2. No tests require real Firebase credentials or network calls

3. Coverage report is generated with:
   - pytest tests/ --cov=utils --cov=blueprints --cov=decorators

4. GitHub Actions workflow runs on push and reports test results in the Actions tab

5. Submission includes CI proof (green run screenshot, triggering commit SHA, and run URL)

---

## Rubric

Each criterion is scored out of 4 points.

### 1. Unit Testing (Validators) - /4

- Level 4 (4): Thorough parametrized tests for both validator functions, including None, empty, whitespace, and valid inputs.
- Level 3 (3): Most validator scenarios are covered with good assertions; a few edge cases are missing.
- Level 2 (2): Basic validator tests exist but miss several required partitions.
- Level 1 (1): Minimal or ineffective validator testing.

### 2. Test Infrastructure (Fixtures and Mocking) - /4

- Level 4 (4): Reusable fixtures (client, mock_firebase_auth, mock_firestore) are complete and isolate tests from real Firebase/network calls.
- Level 3 (3): Required fixtures are mostly correct with minor gaps.
- Level 2 (2): Fixtures are incomplete or unreliable; isolation is inconsistent.
- Level 1 (1): Little or no fixture setup; tests depend on real services.

### 3. Integration Testing (/api/profile) - /4

- Level 4 (4): All required /api/profile scenarios are tested with accurate status and payload checks.
- Level 3 (3): Most required scenarios are covered; minor assertion gaps remain.
- Level 2 (2): Some profile tests exist, but several required scenarios are missing.
- Level 1 (1): Minimal or no meaningful /api/profile integration testing.

### 4. Device Authentication Testing (/api/sensor_data) - /4

- Level 4 (4): Missing key, wrong key, and valid key paths are all tested with correct assertions.
- Level 3 (3): Core API key scenarios are covered with minor detail gaps.
- Level 2 (2): Partial sensor auth testing with weak or incomplete assertions.
- Level 1 (1): Minimal or no API key testing for sensor endpoint.

### 5. Continuous Integration (CI) with GitHub Actions - /4

- Level 4 (4): Workflow is correctly configured in .github/workflows, runs automatically on push, and submission includes clear proof of a successful green run (screenshot, SHA, URL).
- Level 3 (3): Workflow runs on push and basic proof is provided, but there are minor reliability/configuration issues.
- Level 2 (2): Basic CI exists but is inconsistent, incomplete, or proof is partial.
- Level 1 (1): Minimal or no CI setup; tests do not run automatically and no valid proof is provided.

**Total Score: /20**
