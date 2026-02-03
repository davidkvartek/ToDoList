import pytest
import re
from playwright.sync_api import Page, expect

def test_add_todo(page: Page, server):
    """Test adding a new todo item with priority and due date."""
    page.goto(server)
    
    page.fill('input[name="todo"]', "Buy milk")
    page.select_option('select[name="priority"]', "3") # High
    page.fill('input[name="due_date"]', "2024-12-31")
    
    page.click('button:has-text("Add")')
    
    # Verify content
    item = page.locator("li").filter(has_text="Buy milk")
    expect(item).to_be_visible()
    expect(item).to_contain_text("High")
    expect(item).to_contain_text("2024-12-31")

def test_sorting(page: Page, server):
    """Test that high priority items appear before low priority."""
    page.goto(server)
    
    # Add Low Priority Item
    page.fill('input[name="todo"]', "Low Priority Task")
    page.select_option('select[name="priority"]', "1")
    page.click('button:has-text("Add")')
    
    # Add High Priority Item
    page.fill('input[name="todo"]', "High Priority Task")
    page.select_option('select[name="priority"]', "3")
    page.click('button:has-text("Add")')
    
    # Verify High Priority is visible
    expect(page.locator("li").filter(has_text="High Priority Task")).to_be_visible()
    expect(page.locator("li").filter(has_text="Low Priority Task")).to_be_visible()
    
    # Check order
    # Note: "Buy milk" might exist from previous test (session scope)
    # We just need to ensure High Priority Task comes before Low Priority Task
    
    items = page.locator("li").all_text_contents()
    
    high_index = -1
    low_index = -1
    
    for i, text in enumerate(items):
        if "High Priority Task" in text:
            high_index = i
        if "Low Priority Task" in text:
            low_index = i
            
    assert high_index != -1, "High Priority Task not found"
    assert low_index != -1, "Low Priority Task not found"
    assert high_index < low_index, f"High ({high_index}) should be before Low ({low_index})"

def test_complete_todo(page: Page, server):
    """Test completing a todo item."""
    page.goto(server)
    page.fill('input[name="todo"]', "Walk the dog")
    page.click('button:has-text("Add")')
    
    item = page.locator("li").filter(has_text="Walk the dog")
    item.get_by_role("link", name="Complete").click()
    
    # Use re.compile explicitly
    expect(item).to_have_class(re.compile(r"completed"))

def test_delete_todo(page: Page, server):
    """Test deleting a todo item."""
    page.goto(server)
    page.fill('input[name="todo"]', "Delete me")
    page.click('button:has-text("Add")')
    
    expect(page.locator("ul")).to_contain_text("Delete me")
    
    page.locator("li").filter(has_text="Delete me").get_by_role("link", name="Delete").click()
    
    expect(page.locator("ul")).not_to_contain_text("Delete me")
