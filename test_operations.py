from Calculator.Addition import addition
from Calculator.Subtraction import subtraction
from Calculator.Division import division
from httpx import AsyncClient, ASGITransport
from main import app
from playwright.sync_api import sync_playwright
import pytest
import subprocess
import time

def test_add():
    assert addition(2, 3) == 5
def test_subtract():
    assert subtraction(3, 5) == 2
def test_divide():
    assert division(2, 6) == 3    

@pytest.mark.asyncio
async def test_add_endpoint():
 transport = ASGITransport(app=app)
 async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/add?a=5&b=3")
 assert response.status_code == 200
 assert response.json() == {"result": 8}

def test_calculator_ui():
    
    
    
    server = subprocess.Popen(["uvicorn", "main:app", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000")

        page.fill("#a", "2")
        page.fill("#b", "3")
        page.click("#add-btn")
        
        result = page.text_content("#result")
        assert result == "5"
        browser.close()
