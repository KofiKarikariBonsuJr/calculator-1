from pydantic import ValidationError
from app.schemas.user import UserCreate

def test_email_validation():
    try:
        UserCreate(username="test", email="not-an-email", password="123")
        assert False
    except ValidationError:
        assert True
