
import pytest
from app import db, Todo

def test_home_page(client):
    """Test that the home page loads correctly."""
    # The error suggests the template might be using 'index' instead of 'main.index'
    response = client.get('/')
    assert response.status_code == 200
    assert b"To-Do List" in response.data

def test_add_todo(client, app):
    """Test adding a new todo item."""
    response = client.post('/', data={'todo': 'Test Item'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Item" in response.data
    
    with app.app_context():
        assert Todo.query.count() == 1
        assert Todo.query.first().title == 'Test Item'

def test_update_todo(client, app):
    """Test updating (completing) a todo item."""
    # Add an item first
    with app.app_context():
        todo = Todo(title="Update Me", complete=False)
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    # Call update route - ensure we use the correct URL
    # The blueprint prefix is not set, so it's just /update/...
    response = client.get(f'/update/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        updated_todo = db.session.get(Todo, todo_id)
        assert updated_todo.complete == True

def test_delete_todo(client, app):
    """Test deleting a todo item."""
    # Add an item first
    with app.app_context():
        todo = Todo(title="Delete Me")
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    # Call delete route
    response = client.get(f'/delete/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        assert db.session.get(Todo, todo_id) is None
