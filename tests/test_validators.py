import pytest
from utils.validation import validate_profile_data, normalize_profile_data


@pytest.mark.parametrize("first_name, last_name, student_id, expected",
    [
        # Valid partition
        ("Bryce", "Reid", "A01298718", None),
        # Valid partition with whitespaces
        (" Bryce ", " Reid ", " A01298718 ", None),
        # Missing first_name
        ("", "Reid", "A01298718", "All fields are required."),
        # Missing last_name
        ("Bryce", "", "A01298718", "All fields are required."),
        # Missing student_id
        ("Bryce", "Reid", "", "All fields are required."),
        # None value first_name
        (None, "Reid", "A01298718", "All fields are required."),
        # None value last_name
        ("Bryce", None, "A01298718", "All fields are required."),
        # None value student_id
        ("Bryce", "Reid", None, "All fields are required."),
        # Missing first_name & last_name
        ("", "", "A01298718", "All fields are required."),
        # Missing last_name & student_id
        ("Bryce", "", "", "All fields are required."),
        # Missing first_name & student_id
        ("", "Reid", "", "All fields are required."),
        # Whitespace-only first_name
        (" ", "Reid", "A01298718", None),
        # Whitespace-only last_name
        ("Bryce", " ", "A01298718", None),
        # Whitespace-only student_id
        ("Bryce", "Reid", " ", None),
        # Whitespace-only first_name & last_name
        (" ", " ", "A01298718", None),
        # Whitespace-only last_name & student_id
        ("Bryce", " ", " ", None),
        # Whitespace-only first_name & student_id
        (" ", "Reid", " ", None),
        # All empty
        ("", "", "", "All fields are required."),
        # All None
        (None, None, None, "All fields are required."),
        # All Whitespace-only strings
        (" ", " ", " ", None),
    ]
)
def test_validate(first_name, last_name, student_id, expected):
    assert validate_profile_data(first_name, last_name, student_id) == expected


@pytest.mark.parametrize("first_name, last_name, student_id, expected_first, expected_last, expected_sid",
    [
        # Whitespace stripping behavior
        (" Bryce ", " Reid ", " A01298718 ", "Bryce", "Reid", "A01298718"),
        # None value first_name
        (None, "Reid", "A01298718", "", "Reid", "A01298718"),
        # None value last_name
        ("Bryce", None, "A01298718", "Bryce", "", "A01298718"),
        # None value student_id
        ("Bryce", "Reid", None, "Bryce", "Reid", ""),
        # Conversion of student_id to string
        ("Bryce", "Reid", 111298718, "Bryce", "Reid", "111298718"),
    ]
)
def test_normalize(first_name, last_name, student_id, expected_first, expected_last, expected_sid):
    data = normalize_profile_data(first_name, last_name, student_id)
    assert data["first_name"] == expected_first
    assert data["last_name"] == expected_last
    assert data["student_id"] == expected_sid


def test_get_current_user_logged_in(client):
    # Arrange
    app = client.application

    with app.test_request_context():
        from flask import session
        session["logged_in"] = True
        session["username"] = "bryce"

        # Act
        from utils.auth import get_current_user
        user = get_current_user()

        # Assert
        assert user == "bryce"
