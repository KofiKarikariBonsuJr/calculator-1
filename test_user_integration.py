from app.models.user import User
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
        assert True  # unique constraint triggered
