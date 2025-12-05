def test_user_registration_and_login(db_session, client):
    payload = {"username": "u1111", "email": "u1@example.com", "password": "pass123321"}

    r = client.post("/users/register", json=payload)
    assert r.status_code == 200
    data = r.json()

    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"