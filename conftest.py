import pytest
import threading
import time
from wsgiref.simple_server import make_server
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' # Use in-memory DB for unit tests
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's CLI commands."""
    return app.test_cli_runner()

@pytest.fixture(scope="session")
def server():
    """Start the Flask server for the Playwright tests."""
    # Create an app specifically for the server
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:' # Use in-memory DB or file for E2E
        # Note: In-memory DB might be tricky with threads if not careful, 
        # but SQLite in-memory is shared if named or per connection. 
        # Safest for E2E with simple_server is a file that we can clean up, 
        # or just use in-memory if we can ensure the app instance is shared.
        # But make_server takes 'app', so it should be fine.
    })
    
    # We need to initialize the DB for the server context
    with app.app_context():
        db.create_all()

    port = 5001
    httpd = make_server('127.0.0.1', port, app)
    
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()
    
    time.sleep(1)
    
    yield f"http://127.0.0.1:{port}"
    
    httpd.shutdown()
    thread.join()
