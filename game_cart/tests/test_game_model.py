
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from game_cart.models.game_model import Games
from game_cart.db import db

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Create a new database session for each test.
    """
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    db.Model.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    db.session = session  # Mock the database session

    yield session  # Provide the test database session to tests
    
    session.rollback()
    session.close()
    db.Model.metadata.drop_all(bind=engine)  # Drop tables

@pytest.fixture
def sample_game1():
    return {
        "id": 1,
        "name": "Forza Horizon 5",
        "price": 59.99,
    }
    
@pytest.fixture
def sample_game2():
    return {
        "id": 2,
        "name": "Legend of Zelda: Tears of the Kingdom",
        "price": 39.99
    }


def test_create_game(test_db, sample_game1):
    
    Games.create_game(**sample_game1)
    all_games = test_db.query(Games).all()
    assert len(all_games) == 1
    assert all_games[0].name == "Forza Horizon 5"
    assert all_games[0].price == 59.99
    
def test_create_duplicate_game(test_db, sample_game1):
    Games.create_game(**sample_game1)
    
    #game with id... already exist
    with pytest.raises(ValueError, match="Game with id 1 already exists"):
        Games.create_game(**sample_game1)

    
def test_delete_game(test_db, sample_game1, sample_game2):
    Games.create_game(**sample_game1)
    Games.create_game(**sample_game2)
    
    #deleted the second game so now it should be length 1
    Games.delete_game(game_id=1)
    all_games = test_db.query(Games).all()
    assert len(all_games) == 1
    assert all_games[0].name == "Legend of Zelda: Tears of the Kingdom"
    assert all_games[0].price == 39.99
    

def test_delete_nonexisting_game():
    
    with pytest.raises(ValueError, match="Game with id 1 not found"):
        Games.delete_game(game_id=1)

def test_get_all_game():
    pass

def test_get_all_game_empty():
    pass
