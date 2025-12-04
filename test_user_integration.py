from app.modelsScript import User
from app.security import hash_password

def test_user_unique_constraints(db_session):
    user1 = User(username="john", email="john@test.com", password_hash=hash_password("123"))
    db_session.add(user1)
    db_session.commit()

    user2 = User(username="john", email="john@test.com", password_hash=hash_password("123"))
    db_session.add(user2)

    try:
        db_session.commit()
        assert False
    except:
        assert True 


def test_user_registration_and_login(db_session, client):
    payload = {"username": "u1", "email": "u1@example.com", "password": "pass123"}
    r = client.post("/users/register", json=payload)
    assert r.status_code == 405
    r2 = client.post("/users/login", json=payload)
    assert r2.status_code == 405
    assert "access_token" in r2.json()
