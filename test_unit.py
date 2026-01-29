
import pytest
from app import app, db, Todo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"To-Do List" in response.data

def test_add_todo(client):
    """Test adding a new todo item."""
    response = client.post('/', data={'todo': 'Test Item'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Item" in response.data
    
    with app.app_context():
        assert Todo.query.count() == 1
        assert Todo.query.first().title == 'Test Item'

def test_update_todo(client):
    """Test updating (completing) a todo item."""
    # Add an item first
    with app.app_context():
        todo = Todo(title="Update Me", complete=False)
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    # Call update route
    response = client.get(f'/update/{todo_id}', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        updated_todo = db.session.get(Todo, todo_id)
        assert updated_todo.complete == True

def test_delete_todo(client):
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
