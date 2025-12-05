def test_user_registration_and_login(db_session, client):
    payload = {"username": "u1", "email": "u1@example.com", "password": "pass123"}

    # Register a new user
    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "id" in data

    # Login with the same username
    login_payload = {"username": "u1", "email": "u1@example.com"}
    r2 = client.post("/users/login", json={"username": "u1", "password": "pass123"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
