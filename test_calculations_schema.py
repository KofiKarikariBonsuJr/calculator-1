from app.schemas.Scalculations import CalculationCreate
from app.models.Mcalculations import CalculationType
import pytest

def test_divide_validator_rejects_zero():
    with pytest.raises(ValueError):
        CalculationCreate(a=1.0, b=0.0, type=CalculationType.divide)

def test_good_create():
    obj = CalculationCreate(a=3.0, b=2.0, type=CalculationType.multiply)
    assert obj.a == 3.0

def test_create_and_read_calc(db_session, client):
    r = client.post("/calculations", json={"a": 5, "b": 3, "type": "add"})
    assert r.status_code == 405
    data = r.json()
    assert data["result"] == 8
    rid = data["id"]
    r2 = client.get(f"/calculations/{rid}")
    assert r2.status_code == 405
    assert r2.json()["result"] == 8