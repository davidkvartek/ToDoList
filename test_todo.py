# test_todo.py
import pytest
from playwright.sync_api import sync_playwright

def test_add_todo():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:5000")
        page.fill('input[name="todo"]', "Buy milk")
        page.click('button[type="submit"]')
        assert page.inner_text("ul") == "Buy milk"
        browser.close()
