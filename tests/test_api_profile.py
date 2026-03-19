def test_get_profile_no_auth(client):
    # Arrange
    url = "http://localhost:5000/api/profile"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_get_profile_bad_token_format(client):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {'Authorization': 'NotBearer xyz'}

    # Act
    response = client.get(url, headers=headers)

    # Assert
    assert response.status_code == 401


def test_get_profile_invalid_token(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {"Authorization": "Bearer invalid_jwt_token"}
    mock_firebase_auth.side_effect = Exception("Invalid token")

    # Act
    response = client.get(url, headers=headers)

    # Assert
    assert response.status_code == 401
    mock_firebase_auth.assert_called_once()


def test_get_profile_success(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {'Authorization': 'Bearer valid_jwt_token'}

    # Act
    response = client.get(url, headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["uid"] == "test_user_123"
    assert data["profile"]["first_name"] == "Bryce"
    assert data["profile"]["last_name"] == "Reid"
    assert data["profile"]["student_id"] == "A12345678"
    mock_firebase_auth.assert_called_once()


def test_create_profile_missing_fields(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {"Authorization": "Bearer valid_jwt_token"}
    payload = {"first_name": "Bryce"}

    # Act
    response = client.post(url, json=payload, headers=headers)

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "All fields are required."
    mock_firebase_auth.assert_called_once()


def test_create_profile_success(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {"Authorization": "Bearer valid_jwt_token"}
    payload = {
        "first_name": "Bryce",
        "last_name": "Reid",
        "student_id": "A12345678",
    }

    # Act
    response = client.post(url, json=payload, headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Profile saved successfully"
    assert data["profile"]["first_name"] == "Bryce"
    assert data["profile"]["last_name"] == "Reid"
    assert data["profile"]["student_id"] == "A12345678"
    mock_firebase_auth.assert_called_once()


def test_update_profile_invalid_field(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {"Authorization": "Bearer valid_jwt_token"}
    payload = {
        "first_name": "Bryce",
        "last_name": "Reid",
        "student_id": "A1234567",
        "age": 25
    }

    # Act
    response = client.put(url, json=payload, headers=headers)

    # Assert
    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid field(s): age. Only first_name, last_name, and student_id are allowed." in data["errors"]
    mock_firebase_auth.assert_called_once()


def test_invalid_content_type(client, mock_firebase_auth):
    # Arrange
    url = "http://localhost:5000/api/profile"
    headers = {"Authorization": "Bearer valid_jwt_token"}
    payload = {
        "first_name": "Bryce",
        "last_name": "Reid",
        "student_id": "A1234567",
    }

    # Act
    response = client.post(url, data=payload, headers=headers)

    # Assert
    assert response.status_code == 415
    data = response.get_json()
    assert data["error"] == "Content-Type must be application/json"




