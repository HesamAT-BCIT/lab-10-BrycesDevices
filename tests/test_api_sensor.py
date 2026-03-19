def test_sensor_data_server_api_key_not_configured(client, monkeypatch):
    # Arrange
    url = "http://localhost:5000/api/sensor_data"
    monkeypatch.setenv("SENSOR_API_KEY", "")

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "API key not configured on server"


def test_sensor_data_no_api_key(client):
    # Arrange
    url = "http://localhost:5000/api/sensor_data"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Missing X-API-Key header"


def test_sensor_data_wrong_key(client):
    # Arrange
    url = "http://localhost:5000/api/sensor_data"
    headers = {"X-API-Key": "wrong-key"}

    # Act
    response = client.post(url, headers=headers)

    # Assert
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Unauthorized"


def test_sensor_data_valid_key(client):
    # Arrange
    url = "http://localhost:5000/api/sensor_data"
    headers = {"X-API-Key": "test-sensor-key"}
    payload = {"temp": 22}

    # Act
    response = client.post(url, json=payload, headers=headers)

    # Assert
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Sensor data received successfully"
