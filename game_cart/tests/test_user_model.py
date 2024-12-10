import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from game_cart.models.user_model import User
from game_cart.db import db

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Create a new database session for each test.
    """
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = scoped_session(sessionmaker(bind=engine))

    db.session = TestingSessionLocal
    db.Model.metadata.create_all(bind=engine)

    yield TestingSessionLocal
    
    TestingSessionLocal.remove()
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

def test_create_duplicate_user(test_db, sample_user):
    """Test attempting to create a user with a duplicate username."""
    User.create_user(**sample_user)
    with pytest.raises(ValueError, match="User with username 'testuser' already exists"):
        User.create_user(**sample_user)

##########################################################
# User Authentication
##########################################################

def test_check_password_correct(test_db, sample_user):
    """Test checking the correct password."""
    User.create_user(**sample_user)
    assert User.check_password(sample_user["username"], sample_user["password"]) is True, "Password should match."

def test_check_password_incorrect(test_db, sample_user):
    """Test checking an incorrect password."""
    User.create_user(**sample_user)
    assert User.check_password(sample_user["username"], "wrongpassword") is False, "Password should not match."

def test_check_password_user_not_found(test_db):
    """Test checking password for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.check_password("nonexistentuser", "password")

##########################################################
# Update Password
##########################################################

def test_update_password(test_db, sample_user):
    """Test updating the password for an existing user."""
    User.create_user(**sample_user)
    new_password = "newpassword456"
    User.update_password(sample_user["username"], new_password)
    assert User.check_password(sample_user["username"], new_password) is True, "Password should be updated successfully."

def test_update_password_user_not_found(test_db):
    """Test updating the password for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.update_password("nonexistentuser", "newpassword")
