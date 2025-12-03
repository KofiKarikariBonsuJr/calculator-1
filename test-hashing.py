from app.security import hash_password, verify_password

def test_password_hashing():
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)