import time
import pytest


@pytest.mark.e2e
def test_register_positive(page, fastapi_server):
    # Use a unique email to avoid duplicates across runs
    email = f"e2e_user_{int(time.time() * 1000)}@example.com"
    page.goto('http://127.0.0.1:8000/register')

    page.fill('input#email', email)
    page.fill('input#password', 'password123')
    page.fill('input#confirm', 'password123')
    page.click('button[type="submit"]')

    # Wait for message to be set by frontend
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert page.inner_text('#message') == 'Registration successful!'

    # Ensure token was stored
    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None and len(token) > 0


@pytest.mark.e2e
def test_register_short_password_shows_error(page, fastapi_server):
    page.goto('http://127.0.0.1:8000/register')
    page.fill('input#email', f"short_{int(time.time() * 1000)}@example.com")
    page.fill('input#password', 'short')
    page.fill('input#confirm', 'short')
    page.click('button[type="submit"]')

    # Frontend will show client-side validation message
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Password must be at least 8 characters' in page.inner_text('#message')

    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is None


@pytest.mark.e2e
def test_login_positive(page, fastapi_server):
    # Register then login using the same browser session
    email = f"login_user_{int(time.time() * 1000)}@example.com"
    # Register
    page.goto('http://127.0.0.1:8000/register')
    page.fill('input#email', email)
    page.fill('input#password', 'password123')
    page.fill('input#confirm', 'password123')
    page.click('button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Registration successful' in page.inner_text('#message')

    # Clear storage to simulate fresh login
    page.evaluate("() => localStorage.removeItem('access_token')")

    # Login
    page.goto('http://127.0.0.1:8000/login')
    page.fill('input#email', email)
    page.fill('input#password', 'password123')
    page.click('button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Login successful' in page.inner_text('#message')
    token = page.evaluate("() => localStorage.getItem('access_token')")
    assert token is not None and len(token) > 0


@pytest.mark.e2e
def test_login_wrong_password_shows_invalid(page, fastapi_server):
    # Register a user
    email = f"wrongpass_{int(time.time() * 1000)}@example.com"
    page.goto('http://127.0.0.1:8000/register')
    page.fill('input#email', email)
    page.fill('input#password', 'password123')
    page.fill('input#confirm', 'password123')
    page.click('button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Registration successful' in page.inner_text('#message')

    # Attempt login with wrong password
    page.goto('http://127.0.0.1:8000/login')
    page.fill('input#email', email)
    page.fill('input#password', 'wrongpass')
    page.click('button[type="submit"]')
    page.wait_for_function("() => document.querySelector('#message') && document.querySelector('#message').innerText.length > 0")
    assert 'Invalid credentials' in page.inner_text('#message')
