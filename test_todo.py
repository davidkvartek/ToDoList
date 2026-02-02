import pytest
from playwright.sync_api import Page, expect

def test_add_todo(page: Page, server):
    """Test adding a new todo item."""
    page.goto(server)
    page.fill('input[name="todo"]', "Buy milk")
    page.click('button:has-text("Add")')
    expect(page.locator("ul")).to_contain_text("Buy milk")

def test_complete_todo(page: Page, server):
    """Test completing a todo item."""
    page.goto(server)
    page.fill('input[name="todo"]', "Walk the dog")
    page.click('button:has-text("Add")')
    
    # Locate the item
    item = page.locator("li").filter(has_text="Walk the dog")
    
    # Click Complete
    item.get_by_role("link", name="Complete").click()
    
    # Verify completed class
    expect(item).to_have_class("completed")
    
    # Verify link text changes to Undo
    expect(item.get_by_role("link", name="Undo")).to_be_visible()

def test_delete_todo(page: Page, server):
    """Test deleting a todo item."""
    page.goto(server)
    page.fill('input[name="todo"]', "Delete me")
    page.click('button:has-text("Add")')
    
    # Verify presence
    expect(page.locator("ul")).to_contain_text("Delete me")
    
    # Click Delete
    page.locator("li").filter(has_text="Delete me").get_by_role("link", name="Delete").click()
    
    # Verify absence
    expect(page.locator("ul")).not_to_contain_text("Delete me")
