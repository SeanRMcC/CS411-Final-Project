import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from game_cart.models.user_model import User
from game_cart.db import db

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Create a new database session for each test.
    """
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    db.Model.metadata.create_all(bind=engine)  
    session = TestingSessionLocal()
    db.session = session  

    yield session  
    
    session.rollback()
    session.close()
    db.Model.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user():
    return {
        "username": "testuser",
        "password": "securepassword123"
    }


##########################################################
# User Creation
##########################################################

def test_create_user(test_db, sample_user):
    """Test creating a new user with a unique username."""
    User.create_user(**sample_user)
    user = test_db.query(User).filter_by(username=sample_user["username"]).first()
    assert user is not None, "User should be created in the database."
    assert user.username == sample_user["username"], "Username should match the input."
    assert len(user.salt) == 32, "Salt should be 32 characters (hex)."
    assert len(user.password) == 64, "Password should be a 64-character SHA-256 hash."