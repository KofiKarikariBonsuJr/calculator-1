from playwright.sync_api import sync_playwright
import subprocess, time

def test_register_short_password():
    proc = subprocess.Popen(["uvicorn", "main:app", "--port", "8000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.5)
    try:
        with sync_playwright() as p:
            page = p.chromium.launch().new_page()
            page.goto("http://localhost:8000/register")
            page.fill("#username", "u2")
            page.fill("#email", "u2@example.com")
            page.fill("#password", "123")
            page.fill("#confirm", "123")
            page.click("#register-btn")
            # should show client-side warning
            assert "Password too short" in page.text_content("#msg")
    finally:
        proc.terminate()
