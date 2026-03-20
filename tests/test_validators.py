import pytest
from utils.validation import validate_profile_data, normalize_profile_data

'''
Unit tests for profile data validation and normalization functions.
'''
@pytest.mark.parametrize(
    "first_name, last_name, student_id, expected",
    [
        ("", "", "", "All fields are required."),  # all empty
        (None, None, None, "All fields are required."),  # all None
        (" ", " ", " ", None),  # all whitespace (should pass, as whitespace is not checked)
        ("John", "", "123456", "All fields are required."),  # missing last name
        ("", "Doe", "123456", "All fields are required."),  # missing first name
        ("John", "Doe", None, "All fields are required."),  # missing student_id
        ("John", "Doe", "123456", None),  # all valid
        (" Jane ", " Doe ", " 654321 ", None),  # valid with whitespace
        ("John", "Doe", 123456, None),  # student_id as int
        ("John", "Doe", "", "All fields are required."),  # missing student_id (empty string)
    ]
)
def test_validate_profile_data(first_name, last_name, student_id, expected):
    result = validate_profile_data(first_name, last_name, student_id)
    assert result == expected

'''
Unit tests for profile data normalization function.
'''
@pytest.mark.parametrize(
    "first_name, last_name, student_id, expected",
    [
        (" John ", " Doe ", " 123456 ", {"first_name": "John", "last_name": "Doe", "student_id": "123456"}),
        (None, "Doe", 123456, {"first_name": "", "last_name": "Doe", "student_id": "123456"}),
        ("Jane", None, None, {"first_name": "Jane", "last_name": "", "student_id": ""}),
        (" ", " ", " ", {"first_name": "", "last_name": "", "student_id": ""}),
        ("Alice", "Smith", 789012, {"first_name": "Alice", "last_name": "Smith", "student_id": "789012"}),
    ]
)
def test_normalize_profile_data(first_name, last_name, student_id, expected):
    result = normalize_profile_data(first_name, last_name, student_id)
    assert result == expected

# ----------------------
# Additional utils tests
# ----------------------


import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, session

# --- Tests for utils.auth.get_current_user ---
@pytest.mark.parametrize("logged_in, username, expected", [
    (True, "alice", "alice"),
    (False, "alice", None),
    (True, None, None),
    (False, None, None),
])
def test_get_current_user(logged_in, username, expected):
    app = Flask(__name__)
    app.secret_key = "test"
    with app.test_request_context():
        session.clear()
        session["logged_in"] = logged_in
        if username is not None:
            session["username"] = username
        from utils.auth import get_current_user
        assert get_current_user() == expected

# --- Tests for utils.profile.get_profile_doc_ref ---
def test_get_profile_doc_ref():
    with patch.dict("sys.modules", {"firebase": MagicMock()}):
        from utils import profile
        mock_db = MagicMock()
        profile.db = mock_db
        mock_collection = MagicMock()
        mock_doc = MagicMock()
        mock_db.collection.return_value = mock_collection
        mock_collection.document.return_value = mock_doc
        result = profile.get_profile_doc_ref("bob")
        mock_db.collection.assert_called_once_with("profiles")
        mock_collection.document.assert_called_once_with("bob")
        assert result == mock_doc

# --- Tests for utils.profile.get_profile_data ---
def test_get_profile_data_exists():
    with patch.dict("sys.modules", {"firebase": MagicMock()}):
        from utils import profile
        mock_doc = MagicMock()
        mock_doc.get.return_value = mock_doc
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"foo": "bar"}
        profile.get_profile_doc_ref = MagicMock(return_value=mock_doc)
        result = profile.get_profile_data("bob")
        assert result == {"foo": "bar"}

def test_get_profile_data_missing():
    with patch.dict("sys.modules", {"firebase": MagicMock()}):
        from utils import profile
        mock_doc = MagicMock()
        mock_doc.get.return_value = mock_doc
        mock_doc.exists = False
        profile.get_profile_doc_ref = MagicMock(return_value=mock_doc)
        result = profile.get_profile_data("bob")
        assert result == {}

# --- Tests for utils.profile.set_profile ---
def test_set_profile():
    with patch.dict("sys.modules", {"firebase": MagicMock()}):
        from utils import profile
        mock_doc = MagicMock()
        profile.get_profile_doc_ref = MagicMock(return_value=mock_doc)
        profile.set_profile("bob", {"foo": "bar"}, merge=True)
        mock_doc.set.assert_called_once_with({"foo": "bar"}, merge=True)
