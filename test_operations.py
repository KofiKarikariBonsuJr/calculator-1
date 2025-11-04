from Calculator.Addition import addition
from Calculator.Subtraction import subtraction
from Calculator.Division import division
from httpx import AsyncClient
from main import app
import pytest

def test_add():
    assert addition(2, 3) == 5
def test_subtract():
    assert subtraction(3, 5) == 2
def test_divide():
    assert division(2, 6) == 3    

@pytest.mark.asyncio
async def test_add_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 5}
