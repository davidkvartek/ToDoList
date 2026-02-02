import pytest
import threading
import time
from wsgiref.simple_server import make_server
from app import app, db

@pytest.fixture(scope="session", autouse=True)
def server():
    """Start the Flask server for the tests."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_todo.db'
    
    # Create test database
    with app.app_context():
        db.create_all()

    # Start the server in a separate thread
    port = 5001
    # app is the WSGI application
    httpd = make_server('127.0.0.1', port, app)
    
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    yield f"http://127.0.0.1:{port}"
    
    # Teardown
    httpd.shutdown()
    thread.join()
    
    # Cleanup database
    with app.app_context():
        db.drop_all()
