import pytest
from app import create_app
from extensions import db

@pytest.fixture(scope='session')
def app():

    app = create_app()
    
    with app.app_context():
        db.create_all()   # create tables in the test DB
    yield app
    


@pytest.fixture
def client(app):
    return app.test_client()
